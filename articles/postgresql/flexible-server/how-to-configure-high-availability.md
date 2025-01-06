---
title: Manage high availability
description: This article describes how to enable and disable high availability in an Azure Database for PostgreSQL flexible server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 01/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to enable and disable high availability in an Azure Database for PostgreSQL flexible server.
---

# Configure high availability in an Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article describes how you can enable or disable high availability configuration in your Azure Database for PostgreSQL flexible server in same zone, or zone redundant deployment models.

High availability feature deploys physically separate primary and standby replicas. Both replicas can be provisioned within the same availability zone or each on a different zone, depending on the deployment model you choose. For more information, see [high availability concepts](/azure/reliability/reliability-postgresql-flexible-server). You can enable high availability at creation time of your Azure Database for PostgreSQL flexible server, or you can do it after the server is created.

Enabling or disabling high availability on an Azure Database for PostgreSQL flexible server doesn't change other settings, including networking configuration, firewall settings, server parameters, or backup retention. Enabling or disabling high availability is an online operation, and doesn't affect your application connectivity and operations.

High availability with both replicas deployed in the same zone is supported and available in all regions in which Azure Database for PostgreSQL - Flexible Server is supported. However, high availability with zone redundancy is [only available in certain regions](overview.md#azure-regions).

> [!IMPORTANT]
> _Billing Model Update for Azure Database for PostgreSQL Flexible Server (v5 HA):_
In April, we implemented a billing model update for v5 SKU with High Availability (HA) enabled servers. This change aims to correctly reflect the charges, by accounting for both the primary and standby servers. Before this change, we were incorrectly charging customers for the primary server only. Customers using v5 SKU with HA enabled servers will now see billing quantities multiplied by 2. This update doesn't impact v4 and v3 SKUs.

## Enable high availability for existing servers

### [Portal](#tab/portal-enable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **High availability**.

    :::image type="content" source="./media/how-to-manage-high-availability/high-availability.png" alt-text="Screenshot showing the High availability page." lightbox="./media/how-to-manage-high-availability/high-availability.png":::

3. If high availability isn't enabled, the **Enable high availability** checkbox appears unchecked, and **High availability status** is shown as **Not Enabled**.

    :::image type="content" source="./media/how-to-manage-high-availability/high-availability-not-enabled.png" alt-text="Screenshot showing how the High availability page looks, when high availability isn't enabled." lightbox="./media/how-to-manage-high-availability/high-availability-not-enabled.png":::

4. Select the **Enable high availability** checkbox to enable the option. It shows **Same zone** and **Zone redundant** options. If you choose **Same zone**, the standby server is created in the same availability zone as the primary server.

    :::image type="content" source="./media/how-to-manage-high-availability/high-availability-same-zone.png" alt-text="Screenshot showing how the High availability page looks, when high availability is enabled with same zone." lightbox="./media/how-to-manage-high-availability/high-availability-same-zone.png":::

>[!NOTE]
>If the region in which your server is created doesn't support high availability with zone redundancy, the **Zone redundant** option is grayed out and disabled.

5. If the region supports zone redundancy, and you select **Zone redundant**, you can choose in which of the other available zones you want to deploy your standby server.

    :::image type="content" source="./media/how-to-manage-high-availability/high-availability-zone-redundant.png" alt-text="Screenshot showing the High availability page, when the feature is enabled with standby server deployed in a different zone than the primary." lightbox="./media/how-to-manage-high-availability/high-availability-zone-redundant.png":::

6. When everything is configured according to your needs, select **Save** to apply the changes. A dialog informs you of the cost increase associated with the deployment of the standby server. If you decide to proceed, select **Enable HA**.

    :::image type="content" source="./media/how-to-manage-high-availability/confirm-enable-high-availability.png" alt-text="Screenshot showing the dialog to confirm enablement of high availability." lightbox="./media/how-to-manage-high-availability/confirm-enable-high-availability.png.png":::

7. A deployment initiates and, when it completes, a notification shows that high availability is successfully enabled.

    :::image type="content" source="./media/how-to-manage-high-availability/notification-enable-high-availability.png" alt-text="Screenshot showing notification informing that high availability is successfully enabled." lightbox="./media/how-to-manage-high-availability/notification-enable-high-availability.png.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable high availability in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To enable high availability so that standby server is deployed in the same zone as the primary server, use this command:

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --high-availability SameZone
```

To enable high availability with standby server deployed in a different zone than the primary server, and if you want the zone to be automatically selected, use this command:

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --high-availability ZoneRedundant
```

Also, optionally, you can select the availability zone in which the standby server should be deployed. To do so, use this command:

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --high-availability ZoneRedundant --standby-zone <standby_zone>
```

If you're enabling high availability with zone redundancy, and the zone specified for standby matches the zone of the primary, you get this error:

```output
Your server is in availability zone <server>. The zone of the server cannot be same as the standby zone.
```

If you're enabling high availability with zone redundancy, and the zone specified for standby isn't available in that region, you get this error:

```output
(InvalidParameterValue) Invalid value given for parameter StandbyAvailabilityZone,availabilityZone. Specify a valid parameter value.
Code: InvalidParameterValue
Message: Invalid value given for parameter StandbyAvailabilityZone,availabilityZone. Specify a valid parameter value.
```

If high availability is enabled in one mode, and you try to enable it again, specifying a different mode, you get the following error:

```output
(InvalidParameterValue) Invalid value given for parameter Cannot switch Properties.HighAvailability.Mode directly from SameZone to ZoneRedundant. Please disable HA and then enable HA.. Specify a valid parameter value.
Code: InvalidParameterValue
Message: Invalid value given for parameter Cannot switch Properties.HighAvailability.Mode directly from SameZone to ZoneRedundant. Please disable HA and then enable HA.. Specify a valid parameter value.
```

---

## Disable high availability

Follow these steps to disable high availability for your Azure Database for PostgreSQL flexible server instance that is already configured with high availability.

1.  In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for PostgreSQL flexible server instance.

2.  On the Azure Database for PostgreSQL flexible server instance page, select **High Availability** from the front panel to open high availability page.
   
    :::image type="content" source="./media/how-to-manage-high-availability-portal/high-availability-left-panel.png" alt-text="Left panel selection screenshot."::: 

3.  Select on the **High availability** checkbox to **disable** the option. Then select **Save** to save the change.

     :::image type="content" source="./media/how-to-manage-high-availability-portal/disable-high-availability.png" alt-text="Screenshot showing disable high availability."::: 

4.  A confirmation dialog is shown where you can confirm disabling high availability.

5.  Select **Disable HA** button to disable the high availability.

6.  A notification appears stating that decommissioning of the high availability deployment is in progress.


## Enable high availability during server creation

This section provides details specifically for HA-related fields. You can follow these steps to deploy high availability while creating your Azure Database for PostgreSQL flexible server instance.

1.  In the [Azure portal](https://portal.azure.com/), choose Azure Database for PostgreSQL flexible server and select create. For details on how to fill details such as **Subscription**, **Resource group**, **Server name**, **Region**, and other fields, see [Create an instance of Azure Database for PostgreSQL - Flexible Server](quickstart-create-server.md).
   
    :::image type="content" source="./media/how-to-manage-high-availability-portal/subscription-region.png" alt-text="Screenshot of subscription and region selection.":::

2.  Choose your **availability zone**. This is useful if you want to collocate your application in the same availability zone as the database to reduce latency. Choose **No Preference** if you want the Azure Database for PostgreSQL flexible server instance to deploy the primary server on any availability zone. Only if you choose the availability zone for the primary in a zone-redundant HA deployment are you allowed to choose the standby availability zone.

     :::image type="content" source="./media/how-to-manage-high-availability-portal/zone-selection.png" alt-text="Screenshot of availability zone selection.":::  

3.  Select the checkbox for **Enable high availability**. That opens up an option to choose high availability mode. If the region doesn't support AZs, then only same-zone mode is enabled.

    :::image type="content" source="./media/how-to-manage-high-availability-portal/choose-high-availability-deployment-model.png" alt-text="High availability checkbox and mode selection.":::

4.  If you chose the Availability zone in step 2 and if you chose zone-redundant HA, then you can choose the standby zone.
    :::image type="content" source="./media/how-to-manage-high-availability-portal/choose-standby-availability-zone.png" alt-text="Screenshot of Standby AZ selection.":::
 

5.  If you want to change the default compute and storage, select  **Configure server**.
 
    :::image type="content" source="./media/how-to-manage-high-availability-portal/configure-server.png" alt-text="Screenshot of configure compute and storage screen.":::  

6.  If high availability option is checked, the burstable tier isn't available to choose. You can choose either
    **General purpose** or **Memory Optimized** compute tiers. Then you can select **compute size** for your choice from the dropdown.

    :::image type="content" source="./media/how-to-manage-high-availability-portal/select-compute.png" alt-text="Compute tier selection screen.":::  


7.  Select **storage size** in GiB using the sliding bar and select the **backup retention period** between 7 days and 35 days.
   
    :::image type="content" source="./media/how-to-manage-high-availability-portal/storage-backup.png" alt-text="Screenshot of Storage Backup."::: 

8. Select **Save**. 


## Forced failover

Follow these steps to force failover your primary to the standby Azure Database for PostgreSQL flexible server instance. This immediately brings the primary down and triggers a failover to the standby server. This is useful for cases like testing the unplanned outage failover time for your workload.

1.	In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for PostgreSQL flexible server instance that has high availability feature already enabled.
2.	On the Azure Database for PostgreSQL flexible server instance page, select High Availability from the front panel to open high availability page.
3.	Check the Primary availability zone and the Standby availability zone
4.	Select on Forced Failover to initiate the manual failover procedure. A dialog informs you of the potential downtime until the failover is complete. Read the message and select Ok.
5.	A notification appears to mention that failover is in progress.
6.	Once failover to the standby server is complete, a notification pops up.
7.	Check the new Primary availability zone and the Standby availability zone.
    
    :::image type="content" source="./media/how-to-manage-high-availability-portal/ha-forced-failover.png" alt-text="On-demand forced failover option screenshot."::: 

>[!IMPORTANT] 
> * Don't perform immediate, back-to-back failovers. Wait for at least 15-20 minutes between failovers, which will also allow the new standby server to be fully established.
>
> * The overall end-to-end operation time as reported on the portal may be longer than the actual downtime experienced by the application. Measure the downtime from the application perspective. 

## Planned failover

Follow these steps to perform a planned failover from your primary to the standby Azure Database for PostgreSQL flexible server instance. This will first prepare the standby server and performs the failover. This provides the least downtime as this performs a graceful failover to the standby server for situations like after a failover event, you want to bring the primary back to the preferred availability zone.
1.	In the [Azure portal](https://portal.azure.com/), select your existing Azure Database for PostgreSQL flexible server instance that has high availability feature already enabled.
2.	On the Azure Database for PostgreSQL flexible server instance page, select High Availability from the front panel to open high availability page.
3.	Check the Primary availability zone and the Standby availability zone
4.	Select on Planned Failover to initiate the manual failover procedure. A pop up informs you about the process. Read the message and select Ok.
5.	A notification appears mentioning that failover is in progress.
6.	Once failover to the standby server is complete, a notification pops up.
7.	Check the new Primary availability zone and the Standby availability zone.
        :::image type="content" source="./media/how-to-manage-high-availability-portal/ha-planned-failover.png" alt-text="Screenshot of On-demand planned failover."::: 

>[!IMPORTANT] 
>
> * Don't perform immediate, back-to-back failovers. Wait for at least 15-20 minutes between failovers, to allow the new standby server to be fully established.
>
> * We recommended performing planned failover during low activity periods.
>
> * The overall end-to-end operation time may be longer than the actual downtime experienced by the application. Measure the downtime from the application perspective.

## Enabling Zone redundant HA after the region supports AZ

There are Azure regions that don't support availability zones. If you already deployed non-HA servers, you can't directly enable zone redundant HA on the server, but you can perform restore and enable HA in that server. The following steps show how to enable Zone redundant HA for that server.

1. From the overview page of the server, select **Restore** to [perform a PITR](how-to-restore-server-portal.md#restore-to-the-latest-restore-point). Choose **Latest restore point**. 
2. Choose a server name, availability zone.
3. Select **Review+Create**".
4. A new Azure Database for PostgreSQL flexible server instance is created from the backup. 
5. Once the new server is created, from the overview page of the server, follow the [guide](#enable-high-availability-post-server-creation) to enable HA.
6. After data verification, you can optionally [delete](how-to-manage-server-portal.md#delete-a-server) the old server. 
7. Make sure your clients connection strings are modified to point to your new HA-enabled server.
   
[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

- [Overview of business continuity with Azure Database for PostgreSQL - Flexible Server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL - Flexible Server](/azure/reliability/reliability-postgresql-flexible-server).
- [Point-in-time restore of an Azure Database for PostgreSQL - Flexible Server instance](how-to-restore-server-portal.md).
