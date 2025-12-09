---
title: Query store
description: This article describes the query store feature for Azure Database for PostgreSQL flexible server instance.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 02/24/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.custom:
  - ignite-2024
ms.topic: how-to
---

# Query store

Query store is a feature in an Azure Database for PostgreSQL flexible server instance that provides a way to track query performance over time. Query store simplifies the troubleshooting of performance issues by helping you quickly find the longest running and most resource-intensive queries. Query store automatically captures a history of queries and runtime statistics, and retains them for your review. It slices the data by time so that you can see temporal usage patterns. Data for all users, databases, and queries is stored in a database named `azure_sys` in the Azure Database for PostgreSQL flexible server instance.

## Enable query store

Query store is available to use with no extra charges. It's an opt-in feature, so it isn't enabled by default on a server. Query store can be enabled or disabled globally for all databases on a given server and can't be turned on or off per database.

> [!IMPORTANT]  
> Do not enable query store on Burstable pricing tier as it would cause performance impact.

### Enable query store in Azure portal

1. Sign in to the Azure portal and select your Azure Database for PostgreSQL flexible server instance.
1. Select **Server parameters** in the **Settings** section of the menu.
1. Search for the `pg_qs.query_capture_mode` parameter.
1. Set the value to `top` or `all`, depending on whether you want to track top-level queries or also nested queries (the ones which execute inside a function or procedure), and select **Save**.
Allow up to 20 minutes for the first batch of data to persist in the `azure_sys` database.

### Enable query store wait sampling

1. Search for the `pgms_wait_sampling.query_capture_mode` parameter.
1. Set the value to `all` and **Save**.

## Information in query store

#### Query store consists of two stores:
- A runtime stats store for persisting the query execution statistics information.
- A wait stats store for persisting wait statistics information.

#### Common scenarios for using query store include:
- Determining the number of times a query was executed in a given time window.
- Comparing the average execution time of a query across time windows to see large variations.
- Identifying longest running queries in the past few hours.
- Identifying top N queries that are waiting on resources.
- Understanding nature of the waits for a particular query.

To minimize space usage, the runtime execution statistics in the runtime stats store are aggregated over a fixed, configurable time window. The information in these stores can be queried using views.

## Access query store information

Query store data is stored in the `azure_sys` database on your Azure Database for PostgreSQL flexible server instance.
The following query returns information about queries which were recorded in query store:

```sql
SELECT * FROM  query_store.qs_view;
```
And this query returns information about waiting statistics:

```sql
SELECT * FROM  query_store.pgms_wait_sampling_view;
```

## Find wait queries

Wait event types combine different wait events into buckets by similarity. Query store provides the wait event type, specific wait event name, and the query in question. Being able to correlate this wait information with the query runtime statistics means you can gain a deeper understanding of what contributes to query performance characteristics.

Here are some examples of how you can gain more insights into your workload using the wait statistics in query store:

| **Observation** | **Action** |
| --- | --- |
| High lock waits | Check the query texts for the affected queries and identify the target entities. Look in query store for other queries which are executed frequently and/or have high duration and are modifying the same entity. After identifying these queries, consider changing the application logic to improve concurrency, or use a less restrictive isolation level. |
| High buffer IO waits | Find the queries with a high number of physical reads in query store. If they match the queries with high IO waits, consider enabling the [automated index tuning](concepts-index-tuning.md) feature to see if it can recommend creating some indexes which might decrease the number of physical reads for those queries. |
| High memory waits | Find the top memory consuming queries in query store. These queries are probably delaying further progress of the affected queries. |

## Configuration options

