---
title: Delete Firewall Rules in Azure HorizonDB
description: This article describes how to delete firewall rules in Azure HorizonDB.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
# customer intent: As a user, I want to learn how to delete firewall rules in Azure HorizonDB.
---

# Delete firewall rules in Azure HorizonDB

When you enable public access, you can set up firewall rules that allow connections from specific IP addresses or from any Azure service.

## [Portal](#tab/portal-delete-firewall-rules)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure HorizonDB.

1. In the resource menu, select **Networking**.

   :::image type="content" source="media/how-to-networking/public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page." lightbox="media/how-to-networking/public-access-networking-enabled-existing-firewall-rules.png":::

1. To delete a firewall rule, select the trash bin icon located to the right of the rule definition.

1. To delete the firewall rule that allows connections from any IP address allocated to any Azure service or asset, clear the **Allow public access from any Azure service within Azure to this server** checkbox.

> [!IMPORTANT]  
> **Allow public access from any Azure service within Azure to this server** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of this rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

1. Select **Save**.

1. A notification informs you that the changes are being applied.

1. The status of the server changes to **Updating**.

1. When the process completes, a notification informs you that the changes were applied.

1. The status of the server changes to **Ready**.

<!--

## [CLI](#tab/CLI-delete-firewall-rules)

To delete firewall rules from a server, use the [az postgres flexible-server firewall-rule delete](/CLI/azure/postgres/flexible-server/firewall-rule#az-postgres-flexible-server-firewall-rule-delete) command.

```azurecli-interactive
az postgres flexible-server firewall-rule delete \
  --resource-group <resource_group> \
  --name <server> \
  --rule-name <rule>
```
-->

If you try to delete a firewall rule on a server that isn't in the `Ready` state, you receive an error like this:

```output
Code: InternalServerError
Message: An unexpected error occured while processing the request. Tracking ID: '<tracking_id>'
```

> [!NOTE]  
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-`, and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you try to delete a firewall rule with an invalid name, you receive an error like this:

```output
The firewall rule name can only contain 0-9, a-z, A-Z, '-' and '_'. Additionally, the name of the firewall rule must be at least 3 characters and no more than 128 characters in length.
```

If you try to remove a firewall rule from a server that doesn't have public access enabled, you receive an error like this:

```output
Firewall rule operations cannot be requested for a private access enabled server.
```

---

## Related content

- [Networking in Azure HorizonDB](how-to-networking.md)
- [Enable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-enable-public-access.md)
- [Disable public access in Azure HorizonDB](how-to-networking-servers-deployed-public-access-disable-public-access.md)
- [Add firewall rules in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-firewall-rules.md)
- [Add private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-add-private-endpoint.md)
- [Delete private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md)
- [Approve private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md)
- [Reject private endpoint connections in Azure HorizonDB](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md)
