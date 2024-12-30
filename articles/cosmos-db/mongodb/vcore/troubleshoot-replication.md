---
title: Troubleshoot common issues in Azure Cosmos DB for MongoDB Azure Cosmos DB for MongoDB vCore cross-region replication
description: This doc discusses the ways to troubleshoot common issues encountered in Azure Cosmos DB for MongoDB Azure Cosmos DB for MongoDB vCore cross-region replication.
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: troubleshooting
ms.date: 12/22/2024
author: niklarin
ms.author: nlarin
---

# Troubleshooting guide: Cross-region replication in Azure Cosmos DB for MongoDB vCore
[!INCLUDE[MongoDB Azure Cosmos DB for MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-Azure Cosmos DB for MongoDB vCore.md)]

This guide is designed to help you troubleshoot common issues when using [cross-region replication](./cross-region-replication.md) with Azure Cosmos DB for MongoDB vCore. It offers practical solutions for connectivity problems and optimization challenges to improve your experience.

## Common issues and solutions
### My data doesn't seem to replicate to another region.
Ensure your vCore cluster has a cross-region replica created. A replica cluster can be created during initial cluster provisioning or added later. You can [verify the existence of a replica on the 'Overview' page](./how-to-cluster-replica.md#check-cluster-replication-role-and-replication-region) or [create a new one on the 'Global distribution' page](./how-to-cluster-replica.md#enable-cross-region-replication) of your vCore cluster in the Azure portal.

### I can't find connection string for replica cluster.
The replica cluster is a full replica of the primary cluster with writes disabled. It is represented as a separate vCore cluster resource in Azure and has its own connection string.

To locate the replica cluster:

- Open the properties page of the primary vCore cluster in the Azure portal.
- Navigate to the 'Global distribution' page and click on the hyperlinked name of the replica cluster.
- This will open the replica cluster’s properties. [Navigate to the 'Connection strings' page](./how-to-cluster-replica.md#use-connection-strings) to copy the connection string.

Q: I can't connect to replica cluster.
A: Make sure that you enabled public or private access on replica cluster. When replica cluster is created in another region, network settings from its primary Azure Cosmos DB for MongoDB vCore cluster are not replicated. You need to add firewall rules to enable public access or create private endpoints to enable private access to replica cluster.

Q: How can I track utilization of various resources such as memory or IOPS on my replica cluster?
A: As your replica cluster is a full replica of its primary cluster, it has its own set of metrics to monitor resource consumption. Open replica cluster properties in Azure portal and select 'Metrics' page to access replica cluster metrics.

Q: How can I open replica cluster in another region for writes?
A: You can promote your replica cluster to become a read-write one at any time. Promoting replica cluster in region B sets its ex-primary cluster in region A to read-only mode and makes ex-primary cluster a replica cluster for the promoted replica. 
You can initiate promotion from the replica cluster properties in Azure portal. Select 'Promote' on the 'Global distribution' page in replica cluster's properties and confirm promotion.
During promotion global read-write string is updated to point to the promoted replica once it is open for write operations.

## Next steps
If you've completed all the troubleshooting steps and haven't been able to discover a solution for your issue, open a [support request](https://azure.microsoft.com/support/create-ticket/).