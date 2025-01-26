---
title: Configure networking
description: This article describes how to configure networking related settings of an Azure Database for PostgreSQL flexible server.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/26/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
#customer intent: As a user, I want to learn how to configure network related settings of an Azure Database for PostgreSQL flexible server.
---

# Configure networking

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

When you deploy your Azure Database for PostgreSQL flexible server, you can choose between configuring its networking mode as **Public access (allowed IP addresses)** or as **Private access (VNET Integration)**. For more information about these options, see [Networking with public access (allowed IP addresses)](concepts-networking-public.md) and [Networking with private access (VNET integration)](concepts-networking-private.md).

This article provides step-by-step instructions to configure networking related settings of an Azure Database for PostgreSQL flexible server, regardless of the networking mode you selected to deploy it.

## Servers deployed with public access

### Enable public access
 
If you enable public access, connectivity to the server is also possible via private endpoints. With public access enabled, you can also configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service. When you enable public access, any firewall rules that already existed last time the server was configured with enabled public access, and that weren't explicitly deleted, are enforced again.

#### [Portal](#tab/portal-enable-public-access)

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

    :::image type="content" source="./media/how-to-networking/configure-public-access-networking-disabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/configure-public-access-networking-disabled.png":::

6. Select the **Allow public access to this resource through the internet using a public IP address** checkbox.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access.png" alt-text="Screenshot showing how to enable public access." lightbox="./media/how-to-networking/configure-public-access-enable-public-access.png":::

7. Select **Save**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-save.png":::

8. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-progressing-notification.png":::

9. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/configure-public-access-updating.png":::

10. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/configure-public-access-enable-public-access-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/configure-public-access-enable-public-access-succeeded-notification.png":::

11. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/configure-public-access-available.png":::

#### [CLI](#tab/cli-enable-public-access)

You can enable public access on a server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --public-access enabled
```

If you attempt to enable public access on a server which isn't in `Available` state, you receive an error like this:

```output
Code: 
Message: Server <server> is busy with other operations. Please try later
```

If you attempt to enable public access on a server which wasn't deployed with networking mode public access (allowed IP addresses), but was deployed with networking mode set to private access (VNET Integration), you don't receive an error. The request to change that configuration is ignored.

To determine if a server has public access enabled or disabled, run the following command:

```azurecli-interactive
az postgres flexible-server show --resource-group <resource_group> --name <server> --query '{"publicAccess":network.publicNetworkAccess}'
```

---

### Disable public access

If you disable public access, connectivity to the server is only possible via private endpoints. You must configure those private endpoints so that hosts that can route traffic to the Azure virtual network in which you inject the private endpoints, can access your Azure Database for PostgreSQL flexible server. When public access is disabled, any firewall rules you created while public access was enabled, aren't enforced. Also, any modifications made to the firewall rules are discarded.

#### [Portal](#tab/portal-disable-public-access)

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

    :::image type="content" source="./media/how-to-networking/configure-public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/configure-public-access-networking-enabled.png":::

6. Clear the **Allow public access to this resource through the internet using a public IP address** checkbox.

    :::image type="content" source="./media/how-to-networking/configure-public-access-disable-public-access.png" alt-text="Screenshot showing how to disable public access." lightbox="./media/how-to-networking/configure-public-access-disable-public-access.png":::

7. Select **Save**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-disable-public-access-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/configure-public-access-disable-public-access-save.png":::

8. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/configure-public-access-disable-public-access-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/configure-public-access-disable-public-access-progressing-notification.png":::

9. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/configure-public-access-updating.png":::

10. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/configure-public-access-disable-public-access-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/configure-public-access-disable-public-access-succeeded-notification.png":::

11. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/configure-public-access-available.png":::

#### [CLI](#tab/cli-disable-public-access)

You can disable public access on a server via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update --resource-group <resource_group> --name <server> --public-access disabled
```

If you attempt to disable public access on a server which isn't in `Available` state, you receive an error like this:

```output
Code: 
Message: Server <server> is busy with other operations. Please try later
```

If you attempt to disable public access on a server which wasn't deployed with networking mode public access (allowed IP addresses), but was deployed with networking mode set to private access (VNET Integration), you don't receive an error. The request to change that configuration is ignored.

