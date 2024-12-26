---
title: Server Parameters in Azure Database for MySQL - Flexible Server
description: This article provides guidelines for configuring server parameters in Azure Database for MySQL - Flexible Server.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---
# Server parameters in Azure Database for MySQL - Flexible Server

This article provides considerations and guidelines for configuring server parameters in Azure Database for MySQL - Flexible Server.

> [!NOTE]  
> This article contains references to the term *slave*, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## What are server parameters?

The MySQL engine provides many [server parameters](https://dev.mysql.com/doc/refman/5.7/en/server-option-variable-reference.html) (also called *variables*) that you can use to configure and tune engine behavior. Some parameters can be set dynamically during runtime. Others are static and require a server restart after you set them.

In Azure Database for MySQL - Flexible Server, you can change the value of various MySQL server parameters by using the [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md) and the [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-configure-server-parameters-cli.md) to match your workload's needs.

## Configurable server parameters

You can manage the configuration of an Azure Database for MySQL Flexible Server by using server parameters. The server parameters are configured with the default and recommended values when you create the server. The **Server parameters** pane in the Azure portal shows both the modifiable and nonmodifiable parameters. The nonmodifiable server parameters are unavailable.

The list of supported server parameters is constantly growing. You can use the Azure portal to periodically view the full list of server parameters and configure the values.

If you modify a static server parameter by using the portal, you need to restart the server for the changes to take effect. If you're using automation scripts (through tools like Azure Resource Manager templates, Terraform, or the Azure CLI), your script should have a provision to restart the service for the settings to take effect, even if you're changing the configuration as a part of the creation experience.

If you want to modify a nonmodifiable server parameter for your environment, [post an idea via community feedback](https://feedback.azure.com/d365community/forum/47b1e71d-ee24-ec11-b6e6-000d3a4f0da0), or vote if the feedback already exists (which can help us prioritize).

The following sections describe the limits of the commonly updated server parameters. The compute tier and the size (vCores) of the server determine the limits.

### lower_case_table_names

For MySQL version 5.7, the default value of `lower_case_table_names` is `1` in Azure Database for MySQL - Flexible Server. Although it's possible to change the supported value to `2`, reverting from `2` back to `1` isn't allowed. For assistance in changing the default value, [create a support ticket](https://azure.microsoft.com/support/create-ticket/).

For [MySQL version 8.0+](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html) you can configure `lower_case_table_names` only when you're initializing the server. [Learn more](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html). Changing the `lower_case_table_names` setting after the server is initialized is prohibited.

Supported values for MySQL version 8.0 are `1` and `2` in Azure Database for MySQL - Flexible Server. The default value is `1`. For assistance in changing the default value during server creation, [create a support ticket](https://azure.microsoft.com/support/create-ticket/).

### innodb_tmpdir

You use the [innodb_tmpdir](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_tmpdir) parameter in Azure Database for MySQL - Flexible Server to define the directory for temporary sort files created during online `ALTER TABLE` operations that rebuild.

The default value of `innodb_tmpdir` is `/mnt/temp`. This location corresponds to the [temporary storage (SSD)](./concepts-service-tiers-storage.md#service-tiers-size-and-server-types) and is available in gibibytes (GiB) with each server compute size. This location is ideal for operations that don't require a large amount of space.

If you need more space, you can set `innodb_tmpdir` to `/app/work/tmpdir`. This setting utilizes the available storage capacity on your Azure Database for MySQL Flexible Server. This setting can be useful for larger operations that require more temporary storage.

Keep in mind that using `/app/work/tmpdir` results in slower performance compared to the [default temporary storage (SSD)](./concepts-service-tiers-storage.md#service-tiers-size-and-server-types) `/mnt/temp` value. Make the choice based on the specific requirements of the operations.

The information provided for `innodb_tmpdir` is applicable to the parameters [innodb_temp_tablespaces_dir](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_temp_tablespaces_dir), [tmpdir](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_tmpdir), and [slave_load_tmpdir](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#sysvar_replica_load_tmpdir) where:

- The default value `/mnt/temp` is common.
- The alternative directory `/app/work/tmpdir` is available for configuring increased temporary storage, with a trade-off in performance based on specific operational requirements.

### log_bin_trust_function_creators

In Azure Database for MySQL - Flexible Server, binary logs are always enabled (that is, `log_bin` is set to `ON`). The [`log_bin_trust_function_creators`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_log_bin_trust_function_creators) parameter is set to `ON` by default in flexible servers.

The binary logging format is always `ROW`, and connections to the server always use row-based binary logging. With row-based binary logging, security issues don't exist and binary logging can't break, so you can safely allow `log_bin_trust_function_creators` to remain as `ON`.

If `log_bin_trust_function_creators` is set to `OFF` and you try to create triggers, you might get errors similar to: "You don't have the SUPER privilege, and binary logging is enabled (you might want to use the less safe `log_bin_trust_function_creators` variable)."

### innodb_buffer_pool_size

To learn about the `innodb_buffer_pool_size` parameter, review the [MySQL documentation](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_buffer_pool_size).

The [physical memory size](./concepts-service-tiers-storage.md#physical-memory-size-gb) in the following table represents the available random-access memory (RAM), in gigabytes (GB), on your Azure Database for MySQL Flexible Server.

| Pricing tier | vCores | Physical memory size (GB) | Default value (bytes) | Min value (bytes) | Max value (bytes) |
| --- | --- | --- | --- | --- | --- |
| Burstable (B1s) | 1 | 1 | 134217728 | 33554432 | 268435456 |
| Burstable (B1ms) | 1 | 2 | 536870912 | 134217728 | 1073741824 |
| Burstable (B2s) | 2 | 4 | 2147483648 | 134217728 | 2147483648 |
| Burstable (B2ms) | 2 | 8 | 4294967296 | 134217728 | 5368709120 |
| Burstable | 4 | 16 | 12884901888 | 134217728 | 12884901888 |
| Burstable | 8 | 32 | 25769803776 | 134217728 | 25769803776 |
| Burstable | 12 | 48 | 51539607552 | 134217728 | 51539607552 |
| Burstable | 16 | 64 | 2147483648 | 134217728 | 2147483648 |
| Burstable | 20 | 80 | 64424509440 | 134217728 | 64424509440 |
| General Purpose | 2 | 8 | 4294967296 | 134217728 | 5368709120 |
| General Purpose | 4 | 16 | 12884901888 | 134217728 | 12884901888 |
| General Purpose | 8 | 32 | 25769803776 | 134217728 | 25769803776 |
| General Purpose | 16 | 64 | 51539607552 | 134217728 | 51539607552 |
| General Purpose | 32 | 128 | 103079215104 | 134217728 | 103079215104 |
| General Purpose | 48 | 192 | 154618822656 | 134217728 | 154618822656 |
| General Purpose | 64 | 256 | 206158430208 | 134217728 | 206158430208 |
| Business Critical | 2 | 16 | 12884901888 | 134217728 | 12884901888 |
| Business Critical | 4 | 32 | 25769803776 | 134217728 | 25769803776 |
| Business Critical | 8 | 64 | 51539607552 | 134217728 | 51539607552 |
| Business Critical | 16 | 128 | 103079215104 | 134217728 | 103079215104 |
| Business Critical | 20 | 160 | 128849018880 | 134217728 | 128849018880 |
| Business Critical | 32 | 256 | 206158430208 | 134217728 | 206158430208 |
| Business Critical | 48 | 384 | 309237645312 | 134217728 | 309237645312 |
| Business Critical | 64 | 504 | 405874409472 | 134217728 | 405874409472 |

### innodb_file_per_table

MySQL stores the InnoDB table in different tablespaces based on the configuration that you provided during the table creation. The [system tablespace](https://dev.mysql.com/doc/refman/5.7/en/innodb-system-tablespace.html) is the storage area for the InnoDB data dictionary. A [file-per-table tablespace](https://dev.mysql.com/doc/refman/5.7/en/innodb-file-per-table-tablespaces.html) contains data and indexes for a single InnoDB table, and it's stored in the file system in its own data file. The [innodb_file_per_table](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_file_per_table) server parameter controls this behavior.

Setting `innodb_file_per_table` to `OFF` causes InnoDB to create tables in the system tablespace. Otherwise, InnoDB creates tables in file-per-table tablespaces.

Azure Database for MySQL - Flexible Server supports a maximum of 8 terabytes (TB) in a single data file. If your database size is larger than 8 TB, you should create the table in the `innodb_file_per_table` tablespace. If you have a single table size larger than 8 TB, you should use the partition table.

### innodb_log_file_size

The value of [innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size) is the size (in bytes) of each [log file](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_log_file) in a [log group](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_log_group). The combined size of log files [(innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size) * [innodb_log_files_in_group](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_files_in_group)) can't exceed a maximum value that is slightly less than 512 GB.

A bigger log file size is better for performance, but the drawback is that the recovery time after a crash is high. You need to balance recovery time for the rare event of a crash versus maximizing throughput during peak operations. A bigger log file size can also result in longer restart times.

You can configure `innodb_log_size` to 256 megabytes (MB), 512 MB, 1 GB, or 2 GB for Azure Database for MySQL - Flexible Server. The parameter is static and requires a restart.

> [!NOTE]  
> If you changed the `innodb_log_file_size` parameter from the default, check if the value of `show global status like 'innodb_buffer_pool_pages_dirty'` stays at `0` for 30 seconds to avoid restart delay.

### max_connections

The memory size of the server determines the value of `max_connections`. The [physical memory size](./concepts-service-tiers-storage.md#physical-memory-size-gb) in the following table represents the available RAM, in gigabytes, on your Azure Database for MySQL Flexible Server.

| Pricing tier | vCores | Physical memory size (GB) | Default value | Min value | Max value |
| --- | --- | --- | --- | --- | --- |
| Burstable (B1s) | 1 | 1 | 85 | 10 | 171 |
| Burstable (B1ms) | 1 | 2 | 171 | 10 | 341 |
| Burstable (B2s) | 2 | 4 | 341 | 10 | 683 |
| Burstable (B2ms) | 2 | 4 | 683 | 10 | 1365 |
| Burstable | 4 | 16 | 1365 | 10 | 2731 |
| Burstable | 8 | 32 | 2731 | 10 | 5461 |
| Burstable | 12 | 48 | 4097 | 10 | 8193 |
| Burstable | 16 | 64 | 5461 | 10 | 10923 |
| Burstable | 20 | 80 | 6827 | 10 | 13653 |
| General Purpose | 2 | 8 | 683 | 10 | 1365 |
| General Purpose | 4 | 16 | 1365 | 10 | 2731 |
| General Purpose | 8 | 32 | 2731 | 10 | 5461 |
| General Purpose | 16 | 64 | 5461 | 10 | 10923 |
| General Purpose | 32 | 128 | 10923 | 10 | 21845 |
| General Purpose | 48 | 192 | 16384 | 10 | 32768 |
| General Purpose | 64 | 256 | 21845 | 10 | 43691 |
| Business Critical | 2 | 16 | 1365 | 10 | 2731 |
| Business Critical | 4 | 32 | 2731 | 10 | 5461 |
| Business Critical | 8 | 64 | 5461 | 10 | 10923 |
| Business Critical | 16 | 128 | 10923 | 10 | 21845 |
| Business Critical | 20 | 160 | 13653 | 10 | 27306 |
| Business Critical | 32 | 256 | 21845 | 10 | 43691 |
| Business Critical | 48 | 384 | 32768 | 10 | 65536 |
| Business Critical | 64 | 504 | 43008 | 10 | 86016 |

When connections exceed the limit, you might receive the following error: "ERROR 1040 (08004): Too many connections."

Creating new client connections to MySQL takes time. After you establish these connections, they occupy database resources, even when they're idle. Most applications request many short-lived connections, which compounds this situation. The result is fewer resources available for your actual workload, leading to decreased performance.

A connection pooler that decreases idle connections and reuses existing connections helps you avoid this problem. For the best experience, we recommend that you use a connection pooler like ProxySQL to efficiently manage connections. To learn about setting up ProxySQL, see [this blog post](https://techcommunity.microsoft.com/blog/adformysql/load-balance-read-replicas-using-proxysql-in-azure-database-for-mysql/880042).

> [!NOTE]  
> ProxySQL is an open-source community tool. Microsoft supports it on a best-effort basis. To get production support with authoritative guidance, contact [ProxySQL product support](https://proxysql.com/services/support/).

### innodb_strict_mode

If you receive an error similar to "Row size too large (> 8126)," you might want to turn off the `innodb_strict_mode` server parameter. This parameter can't be modified globally at the server level because if row data size is larger than 8K, the data is truncated without an error. This truncation can lead to potential data loss. We recommend modifying the schema to fit the page size limit.

You can set this parameter at the session level by using `init_connect`. For more information, see [Setting nonmodifiable server parameters](./how-to-configure-server-parameters-portal.md#setting-non-modifiable-server-parameters).

> [!NOTE]  
> If you have a read replica server, setting `innodb_strict_mode` to `OFF` at the session level on a source server will break the replication. We suggest keeping the parameter set to `ON` if you have read replicas.

### time_zone

Upon initial deployment, an Azure Database for MySQL - Flexible Server instance includes system tables for time zone information, but these tables aren't populated. You can populate the time zone tables by calling the `mysql.az_load_timezone` stored procedure from a tool like the MySQL command line or MySQL Workbench. You can also call the stored procedure and set the global or session-level time zones by using the [Azure portal](./how-to-configure-server-parameters-portal.md#working-with-the-time-zone-parameter) or the [Azure CLI](./how-to-configure-server-parameters-cli.md#working-with-the-time-zone-parameter).

### binlog_expire_logs_seconds

In Azure Database for MySQL - Flexible Server, the `binlog_expire_logs_seconds` parameter specifies the number of seconds that the service waits before deleting the binary log file.

The binary log contains events that describe database changes, such as table creation operations or changes to table data. The binary log also contains events for statements that potentially could have made changes. The binary log is used mainly for two purposes: replication and data recovery operations.

Usually, the binary logs are deleted as soon as the handle is free from the service, backup, or replica set. If there are multiple replicas, the binary logs wait for the slowest replica to read the changes before they're deleted.

If you want to persist binary logs for a longer duration, you can configure the `binlog_expire_logs_seconds` parameter. If `binlog_expire_logs_seconds` is set to the default value of `0`, a binary log is deleted as soon as the handle to it's freed. If the value of `binlog_expire_logs_seconds` is greater than `0`, the binary log is deleted after the configured number of seconds.

Azure Database for MySQL - Flexible Server handles managed features, like backup and read replica deletion of binary files, internally. When you replicate the data-out from Azure Database for MySQL - Flexible Server, this parameter needs to be set in the primary to avoid deletion of binary logs before the replica reads from the changes in the primary. If you set `binlog_expire_logs_seconds` to a higher value, the binary logs won't be deleted soon enough. That delay can lead to an increase in the storage billing.

### event_scheduler

In Azure Database for MySQL - Flexible Server, the `event_scheduler` server parameter manages creating, scheduling, and running events. That is, the parameter manages tasks that run according to a schedule by a special MySQL Event Scheduler thread. When the `event_scheduler` parameter is set to `ON`, the Event Scheduler thread is listed as a daemon process in the output of `SHOW PROCESSLIST`.

For MySQL version 5.7 servers, the server parameter `event_scheduler` is automatically turned 'OFF' when [backup](./concepts-backup-restore.md#backup-overview) is initiated and server parameter `event_scheduler` is turned back 'ON' after the backup completes successfully. In MySQL version 8.0 for Azure Database for MySQL - Flexible Server, the event_scheduler remains unaffected during [backups](./concepts-backup-restore.md#backup-overview). To ensure smoother operations, it's recommended to upgrade your MySQL 5.7 servers to version 8.0 using a [major version upgrade](how-to-upgrade.md).

You can create and schedule events by using the following SQL syntax:

```sql
CREATE EVENT <event name>
ON SCHEDULE EVERY _ MINUTE / HOUR / DAY
STARTS TIMESTAMP / CURRENT_TIMESTAMP
ENDS TIMESTAMP / CURRENT_TIMESTAMP + INTERVAL 1 MINUTE / HOUR / DAY
COMMENT '<comment>'
DO
<your statement>;
```

For more information about creating an event, see the following documentation about the Event Scheduler in the MySQL reference manual:

- [Using the Event Scheduler in MySQL 5.7](https://dev.mysql.com/doc/refman/5.7/en/event-scheduler.html)
- [Using the Event Scheduler in MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/event-scheduler.html)

<a id="configuring-the-event_scheduler-server-parameter"></a>

#### Configure the event_scheduler server parameter

The following scenario illustrates one way to use the `event_scheduler` parameter in Azure Database for MySQL - Flexible Server.

To demonstrate the scenario, consider the following example of a simple table:

```sql
mysql> describe tab1;
+-----------+-------------+------+-----+---------+----------------+
| Field | Type | Null | Key | Default | Extra |
| +-----------+-------------+------+-----+---------+----------------+ |
| id | int(11) | NO | PRI | NULL | auto_increment |
| CreatedAt | timestamp | YES | | NULL | |
| CreatedBy | varchar(16) | YES | | NULL | |
| +-----------+-------------+------+-----+---------+----------------+ |
| 3 rows in set (0.23 sec) |
| ``` |
| To configure the `event_scheduler` server parameter in Azure Database for MySQL - Flexible Server, perform the following steps: |

1. In the Azure portal, go to your Azure Database for MySQL - Flexible Server instance. Under **Settings**, select **Server parameters**.
1. On the **Server parameters** pane, search for `event_scheduler`. In the **VALUE** dropdown list, select **ON**, and then select **Save**.

    > [!NOTE]
    > Deployment of the dynamic configuration change to the server parameter doesn't require a restart.

1. To create an event, connect to the Azure Database for MySQL - Flexible Server instance and run the following SQL command:
    ```sql

    CREATE EVENT test_event_01
    ON SCHEDULE EVERY 1 MINUTE
    STARTS CURRENT_TIMESTAMP
    ENDS CURRENT_TIMESTAMP + INTERVAL 1 HOUR
    COMMENT 'Inserting record into the table tab1 with current timestamp'
    DO
    INSERT INTO tab1(id,createdAt,createdBy)
    VALUES('',NOW(),CURRENT_USER());

    ```
1. To view the Event Scheduler details, run the following SQL statement:
    ```sql

    SHOW EVENTS;

    ```
    The following output appears:
    ```sql

    mysql> show events;
    +-----+---------------+-------------+-----------+-----------+------------+----------------+----------------+---------------------+---------------------+---------+------------+----------------------+----------------------+--------------------+
    | Db | Name | Definer | Time zone | Type | Execute at | Interval value | Interval field | Starts | Ends | Status | Originator | character_set_client | collation_connection | Database Collation |
    | +-----+---------------+-------------+-----------+-----------+------------+----------------+----------------+---------------------+---------------------+---------+------------+----------------------+----------------------+--------------------+ |
    | db1 | test_event_01 | azureuser@% | SYSTEM | RECURRING | NULL | 1 | MINUTE | 2023-04-05 14:47:04 | 2023-04-05 15:47:04 | ENABLED | 3221153808 | latin1 | latin1_swedish_ci | latin1_swedish_ci |
    | +-----+---------------+-------------+-----------+-----------+------------+----------------+----------------+---------------------+---------------------+---------+------------+----------------------+----------------------+--------------------+ |
    | 1 row in set (0.23 sec) |
    | ``` |

1. After a few minutes, query the rows from the table to begin viewing the rows inserted every minute according to the `event_scheduler` parameter that you configured:

    ```azurecli
    mysql> select * from tab1;
    +----+---------------------+-------------+
    | id | CreatedAt | CreatedBy |
    | +----+---------------------+-------------+ |
    | 1 | 2023-04-05 14:47:04 | azureuser@% |
    | 2 | 2023-04-05 14:48:04 | azureuser@% |
    | 3 | 2023-04-05 14:49:04 | azureuser@% |
    | 4 | 2023-04-05 14:50:04 | azureuser@% |
    | +----+---------------------+-------------+ |
    | 4 rows in set (0.23 sec) |
    | ``` |
| 1. After an hour, run a `select` statement on the table to view the complete result of the values inserted into table every minute for an hour (as `event_scheduler` is configured in this case): |
    ```azurecli

    mysql> select * from tab1;
    +----+---------------------+-------------+
    | id | CreatedAt | CreatedBy |
    | +----+---------------------+-------------+ |
    | 1 | 2023-04-05 14:47:04 | azureuser@% |
    | 2 | 2023-04-05 14:48:04 | azureuser@% |
    | 3 | 2023-04-05 14:49:04 | azureuser@% |
    | 4 | 2023-04-05 14:50:04 | azureuser@% |
    | 5 | 2023-04-05 14:51:04 | azureuser@% |
    | 6 | 2023-04-05 14:52:04 | azureuser@% |
    | ..< 50 lines trimmed to compact output >.. |
    | 56 | 2023-04-05 15:42:04 | azureuser@% |
    | 57 | 2023-04-05 15:43:04 | azureuser@% |
    | 58 | 2023-04-05 15:44:04 | azureuser@% |
    | 59 | 2023-04-05 15:45:04 | azureuser@% |
    | 60 | 2023-04-05 15:46:04 | azureuser@% |
    | 61 | 2023-04-05 15:47:04 | azureuser@% |
    | +----+---------------------+-------------+ |
    | 61 rows in set (0.23 sec) |
    | ``` |

#### Other scenarios

You can set up an event based on the requirements of your specific scenario. A few examples of scheduling SQL statements to run at various time intervals follow.

To run a SQL statement now and repeat one time per day with no end:

```sql
CREATE EVENT <event name>
ON SCHEDULE
EVERY 1 DAY
STARTS (TIMESTAMP(CURRENT_DATE) + INTERVAL 1 DAY + INTERVAL 1 HOUR)
COMMENT 'Comment'
DO
<your statement>;
```

To run a SQL statement every hour with no end:

```sql
CREATE EVENT <event name>
ON SCHEDULE
EVERY 1 HOUR
COMMENT 'Comment'
DO
<your statement>;
```

To run a SQL statement every day with no end:

```sql
CREATE EVENT <event name>
ON SCHEDULE
EVERY 1 DAY
STARTS str_to_date( date_format(now(), '%Y%m%d 0200'), '%Y%m%d %H%i' ) + INTERVAL 1 DAY
COMMENT 'Comment'
DO
<your statement>;
```

#### Limitations

For servers with high availability configured, when failover occurs, it's possible that the `event_scheduler` server parameter is set to `OFF`. If this occurs, when the failover is complete, configure the parameter to set the value to `ON`.

## Nonmodifiable server parameters

The **Server parameters** pane in the Azure portal shows both the modifiable and nonmodifiable server parameters. The nonmodifiable server parameters are unavailable. You can configure a nonmodifiable server parameter at the session level by using `init_connect` in the [Azure portal](./how-to-configure-server-parameters-portal.md#setting-non-modifiable-server-parameters) or the [Azure CLI](./how-to-configure-server-parameters-cli.md#setting-non-modifiable-server-parameters).

## Related content

- [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md)
- [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-configure-server-parameters-cli.md)
