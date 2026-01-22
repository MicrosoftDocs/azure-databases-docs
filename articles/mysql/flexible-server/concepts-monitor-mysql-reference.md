---
title: Monitoring Data Reference for Azure Database for MySQL
description: This article contains important reference material you need when you monitor Azure Database for MySQL.
author: sk-microsoft
ms.author: sakirta
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.topic: reference
ms.custom:
  - horz-monitor
---

# Azure Database for MySQL monitor data references

[!INCLUDE [horz-monitor-ref-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-intro.md)]

See [Monitor Azure Database for MySQL](concepts-monitor-mysql.md) for details on the data you can collect for Azure Database for MySQL and how to use it.

[!INCLUDE [horz-monitor-ref-metrics-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-intro.md)]

### Supported metrics for Microsoft.DBforMySQL\flexibleServers

The following table lists the metrics available for the Microsoft.DBforMySQL\flexibleServers resource type.

[!INCLUDE [horz-monitor-ref-metrics-tableheader](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-tableheader.md)]

[!INCLUDE [Microsoft.DBforMySQL\flexibleServers](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/metrics/microsoft-dbformysql-flexibleservers-metrics-include.md)]

This table includes more detailed descriptions of some metrics.

| Metric display name | Description |
| --- | --- |
| MySQL Uptime | This metric indicates the length of time that the MySQL server has been running. In a high-availability (HA) server setup, the system continuously displays the uptime of the current primary server node in seconds. This uptime value doesn't reset during a failover event, as the nodes aren't restarted. |
| Host CPU percent | Host CPU percent is the total utilization of the CPU to process all the tasks on your server over a selected period. This metric includes the workload of your Azure Database for MySQL flexible server instance and Azure MySQL process. High CPU percent can help you find if your database server has a heavier workload than it can handle. This metric is equivalent to total CPU utilization and is similar to CPU utilization on any virtual machine. |
| CPU Credit Consumed | **This is for Burstable Tier Only** CPU credit is calculated based on workload. For more information, see [B-series burstable virtual machine sizes](/azure/virtual-machines/sizes-b-series-burstable). |
| CPU Credit Remaining | **This is for Burstable Tier Only** CPU remaining is calculated based on workload. For more information, see [B-series burstable virtual machine sizes](/azure/virtual-machines/sizes-b-series-burstable). |
| Host Network In | Total sum of incoming network traffic on the server for a selected period. This metric includes traffic to your database and Azure Database for MySQL flexible server features like monitoring, logs, etc. |
| Host Network out | Total sum of outgoing network traffic on the server for a selected period. This metric includes traffic from your database and Azure Database for MySQL flexible server features like monitoring, logs, etc. |
| Active Connections | The number of active connections to the server. Active connections are the total number of [threads connected](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Threads_connected) to your server, which also includes threads from [azure_superuser](security-how-to-create-users.md). |
| Storage IO percent | The percentage of IO used over a selected period. IO percent is for both read and write IOPS. |
| Storage IO Counts | The server's total count of I/O operations (both read and write) per minute. |
| Memory Percent | This metric represents the percentage of memory occupied by the Azure MySQL (`mysqld`) server process. This metric is calculated from the Total Memory Size (GB) available on your Azure Database for MySQL flexible server. |
| Total connections | The number of client connections to your Azure Database for MySQL flexible server instance. Total Connections is the sum of client connections using TCP/IP protocol over a selected period. |
| Aborted Connections | Total number of failed attempts to connect to your Azure Database for MySQL flexible server instance, for example, failed connection due to bad credentials. For more information on aborted connections, see this [documentation](https://dev.mysql.com/doc/refman/5.7/en/communication-errors.html). |
| Queries | Total number of queries executed per minute on your server. Total count of queries per minute on your server from your database workload and Azure MySQL processes. |
| Slow_queries | The total count of slow queries on your server in the selected time range. |
| Active Transactions | This metric represents the total number of transactions within MySQL. Active transactions include all transactions that started but have yet to be committed or rolled back. |

*Storage breakdown metrics* provide valuable insights into the storage usage of your Azure Database for MySQL flexible server. These metrics give you a detailed breakdown of the storage limit, storage percentage, storage used, data storage used, ibdata1 storage used, binlog storage used, other storage used, and backup storage used. By monitoring these metrics, you can effectively manage your storage resources, optimize storage allocation, and ensure efficient utilization of your server's storage capacity. Understanding the storage breakdown metrics helps you make informed decisions to maintain the performance and availability of your Azure Database for MySQL flexible server.

The table below lists descriptions for the storage breakdown metrics available for Azure Database for MySQL flexible server:

| Metric display name | Description |
| --- | --- |
| Storage Limit | The maximum storage size configured for this server. |
| Storage Percent | The percentage of storage used out of the server's maximum storage available. |
| Storage Used | The amount of storage in use. The storage used by the service might include the database files, transaction logs, and server logs. |
| Data Storage Used | The amount of storage used for storing database files. |
| ibdata1 Storage Used | The amount of storage used for storing system tablespace (ibdata1) file. |
| Binlog Storage Used | The amount of storage used for storing binary log files. |
| Other Storage Used | The amount of storage used for other components and metadata files. |
| Backup Storage Used | The amount of backup storage used. |

*Replication metrics* provide valuable insights into the performance and status of replication in Azure Database for MySQL flexible server. These metrics allow you to monitor the replication lag, check the status of replica and HA IO/SQL threads, and measure the replication latency. By tracking these metrics, you can ensure the reliability and efficiency of your replication setup, identify any potential issues or delays, and take appropriate actions to maintain data consistency and availability. Let's explore the different replication metrics available for Azure Database for MySQL flexible server.

The table below lists the replication metrics available for Azure Database for MySQL flexible server:

| Metric display name | Description |
| --- | --- |
| Replication Lag | Replication lag is the number of seconds behind the replica in replaying the transactions received from the source server. This metric is only available for replica servers. For more information, see [Troubleshoot replication latency in Azure Database for MySQL - Flexible Server](../how-to-troubleshoot-replication-latency.md). |
| Replica IO Status | Replica IO Status indicates the state of [replication I/O thread](https://dev.mysql.com/doc/refman/8.0/en/replication-implementation-details.html). The metric value is 1 if the I/O thread runs and 0 if not. |
| Replica SQL Status | Replica SQL Status indicates the state of [replication SQL thread](https://dev.mysql.com/doc/refman/8.0/en/replication-implementation-details.html). The metric value is 1 if the SQL thread runs and 0 if not. |
| HA IO Status | HA IO Status indicates the state of [High-availability in Azure Database for MySQL](concepts-high-availability.md). The metric value is 1 if the I/O thread runs and 0 if not. |
| HA SQL Status | HA SQL Status indicates the state of [High-availability in Azure Database for MySQL](concepts-high-availability.md). The metric value is 1 if the SQL thread runs and 0 if not. |
| HA Replication Lag | HA Replication lag is the number of seconds the HA Standby server is behind in replaying the transactions received from the source server. This metric is available only for HA standby servers. |

In addition to the standard metrics provided by Azure Database for MySQL flexible server, enhanced metrics are available to gain deeper insights into your server's performance. These enhanced metrics provide more granular information about specific aspects of your workload.

The *Data Manipulation Language (DML) statistics metrics* give you visibility into the number of select, update, insert, and delete statements executed on your server. By monitoring these metrics, you can track the usage and performance of your database operations and identify any potential bottlenecks or inefficiencies.

| Metric display name | Description |
| --- | --- |
| Com_select | The total count of select statements executed on your server in the selected time range. |
| Com_update | The total count of update statements executed on your server in the selected time range. |
| Com_insert | The total count of insert statements executed on your server in the selected time range. |
| Com_delete | The total count of deleted statements executed on your server in the selected time range. |

The *Data Definition Language (DDL) statistics metrics* provide information about how often you can create a database, drop a database, create a table, drop a table, and alter table statements run on your server. These metrics help you understand the frequency and impact of schema changes in your database, allowing you to optimize your database design and improve overall performance.

| Metric display name | Description |
| --- | --- |
| Com_create_db | The total count of created database statements executed on your server in the selected time range. |
| Com_drop_db | The total count of drop database statements executed on your server in the selected time range. |
| Com_create_table | The total count of create table statements executed on your server in the selected time range. |
| Com_drop_table | The total count of drop table statements executed on your server in the selected time range. |
| Com_Alter | The total count of alter table statements executed on your server in the selected time range. |

The *Innodb metrics* focus on the performance of the InnoDB storage engine, which is the default engine for Azure Database for MySQL flexible server. These metrics include InnoDB row lock time, InnoDB row lock waits, Innodb buffer pool reads, Innodb buffer pool read requests, and more. By monitoring these metrics, you can gain insights into the efficiency and effectiveness of your database's storage and caching mechanisms.

These enhanced metrics provide valuable information for optimizing your workload and improving the performance of your Azure Database for MySQL flexible server. Using these metrics, you can make data-driven decisions to enhance your database operations' scalability, reliability, and efficiency.

| Metric display name | Description |
| --- | --- |
| InnoDB Row Lock Time | InnoDB row lock time measures the duration of time in milliseconds for InnoDB row-level locks. |
| InnoDB Row Lock Waits | InnoDB row lock waits metric counts the number of times a query had to wait for an InnoDB row-level lock. |
| Innodb_buffer_pool_reads | The total count of logical reads that the InnoDB engine couldn't satisfy from the Innodb buffer pool and had to be fetched from the disk. |
| Innodb_buffer_pool_read_requests | The total count of logical read requests to read from the Innodb Buffer pool. |
| Innodb_buffer_pool_pages_free | The total count of free pages in the InnoDB buffer pool. |
| Innodb_buffer_pool_pages_data | The total count of pages in the InnoDB buffer pool containing data. The number includes both dirty and clean pages. |
| Innodb_buffer_pool_pages_dirty | The total count of pages in the InnoDB buffer pool containing dirty pages. |
| MySQL History List Length | This metric calculates the number of changes in the database, specifically the number of records containing previous changes. It's related to the rate of changes to data, causing new row versions to be created. An increasing history list length can affect the performance of the database. |
| MySQL Lock Timeouts | This metric represents the number of times a query has timed out due to a lock. This situation typically occurs when a query waits for a lock on a row or table held by another query for a longer time than the `innodb_lock_wait_timeout` setting. |
| MySQL Lock Deadlocks | This metric represents the number of [deadlocks](https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html) on your Azure Database for MySQL flexible server instance in the selected period. |
| [!INCLUDE [horz-monitor-ref-metrics-dimensions-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-dimensions-intro.md)] | [!INCLUDE [horz-monitor-ref-no-metrics-dimensions](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-no-metrics-dimensions.md)] |

### Troubleshoot metrics

Sometimes, you might encounter issues with creating, customizing, or interpreting charts in Azure Metrics Explorer.

A *Chart showing no data* could arise due to various factors. These issues might include the Microsoft Insights resource provider not being registered for your subscription or you lacking adequate access rights to your Azure Database for MySQL. Other possibilities could be that your resource didn't generate metrics within the chosen time frame or the selected time range exceeds 30 days.

Several reasons that follow can cause this behavior:

- *Microsoft.Insights resource provider isn't registered*: Exploring metrics requires Microsoft.Insights resource provider registered in your subscription. Register your server manually by following the steps described in [Azure resource providers and types](/azure/azure-resource-manager/management/resource-providers-and-types).
- *Insufficient access rights to your resource*: Ensure you have sufficient permissions for your Azure Database for MySQL from which you're exploring metrics. Your resource didn't emit metrics during the selected time range. Change the time of the chart to a wider range. In Azure, [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) controls access to metrics. You must be a member of [monitoring reader](/azure/role-based-access-control/built-in-roles#monitoring-reader), [monitoring contributor](/azure/role-based-access-control/built-in-roles#monitoring-contributor), or [contributor](/azure/role-based-access-control/built-in-roles#contributor) to explore metrics for any resource.
- *Your resource didn't emit metrics during the selected time range*: This behavior could be due to several reasons. One possibility is that your resource didn't generate metrics within the chosen time frame. Change the time of the chart to a broader range to see if this approach resolves the issue. For more detailed information on troubleshooting this issue, refer to the [Azure Monitor metrics troubleshooting guide](/azure/azure-monitor/essentials/metrics-troubleshoot#your-resource-didnt-emit-metrics-during-the-selected-time-range).
- *Time range greater than 30 days*: Verify that the difference between the start and end dates in the time picker doesn't exceed the 30-day interval. For more detailed information on troubleshooting metrics, refer to the [Azure Monitor metrics troubleshooting guide](/azure/azure-monitor/essentials/metrics-troubleshoot).
- *Dashed Line Indication*: In Azure Monitor, a dashed line signifies a gap in data, or a *null value*, between two points of known time grain data. This aspect is a deliberate design that helps detect missing data points. If your chart displays dashed lines, it indicates missing data. For more information, see [Chart shows dashed line](/azure/azure-monitor/essentials/metrics-troubleshoot#chart-shows-dashed-line).

For more detailed information on troubleshooting metrics, refer to the [Azure Monitor metrics troubleshooting guide.](/azure/azure-monitor/essentials/metrics-troubleshoot)

> [!NOTE]  
> Metrics marked as deprecated are scheduled to be removed from the Azure portal. You should ignore these metrics when monitoring your Azure Database for MySQL flexible server.

[!INCLUDE [horz-monitor-ref-resource-logs](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-resource-logs.md)]

### Supported resource logs for Microsoft.DBforMySQL\flexibleServers

[!INCLUDE [Microsoft.DBforMySQL\flexibleServers](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/logs/microsoft-dbformysql-flexibleservers-logs-include.md)]

[!INCLUDE [horz-monitor-ref-logs-tables](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-logs-tables.md)]

### Azure Database for MySQL Microsoft.DBforMySQL\flexibleServers

- [AzureActivity](/azure/azure-monitor/reference/tables/azureactivity#columns)
- [AzureDiagnostics](/azure/azure-monitor/reference/tables/azurediagnostics#columns)
- [AzureMetrics](/azure/azure-monitor/reference/tables/azuremetrics#columns)

[!INCLUDE [horz-monitor-ref-activity-log](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-activity-log.md)]

- [Microsoft.DBforMySQL\flexibleServers resource provider operations](/azure/role-based-access-control/resource-provider-operations#microsoftdocumentdb)

## Related content

- [Monitor Azure Database for MySQL - Flexible Server](concepts-monitor-mysql.md)
- [Monitor Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource)
