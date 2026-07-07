---
title: Delete Firewall Rules in Azure HorizonDB
description: This article describes how to delete firewall rules in Azure HorizonDB.
#customer intent: As a user, I want to delete a firewall rule in Azure HorizonDB, so that I can remove access for IP addresses that no longer need to connect to my cluster.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: networking
ms.topic: how-to
---

# Delete firewall rules in Azure HorizonDB (Preview)

When you enable public access, you can set up firewall rules that allow connections from specific IP addresses or from any Azure service.

## Steps to delete firewall rules

### [Portal](#tab/portal-delete-firewall-rules)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **Networking**.

   :::image type="content" source="media/how-to-cluster-public-access-delete-firewall/public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page from where you can add or remove firewall rules." lightbox="media/how-to-cluster-public-access-delete-firewall/public-access-networking-enabled-existing-firewall-rules.png":::

1. To delete a firewall rule, select the trash bin icon located to the right of the rule definition so that the rule definition disappears from the grid.

   :::image type="content" source="media/how-to-cluster-public-access-delete-firewall/public-access-networking-enabled-no-firewall-rules.png" alt-text="Screenshot showing the Networking page with the firewall rule removed from the grid." lightbox="media/how-to-cluster-public-access-delete-firewall/public-access-networking-enabled-no-firewall-rules.png":::

1. To delete the firewall rule that allows connections from any IP address allocated to any Azure service or asset, clear the **Allow public access from any Azure service within Azure to this cluster** checkbox.

   :::image type="content" source="media/how-to-cluster-public-access-delete-firewall/public-access-networking-enabled-no-azure-firewall-rules.png" alt-text="Screenshot showing the Networking page with the Allow public access from any Azure service within Azure to this cluster clear." lightbox="media/how-to-cluster-public-access-delete-firewall/public-access-networking-enabled-no-azure-firewall-rules.png":::

   > [!IMPORTANT]  
   > **Allow public access from any Azure service within Azure to this cluster** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of this rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

1. Select **Save** when you're done configuring firewall rules. A notification informs you that the changes are being applied.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-in-progress.png" alt-text="Screenshot showing the notification informing that the update of connection security settings is in progress." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-in-progress.png":::

1. When the process completes, a notification informs you that the changes were applied.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-completed.png" alt-text="Screenshot showing the notification informing that the update of connection security settings completed." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-completed.png":::

### [CLI](#tab/cli-delete-firewall-rules)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

Use the `az rest` command to delete a firewall rule from your Azure HorizonDB cluster.

```azurecli-interactive
az rest --method DELETE \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HorizonDB/clusters/{cluster}/pools/DefaultPool/firewallRules/{firewallRule}?api-version=2026-01-20-preview"

```

---

## Related content

- [Networking in Azure HorizonDB (Preview)](how-to-network.md)
- [Add firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-add-firewall.md)
