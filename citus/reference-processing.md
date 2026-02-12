---
title: "Query Processing in Citus: Distributed Execution Architecture"
description: This article describes the architecture that Citus uses to process, coordinate, and distribute queries.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: reference
monikerRange: "citus-13 || citus-14"
---

# Query processing in Citus: Distributed execution architecture

A Citus cluster consists of a coordinator instance and multiple worker instances. The data is sharded on the workers while the coordinator stores metadata about these shards. You execute all queries to the cluster through the coordinator. The coordinator partitions the query into smaller query fragments where each query fragment can run independently on a shard. The coordinator assigns the query fragments to workers, oversees their execution, merges their results, and returns the final result to the user. The following diagram provides a brief description of the query processing architecture.

:::image type="content" source="./media/reference-processing/citus-high-level-architecture.png" alt-text="Diagram showing the Citus query processing architecture with queries being distributed through the coordinator node to worker nodes.":::

Citus's query processing pipeline involves two components:

- **Distributed Query Planner and Executor**
- **PostgreSQL Planner and Executor**

The following sections discuss these components in greater detail.

## Distributed query planner

Citus's distributed query planner takes in a SQL query and plans it for distributed execution.

For `SELECT` queries, the planner first creates a plan tree of the input query and transforms it into its commutative and associative form so it can be parallelized. It also applies several optimizations to ensure that the queries are executed in a scalable manner, and that network I/O is minimized.

Next, the planner breaks the query into two parts: The coordinator query, which runs on the coordinator and the worker query fragments, which run on individual shards on the workers. The planner then assigns the query fragments to the workers such that all their resources are used efficiently. After this step, the distributed query plan is passed on to the distributed executor for execution.

The planning process for key-value lookups on the distribution column or modification queries is slightly different as they hit exactly one shard. When the planner receives an incoming query, it decides the correct shard to which the query should be routed. It determines the right shard for the query by extracting the distribution column in the incoming row and looking up the metadata. Then, the planner rewrites the SQL of that command to reference the shard table instead of the original table. This rewritten plan is then passed to the distributed executor.

### Delayed fast path planning (Citus 13.2)

In Citus 13.2, the planner delays building the fast-path placeholder plan until it identifies the shard. If the shard placement is local to the node that handles the client query (MX mode), Citus can avoid deparse, parse, and plan steps for the shard query and reuse a cached plan. This approach improves throughput.

Eligibility:

- Query is `SELECT` or `UPDATE` on a distributed table (schema or column-sharded) or Citus-managed local table.
- No volatile functions.
- Shard can be determined at plan time and is local to the node (MX mode).
- Reference tables aren't currently supported.

Behavior:

- If the shard is local and safe, the executor replaces the distributed table OID with the shard OID, calls `standard_planner`, and caches the plan in the task.
- Otherwise, the executor falls back to the fast-path placeholder plan.

GUC:

- `citus.enable_local_fast_path_query_optimization` (default `on`).

## Distributed query executor

Citus's distributed executor runs distributed query plans and handles failures. The executor is well suited for getting fast responses to queries that involve filters, aggregations, and colocated joins. It's also good for running single-tenant queries with full SQL coverage. The executor opens one connection per shard to the workers as needed and sends all fragment queries to them. It then fetches the results from each fragment query, merges them, and returns the final results to the user.

### Subquery and CTE push-pull execution

If necessary, Citus can gather results from subqueries and common table expressions (CTEs) into the coordinator node and then push them back across workers for use by an outer query. This architecture allows Citus to support a greater variety of SQL constructs.

For example, having subqueries in a WHERE clause can't always execute inline at the same time as the main query, but must be done separately. Suppose a web analytics application maintains a `page_views` table partitioned by `page_id`. To query the number of visitor hosts on the top 20 most visited pages, use a subquery to find the list of pages, then an outer query to count the hosts.

```sql
SELECT page_id, count(distinct host_ip)
FROM page_views
WHERE page_id IN (
  SELECT page_id
  FROM page_views
  GROUP BY page_id
  ORDER BY count(*) DESC
  LIMIT 20
)
GROUP BY page_id;
```

The executor runs a fragment of this query against each shard by `page_id`, counts distinct `host_ip`s, and combines the results on the coordinator. However, the `LIMIT` in the subquery means the subquery can't be executed as part of the fragment. By recursively planning the query Citus can run the subquery separately, push the results to all workers, run the main fragment query, and pull the results back to the coordinator. The *push-pull* design supports subqueries like the one in the previous example.

