---
title: Compatibility and feature support
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn about the compatibility and feature support of Azure Cosmos DB for MongoDB vCore, including supported commands and features.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 10/30/2025
---

# Compatibility and feature support in Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Azure Cosmos DB for MongoDB vCore fully implements the MongoDB wire protocol, allowing you to run nearly all MongoDB workloads without any application changes. This native Azure service offers optimized performance, lower total cost of ownership (TCO), and built-in AI capabilities, empowering modern, data-driven applications with ease.

The table below outlines MongoDB commands that are unsupported or limited in vCore based Azure Cosmos DB for MongoDB. As a fully managed PaaS solution, Cosmos DB abstracts or restricts certain administrative operations to ensure enhanced reliability, security, and performance - so you can focus on building, not managing infrastructure.

### Aggregation pipeline stages and aggregators

<table>
<tr><td><b>Command</b></td><td><b>Reason</b></td></tr>

<tr><td>$planCacheStats</td><td rowspan="1">Not applicable, as the query plan cache is automatically managed by the service.</td></tr>
<tr><td>$listSearchIndexes</td><td rowspan="3">Not prioritized due to weak customer demand.</td></tr>
<tr><td>$listSampledQueries</td></tr>
<tr><td>$shardedDataDistribution</td></tr>

</table>


### Database commands

<table>
<tr><td><b>Command Type</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="1">Query plan cache commands</td><td rowspan="1">Obsolete, query caching is fully managed by the service.</td></tr>

<tr><td rowspan="1">Replication commands</td><td rowspan="1">Replication is fully managed as part of the platform-as-a-service (PaaS) offering.</td></tr>

<tr><td rowspan="1">Sharding commands (except: getShardMap, balancerStart, balancerStatus, balancerStop)</td><td rowspan="1">Sharding operations are managed automatically by Azure Cosmos DB. You retain control over essential operations like adding shards, rebalancing data, and retrieving shard maps.</td></tr>

<tr><td rowspan="1">Session commands ($killAllSessionsByPattern, $killSessions) </td><td rowspan="1">Most session commands are supported. However, a few are restricted due to potential security and stability risks. These commands could allow unauthorized users to terminate active sessions or perform denial-of-service (DoS) attacks.</td></tr>

<tr><td rowspan="1">Administration commands</td><td rowspan="1">All administrative operations are fully managed by the Azure.</td></tr>

<tr><td rowspan="1">Diagnostic & Auditing commands</td><td>vCore based Azure Cosmos DB for MongoDB integrates with Azure Log Analytics to provide unified diagnostics and auditing across Azure services. This integration offers deep insights into performance and health without additional configuration or third-party tools.
</td></tr>

<tr><td rowspan="1">Monitoring commands</td><td rowspan="1">Azure Cosmos DB is fully integrated with Azure Monitor, making it easy to track server utilization metrics like CPU, memory, storage, IOPS etc. This seamless integration across Azure services ensures a scalable and unified monitoring solution, providing real-time insights into your system's performance without the need for external monitoring tools.
</td></tr>


</table>


### Features

<table>
<tr><td><b>Feature</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="1">Time series collections</td><td rowspan="3">Not prioritized due to weak customer demand.</td></tr>

<tr><td>Capped collections</td></tr>
<tr><td>Clustered collections</td></tr>

</table>


## Next steps

> [!div class="nextstepaction"]
> [Feature Compatibility with MongoDB vCore](compatibility.md)



