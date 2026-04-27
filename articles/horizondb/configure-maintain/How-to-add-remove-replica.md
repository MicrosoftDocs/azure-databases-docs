---
title: How to add or remove replica
description: This article describes the steps to add or remove a HorizonDB replica.
author: DDL-PM
ms.author: ludingding
ms.reviewer: maghan
ms.date: 04/27/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: how-to
---

# Add or remove a replica

An Azure HorizonDB cluster can have up to 15 replicas. Because a replica of Azure HorizonDB is a readable standby replica, adding or removing a replica can impact the high availability behavior of a HorizonDB cluster. This article provides step-by-step instructions to add or remove a replica  to or from a HorizonDB cluster.

## Prerequisites

Before you begin, make sure you have an existing HorizonDB. If you don't, create an Azure HorizonDB cluster. 

## Add a replica

### [Portal](#tab/portal-add-replica)

If your HorizonDB cluster is configured with high availability, your HorizonDB cluster already has at least 1 replica. You can add a replica:

	1. Select your HorizonDB in the Azure portal. 
	2. Select **compute**, located in the **Settings** section. 
	3. Under **High availability replicas**, click **change** next to the **Readable high availability replicas**. It takes you to the **Replicas** 
	4. Alternatively, you can skip step 2 and step 3 above by directly selecting **Replicas** located in the **Settings** section
	5. Select **Add new replicas**, then select the number of replicas you want to add from the dropdown list. A HorizonDB cluster can have maximum 15 replicas
	6. Select **Save**

If your HorizonDB cluster is not configured with high availability, your HorizonDB cluster only has the primary. 

## Remove a replica

### [Portal](#tab/portal-remove-replica)

If your HorizonDB cluster has more than 1 replicas. You can remove a replica:

	1. Select your HorizonDB in the Azure portal. 
	2. Select **Replicas** located in the **Settings** section
	3. Select the replica you want to remove by clicking the **…** next to the replica name then click **Remove replica**. 
	4. Removing replica will reduce the read capacity of this HorizonDB cluster. Click **Remove** to confirm.
	
If your HorizonDB is created with zone redundant HA and the replica you want to remove is the last replica that is in the different zone than the primary, removing this replica will violate the zone redundant HA and is not allowed. To remove this replica, you need to change your HA preference to allow same zone or disable HA.

If your HorizonDB cluster has only 1 replica. Removing this replica results to HA being disabled. Click **Remove** to confirm.

