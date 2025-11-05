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

In a fully distributed environment, it's possible that that every node participates in the coordinator node's operations. In order to access data across the cluster, an additional underlying connection is required between the coordinator and each node in the cluster.  To compensate for these inter-node connections, the coordinator's maximum client connection parameter and maximum shared pool size parameter are adjusted to align to the number of available nodes.

## citus.max_client_connections

The citus.max_client_connections parameter limits how many client sessions the coordinator will allow to proceed concurrently through Citus’ distributed executor. This is important because the coordinator handles query planning and distribution across worker nodes.  The goal is to protect worker nodes from being overwhelmed by fan‑out connections that each coordinator session can create. It doesn’t replace Postgres’ max_connections; it sits “in front of it.” 

As an exmaple, when using a 10-node cluster, the default value for citus.max_client_connections is set to 250 connections (250 x 10 = 2500). 

## citus.max_shared_pool_size

The citus.max_client_connections parameter limits the total number of outbound connections the coordinator may open to each worker node across all backends, i.e., it throttles the fan‑out. It is recommended to keep max_shared_pool_size less than worker max_connections (to leave headroom). 

> [!NOTE]
> These parameters only apply to the coordinator node.

   