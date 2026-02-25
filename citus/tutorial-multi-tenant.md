---
title: Multitenant Applications
description: End-to-end guide to modeling, distributing, and operating multitenant SaaS workloads on Citus.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: tutorial
monikerRange: "citus-13 || citus-14"
---

# Multitenant applications

This unified guide combines the former conceptual ("multitenant") and tutorial ("tutorial-multi-tenant") documents into a single end-to-end resource. You learn how to (1) model and distribute a SaaS schema, (2) load and query data efficiently, and (3) operate at scale. Operating at scale includes schema changes, shared data, rebalancing, tenant isolation, and JSONB customization.

> [!NOTE]  
> This article assumes you have a Citus cluster (elastic clusters on Azure Database for PostgreSQL, or self-managed) and psql access to the coordinator. See [Getting Started](getting-started.md) if you still need a local setup.

## 1. Understand the pattern

Multitenant SaaS apps store many customers' (tenants') data in a shared database while providing each tenant an isolated view. Citus lets you keep normal PostgreSQL semantics—schemas, joins, constraints, transactions—while horizontally scaling by sharding tables across worker nodes.

Key goals:

| Goal | How Citus Helps |
| --- | --- |
| Fast per-tenant OLTP and analytics | Colocated tenant data on one node avoids cross-node chatter. |
| Operational simplicity | Single logical PostgreSQL endpoint; standard SQL and drivers. |
| Elastic growth | Add nodes; rebalance shards online. |
| Handle tenant skew | Isolate large tenants to dedicated shards and nodes. |
| Custom per-tenant fields | JSONB (and partial/GIN indexes) per tenant. |

## 2. Sample ad analytics schema

Use an ad analytics workload (companies → campaigns → ads plus select and impression fact tables). Initial single-node style schema (simplified) before distribution tweaks:

```sql
CREATE TABLE companies (
  id bigserial PRIMARY KEY,
  name text NOT NULL,
  image_url text,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
CREATE TABLE campaigns (
  id bigserial PRIMARY KEY,
  company_id bigint REFERENCES companies(id),
  name text NOT NULL,
  cost_model text NOT NULL,
  state text NOT NULL,
  monthly_budget bigint,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
CREATE TABLE ads (
  id bigserial PRIMARY KEY,
  campaign_id bigint REFERENCES campaigns(id),
  name text NOT NULL,
  image_url text,
  target_url text,
  impressions_count bigint DEFAULT 0,
  clicks_count bigint DEFAULT 0,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
```

### Distribution principle

Choose one tenant identifier (here `company_id`) and ensure every table either: (a) has that column directly, or (b) can join through a chain of foreign keys that includes it. For stronger constraints and routing performance, embed the distribution column in composite primary key and foreign key pairs.

## 3. Make the schema distribution-friendly

Adapt tables so primary and foreign keys include `company_id` (or equivalent). Here's an example of the final form for a fact table:

```postgresql
CREATE TABLE ads (
  id bigserial,
  company_id bigint,
  campaign_id bigint,
  name text NOT NULL,
  image_url text,
  target_url text,
  impressions_count bigint DEFAULT 0,
  clicks_count bigint DEFAULT 0,
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL,
  PRIMARY KEY (company_id, id),
  FOREIGN KEY (company_id, campaign_id) REFERENCES campaigns(company_id, id)
);
```

Repeat this process for other tables (see the original conceptual example) so every distributed join and constraint are local to one worker for a given tenant value.

## 4. Create and distribute tables

Connect to the coordinator (native install: port 9700; Docker example shown):

```bash
docker exec -it citus psql -U postgres
```

Create the adapted tables, then shard them:

```postgresql
SELECT create_distributed_table('companies',   'id');        -- small dimension; distributing by id ok
SELECT create_distributed_table('campaigns',   'company_id');
SELECT create_distributed_table('ads',         'company_id');
SELECT create_distributed_table('clicks',      'company_id');
SELECT create_distributed_table('impressions', 'company_id');
```

Why mix `id` for `companies` and `company_id` elsewhere? The company row count is modest, and using the primary key avoids extra denormalization. Downstream tables still colocate via `company_id`.

## 5. Load sample data

Download CSVs:

```bash
for f in companies campaigns ads clicks impressions geo_ips; do \
  curl -O https://examples.citusdata.com/mt_ref_arch/${f}.csv; \
done
```

If you're using Docker, copy them in:

```bash
for f in companies campaigns ads clicks impressions geo_ips; do \
  docker cp ${f}.csv citus:. ; \
done
```

In psql:

```psql
\copy companies   from 'companies.csv'   with csv
\copy campaigns   from 'campaigns.csv'   with csv
\copy ads         from 'ads.csv'         with csv
\copy clicks      from 'clicks.csv'      with csv
\copy impressions from 'impressions.csv' with csv
```

## 6. Per-tenant queries and transactions

Queries with `WHERE company_id = ?` (and constrained joins) route to one worker. All SQL features, such as joins, window functions, and transactions, remain available:

