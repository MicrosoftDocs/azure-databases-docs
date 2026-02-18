---
title: PostgreSQL Parallel Indexing in Citus
description: Learn how to use parallel indexing in Citus with PostgreSQL so you can create indexes faster on large datasets.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# PostgreSQL Parallel Indexing in Citus

(Copy of [original publication](https://www.citusdata.com/blog/2017/01/17/parallel-indexing-with-citus/))

Indexes are an essential tool for optimizing database performance and are becoming ever more important with big data. However, as the volume of data increases, index maintenance often becomes a write bottleneck, especially for [advanced index types](https://www.postgresql.org/docs/current/static/textsearch-indexes.html). These types use CPU time for every row that gets written. Index creation might also become prohibitively expensive as it might take hours or even days to build a new index on terabytes of data in PostgreSQL. Citus makes creating and maintaining indexes faster through parallelization.

Citus can be used to distribute PostgreSQL tables across many machines. One advantage of Citus is that you can keep adding more machines with more CPUs, so you can keep increasing your write capacity. You can increase your write capacity even if indexes are becoming the bottleneck. Citus allows `CREATE INDEX` to be performed in a massively parallel fashion, allowing fast index creation on large tables. Moreover, the [COPY command](https://www.postgresql.org/docs/current/static/sql-copy.html) can write multiple rows in parallel when used on a distributed table. Writing multiple rows in parallel improves performance for use-cases, which can use bulk ingestion (for example, sensor data, select streams).

To show the benefits of parallel indexing, the following example shows indexing ~200k rows containing large JSON objects from the [GitHub archive](https://www.githubarchive.org/). To run the examples, set up a formation that uses [Citus Cloud](https://www.citusdata.com/product/cloud/), consisting of four worker nodes with four cores each, running PostgreSQL 9.6.

You can download the sample data by running the following commands:

```bash
wget http://examples.citusdata.com/github_archive/github_events-2015-01-01-{0..24}.csv.gz
gzip -d github_events-*.gz
```

Next, create the table for the GitHub events once as a regular PostgreSQL table and then distribute it across the four nodes:

```sql
CREATE TABLE github_events (
    event_id bigint,
    event_type text,
    event_public boolean,
    repo_id bigint,
    payload jsonb,
    repo jsonb,
    actor jsonb,
    org jsonb,
    created_at timestamp
);

-- (distributed table only) Shard the table by repo_id
SELECT create_distributed_table('github_events', 'repo_id');

-- Initial data load: 218934 events from 2015-01-01
\COPY github_events FROM PROGRAM 'cat github_events-*.csv' WITH (FORMAT CSV)
```

Each event in the GitHub data set has a detailed payload object in JSON format. Building a GIN index on the payload gives us the ability to quickly perform fine-grained searches on events, such as finding commits from a specific author. However, building such an index can be expensive. Fortunately, parallel indexing makes this a lot faster by using all cores at the same time and building many smaller indexes:

```sql
CREATE INDEX github_events_payload_idx ON github_events USING GIN (payload);
```

| Operation | Regular table | Distributed table | Speedup |
| --- | --- | --- | --- |
| CREATE INDEX on 219k rows | 33.2s | 2.6s | 13x |

Parallel `CREATE INDEX` exhibits super-linear speedups giving \>16x speedup despite having only 16 cores. Inserting into one index is less efficient than inserting into a small, per-shard index (following O(log N) for N rows), which gives another performance benefit to sharding.

| Operation | Regular table | Distributed table | Speedup |
| --- | --- | --- | --- |
| CREATE INDEX on 438k rows | 55.9s | 3.2s | 17x |
| CREATE INDEX on 876k rows | 110.9s | 5.0s | 22x |
| CREATE INDEX on 1.8M rows | 218.2s | 8.9s | 25x |

Once the index is created, the `COPY` command also takes advantage of parallel indexing. Internally, COPY sends a large number of rows over multiple connections to different workers asynchronously which then store and index the rows in parallel. This allows for faster load times than a single PostgreSQL process could achieve. How much speedup depends on the data distribution. If all data goes to a single shard, performance is similar to PostgreSQL.

```
\COPY github_events FROM PROGRAM 'cat github_events-*.csv' WITH (FORMAT CSV)
```

| Operation | Regular table | Distributed table | Speedup |
| --- | --- | --- | --- |
| COPY 219k rows no index | 18.9s | 12.4s | 1.5x |
| COPY 219k rows with GIN | 49.3s | 12.9s | 3.8x |

Finally, measure the effect that the index has on query time. Try two different queries, one across all repos and one with a specific `repo_id` filter. This distinction is relevant to Citus because `repo_id`shards the `github_events` table. A query with a specific `repo_id` filter goes to a single shard, whereas the other query is parallelized across all shards.

```sql
-- Get all commits by test@gmail.com from all repos
SELECT repo_id, jsonb_array_elements(payload->'commits')
  FROM github_events
 WHERE event_type = 'PushEvent' AND
       payload @> '{"commits":[{"author":{"email":"test@gmail.com"}}]}';

-- Get all commits by test@gmail.com from a single repo
SELECT repo_id, jsonb_array_elements(payload->'commits')
  FROM github_events
 WHERE event_type = 'PushEvent' AND
       payload @> '{"commits":[{"author":{"email":"test@gmail.com"}}]}' AND
       repo_id = 17330407;
```

On 219k rows, this gives us the following query times. Times marked with \* are of queries that Citus enacts in parallel. Parallelization creates some fixed overhead, but also allows for more heavy lifting, which is why it can either be faster or a bit slower than queries on a regular table.

| Operation | Regular table | Distributed table |
| --- | --- | --- |
| SELECT no indexes, all repos | 900ms | 68ms* |
| SELECT with GIN on payload, all repos | 2ms | 11ms* |
| SELECT no indexes, single repo | 900ms | 28ms |
| SELECT with indexes, single repo | 2ms | 2ms |

Indexes in PostgreSQL can dramatically reduce query times, but at the same time dramatically slow down writes. Citus gives you the possibility of scaling out your cluster to get good performance on both sides of the pipeline. A particular sweet spot for Citus is parallel ingestion and single-shard queries, which gives querying performance that's better than regular PostgreSQL, but with higher and more scalable write throughput.

## Related content

- [Guides overview](guides.md)
- [Performance tuning](performance-tuning.md)
