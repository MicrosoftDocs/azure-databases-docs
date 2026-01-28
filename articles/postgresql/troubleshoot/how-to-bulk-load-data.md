---
title: Upload Data in Bulk
description: This article discusses best practices for uploading data in bulk to an Azure Database for PostgreSQL flexible server instance.
author: sarat0681
ms.author: sbalijepalli
ms.reviewer: maghan
ms.date: 12/16/2024
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: best-practice
ai.usage: ai-assisted
---

# Best practices to bulk upload data to Azure Database for PostgreSQL 

This article discusses various methods for loading data in bulk to an Azure Database for PostgreSQL flexible server instance, along with best practices for both initial data loads in empty databases and incremental data loads.

## Loading methods

The following data-loading methods are arranged in order from most time-consuming to least time-consuming:

- Run a single-record `INSERT` command.
- Batch into 100 to 1,000 rows per commit. You can use a transaction block to wrap multiple records per commit.
- Run `INSERT` with multiple row values.
- Run the `COPY` command.

The preferred method for loading data into a database is the `COPY` command. If the `COPY` command isn't impossible, batch `INSERT` is the next best method. Multi-threading with a `COPY` command is optimal for loading data in bulk.

## Steps to upload bulk data

Here are steps to bulk upload data to an Azure Database for PostgreSQL flexible server instance.

### Step 1: Prepare your data

Ensure your data is clean and properly formatted for the database.

### Step 2: Choose the loading method

Select the appropriate loading method based on the size and complexity of your data.

### Step 3: Execute the loading method

Run the chosen loading method to upload your data to the database.

### Step 4: Verify the data

After uploading, verify that the data has been correctly loaded into the database.

## Best practices for initial data loads

Here are best practices for initial data loads.

### Drop indexes

Before you do an initial data load, we recommend dropping all the indexes in the tables. Creating the indexes after the data is loaded is always more efficient.

### Drop constraints

The main drop constraints are described here:

- **Unique key constraints**

To achieve strong performance, we recommend dropping unique key constraints before an initial data load and re-creating them after the data load is completed. However, dropping unique key constraints cancels the safeguards against duplicated data.

- **Foreign key constraints**

We recommend dropping foreign key constraints before the initial data load and re-creating them after the data load is completed.

Changing the `session_replication_role` parameter to `replica` also disables all foreign key checks. However, if the change isn't properly used, it can leave data inconsistent.

### Unlogged tables

Consider the pros and cons of unlogged tables before using them in initial data loads.

Using unlogged tables speeds up data loading. Data written to unlogged tables isn't written to the write-ahead log.

The disadvantages of using unlogged tables are:
- They aren't crash-safe. An unlogged table is automatically truncated after a crash or unclean shutdown.
- Data from unlogged tables can't be replicated to standby servers.

To create an unlogged table or change an existing table to an unlogged table, use the following options:

- Create a new unlogged table by using the following syntax:

    ```sql
    CREATE UNLOGGED TABLE <tablename>;
    ```

- Convert an existing logged table to an unlogged table by using the following syntax:

    ```sql
    ALTER TABLE <tablename> SET UNLOGGED;
    ```

### Server parameter tuning

- `auto vacuum': It's best to turn off `auto vacuum' during the initial data load. After the initial load is completed, we recommend that you run a manual `VACUUM ANALYZE` on all tables in the database and then turn on `auto vacuum`.

> [!NOTE]  
> Follow the recommendations here only if there's enough memory and disk space.

- `maintenance_work_mem`: Can be set to a maximum of 2 gigabytes (GB) on an Azure Database for PostgreSQL flexible server instance. `maintenance_work_mem` helps in speeding up auto vacuum, index, and foreign key creation.

- `checkpoint_timeout`: On an Azure Database for PostgreSQL flexible server instance, the `checkpoint_timeout` value can be increased to a maximum of 24 hours from the default setting of 5 minutes. We recommend increasing the value to 1 hour before you initially load data on the Azure Database for PostgreSQL flexible server instance.

- `checkpoint_completion_target`: We recommend a value of 0.9.

- `max_wal_size`: Can be set to the maximum allowed value on an Azure Database for PostgreSQL flexible server instance, which is 64 GB while you're doing the initial data load.

- `wal_compression`: This can be turned on. Enabling this parameter can incur some extra CPU costs for compression during write-ahead log (WAL) logging and decompression during WAL replay.

### Recommendations

Before you begin an initial data load on the Azure Database for PostgreSQL flexible server instance, we recommend that you:

- Disable high availability on the server. You can enable it after the initial load is completed on the primary.
- Create read replicas after the initial data load is completed.
- Make logging minimal or disable it all together during initial data loads (for example, disable pgaudit, pg_stat_statements, query store).

### Re-create indexes and add constraints

Assuming that you dropped the indexes and constraints before the initial load, we recommend using high values in `maintenance_work_mem` (as mentioned earlier) to create indexes and add constraints. In addition, starting with PostgreSQL version 11, the following parameters can be modified for faster parallel index creation after the initial data load:

- `max_parallel_workers`: Sets the maximum number of workers the system can support for parallel queries.

- `max_parallel_maintenance_workers`: Controls the maximum number of worker processes, which can be used in `CREATE INDEX`.

You can also create the indexes by making the recommended settings at the session level. Here's an example of how to do it:

