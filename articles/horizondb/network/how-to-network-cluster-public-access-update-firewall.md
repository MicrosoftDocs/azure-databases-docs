---
title: Update firewall rules in Azure HorizonDB
description: This article describes how to update existing firewall rules in Azure HorizonDB.
#customer intent: As a user, I want to update existing firewall rules in Azure HorizonDB, so that I can change rule names or IP ranges without recreating all networking settings.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-horizondb
ms.subservice: networking
ms.topic: how-to
---

# Update firewall rules in Azure HorizonDB (preview)

When you enable public access and create firewall rules, you can update them to change the rule name, start IP address, end IP address, or description.

## Steps to update firewall rules

### [Portal](#tab/portal-update-firewall-rules)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **Networking**.

   :::image type="content" source="media/how-to-cluster-public-access-update-firewall/public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page from where you can view and edit firewall rules." lightbox="media/how-to-cluster-public-access-update-firewall/public-access-networking-enabled-existing-firewall-rules.png":::

1. In the firewall rules grid, find the existing rule that you want to update. Update any of the following values based on your needs: **Firewall rule name**, **Start IP address**, and **End IP address**.

   :::image type="content" source="media/how-to-cluster-public-access-update-firewall/public-access-networking-other-ip-firewall-rule.png" alt-text="Screenshot showing the Networking page with an existing firewall rule selected and start and end IP addresses modified." lightbox="media/how-to-cluster-public-access-update-firewall/public-access-networking-other-ip-firewall-rule.png":::

   > [!IMPORTANT]
   > Because the backend doesn't support updating the name of an existing firewall rule, the portal implements this update as the creation of a new rule with the new name, and then deletion of the existing rule with the old name.

1. Select **Save** when you're done configuring firewall rules. A notification informs you that the changes are being applied.

   :::image type="content" source="media/how-to-cluster-public-access-update-firewall/public-access-networking-firewall-rule-in-progress.png" alt-text="Screenshot showing the notification informing that the update of connection security settings is in progress." lightbox="media/how-to-cluster-public-access-update-firewall/public-access-networking-firewall-rule-in-progress.png":::

1. When the process completes, a notification informs you that the changes were applied.

   :::image type="content" source="media/how-to-cluster-public-access-update-firewall/public-access-networking-firewall-rule-completed.png" alt-text="Screenshot showing the notification informing that the update of connection security settings completed." lightbox="media/how-to-cluster-public-access-update-firewall/public-access-networking-firewall-rule-completed.png":::

> [!NOTE]  
> Although not recommended, you can create multiple firewall rules with different names and either overlapping IP ranges or even matching start and end IP addresses.

> [!IMPORTANT]  
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

### [CLI](#tab/cli-update-firewall-rules)

Use the [az horizondb firewall-rule update](/cli/azure/horizondb/firewall-rule?view=azure-cli-latest#az-horizondb-firewall-rule-update) command to update a firewall rule in your Azure HorizonDB cluster.

```azurecli-interactive
az horizondb firewall-rule update \
  --resource-group <resource_group> \
  --cluster-name <cluster> \
  --name <firewall_rule> \
  --start-ip-address <updated_start_ip_address> \
  --end-ip-address <updated_end_ip_address> \
  --description <updated_description>
```

To update the name of an existing firewall rule by using CLI, you must [delete the existing firewall rule](./how-to-network-cluster-public-access-delete-firewall.md?tabs=cli-delete-firewall-rules), and [create a new firewall rule](./how-to-network-cluster-public-access-add-firewall.md?tabs=cli-add-firewall-rules.md) with all identical properties but with the new name.

---

## Related content

- [Networking in Azure HorizonDB (Preview)](how-to-network.md)
- [Add firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-update-firewall.md)
- [Delete firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-delete-firewall.md)
