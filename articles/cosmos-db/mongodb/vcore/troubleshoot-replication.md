---
title: Troubleshoot common issues in Azure Cosmos DB for MongoDB vCore cross-region replication
description: This doc discusses the ways to troubleshoot common issues encountered in Azure Cosmos DB for MongoDB vCore cross-region replication.
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: troubleshooting
ms.date: 12/22/2024
author: niklarin
ms.author: nlarin
---

# Troubleshoot common issues with cross-region replication in Azure Cosmos DB for MongoDB vCore
[!INCLUDE[MongoDB vCore](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

This guide is tailored to assist you in resolving issues you may encounter when using [cross-region replication](./cross-region-replication.md) Azure Cosmos DB for MongoDB vCore. The guide provides solutions for connectivity problems and optimization challenges offering practical insights to improve your experience.

## Common issues and solutions
Q: My data doesn't seem to replicate to another region
A: Make sure your vCore cluster has a cross-region replica created. You can create a replica cluster in another region at cluster provisioning or any time after. You can verify whether your vCore cluster has a replica or create a new one on 'Global distribution' page of your vCore cluster in the Azure portal.

Q: I can't find connection string for replica cluster.
A: REplica cluster is a full replica of its primary cluster with disalbed writes. As such it is represented as a separate resource (vCore cluster) in Azure and has its own connection string. To navigate to replica cluster, open properties of the primary vCore cluster in Azure portal, select 'Global distribution' page, select hyperlinked replica cluster name. That opens replica cluster properties in Azure portal. Navigate to 'Connection strings' page to copy replica cluster connection string. 

Q: I can't connect to replica cluster.
A: Make sure that you enabled public or private access on replica cluster. When replica cluster is created in another region, network settings from its primary vCore cluster are not replicated. You need to add firewall rules to enable public access or create private endpoints to enable private access to replica cluster.

Q: How can I track utilization of various resources such as memory or IOPS on my replica cluster?
A: As your replica cluster is a full replica of its primary cluster, it has its own set of metrics to monitor resource consumption. Open replica cluster properties in Azure portal and select 'Metrics' page to access replica cluster metrics.

Q: How can I open replica cluster in another region for writes?
A: You can promote your replica cluster to become a read-write one at any time. Promoting replica cluster in region B sets its ex-primary cluster in region A to read-only mode and makes ex-primary cluster a replica cluster for the promoted replica. 
You can initiate promotion from the replica cluser properties in Azure portal. Select 'Promote' on the 'Global distribution' page in replica cluster's properties and confirm promotion.
During promotion global read-write string is updated to point to the promoted replica once it is open for write operations.

## Next steps
If you've completed all the troubleshooting steps and haven't been able to discover a solution for your issue, open a [support request](https://azure.microsoft.com/support/create-ticket/).