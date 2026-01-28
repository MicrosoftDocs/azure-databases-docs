---
title: Configure High Availability
description: This article describes how to configure and operate high availability on an Azure Database for PostgreSQL flexible server instance.
author: gaurikasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 01/13/2026
ms.service: azure-database-postgresql
ms.subservice: high-availability
ms.topic: how-to
# customer intent: As a user, I want to learn how to configure and operate high availability on an Azure Database for PostgreSQL flexible server instance.
---

# Configure high availability for Azure Database for PostgreSQL

This article describes how to enable or disable high availability (HA) on your Azure Database for PostgreSQL flexible server instance by using the Azure portal or the Azure CLI. The information applies whether you're using instances in the same zone or using a zone-redundant deployment model.

The high-availability feature deploys physically separate primary and standby replicas. You can provision the replicas within the same availability zone or in different zones, depending on the deployment model that you choose. For more information, see the [article about high-availability concepts](/azure/reliability/reliability-postgresql-flexible-server). You can enable high availability during or after the creation of your Azure Database for PostgreSQL flexible server instance.

> [!IMPORTANT]  
> In April 2024, Microsoft updated the billing model for the v5 compute tier with HA-enabled servers. This change correctly reflects the charges by accounting for both the primary and standby servers. Before this change, you were incorrectly charged for the primary server only. If you use the v5 tier with HA-enabled servers, you now see billing quantities multiplied by 2. This update doesn't affect the v4 and v3 tiers.

## Enable high availability for existing servers

You can enable high availability on an existing Azure Database for PostgreSQL flexible server instance at any time. When you enable high availability, the service creates a standby replica that mirrors your primary server. Depending on regional capacity and your configuration choices, the standby can be deployed in a different availability zone for maximum protection or in the same zone as the primary.

### [Portal](#tab/portal-enable-existing-server)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server instance.

1. On the left menu, in the **Settings** section, select **High availability**.

The **Zonal Resiliency** option controls whether your server is protected across availability zones. You have two choices:

- Enabled – When you select this option, Azure tries to create the standby server in a different availability zone than the primary. This option gives you the best protection against zone-level failures.
- Disabled – High availability isn't configured.

