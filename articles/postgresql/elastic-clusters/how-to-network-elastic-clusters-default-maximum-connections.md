---
title: Elastic Cluster Maximum Client Connections Default Behavior
description: This article describes how the maximum number of client connections are adjusted when scaling out nodes of an Azure Database for PostgreSQL flexible server elastic cluster.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
---

# Maximum client connections across an elastic cluster

The default connection configuration of an elastic cluster apportions a subset of available connections to the cluster to ensure maximum connectivity for distributed queries. To accomplish this configuration, the cluster reserves connections on each worker node based on the number of nodes in the cluster and the maximum connections the selected SKU size supports. The default configuration guarantees that every node can participate in distributed operations without connection limits becoming a bottleneck. For example, if you use a SKU that supports 5,000 connections, the default configuration for a two-node cluster allows 2,500 active client connections. The remaining 2,500 connections are reserved to allow extended connectivity to the second node for any potential distributed queries. Similarly, a four-node cluster defaults to allowing 1,250 active client connections to ensure there's overhead for the extra connections to each connected node.

**Max Connections = 5,000**

| Node Count | Max Client Connections | Max Shared Pool |
| --- | --- | --- |
| 2 | 2,500 | 2,500 |
| 4 | 1,250 | 1,250 |
| 8 | 625 | 625 |
| 10 | 250 | 250 |

The default configuration ensures that cluster-wide operations always have available connections to allow a connection to each node. This configuration is suitable for use cases involving operations that include all of your data across all nodes. However, this configuration might not be suitable for all types of workloads. For instance, in other circumstances, your workloads might involve more targeted and shard-specific data operations. In these situations, you might want to configure your cluster to allow more active client connections. To do so, you adjust the **citus.max_client_connections** parameter.

## citus.max_client_connections

The citus.max_client_connections parameter governs how many client sessions can connect concurrently throughout the cluster's distributed environment. This parameter is important because query planning and data distributions can potentially extend out to multiple worker nodes. The goal is to protect worker nodes from being overwhelmed by fan‑out connections that require connections to each extra node. This parameter doesn't replace Postgres' max_connections; it sits "in front of it."

Keep in mind that while increasing the max_client_connections allows you to override the default cluster connection limits, each node is still bound by the number of active connections defined by the max_connections setting. Increasing the number of client connections can require additional connections to each other node in your cluster if warranted.

> [!NOTE]  
> Each workload use case is different, so make sure you monitor your cluster's connection characteristics closely before and after making any changes to how active cluster connections are managed.

## Related content

- [Quickstart: Create an instance of elastic cluster in Azure Database for PostgreSQL](../elastic-clusters/quickstart-create-elastic-cluster-portal.md)
