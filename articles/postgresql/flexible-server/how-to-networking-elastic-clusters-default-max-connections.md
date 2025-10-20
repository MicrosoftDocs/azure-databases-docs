---
title: Elastic cluster maximum client connections default behvaior
description: This article describes how the maximum number of client connections are adjusted when scaling out nodes of an Azure Database for PostgreSQL flexible server elastic cluster.
author: jaredmeade
ms.author: jaredmeade
ms.reviewer: 
ms.date: 11/17/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how the maximum client connections server parameter is adjusted when additional nodes are added to an Azure Database for PostgreSQL flexible server elastic cluster.

---

# Maximum client connections across an elastic cluster

In a fully distributed environment, it's possible that that every node participates in database operations. In order to access your clustered data, an additional underlying connection is required between each node in the cluster.  To compensate for the inter-node connections, the cluster's maximum client connection parameter is adjusted to align to the number of nodes.  For example, when using a 10-node cluster, the value for citus.max_client_connections default is set to 250 connections (250 x 10 = 2500).