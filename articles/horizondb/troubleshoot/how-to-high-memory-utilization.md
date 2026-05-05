---
title: High Memory Utilization in Azure HorizonDB
description: Troubleshooting guide for high memory utilization in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 05/05/2026
ms.service: azure-database-postgresql
ms.subservice: performance
ms.topic: troubleshooting-general
---

# Troubleshoot high memory utilization in Azure HorizonDB

This article describes how to identify the root cause of high memory utilization. It also provides possible remedial actions to control CPU utilization when using [What is Azure HorizonDB?](../overview.md)

In this article, you can learn:

- About troubleshooting guides to identify and get recommendations to mitigate root causes.
- About tools to identify high memory utilization.
- Reasons for high memory utilization and remedial actions.

<a id="troubleshooting-guides"></a>

## Troubleshoot guides

Using the **Troubleshooting guides** you can identify the probable root cause of a high CPU scenario, and can read through recommendations to mitigate the problem found.

To learn how to set up and use the troubleshooting guides, follow [setup troubleshooting guides](how-to-troubleshooting-guides.md).

## Tools to identify high memory utilization

Consider the use of the following list of tools to identify high CPU utilization.

### Azure Metrics

Azure Metrics is a good starting point to monitor the percentage of memory in use for a specific period.

For proactive monitoring, you can configure alerts on the metrics. For step-by-step guidance, see [Use the Azure portal to set up alerts on metrics in Azure HorizonDB](../monitor/how-to-alert-on-metrics.md).

### Query store

Query store automatically captures the history of queries and runtime statistics, and it retains them for your review. It slices the data by time, so that you can see temporal usage patterns. Data for all users, databases, and queries is stored in a database named `azure_sys` in the Azure HorizonDB instance.

Query store can correlate wait event information with query run time statistics. Use query store to identify queries that have high memory consumption during the period of interest.

For more information, see [query store](../monitor/concepts-query-store.md).

## Reasons and remedial actions

Consider the following reasons and remedial actions for resolving high memory utilization.

### Server parameters

An inappropriate configuration of the following server parameters could have an impact in the amount of memory consumed by your workload. Therefore, their values should be reviewed and adjusted according to your needs:

- [work_mem](../server-parameters/param-resource-usage-memory.md#work_mem).
- [maintenance_work_mem](../server-parameters/param-resource-usage-memory.md#maintenance_work_mem). - [shared_buffers](../server-parameters/param-resource-usage-memory.md#shared_buffers).
- [max_connections](../server-parameters/param-connections-authentication-connection-settings.md#max_connections).

### Use EXPLAIN ANALYZE

Once you know the queries that are consuming more memory, use **EXPLAIN ANALYZE** to further investigate and tune them.

For more information about the **EXPLAIN ANALYZE** command, review its [documentation](https://www.postgresql.org/docs/current/sql-explain.html).

## Related content

- [Troubleshoot high CPU utilization in Azure HorizonDB](how-to-high-cpu-utilization.md)
- [Troubleshoot high IOPS utilization in Azure HorizonDB](how-to-high-io-utilization.md)
- [Troubleshoot and identify slow-running queries in Azure HorizonDB](how-to-identify-slow-queries.md)
- [Parameters in Azure HorizonDB](../server-parameters/concepts-server-parameters.md)
- [Autovacuum tuning in Azure HorizonDB](how-to-autovacuum-tuning.md)
