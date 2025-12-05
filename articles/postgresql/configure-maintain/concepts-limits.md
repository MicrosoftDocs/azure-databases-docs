---
title: Limits in Flexible Server
description: This article describes limits in Azure Database for PostgreSQL, such as the number of connections and storage engine options.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 11/13/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
ms.custom:
  - ai-assistant-test
---

# Limits in Azure Database for PostgreSQL 

The following sections describe capacity and functional limits for Azure Database for PostgreSQL flexible server instances. If you'd like to learn about resource (compute, memory, storage) tiers, see the [compute ](concepts-compute.md) and [storage ](../extensions/concepts-storage.md)  articles.

## Maximum connections

The following table shows the *default* maximum number of connections for each pricing tier and vCore configuration. An Azure Database for PostgreSQL flexible server instance reserves 15 connections for physical replication and monitoring of the Azure Database for PostgreSQL flexible server instance. Consequently, the table reduces the value for maximum user connections by 15 from the total maximum connections.

|Product name                                 |vCores|Memory size|Maximum connections|Maximum user connections|
|-----------------------------------------|------|-----------|---------------|--------------------|
|**Burstable**                            |      |           |               |                    |
|B1ms                                     |1     |2 GiB      |50             |35                  |
|B2s                                      |2     |4 GiB      |429            |414                 |
|B2ms                                     |2     |8 GiB      |859            |844                 |
|B4ms                                     |4     |16 GiB     |1,718           |1,703                |
|B8ms                                     |8     |32 GiB     |3,437           |3,422                |
|B12ms                                    |12    |48 GiB     |5,000           |4,985                |
|B16ms                                    |16    |64 GiB     |5,000           |4,985                |
|B20ms                                    |20    |80 GiB     |5,000           |4,985                |
|**General Purpose**                      |      |           |               |                    |
|D2s_v3 / D2ds_v4 / D2ds_v5 / D2ads_v5    |2     |8 GiB      |859            |844                 |
|D4s_v3 / D4ds_v4 / D4ds_v5 / D4ads_v5    |4     |16 GiB     |1,718           |1,703                |
|D8s_v3 / D8ds_V4 / D8ds_v5 / D8ads_v5    |8     |32 GiB     |3,437           |3,422                |
|D16s_v3 / D16ds_v4 / D16ds_v5 / D16ads_v5|16    |64 GiB     |5,000           |4,985                |
|D32s_v3 / D32ds_v4 / D32ds_v5 / D32ads_v5|32    |128 GiB    |5,000           |4,985                |
|D48s_v3 / D48ds_v4 / D48ds_v5 / D48ads_v5|48    |192 GiB    |5,000           |4,985                |
|D64s_v3 / D64ds_v4 / D64ds_v5 / D64ads_v5|64    |256 GiB    |5,000           |4,985                |
|D96ds_v5 / D96ads_v5                     |96    |384 GiB    |5,000           |4,985                |
|**Memory Optimized**                     |      |           |               |                    |
|E2s_v3 / E2ds_v4 / E2ds_v5 / E2ads_v5    |2     |16 GiB     |1,718           |1,703                |
|E4s_v3 / E4ds_v4 / E4ds_v5 / E4ads_v5    |4     |32 GiB     |3,437           |3,422                |
|E8s_v3 / E8ds_v4 / E8ds_v5 / E8ads_v5    |8     |64 GiB     |5,000           |4,985                |
|E16s_v3 / E16ds_v4 / E16ds_v5 / E16ads_v5|16    |128 GiB    |5,000           |4,985                |
|E20ds_v4 / E20ds_v5 / E20ads_v5          |20    |160 GiB    |5,000           |4,985                |
|E32s_v3 / E32ds_v4 / E32ds_v5 / E32ads_v5|32    |256 GiB    |5,000           |4,985                |
|E48s_v3 / E48ds_v4 / E48ds_v5 / E48ads_v5|48    |384 GiB    |5,000           |4,985                |
|E64s_v3 / E64ds_v4 / E64ds_v5 / E64ads_v5|64    |432 GiB    |5,000           |4,985                |
|E96ds_v5 / E96ads_v5                     |96    |672 GiB    |5,000           |4,985                |

The reserved connection slots, presently at 15, can change. We advise regularly verifying the total reserved connections on the server. You calculate this number by summing the values of the `reserved_connections` and `superuser_reserved_connections` server parameters. The maximum number of available user connections is `max_connections` - (`reserved_connections` + `superuser_reserved_connections`).

The system calculates the default value for the `max_connections` server parameter when you provision the instance of Azure Database for PostgreSQL flexible server, based on the product name that you select for its compute. Any subsequent changes of product selection to the compute that supports the instance won't have any effect on the default value for the `max_connections` server parameter of that instance. We recommend that whenever you change the product assigned to an instance, you also adjust the value for the `max_connections` parameter according to the values in the preceding table.

