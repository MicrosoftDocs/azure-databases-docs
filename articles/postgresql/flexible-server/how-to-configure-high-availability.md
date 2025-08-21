---
title: Configure High Availability
description: This article describes how to configure and operate high availability on an Azure Database for PostgreSQL flexible server.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure and operate high availability on an Azure Database for PostgreSQL flexible server.
---

# Configure high availability for Azure Database for PostgreSQL

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article describes how to enable or disable high availability (HA) on your Azure Database for PostgreSQL flexible server by using the Azure portal or the Azure CLI. The information applies whether you're using flexible servers in the same zone or using a zone-redundant deployment model.

The high-availability feature deploys physically separate primary and standby replicas. You can provision the replicas within the same availability zone or in different zones, depending on the deployment model that you choose. For more information, see the [article about high-availability concepts](/azure/reliability/reliability-postgresql-flexible-server). You can enable high availability during or after the creation of your Azure Database for PostgreSQL flexible server.

> [!IMPORTANT]
> In April 2024, we implemented a billing model update for the v5 compute tier with HA-enabled servers. This change aimed to correctly reflect the charges by accounting for both the primary and standby servers. Before this change, we were incorrectly charging customers for the primary server only. Customers who use the v5 tier with HA-enabled servers now see billing quantities multiplied by 2. This update doesn't affect the v4 and v3 tiers.

## Enable high availability for existing servers

### [Portal](#tab/portal-enable-existing-server)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If high availability isn't enabled, the **Enable high availability** checkbox is cleared. Also, the **High availability status** value is **Not enabled**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-disabled.png" alt-text="Screenshot that shows the pane for configuring high availability." lightbox="./media/how-to-configure-high-availability/high-availability-disabled.png":::

1. Select the **Enable high availability** checkbox to enable the option.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable.png" alt-text="Screenshot that shows the checkbox selected to enable high availability." lightbox="./media/how-to-configure-high-availability/high-availability-enable.png":::

1. For **High availability mode**, the **Same zone** and **Zone redundant** options appear:

    * To create the standby server in the same availability zone as the primary server, select **Same zone**.

      :::image type="content" source="./media/how-to-configure-high-availability/high-availability-same-zone.png" alt-text="Screenshot that shows selection of the same-zone option for high availability." lightbox="./media/how-to-configure-high-availability/high-availability-same-zone.png":::

    * To choose zone redundancy, select **Zone redundant**. Then, for **Standby availability zone**, choose the other availability zones in which you want to deploy your standby server.

      > [!NOTE]
      > If the region in which your server is created doesn't support high availability with zone redundancy, the **Zone redundant** option is unavailable.

      :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant-zone-selection.png" alt-text="Screenshot that shows selection of the zone-redundant option and a standby availability zone for high availability." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant-zone-selection.png":::

1. When everything is configured according to your needs, select **Save** to apply the changes.

1. A dialog shows the cost increase associated with the deployment of the standby server. If you decide to proceed, select **Enable high availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-enable-high-availability.png" alt-text="Screenshot that shows the dialog to confirm the enablement of high availability." lightbox="./media/how-to-configure-high-availability/confirm-enable-high-availability.png":::

1. A deployment starts. When it finishes, a notification shows that you successfully enabled high availability.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png" alt-text="Screenshot that shows a notification about completed deployment of a high-availability configuration." lightbox="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable high availability in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To enable high availability so that the standby server is deployed in the same zone as the primary server, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability SameZone
```

To enable high availability with the standby server deployed in a different zone from the primary server's zone, and if you want the zone to be automatically selected, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant
```

Optionally, you can select the availability zone in which to deploy the standby server. Use this command:

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

If high availability is enabled in one mode, and you try to enable it again by specifying a different mode, you get this error:

```output
Code: InvalidParameterValue
Message: Invalid value given for parameter Cannot switch Properties.HighAvailability.Mode directly from SameZone to ZoneRedundant. Please disable HA and then enable HA.. Specify a valid parameter value.
```

---

## Disable high availability

### [Portal](#tab/portal-disable-existing-server)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If high availability is enabled, the **Enable high availability** checkbox is already selected. Also, **High availability mode** is set to the configured mode, and the **High availability status** value is typically **Healthy**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-status.png" alt-text="Screenshot that shows the pane for configuring high availability, with high-availability options already selected and a status of Healthy." lightbox="./media/how-to-configure-high-availability/high-availability-status.png":::

1. Clear the **Enable high availability** checkbox to disable the option.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-disabling.png" alt-text="Screenshot that shows the checkbox for enabling high availability cleared." lightbox="./media/how-to-configure-high-availability/high-availability-disabling.png":::

1. Select **Save** to apply the changes.

