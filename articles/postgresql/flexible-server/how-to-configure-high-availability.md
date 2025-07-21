---
title: Configure high availability
description: This article describes how to configure and operate high availability in an Azure Database for PostgreSQL flexible server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure and operate high availability in an Azure Database for PostgreSQL flexible server.
---

# Configure high availability

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article describes how you can enable or disable high availability configuration in your Azure Database for PostgreSQL flexible server in same zone, or zone redundant deployment models.

High availability feature deploys physically separate primary and standby replicas. Both replicas can be provisioned within the same availability zone or each on a different zone, depending on the deployment model you choose. For more information, see [high availability concepts](/azure/reliability/reliability-postgresql-flexible-server). You can enable high availability at creation time of your Azure Database for PostgreSQL flexible server, or you can do it after the server is created.

> [!IMPORTANT]
> _Billing Model Update for Azure Database for PostgreSQL Flexible Server (v5 HA):_
In April, we implemented a billing model update for v5 SKU with High Availability (HA) enabled servers. This change aims to correctly reflect the charges, by accounting for both the primary and standby servers. Before this change, we were incorrectly charging customers for the primary server only. Customers using v5 SKU with HA enabled servers would now see billing quantities multiplied by 2. This update doesn't impact v4 and v3 SKUs.

## Steps to enable high availability for existing servers

### [Portal](#tab/portal-enable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **High availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-disabled.png" alt-text="Screenshot showing the High availability page." lightbox="./media/how-to-configure-high-availability/high-availability-disabled.png":::

3. If high availability isn't enabled, the **Enable high availability** checkbox appears unchecked.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-not-enabled.png" alt-text="Screenshot showing how the Enable high availability checkbox is unchecked, when high availability isn't enabled." lightbox="./media/how-to-configure-high-availability/high-availability-not-enabled.png":::

4. Also, **High availability status** is shown as **Not enabled**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-not-enabled-status.png" alt-text="Screenshot showing how the High availability status shows as Not enabled, when high availability isn't enabled." lightbox="./media/how-to-configure-high-availability/high-availability-not-enabled-status.png":::

5. Select the **Enable high availability** checkbox to enable the option.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable.png" alt-text="Screenshot showing how to enable high availability, when high availability isn't enabled." lightbox="./media/how-to-configure-high-availability/high-availability-enable.png":::

6. It shows **Same zone** and **Zone redundant** options. If you choose **Same zone**, the standby server is created in the same availability zone as the primary server.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-same-zone.png" alt-text="Screenshot showing how to select Same zone for High availability mode, while enabling high availability." lightbox="./media/how-to-configure-high-availability/high-availability-same-zone.png":::

>[!NOTE]
>If the region in which your server is created doesn't support high availability with zone redundancy, the **Zone redundant** option is grayed out and disabled.

7. If the region supports zone redundancy, you can select **Zone redundant**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant.png" alt-text="Screenshot showing the High availability page, when you enable high availability with standby server deployed in a different zone than the primary." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant.png":::

8. In that case, you can choose in which of the other availability zones you want to deploy your standby server.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant-zone-selection.png" alt-text="Screenshot showing the High availability page, and how you can select a specific zone, when you enable high availability with standby server deployed in a different zone than the primary." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant-zone-selection.png":::

9. When everything is configured according to your needs, select **Save** to apply the changes.

    :::image type="content" source="./media/how-to-configure-high-availability/enable-high-availability-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-configure-high-availability/enable-high-availability-save.png":::

9. A dialog informs you of the cost increase associated with the deployment of the standby server. If you decide to proceed, select **Enable high availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-enable-high-availability.png" alt-text="Screenshot showing the dialog to confirm enablement of high availability." lightbox="./media/how-to-configure-high-availability/confirm-enable-high-availability.png":::

7. A deployment initiates and, when it completes, a notification shows that high availability is successfully enabled.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png" alt-text="Screenshot showing notification informing that high availability is successfully enabled." lightbox="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable high availability in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To enable high availability so that standby server is deployed in the same zone as the primary server, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability SameZone
```

To enable high availability with standby server deployed in a different zone than the primary server, and if you want the zone to be automatically selected, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant
```

Also, optionally, you can select the availability zone in which the standby server should be deployed. To do so, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant \
  --standby-zone <standby_zone>
