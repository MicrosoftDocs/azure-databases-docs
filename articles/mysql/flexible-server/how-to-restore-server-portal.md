---
title: Restore From Backup
description: This article describes how to perform restore operations in Azure Database for MySQL flexible server through the Azure portal.
author: VandhanaMehta  
ms.author: vamehta  
ms.reviewer: maghan
ms.date: 05/06/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ms.custom: sfi-image-nochange
---

# Point-in-time restore in Azure Database for MySQL with the Azure portal

This article provides step-by-step procedure to perform point-in-time recoveries in Azure Database for MySQL - Flexible Server using backups.

## Prerequisites

To complete this how-to guide, you need:

- An Azure Database for MySQL flexible server instance.

## Restore to the latest restore point

Follow these steps to restore your Azure Database for MySQL - Flexible Server instance using an earliest existing backup.

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for MySQL - Flexible Server instance that you want to restore the backup from.

1. Select **Overview** from the left panel.

1. From the overview page, select **Restore**.

1. The restore page appears with an option to choose between **Latest restore point** and Custom restore point.

1. Select **Latest restore point**.

1. Enter a new server name in the **Restore to new server** field.

    :::image type="content" source="media/how-to-restore-server-portal/point-in-time-restore-latest.png" alt-text="Screenshot of earliest restore time." lightbox="media/how-to-restore-server-portal/point-in-time-restore-latest.png":::

1. Select **OK**.

1. A notification appears that the restore operation is initiated.

## Restore to a fastest restore point

Follow these steps to restore your Azure Database for MySQL - Flexible Server instance using an existing full backup as the fastest restore point.

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for MySQL - Flexible Server instance that you want to restore the backup from.

1. Select **Overview** from the left panel.

1. From the overview page, select **Restore**.

1. View the restore page with an option to choose between **Latest restore point**, **Custom restore point**, and **Fastest Restore Point**.

1. Select **Select fastest restore point (Restore using full backup)**.

1. Select the desired full backup from the **Fastest Restore Point (UTC)** dropdown list.

    :::image type="content" source="media/how-to-restore-server-portal/fastest-restore-point.png" alt-text="Screenshot of Fastest Restore Point." lightbox="media/how-to-restore-server-portal/fastest-restore-point.png":::

1. Enter a new server name in the **Restore to new server** field.

1. Select **Review + Create**.

1. After selecting **Create**, view a notification that the restore operation has been initiated.

## Restore from a full backup through the Backup and Restore page

Follow these steps to restore your Azure Database for MySQL - Flexible Server instance using an existing full backup.

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for MySQL - Flexible Server instance that you want to restore the backup from.

1. Select **Backup and Restore** from the left panel.

1. View the Available Backups page with the option to restore from available full automated backups and on-demand backups taken for the server within the retention period.

1. Select the desired full backup from the list by selecting on corresponding **Restore** action.

    :::image type="content" source="media/how-to-restore-server-portal/view-available-backups.png" alt-text="Screenshot of view Available Backups." lightbox="media/how-to-restore-server-portal/view-available-backups.png":::

1. View the Restore page with the Fastest Restore Point option selected by default and the desired full backup timestamp selected on the View Available backups page.

1. Enter a new server name in the **Restore to new server** field.

1. Select **Review + Create**.

1. After selecting **Create**, view a notification that the restore operation has been initiated.

## Geo restores to latest restore point

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for MySQL - Flexible Server instance that you want to restore the backup from.

1. Select **Overview** from the left panel.

1. From the overview page, select **Restore**.

1. The restore page appears with an option to choose **Geo-redundant restore**. If you configured your server for geographically redundant backups, you can restore the server to the corresponding Azure paired region and enable the geo-redundant restore option. The geo-redundant restore option restores the server to the latest UTC Now timestamp. After you select **Geo-redundant restore**, you can't select the point-in-time restore options.

   :::image type="content" source="media/how-to-restore-server-portal/geo-restore-flex.png" alt-text="Screenshot of Geo-restore option." lightbox="media/how-to-restore-server-portal/geo-restore-flex.png":::

   :::image type="content" source="media/how-to-restore-server-portal/geo-restore-enabled-flex.png" alt-text="Screenshot of enabling Geo-Restore." lightbox="media/how-to-restore-server-portal/geo-restore-enabled-flex.png":::

    :::image type="content" source="media/how-to-restore-server-portal/geo-restore-flex-location-dropdown.png" alt-text="Screenshot of location dropdown." lightbox="media/how-to-restore-server-portal/geo-restore-flex-location-dropdown.png":::

1. Enter a new server name in the **Name** field in the Server details section.

