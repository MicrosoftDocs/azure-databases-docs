---
title: Delete firewall rules
description: This article describes how to delete firewall rules to an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to delete firewall rules to an Azure Database for PostgreSQL flexible server.
---

# Delete firewall rules

With public access enabled, you can configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service.

## [Portal](#tab/portal-delete-firewall-rules)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Overview**.

    :::image type="content" source="./media/how-to-networking/networking-overview.png" alt-text="Screenshot showing the Overview page." lightbox="./media/how-to-networking/networking-overview.png":::

3. The status of the server must be **Available**, for the **Networking** menu option to be enabled.

    :::image type="content" source="./media/how-to-networking/networking-server-status.png" alt-text="Screenshot showing where in the Overview page you can find the status of the server." lightbox="./media/how-to-networking/networking-server-status.png":::

4. If the status of the server isn't **Available**, the **Networking** option is disabled.

    :::image type="content" source="./media/how-to-networking/networking-disabled.png" alt-text="Screenshot showing that Networking menu is disabled when status of server isn't Available." lightbox="./media/how-to-networking/networking-disabled.png":::

> [!NOTE]
> Any attempt to configure the networking settings of a server whose status is other than available, would fail with an error.

5. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-enabled-existing-firewall-rules.png":::

6. If you want to delete a firewall rule, select the icon that resembles a trash bin, which is located to the right of the rule definition.

    :::image type="content" source="./media/how-to-networking/delete-firewall-rule-current-client.png" alt-text="Screenshot showing how to delete the firewall rule that you created to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/delete-firewall-rule-current-client.png":::

7. If you want to delete the firewall rule that allows connections originating from any IP address allocated to any Azure service or asset, clear the **Allow public access from any Azure service within Azure to this server** checkbox.

    :::image type="content" source="./media/how-to-networking/delete-firewall-rule-any-azure-service.png" alt-text="Screenshot showing how to delete the firewall rule to allow connections from any Azure service." lightbox="./media/how-to-networking/delete-firewall-rule-any-azure-service.png":::

> [!IMPORTANT]
> **Allow public access from any Azure service within Azure to this server** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of such rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

8. Select **Save**.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-save.png":::

9. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-progressing-notification.png":::

10. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/public-access-updating.png":::

11. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-succeeded-notification.png":::

12. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/public-access-available.png":::

## [CLI](#tab/cli-delete-firewall-rules)

You can delete firewall rules from a server via the [az postgres flexible-server firewall-rule delete](/cli/azure/postgres/flexible-server/firewall-rule#az-postgres-flexible-server-firewall-rule-delete) command.

```azurecli-interactive
az postgres flexible-server firewall-rule delete --resource-group <resource_group> --name <server> --rule-name <rule>
```

If you attempt to delete a firewall rule on a server which isn't in `Available` state, you receive an error like this:

```output
Code: InternalServerError
Message: An unexpected error occured while processing the request. Tracking ID: '<tracking_id>'
```

> [!NOTE]
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-`, and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you attempt to delete a firewall rule with an invalid name, you receive an error like this:

```output
The firewall rule name can only contain 0-9, a-z, A-Z, '-' and '_'. Additionally, the name of the firewall rule must be at least 3 characters and no more than 128 characters in length. 
```

If you attempt to remove a firewall rule from a server that doesn't have public access enabled, you receive an error like this:

```output
Firewall rule operations cannot be requested for a private access enabled server.
```

---

## Related content

- [Networking](how-to-networking.md).
- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