```sql
SELECT name, cost_model, state, monthly_budget
FROM campaigns
WHERE company_id = 5
ORDER BY monthly_budget DESC
LIMIT 10;

UPDATE campaigns
SET monthly_budget = monthly_budget - 2
WHERE company_id = 5;

BEGIN;
UPDATE campaigns SET monthly_budget = monthly_budget + 1000 WHERE company_id = 5 AND id = 40;
UPDATE campaigns SET monthly_budget = monthly_budget - 1000 WHERE company_id = 5 AND id = 41;
COMMIT;
```

### Distributed functions (reduce round trips)

Wrap multi-statement per-tenant work in a function and mark it distributed:

```postgresql
CREATE OR REPLACE FUNCTION delete_campaign(company_id int, campaign_id int)
RETURNS void LANGUAGE plpgsql AS $fn$
BEGIN
  DELETE FROM ads       WHERE campaign_id = delete_campaign.campaign_id AND company_id = delete_campaign.company_id;
  DELETE FROM campaigns WHERE id = campaign_id AND company_id = delete_campaign.company_id;
END; $fn$;

SELECT create_distributed_function('delete_campaign(int,int)', 'company_id', colocate_with := 'campaigns');
SELECT delete_campaign(5, 46);
```

### Rich analytics example

```sql
SELECT a.campaign_id,
       RANK() OVER (PARTITION BY a.campaign_id ORDER BY count(*) DESC) AS rnk,
       count(*) AS n_impressions,
       a.id
FROM ads a
JOIN impressions i
  ON i.company_id = a.company_id
 AND i.ad_id      = a.id
WHERE a.company_id = 5
GROUP BY a.campaign_id, a.id
ORDER BY a.campaign_id, n_impressions DESC;
```

## 7. Shared (reference) tables

Some lookup data should be present for every tenant without duplication. Use reference tables so each worker has a synchronized full copy:

```postgresql
CREATE TABLE geo_ips (
  addrs cidr PRIMARY KEY,
  latlon point NOT NULL CHECK (-90 <= latlon[0] AND latlon[0] <= 90 AND -180 <= latlon[1] AND latlon[1] <= 180)
);
CREATE INDEX ON geo_ips USING gist(addrs inet_ops);
SELECT create_reference_table('geo_ips');
\copy geo_ips from 'geo_ips.csv' with csv
```

Query (per-tenant join remains local because lookup is replicated):

```sql
SELECT c.id, clicked_at, latlon
FROM geo_ips, clicks c
WHERE addrs >> c.user_ip
  AND c.company_id = 5
  AND c.ad_id = 290;
```

## 8. Online schema changes

DDL issued on the coordinator propagates atomically (2PC) to workers:

```sql
ALTER TABLE ads ADD COLUMN caption text;
```

See [Creating and Modifying Distributed Objects (DDL)](reference-ddl.md) for details and limitations.

## 9. Per-tenant customization with JSONB

Store variable attributes in JSONB and index selectively:

```sql
SELECT user_data->>'is_mobile' AS is_mobile, count(*)
FROM clicks
WHERE company_id = 5
GROUP BY user_data->>'is_mobile'
ORDER BY count DESC;

CREATE INDEX click_user_data_is_mobile ON clicks ((user_data->>'is_mobile')) WHERE company_id = 5;
CREATE INDEX click_user_data ON clicks USING gin(user_data);
```

## 10. Scaling out and rebalancing

Add a worker node (portal or `citus_add_node`), and then rebalance shards:

```postgresql
SELECT citus_rebalance_start();
```

Reads continue during rebalancing. Depending on the edition and version, writes to moving shards might block briefly (community) or proceed (cloud article or recent versions).

## 11. Handling large (hot) tenants

Skew is often Zipfian: a few tenants dominate size and traffic. Isolate a large tenant to its own shard (and optionally node):

```sql
SELECT isolate_tenant_to_new_shard('companies', 5, 'CASCADE') AS shard_id;  -- returns shard id
```

Then move that shard (and cascaded siblings) to a chosen node. Ensure `wal_level >= logical`:

```sql
SELECT citus_move_shard_placement(
  <shard_id>,
  'source_host', source_port,
  'dest_host',   dest_port
);
```

Verify via `pg_dist_placement` queries.

## 12. Next steps

You've built a multitenant application on Citus that scales horizontally, supports rich SQL semantics, and handles tenant isolation. Continue your journey by exploring migration guides, framework integrations, and advanced operational patterns:

- Migrate an existing schema: [Identify Distribution Strategy](migrate/migration-schema.md).
- Add framework integration: [Django](https://docs.citusdata.com/en/v8.1/develop/migration_mt_django.html) or [ASP.NET](getting-started.md).
- Use [Citus Utility Functions](api-udf.md) for functions like `isolate_tenant_to_new_shard`.
- Try on Azure: [Elastic clusters on Azure Database for PostgreSQL Flexible server](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-horizontal-scaling-with-elastic-clusters-on-azure-database-for-postgres/4303508).

This article replaces prior separate conceptual and tutorial pages.

## Related content

- [Analytics and dashboards tutorial](tutorial-analytics.md)
- [Time-series data tutorial](tutorial-time-series.md)
- [What is Citus?](what-is-citus.md)
