---
title: Best practices to migrate from Oracle into Flexible Server
description: Best practices for migrations from Oracle into Azure Database for PostgreSQL.
author: jaredmeade
ms.author: jaredmeade
ms.reviewer: tbd
ms.date: 12/11/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual

---

# Best practices for migrations from Oracle into Azure Database for PostgreSQL.

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The following scenarios outline some of the potential challenges which may be encountered during an Oracle to Azure Postgres migration.  The recommended solutions can be helpful when planning and executing your own migration(s).

**Scenario:** Two separate low-latency client applications were discovered to be connected to the same database.  Each system was inadvertently bumping the other cached queries out of the buffers.  The shared load and combined resource contention created a situation wherein the database’s shared buffers were being flushed too frequently, resulting in degraded performance across both systems.  

**Recommended Solution:** Ensure that your initial assessments are capturing ALL aspects of your database platform environment, including the memory consumption by both systems global area (SGA) and program global area (PGA) memory structures.  Select the appropriate family of compute that matches your resource requirements and ensure your Postgres planned capacity is adjusted as required.

> [!TIP]
> The **pg_buffercache** extension provides a means for examining the utilization and allows you to observe what’s happening in the shared buffer cache in real time.

#### Buffer Cache Hit Ratio
Examining hit ratios allows you to evaluate cache effectiveness and determine whether shared buffer size is appropriate.  A good cache hit ratio is a sign that most data requests are being served from memory rather than disk, providing optimal performance:

```sql
SELECT COUNT(*) AS total
, SUM(CASE WHEN isdirty THEN 1 ELSE 0 END) AS dirty -- # of buffers out of sync with disk
, SUM(CASE WHEN isdirty THEN 0 ELSE 1 END) AS clean -- # of buffers in sync with data on disk
FROM pg_buffercache;
```

#### Most Frequently Accessed Tables & Indexes
Examining which tables and indexes are most frequently accessed and/or occupying the most space in the buffer cache can help identify hotspots being cached in memory:

```sql
SELECT b.relfilenode, relname, relblocknumber
, relkind 
--r = ordinary table, i = index, S = sequence, t = TOAST table
--, v = view, m = materialized view, c = composite type
--, f = foreign table, p = partitioned table, I = partitioned index
, COUNT(*) AS buffers
FROM pg_buffercache b
JOIN pg_class c ON c.oid = b.relfilenode
GROUP BY b.relfilenode, relname, relblocknumber, relkind
ORDER BY buffers DESC
LIMIT 10;
```

#### Buffer Cache Contention
Significant contention in your buffer cache indicates queries might be fighting for the same buffers, leading to performance bottlenecks.  Examining the location and frequency of buffer access can help in diagnosing such issues:

```sql
SELECT c.relname, b.relblocknumber, COUNT(*) AS access_count
FROM pg_buffercache b
JOIN pg_class c ON c.relfilenode = b.relfilenode
GROUP BY c.relname, b.relblocknumber
ORDER BY access_count DESC
LIMIT 10;
```
**Scenario:** A migration effort was initiated in between and spanning releases of the Postgres platform releases.  Despite new features and improvements being available in the latest release, the version identified at the outset of the migration was kept to complete the migration.  Subsequent additional effort, time, and expense were exerted to upgrade the Postgres database following the initial migration in order to achieve optimal performance and new capabilities.

**Recommended Solution:** Whenever possible, prioritize the adoption of the latest release version of Postgres when migrating.  The Postgres community dev teams work incredibly hard to squeeze every bit of performance and stability into each new release, and holding back potentially translates to leaving performance on the sidelines.  Additionally, take full advantage of new Azure features, including SSDv2 storage, the latest server family of infrastructure, and automated index tuning and autonomous server parameter tuning capabilities.

**Scenario:** Organizations migrating to Postgres for the first time may be unfamiliar with best practices and approaches when identifying slow-running queries, implementing new index-types appropriately, and operating within a database engine environment which does not require query hints.