If you enable zonal resiliency but your region lacks capacity for a zone-redundant setup, an extra checkbox appears under the Enabled option. Selecting this checkbox allows the standby server to be created in the same zone as the primary server. When zonal capacity becomes available, Azure notifies you. At that point, you can use either PITR or read replicas to migrate workloads to a zone-redundant HA configuration for maximum resiliency. For more information, see the [Limitations and Considerations](#limitations-and-considerations) section.

1. If you didn't enable Zonal Resiliency, select the **Enabled** option.

   :::image type="content" source="./media/how-to-configure-high-availability/high-availability-disabled.png" alt-text="Screenshot that shows the pane for configuring high availability." lightbox="./media/how-to-configure-high-availability/high-availability-disabled.png":::

1. When you select the **Enabled** option, the **Zone redundant** option is applied by default for regions that support [availability zones](/azure/postgresql/flexible-server/overview#azure-regions). This configuration protects against zonal failures.

   :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable.png" alt-text="Screenshot that shows the checkbox selected to enable high availability." lightbox="./media/how-to-configure-high-availability/high-availability-enable.png":::

1. If the region doesn't have zonal capacity, to make sure that high availability (HA) gets enabled in your preferred region, select the checkbox under the enabled option to allow creating HA with Same-Zone mode of the region:

   :::image type="content" source="./media/how-to-configure-high-availability/high-availability-same-zone.png" alt-text="Screenshot that shows selection of the same-zone option for high availability." lightbox="./media/how-to-configure-high-availability/high-availability-same-zone.png":::

1. When you're done configuring the settings, select **Save** to apply the changes.

1. A dialog shows the cost increase associated with the deployment of the standby server. If you decide to proceed, select **Enable high availability**.

   :::image type="content" source="./media/how-to-configure-high-availability/confirm-enable-high-availability.png" alt-text="Screenshot that shows the dialog to confirm the enablement of high availability." lightbox="./media/how-to-configure-high-availability/confirm-enable-high-availability.png":::

1. A deployment starts. When it finishes, a notification shows that you successfully enabled high availability.

   :::image type="content" source="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png" alt-text="Screenshot that shows a notification about completed deployment of a high-availability configuration." lightbox="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png":::

### [CLI](#tab/cli-enable-existing-server)

You can enable high availability in an existing server by using the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

To enable high availability with the standby server in the same zone as the primary server, use this command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability SameZone
```

To enable high availability with the standby server in a different zone from the primary server's zone, and if you want the zone to be automatically selected, use this command:

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

If you enable high availability with zone redundancy, and the zone you specify for standby matches the zone of the primary, you get this error:

```output
Your server is in availability zone <server>. The zone of the server cannot be same as the standby zone.
```

If you enable high availability with zone redundancy, and the zone you specify for standby isn't available in that region, you get this error:

```output
Code: InvalidParameterValue
Message: Invalid value given for parameter StandbyAvailabilityZone,availabilityZone. Specify a valid parameter value.
```

If you enable high availability with zone redundancy, and the region doesn't have multiple availability zones, you get this error:

```output
This region is single availability zone. Zone redundant high availability is not supported in a single availability zone region.
```

If you enable high availability in one mode, and then try to enable it again by specifying a different mode, you get this error:

```output
Code: InvalidParameterValue
Message: Invalid value given for parameter Cannot switch Properties.HighAvailability.Mode directly from SameZone to ZoneRedundant. Please disable HA and then enable HA.. Specify a valid parameter value.
```

> [!NOTE]  
> The `--high-availability` parameter is deprecated and scheduled for removal in release 2.86.0 (May 2026). Use `--zonal-resiliency` instead for compatibility with future Azure CLI releases.

The **--zonal-resiliency** parameter helps you create a standby server in a different availability zone than primary and protects against zone‑level failures. It accepts two values: 

- Enabled – When you select this option, Azure tries to create the standby server in a different availability zone than the primary. This option gives you the best protection against zone-level failures.
- Disabled – High availability isn't configured.

To ensure your server is configured for high availability, enable the `--allow-same-zone` parameter. In regions without multiple availability zones, this option allows the standby server to be created in the same zone as the primary. When zonal capacity becomes available, Azure notifies you. At that point, you can use PITR or read replicas to migrate to a zone‑redundant HA configuration for maximum resiliency. For more information, refer to the [Limitations and Considerations](#limitations-and-considerations) section.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --zonal-resiliency enabled
  --allow-same-zone
```

---

## Disable high availability

You can disable high availability on your Azure Database for PostgreSQL flexible server instance when you no longer need the protection of a standby replica. Disabling high availability removes the standby server and reduces costs, but your server is no longer protected against zone or server failures.

### [Portal](#tab/portal-disable-existing-server)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server instance.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If high availability is enabled, the **Enabled** radio button for **Zonal Resiliency** is already selected. Also, **High availability mode** is set to the configured mode, and the **High availability status** value is typically **Healthy**.

   :::image type="content" source="./media/how-to-configure-high-availability/high-availability-status.png" alt-text="Screenshot that shows the pane for configuring high availability, with high-availability options already selected and a status of Healthy." lightbox="./media/how-to-configure-high-availability/high-availability-status.png":::

1. Select the **Disabled** radio button to disable high availability.

   :::image type="content" source="./media/how-to-configure-high-availability/high-availability-disabling.png" alt-text="Screenshot that shows the checkbox for enabling high availability cleared." lightbox="./media/how-to-configure-high-availability/high-availability-disabling.png":::

1. Select **Save** to apply the changes.

1. A dialog shows the cost reduction associated with the removal of the standby server. If you decide to proceed, select **Disable high availability**.

   :::image type="content" source="./media/how-to-configure-high-availability/confirm-disable-high-availability.png" alt-text="Screenshot that shows the dialog to confirm disablement of high availability." lightbox="./media/how-to-configure-high-availability/confirm-disable-high-availability.png":::

1. A deployment starts. When it finishes, a notification shows that you successfully disabled high availability.

   :::image type="content" source="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png" alt-text="Screenshot that shows a notification about successful disablement of high availability." lightbox="./media/how-to-configure-high-availability/notification-enable-disable-high-availability.png":::

### [CLI](#tab/cli-disable-existing-server)

You can disable high availability in an existing server by using the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --high-availability Disabled
```

To disable high availability, run the same command with `--zonal-resiliency` set to `disabled`. The previous `--high-availability` parameter is deprecated and now triggers this warning: "Argument '--high-availability' has been deprecated and will be removed in next breaking change release(2.86.0) scheduled for May 2026. Use '--zonal-resiliency' instead."

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --zonal-resiliency Disabled
```

---

## Enable Business Critical (High Availability) during server provisioning

You can configure high availability when you first create your Azure Database for PostgreSQL flexible server instance. By enabling high availability during provisioning, you deploy a standby replica alongside your primary server, so you get immediate protection against zone or server failures.

### [Portal](#tab/portal-enable-new-server)

1. In the [Azure portal](https://portal.azure.com/), during provisioning of a new Azure Database for PostgreSQL flexible server instance, go to the **Business Critical (High availability)** section. Select the **Enabled** option in the Zonal Resiliency section.
   - By default, the server tries to create the standby server in a different availability zone with **Zone-Redundant** HA mode for maximum zonal resiliency.

   :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable-zonal-resiliency.png" alt-text="Screenshot that shows enabling HA with zone-redundant option." lightbox="./media/how-to-configure-high-availability/high-availability-enable-zonal-resiliency.png":::

   - If zonal capacity isn't available, select the **Allow standby in same zone if zonal resiliency fails** checkbox as a fallback. If you don't select this option, you can't proceed to the next step in the create workflow. This check ensures high availability remains enabled. When zonal capacity becomes available, Azure notifies you. You can then use PITR or read replicas to migrate workloads to a zone-redundant HA configuration for maximum resiliency.

     :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable-same-zone-error.png" alt-text="Screenshot that shows validation error message for same-zone HA option." lightbox="./media/how-to-configure-high-availability/high-availability-enable-same-zone-error.png":::

   - After you select the checkbox, proceed to the Authentication section in the create workflow.

     :::image type="content" source="./media/how-to-configure-high-availability/high-availability-enable-same-zone.png" alt-text="Screenshot that shows high-availability with same-zone HA option." lightbox="./media/how-to-configure-high-availability/high-availability-enable-same-zone.png":::

1. Select a specific zone for the primary server by setting **Availability zone** to any value other than **No preference**.

   :::image type="content" source="./media/how-to-configure-high-availability/primary-az-value.png" alt-text="Screenshot that shows the selection of specific availability zones for primary server." lightbox="./media/how-to-configure-high-availability/primary-az-value.png":::

### [CLI](#tab/cli-enable-new-server)

You can enable high availability while provisioning a new server by using the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

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

If you choose zone-redundant high availability, and specify the same value for the zones of the primary and standby servers, you get this error:

```output
Your server is in availability zone <zone>. The zone of the server cannot be same as the standby zone.
```

If the high-availability mode that you select is zone redundant, and the region doesn't have multiple availability zones, you get this error:

```output
This region is single availability zone. Zone redundant high availability is not supported in a single availability zone region.
```
> [!NOTE]  
> Using the `--high-availability` parameter triggers a deprecation warning: "Argument '--high-availability' has been deprecated and will be removed in next breaking change release(2.86.0) scheduled for May 2026. Use '--zonal-resiliency' instead." Update your scripts and commands to use `--zonal-resiliency` to ensure compatibility with future Azure CLI releases.

Use the **--zonal-resiliency** parameter when creating an Azure Database for PostgreSQL flexible server instance. This ensures the standby server is provisioned in a different availability zone than the primary, improving protection against zone‑level failures.

If the region doesn't currently support multiple availability zones, add the **--allow-same-zone** parameter. This parameter acts as a fallback: if Azure can't create the standby in another zone, it creates the standby in the same zone as the primary so that high availability is still enabled in your chosen region.
When zonal capacity later becomes available, Azure notifies you. You can then use PITR or a read replica to move your workloads to a zone‑redundant HA configuration for improved resiliency.

The `--zonal-resiliency` parameter accepts these values:

- Enabled – When you select this option, Azure tries to create the standby server in a different availability zone than the primary. This option gives you the best protection against zone-level failures.
- Disabled – High availability isn't configured.

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --zonal-resiliency enabled \
  --allow-same-zone
```

---

## Initiate a forced failover

Follow these steps to force a failover of your primary server to the standby server in Azure Database for PostgreSQL.

When you initiate a forced failover, the primary server immediately goes down and triggers a failover to the standby server. Initiating a forced failover is useful when you want to test how a failover caused by an unplanned outage would affect your workload.

> [!IMPORTANT]  
>
> - Don't perform immediate, back-to-back failovers. Wait for at least 15 to 20 minutes between failovers. This wait time allows the new standby server to be fully established.
>
> - The overall end-to-end operation time, as reported on the portal, might be longer than the actual downtime that the application experiences. You should measure the downtime from the application's perspective.

### [Portal](#tab/portal-forced-failover)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server instance that has high availability enabled.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If the high-availability mode is set to **Zone redundant**, note the values assigned to **Primary availability zone** and **Standby availability zone**. Reverse these values after the failover operation finishes.

1. Select **Forced failover** to start the manual failover procedure. A dialog informs you of the expected downtime until the failover finishes. If you decide to proceed, select **Initiate forced failover**.

   :::image type="content" source="./media/how-to-configure-high-availability/confirm-forced-failover.png" alt-text="Screenshot that shows the dialog displayed before the initiation of a forced failover." lightbox="./media/how-to-configure-high-availability/confirm-forced-failover.png":::

1. A notification appears and mentions that a failover is in progress.

   :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png" alt-text="Screenshot that shows a notification about a failover in progress after the initiation of a forced failover." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-initiating.png":::

1. After the failover to the standby server completes, a notification informs you of the completion.

   :::image type="content" source="./media/how-to-configure-high-availability/notification-forced-failover-completed.png" alt-text="Screenshot that shows the notification displayed when a forced failover finishes." lightbox="./media/how-to-configure-high-availability/notification-forced-failover-completed.png":::

1. If the high-availability mode is configured as **Zone redundant**, confirm that the values of **Primary availability zone** and **Standby availability zone** are now reversed.

### [CLI](#tab/cli-force-failover)

You can enable high availability while provisioning a new server by using the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

To initiate a forced failover, use this command:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server> \
  --failover Forced
```

If you try to force the failover of an Azure Database for PostgreSQL flexible server instance that doesn't have high availability enabled, you get this error:

```output
Failing over can only be triggered for zone redundant or same zone servers.
```

If you try to force the failover of an Azure Database for PostgreSQL flexible server instance that has high availability enabled but isn't ready to initiate the failover operation, you get this error:

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
> * Perform planned failovers during low-activity periods.
>
> * The overall end-to-end operation time, as reported on the portal, might be longer than the actual downtime that the application experiences. You should measure the downtime from the application's perspective.

### [Portal](#tab/portal-planned-failover)

1. In the [Azure portal](https://portal.azure.com/), select your Azure Database for PostgreSQL flexible server instance that has high availability enabled.

1. On the left menu, in the **Settings** section, select **High availability**.

1. If the high-availability mode is set to **Zone redundant**, note the values assigned to **Primary availability zone** and **Standby availability zone**. Reverse these values after the failover operation finishes.

1. Select **Planned failover** to start the manual failover procedure. A dialog informs you of the expected downtime until the failover finishes. If you decide to proceed, select **Initiate planned failover**.

   :::image type="content" source="./media/how-to-configure-high-availability/confirm-planned-failover.png" alt-text="Screenshot that shows the dialog displayed before the initiation of a planned failover." lightbox="./media/how-to-configure-high-availability/confirm-planned-failover.png":::

1. A notification appears and mentions that failover is in progress.

   :::image type="content" source="./media/how-to-configure-high-availability/notification-planned-failover-initiating.png" alt-text="Screenshot that shows a notification about a failover in progress after the initiation of a planned failover." lightbox="./media/how-to-configure-high-availability/notification-planned-failover-initiating.png":::

1. After the failover to the standby server completes, a notification informs you of the completion.

   :::image type="content" source="./media/how-to-configure-high-availability/notification-planned-failover-completed.png" alt-text="Screenshot that shows the notification displayed when a planned failover finishes." lightbox="./media/how-to-configure-high-availability/notification-planned-failover-completed.png":::

1. If the high-availability mode is configured as **Zone redundant**, confirm that the values of **Primary availability zone** and **Standby availability zone** are now reversed.

### [CLI](#tab/cli-planned-failover)

You can enable high availability while provisioning a new server by using the [az postgres flexible-server restart](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-restart) command.

To initiate a planned failover, use the following command:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server> \
  --failover Planned
```

If you try to initiate the planned failover of an Azure Database for PostgreSQL flexible server instance that doesn't have high availability enabled, you get the following error:

```output
Failing over can only be triggered for zone redundant or same zone servers.
```

If you try to initiate the planned failover of an Azure Database for PostgreSQL flexible server instance that has high availability enabled but isn't ready for the failover operation, you get the following error:

```output
Code: OperationFailed
Message: Operation HandleWalServiceFailureManagementOperation failed, because server <server> not in active state.
```

---

## Limitations and considerations

- Enabling or disabling high availability on an Azure Database for PostgreSQL flexible server instance doesn't change other settings, including networking configuration, firewall settings, server parameters, or backup retention. Enabling or disabling high availability is an online operation. It doesn't affect your application connectivity and operations.

- Azure Database for PostgreSQL supports high availability with both replicas deployed in the same zone. This configuration is available in all supported regions. However, high availability with zone redundancy is [available only in certain regions](../overview.md#azure-regions).

- The **Burstable** tier doesn't support high availability. Only the **General purpose** and **Memory optimized** tiers support high availability.

- If you deploy a server in a region that consists of a single availability zone, you can enable high availability in the same-zone mode only. If the region is enhanced in the future with multiple availability zones, you can deploy new Azure Database for PostgreSQL flexible server instances with high availability configured as same zone or zone redundant.

  However, for any instances that you deployed in the region when the region consisted of a single availability zone, you can't directly enable high availability in zone-redundant mode. As a workaround, you can use the restore option or read replica option:

#### Restore option
  1. [Restore an existing instance on a new server by using the latest restore point](../backup-restore/how-to-restore-latest-restore-point.md).
  1. After you create the new server, [enable high availability with zone redundancy](#enable-high-availability-for-existing-servers).
  1. After data verification, you can optionally [delete](../configure-maintain/how-to-delete-server.md) the old server.
  1. Make sure that the connection strings of your clients are modified to point to your newly restored server.

#### Read replica option
  1. [Create a read replica in the same region as your primary server](../read-replica/concepts-read-replicas.md).
  1. Promote the read replica to become the new primary server.
  1. To preserve the original name, either use virtual endpoints or drop the old primary, then create and promote a new read replica.
  1. For portal users, enable Zonal Resiliency. For developer tools, set High Availability with the Zone-Redundant option.


## Related content

- [Overview of business continuity with Azure Database for PostgreSQL](../backup-restore/concepts-business-continuity.md)
- [High availability (reliability) in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server)
