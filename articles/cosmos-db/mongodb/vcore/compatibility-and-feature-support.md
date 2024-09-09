---
title: Compatibility and feature support
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Provide information on the category and list of commands which are currently not supported on Mongo vCore.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 04/09/2024
---

# Compatibility and feature support

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Azure Cosmos DB for MongoDB vCore implements the MongoDB wire protocol, supporting nearly all MongoDB workloads with no application changes, giving you better TCO, superior performance, and next-gen AI features in a native Azure service.

The following table lists commands not supported/restricted by the database. As a PaaS service, Azure Cosmos DB subsumes or restricts the functionality of these commands to ensure cluster stability, security and performance, rendering them unnecessary.


## Aggregation Pipeline Stages & Aggregators

<table>
<tr><td><b>Category</b></td><td><b>Command</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="7">Aggregation Pipeline Stages</td><td>$listLocalSessions</td><td rowspan="5">Restricted to Azure Portal/CLI.</td></tr>
<tr><td>$listSessions</td></tr>
<tr><td>$listSearchIndexes</td></tr>
<tr><td>$listSampledQueries</td></tr>
<tr><td>$$searchMeta</td></tr>
<tr><td>$planCacheStats</td><td rowspan="2">Privileged operations. Will be managed by the service.</td></tr>
<tr><td>$shardedDataDistribution</td></tr>

<tr><td rowspan="1">Accumulators</td><td>$accumulator</td><td rowspan="1">Not supported. Require JS engine to be hosted on DB and allows CX to run arbitrary JS commands.</td></tr>

<tr><td rowspan="1">Custom Aggregation Expression Operators</td><td>$function</td><td rowspan="1">Not supported. Require JS engine to be hosted on DB and allows CX to run arbitrary JS commands.</td></tr>

<tr><td rowspan="1">Query & Projection Operators</td><td>$where</td><td rowspan="1">Not supported. Require JS engine to be hosted on DB and allows CX to run arbitrary JS commands.</td></tr>

</table>


## Database Commands

<table>
<tr><td><b>Category</b></td><td><b>Command</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="1">Query Plan Cache Commands</td><td>All</td><td rowspan="1">These commands will be managed by service.</td></tr>

<tr><td rowspan="1">User/Role Management Commands</td><td>All</td><td rowspan="1">Restricted via. Azure Portal/CLI. (AAD/RBAC)</td></tr>

<tr><td rowspan="1">Replication Commands</td><td>All</td><td rowspan="1">Replication will be managed by the service.</td></tr>

<tr><td rowspan="1">Sharding Commands</td><td>All (Except $enableSharding, $isdbgrid, $reshardCollection and $shardCollection) </td><td rowspan="1">Sharding will be managed by the service.</td></tr>

<tr><td rowspan="2">Session Commands</td><td>$killAllSessionsByPattern</td><td rowspan="2">Restricted via. Azure Portal/CLI.</td></tr>
<tr><td>$killSessions</td></tr>

<tr><td rowspan="1">Administration Commands</td><td>All</td><td rowspan="1">High privilege operations. Will not be supported due to security concerns.</td></tr>

<tr><td rowspan="1">Diagnostic Commands</td><td>All</td><td rowspan="1">Offered using Azure Diagnostic Logging.</td></tr>

<tr><td rowspan="1">Free Monitoring Commands</td><td>All</td><td rowspan="1">Offered using Azure Monitor.</td></tr>

<tr><td rowspan="1">Auditing Commands</td><td>All</td><td rowspan="1">Offered using Azure Diagnostic Logging.</td></tr>

</table>



## Next steps

> [!div class="nextstepaction"]
> [Feature Compatibility with MongoDB vCore](compatibility.md)



