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
> Although not recommended, it's supported to create multiple firewall rules with different names and either overlapping IP ranges, or even matching start and end IP addresses.

To allow public access, from any Azure service within Azure, to your server, you must create a firewall rule whose start and end IP addresses are both set to `0.0.0.0`.

> [!IMPORTANT]
> When you configure a rule in the firewall with start and end IP addresses set to `0.0.0.0`, it configures the firewall to allow connections from IP addresses allocated to any Azure service or asset, including connections from the subscriptions of other customers.

---

### Delete firewall rules

With public access enabled, you can configure firewall rules to allow connections originating from specific IP addresses, or from any Azure service.

#### [Portal](#tab/portal-delete-firewall-rules)

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

    :::image type="content" source="./media/how-to-networking/configure-public-access-networking-enabled-existing-firewall-rules.png" alt-text="Screenshot showing the Networking page." lightbox="./media/how-to-networking/configure-public-access-networking-enabled-existing-firewall-rules.png":::

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

    :::image type="content" source="./media/how-to-networking/configure-public-access-updating.png" alt-text="Screenshot showing that server status is Updating." lightbox="./media/how-to-networking/configure-public-access-updating.png":::

11. When the process completes, a notification informs you that the changes were applied.

    :::image type="content" source="./media/how-to-networking/deleted-firewall-rule-current-client-succeeded-notification.png" alt-text="Screenshot showing a server whose network settings were successfully saved." lightbox="./media/how-to-networking/deleted-firewall-rule-current-client-succeeded-notification.png":::

12. Also, the status of the server changes to **Available**.

    :::image type="content" source="./media/how-to-networking/configure-public-access-available.png" alt-text="Screenshot showing that server status is Available." lightbox="./media/how-to-networking/configure-public-access-available.png":::

#### [CLI](#tab/cli-delete-firewall-rules)

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
> Firewall rule names can only contain `0`-`9`, `a`-`z`, `A`-`Z`, `-` and `_`. Additionally, the name of the firewall rule must be at least 3 characters, and no more than 128 characters in length.

If you attempt to delete a firewall rule with an invalid name, you receive an error like this:

```output
The firewall rule name can only contain 0-9, a-z, A-Z, '-' and '_'. Additionally, the name of the firewall rule must be at least 3 characters and no more than 128 characters in length. 
```

If you attempt to remove a firewall rule from a server that doesn't have public access enabled, you receive an error like this:

```output
Firewall rule operations cannot be requested for a private access enabled server.
```

---

### Add private endpoints

Azure Database for PostgreSQL - Flexible Server is an Azure Private Link service. Because of that, you can create private endpoints so that your client applications can connect privately and securely to your Azure Database for PostgreSQL flexible server.

A private endpoint to your Azure Database for PostgreSQL flexible server is a network interface that you can inject in a subnet of an Azure virtual network. Any host or service that can route network traffic to that subnet, are able to communicate with your flexible server so that the network traffic doesn't have to traversethe internet. All traffic is sent privately using Microsoft backbone.

For more information about Azure Private Link and Azure Private Endpoint, see [Azure Private Link frequently asked questions](/azure/private-link/private-link-faq).

#### [Portal](#tab/portal-add-private-endpoint)

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

6. If you have the required permissions to deploy a private endpoint, you can create it by selecting **Add private endpoint**.

    :::image type="content" source="./media/how-to-networking/add-private-endpoint.png" alt-text="Screenshot showing how to begin adding a new private endpoint." lightbox="./media/how-to-networking/add-private-endpoint.png":::

> [!NOTE]
> To learn about the necessary permissions to deploy a private endpoint, see [Azure RBAC permissions for Azure Private Link](/azure/private-link/rbac-permissions).

7. In the **Basics** page, fill all the details required. Then, select **Next: Resource**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-basics.png" alt-text="Screenshot showing the Basics page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-basics.png":::