```

If you're enabling high availability with zone redundancy, and the zone specified for standby matches the zone of the primary, you get this error:

```output
Your server is in availability zone <server>. The zone of the server cannot be same as the standby zone.
```

If you're enabling high availability with zone redundancy, and the zone specified for standby isn't available in that region, you get this error:

```output
Code: InvalidParameterValue
Message: Invalid value given for parameter StandbyAvailabilityZone,availabilityZone. Specify a valid parameter value.
```

If you're enabling high availability with zone redundancy, and the region doesn't have multiple availability zones, you get this error:

```output
This region is single availability zone. Zone redundant high availability is not supported in a single availability zone region.
```

If high availability is enabled in one mode, and you try to enable it again, specifying a different mode, you get the following error:

```output
Code: InvalidParameterValue
Message: Invalid value given for parameter Cannot switch Properties.HighAvailability.Mode directly from SameZone to ZoneRedundant. Please disable HA and then enable HA.. Specify a valid parameter value.
```

---

## Steps to disable high availability

### [Portal](#tab/portal-disable-existing-server)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, under the **Settings** section, select **High availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot showing the High availability page with same zone high availability enabled." lightbox="./media/how-to-configure-high-availability/high-availability-enabled.png":::

3. If high availability is enabled, the **Enable high availability** checkbox appears checked.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable-marked.png" alt-text="Screenshot showing the High availability page with the Enable high availability checkbox marked." lightbox="./media/how-to-configure-high-availability/high-availability-enable-marked.png":::

4. Also, **High availability mode** is set to the mode configured.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-mode.png" alt-text="Screenshot showing how the High availability mode looks, when same zone high availability is enabled." lightbox="./media/how-to-configure-high-availability/high-availability-mode.png":::

5. And **High availability status** is typically shown as **Healthy**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-status.png" alt-text="Screenshot showing how the High availability status shows as Healthy." lightbox="./media/how-to-configure-high-availability/high-availability-status.png":::

6. Clear the **Enable high availability** checkbox to disable the option.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-disabling.png" alt-text="Screenshot showing how the High availability page looks, when disabling high availability." lightbox="./media/how-to-configure-high-availability/high-availability-disabling.png":::

6. Select **Save** to apply the changes.

    :::image type="content" source="./media/how-to-configure-high-availability/disable-high-availability-save.png" alt-text="Screenshot showing the Save button to disable high availability." lightbox="./media/how-to-configure-high-availability/disable-high-availability-save.png":::

7.  A dialog informs you of the cost reduction associated with the removal of the standby server. If you decide to proceed, select **Disable high availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-disable-high-availability.png" alt-text="Screenshot showing the dialog to confirm disablement of high availability." lightbox="./media/how-to-configure-high-availability/confirm-disable-high-availability.png":::

8. A deployment initiates and, when it completes, a notification shows that high availability is successfully disabled.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png" alt-text="Screenshot showing notification informing that high availability is successfully disabled." lightbox="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png":::

### [CLI](#tab/cli-disable-existing-server)

You can disable high availability in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To disable high availability, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability Disabled
```

---

## Steps to enable high availability during server provisioning

### [Portal](#tab/portal-enable-new-server)