**Recommended Solution:** Extensions are an integral part of what makes Postgres so powerful.  There are several extensions that can provide important features enabling you to ensure your database is operating at peak performance.  Some key extensions to consider include: 

 - **auto_explain:** automatically logs execution plans for queries which run beyond a set threshold.  Allows database administrators to diagnose performance issues and optimize query performance without manually running EXPLAIN on each query.

 - **pg_trgm:** provides functions and operators for determining similarity of text-based data by way of trigram matching.  This extension is useful for tasks involving text search, fuzzy matching, and similarity-based queries.  Combined with GIN or GIST indexes on text columns offers improved performance on LIKE queries and similarity searches.

 - **pg_cron:** allows for scheduling and management of periodic tasks directly within the database.  Integrates cron-like job scheduling into Postgres enabling the automation of routine maintenance tasks, data processing, and similar repetitive operations.  

> [!TIP]
> if your database operations involve a significant amount of repeated creation and deletion of database objects, older pg_catalog system table tuples will increase, leading to table “bloat”.  As pg_catalog is a system table involved in many database operations, unmitigated maintenance on this table can result in degraded performance across the database.  Ensuring that pg_catalog is adequately maintained and appropriately vacuumed can be ensured by configuring a pg_cron schedule.

 - **pg_hint_plan:** Postgres aims to provide consistent and reliable performance without the need for manual intervention, resulting in the intentional design decision to not include query hints.  For some scenarios where specific and precise control over query plan designs are needed, pg_hint_plan provides a way to influence the query planner’s decisions by using hints embedded into SQL comments.  These hints allow database administrators to guide the query planner to choose specific plans in order to optimize complex queries or address performance issues that the planner may not be able to handle on its own.

These examples are just scratching the surface of the incredibly vast set of extensions available to your Postgres database.  We encourage you to fully explore these extensions as an opportunity to supercharge your Postgres database and to consider the possibility of authoring your own extensions where you see the potential to expand Postgres beyond its current capabilities.  The powerfully flexible extension architecture ensures that Postgres will always be able to adapt and evolve with your platform requirements.

**Scenario:** In some instances, table partition strategies resulting in the creation of thousands of partitions can slow query performance when the query planner is unable to determine the partition key when parsing the query.  The resulting behavior of extended planning time causes query planning to take longer than the actual query execution.

**Recommended Solution:** Re-evaluate the need for excessive partitioning strategies.  The Postgres database engine may no longer require the same structuring of data and reducing the number of partitions may likely improve performance.  If the partitioning scheme is assessed to be required, consider restructuring your query into discrete operations to first identify and extract dynamic partition keys, and then use the partition keys in your operations.

**Scenario:** At times, external dependencies and environmental circumstances may require hybrid database scenarios where both Oracle and Azure Postgres databases need to coexist.  There may be occasions where phased migrations are necessary to access and query Oracle data directly from Azure Postgres without the overhead of importing data or modifying complex ETL processes.  In other instances, performing parallel data validation by comparing equivalent datasets in both Oracle and Azure Postgres environments simultaneously can help ensure data consistency and integrity during/after your migration.

**Recommended Solution:** PostgreSQL Foreign Data Wrapper (FDW) Extensions are a key Postgres feature allowing you to access and manipulate data stored in external systems as if that data was within Azure Postgres database natively.  FDWs enable Azure Postgres to function as a federated database, allowing integration with any number of external data sources, including Oracle databases.  FDWs create foreign table definitions within your Postgres database and these foreign tables act as a proxy for your defined external data source allowing users to query these foreign tables using regular SQL queries.  Internally, the Postgres engine uses the external FDW definition to communicate with and coordinate data on demand from the remote data source.

**oracle_fdw:** (Foreign Data Wrapper for Oracle) is a Postgres extension that allows you to access Oracle databases from within Azure Postgres.  When migrating from Oracle to Azure Postgres, oracle_fdw can play a crucial role by providing data access, data validation, incremental migration, and real-time data synchronization.  It is important to keep in mind the following key considerations when using FDWs:

 - Running queries through oracle_fdw will incur overhead in the form of network communications and authentication negotiation while the data is processed and fetched from the remote Oracle server
 - Some data types may need special handling or conversion to ensure data types are correctly mapped between systems.  

Effectively using oracle_fdw can potentially help in simplifying the database transition and ensuring data accessibility by enabling your applications and data to remain accessible throughout the overall migration process.