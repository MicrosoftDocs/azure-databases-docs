---
title: Best Practices for Query Store in Azure Database for PostgreSQL Flexible Server
description: This article describes best practices for query store in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to configure the optimal query capture mode, so that query store captures the queries that matter most to my workload.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: monitoring
ms.topic: best-practice
---

# Best practices for query store in Azure Database for PostgreSQL flexible server

This article outlines best practices for using query store in an Azure Database for PostgreSQL flexible server.

## Set the optimal query capture mode

Configure query store to capture the queries that matter to you.

| **pg_qs.query_capture_mode** | **Scenario** |
|---|---|
| `all`	| Captures all queries (top-level or nested) and their execution frequencies and other statistics. Use this mode to identify new queries in your workload. Detect if ad-hoc queries are used, to identify opportunities for user defined parameterization or automatic parameterization. |
| `top` | Captures top-level queries only. Top-level queries are those issued directly by clients. These queries don't include nested statements (statements executed inside a procedure or a function). |
| `none` | Doesn't capture any new queries. Set this value if you already captured a query set in the time window that you wanted to investigate, and you don't want to continue recording any new queries. `none` is suitable for testing and benchmarking environments. Use `none` with caution as you might miss the opportunity to track and optimize important new queries. |


> [!NOTE] 
> `pg_qs.query_capture_mode` supersedes `pgms_wait_sampling.query_capture_mode`. If `pg_qs.query_capture_mode` is `none`, the `pgms_wait_sampling.query_capture_mode` setting has no effect. 


## Keep the data you need

The `pg_qs.retention_period_in_days` parameter specifies the data retention period for query store. The system deletes statistics that are older than that period. The system also deletes query texts or query plans for queries that have no statistics referring to them. By default, query store is configured to retain the data for seven days. Avoid keeping historical data that you don't plan to use. Increase the value if you need to keep data for longer.


## Related content

- [Query store](concepts-query-store.md)
- [Usage scenarios for query store](concepts-query-store-scenarios.md)
- [Query Performance Insight](concepts-query-performance-insight.md)