When query store is enabled, it saves data in aggregation windows of length determined by the [pg_qs.interval_length_minutes](../server-parameters/param-customized-options.md#pg_qsinterval_length_minutes) server parameter (defaults to 15 minutes). For each window, it stores up to 500 distinct queries per window. Attributes that distinguish the uniqueness of each query are user_id (identifier of the user who executes the query), db_id (identifier of the database in whose context the query executes), and query_id (an integer value uniquely identifying the query executed). If the number of distinct queries reaches 500 during the configured interval, 5% of the ones that are recorded are deallocated to make room for more. The ones deallocated first are the ones which were executed the least number of times.

The following options are available for configuring Query Store parameters:

| **Parameter** | **Description** | **Default** | **Range** |
| --- | --- | --- | --- |
| `pg_qs.interval_length_minutes` (*) | Capture interval in minutes for query store. Defines the frequency of data persistence. | `15` | `1` - `30` |
| `pg_qs.is_enabled_fs` | Internal Use Only: This parameter is used as a feature override switch. If it shows as off, query store is disabled, despite the value set for `pg_qs.query_capture_mode`. | `on` | `on`, `off` |
| `pg_qs.max_plan_size` | Maximum number of bytes saved from query plan text by query store; longer plans are truncated. | `7500` | `100` - `10000` |
| `pg_qs.max_query_text_length` | Maximum query length that can be saved; longer queries are truncated. | `6000` | `100` - `10000` |
| `pg_qs.parameters_capture_mode` | Whether and when to capture query positional parameters. | `capture_parameterless_only` | `capture_parameterless_only`, `capture_first_sample` |
| `pg_qs.query_capture_mode` | Statements to track. | `none` | `none`, `top`, `all` |
| `pg_qs.retention_period_in_days` | Retention period window in days for query store. Older data is automatically deleted. | `7` | `1` - `30` |
| `pg_qs.store_query_plans` | Whether query plans should be saved in query store. | `off` | `on`, `off` |
| `pg_qs.track_utility` | Whether query store must track utility commands. | `on` | `on`, `off` |

(*) Static server parameter which requires a server restart for a change in its value to take effect. 

> [!NOTE]  
> If you change the value for `pg_qs.max_query_text_length` parameter, the text of all queries that were captured before you make the change continue to use the same query_id and sql_query_text. It might give the impression that the new value doesn't take effect but, for queries that weren't recorded in query store before, you will see that the query text uses the newly configured maximum length. This is by design, and is explained at [Views and functions](#views-and-functions). If you execute [query_store.qs_reset](#query_storeqs_reset), it removes all the information recorded by query store until now, including the text that was captured for each query ID, and if any of those queries is executed again, the newly configured maximum length is applied to the text being captured.


The following options apply specifically to wait statistics:

| **Parameter** | **Description** | **Default** | **Range** |
| --- | --- | --- | --- |
| `pgms_wait_sampling.history_period` | Frequency, in milliseconds, at which wait events are sampled. | `100` | `1` - `600000` |
| `pgms_wait_sampling.is_enabled_fs` | Internal Use Only: This parameter is used as a feature override switch. If it shows as `off`, wait sampling is disabled despite the value set for `pgms_wait_sampling.query_capture_mode`. | `on` | `on`, `off` |
| `pgms_wait_sampling.query_capture_mode` | Which statements the `pgms_wait_sampling` extension must track. | `none` | `none`, `all` |

> [!NOTE]  
> `pg_qs.query_capture_mode` supersedes `pgms_wait_sampling.query_capture_mode`. If `pg_qs.query_capture_mode` is `none`, the `pgms_wait_sampling.query_capture_mode` setting has no effect.

Use the [Azure portal](../server-parameters/how-to-server-parameters-list-all.md) to get or set a different value for a parameter.

## Views and functions

You can query the information recorded by query store and or delete it using some views and functions available in the `query_store` schema of the `azure_sys` database. Anyone in the PostgreSQL public role can use these views to see the data in query store. These views are only available in the **azure_sys** database.

Queries are normalized by looking at their structure and ignoring anything not semantically significant, like literals, constants, aliases, or differences in casing.

If two queries are semantically identical, even if they use different aliases for the same referenced columns and tables, they're identified with the same query_id. If two queries only differ in the literal values used in them, they're also identified with the same query_id. For queries identified with the same query_id, their sql_query_text is that of the query that executed first since query store started recording activity, or since the last time the persisted data was discarded because the function [query_store.qs_reset](#query_storeqs_reset) was executed.

### How query normalization works

Following are some examples to try to illustrate how this normalization works:

Say that you create a table with the following statement:

```sql
create table tableOne (columnOne int, columnTwo int);
```

You enable Query Store data collection, and a single or multiple users execute the following queries, in this exact order:

```sql
select * from tableOne;
select columnOne, columnTwo from tableOne;
select columnOne as c1, columnTwo as c2 from tableOne as t1;
select columnOne as "column one", columnTwo as "column two" from tableOne as "table one";
```

All the previous queries share the same query_id. And the text that Query Store keeps is that of the first query executed after enabling data collection. Therefore, it would be `select * from tableOne;`.

The following set of queries, once normalized, don't match the previous set of queries because the WHERE clause makes them semantically different:

```sql
select columnOne as c1, columnTwo as c2 from tableOne as t1 where columnOne = 1 and columnTwo = 1;
select * from tableOne where columnOne = -3 and columnTwo = -3;
select columnOne, columnTwo from tableOne where columnOne = '5' and columnTwo = '5';
select columnOne as "column one", columnTwo as "column two" from tableOne as "table one" where columnOne = 7 and columnTwo = 7;
```

However, all queries in this last set share the same query_id and the text used to identify them all is that of the first query in the batch `select columnOne as c1, columnTwo as c2 from tableOne as t1 where columnOne = 1 and columnTwo = 1;`.

Finally, find below some queries not matching the query_id of the ones in the previous batch, and the reason why they don't:

**Query**:
```sql
select columnTwo as c2, columnOne as c1 from tableOne as t1 where columnOne = 1 and columnTwo = 1;
```
**Reason for not matching**:
List of columns refers to the same two columns (columnOne and ColumnTwo), but the order in which they're referred is reversed, from `columnOne, ColumnTwo` in the previous batch to `ColumnTwo, columnOne` in this query.

**Query**:
```sql
select * from tableOne where columnTwo = 25 and columnOne = 25;
```
**Reason for not matching**:
Order in which the expressions evaluated in the WHERE clause are referred is reversed from `columnOne = ? and ColumnTwo = ?` in the previous batch to `ColumnTwo = ? and columnOne = ?` in this query.

**Query**:
```sql
select abs(columnOne), columnTwo from tableOne where columnOne = 12 and columnTwo = 21;
```
**Reason for not matching**:
The first expression in the column list isn't `columnOne` anymore, but function `abs` evaluated over `columnOne` (`abs(columnOne)`), which isn't semantically equivalent.

**Query**:
```sql
select columnOne as "column one", columnTwo as "column two" from tableOne as "table one" where columnOne = ceiling(16) and columnTwo = 16;
```
**Reason for not matching**:
The first expression in the WHERE clause doesn't evaluate the equality of `columnOne` with a literal anymore, but with the result of function `ceiling` evaluated over a literal, which isn't semantically equivalent.


### Views


#### query_store.qs_view

This view returns all the data that is persisted in the supporting tables of query store. Data that is still recording  in-memory for the currently active time window, isn't visible until the time window comes to an end, and its in-memory volatile data is collected and persisted to tables stored on disk. This view returns a different row for each distinct database (db_id), user (user_id), and query (query_id).

| **Name** | **Type** | **References** | **Description** |
| --- | --- | --- | --- |
| `runtime_stats_entry_id` | bigint | | ID from the runtime_stats_entries table. |
| `user_id` | oid | pg_authid.oid | OID of user who executed the statement. |
| `db_id` | oid | pg_database.oid | OID of database in which the statement was executed. |
| `query_id` | bigint | | Internal hash code, computed from the statement's parse tree. |
| `query_sql_text` | varchar(10000) | | Text of a representative statement. Different queries with the same structure are clustered together; this text is the text for the first of the queries in the cluster. The default value for the maximum query text length is 6000, and can be modified using query store parameter `pg_qs.max_query_text_length`. If the text of the query exceeds this maximum value, it's truncated to the first `pg_qs.max_query_text_length` bytes. |
| `plan_id` | bigint | | ID of the plan corresponding to this query. |
| `start_time` | timestamp | | Queries are aggregated by time windows. Server parameter `pg_qs.interval_length_minutes` defines the time span of those windows (default is 15 minutes). This column corresponds to the start time of the window in which this entry was recorded. |
| `end_time` | timestamp | | End time corresponding to the time window for this entry. |
| `calls` | bigint | | Number of times the query executed in this time window. Notice that for parallel queries, the number of calls for each execution corresponds to 1 for the backend process that drives the execution of the query, plus as many other units for each backend worker process which launches to collaborate executing the parallel branches of the execution tree. |
| `total_time` | double precision | | Total query execution time, in milliseconds. |
| `min_time` | double precision | | Minimum query execution time, in milliseconds. |
| `max_time` | double precision | | Maximum query execution time, in milliseconds. |
| `mean_time` | double precision | | Mean query execution time, in milliseconds. |
| `stddev_time` | double precision | | Standard deviation of the query execution time, in milliseconds. |
| `rows` | bigint | | Total number of rows retrieved or affected by the statement. Notice that for parallel queries, the number of rows for each execution corresponds to the number of rows returned to the client by the backend process that drives the execution of the query, plus the sum of all rows that each backend worker process, launched to collaborate executing the parallel branches of the execution tree, returns to the backend process that drives the execution of the query. |
| `shared_blks_hit` | bigint | | Total number of shared block cache hits by the statement. |
| `shared_blks_read` | bigint | | Total number of shared blocks read by the statement. |
| `shared_blks_dirtied` | bigint | | Total number of shared blocks dirtied by the statement. |
| `shared_blks_written` | bigint | | Total number of shared blocks written by the statement. |
| `local_blks_hit` | bigint | | Total number of local block cache hits by the statement. |
| `local_blks_read` | bigint | | Total number of local blocks read by the statement. |
| `local_blks_dirtied` | bigint | | Total number of local blocks dirtied by the statement. |
| `local_blks_written` | bigint | | Total number of local blocks written by the statement. |
| `temp_blks_read` | bigint | | Total number of temp blocks read by the statement. |
| `temp_blks_written` | bigint | | Total number of temp blocks written by the statement. |
| `blk_read_time` | double precision | | Total time the statement spent reading blocks, in milliseconds (if track_io_timing is enabled, otherwise zero). |
| `blk_write_time` | double precision | | Total time the statement spent writing blocks, in milliseconds (if track_io_timing is enabled, otherwise zero). |
| `is_system_query` | boolean | | Determines whether role with user_id = 10 (azuresu) executed the query. That user has superuser privileges and is used to perform control plane operations. Since this service is a managed PaaS service, only Microsoft is part of that superuser role. |
| `query_type` | text | | Type of operation represented by the query. Possible values are `unknown`, `select`, `update`, `insert`, `delete`, `merge`, `utility`, `nothing`, `undefined`. |
| `search_path` | text | | Value of search_path set at the time the query was captured. |
| `query_parameters` | text | | Text representation of a JSON object with the values passed to the positional parameters of a parameterized query. This column only populates its value in two cases: 1) for nonparameterized queries. 2) For parameterized queries, when `pg_qs.parameters_capture_mode` is set to `capture_first_sample`, and if query store can fetch the values for the parameters of the query at execution time. |
| `parameters_capture_status` | text | | Type of operation represented by the query. Possible values are `succeeded` (either the query wasn't parameterized or it was a parameterized query and values were successfuly captured), `disabled` (query was parameterized but, parameters weren't captured because `pg_qs.parameters_capture_mode` was set to `capture_parameterless_only`), `too_long_to_capture` (query was parameterized, but parameters weren't captured because the length of the resulting JSON that would be surfaced in the `query_parameters` column of this view, was considered excessively long for query store to persist), `too_many_to_capture` (query was parameterized, but parameters weren't captured because the total number of parameters, were considered excessive for query store to persist), `serialization_failed` (query was parameterized, but at least one of the values passed as a parameter couldn't be serialized to text). |

#### query_store.query_texts_view

This view returns query text data in Query Store. There's one row for each distinct query_sql_text.

| **Name** | **Type** | **Description** |
|--| -- |--|
| `query_text_id` | bigint | ID for the query_texts table |
| `query_sql_text` | varchar(10000) | Text of a representative statement. Different queries with the same structure are clustered together; this text is the text for the first of the queries in the cluster. |
| `query_type` | smallint | Type of operation represented by the query. In version of PostgreSQL <= 14, possible values are `0` (unknown), `1` (select), `2` (update), `3` (insert), `4` (delete), `5` (utility), `6` (nothing). In version of PostgreSQL >= 15, possible values are `0` (unknown), `1` (select), `2` (update), `3` (insert), `4` (delete), `5` (merge), `6` (utility), `7` (nothing). |

#### query_store.pgms_wait_sampling_view

This view returns wait events data in Query Store. This view returns a different row for each distinct database (db_id), user (user_id), query (query_id), and event (event).

| **Name** | **Type** | **References** | **Description** |
|--|--|--|--|
| `start_time` | timestamp | | Queries are aggregated by time windows. Server parameter `pg_qs.interval_length_minutes` defines the time span of those windows (default is 15 minutes). This column corresponds to the start time of the window in which this entry was recorded. |
| `end_time` | timestamp | | End time corresponding to the time window for this entry. |
| `user_id` | oid | pg_authid.oid | Object identifier of user who executed the statement. |
| `db_id` | oid | pg_database.oid | Object identifier of database in which the statement was executed. |
| `query_id` | bigint | | Internal hash code, computed from the statement's parse tree. |
| `event_type` | text | | The type of event for which the backend is waiting. |
| `event` | text | | The wait event name if backend is currently waiting. |  
| `calls` | integer | | Number of times the same event was captured. |

> [!NOTE]  
> For a list of possible values in the `event_type` and `event` columns of the `query_store.pgms_wait_sampling_view` view, refer to the official documentation of [pg_stat_activity](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW) and look for the information referring to columns with the same names.


#### query_store.query_plans_view

This view returns the query plan that was used to execute a query. There's one row per each distinct database ID, and query ID. Query store only records query plans for nonutility queries.

| **Name** | **Type** | **References** | **Description** |
|--|--|--|--|
| `plan_id` | bigint | | The hash value from the normalized query plan produced by [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html). It's in normalized form because it excludes the estimated costs of plan nodes and usage of buffers. |
| `db_id` | oid | pg_database.oid | OID of database in which the statement was executed. |
| `query_id` | bigint | | Internal hash code, computed from the statement's parse tree. |
| `plan_text` | varchar(10000) | | Execution plan of the statement given costs=false, buffers=false, and format=text. Identical output as the one produced by [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html). |


### Functions


#### query_store.qs_reset

This function discards all statistics gathered so far by query store. It discards the statistics for already closed time windows, which are already persisted to on-disk tables. It also discards the statistics for the current time window, which only exist in-memory. Only members of the server admin role (`azure_pg_admin`) can execute this function.


#### query_store.staging_data_reset

This function discards all statistics gathered in-memory by query store (that is, the data in memory that isn't flushed yet to the on disk tables supporting persistence of collected data for query store). Only members of the server admin role (`azure_pg_admin`) can execute this function.

### Read-only mode
When an Azure Database for PostgreSQL flexible server instance is in read-only mode, such as when the `default_transaction_read_only` parameter is set to `on`, or if read-only mode is [automatically enabled due to reaching storage capacity](../configure-maintain/concepts-limits.md#storage), query store doesn't capture any data.

Enabling query store on a server that has [read replicas](../read-replica/concepts-read-replicas.md), doesn't automatically enable query store on any of the read replicas. Even if you enable it on any of the read replicas, query store doesn't record the queries executed on any read replicas, because they operate in read-only mode until you promote them to primary.

## Related content

- [Usage scenarios for query store](concepts-query-store-scenarios.md)
- [Best practices for query store](concepts-query-store-best-practices.md)
- [Query Performance Insight](concepts-query-performance-insight.md)
