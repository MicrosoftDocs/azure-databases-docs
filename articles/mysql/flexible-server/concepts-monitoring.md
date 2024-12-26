---
title: Monitoring
description: This article describes the metrics for monitoring and alerting for Azure Database for MySQL - Flexible Server, including CPU, storage, and connection statistics.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Monitor Azure Database for MySQL - Flexible Server

> [!NOTE]  
> This article contains references to the term *slave*, a term that Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

Azure Database for MySQL Flexible Server provides monitoring of servers through Azure Monitor. Monitoring data about your servers helps you troubleshoot and optimize for your workload.

In this article, you learn about the various metrics available and Server logs for your flexible server, which give insight into its behavior.

## Metrics

Metrics are numerical values that describe some aspect of your server's resources at a particular time. Monitoring your server's resources helps you troubleshoot and optimize your workload by allowing you to monitor what matters most to you. Monitoring the right metrics helps you maintain the performance, reliability, and availability of your server and applications.

Azure Database for MySQL Flexible Server provides various metrics to help you understand how your workload is performing. Based on this data, you can understand the impact on your server and application.

All Azure metrics have a one-minute frequency, each providing 30 days of history. You can configure alerts on the metrics. See [Set up alerts on metrics for Azure Database for MySQL - Flexible Server](how-to-alert-on-metric.md). Other tasks include setting up automated actions, performing advanced analytics, and archiving history. For more information, see the [Azure Metrics Overview](/azure/azure-monitor/data-platform).

### Troubleshoot metrics

Sometimes, you might encounter issues with creating, customizing, or interpreting charts in Azure Metrics Explorer.  
A *Chart showing no data* could arise due to various factors. These might include the Microsoft Insights resource provider not being registered for your subscription or you lacking adequate access rights to your Azure Database for MySQL - Flexible Server. Other possibilities could be that your resource didn't generate metrics within the chosen time frame or the selected time range exceeds 30 days.

Several reasons that follow can cause this behavior:

