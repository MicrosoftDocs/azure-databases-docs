---
title: Configure High Availability in Azure HorizonDB
description: This article describes how to configure and operate high availability in Azure HorizonDB.
#customer intent: As a user, I want to enable high availability on my existing Azure HorizonDB cluster, so that I can protect my database against zone outages without recreating the instance.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 07/06/2026
ms.service: azure-horizondb
ms.subservice: high-availability
ms.topic: how-to
---

# Configure high availability in Azure HorizonDB (Preview)

This article describes how to enable or disable high availability (HA) on your Azure HorizonDB cluster.

The high-availability feature enhances reliability and fault tolerance by deploying physically isolated primary and standby compute replicas across different availability zones within the same Azure region. This zone-level separation ensures that your database remains resilient to infrastructure failures, such as zone outages, and enabling automatic failover to the standby replica when needed.

The high-availability feature enhances reliability and fault tolerance by deploying physically isolated primary and standby compute replicas across different availability zones within the same Azure region. This zone-level separation ensures that your database remains resilient to infrastructure failures, such as zone outages. When you enable high availability, you also enable automatic failover to the standby replica.

## Steps to enable high availability on an existing cluster

You can enable high availability on an existing Azure HorizonDB cluster at any time. Enabling high availability creates a standby compute replica that mirrors your primary replica.

### [Portal](#tab/portal-enable-high-availability-existing-cluster)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **High availability**.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-disabled.png" alt-text="Screenshot showing the High availability page with high availability disabled." lightbox="media/how-to-configure-high-availability/high-availability-disabled.png":::

1. From the two options, this is what each option represents:

   - **Disabled** - High availability isn't configured.
   - **Zone redundant - Replica in a different availability zone** - A standby compute replica is provisioned in a different availability zone.

1. Select the **Zone redundant - Replica in a different availability zone** option to enable high availability.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enable-save.png" alt-text="Screenshot showing the High availability page with high availability set to Zone redundant and ready to select Save." lightbox="media/how-to-configure-high-availability/high-availability-enable-save.png":::

1. Select **Save** to enable high availability. A notification informs you that the service is enabling high availability.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-notification-enabling.png" alt-text="Screenshot showing the High availability page with high availability set to Zone redundant and the norification that informs the service is enabling high availability." lightbox="media/how-to-configure-high-availability/high-availability-notification-enabling.png":::

1. When the process completes, a notification informs you that the service enabled high availability, and the standby replica is included in the list.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-notification-enabled.png" alt-text="Screenshot showing the High availability page with high availability set to Zone redundant and the norification that informs the service enabled high availability." lightbox="media/how-to-configure-high-availability/high-availability-notification-enabled.png":::

> [!NOTE]
> You can't set or change the name of the standby replica deployed to provide high availability. The portal assigns the name for you. The name consists of \<cluster-name\>-replica-1-YYYYMMDDHHmmss.

### [CLI](#tab/cli-enable-high-availability-existing-cluster)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to enable high availability by adding a new standby replica.

```azurecli-interactive
az rest --method PUT \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{cluster}/pools/DefaultPool/replicas/{replica}?api-version=2026-01-20-preview" \
  --body '{
    "location": "{location}",
    "properties": {
      "role": "Read"
    }
  }'

```

---

## Steps to enable high availability during cluster provisioning

You can configure high availability when you first create your Azure HorizonDB instance. By enabling high availability during provisioning, you deploy a standby replica alongside your primary replica, so you get immediate protection against zone or replica failures.

Using the [Azure portal](https://portal.azure.com/):

1. Select Azure HorizonDB (Preview) service and select **Create**.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-provisioning.png" alt-text="Screenshot that shows the pane for configuring high availability during provisioning." lightbox="media/how-to-configure-high-availability/high-availability-provisioning.png":::

1. Provide your resource group and cluster name and go to **High availability** section.

   You have two high availability mode choices:

   - **Disabled** - High availability isn't configured.
   - **Zone redundant - Replica in a different availability zone** - a stand-by compute replica is provisioned in a different availability zone.

1. Select the **Zone redundant - Replica in a different availability zone** option.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot that shows the pane for configuring high availability." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::

1. When you're done configuring the settings, select **Review + create** to review the changes then select **create**.

1. A deployment starts. Deployment begins. After completion, a notification confirms that the HorizonDB cluster has been successfully created with high availability enabled.


## Steps to disable high availability on an existing cluster

You can disable high availability on an existing Azure HorizonDB cluster at any time. Disabling high availability basically consists on deleting all existing read only replicas that mirror your primary replica.

### [Portal](#tab/portal-disable-high-availability-existing-cluster)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **High availability**.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-enabled.png" alt-text="Screenshot showing the High availability page with high availability enabled." lightbox="media/how-to-configure-high-availability/high-availability-enabled.png":::

1. From the two options, this is what each option represents:

   - **Disabled** - High availability isn't configured.
   - **Zone redundant - Replica in a different availability zone** - A standby compute replica is provisioned in a different availability zone.

1. Select the **Disabled** option to disable high availability.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-disable-save.png" alt-text="Screenshot showing the High availability page with high availability set to Disable and ready to select Save." lightbox="media/how-to-configure-high-availability/high-availability-disable-save.png":::

1. Select **Save** to disable high availability. A notification informs you that the service is disabling high availability.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-notification-disabling.png" alt-text="Screenshot showing the High availability page with high availability set to Disable and the norification that informs the service is disabling high availability." lightbox="media/how-to-configure-high-availability/high-availability-notification-disabling.png":::

1. When the process completes, a notification informs you that all read replicas were deleted and high availability is disabled.

   :::image type="content" source="media/how-to-configure-high-availability/high-availability-notification-disabled.png" alt-text="Screenshot showing the High availability page with high availability set to Zone redundant and the norification that informs the service disabled high availability." lightbox="media/how-to-configure-high-availability/high-availability-notification-disabled.png":::

### [CLI](#tab/cli-disable-high-availability-existing-cluster)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to disable high availability by deleting all read replicas.

```azurecli-interactive
subscriptionId="{subscriptionId}"
resourceGroupName="{resourceGroupName}"
cluster="{cluster}"
readReplicas=$(az rest --method GET \
  --uri "https://management.azure.com/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}/providers/Microsoft.HorizonDB/clusters/$cluster/pools/DefaultPool/replicas?api-version=2026-01-20-preview" \
  --query "value[?properties.role=='Read'].name" \
  --output tsv
)
for replica in $readReplicas; do
  az rest --method DELETE \
    --uri "https://management.azure.com/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}/providers/Microsoft.HorizonDB/clusters/$cluster/pools/DefaultPool/replicas/${replica}?api-version=2026-01-20-preview" 
```

---

## Related content

- [Overview of business continuity in Azure HorizonDB (Preview)](../backup-restore/concepts-business-continuity.md)
- [Backups in Azure HorizonDB (Preview)](../backup-restore/concepts-backup-restore.md)
