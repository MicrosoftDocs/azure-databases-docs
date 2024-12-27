---
title: Configure managed identities in Azure Database for PostgreSQL - Flexible Server
description: Learn how to configure managed identities in Azure Database for PostgreSQL - Flexible Server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 12/27/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Configure system or user assigned managed identities in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

In this article you can learn how to enable or disable a system assigned managed identity or how to add or remove one or more user assigned managed identities to your instance of Azure Database for PostgreSQL flexible server.

## Enable the system assigned managed identity for existing servers

## [Portal](#tab/portal-enable)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/concepts-identity/server-search.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/concepts-identity/server-search.png":::

2. In the resource menu, under **Security**, select **Identity**. Then, in the **System assigned managed identity** section, select the **On** option. Select **Save**.

    :::image type="content" source="./media/concepts-identity/enable-system-assigned-managed-identity.png" alt-text="Screenshot that shows how to enable the system assigned managed identity on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/concepts-identity/enable-system-assigned-managed-identity.png":::

3. When the process completes, a notification informs you that the system assigned managed identity is enabled.

    :::image type="content" source="./media/concepts-identity/enable-system-assigned-managed-identity-notification.png" alt-text="Screenshot that shows the notification informing that the system assigned managed identity is enabled." lightbox="./media/concepts-identity/enable-system-assigned-managed-identity-notification.png":::


## [CLI](#tab/cli-enable)

Although the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) commands don't provide built-in support to enable and disable the system assigned managed identity yet, you can use the [az rest](/cli/azure/reference-index#az-rest) command to directly invoke the [Servers - Update](/rest/api/postgresql/flexibleserver/servers/update) REST API.

```azurecli-interactive
# Enable system assigned managed identity
subscriptionId=<subscription-id>
resourceGroup=<resource-group>
server=<server>
result=$(az postgres flexible-server show --resource-group $resourceGroup --name $server --query "identity.type" --output tsv)
if [ -z "$result" ]; then
    az rest --method patch --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DBforPostgreSQL/flexibleServers/$server?api-version=2024-08-01 --body '{"identity":{"type":"SystemAssigned"}}'
elif [ "$result" == "UserAssigned" ]; then
    az rest --method patch --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DBforPostgreSQL/flexibleServers/$server?api-version=2024-08-01 --body '{"identity":{"type":"SystemAssigned,UserAssigned"}}'
else
    echo "System Assigned Managed identity is already enabled."
fi
```
---

## Disable the system assigned managed identity for existing servers

## [Portal](#tab/portal-disable)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/concepts-identity/server-search.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/concepts-identity/server-search.png":::

2. In the resource menu, under **Security**, select **Identity**. Then, in the **System assigned managed identity** section, select the **Off** option. Select **Save**.

    :::image type="content" source="./media/concepts-identity/disable-system-assigned-managed-identity.png" alt-text="Screenshot that shows how to disable the system assigned managed identity on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/concepts-identity/disable-system-assigned-managed-identity.png":::

3. When the process completes, a notification informs you that the system assigned managed identity is disabled.

    :::image type="content" source="./media/concepts-identity/disable-system-assigned-managed-identity-notification.png" alt-text="Screenshot that shows the notification informing that the system assigned managed identity is disabled." lightbox="./media/concepts-identity/disable-system-assigned-managed-identity-notification.png":::


## [CLI](#tab/cli-disable)

Although the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) commands don't provide built-in support to enable and disable the system assigned managed identity yet, you can use the [az rest](/cli/azure/reference-index#az-rest) command to directly invoke the [Servers - Update](/rest/api/postgresql/flexibleserver/servers/update) REST API.

```azurecli-interactive
# Disable system assigned managed identity
subscriptionId=<subscription-id>
resourceGroup=<resource-group>
server=<server>
result=$(az postgres flexible-server show --resource-group $resourceGroup --name $server --query "identity.type" --output tsv)
if [ "$result" == "SystemAssigned" ]; then
    az rest --method patch --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DBforPostgreSQL/flexibleServers/$server?api-version=2024-08-01 --body '{"identity":{"type":"None"}}'
elif [ "$result" == "SystemAssigned,UserAssigned" ]; then
    echo "System Assigned Managed identity cannot be disabled as the instance has User Assigned Managed identities assigned."
else
    echo "System Assigned Managed identity is already disabled."
fi
```

---

## Verify the system assigned managed identity

## [Portal](#tab/portal-verify)

You can verify the managed identity created by going to **Enterprise Applications** 

1. Choose  **Application Type == Managed Identity**

2. Provide your flexible server name in **Search by application name or Identity** as shown in the screenshot.

![Screenshot verifying system assigned managed identity.](media/concepts-Identity/verify-managed-identity.png)

## [CLI](#tab/cli-verify)


```azurecli-interactive
server=<server>
az ad sp list --display-name $server
```

---

## Special considerations



[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Managed identities in Azure Database for PostgreSQL - Flexible Server](concepts-identity.md).
- [Firewall rules in Azure Database for PostgreSQL - Flexible Server](concepts-firewall-rules.md).
- [Public access and private endpoints in Azure Database for PostgreSQL - Flexible Server](concepts-networking-public.md).
- [Virtual network integration in Azure Database for PostgreSQL - Flexible Server](concepts-networking-private.md).