- *Microsoft.Insights resource provider isn't registered*: Exploring metrics requires Microsoft.Insights resource provider registered in your subscription. Register your server manually by following the steps described in [Azure resource providers and types](/azure/azure-resource-manager/management/resource-providers-and-types).
- *Insufficient access rights to your resource*: Ensure you have sufficient permissions for your Azure Database for MySQL - Flexible Server from which you're exploring metrics. Your resource didn't emit metrics during the selected time range. Change the time of the chart to a wider range. In Azure, [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) controls access to metrics. You must be a member of [monitoring reader](/azure/role-based-access-control/built-in-roles#monitoring-reader), [monitoring contributor](/azure/role-based-access-control/built-in-roles#monitoring-contributor), or [contributor](/azure/role-based-access-control/built-in-roles#contributor) to explore metrics for any resource.
- *Your resource didn't emit metrics during the selected time range*: This could be due to several reasons. One possibility is that your resource didn't generate metrics within the chosen time frame. Change the time of the chart to a broader range to see if this resolves the issue. For more detailed information on troubleshooting this issue, refer to the [Azure Monitor metrics troubleshooting guide](/azure/azure-monitor/essentials/metrics-troubleshoot#your-resource-didnt-emit-metrics-during-the-selected-time-range).
- *Time range greater than 30 days*: Verify that the difference between the start and end dates in the time picker doesn't exceed the 30-day interval. For more detailed information on troubleshooting metrics, refer to the [Azure Monitor metrics troubleshooting guide](/azure/azure-monitor/essentials/metrics-troubleshoot).
- *Dashed Line Indication*: In Azure Monitor, a dashed line signifies a gap in data, or a "null value", between two points of known time grain data. This is a deliberate design that helps detect missing data points. If your chart displays dashed lines, it indicates missing data. You can refer to the [documentation for further information.](/azure/azure-monitor/essentials/metrics-troubleshoot#chart-shows-dashed-line)

For more detailed information on troubleshooting metrics, refer to the [Azure Monitor metrics troubleshooting guide.](/azure/azure-monitor/essentials/metrics-troubleshoot)

> [!NOTE]  
> Metrics marked as deprecated are scheduled to be removed from the Azure portal. You should ignore these metrics when monitoring your Azure Database for MySQL Flexible Server.

## List of metrics

These metrics are available for Azure Database for MySQL Flexible Server:

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| MySQL Uptime | uptime | Seconds | This metric indicates the length of time that the MySQL server has been running. |
| Host CPU percent | cpu_percent | Percent | Host CPU percent is the total utilization of the CPU to process all the tasks on your server over a selected period. This metric includes the workload of your Azure Database for MySQL Flexible Server instance and Azure MySQL process. High CPU percent can help you find if your database server has more workload than it can handle. This metric is equivalent to total CPU utilization and is similar to CPU utilization on any virtual machine. |
| CPU Credit Consumed | cpu_credits_consumed | Count | **This is for Burstable Tier Only** CPU credit is calculated based on workload. See [B-series burstable virtual machine sizes](/azure/virtual-machines/sizes-b-series-burstable) for more information. |
| CPU Credit Remaining | cpu_credits_remaining | Count | **This is for Burstable Tier Only** CPU remaining is calculated based on workload. See [B-series burstable virtual machine sizes](/azure/virtual-machines/sizes-b-series-burstable) for more information. |
| Host Network In | network_bytes_ingress | Bytes | Total sum of incoming network traffic on the server for a selected period. This metric includes traffic to your database and Azure Database for MySQL Flexible Server features like monitoring, logs, etc. |
| Host Network out | network_bytes_egress | Bytes | Total sum of outgoing network traffic on the server for a selected period. This metric includes traffic from your database and Azure Database for MySQL Flexible Server features like monitoring, logs, etc. |
| Active Connections | active_connection | Count | The number of active connections to the server. Active connections are the total number of [threads connected](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Threads_connected) to your server, which also includes threads from [azure_superuser](../single-server/how-to-create-users.md). |
| Storage IO percent | io_consumption_percent | Percent | The percentage of IO used over a selected period. IO percent is for both read and write IOPS. |
| Storage IO Counts | storage_io_count | Count | The server's total count of I/O operations (both read and write) per minute. |
| Memory Percent | memory_percent | Percent | This metric represents the percentage of memory occupied by the Azure MySQL (mysqld) server process. This metric is calculated from the Total Memory Size (GB) available on your Azure Database for MySQL Flexible Server. |
| Total connections | total_connections | Count | The number of client connections to your Azure Database for MySQL Flexible Server instance. Total Connections is the sum of client connections using TCP/IP protocol over a selected period. |
| Aborted Connections | aborted_connections | Count | Total number of failed attempts to connect to your Azure Database for MySQL Flexible Server instance, for example, failed connection due to bad credentials. For more information on aborted connections, see this [documentation](https://dev.mysql.com/doc/refman/5.7/en/communication-errors.html). |
| Queries | queries | Count | Total number of queries executed per minute on your server. Total count of queries per minute on your server from your database workload and Azure MySQL processes. |
| Slow_queries | slow_queries | Count | The total count of slow queries on your server in the selected time range. |
| Active Transactions | active_transactions | Count | This metric represents the total number of transactions within MySQL. Active transactions include all transactions that have started but have yet to be committed or rolled back. |

## Storage breakdown metrics

Storage breakdown metrics provide valuable insights into the storage usage of your Azure Database for MySQL Flexible Server. These metrics give you a detailed breakdown of the storage limit, storage percentage, storage used, data storage used, ibdata1 storage used, binlog storage used, other storage used, and backup storage used. By monitoring these metrics, you can effectively manage your storage resources, optimize storage allocation, and ensure efficient utilization of your server's storage capacity. Understanding the storage breakdown metrics helps you make informed decisions to maintain the performance and availability of your Azure Database for MySQL Flexible Server.

The table below lists the storage breakdown metrics available for Azure Database for MySQL Flexible Server:

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| Storage Limit | storage_limit | Bytes | The maximum storage size configured for this server. |
| Storage Percent | storage_percent | Percent | The percentage of storage used out of the server's maximum storage available. |
| Storage Used | storage_used | Bytes | The amount of storage in use. The storage used by the service might include the database files, transaction logs, and server logs. |
| Data Storage Used | data_storage_used | Bytes | The amount of storage used for storing database files. |
| ibdata1 Storage Used | ibdata1_storage_used | Bytes | The amount of storage used for storing system tablespace (ibdata1) file. |
| Binlog Storage Used | binlog_storage_used | Bytes | The amount of storage used for storing binary log files. |
| Other Storage Used | other_storage_used | Bytes | The amount of storage used for other components and metadata files. |
| Backup Storage Used | backup_storage_used | Bytes | The amount of backup storage used. |

## Replication metrics

Replication metrics provide valuable insights into the performance and status of replication in Azure Database for MySQL Flexible Server. These metrics allow you to monitor the replication lag, check the status of replica and HA IO/SQL threads, and measure the replication latency. By tracking these metrics, you can ensure the reliability and efficiency of your replication setup, identify any potential issues or delays, and take appropriate actions to maintain data consistency and availability. Let's explore the different replication metrics available for Azure Database for MySQL Flexible Server.

The table below lists the replication metrics available for Azure Database for MySQL Flexible Server:

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| Replication Lag | replication_lag | Seconds | Replication lag is the number of seconds behind the replica in replaying the transactions received from the source server. This metric is calculated from "Seconds_behind_Master" from the command "SHOW SLAVE STATUS" command and is only available for replica servers. For more information, see "[Troubleshoot replication latency in Azure Database for MySQL - Flexible Server](../how-to-troubleshoot-replication-latency.md)" |
| Replica IO Status | replica_io_running | State | Replica IO Status indicates the state of [replication I/O thread](https://dev.mysql.com/doc/refman/8.0/en/replication-implementation-details.html). The metric value is 1 if the I/O thread runs and 0 if not. |
| Replica SQL Status | replica_sql_running | State | Replica SQL Status indicates the state of [replication SQL thread](https://dev.mysql.com/doc/refman/8.0/en/replication-implementation-details.html). The metric value is 1 if the SQL thread runs and 0 if not. |
| HA IO Status | ha_io_running | State | HA IO Status indicates the state of [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md). The metric value is 1 if the I/O thread runs and 0 if not. |
| HA SQL Status | ha_sql_running | State | HA SQL Status indicates the state of [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md). The metric value is 1 if the SQL thread runs and 0 if not. |
| HA Replication Lag | ha_replication_lag | Seconds | HA Replication lag is the number of seconds the HA Standby server is behind in replaying the transactions received from the source server. This metric is calculated from "Seconds_behind_Master" from the command "SHOW SLAVE STATUS" command and is available only for HA standby servers. |

## Enhanced metrics

In addition to the standard metrics provided by Azure Database for MySQL Flexible Server, enhanced metrics are available to gain deeper insights into your server's performance. These enhanced metrics provide more granular information about specific aspects of your workload.

### DML statistics

The DML (Data Manipulation Language) statistics metrics give you visibility into the number of select, update, insert, and delete statements executed on your server. By monitoring these metrics, you can track the usage and performance of your database operations and identify any potential bottlenecks or inefficiencies.

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| Com_select | Com_select | Count | The total count of select statements executed on your server in the selected time range. |
| Com_update | Com_update | Count | The total count of update statements executed on your server in the selected time range. |
| Com_insert | Com_insert | Count | The total count of insert statements executed on your server in the selected time range. |
| Com_delete | Com_delete | Count | The total count of deleted statements executed on your server in the selected time range. |

### DDL statistics

The DDL (Data Definition Language) statistics metrics provide information about how often you can create a database, drop a database, create a table, drop a table, and alter table statements executed on your server. These metrics help you understand the frequency and impact of schema changes in your database, allowing you to optimize your database design and improve overall performance.

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| Com_create_db | Com_create_db | Count | The total count of created database statements executed on your server in the selected time range. |
| Com_drop_db | Com_drop_db | Count | The total count of drop database statements executed on your server in the selected time range. |
| Com_create_table | Com_create_table | Count | The total count of create table statements executed on your server in the selected time range. |
| Com_drop_table | Com_drop_table | Count | The total count of drop table statements executed on your server in the selected time range. |
| Com_Alter | Com_Alter | Count | The total count of alter table statements executed on your server in the selected time range. |

### Innodb metrics

The Innodb metrics focus on the performance of the InnoDB storage engine, which is the default engine for Azure Database for MySQL Flexible Server. These metrics include InnoDB row lock time, InnoDB row lock waits, Innodb buffer pool reads, Innodb buffer pool read requests, and more. By monitoring these metrics, you can gain insights into the efficiency and effectiveness of your database's storage and caching mechanisms.

These enhanced metrics provide valuable information for optimizing your workload and improving the performance of your Azure Database for MySQL Flexible Server. Using these metrics, you can make data-driven decisions to enhance your database operations' scalability, reliability, and efficiency.

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| InnoDB Row Lock Time | innodb_row_lock_time | Milliseconds | InnoDB row lock time measures the duration of time in milliseconds for InnoDB row-level locks. |
| InnoDB Row Lock Waits | innodb_row_lock_waits | Count | InnoDB row lock waits metric counts the number of times a query had to wait for an InnoDB row-level lock. |
| Innodb_buffer_pool_reads | Innodb_buffer_pool_reads | Count | The total count of logical reads that the InnoDB engine couldn't satisfy from the Innodb buffer pool and had to be fetched from the disk. |
| Innodb_buffer_pool_read_requests | Innodb_buffer_pool_read_requests | Count | The total count of logical read requests to read from the Innodb Buffer pool. |
| Innodb_buffer_pool_pages_free | Innodb_buffer_pool_pages_free | Count | The total count of free pages in the InnoDB buffer pool. |
| Innodb_buffer_pool_pages_data | Innodb_buffer_pool_pages_data | Count | The total count of pages in the InnoDB buffer pool containing data. The number includes both dirty and clean pages. |
| Innodb_buffer_pool_pages_dirty | Innodb_buffer_pool_pages_dirty | Count | The total count of pages in the InnoDB buffer pool containing dirty pages. |
| MySQL History List Length | trx_rseg_history_len | Count | This metric calculates the number of changes in the database, specifically the number of records containing previous changes. It's related to the rate of changes to data, causing new row versions to be created. An increasing history list length can impact the performance of the database. |
| MySQL Lock Timeouts | lock_timeouts | Count | This metric represents the number of times a query has timed out due to a lock. This typically occurs when a query waits for a lock on a row or table held by another query for a longer time than the `innodb_lock_wait_timeout` setting. |
| MySQL Lock Deadlocks | lock_deadlock | Count | This metric represents the number of [deadlocks](https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html) on your Azure Database for MySQL Flexible Server instance in the selected period. |

## Server logs

In Azure Database for MySQL Flexible Server, users can configure and download server logs to assist with troubleshooting efforts. With this feature enabled, an Azure Database for MySQL Flexible Server instance starts capturing events of the selected log type and writes them to a file. You can then use the Azure portal and Azure CLI to download the files to work with them.
The server logs feature is disabled by default. For information about how to enable server logs, see [Enable and download server logs for Azure Database for MySQL - Flexible Server](how-to-server-logs-portal.md)

Server logs support enabling and downloading [slow query logs](concepts-slow-query-logs.md) and [error logs](concepts-error-logs.md).
To perform a historical analysis of your data, in the Azure portal, on the Diagnostics settings pane for your server, add a diagnostic setting to send the logs to the Log Analytics workspace, Azure Storage, or event hubs. For more information, see [Set up diagnostics](./tutorial-query-performance-insights.md#set-up-diagnostics).

### Server logs retention

When logging is enabled for an Azure Database for MySQL Flexible Server instance, logs are available up to seven days from their creation. If the total size of the available logs exceeds 7 GB, then the oldest files are deleted until space is available.
The 7-GB storage limit for server logs is available free of cost and can't be extended.
Logs are rotated every 24 hours or 500 MB, whichever comes first.

## Related content

- [Set up alerts on metrics for Azure Database for MySQL - Flexible Server](how-to-alert-on-metric.md)
- [Enable and download server logs for Azure Database for MySQL - Flexible Server](how-to-server-logs-portal.md)
- [List and download Azure Database for MySQL - Flexible Server logs by using the Azure CLI](how-to-server-logs-cli.md)