1. When the primary region is down, you can't create geo-redundant servers in the respective geo-paired region because storage can't be provisioned in the primary region. You must wait for the primary region to be up to provision geo-redundant servers in the geo-paired region. When the primary region is down, you can still geo-restore the source server to the geo-paired region by disabling the geo-redundancy option in the **Compute + Storage Configure Server** settings in the restore portal experience and restore as a locally redundant server to ensure business continuity.

    :::image type="content" source="media/how-to-restore-server-portal/geo-restore-region-down-1.png" alt-text="Screenshot of Compute + Storage window." lightbox="media/how-to-restore-server-portal/geo-restore-region-down-1.png":::

   :::image type="content" source="media/how-to-restore-server-portal/geo-restore-region-down-2.png" alt-text="Screenshot of Disabling Geo-Redundancy." lightbox="media/how-to-restore-server-portal/geo-restore-region-down-2.png":::

   :::image type="content" source="media/how-to-restore-server-portal/geo-restore-region-down-3.png" alt-text="Screenshot of Restoring as Locally redundant server." lightbox="media/how-to-restore-server-portal/geo-restore-region-down-3.png":::

1. Select **Review + Create** to review your selections.

1. A notification appears that the restore operation has been initiated. This operation might take a few minutes.

    The new server created by geo restore has the same server admin sign-in name and password that was valid for the existing server at the time the restore was initiated. You can change the password from the new server's **Overview** page. Additionally, during a restore, you can configure **Networking** settings such as virtual network settings and firewall rules as described in the following section.

## Use restore to move a server from Public access to Private access

Follow these steps to restore your Azure Database for MySQL - Flexible Server instance using an earliest existing backup.

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for MySQL - Flexible Server instance that you want to restore the backup from.

1. From the overview page, select **Restore**.

1. The Restore page appears with an option to choose between geo restore or point-in-time restore options.

1. Choose either **Geo restore** or a **Point-in-time restore** option.

1. Enter a new server name in the **Restore to new server** field.

    :::image type="content" source="media/how-to-restore-server-portal/point-in-time-restore-private-dns-zone.png" alt-text="Screenshot of view overview." lightbox="media/how-to-restore-server-portal/point-in-time-restore-private-dns-zone.png":::

1. Go to the **Networking** tab to configure networking settings.

1. In the **Connectivity method** section, select **Private access (VNet Integration)**. In the **Virtual Network** section, you can either select an existing *virtual network* and *Subnet* that is delegated to *Microsoft.DBforMySQL/flexibleServers* or create a new one by selecting the *create virtual network* link.
    > [!NOTE]  
    > Only virtual networks and subnets in the same region and subscription appear in the dropdown list. </br>
    > The chosen subnet is delegated to *Microsoft.DBforMySQL/flexibleServers*. It means that only Azure Database for MySQL - Flexible Server instances can use that subnet.</br>

1. Create a new or select an existing **Private DNS Zone**.
    > [!NOTE]  
    > Private DNS zone names must end with `mysql.database.azure.com`. </br>
    > If you don't see the option to create a new private dns zone, enter the server name on the **Basics** tab.</br>
    > After you deploy the Azure Database for MySQL - Flexible Server instance to a virtual network and subnet, you can't move it to Public access (allowed IP addresses).</br>

1. Select **Review + create** to review your Azure Database for MySQL - Flexible Server configuration.
1. Select **Create** to provision the server. Provisioning can take a few minutes.

1. A notification appears that the restore operation is initiated.

## Autoscale IOPS for faster restore

You can enable autoscaling of IOPS for both the source and target servers during restore operations. You can only select this option if the source server doesn't already have autoscaling of IOPS enabled. Temporarily boosting IOPS helps speed up the restore process by meeting its increased performance demands. When provisioning is complete, you can disable autoscaling if it's no longer needed. In the restore workflow, you see a checkbox option labeled **Fast Restore**. Select this option to use autoscaling of IOPS for a faster and more reliable restore operation.

:::image type="content" source="media/how-to-restore-server-portal/fast-restore.png" alt-text="Screenshot of autoscale iops for restore." lightbox="media/how-to-restore-server-portal/fast-restore.png":::

## Perform post-restore tasks

After the restore completes, perform the following tasks to get your users and applications back up and running:

- If the new server replaces the original server, redirect clients and client applications to the new server.
- Make sure users can connect by setting up appropriate virtual network rules. These rules aren't copied from the original server.
- Make sure appropriate logins and database level permissions are in place.
- Configure alerts as appropriate for the newly restored server.

## Common errors

- Restore to same server name isn't supported. Use a different name when you start the restore process, otherwise restore operations fail. 

- Ensure server isn't in "Inaccessible" state during restore. Restore isn't successful for such servers.

### Next step

> [!div class="nextstepaction"]
> [business continuity](concepts-business-continuity.md)
