---
title: Sharding PostgreSQL with Semi-Structured Data and Its Performance Implications
description: Learn how to shard PostgreSQL with semi-structured data by using Citus so you can optimize performance and scalability.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Shard PostgreSQL with semi-structured data and its performance implications

(Copy of [original publication](https://www.citusdata.com/blog/2016/07/25/sharding-json-in-postgres-and-performance/))

Citus can help you move beyond a single node database. In cases where your data is still under 100 GB, a single PostgreSQL instance works well. At larger levels, Citus can help, but how you model your data affects your system's performance.

Some applications fit naturally in a scaled out model, but others require changes in your application. The model you choose determines the queries you're able to run in a performant manner. You can approach this situation in two ways:

- Verifying how your data might already be modeled today.
- Examining the queries you're looking to run and their performance needs to inform which data model might make the most sense.

## One large table, without joins

Storing semi-structured data in JSONB helps reduce the number of tables required, which improves scalability. For example, web analytics data traditionally stores a table of events with minimal information and uses lookup tables to refer to the events and record extra information. Some events have more associated information than others. By replacing the lookup tables by a JSONB column, you can query and filter while still having great performance. For example:

```sql
CREATE TABLE visits AS (
  id UUID,
  site_id uuid,
  visited_at TIMESTAMPTZ,
  session_id UUID,
  page TEXT,
  url_params JSONB
)
```

URL parameters for an event are open-ended, and no parameters are guaranteed. The common "utm" parameters, such as `utm_source`, `utm_medium`, `utm_campaign`, aren't universal. A [JSONB](https://www.citusdata.com/blog/2016/07/14/choosing-nosql-hstore-json-jsonb/) column for `url_params` is more convenient than creating columns for each parameter. With JSONB, you can get both the flexibility of schema, and, combined with [GIN indexing](https://www.postgresql.org/docs/current/static/gin.html). You can still have performant queries against all keys and values without having to index them individually.

## How Citus supports scaling

Assuming you do need to scale beyond a single node, [Citus](https://www.citusdata.com/product/) can help at scaling out your processing power, memory, and storage. In the early stages of utilizing Citus, you create your schema, then tell the system how you wish to shard your data.

In order to determine the ideal sharding key, you need to examine the query load and types of operations that you're looking to perform. If you're storing aggregated data and all of your queries are per customer, then a shard key such as `customer_id` or `tenant_id` can be a great choice. Even if you have minutely rollups, and need to report on a daily basis, this process works well. You can route queries to shards just for that customer. As a result of routing queries to a single shard, you can allow for a higher concurrency.

In the case where you're storing raw data, there's a large amount of data per customer. This situation can be more difficult to get a subsecond response without further parallelizing queries per customer. You might also find it difficult to get predictable subsecond responsiveness if you have a low number of customers or if 80% of your data comes from one customer. In these cases, picking a shard key that's more granular than customer or tenant ID can be ideal.

The distribution of your data and query workload is what heavily determines which key is right for you.

With the previous example, if all of your sites have the same amount of traffic, then `site_id` might be reasonable. However, if either of the above cases is true, then something like `session_id` is a more ideal distribution key.

## The query workload

With a sharding key of `session_id`, you can easily perform many queries such as:

Top page views over the last seven days for a given site:

```sql
SELECT page,
       count(*)
FROM visits
WHERE site_id = 'foo'
  AND visited_at > now() - '7 days'::interval
GROUP BY page
ORDER BY 2 DESC;
```

Unique sessions today:

```sql
SELECT distinct(session_id)
FROM visits
WHERE site_id = 'foo'
  AND visited_at > date_trunc('date', now())
```

If you have an index on `url_params`, you can easily do various rollups, such as finding the campaigns that drove the most traffic to you over the past 30 days and which pages received the most benefit:

```sql
SELECT url_params ->> 'utm_campaign',
       page,
       count(*)
FROM visits
WHERE url_params ? 'utm_campaign'
  AND visited_at >= now() - '30 days'::interval
  AND site_id = 'foo'
GROUP BY url_params ->> 'utm_campaign',
         page
ORDER BY 3 DESC;
```

## Optimizing distribution

If you're optimizing for the parallelism out of your database, then matching your cores to the number of shards ensures that every query takes advantage of your resources. In contrast, if you're optimizing for higher read concurrency, then allowing queries to run against only a single shard allows more queries to run at once, although each individual query experiences less parallelism.


:::moniker range=">=citus-14"

## JSON_TABLE() with COLUMNS (PostgreSQL 18)

PostgreSQL 18 expands SQL/JSON with `JSON_TABLE(... COLUMNS ...)`, letting you extract multiple typed fields from JSON documents in one pass. Citus 14 supports this syntax end-to-end in distributed queries.

```sql
CREATE TABLE pg18_json_test (id serial PRIMARY KEY, data json);
SELECT create_distributed_table('pg18_json_test', 'id');

INSERT INTO pg18_json_test (data) VALUES
  ('{"user": {"name": "Alice",   "age": 30, "city": "San Diego"}}'),
  ('{"user": {"name": "Bob",     "age": 25, "city": "Los Angeles"}}'),
  ('{"user": {"name": "Charlie", "age": 35, "city": "Los Angeles"}}');

SELECT jt.name, jt.age
FROM pg18_json_test,
     JSON_TABLE(
       data,
       '$.user'
       COLUMNS (
         age  INT  PATH '$.age',
         name TEXT PATH '$.name'
       )
     ) AS jt
WHERE jt.age BETWEEN 25 AND 35
ORDER BY jt.age, jt.name;
```

:::moniker-end

## Related content

- [Guides overview](guides.md)
- [Scalable real-time product search](faceted-search.md)
