---
title: Query store best practices
description: This article describes best practices for query store in Azure Database for PostgreSQL - Flexible Server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 11/05/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.custom:
  - ignite-2024
ms.topic: conceptual
ms.custom:
  - ignite-2024
---

# Best practices for query store in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article outlines best practices for using query store in Azure Database for PostgreSQL - Flexible Server.

## Set the optimal query capture mode

Configure query store so that it captures the queries that matter to you.

| **pg_qs.query_capture_mode** | **Scenario** |
|---|---|
| `all`	| Captures all queries (top-level or nested) and their execution frequencies and other statistics. Identify new queries in your workload. Detect if ad-hoc queries are used, to identify opportunities for user defined parameterization or automatic parameterization. |
| `top` | Captures top-level queries only. Top-level queries are those issued directly by clients. These don't include nested statements (statements executed inside a procedure or a function). |
| `top` | Doesn't capture any new queries, while configured like this. You might want to set it to this value if you've already captured a query set in the time window that you wanted to investigate, and you don't want to continue recording any new queries. `none` is suitable for testing and bench-marking environments. `none` should be used with caution as you might miss the opportunity to track and optimize important new queries. |


> [!NOTE] 
> `pg_qs.query_capture_mode` supersedes `pgms_wait_sampling.query_capture_mode`. If `pg_qs.query_capture_mode` is `none`, the `pgms_wait_sampling.query_capture_mode` setting has no effect. 


## Keep the data you need

The `pg_qs.retention_period_in_days` parameter specifies the data retention period for query store. Statistics recorded which are older than that period are deleted. And query texts or query plans for queries that have no statistics referring to them, are also deleted. By default, query store is configured to retain the data for seven days. Avoid keeping historical data that you don't plan to use. Increase the value if you need to keep data for longer.


## Related content

- [monitor performance with query store](concepts-query-store.md)
- [scenarios where query store can be especially helpful](concepts-query-store-scenarios.md)
- [visualizing data from query store via Query Performance Insight](./concepts-query-performance-insight.md)