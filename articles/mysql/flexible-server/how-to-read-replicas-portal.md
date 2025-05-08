---
title: Manage Read Replicas With Azure Portal
description: Learn how to set up and manage read replicas in Azure Database for MySQL - Flexible Server by using the Azure portal.
author: VandhanaMehta
ms.author: vamehta
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
---

# How to create and manage read replicas in Azure Database for MySQL - Flexible Server by using the Azure portal

In this article, you learn how to create and manage read replicas in Azure Database for MySQL Flexible Server using the Azure portal.

> [!NOTE]  
>  
> If GTID is enabled on a primary server (`gtid_mode` = ON), newly created replicas also have GTID enabled and use GTID based replication. To learn more refer to [Global transaction identifier (GTID)](concepts-read-replicas.md#global-transaction-identifier-gtid)

## Prerequisites

- An [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md) that is used as the source server.

## Create a read replica

A read replica server can be created using the following steps:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Select the existing Azure Database for MySQL Flexible Server instance that you want to use as a source. This action opens the **Overview** page.

1. Select **Replication** from the menu, under **SETTINGS**.

1. Select **Add Replica**.

   :::image type="content" source="media/how-to-read-replicas-portal/add-replica.png" alt-text="Screenshot of adding a replica" lightbox="media/how-to-read-replicas-portal/add-replica.png":::

1. Enter a name for the replica server. If your region supports Availability Zones, you can select the Availability zone of your choice.

   :::image type="content" source="media/how-to-read-replicas-portal/replica-name.png" alt-text="Screenshot of adding a replica name":::

1. Enter location based on your need to create an in-region or universal cross-region read-replica.

   :::image type="content" source="media/how-to-read-replicas-portal/select-cross-region.png" alt-text="Screenshot of selecting a cross region":::

1. You now have the capability to enable auto-scaling of IOPS for both the source and target servers during replica creation. This option is available only if the source server does not already have auto-scaling of IOPS enabled. Temporarily boosting IOPS helps accelerate the replica provisioning process. Once provisioning is complete, you may choose to disable auto-scaling if it is no longer needed. In the replica creation workflow, you see a checkbox option labeled Faster Provisioning. Select this option to leverage auto-scaling of IOPS for a faster and more reliable replica provisioning.

   :::image type="content" source="media/how-to-read-replicas-portal/faster-provisioning.png" alt-text="Screenshot of faster provisioning":::


1. Select **OK** to confirm the creation of the replica.

Once the replica server has been created, it can be viewed from the **Replication** page.

   :::image type="content" source="media/how-to-read-replicas-portal/list-replica.png" alt-text="Screenshot of a list of replicas" lightbox="media/how-to-read-replicas-portal/list-replica.png":::

> [!NOTE]  
> Read replicas are created with the same server configuration as the source. The replica server configuration can be changed after it has been created. The replica server is always created in the same resource group and the same subscription as the source server. Suppose you want to create a replica server for a different resource group or different subscription. In that case, you can [move the replica server](/azure/azure-resource-manager/management/move-resource-group-and-subscription) after creation. It is recommended that the replica server's configuration should be kept at equal or greater values than the source to ensure the replica can keep up with the source.

## Stop replication to a replica server

> [!IMPORTANT]  
> Stopping replication to a server is irreversible. Once replication has stopped between a source and replica, it cannot be undone. The replica server then becomes a standalone server and now supports read and write. This server cannot be made into a replica again.

To stop replication between a source and a replica server from the Azure portal, use the following steps:

1. In the Azure portal, select your source Azure Database for MySQL Flexible Server instance.

1. Select **Replication** from the menu, under **SETTINGS**.

1. Select the replica server you wish to stop replication.

1. Select Promote. Promote action caused replication to stop and convert the replica into an independent, standalone read-writeable server.

   :::image type="content" source="media/how-to-read-replicas-portal/promote-action.png" alt-text="Screenshot of selecting promote." lightbox="media/how-to-read-replicas-portal/promote-action.png":::

1. Confirm you want to stop replication by selecting **Promote**.

   :::image type="content" source="media/how-to-read-replicas-portal/stop-replication-confirm.png" alt-text="Screenshot of stopping replication by selecting promote." lightbox="media/how-to-read-replicas-portal/stop-replication-confirm.png":::

## Delete a replica server

To delete a read replica server from the Azure portal, use the following steps:

1. In the Azure portal, select your source Azure Database for MySQL Flexible Server instance.

1. Select **Replication** from the menu, under **SETTINGS**.

1. Select the replica server you wish to delete.

   :::image type="content" source="media/how-to-read-replicas-portal/delete-replica-select.png" alt-text="Screenshot of deleting a selected server replica." lightbox="media/how-to-read-replicas-portal/delete-replica-select.png":::

1. Select **Delete replica**

   :::image type="content" source="media/how-to-read-replicas-portal/delete-replica.png" alt-text="Screenshot of deleting a replica." lightbox="media/how-to-read-replicas-portal/delete-replica.png":::

1. Type the name of the replica and select **Delete** to confirm the deletion of the replica.

   :::image type="content" source="media/how-to-read-replicas-portal/delete-replica-confirm.png" alt-text="Screenshot confirming deletion of a replica" lightbox="media/how-to-read-replicas-portal/delete-replica-confirm.png":::

## Delete a source server

> [!IMPORTANT]  
> Deleting a source server stops replication to all replica servers and deletes the source server itself. Replica servers become standalone servers that now support both read and writes.

To delete a source server from the Azure portal, use the following steps:

1. In the Azure portal, select your source Azure Database for MySQL Flexible Server instance.

1. From the **Overview**, select **Delete**.

   :::image type="content" source="media/how-to-read-replicas-portal/delete-master-overview.png" alt-text="Screenshot of deleting the source." lightbox="media/how-to-read-replicas-portal/delete-master-overview.png":::

1. Type the name of the source server and select **Delete** to confirm the deletion of the source server.

   :::image type="content" source="media/how-to-read-replicas-portal/delete-master-confirm.png" alt-text="Screenshot of deleting the source confirmed.":::

## Monitor replication

1. In the [Azure portal](https://portal.azure.com/), select the replica Azure Database for MySQL Flexible Server instance you want to monitor.

1. Under the **Monitoring** section of the sidebar, select **Metrics**:

1. Select **Replication lag in seconds** from the dropdown list of available metrics.

   :::image type="content" source="media/how-to-read-replicas-portal/monitor-select-replication-lag.png" alt-text="Screenshot of selecting the replication lag." lightbox="media/how-to-read-replicas-portal/monitor-select-replication-lag.png":::

1. Select the time range you wish to view. The image below selects a 30-minute time range.

   :::image type="content" source="media/how-to-read-replicas-portal/monitor-replication-lag-time-range.png" alt-text="Screenshot of selecting time range." lightbox="media/how-to-read-replicas-portal/monitor-replication-lag-time-range.png":::

1. View the replication lag for the selected time range. The image below displays the last 30 minutes.

   :::image type="content" source="media/how-to-read-replicas-portal/monitor-replication-lag-time-range-thirty-mins.png" alt-text="Selecting time range 30 minutes" lightbox="media/how-to-read-replicas-portal/monitor-replication-lag-time-range-thirty-mins.png":::

## Related content

- [Read replicas](concepts-read-replicas.md)
- [Troubleshoot replication latency](../how-to-troubleshoot-replication-latency.md)
