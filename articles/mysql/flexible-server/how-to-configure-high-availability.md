---
title: Manage Zone Redundant High Availability - Azure portal
description: This article describes how to enable or disable zone redundant high availability in Azure Database for MySQL - Flexible Server through the Azure portal.
author: aditivgupta
ms.author: adig
ms.reviewer: maghan
ms.date: 08/15/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom:
  - references_regions
---

# Manage zone redundant high availability in Azure Database for MySQL with the Azure portal

This article describes how to turn on or off the zone redundant high availability configuration in Azure Database for MySQL.

The high availability feature provisions physically separate primary and standby replicas in different zones. For more information, see the [high availability concepts documentation](concepts-high-availability.md).

> [!IMPORTANT]  
> You can enable zone redundant high availability only during Azure Database for MySQL Flexible Server instance creation.

This article provides guidelines to turn high availability on or off. This operation doesn't change your other settings, including virtual network configuration, firewall settings, and backup retention. Similarly, disabling high availability is an online operation that doesn't impact your application's connectivity or operations.

## Enable high availability during server creation

This section provides details specifically for HA-related fields. You can follow these steps to deploy high availability while creating your Azure Database for MySQL Flexible Server instance.

1. In the [Azure portal](https://portal.azure.com/), choose flexible Server and select **Create**. For information about how to fill in details such as **Subscription**, **Resource group**, **Server name**, **Region**, and other fields, see the how-to documentation for Azure Database for MySQL Flexible Server instance creation.

1. Select the radio button for **Zone-redundant** in the High availability option.
    
    :::image type="content" source="media/how-to-configure-high-availability\flexible-server-ha-configure.png" alt-text="Screenshot that shows how to configure high-availability." lightbox="media/how-to-configure-high-availability\flexible-server-ha-configure.png":::

1. Select **Configure server** if you want to change the default compute and storage settings.

1. If you select the high availability option, you can't choose the burstable tier. You can choose either
   **General purpose** or **Memory-Optimized** compute tiers.

   > [!IMPORTANT]  
   > We only support zone-redundant high availability for the **General purpose** and **Memory-Optimized** pricing tiers.

1. Select the **Compute size** for your choice from the dropdown list.

1. Select **Storage size** in GiB by using the sliding bar and select the **Backup retention period** between 7 days and 35 days.

## Disable high availability

Follow these steps to disable high availability for your Azure Database for MySQL Flexible Server instance that is already configured with zone redundancy.

1. In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for MySQL Flexible Server instance.

1. On the Azure Database for MySQL Flexible Server instance page, select **High Availability** from the front panel to open the high availability page.

1. Select the **zone redundant high availability** checkbox to disable the option and select **Save** to save the change.

1. When the confirmation dialog appears, confirm disabling high availability. Select **Disable HA** to disable high availability.

1. A notification states that the high availability decommissioning deployment is in progress.

## Forced failover

Follow these steps to force failover from your primary to a standby Azure Database for MySQL Flexible Server instance.

1. In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for MySQL Flexible Server instance that has the high availability feature enabled.

1. On the Azure Database for MySQL Flexible Server instance page, select **High Availability** from the front panel to open the high availability page.

1. Check the **Primary availability zone** and the **Standby availability zone**.

1. Select **Forced Failover** to initiate the manual failover procedure. A pop-up informs you of the expected failover time depending on the current workload on the primary and the recency of the last checkpoint. Read the message and select **OK**.

1. A notification states that failover is in progress. When failover to the standby server succeeds, a notification appears.

1. Check the new **Primary availability zone** and the **Standby availability zone**.

:::image type="content" source="media/how-to-configure-high-availability/how-to-forced-failover.png" alt-text="Screenshot of How to force failover." lightbox="media/how-to-configure-high-availability/how-to-forced-failover.png":::

## Related content

- [business continuity](concepts-business-continuity.md)
- [zone redundant high availability](concepts-high-availability.md)