```sql
SET maintenance_work_mem = '2GB';
SET max_parallel_workers = 16;
SET max_parallel_maintenance_workers = 8;
CREATE INDEX test_index ON test_table (test_column);
```

## Best practices for incremental data loads

Best practices for incremental data loads are described here:.

### Partition tables

We always recommend that you partition large tables. Some advantages of partitioning, especially during incremental loads, include:
- Creating new partitions based on new deltas makes adding new data to the table efficient.
- Maintaining tables becomes easier. You can drop a partition during an incremental data load to avoid time-consuming deletions in large tables.
- Autovacuum would be triggered only on partitions that were changed or added during incremental loads, which make maintaining statistics on the table easier.

### Maintain up-to-date table statistics

Monitoring and maintaining table statistics is important for query performance on the database. This also includes scenarios where you have incremental loads. PostgreSQL uses the autovacuum daemon process to clean up dead tuples and analyze the tables to keep the statistics updated. For more information, see [Autovacuum monitoring and tuning](how-to-autovacuum-tuning.md).

### Create indexes on foreign key constraints

Creating indexes on foreign keys in the child tables can be beneficial in the following scenarios:
- Data updates or deletions in the parent table. When data is updated or deleted in the parent table, lookups are performed on the child table. You could index foreign keys on the child table to make lookups faster.
- Queries, where you can see parent and child tables joining on key columns.

### Identify unused indexes

Identify unused indexes in the database and drop them. Indexes are an overhead on data loads. The fewer the indexes on a table, the better the performance during data ingestion.

You can identify unused indexes in two ways: by Query Store and an index usage query.

**Query Store**

The Query Store feature helps identify indexes, which can be dropped based on query usage patterns on the database. For step-by-step guidance, see [Query Store](../monitor/concepts-query-store.md).

After you've enabled Query Store on the server, you can use the following query to identify indexes that can be dropped by connecting to azure_sys database.

```sql
SELECT * FROM IntelligentPerformance.DropIndexRecommendations;
```

**Index usage**

You can also use the following query to identify unused indexes:

```sql
SELECT
    t.schemaname,
    t.tablename,
    c.reltuples::bigint                            AS num_rows,
 pg_size_pretty(pg_relation_size(c.oid))        AS table_size,
    psai.indexrelname                              AS index_name,
 pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    CASE WHEN i.indisunique THEN 'Y' ELSE 'N' END AS "unique",
    psai.idx_scan                                  AS number_of_scans,
    psai.idx_tup_read                              AS tuples_read,
    psai.idx_tup_fetch                             AS tuples_fetched
FROM
 pg_tables t
    LEFT JOIN pg_class c ON t.tablename = c.relname
    LEFT JOIN pg_index i ON c.oid = i.indrelid
    LEFT JOIN pg_stat_all_indexes psai ON i.indexrelid = psai.indexrelid
WHERE
    t.schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY 1, 2;
```

The `number_of_scans`, `tuples_read`, and `tuples_fetched` columns would indicate the index usage.number_of_scans column value of zero points as an index that's not being used.

### Server parameter tuning

> [!NOTE]  
> Follow the recommendations in the following parameters only if there's enough memory and disk space.

- `maintenance_work_mem`: This parameter can be set to a maximum of 2 GB on the Azure Database for PostgreSQL flexible server instance. `maintenance_work_mem` helps speed up index creation and foreign key additions.

- `checkpoint_timeout`: On the Azure Database for PostgreSQL flexible server instance, the `checkpoint_timeout` value can be increased to 10 or 15 minutes from the default setting of 5 minutes. Increasing `checkpoint_timeout` to a more significant value, such as 15 minutes, can reduce the I/O load, but the downside is that it takes longer to recover if there's a crash. We recommend careful consideration before you make the change.

- `checkpoint_completion_target`: We recommend a value of 0.9.

- `max_wal_size`: This value depends on SKU, storage, and workload. The following example shows one way to arrive at the correct value for `max_wal_size`.

During peak business hours, arrive at a value by doing the following:

a. Take the current WAL log sequence number (LSN) by running the following query:

```sql
SELECT pg_current_wal_lsn ();
``` 

b. Wait for the `checkpoint_timeout` number of seconds. Take the current WAL LSN by running the following query:

```sql
SELECT pg_current_wal_lsn ();
```

c. Use the two results to check the difference in GB:

```sql
SELECT round (pg_wal_lsn_diff('LSN value when running the second time','LSN value when run the first time')/1024/1024/1024,2) WAL_CHANGE_GB;
```

- `wal_compression`: This can be turned on. Enabling this parameter can incur an extra CPU cost for compressing during WAL logging and decompressing during WAL replay.

## Related content

- [Troubleshoot high CPU utilization in Azure Database for PostgreSQL](how-to-high-cpu-utilization.md).
- [Troubleshoot high memory utilization in Azure Database for PostgreSQL](how-to-high-memory-utilization.md).
- [Troubleshoot and identify slow-running queries in Azure Database for PostgreSQL](how-to-identify-slow-queries.md).
- [Server parameters in Azure Database for PostgreSQL](../server-parameters/concepts-server-parameters.md).
- [Autovacuum tuning in Azure Database for PostgreSQL](how-to-autovacuum-tuning.md).
