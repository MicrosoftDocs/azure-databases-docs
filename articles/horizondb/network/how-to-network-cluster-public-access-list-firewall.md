---
title: List firewall rules in Azure HorizonDB
description: This article describes how to list existing firewall rules in Azure HorizonDB.
#customer intent: As a user, I want to list the existing firewall rules in Azure HorizonDB, so that I can review the IP addresses and ranges that can connect to my cluster.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-horizondb
ms.subservice: networking
ms.topic: how-to
---

# List firewall rules in Azure HorizonDB (preview)

When you enable public access, you can view the existing firewall rules configured for your Azure HorizonDB cluster.

## Steps to list firewall rules

### [Portal](#tab/portal-list-firewall-rules)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **Networking**. In the firewall rules grid, review the existing rules. For each rule, the portal shows the following information: **Firewall rule name**, **Start IP address**, and **End IP address**.

   :::image type="content" source="media/how-to-cluster-public-access-list-firewall/public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page with existing firewall rules listed." lightbox="media/how-to-cluster-public-access-list-firewall/public-access-networking-enabled-existing-firewall-rules.png":::

> [!NOTE]
> You can have multiple firewall rules with different names, including rules with overlapping IP ranges.

> [!IMPORTANT]  
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

### [CLI](#tab/cli-list-firewall-rules)

Use the [az horizondb firewall-rule list](/cli/azure/horizondb/firewall-rule?view=azure-cli-latest#az-horizondb-firewall-rule-list) command to list all firewall rules for your Azure HorizonDB cluster.

```azurecli-interactive
az horizondb firewall-rule list \
  --resource-group <resource_group> \
  --cluster-name <cluster> \
```

Use the [az horizondb firewall-rule show](/cli/azure/horizondb/firewall-rule?view=azure-cli-latest#az-horizondb-firewall-rule-show) command to show details for one firewall rule in your Azure HorizonDB cluster.

```azurecli-interactive
az horizondb firewall-rule show \
  --resource-group <resource_group> \
  --cluster-name <cluster> \
  --name <firewall_rule>
```

---

## Related content

- [Networking in Azure HorizonDB (Preview)](how-to-network.md)
- [Add firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-add-firewall.md)
- [Update firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-update-firewall.md)
- [Delete firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-delete-firewall.md)