1. A dialog shows the cost reduction associated with the removal of the standby server. If you decide to proceed, select **Disable high availability**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-disable-high-availability.png" alt-text="Screenshot that shows the dialog to confirm disablement of high availability." lightbox="./media/how-to-configure-high-availability/confirm-disable-high-availability.png":::

1. A deployment starts. When it finishes, a notification shows that you successfully disabled high availability.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png" alt-text="Screenshot that shows a notification about successful disablement of high availability." lightbox="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png":::

### [CLI](#tab/cli-disable-existing-server)

You can disable high availability in an existing server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability Disabled
```

---

## Enable high availability during server provisioning

### [Portal](#tab/portal-enable-new-server)

1. In the [Azure portal](https://portal.azure.com/), during provisioning of a new Azure Database for PostgreSQL flexible server, go to the **High availability** section. Select **Same zone** or **Zone redundant**.

    > [!NOTE]
    > If the region in which your server is created doesn't support high availability with zone redundancy, the **Zone redundant** option is unavailable.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable-server-provisioning.png" alt-text="Screenshot that shows high-availability options during provisioning of a new flexible server." lightbox="./media/how-to-configure-high-availability/high-availability-enable-server-provisioning.png":::

1. Select a specific zone for the primary server by setting **Availability zone** to any value other than **No preference**.

1. For **Standby availability zone**, you can select a value for the standby server. Setting specific zones is useful if you want to reduce latency by collocating your application in the same zone as the database. If you want the standby server deployed on an availability zone that the service chooses for you automatically, select **No preference**.

    :::image type="content" source="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-standby-zone.png" alt-text="Screenshot that shows the selection of specific availability zones for primary and standby servers." lightbox="./media/how-to-configure-high-availability/high-availability-zone-redundant-server-provisioning-standby-zone.png":::

### [CLI](#tab/cli-enable-new-server)

You can enable high availability while provisioning a new server via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

> [!NOTE]
> You need to complete the following commands with parameters and values that vary, depending on how you want to configure other features of the provisioned server.

To deploy the primary server with a standby server in the same zone, and let the service choose the zone for you, use this command:

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

If the specified availability zone isn't supported in the selected region, you get this error:

```output
Code: AvailabilityZoneNotAvailable
Message: Specified availability zone is not supported in this region. Please choose a different availability zone.
```

To deploy the primary server with a standby server in a different zone, and let the service choose both zones for you, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant ...
```

To deploy the primary server with a standby server in a different zone, and to specify the zone for the primary but let the service choose the zone for the standby, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant \
  --zone <zone> ...
```

To deploy the primary server with a standby server in a different zone, and to specify the zone for the primary and the standby, use this command:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability ZoneRedundant \
  --zone <zone> \
  --standby-zone <standby_zone>...
```

If you chose zone-redundant high availability, and the same value is specified for the zones of the primary and standby servers, you get this error:

```output
Your server is in availability zone <zone>. The zone of the server cannot be same as the standby zone.
```

If the high-availability mode that you selected is zone redundant, and the region doesn't have multiple availability zones, you get this error:

```output
This region is single availability zone. Zone redundant high availability is not supported in a single availability zone region.
```

---

## Initiate a forced failover

Follow these steps to force a failover of your primary server to the standby server in Azure Database for PostgreSQL.

Initiating a forced failover immediately brings the primary server down and triggers a failover to the standby server. Initiating a forced failover is useful when you want to test how a failover caused by an unplanned outage would affect your workload.

> [!IMPORTANT]
>
> * Don't perform immediate, back-to-back failovers. Wait for at least 15 to 20 minutes between failovers. This wait time allows the new standby server to be fully established.
>
> * The overall end-to-end operation time, as reported on the portal, might be longer than the actual downtime that the application experiences. You should measure the downtime from the application's perspective.

### [Portal](#tab/portal-forced-failover)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server that has high availability enabled.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If the high-availability mode is set to **Zone redundant**, note the values assigned to **Primary availability zone** and **Standby availability zone**. They should be reversed after the failover operation finishes.

1. Select **Forced failover** to initiate the manual failover procedure. A dialog informs you of the expected downtime until the failover finishes. If you decide to proceed, select **Initiate forced failover**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-forced-failover.png" alt-text="Screenshot that shows the dialog displayed before the initiation of a forced failover." lightbox="./media/how-to-configure-high-availability/confirm-forced-failover.png":::

1. A notification appears and mentions that a failover is in progress.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png" alt-text="Screenshot that shows a notification about a failover in progress after the initiation of a forced failover." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png":::

1. After the failover to the standby server is complete, a notification informs you of the completion.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-completed.png" alt-text="Screenshot that shows the notification displayed when a forced failover finishes." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-completed.png":::

1. If the high-availability mode is configured as **Zone redundant**, confirm that the values of **Primary availability zone** and **Standby availability zone** are now reversed.

