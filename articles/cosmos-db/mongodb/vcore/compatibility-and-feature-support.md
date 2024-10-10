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

The following table lists commands not supported/restricted by the database. As a Platform as a service (PaaS), Azure Cosmos DB subsumes or restricts the functionality of these commands to ensure cluster stability, security and performance, rendering them unnecessary.


## Aggregation Pipeline Stages & Aggregators

<table>
<tr><td><b>Command</b></td><td><b>Reason</b></td></tr>

<tr><td>$planCacheStats</td><td rowspan="1">Obsolete on MongoDB vCore, as the query plan cache is automatically managed by the service.</td></tr>


<tr><td>$accumulator</td><td rowspan="3">These commands require a JavaScript engine to be hosted on the database server, enabling users to run arbitrary commands. This can pose significant security risks, including the potential for injection attacks or execution of malicious code. Due to the associated security risks and low demand from customers, these commands are currently not supported. </td></tr>
<tr><td>$function</td></tr>
<tr><td>$where</td></tr>

<tr><td>$searchMeta</td><td rowspan="4">Not prioritized yet due to weak demand—support will be added in the future.</td></tr>
<tr><td>$listSearchIndexes</td></tr>
<tr><td>$listSampledQueries</td></tr>
<tr><td>$shardedDataDistribution</td></tr>

</table>


## Database Commands

<table>
<tr><td><b>Command Type</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="1">Query plan cache commands</td><td rowspan="1">Obsolete on MongoDB vCore, as the query plan cache is automatically managed by the service.</td></tr>

<tr><td rowspan="1">User/Role management commands</td><td rowspan="1">As a native Azure service, user and role management are integrated in the Azure ecosystem across services, eliminating the need for these database commands from the community version.</td></tr>

<tr><td rowspan="1">Replication commands</td><td rowspan="1">Obsolete on MongoDB vCore, as replication is fully managed by the service.</td></tr>

<tr><td rowspan="1">Sharding commands (except: getShardMap, balancerStart, balancerStatus, balancerStop)</td><td rowspan="1">With MongoDB vCore, we manage sharding for you, so you can focus on more critical tasks. However, you still have control over adding new shards, rebalancing shards, and retrieving a shard map whenever you need it.</td></tr>

<tr><td rowspan="1">Session commands ($killAllSessionsByPattern, $killSessions) </td><td rowspan="1">While most session commands are supported, a few have been excluded due to low demand and potential security risks.</td></tr>

<tr><td rowspan="1">Administration commands</td><td rowspan="1">As a PaaS service, MongoDB vCore fully manages all high privilege operations on your behalf.</td></tr>

<tr><td rowspan="1">Diagnostic commands</td><td rowspan="2">MongoDB vCore comes pre-loaded with <a href="https://learn.microsoft.com/azure/cosmos-db/mongodb/vcore/how-to-monitor-diagnostics-logs" target="_blank">Azure Diagnostic Logging</a>. Simply enable it for your cluster, and you'll be all set to explore server logs using Kusto Query Language (KQL).</td></tr>

<tr><td>Auditing commands</td></tr>

<tr><td rowspan="1">Monitoring commands</td><td rowspan="1">Monitoring server utilization metrics such as CPU, memory, storage, IOPS etc. is now easy with the integrated <a href="https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/monitor-metrics" target="_blank">Azure Monitor</a>, all at no additional cost.</td></tr>


</table>



## Next steps

> [!div class="nextstepaction"]
> [Feature Compatibility with MongoDB vCore](compatibility.md)



