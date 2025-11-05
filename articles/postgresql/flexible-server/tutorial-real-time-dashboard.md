---
title: 'Tutorial: Real-time dashboard with elastic clusters'
description: This tutorial shows how to parallelize real-time dashboard queries with elastic clusters on Azure Database for PostgreSQL.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: tutorial
#Customer intent: As a developer, I want to parallelize queries so that I can make a real-time dashboard application.
---

# Tutorial: Design a real-time analytics dashboard with elastic clusters

In this tutorial, you use elastic clusters on Azure Database for PostgreSQL elastic clusters to learn how to design a real-time dashboard and parallelize queries.

> [!div class="checklist"]
> * Prerequisites
> * Use psql utility to create a schema
> * Shard tables across nodes
> * Generate sample data
> * Perform rollups
> * Query raw and aggregated data
> * Expire data

## Prerequisites

Create an elastic cluster in one of the following ways:
- [Create an elastic cluster using the Portal](quickstart-create-elastic-cluster-portal.md)
- [Create an elastic cluster using Bicep](quickstart-create-elastic-cluster-bicep.md)
- [Create an elastic cluster with ARM template](quickstart-create-elastic-cluster-arm-template.md)

## Use psql utility to create a schema

Once connected to the elastic cluster using psql, you can configure your elastic cluster. This tutorial walks you through ingesting traffic data from web analytics, then rolling up the data to provide real-time dashboards based on that data.

Let's create a table that consumes all of our raw web traffic data. Run the following commands in the psql terminal:

```sql
CREATE TABLE http_request (
  site_id INT,
  ingest_time TIMESTAMPTZ DEFAULT now(),

  url TEXT,
  request_country TEXT,
  ip_address TEXT,

  status_code INT,
  response_time_msec INT
);
```

We're also going to create a table that holds our per-minute aggregates, and a table that maintains the position of our last rollup. Run the following commands in psql as well:

```sql
CREATE TABLE http_request_1min (
  site_id INT,
  ingest_time TIMESTAMPTZ, -- which minute this row represents

  error_count INT,
  success_count INT,
  request_count INT,
  average_response_time_msec INT,
  CHECK (request_count = error_count + success_count),
  CHECK (ingest_time = date_trunc('minute', ingest_time))
);

CREATE INDEX http_request_1min_idx ON http_request_1min (site_id, ingest_time);

CREATE TABLE latest_rollup (
  minute timestamptz PRIMARY KEY,

  CHECK (minute = date_trunc('minute', minute))
);
```

You can see the newly created tables in the list of tables now with this psql command:

```postgres
\dt
```

## Shard tables across nodes

An elastic cluster deployment stores table rows on different nodes based on the value of a user-designated column. This "distribution column" marks how data is sharded across nodes.

Let's set the distribution column (shard key) to be site_id. In psql, run these functions:

  ```sql
SELECT create_distributed_table('http_request',      'site_id');
SELECT create_distributed_table('http_request_1min', 'site_id');
```

> [!NOTE]
>
> Distributing tables or using schema-based sharding is necessary to take advantage of elastic clusters of Azure Database for PostgreSQL performance features. Until you distribute tables or schemas, your cluster nodes will not run distributed queries involving their data.

## Generate sample data

Now our cluster should be ready to ingest some data. We can run the following locally from our `psql` connection to continuously insert data.

```sql
DO $$
  BEGIN LOOP
    INSERT INTO http_request (
      site_id, ingest_time, url, request_country,
      ip_address, status_code, response_time_msec
    ) VALUES (
      trunc(random()*32), clock_timestamp(),
      concat('http://example.com/', md5(random()::text)),
      ('{China,India,USA,Indonesia}'::text[])[ceil(random()*4)],
      concat(
        trunc(random()*250 + 2), '.',
        trunc(random()*250 + 2), '.',
        trunc(random()*250 + 2), '.',
        trunc(random()*250 + 2)
      )::inet,
      ('{200,404}'::int[])[ceil(random()*2)],
      5+trunc(random()*150)
    );
    COMMIT;
    PERFORM pg_sleep(random() * 0.25);
  END LOOP;
END $$;
```

