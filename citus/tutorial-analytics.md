---
title: Analytics & Dashboards
description: Unified guide to modeling, ingesting, aggregating, and querying real-time events & time-series data with Citus.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: tutorial
monikerRange: "citus-13 || citus-14"
---

# Analytics and dashboards

This unified guide shows how to: (1) model and distribute event streams, (2) ingest at scale, (3) run low-latency analytics, (4) roll up and expire data, (5) apply approximate distinct counting (HLL), and (6) incorporate semi-structured JSONB.

> [!NOTE]  
> This article assumes you have a running Citus cluster (elastic clusters on Azure Database for PostgreSQL, or self-managed) and psql access. See [Getting Started](getting-started.md) if you still need a local setup.

## 1. Use case and architecture

Real-time dashboards need fast slice and trend queries over recent events while retaining longer-term history efficiently. Typical requirements:

| Requirement | Challenge | Citus Approach |
| --- | --- | --- |
| Low-latency per-minute metrics | High ingest + frequent aggregations | Per-tenant/partition hash sharding & local aggregation |
| Time-window graphs (minutes→years) | Rescan large raw tables | Preaggregated rollup tables (multi granularity) |
| Cost control | Raw events grow unbounded | Retention windows + rollups + partitioning |
| Distinct counts (visitors/IPs) | Exact counting expensive | Probabilistic HLL sketches |
| Semi-structured attributes | Schema churn & sparse columns | JSONB with selective indexing |

This article shows two example domains that map to the same design: HTTP request telemetry and GitHub events. Substitute your own eventstream and dimensions.

## 2. Base event model

Example: GitHub-like event firehose (subset). Two core tables: users and events.

```sql
CREATE TABLE github_users (
  user_id bigint PRIMARY KEY,
  url text,
  login text,
  avatar_url text,
  gravatar_id text,
  display_login text
);

CREATE TABLE github_events (
  event_id bigint,
  event_type text,
  event_public boolean,
  repo_id bigint,
  payload jsonb,
  repo jsonb,
  user_id bigint,
  org jsonb,
  created_at timestamp
);

CREATE INDEX event_type_index ON github_events (event_type);
CREATE INDEX payload_index ON github_events USING GIN (payload jsonb_path_ops);
```

### Choose a distribution column

Pick a column with high cardinality, balanced access, and frequent filter predicates (here `user_id`). Distribute both tables on it to colocate joins and rollups:

```sql
SELECT create_distributed_table('github_users',  'user_id');
SELECT create_distributed_table('github_events', 'user_id');
```

### Alternate: HTTP request stream

For per-site dashboards, use `site_id` instead:

```sql
CREATE TABLE http_request (
  site_id INT,
  ingest_time timestamptz DEFAULT now(),
  url text,
  request_region text,
  ip_address text,
  status_code int,
  response_time_msec int
);
SELECT create_distributed_table('http_request', 'site_id');
```

## 3. Loading data

Sample CSV ingestion (GitHub example):

```psql
\copy github_users  from 'users.csv'  with csv
\copy github_events from 'events.csv' with csv
```

## 4. Immediate querying (raw layer)

```sql
-- count users
SELECT count(*) FROM github_users;

-- commits per minute (PushEvent)
SELECT date_trunc('minute', created_at) AS minute,
       sum((payload->>'distinct_size')::int) AS num_commits
FROM github_events
WHERE event_type = 'PushEvent'
GROUP BY minute
ORDER BY minute;

-- top repo creators
SELECT login, count(*)
FROM github_events ge
JOIN github_users  gu USING (user_id)
WHERE event_type = 'CreateEvent'
  AND payload @> '{"ref_type":"repository"}'
GROUP BY login
ORDER BY count(*) DESC
LIMIT 10;
```

## 5. Rollup design (performance layer)

Motivation: dashboards repeatedly rescan raw events for time buckets. Introduce 1‑minute (and optionally 1‑hour or 1‑day) rollup tables keyed by same distribution column and time bucket.

HTTP example rollup (per minute):

```sql
CREATE TABLE http_request_1min (
  site_id INT,
  ingest_time timestamptz, -- truncated minute
  error_count INT,
  success_count INT,
  request_count INT,
  average_response_time_msec INT,
  CHECK (request_count = error_count + success_count),
  CHECK (ingest_time = date_trunc('minute', ingest_time))
);
SELECT create_distributed_table('http_request_1min', 'site_id');
CREATE INDEX ON http_request_1min (site_id, ingest_time);
```

