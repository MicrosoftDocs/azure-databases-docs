---
title: Best Practices for Query Store in Azure HorizonDB
description: This article describes best practices for query store in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: monitoring
ms.topic: best-practice
ms.custom:
  - build-2026-public-preview
---

# Best practices for query store for Azure HorizonDB (Preview)

This article outlines best practices for using query store in Azure HorizonDB.

## Set the optimal query capture mode

Configure query store so that it captures the queries that matter to you.

| **pg_qs.query_capture_mode** | **Scenario** |
| --- | --- |
| `all` | Captures all queries (top-level or nested) and their execution frequencies and other statistics. Identify new queries in your workload. Detect if unplanned queries are used, to identify opportunities for user defined parameterization or automatic parameterization. |
| `top` | Captures top-level queries only. Top-level queries are those issued directly by clients. These don't include nested statements (statements executed inside a procedure or a function). |
| `none` | Doesn't capture any new queries, while configured like this. You might want to set it to this value if you've already captured a queryset in the time window that you wanted to investigate, and you don't want to continue recording any new queries. `none` is suitable for testing and bench-marking environments. `none` should be used with caution as you might miss the opportunity to track and optimize important new queries. |
| > [!NOTE] |
| > `pg_qs.query_capture_mode` supersedes `pgms_wait_sampling.query_capture_mode`. If `pg_qs.query_capture_mode` is `none`, the `pgms_wait_sampling.query_capture_mode` setting has no effect. |

## Keep the data you need

The `pg_qs.retention_period_in_days` parameter specifies the data retention period for query store. Statistics recorded which are older than that period are deleted. And query texts or query plans for queries that have no statistics referring to them, are also deleted. By default, query store is configured to retain the data for seven days. Avoid keeping historical data that you don't plan to use. Increase the value if you need to keep data for longer.

## Related content

- [Query store in Azure HorizonDB (Preview)](concepts-query-store.md)
- [Usage scenarios for query store in Azure HorizonDB (Preview)](concepts-query-store-scenarios.md)
