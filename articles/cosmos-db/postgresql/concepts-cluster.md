---
title: Cluster - Azure Cosmos DB for PostgreSQL
description: What is a cluster in Azure Cosmos DB for PostgreSQL
ms.author: nlarin
author: niklarin
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.topic: concept-article
ms.date: 11/28/2023
appliesto:
  - ✅ PostgreSQL
---

# Clusters in Azure Cosmos DB for PostgreSQL

[!INCLUDE [Note - Recommended services](includes/note-recommended-services.md)]

## Nodes

Azure Cosmos DB for PostgreSQL allows PostgreSQL servers (called nodes) to coordinate with one another in a "cluster."
The cluster's nodes collectively hold more data and use more CPU cores than would be possible on a single server. The architecture also allows the database to scale by adding more nodes to the cluster.

To learn more about the types of nodes, see [nodes and tables](concepts-nodes.md).

### Node status

Azure Cosmos DB for PostgreSQL displays the status of nodes in a cluster on the Overview page in the Azure portal. Each node can have one of these status values:

* **Provisioning**: Initial node provisioning, either as a part of its cluster provisioning, or when a worker node is added.
* **Available**: Node is in a healthy state.
* **Need attention**: An issue is detected on the node. The node is attempting to self-heal. If self-healing fails, an issue gets put in the queue for our engineers to investigate.
* **Dropping**: Cluster deletion started.
* **Disabled**: The cluster's Azure subscription turned into Disabled states. For more information about subscription states, see [this page](/azure/cost-management-billing/manage/subscription-states).

### Node availability zone

Azure Cosmos DB for PostgreSQL displays the [availability zone](./concepts-availability-zones.md) of each node in a cluster on the Overview page in the Azure portal. The **Availability zone** column contains either the name of the zone, or `--` if the node isn't assigned to a zone. (Only [certain regions](./resources-regions.md) support availability zones.)

Azure Cosmos DB for PostgreSQL allows you to set a preferred availability zone for cluster. Usually the reason for it is to put cluster nodes in the same availability zone where the application and the rest of the application stack components are.

If [high availability](./concepts-high-availability.md) is enabled for the cluster, and a node fails over to a standby, you may see its availability zone differs from the other nodes. In this case, the nodes will be moved back into the same availability zone together during the next [maintenance event](./concepts-maintenance.md).

## Next steps

* Learn to [provision a cluster](quickstart-create-portal.md)
* Learn about [high availability fundamentals](./concepts-high-availability.md)