8. Use the following table to understand the meaning of the different fields available in the **Basics** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Subscription** | Select the name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the resource. It automatically selects the subscription in which your server is deployed. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. If you have multiple subscriptions, choose the subscription in which you'd like to be billed for the resource. |
    | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the private endpoint. It can be an existing resource group, or you can select **Create new**, and provide a name in that subscription which is unique among the existing resource group names. It automatically selects the resource group in which your server is deployed. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group. |
    | **Name** | The name that you want to assign to the private endpoint. | A unique name that identifies the private enpoint through which you could connect to your Azure Database for PostgreSQL flexible server. |
    | **Network Interface Name** | The name that you want to assign to the network interface associated to the private endpoint. | A unique name that identifies the network interface associated to the private endpoint. |
    | **Region** | The name of one of the [regions in which you can create private endpoints for Azure Database for PostgreSQL - Flexible Server](/azure/private-link/availability#databases). | The region you select must match that of the virtual network in which you plan to deploy the private endpoint. |


9. In the **Resource** page, fill all the details required. Then, select **Next: Virtual Network**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-resource.png" alt-text="Screenshot showing the Resource page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-resource.png":::

10. Use the following table to understand the meaning of the different fields available in the **Resource** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Resource type** | Automatically set to `Microsoft.DBforPostgreSQL/flexibleServers` | This is automatically chosen for you, and corresponds to the type of resource that an Azure Database for PostgreSQL flexible server is, to the eyes of Azure Private Link. |
    | **Resource** | Automatically set to the name of the Azure Database for PostgreSQL flexible server for which you're creating the private endpoint. | The name of the resource to which the private endpoint will connect to. |
    | **Target sub-resource** | Automatically set to `postgresqlServer`. | The type of sub-resource for the resource selected, that your private endpoint will be able to access. |

11. In the **Virtual Network** page, fill all the details required. Then, select **Next: DNS**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-virtual-network.png" alt-text="Screenshot showing the Virtual Network page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-virtual-network.png":::

12. Use the following table to understand the meaning of the different fields available in the **Virtual Network** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Virtual network** | Automatically set to the first (sorted in alphabetical order) virtual network available in the subscription and region selected. | Only virtual networks on which you have permissions, in the currently selected subscription and region, are listed. |
    | **Subnet** | Automatically set to the name of the Azure Database for PostgreSQL flexible server for which you're creating the private endpoint. | Only subnets in the currently selected virtual network are listed. |
    | **Network policy for private endpoints** | By default, network policies are disabled for a subnet in a virtual network. You can enable network policies either for network security groups only, for user-defined routes only, or for both. | To use network policies like user-defined routes and network security group support, network policy support must be enabled for the subnet. This setting only applies to private endpoints in the subnet and affects all private endpoints in the subnet. For other resources in the subnet, access is controlled based on security rules in the network security group. For more information, see [Manage network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy). |
    | **Private IP configuration** | Automatically set to dynamically allocate one of the available IP addresses in the range assigned to the selected subnet. | This is the IP address assigned to the network interface associated to the private endpoint. It can be dynamycally allocated from the range assigned to the selected subnet, or you can decide which specific address you want to assign to it. After the private endpoint is created, you cannot change its IP address, regardless of which of the two allocation modes you select during creation. |
    | **Application security group** | No application security group is assigned by default. You can choose an existing one, or you can create one and have it assigned. | Application security groups enable you to configure network security as a natural extension of an application's structure, allowing you to group virtual machines and define network security policies based on those groups. You can reuse your security policy at scale without manual maintenance of explicit IP addresses. The platform handles the complexity of explicit IP addresses and multiple rule sets, allowing you to focus on your business logic. For more information, see [Application security groups](/azure/virtual-network/application-security-groups). |

13. In the **DNS** page, fill all the details required. Then, select **Next: Tags**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-dns.png" alt-text="Screenshot showing the DNS page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-dns.png":::

14. Use the following table to understand the meaning of the different fields available in the **DNS** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Integrate with private DNS zone** | Enabled by default. | Select **Yes** if you want your private endpoint to be integrated with an Azure private DNS zone, or **No** if you want to use your own DNS servers, or if you want to resolve the name of the endpoint by using host files in the machines from which you want to connect through the private endpoint. For more information, see [Private endpoint DNS configuration](/azure/private-link/private-endpoint-overview#dns-configuration). If you configure private DNS zone integration, the private DNS zone is automatically linked to the virtual network in which you create the private endpoint. |
    | **Configuration name** | Automatically set for you to `privatelink-postgres-database-azure-com`. | This is the name assigned to DNS configuration which is associated to the private DNS zone. |
    | **Subscription** | Select the name of the [subscription](/microsoft-365/enterprise/subscriptions-licenses-accounts-and-tenants-for-microsoft-cloud-offerings#subscriptions) in which you want to create the private DNS zone. It automatically selects the subscription in which your server is deployed. | A subscription is an agreement with Microsoft to use one or more Microsoft cloud platforms or services, for which charges accrue based on either a per-user license fee or on cloud-based resource consumption. If you have multiple subscriptions, choose the subscription in which you'd like to be billed for the resource. |
    | **Resource group** | The [resource group](/azure/azure-resource-manager/management/manage-resource-groups-portal#what-is-a-resource-group) in the selected subscription, in which you want to create the private DNS zone. It must be an existing resource group. It automatically selects the resource group in which your server is deployed. | A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution, or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can easily deploy, update, and delete them as a group. |
    | **Private DNS zone** | Automatically set for you to `privatelink.postgres.database.azure.com`. | This is the name assigned to the private DNS zone resource. |

15. In the **Tags** page, fill all the details required. Then, select **Next: Review + create**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-tags.png" alt-text="Screenshot showing the Tags page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-tags.png":::

16. Use the following table to understand the meaning of the different fields available in the **Tags** page, and as guidance to fill the page:

    | Setting | Suggested value | Description |
    | --- | --- | --- |
    | **Name** | Leave empty. | Name of the tag that you want to assign to your private endpoint and private DNS zone (if you selected private DNS zone integration in the **DNS** page). |
    | **Value** | Leave empty. | Value that you want to assign to the tag with the given name, and that you want to assign to your private endpoint and private DNS zone (if you selected private DNS zone integration in the **DNS** page). |
    | **Resource** | Leave by default. | You can select to which resources you want the given tag assigned. It can be the private endpoint, the private DNS zone (if you selected private DNS zone integration in the **DNS** page), or both. |

17. In the **Review + create** page, make sure that everything is configured as you wanted to. Then, select **Create**.

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-review-create.png" alt-text="Screenshot showing the Review + create page of Create a private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-review-create.png":::

18. A deployment is initiated, and you see a notification when the deployment completes. 

    :::image type="content" source="./media/how-to-networking/create-private-endpoint-deployment-succeeded.png" alt-text="Screenshot showing the successful deployment of the private endpoint." lightbox="./media/how-to-networking/create-private-endpoint-deployment-succeeded.png":::

#### [CLI](#tab/cli-add-private-endpoint)

ddd

---

## Related content

- [Start an Azure Database for PostgreSQL flexible server](how-to-start-server.md).
- [Stop an Azure Database for PostgreSQL flexible server](how-to-stop-server.md).
- [Reset administrator password of an Azure Database for PostgreSQL flexible server](how-to-reset-admin-password.md).
- [Delete an Azure Database for PostgreSQL flexible server](how-to-delete-server.md).
- [Configure storage autogrow in an Azure Database for PostgreSQL flexible server](how-to-auto-grow-storage.md).
- [Configure high availability in an Azure Database for PostgreSQL flexible server](how-to-configure-high-availability.md).
