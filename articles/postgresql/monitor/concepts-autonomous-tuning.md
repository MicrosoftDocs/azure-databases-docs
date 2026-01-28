---
title: Autonomous Tuning
description: This article describes the autonomous tuning feature available in an Azure Database for PostgreSQL flexible server instance.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/27/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: concept-article
ms.custom:
  - references_regions
  - build-2024
  - ignite-2024
# customer intent: As a user, I want to learn about the autonomous tuning feature available in an Azure Database for PostgreSQL, how does it work and what benefits it provides.
---

# Autonomous tuning

Autonomous tuning is a feature in your Azure Database for PostgreSQL flexible server instance that analyzes queries traced of your workload and provides recommendations to improve the performance of those queries.

It's a built-in offering in your Azure Database for PostgreSQL flexible server instance, which builds on top of [query store](concepts-query-store.md) functionality. Autonomous tuning analyzes the workload tracked by query store, and produces index or table recommendations to improve the performance of the analyzed workload. It can produce recommendations to create new indexes, eliminate duplicate or unused indexes, analyze tables that have no statistics or outdated statistics, or vacuum bloated tables.

- [Identify which indexes are beneficial](#create-index-recommendations) to create because they could significantly improve the queries analyzed during an autonomous tuning session.
- [Identify indexes that are exact duplicates and can be eliminated](#drop-duplicate-indexes).
- [Identify indexes not used in a configurable period](#drop-unused-indexes) that could be candidates to eliminate.
- [Identify indexes marked as invalid](#reindex-invalid-indexes) that should be reindexed to turn them into valid ones.
- [Identify tables that lack current statistics](#analyze-table-recommendations) that should be analyzed.
- [Identify tables that are bloated](#vacuum-table-recommendations) that should be vacuumed.

## General description of the autonomous tuning algorithm

When the `index_tuning.mode` server parameter is configured to `report`, tuning sessions are automatically started with the frequency configured in server parameter `index_tuning.analysis_interval`, expressed in minutes.

In the first phase, the tuning session searches for the list of databases in which it considers that whatever recommendations it might produce might significantly affect the overall performance of the system. To do so, it collects all queries recorded by query store whose executions were captured within the lookup interval this tuning session is focusing on. The lookup interval currently spans to the past `index_tuning.analysis_interval` minutes, from the starting time of the tuning session.

For all user-initiated queries with executions recorded in [query store](concepts-query-store.md) and whose runtime statistics aren't [reset](concepts-query-store.md#query_storeqs_reset), the system ranks them based on their aggregated total execution time. It focuses its attention on the most prominent queries, based on their duration.

The following queries are excluded from that list:
- System-initiated queries. (that is, queries executed by `azuresu` role)
- Queries executed in the context of any system database (`azure_sys`, `template0`, `template1`, and `azure_maintenance`).

The algorithm iterates over the target databases, searching for possible indexes that could improve the performance of analyzed workloads. It also searches for indexes that can be eliminated because they're identified as duplicates or not used for a configurable period of time.

### CREATE INDEX recommendations

For each database identified as a candidate to analyze for producing recommendations, all SELECT, UPDATE, INSERT, and DELETE queries executed during the lookup interval and in the context of that specific database are factored in.

The resulting set of queries is ranked based on their aggregated total execution time, and the top `index_tuning.max_queries_per_database` is analyzed for possible index recommendations.

Potential recommendations aim to improve the performance of these types of queries:
- Queries with filters (that is, queries with predicates in the WHERE clause),
- Queries joining multiple relations, whether they follow the syntax in which joins are expressed with JOIN clause or whether the join predicates are expressed in the WHERE clause.
- Queries combining filters and join predicates.
- Queries with grouping (queries with a GROUP BY clause).
- Queries combining filters and grouping.
- Queries with sorting (queries with an ORDER BY clause).
- Queries combining filters and sorting.

> [!NOTE]
> The only type of indexes the system currently recommends is [B-Tree](https://www.postgresql.org/docs/current/indexes-types.html#INDEXES-TYPES-BTREE).

If a query references one column of a table and that table has no statistics, doesn't produce any index recommendations to improve its execution. However, it will generate a recommendation to analyze the table.

`index_tuning.max_indexes_per_table` specifies the number of indexes that can be recommended, excluding any indexes that might already exist on the table for any single table referenced by any number of queries during a tuning session.

`index_tuning.max_index_count` specifies the number of index recommendations produced for all tables of any database analyzed during a tuning session.

For an index recommendation to be emitted, the tuning engine must estimate that it improves at least one query in the analyzed workload by a factor specified with `index_tuning.min_improvement_factor`.

Likewise, all index recommendations are checked to ensure that they don't introduce regression on any single query in that workload of a factor specified with `index_tuning.max_regression_factor`.

> [!NOTE]
> `index_tuning.min_improvement_factor` and `index_tuning.max_regression_factor` both refer to cost of query plans, not to their duration or the resources they consume during execution.

All the parameters mentioned in the previous paragraphs, their default values and valid ranges are described in [configuration options](#configuring-autonomous-tuning).

The script produced along with the recommendation to create an index, follows this pattern:

`CREATE INDEX CONCURRENTLY {indexName} ON {schema}.{table}({column_name}[, ...])`

It includes the clause `CONCURRENTLY`. For further information about the effects of this clause, visit PostgreSQL official documentation for [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY).

Autonomous tuning automatically generates the names of the recommended indexes, which typically consist of the names of the different key columns separated by "_" (underscores) and with a constant "_idx" suffix. If the total length of the name exceeds PostgreSQL limits or if it clashes with any existing relations, the name is slightly different. It could be truncated, and a number could be appended to the end of the name.

#### Compute the impact of a CREATE INDEX recommendation

The impact of creating an index recommendation is measured on IndexSize (megabytes) and QueryCostImprovement (percentage).

IndexSize is a single value that represents the estimated size of the index, considering the current cardinality of the table and the size of the columns referenced by the recommended index.

QueryCostImprovement consists of an array of values, where each element represents the improvement in the plan's cost for each query whose plan's cost is estimated to improve if this index existed. Each element shows the query's identifier (queried) and the percentage by which the plan's cost would improve if the recommendation were implemented (dimensional).

### DROP INDEX and REINDEX recommendations

For each database identified as a candidate to analyze for producing recommendations, it should initiate a new session, and after the CREATE INDEX recommendations phase completes, it recommends dropping or reindexing existing indexes, based on the following criteria:
- Drop if it's considered duplicate of others.
- Drop if it isn't used for a configurable amount of time.
- Reindex indexes which are marked as invalid.

#### Drop duplicate indexes

Recommendations for dropping duplicate indexes: First, identify which indexes have duplicates.

Duplicates are ranked based on different functions that can be attributed to the index and based on their estimated sizes.

Finally, it recommends dropping all duplicates with a lower ranking than its reference leader and describes why each duplicate was ranked the way it was.

For two indexes to be considered duplicate they must:
- Be created over the same table.
- Be an index of the exact same type.
- Match their key columns and, for multi-column index keys, match the order in which they're referenced.
- Match the expression tree of its predicate. Only applicable to partial indexes.
- Match the expression tree of all nonsimple column references. Only applicable to indexes created on expressions.
- Match the collation of each column referenced in the key.

#### Drop unused indexes

Recommendations for dropping unused indexes identify those indexes which:
- Aren't used for at least `index_tuning.unused_min_period` days.
- Show a minimum (daily average) number of `index_tuning.unused_dml_per_table` DMLs on the table where the index is created.
- Show a minimum (daily average) number of `index_tuning.unused_reads_per_table` reads on the table where the index is created.

#### Reindex invalid indexes

Recommendations for reindex existing indexes identify those indexes which are marked as invalid. To learn more about why and when indexes are marked as invalid, refer to the [REINDEX](https://www.postgresql.org/docs/current/sql-reindex.html#DESCRIPTION) in PostgreSQL official documentation.

#### Compute the impact of a DROP INDEX recommendation

The impact of a drop index recommendation is measured on two dimensions: Benefit (percentage) and IndexSize (megabytes).

The benefit is a single value that can be ignored for now.

IndexSize is a single value that represents the estimated size of the index, considering the current cardinality of the table and the size of the columns referenced by the recommended index.

### Table recommendations

For each database identified as a candidate to analyze, it initiates a session that aims to produce table level recommendations. Those recommendations invite you to run ANALYZE or VACUUM on the tables that were accessed by the queries inspected, for which the tuning engine considers running those commands could improve the performance of your workload.

### ANALYZE table recommendations

Recommendations for analyzing a table identify those tables which:
- Were referenced in a query, and have some column of that table used in one of its predicates (WHERE, JOIN, ORDER BY, GROUP BY), and also meet either of the two following conditions:
  - Have never been analyzed.
  - Were analyzed at some point, but are now lacking statistics (typically because the server crashed before the statistics were persisted to disk).

### VACUUM table recommendations

Recommendations for vacuuming a table identify those tables which are significantly bloated. What's considered significant varies with the estimated size of the table. Also, these recommendations are produced when `autovacuum_enabled` isn't set to `off` at server level when the workload is analyzed.

## Configuring autonomous tuning

Autonomous tuning can be enabled, disabled, and configured through a set of parameters that control its behavior.

When autonomous tuning is enabled, it wakes up with a frequency configured in the `index_tuning.analysis_interval` server parameter (defaults to 720 minutes or 12 hours) and starts analyzing the workload recorded by query store during that period.

Notice that if you change the value for `index_tuning.analysis_interval`, it only is observed after the next scheduled execution completes. So, for example, if you enable autonomous tuning one day at 10:00AM, because default value for `index_tuning.analysis_interval` is 720 minutes, the first execution is scheduled to start at 10:00PM that same day. Any changes you make to the value of `index_tuning.analysis_interval` between 10:00AM and 10:00PM won't affect that initial schedule. Only when the scheduled run completes, it will read current value set for `index_tuning.analysis_interval` and will schedule next execution according to that value.

The following options are available for configuring autonomous tuning parameters:

| **Parameter** | **Description** | **Default** | **Range** | **Units** |
| --- | --- | --- | --- | --- |
| `index_tuning.analysis_interval` | Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to `REPORT`. | `720` | `60 - 10080` | minutes |
| `index_tuning.max_columns_per_index` | Maximum number of columns that can be part of the index key for any recommended index. | `2` | `1 - 10` | |
| `index_tuning.max_index_count` | Maximum indexes recommended for each database during one optimization session. | `10` | `1 - 25` | |
| `index_tuning.max_indexes_per_table` | Maximum number of indexes that can be recommended for each table. | `10` | `1 - 25` | |
| `index_tuning.max_queries_per_database` | Number of slowest queries per database for which indexes can be recommended. | `25` | `5 - 100` | |
| `index_tuning.max_regression_factor` | Acceptable regression introduced by a recommended index on any of the queries analyzed during one optimization session. | `0.1` | `0.05 - 0.2` | percentage |
| `index_tuning.max_total_size_factor` | Maximum total size, in percentage of total disk space, that all recommended indexes for any given database can use. | `0.1` | `0 - 1` | percentage |
| `index_tuning.min_improvement_factor` | Cost improvement that a recommended index must provide to at least one of the queries analyzed during one optimization session. | `0.2` | `0 - 20` | percentage |
| `index_tuning.mode` | Configures index optimization as disabled (`OFF`) or enabled to only emit recommendation. Requires query store to be enabled by setting `pg_qs.query_capture_mode` to `TOP` or `ALL`. | `OFF` | `OFF, REPORT` | |
| `index_tuning.unused_dml_per_table` | Minimum number of daily average DML operations affecting the table, so their unused indexes are considered for dropping. | `1000` | `0 - 9999999` | |
| `index_tuning.unused_min_period` | Minimum number of days the index hasn't been used, based on system statistics, so it's considered for dropping. | `35` | `30 - 70` | |
| `index_tuning.unused_reads_per_table` | Minimum number of daily average read operations affecting the table so that their unused indexes are considered for dropping. | `1000` | `0 - 9999999` | |

If you use the CLI commands `az postgres flexible-server autonomous-tuning show-settings` and `az postgres flexible-server autonomous-tuning set-settings` to display or modify any of the autonomous tuning settings, the values accepted as arguments for the `--name` parameter are the ones shown in the **Parameter** column of the previous table, but without including the prefix `index_tuning.`.

## Information produced by autonomous tuning

[Use autonomous tuning recommendations](how-to-get-apply-recommendations-from-autonomous-tuning.md) describes in full detail how to obtain and use the recommendations produced by autonomous tuning.

## Limitations and supportability

Following is the list of limitations and supportability scope for autonomous tuning.

### Automatic deletion of recommendations

Recommendations are automatically deleted 35 days after the last time they are produced. For this automatic deletion mechanism to work, autonomous tuning must be enabled.

### Dependency on hypopg extension

For autonomous tuning to produce CREATE INDEX recommendations, it uses the [hypopg](https://github.com/HypoPG/hypopg/) extension.

If the extension already exists when a tuning session begins, it is used on the schema in which it was created. And when the tuning session finishes, the extension is not dropped. An exception to this is if the extension was created in the `pg_catalog` schema. If that's the case, autonomous tuning drops the extension.

If the extension didn't exist in the first place or we dropped it because it was created in `pg_catalog` schema, autonomous tuning will create it under a schema called `ms_temp_recommendations709253` and, when the tuning session finishes successfully, it drops the extension and removes the schema.

Users who are members of the `azure_pg_admin` role can drop the hypopg extension at any point in time, even when it was created by the autonomous tuning feature. However, dropping it while an autonomous tuning session is running might cause that session to fail and don't produce any recommendations.

### Supported compute tiers and SKUs

Autonomous tuning is supported on all [currently available tiers](../compute-storage/concepts-compute.md): Burstable, General Purpose, and Memory Optimized, and on any [currently supported compute SKU](../compute-storage/concepts-compute.md) with at least 4 vCores.

### Supported versions of PostgreSQL

Autonomous tuning is supported on [major versions](../configure-maintain/concepts-supported-versions.md) **12 or greater** of Azure Database for PostgreSQL flexible server instances.

### Use of search_path

Autonomous tuning consumes the value persisted in column `search_path` of [query_store.qs_view](concepts-query-store.md#query_storeqs_view), so that when each query is analyzed, the same value of `search_path` that was set when the query executed originally is the one to which it's set to analyze possible recommendations.

### Parameterized queries

Parameterized queries created with [PREPARE](https://www.postgresql.org/docs/current/sql-prepare.html) or using the [extended query protocol](https://www.postgresql.org/docs/current/protocol-flow.html#PROTOCOL-FLOW-EXT-QUERY) are parsed and analyzed to produce index recommendations on them.

For the analysis of parameterized queries, autonomous tuning requires that [pg_qs.parameters_capture_mode](concepts-query-store.md#configuration-options) is set to `capture_first_sample` when query store captures the execution of the query. It also requires that the parameters are correctly captured by query store when the query is executed. In other words, for the query being analyzed, [query_store.qs_view](concepts-query-store.md#query_storeqs_view) must have its column `parameters_capture_status` set to `succeeded`.

### Read-only mode and read replicas

Because autonomous tuning relies on the data that [query store](concepts-query-store.md) persists locally to the `azure_sys` database, which is [not supported in read replicas or when an instance is in read-only mode](concepts-query-store.md#read-only-mode), we don't support it on read replicas or on instances which are in read-only mode.

Any recommendations seen on a read replica were produced on the primary replica after analyzing exclusively the workload that executed on the primary replica.

### Scale down of compute

If autonomous tuning is enabled on a server, and you scale down that server's compute to less than the minimum number of required vCores, the feature remains enabled. Because the feature isn't supported on servers with less than 4 vCores, it doesn't run to analyze the workload and produce recommendations, even if `index_tuning.mode` was set to `ON` when the compute was scaled down. While the server doesn't meet the minimum requirements, all `index_tuning.*` server parameters are inaccessible. Whenever you scale your server back up to a compute that meets the minimum requirements, `index_tuning.mode` is configured with whatever value it was set before you scaled it down to a compute which didn't meet the requirements.

### High availability and read replicas

If you have [high availability](/azure/reliability/reliability-postgresql-flexible-server) or [read replicas](../read-replica/concepts-read-replicas.md) configured on your server, be aware of the implications associated with producing write-intensive workloads on the primary server when implementing the recommended indexes. Be especially careful when creating indexes whose size is estimated to be large.

### Reasons why autonomous tuning might not produce create index recommendations for certain queries

Following is a list of query types for which autonomous tuning won't generate CREATE INDEX recommendations. Those which:

- Encounter an error when autonomous tuning engine tries to obtain its EXPLAIN output during the analysis phase.
- Reference tables that don't have statistics about their contents in the pg_statistic system catalog. Run [ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html) on those tables so that the tuning engine can tae into consideration these queries in the future.
- Have the query text truncated in query store. That's the case when the length of query text exceeds the value configured in [pg_qs.max_query_text_length](concepts-query-store.md#configuration-options).
- Reference objects that were dropped or renamed before the analysis occurs. These queries could still be syntactically valid, but not semantically valid.
- Access temporary tables or indexes on temporary tables.
- Access views or materialized views.
- Access partitioned tables.
- Are identified as utility statements. Utility statements or utility commands are, basically, any statement not considered SELECT, INSERT, UPDATE, DELETE, or MERGE, and certain commands containing one of these.
- Are not among the top [index_tuning.max_queries_per_database](concepts-autonomous-tuning.md#configuring-autonomous-tuning) slowest, for the database and period analyzed.
- Were run in the context of one specific database, when none of those queries were identified as the top slowest at the server level.

## Related content

- [Query store](concepts-query-store.md).
- [Configure autonomous tuning](how-to-configure-autonomous-tuning.md).
- [Use autonomous tuning recommendations](how-to-get-apply-recommendations-from-autonomous-tuning.md).