### Rollup function

```plpgsql
CREATE TABLE latest_rollup (
  minute timestamptz PRIMARY KEY CHECK (minute = date_trunc('minute', minute))
);
INSERT INTO latest_rollup VALUES ('1901-01-01');

CREATE OR REPLACE FUNCTION rollup_http_request() RETURNS void LANGUAGE plpgsql AS $$
DECLARE
  curr_rollup_time timestamptz := date_trunc('minute', now() - interval '1 minute');
  last_rollup_time timestamptz := minute FROM latest_rollup;
BEGIN
  INSERT INTO http_request_1min (
    site_id, ingest_time, request_count,
    success_count, error_count, average_response_time_msec
  )
  SELECT site_id,
         date_trunc('minute', ingest_time),
         COUNT(*) request_count,
         SUM(CASE WHEN status_code BETWEEN 200 AND 299 THEN 1 ELSE 0 END) success_count,
         SUM(CASE WHEN status_code BETWEEN 200 AND 299 THEN 0 ELSE 1 END) error_count,
         SUM(response_time_msec) / COUNT(*) average_response_time_msec
  FROM http_request
  WHERE ingest_time <@ tstzrange(last_rollup_time, curr_rollup_time, '(]')
  GROUP BY 1,2;

  UPDATE latest_rollup SET minute = curr_rollup_time;
END;$$;
```

Schedule every minute (cron or `pg_cron`).

### Dashboard query (rollup layer)

```sql
SELECT site_id, ingest_time AS minute, request_count,
       success_count, error_count, average_response_time_msec
FROM http_request_1min
WHERE ingest_time > date_trunc('minute', now()) - interval '5 minutes';
```

## 6. Data retention and partitioning

Apply TTL policies to limit Azure Storage:

```sql
DELETE FROM http_request      WHERE ingest_time < now() - interval '1 day';
DELETE FROM http_request_1min WHERE ingest_time < now() - interval '1 month';
```

For faster purges, layer native range partitioning on `ingest_time` on top of Citus hash sharding (see `timeseries`).

## 7. Approximate distinct counts (HLL)

Install or enable HLL (already available in Azure Storage managed service):

```sql
CREATE EXTENSION IF NOT EXISTS hll;
ALTER TABLE http_request_1min ADD COLUMN distinct_ip_addresses hll;
```

Extend rollup `INSERT` with:

```sql
 , hll_add_agg(hll_hash_text(ip_address)) AS distinct_ip_addresses
```

Query distinct across interval:

```sql
SELECT hll_cardinality(hll_union_agg(distinct_ip_addresses)) AS unique_ips
FROM http_request_1min
WHERE ingest_time > now() - interval '5 minutes';
```

## 8. Semi-structured aggregations (JSONB)

Add flexible region counts:

```sql
ALTER TABLE http_request_1min ADD COLUMN region_counters jsonb;
```

Augment rollup (window + jsonb_object_agg):

```sql
 , jsonb_object_agg(request_region, region_count) AS region_counters
FROM (
  SELECT *, count(*) OVER (
    PARTITION BY site_id, date_trunc('minute', ingest_time), request_region
  ) AS region_count
  FROM http_request
) h
```

Dashboard extract example:

```sql
SELECT request_count,
       success_count,
       error_count,
       average_response_time_msec,
       COALESCE(region_counters->>'USA','0')::int AS us_visitors
FROM http_request_1min
WHERE ingest_time > now() - interval '5 minutes';
```

## 9. Maintenance and operations

| Task | Notes |
| --- | --- |
| Shard Rebalancing | Run `SELECT citus_rebalance_start();` after adding workers. |
| Schema Evolution | Standard DDL on coordinator propagates. Keep rollup code in a versioned function. |
| Monitoring | Tracks ingest lag (now - latest_rollup.minute). |
| Backfill | Temporarily widen rollup window; disable cron overlap. |
| Large Tenants / Hot Keys | Consider secondary sharding or isolating via `isolate_tenant_to_new_shard` if single key dominates. |

## 10. Related content

- [Tutorial: Time-series data](tutorial-time-series.md)
- [Tutorial: Multi-tenant applications](tutorial-multi-tenant.md)
- [What is Citus?](what-is-citus.md)