Using the [Azure portal](https://portal.azure.com/):

1. During provisioning of a new instance of Azure Database for PostgreSQL Flexible Server, in the **High availability** section, select **Same zone** or **Zone redundant**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable-server-provisioning.png" alt-text="Screenshot showing how to configure high availability options during provisioning of a new instance." lightbox="./media/how-to-configure-high-availability/high-availability-enable-server-provisioning.png":::

>[!NOTE]
>If the region in which your server is created doesn't support high availability with zone redundancy, the **Zone redundant** option is grayed out and disabled.

2.  Select a specific zone for the primary server by setting **Availability zone** to any value other than **No preference**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-availability-zone.png" alt-text="Screenshot showing how to select specific availability zone for primary server." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-availability-zone.png":::

3.  When you select a specific availability zone for the primary server, and select **Zone redundant**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-zone-redundant.png" alt-text="Screenshot showing how to select Zone redundant to have the standby server created in a different zone than the primary server." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-zone-redundant.png":::

4.  You can also select an explicitly a value for the standby server in **Standby availability zone**. Setting the zones to specific zones is useful if you want to collocate your application in the same zone as the database, to reduce latency. Choose **No preference** if you want the standby server to deploy on an availability zone automatically chosen for you.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-standby-zone.png" alt-text="Screenshot showing how to select specific availability zones for primary and standby servers." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-standby-zone.png":::

### [CLI](#tab/cli-enable-new-server)

You can enable high availability while provisioning a new server via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

> [!NOTE]
> The following commands need to be completed with other parameters, whose presence and values would vary depending on how you want to configure other features of the provisioned server.

To deploy the primary server with a standby server in the same zone, and let the service choose for you the zone, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability SameZone ...
```

To deploy the primary server with a standby server in the same zone, and explicitly choose the zone, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability SameZone \
  --zone <zone> ...
```

If the availability zone specified isn't supported in the selected region, you get this error:

```output
Code: AvailabilityZoneNotAvailable
Message: Specified availability zone is not supported in this region. Please choose a different availability zone.
```

To deploy the primary server with a standby server in a different zone, and let the service choose for you both zones, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant ...
```

To deploy the primary server with a standby server in a different zone, explicitly specify the zone for the primary but let the service choose the zone for the standby, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant \
  --zone <zone> ...
```

To deploy the primary server with a standby server in a different zone, and explicitly specify the zone for the primary and the standby, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant \
  --zone <zone> \
  --standby-zone <standby_zone>...
```

If you choose zone redundant high availability, and the same value is specified for the zones of the primary and standby servers, you get this error:

```output
Your server is in availability zone <zone>. The zone of the server cannot be same as the standby zone.
```

If the high availability mode selected is zone redundant, and the region doesn't have multiple availability zones, you get this error:

```output
This region is single availability zone. Zone redundant high availability is not supported in a single availability zone region.
```

---

## Steps to initiate a forced failover

Follow these steps to force a failover of your primary server to the standby server in an Azure Database for PostgreSQL flexible server. Initiating a forced failover immediately brings the primary server down, and triggers a failover to the standby server. Initiating a forced failover is useful for cases in which you want to test how a failover caused by an unplanned outage would affect your workload.

>[!IMPORTANT] 
> * Don't perform immediate, back-to-back failovers. Wait for at least 15-20 minutes between failovers. Such wait allows the new standby server to be fully established.
>
> * The overall end-to-end operation time, as reported on the portal, could be longer than the actual downtime experienced by the application. You should measure the downtime from the application perspective.

### [Portal](#tab/portal-forced-failover)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server that has high availability enabled.

2. In the resource menu, under the **Settings** section, select **High availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot showing the High availability page." lightbox="./media/how-to-configure-high-availability/high-availability-enabled.png":::

3.	If high availability mode is set to **Zone redundant** mode, you might want to take note of the values assigned to **Primary availability zone** and **Standby availability zone**, as they should be reversed after the failover operation completes.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png" alt-text="Screenshot showing the zones in which primary and standby servers are deployed." lightbox="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png":::

4.	Select **Forced failover** to initiate the manual failover procedure. A dialog informs you of the expected downtime until the failover completes. If you decide to proceed, select **Initiate forced failover**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-forced-failover.png" alt-text="Screenshot showing the informational message displayed before initiating a forced failover." lightbox="./media/how-to-configure-high-availability/confirm-forced-failover.png":::

5.	A notification appears to mention that failover is in progress.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png" alt-text="Screenshot showing the informational message displayed when initiating a forced failover." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png":::

6.	Once the failover to the standby server is complete, a notification informs you of the operation completion.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-completed.png" alt-text="Screenshot showing the informational message displayed when forced failover completed." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-completed.png":::

7.	If the high availability mode is configured as zone redundant, confirm that the values of **Primary availability zone** and **Standby availability zone** are now reversed.
    
    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png" alt-text="Screenshot showing the zones in which primary and standby servers are deployed." lightbox="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png":::

### [CLI](#tab/cli-force-failover)

You can enable high availability while provisioning a new server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

To initiate a forced failover, use this command:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server> \
  --failover Forced
```

If you try to force a failover of an Azure Database for PostgreSQL flexible server that doesn't have high availability enabled, you get this error:

```output
Failing over can only be triggered for zone redundant or same zone servers.
```

If you try to force a failover of an Azure Database for PostgreSQL flexible server that has high availability enabled, but isn't ready to initiate the failover operation, you get this error:

```output
Code: OperationFailed
Message: Operation HandleWalServiceFailureManagementOperation failed, because server <server> not in active state.
```

---

## Steps to initiate a planned failover

Follow these steps to perform a planned failover from your primary server to the standby server in an Azure Database for PostgreSQL flexible server. Initiating this operation first prepares the standby server, and then performs the failover. This failover operation provides the least downtime, as it performs a graceful failover to the standby server. It's useful for situations like after an unexpected failover occurs, and you want to bring the primary server back to your preferred availability zone.

>[!IMPORTANT] 
> * Don't perform immediate, back-to-back failovers. Wait for at least 15-20 minutes between failovers. Such wait allows the new standby server to be fully established.
>
> * We recommended performing planned failovers during low activity periods.
>
> * The overall end-to-end operation time, as reported on the portal, could be longer than the actual downtime experienced by the application. You should measure the downtime from the application perspective.

### [Portal](#tab/portal-planned-failover)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server that has high availability enabled.

2. In the resource menu, under the **Settings** section, select **High availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot showing the High availability page." lightbox="./media/how-to-configure-high-availability/high-availability-enabled.png":::

3.	If high availability mode is set to **Zone redundant** mode, you might want to take note of the values assigned to **Primary availability zone** and **Standby availability zone**, as they should be reversed after the failover operation completes.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png" alt-text="Screenshot showing the zones in which primary and standby servers are deployed." lightbox="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png":::

4.	Select **Planned failover** to initiate the manual failover procedure. A dialog informs you of the expected downtime until the failover completes. If you decide to proceed, select **Initiate planned failover**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-planned-failover.png" alt-text="Screenshot showing the informational message displayed before initiating a planned failover." lightbox="./media/how-to-configure-high-availability/confirm-planned-failover.png":::

5.	A notification appears to mention that failover is in progress.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png" alt-text="Screenshot showing the informational message displayed when initiating a planned failover." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png":::

6.	Once the failover to the standby server is complete, a notification informs you of the operation completion.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-completed.png" alt-text="Screenshot showing the informational message displayed when planned failover completed." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-completed.png":::

7.	If the high availability mode is configured as zone redundant, confirm that the values of **Primary availability zone** and **Standby availability zone** are now reversed.
    
    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png" alt-text="Screenshot showing the zones in which primary and standby servers are deployed." lightbox="./media/how-to-configure-high-availability/high-availability-primary-standby-zones.png":::

### [CLI](#tab/cli-planned-failover)

You can enable high availability while provisioning a new server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

To initiate a forced failover, use this command:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server> \
  --failover Planned
```

If you try to force a failover of an Azure Database for PostgreSQL flexible server that doesn't have high availability enabled, you get this error:

```output
Failing over can only be triggered for zone redundant or same zone servers.
```

If you try to force a failover of an Azure Database for PostgreSQL flexible server that has high availability enabled, but isn't ready to initiate the failover operation, you get this error:

```output
Code: OperationFailed
Message: Operation HandleWalServiceFailureManagementOperation failed, because server <server> not in active state.
```

---

## Special considerations

- Enabling or disabling high availability on an Azure Database for PostgreSQL flexible server doesn't change other settings, including networking configuration, firewall settings, server parameters, or backup retention. Enabling or disabling high availability is an online operation, and doesn't affect your application connectivity and operations.

- High availability with both replicas deployed in the same zone is supported and available in all regions in which Azure Database for PostgreSQL flexible server is supported. However, high availability with zone redundancy is [only available in certain regions](overview.md#azure-regions).

- High availability isn't supported in the **Burstable** tier. It's only supported in **General purpose** or **Memory optimized** tiers.

- If you deploy a server in a region that consists of a single availability zone, you can enable high availability in same zone mode only. If the region is enhanced in the future with multiple availability zones, you can deploy new Azure Database for PostgreSQL flexible server with high availability configured as same zone or zone redundant. However, for any instances that were deployed in the region when the region consisted of a single availability zone, you can't directly enable high availability in zone redundant mode for them. As a workaround, you can restore those instances onto new instances, and then enable zone redundant high availability on the restored servers.

    1. Follow the instructions provided in [Restore to latest restore point](how-to-restore-latest-restore-point.md), to restore the existing instance on a new one, using the latest restore point.
    2. Once the new server is created, [enable high availability with zone redundancy](#steps-to-enable-high-availability-for-existing-servers).
    3. After data verification, you can optionally [delete](how-to-delete-server.md) the old server.
    4. Make sure that the connection strings of your clients are modified to point to your newly restored instance.

## Related content

- [Overview of business continuity with Azure Database for PostgreSQL flexible server](concepts-business-continuity.md).
- [High availability in Azure Database for PostgreSQL flexible server](/azure/reliability/reliability-postgresql-flexible-server).