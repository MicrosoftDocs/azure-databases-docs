---
title: Efficient Rollup Tables with HyperLogLog in PostgreSQL
description: Learn how to use HyperLogLog with rollup tables in PostgreSQL so you can efficiently aggregate and query large datasets.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
monikerRange: "citus-13 || citus-14"
---

# Efficient rollup tables with HyperLogLog in PostgreSQL

(Copy of [original publication](https://www.citusdata.com/blog/2017/06/30/efficient-rollup-with-hyperloglog-on-postgres/))

Rollup tables are commonly used in PostgreSQL when you don't need to perform detailed analysis, but you still need to answer basic aggregation queries on older data.

With rollup tables, you can preaggregate your older data for the queries you still need to answer. Then you no longer need to store all of the older data, rather, you can delete the older data or roll it off to slower storage—saving space and computing power.

This article shows you a rollup table example in PostgreSQL without the use of HyperLogLog (HLL).

## Rollup tables without HLL—using GitHub events data as an example

Each record in this GitHub data set represents an event created in GitHub. In addition, each record has key information regarding the event such as event type, creation date, and the user who created the event. For more information, see [getting started with GitHub event data on Citus](https://www.citusdata.com/blog/2017/01/27/getting-started-with-github-events-data/).

If you want to create a chart to show the number of GitHub event creations in each minute, use a rollup table. With a rollup table, you don't need to store all user events in order to create the chart. Rather, you can aggregate the number of event creations for each minute and just store the aggregated data. You can then throw away the rest of the events data, if you're trying to conserve space.

To illustrate the process, see the following `github_events` table example:

``` psql
CREATE TABLE github_events
(
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

\COPY github_events FROM events.csv CSV
```

For this example, if you don't perform detailed analysis on your older data regularly, there's no need to allocate resources for the older data. Instead you can use rollup tables, and keep the necessary information in memory. You can create a rollup table for this purpose:

```sql
CREATE TABLE github_events_rollup_minute
(
    created_at timestamp,
    event_count bigint
);
```

And populate with INSERT/SELECT:

```sql
INSERT INTO github_events_rollup_minute(
    created_at,
    event_count
)
SELECT
    date_trunc('minute', created_at) AS created_at,
    COUNT(*) AS event_count
FROM github_events
GROUP BY 1;
```

Now you can store the older (and bigger) data in a less expensive resource like disk so that you can access it in the future—and keep the `github_events_rollup_minute` table in memory so you can create your analytics dashboard.

By aggregating the data by minute in the previous example, you can answer queries like hourly and daily total event creations. However, it isn't possible to know the more granular event creation count for each second.

Further, since you don't keep event creations for each user separately, you can't have a separate analysis for each user with this rollup table.

## Without HLL, rollup tables have a few limitations

For queries involving distinct count, rollup tables are less useful. For example, if you preaggregate over minutes, you can't answer queries asking for distinct counts over an hour. You can't add each minute's result to have hourly event creations by unique users because you're likely to have overlapping records in different minutes.

If you want to calculate distinct counts constrained by combinations of columns, you would need multiple rollup tables.

Sometimes you want to get event creation count by unique users filtered by date and sometimes you want to get unique event creation counts filtered by event type (and sometimes a combination of both.) With HLL, one rollup table can answer all of these queries—but without HLL, you would need a separate rollup table for each of these different types of queries.

## HLL in use

If you do rollups with the HLL data type (instead of rolling up the final unique user count), you can easily overcome the overlapping records problem. HLL encodes the data in a way that allows summing up individual unique counts without recounting overlapping records.

HLL is also useful if you want to calculate distinct counts constrained by combinations of columns. For example, if you want to get unique event creation counts per date and/or per event type, with HLL, you can use just one rollup table for all combinations.

Whereas without HLL, if you want to calculate distinct counts constrained by combinations of columns, you would need to create:

- Seven different rollup tables to cover all combinations of three columns
- 15 rollup tables to cover all combinations of four columns
- Two-in-one rollup tables to cover all combinations in "n" columns

## HLL and rollup tables in action, together

HLL can help you to answer some typical distinct count queries on GitHub events data. First, create the `github_events` table and load data into it:

``` psql
CREATE TABLE github_events
(
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

\COPY github_events FROM events.csv CSV
```

After creating your table, create a rollup table. You want to get distinct counts both per `user` and per `event_type` basis. Therefore, you should use a slightly different rollup table:

```sql
DROP TABLE IF EXISTS github_events_rollup_minute;

CREATE TABLE github_events_rollup_minute(
    created_at timestamp,
    event_type text,
    distinct_user_id_count hll
);
```

Finally, you can use INSERT/SELECT to populate your rollup table and you can use `hll_hash_bigint` function to hash each `user_id`.

```sql
INSERT INTO github_events_rollup_minute(
    created_at,
    event_type,
    distinct_user_id_count
)
SELECT
    date_trunc('minute', created_at) AS created_at,
    event_type,
    hll_add_agg(hll_hash_bigint(user_id))
FROM github_events
GROUP BY 1, 2;

INSERT 0 2484
```

## What kinds of queries can HLL answer?

To materialize HLL values to actual distinct counts, consider the question:

**How many distinct users created an event for each event type at each minute at 2016-12-01 05:35:00?**

You need to use the `hll_cardinality` function to materialize the HLL data structures to actual distinct count.

```sql
SELECT
    created_at,
    event_type,
    hll_cardinality(distinct_user_id_count) AS distinct_count
FROM
    github_events_rollup_minute
WHERE
    created_at = '2016-12-01 05:35:00'::timestamp
ORDER BY 2;

     created_at      |          event_type           |  distinct_count
---------------------+-------------------------------+------------------
 2016-12-01 05:35:00 | CommitCommentEvent            |                1
 2016-12-01 05:35:00 | CreateEvent                   |               59
 2016-12-01 05:35:00 | DeleteEvent                   |                6
 2016-12-01 05:35:00 | ForkEvent                     |               20
 2016-12-01 05:35:00 | GollumEvent                   |                2
 2016-12-01 05:35:00 | IssueCommentEvent             |               42
 2016-12-01 05:35:00 | IssuesEvent                   |               13
 2016-12-01 05:35:00 | MemberEvent                   |                4
 2016-12-01 05:35:00 | PullRequestEvent              |               24
 2016-12-01 05:35:00 | PullRequestReviewCommentEvent |                4
 2016-12-01 05:35:00 | PushEvent                     | 254.135297564883
 2016-12-01 05:35:00 | ReleaseEvent                  |                4
 2016-12-01 05:35:00 | WatchEvent                    |               57
(13 rows)
```

HLL helps answer the following query:

**How many distinct users created an event during this one-hour period?**

With HLLs, you can see the answer.

```sql
SELECT
    hll_cardinality(SUM(distinct_user_id_count)) AS distinct_count
FROM
    github_events_rollup_minute
WHERE
    created_at BETWEEN '2016-12-01 05:00:00'::timestamp AND '2016-12-01 06:00:00'::timestamp;

 distinct_count
------------------
 10978.2523520687
(1 row)
```

Another question to consider for the use of HLL's additivity property is:

**How many unique users created an event during each hour at 2016-12-01?**

```sql
SELECT
    EXTRACT(HOUR FROM created_at) AS hour,
    hll_cardinality(SUM(distinct_user_id_count)) AS distinct_count
FROM
    github_events_rollup_minute
WHERE
    created_at BETWEEN '2016-12-01 00:00:00'::timestamp AND '2016-12-01 23:59:59'::timestamp
GROUP BY 1
ORDER BY 1;

  hour |  distinct_count
-------+------------------
     5 |  10598.637184899
     6 | 17343.2846931687
     7 | 18182.5699816622
     8 | 12663.9497604266
(4 rows)
```

Since data is limited, the query only returned four rows. Finally, consider the following question:

**How many distinct users created a PushEvent during each hour?**

```sql
SELECT
    EXTRACT(HOUR FROM created_at) AS hour,
    hll_cardinality(SUM(distinct_user_id_count)) AS distinct_push_count
FROM
    github_events_rollup_minute
WHERE
    created_at BETWEEN '2016-12-01 00:00:00'::timestamp AND '2016-12-01 23:59:59'::timestamp
    AND event_type = 'PushEvent'::text
GROUP BY 1
ORDER BY 1;

 hour | distinct_push_count
------+---------------------
    5 |    6206.61586498546
    6 |    9517.80542100396
    7 |    10370.4087640166
    8 |    7067.26073810357
(4 rows)
```

## A rollup table with HLL is worth a thousand rollup tables without HLL

One rollup table with HLL can answer queries where otherwise you would need a different rollup table for each query. In the previous example, you see that with HLL, four example queries all can be answered with a single rollup table. Without HLL, you would need three separate rollup tables to answer all these queries.

Without HLL, you're likely to need even more rollup tables to support your analytics queries. For all combinations of "n" constraints, you would need "2n - 1" rollup tables. With HLL, you can accomplish the job with one rollup table.

One rollup table with HLL is easier to maintain than multiple rollup tables, and that one rollup table uses less memory. In some cases, without HLL, the overhead of rollup tables can become too expensive and exceeds the benefit, so people decide not to use rollup tables at all.

## Want to learn more about HLL in PostgreSQL?

HLL is also useful in distributed systems. As with rollup tables, in a distributed system such as Citus, you often place different parts of data in different nodes. You're therefore likely to have overlapping records at different nodes. The techniques HLL uses to encode data to merge separate unique counts and address the overlapping record problem can also help in distributed systems.

For more information, see [Distributed distinct count with HyperLogLog on PostgreSQL](hyperloglog-count-distinct.md). This article explains the internals of HLL and how HLL merges separate unique counts without counting overlapping records.

## Related content

- [Guides overview](guides.md)
- [Tutorial: Time series](tutorial-time-series.md)
