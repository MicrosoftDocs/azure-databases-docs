---
title: Monitoring Best Practices
description: This article describes the best practices to monitor Azure Database for MySQL - Flexible Server.
author: VandhanaMehta  
ms.author: vamehta  
ms.reviewer: maghan
ms.date: 08/20/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: best-practice
---

# Best practices for monitoring Azure Database for MySQL

Learn about the best practices for monitoring your database operations. These practices help ensure that performance stays strong as your data size grows. As we add new capabilities to the platform, we continue to refine the best practices detailed in this section.

## Layout of the current monitoring toolkit

Azure Database for MySQL Flexible Server provides tools and methods you can use to monitor usage easily. You can add or remove resources such as CPU, memory, or I/O. You can troubleshoot potential problems and help improve the performance of a database. You can [monitor performance metrics](concepts-monitoring.md#metrics) regularly to see the average, maximum, and minimum values for various time ranges.

You can [set up alerts](how-to-alert-on-metric.md#create-an-alert-rule-on-a-metric-from-the-azure-portal) for a metric threshold. With these alerts, you're informed if the server reaches those limits and can take appropriate actions.

Monitor the database server to make sure that the resources assigned to the database can handle the application workload. If the database hits resource limits, consider:

- Identifying and optimizing the top resource-consuming queries.
- Adding more resources by upgrading the service tier.

### CPU utilization

Monitor CPU usage to check if the database exhausts CPU resources. If CPU usage reaches 90% or more, scale up your compute by increasing the number of vCores or scale to next pricing tier. Make sure that the throughput or concurrency meets your expectations as you scale up or down the CPU.

### Memory

The amount of memory available for the Azure Database for MySQL Flexible Server database server is proportional to the [number of vCores](../single-server/concepts-pricing-tiers.md). Make sure the memory is enough for the workload. Load test your application to verify the memory is sufficient for read and write operations. If the database memory consumption frequently grows beyond a defined threshold, upgrade your instance by increasing vCores or higher performance tier. Use [Query Store](../single-server/concepts-query-store.md), [Query Performance Recommendations](../single-server/concepts-performance-recommendations.md) to identify queries with the longest duration and most executed. Explore opportunities to optimize.

### Storage

The [amount of storage](../single-server/how-to-create-manage-server-portal.md#scale-compute-and-storage) you provision for Azure Database for MySQL Flexible Server determines the IOPs for your server. The service uses storage for the database files, transaction logs, the server logs, and backup snapshots. Make sure that the consumed disk space doesn't constantly exceed 85 percent of the total provisioned disk space. If it does, delete or archive data from the database server to free up space.

### Network traffic

**Network Receive Throughput, Network Transmit Throughput** – The rate of network traffic to and from the Azure Database for MySQL Flexible Server instance in megabytes per second. Evaluate the throughput requirement for Azure Database for MySQL Flexible Server and constantly monitor the traffic if throughput is lower than expected.

### Database connections

**Database Connections** – The number of client sessions that are connected to the Azure Database for MySQL Flexible Server instance. This number should align with the [connection limits for the selected SKU](concepts-server-parameters.md#max_connections) size.

## Related content

- [Best practices for optimal performance of Azure Database for MySQL - Flexible Server](concept-performance-best-practices.md)
- [Best practices for server operations on Azure Database for MySQL - Flexible Server](concept-operation-excellence-best-practices.md)
