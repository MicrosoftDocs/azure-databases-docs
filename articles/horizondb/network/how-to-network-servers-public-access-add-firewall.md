---
title: Add Firewall Rules in Azure HorizonDB
description: This article describes how to add firewall rules in Azure HorizonDB.
author: milenak
ms.author: mpopovic
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
ms.custom:
  - build-2026-public-preview
---

# Add firewall rules in Azure HorizonDB

When you enable public access, you can set up firewall rules that allow connections from specific IP addresses or from any Azure service.

## Add firewall rules using the Azure portal

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, select **Networking**.

   :::image type="content" source="media/how-to-network-servers-public-access-add-firewall/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="media/how-to-network-servers-public-access-add-firewall/public-access-networking-enabled.png":::

1. To create a firewall rule that allows connections from the public IP address of the client machine you're using to connect to the portal, select **Add current client IP address (###.###.###.###)**.

1. Add a new firewall rule to the grid. Portal automatically generates the value of your firewall rule name, which you can change to any valid name of your preference. **Start IP address** and **End IP address** are both set to the public IP address from which you're connecting to the Azure portal.

1. To create a firewall rule that allows connections from any IP address allocated to any Azure service or asset, select **Allow public access from any Azure service within Azure to this cluster**.

   > [!IMPORTANT]  
   > **Allow public access from any Azure service within Azure to this cluster** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of this rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

1. Select **Save**.

1. A notification informs you that the changes are being applied.

1. When the process completes, a notification informs you that the changes were applied.

> [!NOTE]  
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-`, and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you try to add a firewall rule with an invalid name, you receive an error like this:

```output
The firewall rule name can only contain 0-9, a-z, A-Z, '-' and '_'. Additionally, the name of the firewall rule must be at least 3 characters and no more than 128 characters in length.
```

If you try to add a firewall rule with a name that matches the name of another existing firewall rule, you don't receive an error, but the rule is updated with the values you provide for `--start-ip-address` and `--end-ip-address`.

If you pass an invalid IP address for the `--start-ip-address` and `--end-ip-address` parameters, you receive an error like this:

```output
Incorrect value for ip address. Ip address should be IPv4 format. Example: 12.12.12.12.
```

If you pass a value for `--start-ip-address` that's bigger than the value you pass for `--end-ip-address`, you receive an error like this:

```output
The end IP address is smaller than the start IP address.
```

If you try to add a firewall rule to a server that doesn't have public access enabled, you receive an error like this:

```output
Firewall rule operations cannot be requested for a private access enabled server.
```

> [!NOTE]  
> Although not recommended, you can create multiple firewall rules with different names and either overlapping IP ranges or even matching start and end IP addresses.

To allow public access from any Azure service within Azure to your server, you must create a firewall rule whose start and end IP addresses are both set to `0.0.0.0`.

> [!IMPORTANT]  
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

---

## Related content

- [Networking in Azure HorizonDB](how-to-network.md)
- [Delete firewall rules in Azure HorizonDB](how-to-network-servers-public-access-delete-firewall.md)
