---
title: Server Parameters in Azure Database for MySQL - Flexible Server
description: This article provides guidelines for configuring server parameters in Azure Database for MySQL - Flexible Server.
author: VandhanaMehta  
ms.author: vamehta  
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
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

For [MySQL version 8.0+](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html) you can configure `lower_case_table_names` only when you're initializing the server. [Learn more](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html). Changing the `lower_case_table_names` setting after the server is initialized is prohibited. Supported values for MySQL version 8.0 are `1` and `2` in Azure Database for MySQL - Flexible Server. The default value is `1`.

You can configure these settings in the portal during server creation by specifying the desired value under Server Parameters on the Additional Configuration page. For restore operations or replica server creation, the parameter will automatically be copied from the source server and cannot be changed. 

:::image type="content" source="media/concepts-server-parameters\flexible-server-lower-case-configure.png" alt-text="Screenshot that shows how to configure lower case table name server parameter at the time of creation." lightbox="media/concepts-server-parameters\flexible-server-lower-case-configure.png":::

For MySQL version 5.7, the default value of `lower_case_table_names` is `1` in Azure Database for MySQL - Flexible Server. Although it's possible to change the supported value to `2`, reverting from `2` back to `1` isn't allowed. For assistance in changing the default value, [create a support ticket](https://azure.microsoft.com/support/create-ticket/).

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

| Compute size | vCores | Physical memory size (GB) | Default value (bytes) | Min value (bytes) | Max value (bytes) |
| --- | --- | --- | --- | --- | --- |  
|**Burstable**    |  |  |  |  |  |                           
| Standard_B1s | 1 | 1 | 134217728 | 33554432 | 268435456 |
| Standard_B1ms | 1 | 2 | 536870912 | 134217728 | 1073741824 |
| Standard_B2s | 2 | 4 | 2147483648 | 134217728 | 2147483648 |
| Standard_B2ms | 2 | 8 | 4294967296 | 134217728 | 5368709120 |
| Standard_B4ms | 4 | 16 | 12884901888 | 134217728 | 12884901888 |
| Standard_B8ms | 8 | 32 | 25769803776 | 134217728 | 25769803776 |
| Standard_B12ms | 12 | 48 | 51539607552 | 134217728 | 32212254720 |
| Standard_B16ms | 16 | 64 | 2147483648 | 134217728 | 51539607552 |
| Standard_B20ms | 20 | 80 | 64424509440 | 134217728 | 64424509440 |
|**General Purpose**    |  |  |  |  |  |  
| Standard_D2ads_v5 | 2 | 8 | 4294967296 | 134217728 | 5368709120 |
| Standard_D2ds_v4 | 2 | 8 | 4294967296 | 134217728 | 5368709120 |
| Standard_D4ads_v5 | 4 | 16 | 12884901888 | 134217728 | 12884901888 |
| Standard_D4ds_v4 | 4 | 16 | 12884901888 | 134217728 | 12884901888 |
| Standard_D8ads_v5 | 8 | 32 | 25769803776 | 134217728 | 25769803776 |
| Standard_D8ds_v4 | 8 | 32 | 25769803776 | 134217728 | 25769803776 |
| Standard_D16ads_v5 | 16 | 64 | 51539607552 | 134217728 | 51539607552 |
| Standard_D16ds_v4 | 16 | 64 | 51539607552 | 134217728 | 51539607552 |
| Standard_D32ads_v5 | 32 | 128 | 103079215104 | 134217728 | 103079215104 |
| Standard_D32ds_v4 | 32 | 128 | 103079215104 | 134217728 | 103079215104 |
| Standard_D48ads_v5 | 48 | 192 | 154618822656 | 134217728 | 154618822656 |
| Standard_D48ds_v4 | 48 | 192 | 154618822656 | 134217728 | 154618822656 |
| Standard_D64ads_v5 | 64 | 256 | 206158430208 | 134217728 | 206158430208 |
| Standard_D64ds_v4| 64 | 256 | 206158430208 | 134217728 | 206158430208 |
|**Memory-Optimized**    |  |  |  |  |  |  
| Standard_E2ds_v4 | 2 | 16 | 12884901888 | 134217728 | 12884901888 |
| Standard_E2ads_v5, Standard_E2ds_v5| 2 | 16 | 12884901888 | 134217728 | 12884901888 |
| Standard_E4ds_v4 | 4 | 32 | 25769803776 | 134217728 | 25769803776 |
| Standard_E4ads_v5, Standard_E4ds_v5 | 4 | 32 | 25769803776 | 134217728 | 25769803776 |
| Standard_E8ds_v4 | 8 | 64 | 51539607552 | 134217728 | 51539607552 |
| Standard_E8ads_v5, Standard_E8ds_v5 | 8 | 64 | 51539607552 | 134217728 | 51539607552 |
| Standard_E16ds_v4  | 16 | 128 | 103079215104 | 134217728 | 103079215104 |
| Standard_E16ads_v5, Standard_E16ds_v5 | 16 | 128 | 103079215104 | 134217728 | 103079215104 |
| Standard_E20ds_v4  | 20 | 160 | 128849018880 | 134217728 | 128849018880 |
| Standard_E20ads_v5, Standard_E20ds_v5 | 20 | 160 | 128849018880 | 134217728 | 128849018880 |
| Standard_E32ds_v4  | 32 | 256 | 206158430208 | 134217728 | 206158430208 |
| Standard_E32ads_v5, Standard_E32ds_v5 | 32 | 256 | 206158430208 | 134217728 | 206158430208 |
| Standard_E48ds_v4  | 48 | 384 | 309237645312 | 134217728 | 309237645312 |
| Standard_E48ads_v5, Standard_E48ds_v5 | 48 | 384 | 309237645312 | 134217728 | 309237645312 |
| Standard_E64ds_v4  | 64 | 504 | 405874409472 | 134217728 | 405874409472 |
| Standard_E64ads_v5 , Standard_E64ds_v5 | 64 | 512 | 412316860416 | 134217728 | 412316860416 |
| Standard_E80ids_v4  | 80 | 504 | 405874409472 | 134217728 | 405874409472 |
| Standard_E96ds_v5 | 96 | 672 | 541165879296 | 134217728 | 541165879296 |

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

| Compute size | vCores | Physical memory size (GB) | Default value | Min value | Max value |
| --- | --- | --- | --- | --- | --- |
| **Burstable** | | | | | |
| Standard_B1s | 1 | 1 | 85 | 10 | 171 |
| Standard_B1ms | 1 | 2 | 171 | 10 | 341 |
| Standard_B2s | 2 | 4 | 341 | 10 | 683 |
| Standard_B2ms | 2 | 4 | 683 | 10 | 1365 |
| Standard_B4ms | 4 | 16 | 1365 | 10 | 2731 |
| Standard_B8ms | 8 | 32 | 2731 | 10 | 5461 |
| Standard_B12ms | 12 | 48 | 4097 | 10 | 8193 |
| Standard_B16ms | 16 | 64 | 5461 | 10 | 10923 |
| Standard_B20ms | 20 | 80 | 6827 | 10 | 13653 |
| **General Purpose** | | | | | |
| Standard_D2ads_v5 | 2 | 8 | 683 | 10 | 1365 |
| Standard_D2ds_v4 | 2 | 8 | 683 | 10 | 1365 |
| Standard_D4ads_v5 | 4 | 16 | 1365 | 10 | 2731 |
| Standard_D4ds_v4 | 4 | 16 | 1365 | 10 | 2731 |
| Standard_D8ads_v5 | 8 | 32 | 2731 | 10 | 5461 |
| Standard_D8ds_v4 | 8 | 32 | 2731 | 10 | 5461 |
| Standard_D16ads_v5 | 16 | 64 | 5461 | 10 | 10923 |
| Standard_D16ds_v4 | 16 | 64 | 5461 | 10 | 10923 |
| Standard_D32ads_v5 | 32 | 128 | 10923 | 10 | 21845 |
| Standard_D32ds_v4 | 32 | 128 | 10923 | 10 | 21845 |
| Standard_D48ads_v5 | 48 | 192 | 16384 | 10 | 32768 |
| Standard_D48ds_v4 | 48 | 192 | 16384 | 10 | 32768 |
| Standard_D64ads_v5 | 64 | 256 | 21845 | 10 | 43691 |
| Standard_D64ds_v4 | 64 | 256 | 21845 | 10 | 43691 |
| **Memory-Optimized** | | | | | |
| Standard_E2ds_v4 | 2 | 16 | 1365 | 10 | 2731 |
| Standard_E2ads_v5, Standard_E2ds_v5 | 2 | 16 | 1365 | 10 | 2731 |
| Standard_E4ds_v4 | 4 | 32 | 2731 | 10 | 5461 |
| Standard_E4ads_v5, Standard_E4ds_v5 | 4 | 32 | 2731 | 10 | 5461 |
| Standard_E8ds_v4 | 8 | 64 | 5461 | 10 | 10923 |
| Standard_E8ads_v5, Standard_E8ds_v5 | 8 | 64 | 5461 | 10 | 10923 |
| Standard_E16ds_v4 | 16 | 128 | 10923 | 10 | 21845 |
| Standard_E16ads_v5, Standard_E16ds_v5 | 16 | 128 | 10923 | 10 | 21845 |
| Standard_E20ds_v4 | 20 | 160 | 13653 | 10 | 27306 |
| Standard_E20ads_v5, Standard_E20ds_v5 | 20 | 160 | 13653 | 10 | 27306 |
| Standard_E32ds_v4 | 32 | 256 | 21845 | 10 | 43691 |
| Standard_E32ads_v5, Standard_E32ds_v5 | 32 | 256 | 21845 | 10 | 43691 |
| Standard_E48ds_v4 | 48 | 384 | 32768 | 10 | 65536 |
| Standard_E48ads_v5, Standard_E48ds_v5 | 48 | 384 | 32768 | 10 | 65536 |
| Standard_E64ds_v4 | 64 | 504 | 43008 | 10 | 86016 |
| Standard_E64ads_v5, Standard_E64ds_v5 | 64 | 512 | 43691 | 10 | 87383 |
| Standard_E80ids_v4 | 80 | 504 | 43008 | 10 | 86016 |
| Standard_E96ds_v5 | 96 | 672 | 50000 | 10 | 100000 |

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

You can populate the time zone tables with the latest time zone information by calling the `mysql.az_load_timezone` stored procedure from a tool like the MySQL command line or MySQL Workbench and then set the global time zones by using the [Azure portal](./how-to-configure-server-parameters-portal.md#working-with-the-time-zone-parameter) or the [Azure CLI](./how-to-configure-server-parameters-cli.md#working-with-the-time-zone-parameter). Time zones are automatically loaded during server creation, removing the need for customers to manually execute the `mysql.az_load_timezone` stored procedure afterwards to load the time zone.

### innodb_temp_data_file_size_max
For Azure Database for MySQL Flexible Server (version 5.7 only), innodb_temp_data_file_size_max parameter defines the maximum size of InnoDB temporary tablespace data files in MB. Setting the value to 0 means no limit, allowing growth up to the full storage size. Any non-zero value below 64 MB is rounded up to 64 MB, while values above 64 MB are applied as specified. This is a static variable and requires a server restart for changes to take effect.

> [!NOTE]  
> - Note: In MySQL 8.0 and above, the [global temporary tablespace](https://dev.mysql.com/doc/refman/8.0/en/innodb-temporary-tablespace.html) (ibtmp1) only stores rollback segments for changes made to user-created temporary tables. Therefore, this parameter is no longer relevant.

### binlog_expire_logs_seconds

In Azure Database for MySQL - Flexible Server, the `binlog_expire_logs_seconds` parameter specifies the number of seconds that the service waits before deleting the binary log file.

The binary log contains events that describe database changes, such as table creation operations or changes to table data. The binary log also contains events for statements that potentially could have made changes. The binary log is used mainly for two purposes: replication and data recovery operations.

Usually, the binary logs are deleted as soon as the handle is free from the service, backup, or replica set. If there are multiple replicas, the binary logs wait for the slowest replica to read the changes before they're deleted.

If you want to persist binary logs for a longer duration, you can configure the `binlog_expire_logs_seconds` parameter. If `binlog_expire_logs_seconds` is set to the default value of `0`, a binary log is deleted as soon as the handle to it's freed. If the value of `binlog_expire_logs_seconds` is greater than `0`, the binary log is deleted after the configured number of seconds.

Azure Database for MySQL - Flexible Server handles managed features, like backup and read replica deletion of binary files, internally. When you replicate the data-out from Azure Database for MySQL - Flexible Server, this parameter needs to be set in the primary to avoid deletion of binary logs before the replica reads from the changes in the primary. If you set `binlog_expire_logs_seconds` to a higher value, the binary logs won't be deleted soon enough. That delay can lead to an increase in the storage billing.

#### Limitations
Once the accelerated logs feature is enabled, the binlog_expire_logs_seconds server parameter is disregarded entirely, and any configured value will no longer have any effect. However, if the accelerated logs feature is disabled, the server will once again adhere to the configured value of binlog_expire_logs_seconds for binary log retention. This applies to replica servers as well. 

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

### innodb_ft_user_stopword_table
`innodb_ft_user_stopword_table` is a server parameter in MySQL that specifies the name of the table containing custom stopwords for InnoDB Full-Text Search. The table must be in the same database as the full-text indexed table, and its first column must be of type `VARCHAR`. In Azure Database for MySQL - Flexible Server, the default setting of `sql_generate_invisible_primary_key=ON` causes all tables without an explicit primary key to automatically include an invisible primary key. This behavior conflicts with the requirements for `innodb_ft_user_stopword_table`, as the invisible primary key becomes the first column of the table, preventing it from functioning as intended during Full-Text Search. To resolve this issue, you must set `sql_generate_invisible_primary_key=OFF` in the same session before creating the custom stopword table. For example:  

```sql
SET sql_generate_invisible_primary_key = OFF;
CREATE TABLE my_stopword_table (
    stopword VARCHAR(50) NOT NULL
);
INSERT INTO my_stopword_table (stopword) VALUES ('and'), ('or'), ('the');
```  

This ensures the stopword table meets MySQL’s requirements and allows custom stopwords to work properly.

## Nonmodifiable server parameters

The **Server parameters** pane in the Azure portal shows both the modifiable and nonmodifiable server parameters. The nonmodifiable server parameters are unavailable. You can configure a nonmodifiable server parameter at the session level by using `init_connect` in the [Azure portal](./how-to-configure-server-parameters-portal.md#setting-non-modifiable-server-parameters) or the [Azure CLI](./how-to-configure-server-parameters-cli.md#setting-non-modifiable-server-parameters).


## Azure mysql system variables


### azure_server_name

The `azure_server_name` variable provides the exact server name of the Azure Database for MySQL - Flexible Server instance. This variable is useful when applications or scripts need to programmatically retrieve the server’s hostname they are connected to, without relying on external configurations and can be retrieved by running following command inside MySQL.

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'azure_server_name';
+-------------------+---------+
| Variable_name     | Value   |
+-------------------+---------+
| azure_server_name | myflex  |
+-------------------+---------+
```  
Note : The `azure_server_name` consistently returns the original server name you use to connect to the service (e.g., myflex) for both HA-enabled and HA-disabled server


### logical_server_name

The `logical_server_name` variable represents the hostname of the instance where Azure Database for MySQL - Flexible Server is running. This variable is useful for identifying the host where the service is currently running, aiding in troubleshooting and failover monitoring. You can retrieve this variable by executing the following command within MySQL.

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'logical_server_name';
+---------------------+--------------+
| Variable_name       | Value        |
+---------------------+--------------+
| logical_server_name | myflex	     |
+---------------------+--------------+
```  
Note: For an HA-enabled server, the `logical_server_name` variable reflects the hostname of the instance acting as the primary server. For a server where HA is disabled, the value of `logical_server_name` is the same as the `azure_server_name` variable since there is only a single instance.


## Related content

- [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md)
- [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-configure-server-parameters-cli.md)
