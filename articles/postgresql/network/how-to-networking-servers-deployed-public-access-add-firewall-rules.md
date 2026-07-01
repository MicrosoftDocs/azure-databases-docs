---
title: Add firewall rules
description: This article describes how to add firewall rules to an Azure Database for PostgreSQL flexible server.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 06/09/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
#customer intent: As a user, I want to learn how to add firewall rules to an Azure Database for PostgreSQL.
---

# Add firewall rules

When you enable public access, set up firewall rules that allow connections from specific IP addresses or from any Azure service.

## [Portal](#tab/portal-add-firewall-rules)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, under the **Settings** section, select **Networking**.

    :::image type="content" source="./media/how-to-networking/public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/public-access-networking-enabled.png":::

1. To create a firewall rule that allows connections from the public IP address of the client machine you're using to connect to the portal, select **Add current client IP address (###.###.###.###)**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-current-client.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/add-firewall-rule-current-client.png":::

1. Add a new firewall rule to the grid. The portal automatically generates the **Firewall rule name**, but you can change it to any valid name you prefer. Set the **Start IP address** and **End IP address** to the public IP address from which you're connected to the Azure portal.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client.png" alt-text="Screenshot showing a new rule added to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/added-firewall-rule-current-client.png":::

1. To create a firewall rule that allows connections from any public IP address, select **Add 0.0.0.0 / 255.255.255.255**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-all-addresses.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from all public IP addresses." lightbox="./media/how-to-networking/add-firewall-rule-all-addresses.png":::

1. To create a firewall rule that allows connections from any IP address allocated to any Azure service or asset, select **Allow public access from any Azure service within Azure to this server**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-any-azure-service.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from any Azure service." lightbox="./media/how-to-networking/add-firewall-rule-any-azure-service.png":::

    > [!IMPORTANT]
    > **Allow public access from any Azure service within Azure to this server** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of this rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.
    
1. Select **Save**.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/added-firewall-rule-current-client-save.png":::

1. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/added-firewall-rule-current-client-progressing-notification.png":::

1. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/added-firewall-rule-current-client-succeeded-notification.png":::

## [CLI](#tab/cli-add-firewall-rules)

Use the [az postgres flexible-server firewall-rule create](/cli/azure/postgres/flexible-server/firewall-rule#az-postgres-flexible-server-firewall-rule-create) command to add firewall rules to a server.

```azurecli-interactive
az postgres flexible-server firewall-rule create \
  --resource-group <resource_group> \
  --server-name <server> \
  --name <rule> \
  --start-ip-address <start_ip_address> \
  --end-ip-address <end_ip_address>
```

If you try to add a firewall rule on a server that isn't in the `Ready` state, you get an error like this:

```output
Code: InternalServerError
Message: An unexpected error occured while processing the request. Tracking ID: '<tracking_id>'
```

> [!NOTE]
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-`, and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you try to add a firewall rule with an invalid name, you get an error like this:

```output
The firewall rule name can only contain 0-9, a-z, A-Z, '-' and '_'. Additionally, the name of the firewall rule must be at least 3 characters and no more than 128 characters in length. 
```

If you try to add a firewall rule with a name that matches the name of another existing firewall rule, you don't get an error, but the rule is updated with the values you provide for `--start-ip-address` and `--end-ip-address`.

If you pass an invalid IP address for the `--start-ip-address` and `--end-ip-address` parameters, you get an error like this:

```output
Incorrect value for ip address. Ip address should be IPv4 format. Example: 12.12.12.12.
```

If you pass a value for `--start-ip-address` that's bigger than the value you pass for `--end-ip-address`, you get an error like this:

```output
The end IP address is smaller than the start IP address.
```

If you try to add a firewall rule to a server that doesn't have public access enabled, you get an error like this:

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

- [Networking](how-to-networking.md).
- [Enable or disable public access](how-to-networking-servers-deployed-public-access-enable-disable-public-access.md).
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md).
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md).
- [Delete private endpoint connections](how-to-networking-servers-deployed-public-access-delete-private-endpoint.md).
- [Approve private endpoint connections](how-to-networking-servers-deployed-public-access-approve-private-endpoint.md).
- [Reject private endpoint connections](how-to-networking-servers-deployed-public-access-reject-private-endpoint.md).
