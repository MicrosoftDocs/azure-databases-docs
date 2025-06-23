---
title: Monitoring Best Practices
description: This article describes the best practices to monitor Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: best-practice
---

# Best practices for monitoring Azure Database for MySQL - Flexible Server

Learn about the best practices that can be used to monitor your database operations and ensure that the performance isn't compromised as data size grows. As we add new capabilities to the platform, we'll continue to refine the best practices detailed in this section.

## Layout of the current monitoring toolkit

Azure Database for MySQL Flexible Server provides tools and methods you can use to monitor usage easily, add, or remove resources (such as CPU, memory, or I/O), troubleshoot potential problems, and help improve the performance of a database. You can [monitor performance metrics](concepts-monitoring.md#metrics) regularly to see the average, maximum, and minimum values for various time ranges.

You can [set up alerts](how-to-alert-on-metric.md#create-an-alert-rule-on-a-metric-from-the-azure-portal) for a metric threshold, so you're informed if the server has reached those limits and take appropriate actions.

Monitor the database server to make sure that the resources assigned to the database can handle the application workload. If the database is hitting resource limits, consider:

- Identifying and optimizing the top resource-consuming queries.
- Adding more resources by upgrading the service tier.

### CPU utilization

Monitor CPU usage and if the database is exhausting CPU resources. If CPU usage is 90% or more, than you should scale up your compute by increasing the number of vCores or scale to next pricing tier. Make sure that the throughput or concurrency is as expected as you scale up/down the CPU.

### Memory

The amount of memory available for the Azure Database for MySQL Flexible Server database server is proportional to the [number of vCores](../single-server/concepts-pricing-tiers.md). Make sure the memory is enough for the workload. Load test your application to verify the memory is sufficient for read and write operations. If the database memory consumption frequently grows beyond a defined threshold, this indicates that you should upgrade your instance by increasing vCores or higher performance tier. Use [Query Store](../single-server/concepts-query-store.md), [Query Performance Recommendations](../single-server/concepts-performance-recommendations.md) to identify queries with the longest duration, most executed. Explore opportunities to optimize.

### Storage

The [amount of storage](../single-server/how-to-create-manage-server-portal.md#scale-compute-and-storage) provisioned for Azure Database for MySQL Flexible Server determines the IOPs for your server. The storage used by the service includes the database files, transaction logs, the server logs and backup snapshots. Ensure that the consumed disk space doesn't constantly exceed above 85 percent of the total provisioned disk space. If that is the case, you need to delete or archive data from the database server to free up some space.

### Network traffic

**Network Receive Throughput, Network Transmit Throughput** – The rate of network traffic to and from the Azure Database for MySQL Flexible Server instance in megabytes per second. You need to evaluate the throughput requirement for Azure Database for MySQL Flexible Server and constantly monitor the traffic if throughput is lower than expected.

### Database connections

**Database Connections** – The number of client sessions that are connected to the Azure Database for MySQL Flexible Server instance should be aligned with the [connection limits for the selected SKU](concepts-server-parameters.md#max_connections) size.

## Related content

- [Best practices for optimal performance of Azure Database for MySQL - Flexible Server](concept-performance-best-practices.md)
- [Best practices for server operations on Azure Database for MySQL - Flexible Server](concept-operation-excellence-best-practices.md)