### Changing the max_connections value

When you first set up your Azure Database for Postgres flexible server instance, it automatically decides the highest number of connections that it can handle concurrently. Your server's configuration determines this number and you can't change it.

However, you can use the `max_connections` setting to adjust how many connections are allowed at a particular time. After you change this setting, you need to restart your server for the new limit to start working.

> [!CAUTION]
> Although it's possible to increase the value of `max_connections` beyond the default setting, we advise against it.
>
> Instances might encounter difficulties when the workload expands and demands more memory. As the number of connections increases, memory usage also rises. Instances with limited memory might face issues such as crashes or high latency. Although a higher value for `max_connections` might be acceptable when most connections are idle, it can lead to significant performance problems after they become active.
>
> If you need more connections, we suggest that you instead use PgBouncer, the built-in Azure solution for connection pool management. Use it in transaction mode. To start, we recommend that you use conservative values by multiplying the vCores within the range of 2 to 5. Afterward, carefully monitor resource utilization and application performance to ensure smooth operation. For detailed information on PgBouncer, see [PgBouncer in Azure Database for PostgreSQL](../connectivity/../connectivity/concepts-pgbouncer.md).

When connections exceed the limit, you might receive the following error:

`FATAL:  sorry, too many clients already.`

When you're using an Azure Database for PostgreSQL flexible server instance for a busy database with a large number of concurrent connections, there might be a significant strain on resources. This strain can result in high CPU utilization, especially when many connections are established simultaneously and when connections have short durations (less than 60 seconds). These factors can negatively affect overall database performance by increasing the time spent on processing connections and disconnections.

Each connection in an Azure Database for PostgreSQL flexible server instance, regardless of whether it's idle or active, consumes a significant amount of resources from your database. This consumption can lead to performance issues beyond high CPU utilization, such as disk and lock contention. The [Number of Database Connections](https://wiki.postgresql.org/wiki/Number_Of_Database_Connections) article on the PostgreSQL Wiki discusses this article in more detail. To learn more, see [Identify and solve connection performance in Azure Postgres](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/identify-and-solve-connection-performance-in-azure-postgres/ba-p/3698375).

## Functional limitations

The following sections list considerations for what is and isn't supported for your Azure Database for PostgreSQL flexible server instances.

### Scale operations

- At this time, scaling up the server storage requires a server restart.
- Server storage can only be scaled in 2x increments. See [Storage](../extensions/concepts-storage.md) for details.
- We currently don't support decreasing server storage size. The only way to do this operation is to [dump and restore](../howto-migrate-using-dump-and-restore.md) it to a new Azure Database for PostgreSQL flexible server instance.
   
### Storage