You can see this push-pull execution in action by reviewing the [EXPLAIN](https://www.postgresql.org/docs/current/static/sql-explain.html) output for this query.

```sql
GroupAggregate (cost=0.00..0.00 rows=0 width=0)
  Group Key: remote_scan.page_id
  -> Sort (cost=0.00..0.00 rows=0 width=0)
    Sort Key: remote_scan.page_id
    -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
      -> Distributed Subplan 6_1
        -> Limit (cost=0.00..0.00 rows=0 width=0)
          -> Sort (cost=0.00..0.00 rows=0 width=0)
            Sort Key: COALESCE((pg_catalog.sum((COALESCE((pg_catalog.sum(remote_scan.worker_column_2))::bigint, '0'::bigint))))::bigint, '0'::bigint) DESC
            -> HashAggregate (cost=0.00..0.00 rows=0 width=0)
              Group Key: remote_scan.page_id
              -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
                Task Count: 32
                Tasks Shown: One of 32
                -> Task
                  Node: host=localhost port=9701 dbname=postgres
                  -> HashAggregate (cost=54.70..56.70 rows=200 width=12)
                    Group Key: page_id
                    -> Seq Scan on page_views_102008 page_views (cost=0.00..43.47 rows=2247 width=4)
      Task Count: 32
      Tasks Shown: One of 32
      -> Task
        Node: host=localhost port=9701 dbname=postgres
        -> HashAggregate (cost=84.50..86.75 rows=225 width=36)
          Group Key: page_views.page_id, page_views.host_ip
          -> Hash Join (cost=17.00..78.88 rows=1124 width=36)
            Hash Cond: (page_views.page_id = intermediate_result.page_id)
            -> Seq Scan on page_views_102008 page_views (cost=0.00..43.47 rows=2247 width=36)
            -> Hash (cost=14.50..14.50 rows=200 width=4)
              -> HashAggregate (cost=12.50..14.50 rows=200 width=4)
                Group Key: intermediate_result.page_id
                -> Function Scan on read_intermediate_result intermediate_result (cost=0.00..10.00 rows=1000 width=4)
```

The process is fairly involved, so let's break it apart and examine each piece.

```sql
GroupAggregate (cost=0.00..0.00 rows=0 width=0)
  Group Key: remote_scan.page_id
  -> Sort (cost=0.00..0.00 rows=0 width=0)
    Sort Key: remote_scan.page_id
```

The root of the tree is what the coordinator node does with the results from the workers. In this case, it's grouping them, and `GroupAggregate` requires they be sorted first.

```sql
    -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
      -> Distributed Subplan 6_1
```

The custom scan has two large subtrees, starting with a *distributed subplan*.

```sql
        -> Limit (cost=0.00..0.00 rows=0 width=0)
          -> Sort (cost=0.00..0.00 rows=0 width=0)
            Sort Key: COALESCE((pg_catalog.sum((COALESCE((pg_catalog.sum(remote_scan.worker_column_2))::bigint, '0'::bigint))))::bigint, '0'::bigint) DESC
            -> HashAggregate (cost=0.00..0.00 rows=0 width=0)
              Group Key: remote_scan.page_id
              -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
                Task Count: 32
                Tasks Shown: One of 32
                -> Task
                  Node: host=localhost port=9701 dbname=postgres
                  -> HashAggregate (cost=54.70..56.70 rows=200 width=12)
                    Group Key: page_id
                    -> Seq Scan on page_views_102008 page_views (cost=0.00..43.47 rows=2247 width=4)
```

Worker nodes run this subplan for each of the 32 shards (Citus is choosing one representative for display). You can recognize all the pieces of the `IN (...)` subquery: the sorting, grouping, and limiting. When all workers complete this query, they send their output back to the coordinator, which puts it together as *intermediate results*.

```sql
      Task Count: 32
      Tasks Shown: One of 32
      -> Task
        Node: host=localhost port=9701 dbname=postgres
        -> HashAggregate (cost=84.50..86.75 rows=225 width=36)
          Group Key: page_views.page_id, page_views.host_ip
          -> Hash Join (cost=17.00..78.88 rows=1124 width=36)
            Hash Cond: (page_views.page_id = intermediate_result.page_id)
```

Citus starts another executor job in this second subtree. It's going to count distinct hosts in `page_views`. It uses a JOIN to connect with the intermediate results. The intermediate results help restrict it to the top 20 pages.

```sql
            -> Seq Scan on page_views_102008 page_views (cost=0.00..43.47 rows=2247 width=36)
            -> Hash (cost=14.50..14.50 rows=200 width=4)
              -> HashAggregate (cost=12.50..14.50 rows=200 width=4)
                Group Key: intermediate_result.page_id
                -> Function Scan on read_intermediate_result intermediate_result (cost=0.00..10.00 rows=1000 width=4)
```

The worker internally retrieves intermediate results by using a `read_intermediate_result` function, which loads data from a file that the coordinator node copied in.

This example showed how Citus executed the query in multiple steps with a distributed subplan, and how you can use EXPLAIN to learn about distributed query execution.

## PostgreSQL planner and executor

After the distributed executor sends the query fragments to the workers, the workers process the fragments like regular PostgreSQL queries. The PostgreSQL planner on each worker chooses the most optimal plan for executing the query locally on the corresponding shard table. The PostgreSQL executor runs the query and returns the query results back to the distributed executor. For more information about the PostgreSQL [planner](http://www.postgresql.org/docs/current/static/planner-optimizer.html) and [executor](http://www.postgresql.org/docs/current/static/executor.html), see the PostgreSQL manual. Finally, the distributed executor passes the results to the coordinator for final aggregation.

## Related content

- [Command propagation reference](reference-propagation.md)
- [Citus SQL reference overview](reference.md)