The query inserts approximately eight rows every second. The rows are stored on different worker nodes based upon their distribution column, `site_id`.

   > [!NOTE]
   > Leave the data generation query running, and open a second psql
   > connection for the remaining commands in this tutorial.
   >

## Query

Azure Database for PostgreSQL  elastic clusters allows multiple nodes to process queries in parallel for speed. For instance, the database calculates aggregates like SUM and COUNT on worker nodes, and combines the results into a final answer.

Here's a query to count web requests per minute along with a few statistics. Try running it in psql and observe the results.

```sql
SELECT
  site_id,
  date_trunc('minute', ingest_time) AS minute,
  COUNT(1) AS request_count,
  SUM(CASE WHEN (status_code between 200 and 299) THEN 1 ELSE 0 END) AS success_count,
  SUM(CASE WHEN (status_code between 200 and 299) THEN 0 ELSE 1 END) AS error_count,
  SUM(response_time_msec) / COUNT(1) AS average_response_time_msec
FROM http_request
WHERE date_trunc('minute', ingest_time) > now() - '5 minutes'::interval
GROUP BY site_id, minute
ORDER BY minute ASC;
```

## Rolling up data

The previous query works fine in the early stages, but its performance degrades as your data scales. Even with distributed processing, it's faster to precompute the data than to recalculate it repeatedly.

We can ensure our dashboard stays fast by regularly rolling up the raw data into an aggregate table. You can experiment with the aggregation duration. We used a per-minute aggregation table, but you could break data into 5, 15, or 60 minutes instead.

To run this roll-up more easily, we're going to put it into a plpgsql function. Run these commands in psql to create the `rollup_http_request` function.

```sql
-- initialize to a time long ago
INSERT INTO latest_rollup VALUES ('10-10-1901');

-- function to do the rollup
CREATE OR REPLACE FUNCTION rollup_http_request() RETURNS void AS $$
DECLARE
  curr_rollup_time timestamptz := date_trunc('minute', now());
  last_rollup_time timestamptz := minute from latest_rollup;
BEGIN
  INSERT INTO http_request_1min (
    site_id, ingest_time, request_count,
    success_count, error_count, average_response_time_msec
  ) SELECT
    site_id,
    date_trunc('minute', ingest_time),
    COUNT(1) AS request_count,
    SUM(CASE WHEN (status_code between 200 and 299) THEN 1 ELSE 0 END) AS success_count,
    SUM(CASE WHEN (status_code between 200 and 299) THEN 0 ELSE 1 END) AS error_count,
    SUM(response_time_msec) / COUNT(1) AS average_response_time_msec
  FROM http_request
  -- roll up only data new since last_rollup_time
  WHERE date_trunc('minute', ingest_time) <@
          tstzrange(last_rollup_time, curr_rollup_time, '(]')
  GROUP BY 1, 2;

  -- update the value in latest_rollup so that next time we run the
  -- rollup it will operate on data newer than curr_rollup_time
  UPDATE latest_rollup SET minute = curr_rollup_time;
END;
$$ LANGUAGE plpgsql;
```

With our function in place, execute it to roll up the data:

```sql
SELECT rollup_http_request();
```

And with our data in a preaggregated form we can query the rollup table to get the same report as earlier. Run the following query:

```sql
SELECT site_id, ingest_time AS minute, request_count,
       success_count, error_count, average_response_time_msec
FROM http_request_1min
WHERE ingest_time > date_trunc('minute', now()) - '5 minutes'::interval;
 ```

## Expiring old data

The rollups make queries faster, but we still need to expire old data to avoid unbounded storage costs. Decide how long you’d like to keep data for each granularity, and use standard queries to delete expired data. In the following example, we decided to keep raw data for one day, and per-minute aggregations for one month:

```sql
DELETE FROM http_request WHERE ingest_time < now() - interval '1 day';
DELETE FROM http_request_1min WHERE ingest_time < now() - interval '1 month';
```

In production, you could wrap these queries in a function and call it every minute in a cron job.

## Next step

In this tutorial, you learned how to create an elastic cluster. You connected to it with psql, created a schema, and distributed data. You learned to query data in the raw form, regularly aggregate that data, query the aggregated tables, and expire old data.

> [!div class="nextstepaction"]
> [Learn more about elastic clusters](concepts-elastic-clusters.md)