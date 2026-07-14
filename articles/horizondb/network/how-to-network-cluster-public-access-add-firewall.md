---
title: Add Firewall Rules in Azure HorizonDB
description: This article describes how to add firewall rules in Azure HorizonDB.
#customer intent: As a user, I want to add firewall rules in Azure HorizonDB, so that I can control which IP addresses can connect to my database.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 07/07/2026
ms.service: azure-horizondb
ms.subservice: networking
ms.topic: how-to
---

# Add firewall rules in Azure HorizonDB (Preview)

When you enable public access, set up firewall rules that allow connections from specific IP addresses, ranges of addresses, or from any Azure service.

## Steps to add firewall rules

### [Portal](#tab/portal-add-firewall-rules)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB cluster.

1. In the resource menu, under the **Settings** section, select **Networking**.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page from where you can add or remove firewall rules." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-enabled.png":::

1. To create a firewall rule that allows connections from the public IP address of the client machine you're using to connect to the portal, select **Add current client IP address (###.###.###.###)**. That action adds a new firewall rule to the grid, for which the portal generates the value of the firewall rule name and the IP addresses. You can change any of the three values to any other value of your preference.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-client-ip-firewall-rule.png" alt-text="Screenshot showing the Networking page with everything prepared to create a firewall rule for your client IP address." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-client-ip-firewall-rule.png":::

1.  If you want to add a firewall rule for a different IP address or IP address ranges, on the first empty row of the grid, under **Firewall rule name** set a valid name for the firewall rule. Under **Start IP address** and **End IP address**, set the public IP address (or addresses that define a range of IP addresses) from which you or your applications are connecting to your Azure HorizonDB cluster replicas.

      :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-other-ip-firewall-rule.png" alt-text="Screenshot showing the Networking page with everything prepared to create a firewall rule for your applications range of IP addresses." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-other-ip-firewall-rule.png":::
    
1. To create a firewall rule that allows connections from any IP address allocated to any Azure service or asset, select **Allow public access from any Azure service within Azure to this cluster**.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-azure-ip-firewall-rule.png" alt-text="Screenshot showing the Networking page with everything prepared to create a firewall rule to allow any Azure service to connect via a public IP address to this cluster." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-azure-ip-firewall-rule.png":::

   > [!IMPORTANT]  
   > **Allow public access from any Azure service within Azure to this cluster** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of this rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

1. Select **Save** when you're done configuring firewall rules. A notification informs you that the changes are being applied.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-in-progress.png" alt-text="Screenshot showing the notification informing that the update of connection security settings is in progress." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-in-progress.png":::

1. When the process completes, a notification informs you that the changes were applied.

   :::image type="content" source="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-completed.png" alt-text="Screenshot showing the notification informing that the update of connection security settings completed." lightbox="media/how-to-cluster-public-access-add-firewall/public-access-networking-firewall-rule-completed.png":::

> [!NOTE]  
> Although not recommended, you can create multiple firewall rules with different names and either overlapping IP ranges or even matching start and end IP addresses.

> [!IMPORTANT]  
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

### [CLI](#tab/cli-add-firewall-rules)

Use the [az horizondb firewall-rule create](/cli/azure/horizondb/firewall-rule?view=azure-cli-latest#az-horizondb-firewall-rule-create) command to add a firewall rule to your Azure HorizonDB cluster.

To create a firewall rule that allows a single IP address:  

```azurecli-interactive
az horizondb firewall-rule create \
  --resource-group <resource_group> \
  --cluster-name <cluster> \
  --name <firewall_rule> \
  --start-ip-address <start_ip_address> \
  --description <description>
```

To create a firewall rule that allows a range of IP addresses:  

```azurecli-interactive
az horizondb firewall-rule create \
  --resource-group <resource_group> \
  --cluster-name <cluster> \
  --name <firewall_rule> \
  --start-ip-address <start_ip_address> \
  --end-ip-address <end_ip_address> \
  --description <description>
```

To create a firewall rule that allows public access from any Azure service within Azure:  

```azurecli-interactive
az horizondb firewall-rule create \
  --resource-group <resource_group> \
  --cluster-name <cluster> \
  --name <firewall_rule> \
  --start-ip-address 0.0.0.0 \
  --description <description>
```

---

## Related content

- [Networking in Azure HorizonDB (Preview)](how-to-network.md)
- [Delete firewall rules in Azure HorizonDB (Preview)](how-to-network-cluster-public-access-delete-firewall.md)
