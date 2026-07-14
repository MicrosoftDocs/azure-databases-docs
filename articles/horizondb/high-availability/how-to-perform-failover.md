---
title: Perform Failover in Azure HorizonDB
description: This article describes how to perform failover in Azure HorizonDB.
#customer intent: As a user, I want to perform a planned failover in Azure HorizonDB, so that I can move the primary replica back to my preferred availability zone after an unexpected failover.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: high-availability
ms.topic: how-to
---

# Perform failover in Azure HorizonDB (Preview)

This article describes how to perform planned and forced failover in Azure HorizonDB. Failover operations switch the primary database replica to a standby replica to maintain availability during planned maintenance or unexpected outages. During a failover, client connections are briefly interrupted while the service redirects traffic to the new primary replica. Applications should implement retry logic to handle transient connectivity interruption.

Azure HorizonDB supports both planned and unplanned failover when high availability (HA) and replicas are configured. The service also provides automatic endpoint redirection to minimize application disruption.

- **Planned failover** - Planned failover occurs during scheduled operations, such as periodic software updates or minor version upgrades. You can also initiate a planned failover to move the primary replica to a preferred availability zone. When HA is enabled, Azure HorizonDB first applies these operations to the standby replica while applications continue to connect to the primary replica. The service then switches roles to complete the operation.

- **Unplanned failover** - Unplanned failover occurs due to unexpected events such as hardware failures, network issues, or software defects. If the primary database replica becomes unavailable, Azure HorizonDB automatically fails over to a standby replica and endpoints are automatically redirected allowing client operations to resume with minimal interruption.

- **Forced failover** - You can use a forced failover to test failover scenarios and simulate an unplanned outage while your production workload is running. This approach helps you evaluate application downtime and recovery behavior. You can also initiate a forced failover if the primary replica becomes unresponsive.

## What happens during failover

During a failover:
- Azure HorizonDB promotes the standby replica to primary.
- The service automatically redirects client connections to the new primary endpoint.
- Existing connections are dropped and must reconnect.
- No changes to connection strings are required.

## When to use each failover option

| Failover type | Use case |
| --- | --- |
| Planned failover | Scheduled maintenance, compute scaling, zone rebalancing, controlled testing |
| Forced failover | Disaster recovery testing or when the primary becomes unresponsive |

> [!IMPORTANT]  
>
> * Failover causes a brief interruption in connectivity. Ensure your application implements retry logic.
>
> * The overall end-to-end operation time, as reported on the portal, might be longer than the actual downtime that the application experiences. You should measure the downtime from the application's perspective.

## Steps to initiate a planned failover

Follow these steps to perform a planned failover from your primary replica to the standby replica in Azure HorizonDB.

When you initiate this operation, it prepares the standby replica and then performs the failover. This failover operation provides the least downtime, because it performs a graceful failover to the standby replica. It's useful for situations like bringing the primary replica back to your preferred availability zone after an unexpected failover.

### [Portal](#tab/portal-initiate-planned-failover)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **High availability**. Then, select **Manage replicas and failover**.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot showing the High availability page with high availability enabled." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::

1. Note the **Zone** values assigned to **ReadWrite** and **Read** roles.

   :::image type="content" source="media/how-to-perform-failover/replicas.png" alt-text="Screenshot showing the Replicas page from where you can start a planned failover." lightbox="media/how-to-perform-failover/replicas.png":::

1. Select **Planned failover**. A dialog box opens and you can choose the desired replica to fail over. If you decide to proceed, select **Fail over**.

   :::image type="content" source="media/how-to-perform-failover/planned-failover-selector.png" alt-text="Screenshot showing the dialog to select that read replica that will become the new primary replica." lightbox="media/how-to-perform-failover/planned-failover-selector.png":::

1. A notification appears to indicate that the failover is in progress.

   :::image type="content" source="media/how-to-perform-failover/planned-failover-in-progress.png" alt-text="Screenshot showing a notification to announce that planned failover is in progress." lightbox="media/how-to-perform-failover/planned-failover-in-progress.png":::

1. After the operation completes, the previous read replica becomes the primary replica. You can validate and confirm that **Zone** values assigned to **ReadWrite** and **Read** in roles are now reversed.

   :::image type="content" source="media/how-to-perform-failover/planned-failover-completed.png" alt-text="Screenshot showing a notification to announce that planned failover completed." lightbox="media/how-to-perform-failover/planned-failover-completed.png":::

### [CLI](#tab/cli-initiate-planned-failover)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to start a planned failover to a specific read replica. A planned failover starts by selecting one replica that plays the read role and configuring it to play the read-write role.

```azurecli-interactive
  az rest --method PATCH \
    --uri "https://management.azure.com/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}/providers/Microsoft.HorizonDB/clusters/$cluster/pools/DefaultPool/replicas/${replica}?api-version=2026-01-20-preview" \
  --body '{
    "properties": {
      "role": "ReadWrite"
    }
  }'
```

---

## Steps to initiate a forced failover

Follow these steps to force a failover of your primary server to the standby server in Azure HorizonDB.

When you initiate a forced failover, the primary server immediately goes down and triggers a failover to the standby server. Initiating a forced failover is useful when you want to test how a failover caused by an unplanned outage affects your workload.

### [Portal](#tab/portal-initiate-forced-failover)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **High availability**. Then, select **Manage replicas and failover**.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot showing the High availability page with high availability enabled." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::

1. Note the **Zone** values assigned to **ReadWrite** and **Read** roles.

   :::image type="content" source="media/how-to-perform-failover/replicas.png" alt-text="Screenshot showing the Replicas page from where you can start a forced failover." lightbox="media/how-to-perform-failover/replicas.png":::

1. Select **Forced failover**. A dialog box opens and you can choose the desired replica to fail over. If you decide to proceed, select **Fail over**.

   :::image type="content" source="media/how-to-perform-failover/forced-failover-selector.png" alt-text="Screenshot showing the dialog to select that read replica that will become the new primary replica." lightbox="media/how-to-perform-failover/forced-failover-selector.png":::

1. A notification appears to indicate that the failover is in progress.

   :::image type="content" source="media/how-to-perform-failover/forced-failover-in-progress.png" alt-text="Screenshot showing a notification to announce that forced failover is in progress." lightbox="media/how-to-perform-failover/forced-failover-in-progress.png":::

1. After the operation completes, the previous read replica becomes the primary replica. You can validate and confirm that **Zone** values assigned to **ReadWrite** and **Read** in the **Role** column are now reversed.

   :::image type="content" source="media/how-to-perform-failover/forced-failover-completed.png" alt-text="Screenshot showing a notification to announce that forced failover completed." lightbox="media/how-to-perform-failover/forced-failover-completed.png":::

### [CLI](#tab/cli-initiate-forced-failover)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to start a planned failover to a specific read replica. A forced failover starts by selecting the replica that plays the read-write role and configuring it to play the read role.

```azurecli-interactive
  az rest --method PATCH \
    --uri "https://management.azure.com/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}/providers/Microsoft.HorizonDB/clusters/$cluster/pools/DefaultPool/replicas/${replica}?api-version=2026-01-20-preview" \
  --body '{
    "properties": {
      "role": "Read"
    }
  }'
```

---

## Related content

- [High availability in Azure HorizonDB (Preview)](concepts-high-availability-failover.md)
- [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md)
