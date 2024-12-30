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

In this article, you can learn how to enable or disable a system assigned managed identity for your instance of Azure Database for PostgreSQL flexible server. You can also learn how to add or remove one or more user assigned managed identities to your instance.

## Enable the system assigned managed identity for existing servers

## [Portal](#tab/portal-enable)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, under **Security**, select **Identity**. Then, in the **System assigned managed identity** section, select the **On** option. Select **Save**.

    :::image type="content" source="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity.png" alt-text="Screenshot that shows how to enable the system assigned managed identity on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity.png":::

3. When the process completes, a notification informs you that the system assigned managed identity is enabled.

    :::image type="content" source="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-notification.png" alt-text="Screenshot that shows the notification informing that the system assigned managed identity is enabled." lightbox="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-notification.png":::

## [CLI](#tab/cli-enable)

The [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command doesn't provide built-in support to enable and disable the system assigned managed identity yet. As a workaround, you can use the [az rest](/cli/azure/reference-index#az-rest) command to directly invoke the [Servers - Update](/rest/api/postgresql/flexibleserver/servers/update) REST API.

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

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, under **Security**, select **Identity**. Then, in the **System assigned managed identity** section, select the **Off** option. Select **Save**.

    :::image type="content" source="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity.png" alt-text="Screenshot that shows how to disable the system assigned managed identity on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity.png":::

3. When the process completes, a notification informs you that the system assigned managed identity is disabled.

    :::image type="content" source="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-notification.png" alt-text="Screenshot that shows the notification informing that the system assigned managed identity is disabled." lightbox="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-notification.png":::

## [CLI](#tab/cli-disable)

The [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command doesn't provide built-in support to enable and disable the system assigned managed identity yet. As a workaround, you can use the [az rest](/cli/azure/reference-index#az-rest) command to directly invoke the [Servers - Update](/rest/api/postgresql/flexibleserver/servers/update) REST API.

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

## Show the system assigned managed identity

## [Portal](#tab/portal-show-sami)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, under **Overview**, select **JSON View**.

    :::image type="content" source="./media/how-to-configure-managed-identities/json-view.png" alt-text="Screenshot that shows how to select JSON View on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/json-view.png":::

3. In the **Resource JSON** panel that opens, find the **identity** property and, inside it, you can find the **principalId** and **tenantId** for the system assigned managed identity.

    :::image type="content" source="./media/how-to-configure-managed-identities/system-assigned-managed-identity-details.png" alt-text="Screenshot that shows where to find the principalId and tenantId of the system assigned managed identity." lightbox="./media/how-to-configure-managed-identities/system-assigned-managed-identity-details.png":::

## [CLI](#tab/cli-show-sami)


```azurecli-interactive
# Show the system assigned managed identity
resourceGroup=<resource-group>
server=<server>
az postgres flexible-server identity list --resource-group $resourceGroup --server-name $server --query "{principalId:principalId, tenantId:tenantId}" --output table
```

---

## Verify the system assigned managed identity

## [Portal](#tab/portal-verify-sami)

Using the [Azure portal](https://portal.azure.com/):

1. Locate the **Enterprise Applications** service in the portal, if you don't have it open. One way to do it is by typing its name in the search bar. When the service with the matching name is shown, select it.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-enterprise-applications.png" alt-text="Screenshot that shows how to search for a the Enterprise applications service using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-enterprise-applications.png":::

2. Choose  **Application Type == Managed Identity**

3. Provide the name of your instance of Azure Database for PostgreSQL flexible server in the **Search by application name or object ID** text box.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-managed-identity.png" alt-text="Screenshot that shows how to search for a managed identity using the Enterprise applications service interface in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-managed-identity.png":::

## [CLI](#tab/cli-verify-sami)


```azurecli-interactive
# Verify the system assigned managed identity
server=<server>
az ad sp list --display-name $server
```

---

## Associate user assigned managed identities to existing servers

This article assumes you created the user assigned managed identities that you want to associate to an existing instance of Azure Database for PostgreSQL flexible server.

For more information, see [how to manage user assigned managed identities in Microsoft Entra ID](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities).

You can associate as many user assigned managed identities as you want to an instance of Azure Database for PostgreSQL flexible server.

## [Portal](#tab/portal-associate)

There's no support to associate user assigned managed identities to an instance of Azure Database for PostgreSQL flexible server via the portal.

## [CLI](#tab/cli-associate)

You can associate a user assigned identity to an instance of Azure Database for PostgreSQL flexible server via the [az postgres flexible-server identity assign](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-assign) command.


```azurecli-interactive
# Associate user assigned managed identity
resourceGroup=<resource-group>
server=<server>
identity=<identity>
az postgres flexible-server identity assign --resource-group $resourceGroup --server-name $server --identity $identity
```

---

## Dissociate user assigned managed identities to existing servers

The service supports dissociating user assigned managed identities which are associated to an instance of Azure Database for PostgreSQL flexible server.

An exception to that rule is any of the user assigned managed identities that are designated as the ones that should be used to access the encryption keys. This case is only possible on servers that were deployed with [data encryption using customer managed keys](concepts-data-encryption.md).

## [Portal](#tab/portal-dissociate)

There's no support to dissociate user assigned managed identities from an instance of Azure Database for PostgreSQL flexible server via the portal.

## [CLI](#tab/cli-dissociate)

You can dissociate a user assigned identity from an instance of Azure Database for PostgreSQL flexible server via the [az postgres flexible-server identity remove](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-remove) command.


```azurecli-interactive
# Dissociate user assigned managed identity
resourceGroup=<resource-group>
server=<server>
identity=<identity>
az postgres flexible-server identity remove --resource-group $resourceGroup --server-name $server --identity $identity
```

---

## Show the associated user assigned managed identities

## [Portal](#tab/portal-show-uami)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, under **Overview**, select **JSON View**.

    :::image type="content" source="./media/how-to-configure-managed-identities/json-view.png" alt-text="Screenshot that shows how to select JSON View on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/json-view.png":::

3. In the **Resource JSON** panel that opens, find the **identity** property and, inside it, you can find the **userAssignedIdentities**. That object consists of one or more key/value pairs, where each key represents the resource identifier of one user assigned managed identity, and their corresponding value is made of **principalId** and **clientId** associated to that managed identity.

    :::image type="content" source="./media/how-to-configure-managed-identities/user-assigned-managed-identity-details.png" alt-text="Screenshot that shows where to find the userAssignedManagedIdentities object for a server." lightbox="./media/how-to-configure-managed-identities/user-assigned-managed-identity-details.png":::

## [CLI](#tab/cli-show-uami)


```azurecli-interactive
# List all associated user assigned managed identities
resourceGroup=<resource-group>
server=<server>
az postgres flexible-server identity list --resource-group $resourceGroup --server-name $server --query "userAssignedIdentities"
```

---

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Managed identities in Azure Database for PostgreSQL - Flexible Server](concepts-identity.md).
- [Firewall rules in Azure Database for PostgreSQL - Flexible Server](concepts-firewall-rules.md).
- [Public access and private endpoints in Azure Database for PostgreSQL - Flexible Server](concepts-networking-public.md).
- [Virtual network integration in Azure Database for PostgreSQL - Flexible Server](concepts-networking-private.md).
