---
title: MongoDB Feature Compatibility
description: Discover MongoDB feature compatibility in Azure DocumentDB. Learn supported aggregation stages, commands, and features. Optimize your workloads today.
author: suvishodcitus
ms.author: suvishod
ms.topic: concept-article
ms.date: 11/05/2025
ai-usage: ai-assisted
---

# MongoDB feature compatibility in Azure DocumentDB

Azure DocumentDB fully implements the MongoDB wire protocol for feature compatibility, allowing you to run nearly all MongoDB workloads without any application changes. This native Azure service offers optimized performance, lower total cost of ownership (TCO), and built-in AI capabilities, empowering modern, data-driven applications with ease. The tables in this article outline MongoDB features that are unsupported or limited in Azure DocumentDB. As a fully managed PaaS solution, Azure DocumentDB abstracts or restricts certain administrative operations to ensure enhanced reliability, security, and performance - so you can focus on building, not managing infrastructure.

## Aggregation pipeline stages and aggregators

This table outlines the compatibility of aggregation pipeline stages and aggregators in Azure DocumentDB.

| | Description |
| --- | --- |
| **`$planCacheStats`** | Not applicable, as the service automatically manages the query plan cache. |
| **`$listSearchIndexes`** | Not prioritized due to weak customer demand. |
| **`$listSampledQueries`** | Not prioritized due to weak customer demand. |
| **`$shardedDataDistribution`** | Not prioritized due to weak customer demand. |

## Database commands

This table outlines the compatibility of database command categories in Azure DocumentDB.

| | Description |
| --- | --- |
| **Query plan cache commands** | Obsolete, as the service fully manages query caching. |
| **Replication commands** | Replication is fully managed as part of the platform-as-a-service (PaaS) offering. |
| **Sharding commands (except: `getShardMap`, `balancerStart`, `balancerStatus`, `balancerStop`)** | Azure DocumentDB automatically manages sharding operations. You retain control over essential operations like adding shards, rebalancing data, and retrieving shard maps. |
| **Session commands (`$killAllSessionsByPattern`, `$killSessions`)** | Most session commands are supported. However, a few are restricted due to potential security and stability risks. These commands could allow unauthorized users to terminate active sessions or perform denial-of-service (DoS) attacks. |
| **Administration commands** | As a PaaS service, Azure DocumentDB handles database administration, making these commands unnecessary. |
| **Diagnostic & Auditing commands** | Azure DocumentDB integrates with Azure Log Analytics to provide unified diagnostics and auditing across Azure services. This integration offers deep insights into performance and health without extra configuration or external tools. |
| **Monitoring commands** | Azure DocumentDB is fully integrated with Azure Monitor, making it easy to track server utilization metrics like CPU, memory, storage, IOPS, etc. This seamless integration across Azure services ensures a scalable and unified monitoring solution, providing real-time insights into your system's performance without the need for external monitoring tools. |

## Features

This table outlines the compatibility of collection features in Azure DocumentDB.

| | Description |
| --- | --- |
| **Time series collections** | Not prioritized due to weak customer demand. |
| **Capped collections** | Not prioritized due to weak customer demand. |
| **Clustered collections** | Not prioritized due to weak customer demand. |

## Related content

- [MongoDB Query Language (MQL) compatibility](compatibility-query-language.md)
- [MongoDB Query Language (MQL) commands](commands/index.md)
- [MongoDB Query Language (MQL) operators](operators/index.md)
