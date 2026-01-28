---
title: Enable public access
description: Learn how to enable public access in an Azure Database for PostgreSQL flexible server deployed with public access networking mode.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 01/23/2026
ms.service: azure-database-postgresql
ms.subservice: networking
ms.topic: how-to
ai-usage: ai-assisted
# customer intent: As a user, I want to learn how to enable public network access in an Azure Database for PostgreSQL flexible server.
---

# Enable public access

This article explains how to enable public network access on an Azure Database for PostgreSQL flexible server. Public access allows connections from the internet using a public IP address, which you can secure with firewall rules and private endpoints.

## Prerequisites

Before you begin, verify that your server meets the following requirements:

- **Server deployed with public access networking mode**: You can only enable or disable public access on servers that you originally deployed with the **Public access (allowed IP addresses)** networking option.

- **Server status is Ready**: The server must be in a `Ready` state before you can modify networking settings.

> [!IMPORTANT]
> **This article doesn't apply to servers configured with private access (VNet Integration).** The networking mode is a permanent setting chosen during server creation. If your server's **Networking** page shows **Private access (VNet Integration)** as the connectivity method, you can't enable public access on that server.
>
> To switch from private access to public access, you must either:
> - **Create a new server** with the **Public access (allowed IP addresses)** networking option selected during deployment.
> - **Restore the server** to a new instance with public access enabled.
>
> For more information about the differences between networking modes, see [Private access (VNet Integration)](concepts-networking-private.md) and [Public access (allowed IP addresses)](concepts-networking-public.md).

## Determine your server's networking mode

To check which networking mode your server uses:

### [Portal](#tab/portal-check-mode)

1. In the [Azure portal](https://portal.azure.com), navigate to your Azure Database for PostgreSQL flexible server.
1. In the resource menu, select **Networking**.
1. Check the **Connectivity method** section at the top of the page:
   - **Public access (allowed IP addresses)**: This article applies to your server. Continue with the steps in this article.
   - **Private access (VNet Integration)**: This article doesn't apply. See the [Prerequisites](#prerequisites) section for your options.

### [CLI](#tab/cli-check-mode)

Run the following command to check your server's networking configuration:

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{delegatedSubnetId:network.delegatedSubnetResourceId, publicAccess:network.publicNetworkAccess}'
```

Interpret the results:

- If `delegatedSubnetId` returns a subnet resource ID, your server uses **private access (VNet Integration)**. This article doesn't apply.
- If `delegatedSubnetId` is `null`, your server uses **public access** mode. Continue with this article.

---

## Enable public access

When you enable public access:

- The server accepts connections from IP addresses allowed by your firewall rules.
- You can also connect through private endpoints.
- Any previously configured firewall rules are automatically enforced.

### [Portal](#tab/portal-enable-public-access)

1. In the [Azure portal](https://portal.azure.com), navigate to your Azure Database for PostgreSQL flexible server.
1. In the resource menu, select **Networking**.
1. Under **Public access**, select the **Allow public access to this resource through the internet using a public IP address** checkbox.
1. Select **Save**.
1. Wait for the server status to change from **Updating** to **Ready**. A notification confirms when the changes are applied.

### [CLI](#tab/cli-enable-public-access)

Run the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command:

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --public-access Enabled
```

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Server <server> is busy with other operations. Please try later` | Server isn't in `Ready` state | Wait for the current operation to complete, then retry |
| Command succeeds but setting doesn't change | Server was deployed with private access | You can't enable public access on VNet-integrated servers. Create a new server with public access instead |

**Verify the change:**

```azurecli-interactive
az postgres flexible-server show \
  --resource-group <resource_group> \
  --name <server> \
  --query '{publicAccess:network.publicNetworkAccess}'
```

The output should show `"publicAccess": "Enabled"`.

---

## Next steps

After you enable public access, configure firewall rules to control which IP addresses can connect to your server:

- [Add firewall rules](how-to-networking-servers-deployed-public-access-add-firewall-rules.md)
- [Delete firewall rules](how-to-networking-servers-deployed-public-access-delete-firewall-rules.md)

## Related content

- [Networking overview](how-to-networking.md)
- [Disable public access](how-to-networking-servers-deployed-public-access-disable-public-access.md)
- [Add private endpoint connections](how-to-networking-servers-deployed-public-access-add-private-endpoint.md)
- [Private access (VNet Integration)](concepts-networking-private.md)
- [Public access (allowed IP addresses)](concepts-networking-public.md)
