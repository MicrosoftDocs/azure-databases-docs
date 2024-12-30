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

### I can't connect to replica cluster.
Ensure that [public or private access](./security.md#network-security-options) is enabled for the replica cluster. When a replica cluster is created in another region, its network settings are not automatically replicated from the primary Azure Cosmos DB for MongoDB vCore cluster.  

To enable access:  
- Add firewall rules to allow public access.  
- Alternatively, create private endpoints to enable private access to the replica cluster.  

### How can I track utilization of various resources such as memory or IOPS on my replica cluster?
Since the replica cluster is a full replica of the primary Azure Cosmos DB for MongoDB vCore cluster, it has its own metrics for monitoring resource consumption.  

To view metrics:  
1. Open the properties page of the replica cluster in the Azure portal.  
1. Navigate to the **Metrics** page to access and review the resource consumption details.  

See more detailed guidance on using metrics with Azure Cosmos DB for MongoDB vCore on [this page](./monitor-metrics.md).

### How can I open replica cluster in another region for writes?
You can promote the replica cluster to become a read-write cluster at any time. When you promote the replica cluster in region B, the ex-primary cluster in region A is set to read-only mode, effectively making it the replica cluster for the newly promoted primary cluster.  

To promote the replica cluster:  
1. Open the properties page of the replica cluster in the Azure portal.  
1. Navigate to the **Global distribution** page.  
1. Select **Promote** and confirm the promotion.  

During the promotion process, the [global read-write connection string](./how-to-cluster-replica.md#use-connection-strings) is updated to point to the newly promoted replica cluster once it is open for write operations.

### Replica cluster is not needed anymore. How can I disable replication and delete replica cluster?
You can delete replica cluster at any time. Deletion of the replica cluster doesn't impact the primary cluster or data stored or written to the primary cluster. If you need to delete both replica and primary clusters, you need to delete replica cluster first.

To delete a replica cluster:
1. Open the properties page of the replica cluster in the Azure portal.
1. Select **Delete** in the toolbar on the **Overview** page. 
1. Read the warning and confirm deletion.

## Next steps
If you've completed all the troubleshooting steps and haven't been able to discover a solution for your issue, open a [support request](https://azure.microsoft.com/support/create-ticket/).