---
title: Add firewall rules
description: This article describes how to add firewall rules to an Azure Database for PostgreSQL flexible server.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 03/30/2025
ms.service: azure-database-postgresql
ms.topic: how-to
#customer intent: As a user, I want to learn how to add firewall rules to an Azure Database for PostgreSQL.
---

# Add firewall rules

With public access enabled, you can configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service.

## [Portal](#tab/portal-add-firewall-rules)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

2. In the resource menu, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-enabled.png":::

3. If you want to create a firewall rule to allow connections originating from the public IP address of the client machine that you're using to connect to navigate the portal, select **Add current client IP address (###.###.###.###)**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-current-client.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/add-firewall-rule-current-client.png":::

4. A new firewall rule is added to the grid. Its **Firewall rule name** is automatically generated, but you can change it to any valid name of your preference. **Start IP address** and **End IP address** are set to the public IP address from which you're connected to the Azure portal.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client.png" alt-text="Screenshot showing a new rule added to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/added-firewall-rule-current-client.png":::

5. If you want to create a firewall rule to allow connections originating from any public IP address, select **Add 0.0.0.0 / 255.255.255.255**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-all-addresses.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from all public IP addresses." lightbox="./media/how-to-networking/add-firewall-rule-all-addresses.png":::

6. If you want to create a firewall rule to allow connections originating from any IP address allocated to any Azure service or asset, select **Allow public access from any Azure service within Azure to this server**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-any-azure-service.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from any Azure service." lightbox="./media/how-to-networking/add-firewall-rule-any-azure-service.png":::

> [!IMPORTANT]
> **Allow public access from any Azure service within Azure to this server** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of such rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

7. Select **Save**.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/added-firewall-rule-current-client-save.png":::

8. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/added-firewall-rule-current-client-progressing-notification.png":::

9. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/public-access-updating.png":::

10. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/added-firewall-rule-current-client-succeeded-notification.png":::

11. Also, the status of the server changes to **Ready**.

    :::image type="content" source="./media/how-to-networking/public-access-available.png" alt-text="Screenshot showing that server status is Ready." lightbox="./media/how-to-networking/public-access-available.png":::

## [CLI](#tab/cli-add-firewall-rules)

You can add firewall rules to a server via the [az postgres flexible-server firewall-rule create](/cli/azure/postgres/flexible-server/firewall-rule#az-postgres-flexible-server-firewall-rule-create) command.

```azurecli-interactive
az postgres flexible-server firewall-rule create \
  --resource-group <resource_group> \
  --name <server> \
  --rule-name <rule> \
  --start-ip-address <start_ip_address> \
  --end-ip-address <end_ip_address>
```

If you attempt to add a firewall rule on a server which isn't in `Ready` state, you receive an error like this:

```output
Code: InternalServerError
Message: An unexpected error occured while processing the request. Tracking ID: '<tracking_id>'
```

> [!NOTE]
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-`, and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you attempt to add a firewall rule with an invalid name, you receive an error like this:

```output
The firewall rule name can only contain 0-9, a-z, A-Z, '-' and '_'. Additionally, the name of the firewall rule must be at least 3 characters and no more than 128 characters in length. 
```

If you attempt to add a firewall rule with a name that matches the name of another existing firewall rule, you don't receive an error, but the rule is updated with the values provided for `--start-ip-address` and `--end-ip-address`.

If you pass an invalid IP address for the `--start-ip-address` and `--end-ip-address` parameters, you receive an error like this:

```output
Incorrect value for ip address. Ip address should be IPv4 format. Example: 12.12.12.12.
```

If you pass a value for `--start-ip-address` which is bigger than the value passed `--end-ip-address`, you receive an error like this:

```output
The end IP address is smaller than the start IP address.
```

If you attempt to add a firewall rule to a server that doesn't have public access enabled, you receive an error like this:

```output
Firewall rule operations cannot be requested for a private access enabled server.
```

> [!NOTE]
> Although not recommended, you can create multiple firewall rules with different names and either overlapping IP ranges, or even matching start and end IP addresses.

To allow public access, from any Azure service within Azure, to your server, you must create a firewall rule whose start and end IP addresses are both set to `0.0.0.0`.

> [!IMPORTANT]
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

---

## Related content

- [Networking](how-to-networking.md).
- [Enable public access](how-to-networking-servers-deployed-public-access-enable-public-access.md).
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