To determine if a server has public access disabled or enabled, run the following command:

```azurecli-interactive
az postgres flexible-server show --resource-group <resource_group> --name <server> --query '{"publicAccess":network.publicNetworkAccess}'
```

---

### Add firewall rules

With public access enabled, you can configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service.

#### [Portal](#tab/portal-add-firewall-rules)

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

    :::image type="content" source="./media/how-to-networking/configure-public-access-networking-enabled.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/configure-public-access-networking-enabled.png":::

6. If you want to create a firewall rule to allow connections originating from the public IP address of the client machine that you're using to connect to navigate the portal, select **Add current client IP address (###.###.###.###)**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-current-client.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/add-firewall-rule-current-client.png":::

7. A new firewall rule is added to the grid. Its **Firewall rule name** is automatically generated, but you can change it to any valid name of your preference. **Start IP address** and **End IP address** are set to the public IP address from which you're connnected to the Azure portal.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client.png" alt-text="Screenshot showing a new rule added to allow connections from the IP address of the computer from which you're navigating the Azure portal." lightbox="./media/how-to-networking/added-firewall-rule-current-client.png":::

8. If you want to create a firewall rule to allow connections originating from any public IP address, select **Add 0.0.0.0 / 255.255.255.255**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-all-addresses.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from all public IP addresses." lightbox="./media/how-to-networking/add-firewall-rule-all-addresses.png":::

9. If you want to create a firewall rule to allow connections originating from any IP address allocated to any Azure service or asset, select **Allow public access from any Azure service within Azure to this server**.

    :::image type="content" source="./media/how-to-networking/add-firewall-rule-any-azure-service.png" alt-text="Screenshot showing how to add a firewall rule to allow connections from any Azure service." lightbox="./media/how-to-networking/add-firewall-rule-any-azure-service.png":::

> [!IMPORTANT]
> **Allow public access from any Azure service within Azure to this server** creates a firewall rule whose start and end IP addresses are set to `0.0.0.0`. The presence of such rule configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

10. Select **Save**.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-save.png" alt-text="Screenshot showing the Save button." lightbox="./media/how-to-networking/added-firewall-rule-current-client-save.png":::

11. A notification informs you that the changes are being applied.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-progressing-notification.png" alt-text="Screenshot showing a server whose network settings are being saved." lightbox="./media/how-to-networking/added-firewall-rule-current-client-progressing-notification.png":::

12. Also, the status of the server changes to **Updating**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/configure-public-access-updating.png":::

13. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/added-firewall-rule-current-client-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/added-firewall-rule-current-client-succeeded-notification.png":::

14. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/configure-public-access-available.png":::

#### [CLI](#tab/cli-add-firewall-rules)

You can add firewall rules to a server via the [az postgres flexible-server firewall-rule create](/cli/azure/postgres/flexible-server/firewall-rule#az-postgres-flexible-server-firewall-rule-create) command.

```azurecli-interactive
az postgres flexible-server firewall-rule create --resource-group <resource_group> --name <server> --rule-name <rule> --start-ip-address <start_ip_address> --end-ip-address <end_ip_address>
```

If you attempt to add a firewall rule on a server which isn't in `Available` state, you receive an error like this:

```output
Code: InternalServerError
Message: An unexpected error occured while processing the request. Tracking ID: '<tracking_id>'
```

> [!NOTE]
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-` and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you attempt to add a firewall rule with an invalid name, you receive an error like this:

```output
Code: InvalidParameterValue
Message: Invalid value given for parameter firewallRuleName. Specify a valid parameter value.
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
> Although not recommended, it's supported to create multiple firewall rules with different names and either overlapping IP ranges, or even matching start and end IP addresses.

To allow public access, from any Azure service within Azure, to your server, you must create a firewall rule whose start and end IP addresses are both set to `0.0.0.0`.

> [!IMPORTANT]
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

---

## Servers deployed with private access

### Configure public access

#### [Portal](#tab/portal-restart-server)

## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Reset administrator password of an Azure Database for PostgreSQL flexible server](how-to-reset-admin-password.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