### [CLI](#tab/cli-force-failover)

You can enable high availability while provisioning a new server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

To initiate a forced failover, use this command:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server> \
  --failover Forced
```

If you try to force the failover of an Azure Database for PostgreSQL flexible server that doesn't have high availability enabled, you get this error:

```output
Failing over can only be triggered for zone redundant or same zone servers.
```

If you try to force the failover of an Azure Database for PostgreSQL flexible server that has high availability enabled but isn't ready to initiate the failover operation, you get this error:

```output
Code: OperationFailed
Message: Operation HandleWalServiceFailureManagementOperation failed, because server <server> not in active state.
```

---

## Initiate a planned failover

Follow these steps to perform a planned failover from your primary server to the standby server in Azure Database for PostgreSQL. Initiating this operation prepares the standby server and then performs the failover.

This failover operation provides the least downtime, because it performs a graceful failover to the standby server. It's useful for situations like bringing the primary server back to your preferred availability zone after an unexpected failover.

> [!IMPORTANT]
>
> * Don't perform immediate, back-to-back failovers. Wait for at least 15 to 20 minutes between failovers. This wait time allows the new standby server to be fully established.
>
> * We recommend performing planned failovers during low-activity periods.
>
> * The overall end-to-end operation time, as reported on the portal, might be longer than the actual downtime that the application experiences. You should measure the downtime from the application's perspective.

### [Portal](#tab/portal-planned-failover)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server that has high availability enabled.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If the high-availability mode is set to **Zone redundant**, note the values assigned to **Primary availability zone** and **Standby availability zone**. They should be reversed after the failover operation finishes.

1. Select **Planned failover** to initiate the manual failover procedure. A dialog informs you of the expected downtime until the failover finishes. If you decide to proceed, select **Initiate planned failover**.

    :::image type="content" source="./media/how-to-configure-high-availability/confirm-planned-failover.png" alt-text="Screenshot that shows the dialog displayed before the initiation of a planned failover." lightbox="./media/how-to-configure-high-availability/confirm-planned-failover.png":::

1. A notification appears and mentions that failover is in progress.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png" alt-text="Screenshot that shows a notification about a failover in progress after the initiation of a planned failover." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png":::

1. After the failover to the standby server is complete, a notification informs you of the completion.

    :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-completed.png" alt-text="Screenshot that shows the notification displayed when a planned failover finishes." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-completed.png":::

1. If the high-availability mode is configured as **Zone redundant**, confirm that the values of **Primary availability zone** and **Standby availability zone** are now reversed.

### [CLI](#tab/cli-planned-failover)

You can enable high availability while provisioning a new server via the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

To initiate a planned failover, use this command:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server> \
  --failover Planned
```

If you try to initiate the planned failover of an Azure Database for PostgreSQL flexible server that doesn't have high availability enabled, you get this error:

```output
Failing over can only be triggered for zone redundant or same zone servers.
```

If you try to initiate the planned failover of an Azure Database for PostgreSQL flexible server that has high availability enabled but isn't ready for the failover operation, you get this error:

```output
Code: OperationFailed
Message: Operation HandleWalServiceFailureManagementOperation failed, because server <server> not in active state.
```

---

## Special considerations

* Enabling or disabling high availability on an Azure Database for PostgreSQL flexible server doesn't change other settings, including networking configuration, firewall settings, server parameters, or backup retention. Enabling or disabling high availability is an online operation. It doesn't affect your application connectivity and operations.

* High availability with both replicas deployed in the same zone is supported and available in all regions in which Azure Database for PostgreSQL flexible servers are supported. However, high availability with zone redundancy is [available only in certain regions](overview.md#azure-regions).

* High availability isn't supported in the **Burstable** tier. It's supported only in the **General purpose** and **Memory optimized** tiers.

* If you deploy a server in a region that consists of a single availability zone, you can enable high availability in the same-zone mode only. If the region is enhanced in the future with multiple availability zones, you can deploy new Azure Database for PostgreSQL flexible servers with high availability configured as same zone or zone redundant.

  However, for any flexible servers that were deployed in the region when the region consisted of a single availability zone, you can't directly enable high availability in zone-redundant mode for them. As a workaround, you can restore those instances on new servers, and then enable zone-redundant high availability on the restored servers:

  1. [Restore an existing instance on a new server by using the latest restore point](how-to-restore-latest-restore-point.md).
  2. After you create the new server, [enable high availability with zone redundancy](#enable-high-availability-for-existing-servers).
  3. After data verification, you can optionally [delete](how-to-delete-server.md) the old server.
  4. Make sure that the connection strings of your clients are modified to point to your newly restored server.

## Related content

* [Overview of business continuity with Azure Database for PostgreSQL](concepts-business-continuity.md)
* [High availability (reliability) in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server)
