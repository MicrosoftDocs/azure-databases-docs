---
title: Delete firewall rules in Azure Database for PostgreSQL Flexible Server
description: This article describes how to delete firewall rules to an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to delete firewall rules in Azure Database for PostgreSQL flexible server, so that I can remove access for IP addresses that no longer need to connect.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
---

# Delete firewall rules in Azure Database for PostgreSQL flexible server

When you enable public access, you can set up firewall rules that allow connections from specific IP addresses or from any Azure service.

## [Portal](#tab/portal-delete-firewall-rules)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-enabled-existing-firewall-rules.png":::

1. To delete a firewall rule, select the trash bin icon located to the right of the rule definition.

    :::image type="content" source="./media/how-to-networking/delete-firewall-rule-current-client.png" alt-text="Screenshot showing how to delete the firewall rule that you created to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/delete-firewall-rule-current-client.png":::

1. To delete the firewall rule that allows connections from any IP address allocated to any Azure service or asset, clear the **Allow public access from any Azure service within Azure to this server** checkbox.

    :::image type="content" source="./media/how-to-networking/delete-firewall-rule-any-azure-service.png" alt-text="Screenshot showing how to delete the firewall rule to allow connections from any Azure service." lightbox="./media/how-to-networking/delete-firewall-rule-any-azure-service.png":::

    > [!IMPORTANT]
    > **Allow public access from any Azure service within Azure to this server** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of this rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.
    
1. Select **Save**.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-save.png":::

1. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-progressing-notification.png":::

1. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-succeeded-notification.png":::

## [CLI](#tab/cli-delete-firewall-rules)

You can delete firewall rules from a server by using the [az postgres flexible-server firewall-rule delete](/cli/azure/postgres/flexible-server/firewall-rule#az-postgres-flexible-server-firewall-rule-delete) command.

```azurecli-interactive
az postgres flexible-server firewall-rule delete \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <rule>
```

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

- [Networking](how-to-networking.md).
- [Enable or disable public access](how-to-networking-servers-deployed-public-access-enable-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
