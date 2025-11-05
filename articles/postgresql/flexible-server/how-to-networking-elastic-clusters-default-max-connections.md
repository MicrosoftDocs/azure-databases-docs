---
title: Elastic cluster maximum client connections default behvaior
description: This article describes how the maximum number of client connections are adjusted when scaling out nodes of an Azure Database for PostgreSQL flexible server elastic cluster.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how the maximum client connections server parameter is adjusted when additional nodes are added to an Azure Database for PostgreSQL flexible server elastic cluster.

---

# Maximum client connections across an elastic cluster

The default connection configuration of an elastic cluster ensures maximum connectivity for distributed queries by apportioning a subset of available connections to the cluster. To accomplish this, the cluster reserves connections on each worker node based upon the number of nodes in the cluster and the maximum connections the selected SKU size can support. The default configuration guarantees that every node can participate in distributed operations without connection limits becoming a bottleneck.  For example, if using a SKU which can support 5,000 connections, the default configuration for a two-node cluster is to allow 2,500 active client connections; the remaining 2,500 connections are reserved to allow extended connectivity to the second node for any potential distributed queries.  Similarly, a four-node cluster defaults to allowing 1,250 active client connections to ensure there's overhead for the additional connections to each connected node.

**Max Connections = 5,000**

| Node Count | Max Client Connections | Max Shared Pool |
|----------|----------|----------|
| 2 | 2,500 | 2,500 |
| 4 | 1,250 | 1,250 |
| 8 | 625 | 625 |
| 10 | 250 | 250 |

The default configuration ensures that cluster-wide operations will always have available connections to allow a connection to each node. This is suitable for use cases involving operations that include all of your data across all nodes, however, this may not be suitable for all types of work loads.  For instance, in other circumstances, your workloads may involve more targeted and/or shard-specific data operations.  In these situations, you may want to configure your cluster to allow more active client connections.  To do so, you adjust the **citus.max_client_connections** parameter.

## citus.max_client_connections

The citus.max_client_connections parameter governs how many client sessions are allowed to connect concurrently throughout the cluster's distributed environment. This is important because query planning and data distributions can potentially extend out to multiple worker nodes.  The goal is to protect worker nodes from being overwhelmed by fan‑out connections that require connections to each additional node. This parameter doesn’t replace Postgres’ max_connections; it sits “in front of it.” 

Keep in mind that while increasing the max_client_connections allows you to override the default cluster connection limits, each node is still bound by the number of active connections defined by the max_connections setting.  Increasing the number of client connections carries the potential to require additional connections to each other node in your cluster if warranted.  

> [!NOTE]
> Each workload use case is different, so make sure you are monitoring your cluster's connection characteristics closely before and after making any changes to how active cluster connections are managed.

   