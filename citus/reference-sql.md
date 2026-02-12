---
title: Run SQL Queries on Citus Distributed Tables
description: This article describes how to query distributed tables in Citus using standard PostgreSQL queries.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
ai-usage: ai-assisted
---

# Run SQL queries on Citus distributed tables

As discussed in the previous sections, Citus is an extension that extends the latest PostgreSQL for distributed execution. With Citus, you can use standard PostgreSQL [SELECT](http://www.postgresql.org/docs/current/static/sql-select.html) queries on the Citus coordinator for querying. Citus then parallelizes the SELECT queries involving complex selections, groupings and orderings, and `JOIN`s to speed up the query performance. At a high level, Citus partitions the SELECT query into smaller query fragments, assigns the query fragments to workers, oversees their execution, merges their results (and orders them if needed), and returns the final result to the user.

In the following sections, you learn about the different types of queries you can run by using Citus.

## Aggregate functions

Citus supports and parallelizes most aggregate functions supported by PostgreSQL, including custom user-defined aggregates. Aggregates execute by using one of three methods, in this order of preference:

1. When the aggregate is grouped by a table's distribution column, Citus can push down execution of the entire query to each worker. All aggregates are supported in this situation and execute in parallel on the worker nodes. (TYou must install any custom aggregates, which you plan to use, on the worker nodes.)

1. When the aggregate *isn't* grouped by a table's distribution column, Citus can still optimize on a case-by-case basis. Citus has internal rules for certain aggregates like `sum()`, `avg()`, and `count(distinct)` that allow it to rewrite queries for *partial aggregation* on workers. For instance, to calculate an average, Citus obtains a sum and a count from each worker, and then the coordinator node computes the final average.

   Here's the full list of the special-case aggregates:

   ```sql
   avg, min, max, sum, count, array_agg, jsonb_agg, jsonb_object_agg, json_agg, json_object_agg, bit_and, bit_or, bool_and, bool_or, every, hll_add_agg, hll_union_agg, topn_add_agg, topn_union_agg, any_value, tdigest(double precision, int), tdigest_percentile(double precision, int, double precision), tdigest_percentile(double precision, int, double precision\[\]), tdigest_percentile(tdigest, double precision), tdigest_percentile(tdigest, double precision\[\]), tdigest_percentile_of(double precision, int, double precision), tdigest_percentile_of(double precision, int, double precision\[\]), tdigest_percentile_of(tdigest, double precision), tdigest_percentile_of(tdigest, double precision\[\])
   ```

1. Last resort: pull all rows from the workers and perform the aggregation on the coordinator node. When the aggregate isn't grouped on a distribution column, and isn't one of the predefined special cases, Citus falls back to this approach. It causes network overhead, and can exhaust the coordinator's resources if the data set to be aggregated is too large. (As shown in the following example, you can disable this fallback.)

   Small changes in a query can change execution modes, causing potentially surprising inefficiency. For example, `sum(x)` grouped by a nondistribution column could use distributed execution, while `sum(distinct x)` has to pull up the entire set of input records to the coordinator.

   One column can hurt the execution of a whole query. In the following example, if `sum(distinct value2)` has to be grouped on the coordinator, then so does `sum(value1)` even if the latter was fine on its own.

   ```sql
   SELECT sum(value1), sum(distinct value2) FROM distributed_table;
   ```

   To avoid accidentally pulling data to the coordinator, you can set a global user configuration (GUC):

   ```sql
   SET citus.coordinator_aggregation_strategy TO 'disabled';
   ```

   Disabling the coordinator aggregation strategy prevents *type three* aggregate queries from working at all.

### Count(distinct) aggregates

Citus supports `count(distinct)` aggregates in several ways. If the `count(distinct)` aggregate is on the distribution column, Citus can directly push down the query to the workers. If not, Citus runs select distinct statements on each worker, and returns the list to the coordinator where it obtains the final count.

Transferring this data becomes slower when workers have a greater number of distinct items. Especially for queries containing multiple `count(distinct)` aggregates, for example:

```sql
-- multiple distinct counts in one query tend to be slow
SELECT count(distinct a), count(distinct b), count(distinct c)
FROM table_abc;
```

For this kind of query, the resulting select distinct statements on the workers essentially produce a cross-product of rows to be transferred to the coordinator.

For increased performance you can choose to make an approximate count instead, by following these steps:

1. Download and install the hll extension on all PostgreSQL instances (the coordinator and all the workers).

   Visit the [postgresql-hll GitHub repository](https://github.com/citusdata/postgresql-hll) for specifics on obtaining the hll extension that defines the HyperLogLog (HLL) data structure.

1. Create the hll extension on all the PostgreSQL instances by running the following command from the coordinator:

   ```sql
   CREATE EXTENSION hll;
   ```

1. Enable `count_distinct` approximations by setting the `citus.count_distinct_error_rate` configuration value. Lower values for this configuration setting are expected to give more accurate results but take more time for computation. Set this value to *0.005*.

   ```sql
   SET citus.count_distinct_error_rate to 0.005;
   ```

After this step, `count(distinct)` aggregates automatically switch to using HLL, with no changes necessary to your queries. You should be able to run approximate count distinct queries on any column of the table.

#### HyperLogLog column

Certain users already store their data as HLL columns. In such cases, they can dynamically roll up those data by calling `hll_union_agg(hll_column)`.

### Estimating the top n items

You can calculate the first *n* elements in a set by applying count, sort, and limit. However, as data sizes increase, this method becomes slow and resource intensive. It's more efficient to use an approximation.

The open source [TopN extension](https://github.com/citusdata/postgresql-topn) for PostgreSQL enables fast approximate results to *top-n* queries. The extension materializes the top values into a JSON data type. TopN can incrementally update these top values, or merge them on-demand across different time intervals.

#### Basic operations

Before seeing a realistic example of TopN, let's see how some of its primitive operations work. First, `topn_add` updates a JSON object with counts of how many times a key is seen:

```sql
-- starting from nothing, record that we saw an "a"
select topn_add('{}', 'a');
-- => {"a": 1}

-- record the sighting of another "a"
select topn_add(topn_add('{}', 'a'), 'a');
-- => {"a": 2}
```

The extension also provides aggregations to scan multiple values:

```sql
-- for normal_rand
create extension tablefunc;

-- count values from a normal distribution
SELECT topn_add_agg(floor(abs(i))::text)
  FROM normal_rand(1000, 5, 0.7) i;
-- => {"2": 1, "3": 74, "4": 420, "5": 425, "6": 77, "7": 3}
```

If the number of distinct values crosses a threshold, the aggregation drops information for those values seen least frequently, keeping space usage under control. You can control the threshold by using the global user configuration `topn.number_of_counters`. Its default value is *1000*.

#### Realistic example

Now onto a more realistic example of how TopN works in practice. Let's ingest Amazon product reviews from the year 2000 and use TopN to query it quickly. First, download the dataset:

```bash
curl -L https://examples.citusdata.com/customer_reviews_2000.csv.gz | \
  gunzip > reviews.csv
```

Next, ingest it into a distributed table:

``` psql
CREATE TABLE customer_reviews
(
    customer_id TEXT,
    review_date DATE,
    review_rating INTEGER,
    review_votes INTEGER,
    review_helpful_votes INTEGER,
    product_id CHAR(10),
    product_title TEXT,
    product_sales_rank BIGINT,
    product_group TEXT,
    product_category TEXT,
    product_subcategory TEXT,
    similar_product_ids CHAR(10)[]
);

SELECT create_distributed_table('customer_reviews', 'product_id');

\COPY customer_reviews FROM 'reviews.csv' WITH CSV
```

Next, add the extension, create a destination table to store the json data generated by TopN, and apply the `topn_add_agg` function you saw previously.

```sql
-- run below command from coordinator, it will be propagated to the worker nodes as well
CREATE EXTENSION topn;

-- a table to materialize the daily aggregate
CREATE TABLE reviews_by_day
(
  review_date date unique,
  agg_data jsonb
);

SELECT create_reference_table('reviews_by_day');

-- materialize how many reviews each product got per day per customer
INSERT INTO reviews_by_day
  SELECT review_date, topn_add_agg(product_id)
  FROM customer_reviews
  GROUP BY review_date;
```

Now, rather than writing a complex window function on `customer_reviews`, you can apply TopN to `reviews_by_day`. For instance, the following query finds the most frequently reviewed product for each of the first five days:

```sql
SELECT review_date, (topn(agg_data, 1)).*
FROM reviews_by_day
ORDER BY review_date
LIMIT 5;
```

```output
┌─────────────┬────────────┬───────────┐
│ review_date │    item    │ frequency │
├─────────────┼────────────┼───────────┤
│ 2000-01-01  │ 0939173344 │        12 │
│ 2000-01-02  │ B000050XY8 │        11 │
│ 2000-01-03  │ 0375404368 │        12 │
│ 2000-01-04  │ 0375408738 │        14 │
│ 2000-01-05  │ B00000J7J4 │        17 │
└─────────────┴────────────┴───────────┘
```

The JSON fields created by TopN can be merged with `topn_union` and `topn_union_agg`. You can use the latter to merge the data for the entire first month and list the five most reviewed products during that period.

```sql
SELECT (topn(topn_union_agg(agg_data), 5)).*
FROM reviews_by_day
WHERE review_date >= '2000-01-01' AND review_date < '2000-02-01'
ORDER BY 2 DESC;
```

```output
┌────────────┬───────────┐
│    item    │ frequency │
├────────────┼───────────┤
│ 0375404368 │       217 │
│ 0345417623 │       217 │
│ 0375404376 │       217 │
│ 0375408738 │       217 │
│ 043936213X │       204 │
└────────────┴───────────┘
```

For more information and examples, see the [TopN readme](https://github.com/citusdata/postgresql-topn/blob/master/README.md).

### Percentile calculations

Finding an exact percentile over a large number of rows can be too expensive. The coordinator must receive all rows for final sorting and processing. On the other hand, you can find an approximation in parallel on worker nodes by using a *sketch algorithm*. The coordinator node combines compressed summaries into the final result, rather than reading through the full rows.

A popular sketch algorithm for percentiles uses a compressed data structure called `tdigest`, and is available for PostgreSQL in the [t-digest extension](https://github.com/tvondra/tdigest). Citus contains integrated support for this extension.

Here's how to use `tdigest` in Citus:

1. Download and install the `tdigest` extension on all PostgreSQL nodes (the coordinator and all the workers). The [t-digest extension GitHub repository](https://github.com/tvondra/tdigest) has installation instructions.
1. Create the `tdigest` extension within the database. Run the following command on the coordinator:

   ```sql
   CREATE EXTENSION tdigest;
   ```

   The coordinator propagates the command to the workers as well.

When you use any of the aggregates defined in the extension in queries, Citus rewrites the queries to push down partial `tdigest` computation to the workers where applicable.

You can control the accuracy of `tdigest` with the `compression` argument that you pass into aggregates. The trade-off is accuracy versus the amount of data shared between workers and the coordinator. For a full explanation of how to use the aggregates in the `tdigest` extension, see the documentation on the official [t-digest extension GitHub repository](https://github.com/tvondra/tdigest).

## Limit pushdown

Citus also pushes down the limit clauses to the shards on the workers wherever possible to minimize the amount of data transferred across the network.

However, in some cases, `SELECT` queries with `LIMIT` clauses might need to fetch all rows from each shard to generate exact results. For example, if the query requires ordering by the aggregate column, it needs results of that column from all shards to determine the final aggregate value. This processing reduces performance of the `LIMIT` clause due to high volume of network data transfer. In such cases, and where an approximation would produce meaningful results, Citus provides an option for network efficient approximate `LIMIT` clauses.

`LIMIT` approximations are disabled by default. You can enable them by setting the configuration parameter `citus.limit_clause_row_fetch_count`. Based on this configuration value, Citus limits the number of rows returned by each task for aggregation on the coordinator. Due to this limit, the final results might be approximate. Increasing this limit increases the accuracy of the final results, while still providing an upper bound on the number of rows pulled from the workers.

```sql
SET citus.limit_clause_row_fetch_count to 10000;
```

## Views on distributed tables

Citus supports all views on distributed tables. For an overview of views' syntax and features, see the PostgreSQL documentation for [CREATE VIEW](https://www.postgresql.org/docs/current/static/sql-createview.html).

Some views cause a less efficient query plan than others. For more information about detecting and improving poor view performance, see `subquery_perf`. (Views are treated internally as subqueries.)

Citus supports materialized views as well, and stores them as local tables on the coordinator node.

## Joins

Citus supports equi-JOINs between any number of tables irrespective of their size and distribution method. Based on how the tables are distributed, the query planner determines the optimal join method and join order. It evaluates several possible join orders and creates a join plan, which requires minimum data to be transferred across network.

### Colocated joins

When two tables are colocated, you can join them efficiently on their common distribution columns. A colocated join is the most efficient way to join two large distributed tables.

Internally, the Citus coordinator knows which shards of the colocated tables might match with shards of the other table by looking at the distribution column metadata. This metadata allows Citus to prune away shard pairs that can't produce matching join keys. The joins between remaining shard pairs are executed in parallel on the workers and then the results are returned to the coordinator.

> [!NOTE]  
> Make sure that the tables are distributed into the same number of shards and that the distribution columns of each table have exactly matching types. Attempting to join on columns of slightly different types such as int and bigint can cause problems.

### Reference table joins

Use `reference_tables` as *dimension* tables to join efficiently with large *fact* tables. Because Citus replicates reference tables in full across all worker nodes, a reference join can decompose into local joins on each worker and performed in parallel. A reference join is like a more flexible version of a colocated join because reference tables aren't distributed on any particular column and are free to join on any of their columns.

Reference tables can also join with tables local to the coordinator node.

### Outer join pushdown (Citus 13.2)

Citus 13.2 can push down eligible LEFT and RIGHT outer joins to workers when the outer side is a recurring relation (for example, reference tables or intermediate results). The planner injects shard-interval constraints on the recurring side to ensure correctness, so the join can run on workers and avoid coordinator-side joins and large intermediate results.

- Enabled by default. Disable by using `citus.enable_recurring_outer_join_pushdown`.
- Applies to recurring outer joins where shard intervals can be derived (typically hash-distributed tables) including reference tables, intermediate results, and set-returning functions on the outer side.
- Planner injects constraints derived from shard hash ranges onto the recurring side scan (reference, intermediate, or SRF).
- Planner checks eligibility rules (see `CanPushdownRecurringOuterJoin` in Citus source for details).

Example:

```sql
EXPLAIN (COSTS OFF)
SELECT *
FROM product_categories pc
LEFT JOIN products_table pt
  ON pc.category_id = pt.product_id;
```

**Before 13.2** (reference join not pushed down):

```
Custom Scan (Citus Adaptive)
  -> Distributed Subplan ...
  -> Task
       -> Hash Right Join
            Hash Cond: (intermediate_result.product_id = pc.category_id)
```

**Citus 13.2** (pushed down with constraints):

```
Custom Scan (Citus Adaptive)
  Task Count: 32
  -> Task
       Node: host=localhost port=9701 dbname=postgres
       -> Hash Right Join
            Hash Cond: (pt.product_id = pc.category_id)
            -> Seq Scan on products_table_102072 pt
            -> Hash
                 -> Seq Scan on product_categories_102106 pc
                    Filter: ((category_id IS NULL) OR (btint4cmp('-2147483648', hashint8(category_id::bigint)) < 0
                             AND btint4cmp(hashint8(category_id::bigint), '-2013265921') <= 0))
```

### Repartition joins

In some cases, you need to join two tables on columns other than the distribution column. For such cases, Citus also allows joining on nondistribution key columns by dynamically repartitioning the tables for the query.

In such cases, the query optimizer determines the tables to partition based on the distribution columns, join keys, and sizes of the tables. With repartitioned tables, you can ensure that only relevant shard pairs join each other, which reduces the amount of data transferred across the network drastically.

In general, colocated joins are more efficient than repartition joins as repartition joins require shuffling of data. So, try to distribute your tables by the common join keys whenever possible.

## Related content

- [Data definition language (DDL) operations reference](reference-ddl.md)
- [Data modification language (DML) operations reference](reference-dml.md)
- [Citus SQL reference overview](reference.md)
