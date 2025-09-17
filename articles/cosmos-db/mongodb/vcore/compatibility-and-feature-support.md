---
title: Compatibility and feature support
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Offers an overview of the current compatibility status of Mongo vCore.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: product-comparison
ms.date: 04/09/2024
---

# Compatibility and feature support

[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Azure Cosmos DB for MongoDB vCore implements the MongoDB wire protocol, supporting nearly all MongoDB workloads with no application changes, giving you better TCO, superior performance, and next-gen AI features in a native Azure service.

The following table lists commands not supported/restricted by the database. As a Platform as a service (PaaS), Azure Cosmos DB subsumes or restricts the functionality of these commands to ensure cluster stability, security and performance, rendering them unnecessary.


### Aggregation pipeline stages and aggregators

<table>
<tr><td><b>Command</b></td><td><b>Reason</b></td></tr>

<tr><td>$planCacheStats</td><td rowspan="1">Not applicable, as the query plan cache is automatically managed by the service.</td></tr>

<tr><td>$accumulator</td><td rowspan="3">These commands require a JavaScript engine to be hosted on the database server, enabling users to run arbitrary commands. This can pose significant security risks, including the potential for injection attacks or execution of malicious code. Due to the associated security risks and low demand from customers, these commands are currently not supported. </td></tr>
<tr><td>$function</td></tr>
<tr><td>$where</td></tr>

<tr><td>$listSearchIndexes</td><td rowspan="3">It's not prioritized at this time due to low demand.</td></tr>
<tr><td>$listSampledQueries</td></tr>
<tr><td>$shardedDataDistribution</td></tr>

</table>


### Database commands

<table>
<tr><td><b>Command Type</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="1">Query plan cache commands</td><td rowspan="1">Obsolete, as the query plan cache is automatically managed by the service.</td></tr>

<tr><td rowspan="1">User/Role management commands</td><td rowspan="1">As a native Azure service, user and role management are integrated in the Azure ecosystem across services, eliminating the need for these database commands from the community version.</td></tr>

<tr><td rowspan="1">Replication commands</td><td rowspan="1">Obsolete, as a Platform as a service (PaaS) replication is fully managed by the service.</td></tr>

<tr><td rowspan="1">Sharding commands (except: getShardMap, balancerStart, balancerStatus, balancerStop)</td><td rowspan="1">We manage sharding for you, so you can focus on more critical tasks. However, you still have control over adding new shards, rebalancing shards, and retrieving a shard map whenever you need it.</td></tr>

<tr><td rowspan="1">Session commands ($killAllSessionsByPattern, $killSessions) </td><td rowspan="1">Most session commands are supported, but a couple of them have been excluded due to low demand and inherent security risks. These commands could allow unauthorized users to terminate active sessions, risking service disruptions. Furthermore, they could be exploited to target specific users or usage patterns, potentially impacting normal operations. Without proper security measures, these commands could also create vulnerabilities by enabling the termination of multiple sessions simultaneously, increasing the likelihood of denial of service (DoS) attacks.</td></tr>

<tr><td rowspan="1">Administration commands</td><td rowspan="1">As a PaaS service, Azure Cosmos DB handles database administration, making these commands unnecessary.</td></tr>

<tr><td rowspan="1">Diagnostic commands</td><td rowspan="2">Azure Cosmos DB is seamlessly integrated with Azure Log Analytics, offering a unified experience across Azure services. This enables in-depth analysis of server logs, giving you valuable insights into the performance and health of your database. With Azure’s built-in tools, you gain a powerful and scalable diagnostic solution, eliminating the need for extra configurations or third-party tools.
</td></tr>

<tr><td>Auditing commands</td></tr>

<tr><td rowspan="1">Monitoring commands</td><td rowspan="1">Azure Cosmos DB is fully integrated with Azure Monitor, making it easy to track server utilization metrics like CPU, memory, storage, IOPS etc. This seamless integration across Azure services ensures a scalable and unified monitoring solution, providing real-time insights into your system's performance without the need for external monitoring tools.
</td></tr>


</table>


### Features

<table>
<tr><td><b>Feature</b></td><td><b>Reason</b></td></tr>

<tr><td rowspan="1">Time series collections</td><td rowspan="3">Not prioritized yet due to weak demand—support will be added in the future.</td></tr>

<tr><td>Capped collections</td></tr>
<tr><td>Clustered collections</td></tr>

</table>


## Next steps

> [!div class="nextstepaction"]
> [Feature Compatibility with MongoDB vCore](compatibility.md)