- After you configure the storage size, you can't reduce it. You have to create a new server with the desired storage size, perform a  manual [dump and restore](../howto-migrate-using-dump-and-restore.md) operation, and migrate your databases to the new server.
- When the storage usage reaches 95% or if the available capacity is less than 5 GiB (whichever is more), the system automatically switches the server to *read-only mode* to avoid errors associated with disk-full situations. In rare cases, if the rate of data growth outpaces the time it takes to switch to read-only mode, your server might still run out of storage. You can enable storage autogrow to avoid these issues and automatically scale your storage based on your workload demands.
- We recommend setting alert rules for `storage used` or `storage percent` when they exceed certain thresholds so that you can proactively take action such as increasing the storage size. For example, you can set an alert if the storage percentage exceeds 80% usage.
- If you're using logical replication, you must drop the logical replication slot in the primary server if the corresponding subscriber no longer exists. Otherwise, the write-ahead logging (WAL) files accumulate in the primary and fill up the storage. If the storage exceeds a certain threshold and if the logical replication slot isn't in use (because of an unavailable subscriber), an Azure Database for PostgreSQL flexible server instance automatically drops that unused logical replication slot. This action releases accumulated WAL files and prevents your server from becoming unavailable because the storage is filled.
- We don't support the creation of tablespaces. If you're creating a database, don't provide a tablespace name. An Azure Database for PostgreSQL flexible server instance uses the default tablespace that the template database inherits. It's unsafe to provide a tablespace like the temporary one, because we can't ensure that such objects will remain persistent after events like server restarts and high-availability (HA) failovers.
- Orphaned Data Files and Disk Usage Discrepancies: In rare cases, PostgreSQL may leave behind orphaned data files on disk—files that no longer have corresponding entries in the database's system catalog (which tracks all tables and data). This can happen if a table is created and populated within a transaction that fails to complete successfully (e.g., due to a server crash or interruption), resulting in a mismatch between the database-reported size and actual disk usage. This behavior is from the PostgreSQL community codebase and is not specific to Azure. The PostgreSQL community is aware of the issue and is exploring enhancements for automatic cleanup in future releases. For more details, see: [PostgreSQL: Orphaned Files in PostgreSQL](https://www.postgresql.org/message-id/CAE9k0Pno%3DMns7J5HA4%2BbbXzb%3DyCZnCtSF_wf1ZipCQxardKDjA%40mail.gmail.com). This may lead to unexpectedly high disk or storage consumption.
  - **How to Detect**: Compare the database-reported size (using queries like `SELECT pg_database_size('your_database')`) with [Azure portal metrics](/azure/postgresql/flexible-server/concepts-monitoring) for actual disk usage. If there's a significant discrepancy, orphaned files might be the cause. If so:
    - Run [VACUUM FULL](https://www.postgresql.org/docs/current/routine-vacuuming.html) on affected tables to reclaim space (note: this is resource-intensive, requires a table lock, and may require downtime).
    - Alternatively, use tools like [pg_repack](/azure/postgresql/flexible-server/how-to-perform-fullvacuum-pg-repack) or [pg_squeeze](https://github.com/cybertec-postgresql/pg_squeeze) extensions for reorganization with no downtime, but test in a non-production environment first.
    - Monitor via [Azure portal metrics](/azure/postgresql/flexible-server/concepts-monitoring) for disk usage thresholds. If the issue persists or you're unsure, contact Azure Support for assistance.
  - **How to Prevent**: Ensure transactions are properly managed in your applications to minimize incomplete operations. Regularly monitor disk usage through the [Azure portal metrics](/azure/postgresql/flexible-server/concepts-monitoring). Upgrading to the latest supported PostgreSQL version may include community fixes for related issues.



### Networking

- We currently don't support moving in and out of a virtual network.
- We currently don't support combining public access with deployment in a virtual network.
- Virtual networks don't support firewall rules. You can use network security groups instead.
- Public access database servers can connect to the public internet; for example, through `postgres_fdw`. You can't restrict this access. Servers in virtual networks can have restricted outbound access through network security groups.

### High availability

- See [High availability limitations](/azure/reliability/reliability-postgresql-flexible-server#high-availability-limitations).

### Availability zones

- We currently don't support manually moving servers to a different availability zone. However, by using the preferred availability zone as the standby zone, you can turn on HA. After you establish the standby zone, you can fail over to it and then turn off HA.

### Postgres engine, extensions, and PgBouncer

- An Azure Database for PostgreSQL flexible server instance supports all the features of the PostgreSQL engine, including partitioning, logical replication, and foreign data wrappers.
- An Azure Database for PostgreSQL flexible server instance supports all `contrib` extensions and more. For more information, see [PostgreSQL extensions](/azure/postgresql/flexible-server/concepts-extensions).
- Burstable servers currently don't have access to the built-in PgBouncer connection pooler.

### Stop/start operations

- After you stop the Azure Database for PostgreSQL flexible server instance, it automatically starts after seven days.

### Scheduled maintenance

- You can change the custom maintenance window to any day/time of the week. However, any changes that you make after receiving the maintenance notification will have no impact on the next maintenance. Changes take effect only with the following monthly scheduled maintenance.

### Server backups

- The system manages backups. You currently can't run backups manually. We recommend using `pg_dump` instead.
- The first snapshot is a full backup, and consecutive snapshots are differential backups. The differential backups back up only the changed data since the last snapshot backup.

  For example, if the size of your database is 40 GB and your provisioned storage is 64 GB, the first snapshot backup is 40 GB. Now, if you change 4 GB of data, the next differential snapshot backup size will be only 4 GB. The transaction logs (write-ahead logs) are separate from the full and differential backups, and they're archived continuously.

### Server restoration

- When you're using the point-in-time restore (PITR) feature, the system creates the new server with the same compute and storage configurations as the server that it's based on.
- The system restores database servers in virtual networks into the same virtual networks when you restore from a backup.
- The new server created during a restore doesn't have the firewall rules that existed on the original server. You need to create firewall rules separately for the new server.
- We don't support restore to a different subscription. As a workaround, you can restore the server within the same subscription and then migrate the restored server to a different subscription.

### Security

- Postgres 14 and later versions disable MD5 hashing and the system hashes native Postgres passwords using SCRAM-SHA-256 method only.

## Related content

- [Compute options in Azure Database for PostgreSQL](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL](../extensions/concepts-storage.md).
- [Supported versions of PostgreSQL in Azure Database for PostgreSQL](concepts-supported-versions.md).
