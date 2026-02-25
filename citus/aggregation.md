---
title: Real-Time Event Aggregation at Scale Using PostgreSQL with Citus
description: Learn how to implement real-time event aggregation at scale by using PostgreSQL with Citus so you can efficiently process high-volume data.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Real-time event aggregation at scale by using PostgreSQL with Citus

(Copy of [original publication](https://www.citusdata.com/blog/2016/11/29/event-aggregation-at-scale-with-postgresql/))

> [!NOTE]  
> This article mentions the Citus Cloud service. You can no longer onboard to Citus Cloud on Amazon Web Service (AWS). If you're new to Citus, Citus is still available to you. Citus is now open source and in the cloud on Microsoft Azure, as a fully integrated deployment option in Azure Database for PostgreSQL.
>
> For more information, see [Managed service](citus-cloud.md).

Citus is commonly used to scale out event data pipelines on top of PostgreSQL. Its ability to transparently shard data and parallelize queries over many machines makes it possible to have real-time responsiveness even with terabytes of data. Users with high data volumes often store preaggregated data to avoid the cost of processing raw data at run-time. For large datasets, querying precomputed aggregation tables can be orders of magnitude faster than querying the facts table on demand.

To create aggregations for distributed tables, the latest version of Citus supports the `INSERT .. SELECT` syntax for tables that use the same distribution column. Citus automatically 'colocates' the shards of distributed tables such that the same distribution column value is always placed on the same worker node. You can now transfer data between tables as long as the distribution column value is preserved. A common way of taking advantage of colocation is to follow the multitenant data model and shard all tables by `tenant_id` or `customer_id`. Even without that model, as long as your tables share the same distribution column, you can use the `INSERT .. SELECT` syntax.

`INSERT .. SELECT` queries that can be pushed down to the workers are supported, which excludes some SQL functionality such as limits, and unions. The result is inserted into a colocated shard in the destination table. Therefore, you need to make sure that the distribution column (for example, tenant_id) is preserved in the aggregation and is included in joins. `INSERT .. SELECT` commands on distributed tables usually look like:

```sql
INSERT INTO aggregation_table (tenant_id, ...)
SELECT tenant_id, ... FROM facts_table ...
```

The following are steps of creating aggregations for a typical example of high-volume data: page views. Set up a [Citus Cloud](https://www.citusdata.com/product/cloud/) formation consisting of four workers with four cores each, and create a distributed facts table with several indexes:

```sql
CREATE TABLE page_views (
    tenant_id int,
    page_id int,
    host_ip inet,
    view_time timestamp default now()
);
CREATE INDEX view_tenant_idx ON page_views (tenant_id);
CREATE INDEX view_time_idx ON page_views USING BRIN (view_time);

SELECT create_distributed_table('page_views', 'tenant_id');
```

Next, generate 100 million rows of fake data (takes a few minutes) and load it into the database:

``` psql
\COPY (SELECT s % 307, (random()*5000)::int, '203.0.113.' || (s % 251), now() + random() * interval '60 seconds' FROM generate_series(1,100000000) s) TO '/tmp/views.csv' WITH CSV

\COPY page_views FROM '/tmp/views.csv' WITH CSV
```

You can now perform aggregations at run-time by performing a SQL query against the facts table:

```sql
-- Most views in the past week
SELECT page_id, count(*) AS view_count
FROM page_views
WHERE tenant_id = 5 AND view_time >= date '2016-11-23'
GROUP BY tenant_id, page_id
ORDER BY view_count DESC LIMIT 3;
 page_id | view_count
---------+------------
    2375 |         99
    4538 |         95
    1417 |         93
(3 rows)

Time: 269.125 ms
```

To improve, create a precomputed aggregation, which `tenant_id` also distributes. Citus automatically colocates the table with the `page_views` table:

```sql
CREATE TABLE daily_page_views (
    tenant_id int,
    day date,
    page_id int,
    view_count bigint,
    primary key (tenant_id, day, page_id)
);

SELECT create_distributed_table('daily_page_views', 'tenant_id');
```

You can now populate the aggregation by using a simple `INSERT..SELECT` command, which is parallelized across the cores in workers, processing around 10 million events per second and generating 1.7 million aggregates:

```sql
INSERT INTO daily_page_views (tenant_id, day, page_id, view_count)
  SELECT tenant_id, view_time::date AS day, page_id, count(*) AS view_count
  FROM page_views
  GROUP BY tenant_id, view_time::date, page_id;

INSERT 0 1690649

Time: 10649.870 ms
```

After creating the aggregation, you can get the results from the aggregation table in a fraction of the query time:

```sql
-- Most views in the past week
SELECT page_id, view_count
FROM daily_page_views
WHERE tenant_id = 5 AND day >= date '2016-11-23'
ORDER BY view_count DESC LIMIT 3;
 page_id | view_count
---------+------------
    2375 |         99
    4538 |         95
    1417 |         93
(3 rows)

Time: 4.528 ms
```

You typically want to keep aggregations up-to-date, even as the current day progresses. To keep your aggregations up-to-date, expand your original command to only consider new rows and updating existing rows to consider the new data by using [ON CONFLICT](https://www.postgresql.org/docs/current/static/sql-insert.html#SQL-ON-CONFLICT). If you insert data for a primary key (`tenant_id`, `day`, `page_id`) that already exists in the aggregation table, then the count is added instead.

```sql
INSERT INTO page_views VALUES (5, 10, '203.0.113.1');

INSERT INTO daily_page_views (tenant_id, day, page_id, view_count)
  SELECT tenant_id, view_time::date AS day, page_id, count(*) AS view_count
  FROM page_views
  WHERE view_time >= '2016-11-23 23:00:00' AND view_time < '2016-11-24 00:00:00'
  GROUP BY tenant_id, view_time::date, page_id
  ON CONFLICT (tenant_id, day, page_id) DO UPDATE SET
  view_count = daily_page_views.view_count + EXCLUDED.view_count;

INSERT 0 1

Time: 2787.081 ms
```

To regularly update the aggregation, you need to keep track of which rows in the facts table processed to avoid counting them more than once. A basic approach is to aggregate up to the current time, store the timestamp in a table, and continue from that timestamp on the next run. Consider that there might be in-flight requests with a lower timestamp, which is especially true when you use bulk ingestion through COPY. You therefore roll up to a timestamp that lies slightly in the past, with the assumption that requests finished. You can easily codify this logic into a PL/pgSQL function:

```sql
CREATE TABLE aggregations (name regclass primary key, last_update timestamp);
INSERT INTO aggregations VALUES ('daily_page_views', now());

CREATE OR REPLACE FUNCTION compute_daily_view_counts()
RETURNS void LANGUAGE plpgsql AS $function$
DECLARE
  start_time timestamp;
  end_time timestamp := now() - interval '1 minute'; -- exclude in-flight requests
BEGIN
  SELECT last_update INTO start_time FROM aggregations WHERE name = 'daily_page_views'::regclass;
  UPDATE aggregations SET last_update = end_time WHERE name = 'daily_page_views'::regclass;

  EXECUTE $$
    INSERT INTO daily_page_views (tenant_id, day, page_id, view_count)
      SELECT tenant_id, view_time::date AS day, page_id, count(*) AS view_count
      FROM page_views
      WHERE view_time >= $1 AND view_time < $2
      GROUP BY tenant_id, view_time::date, page_id
      ON CONFLICT (tenant_id, day, page_id) DO UPDATE SET
      view_count = daily_page_views.view_count + EXCLUDED.view_count$$
  USING start_time, end_time;
END;
$function$;
```

After creating the function, periodically call `SELECT compute_daily_view_counts()` to continuously update the aggregation with 1-2 minutes delay. More advanced approaches can bring down this delay to a few seconds.

This example uses a single, database-generated time column. However, it's better to distinguish between the time at which the event happened at the source and the database-generated ingestion time used to keep track of whether an event already processed.

Use a `page_id` instead of a URL in order to dodge the overhead of storing URLs for every page view to make your numbers look better. With Citus, you can often avoid the cost of denormalization in distributed databases that don't support joins. You can put the static details of a page inside another table and perform a join:

```sql
CREATE TABLE pages (
    tenant_id int,
    page_id int,
    url text,
    language varchar(2),
    primary key (tenant_id, page_id)
);

SELECT create_distributed_table('pages', 'tenant_id');

... insert pages ...

-- Most views in the past week
SELECT url, view_count
FROM daily_page_views JOIN pages USING (tenant_id, page_id)
WHERE tenant_id = 5 AND day >= date '2016-11-23'
ORDER BY view_count DESC LIMIT 3;
   url    | view_count
----------+------------
 /home    |         99
 /contact |         95
 /product |         93
(3 rows)

Time: 7.042 ms
```

You can also perform joins in the `INSERT..SELECT` command, allowing you to create more detailed aggregations, for example, by language.

Distributed aggregation adds another tool to Citus' broad tool chest in dealing with big data problems. With parallel `INSERT .. SELECT`, parallel indexing, parallel querying, and many other features, Citus can't only horizontally scale your multitenant database, but can also unify many different parts of your data pipeline into one platform.

## Related content

- [Guides overview](guides.md)
- [What is Citus?](what-is-citus.md)
