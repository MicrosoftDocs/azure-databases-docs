---
title: System assigned managed identity
description: This article describes how to configure system assigned managed identity of an Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 02/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: how-to
# customer intent: As a user, I want to learn how to configure system assigned managed identity of an Azure Database for PostgreSQL flexible server.
---

# System assigned managed identity

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides step-by-step instructions to enable or disable a system assigned managed identity for an Azure Database for PostgreSQL flexible server.

## Steps to enable for existing servers

### [Portal](#tab/portal-enable-system-assigned-existing)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, under **Security**, select **Identity**.

    :::image type="content" source="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-identity.png" alt-text="Screenshot that shows the Identity page, under Security, to enable the system assigned managed identity of an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-identity.png":::

3. In the **System assigned managed identity** section, select **On**.

    :::image type="content" source="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-status-on.png" alt-text="Screenshot that shows the Identity page, to enable the system assigned managed identity of an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-status-on.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-status-on-save.png" alt-text="Screenshot that shows the Save button after having enabled the system assigned managed identity of an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-status-on-save.png":::

5. When the process completes, a notification informs you that the system assigned managed identity is enabled.

    :::image type="content" source="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-notification.png" alt-text="Screenshot that shows the notification informing that the system assigned managed identity is enabled." lightbox="./media/how-to-configure-managed-identities/enable-system-assigned-managed-identity-notification.png":::

### [CLI](#tab/cli-enable-system-assigned-existing)

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

## Steps to disable for existing servers

### [Portal](#tab/portal-disable-system-assigned-existing)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, under **Security**, select **Identity**.

    :::image type="content" source="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-identity.png" alt-text="Screenshot that shows the Identity page, under Security, to disable the system assigned managed identity of an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-identity.png":::

3. In the **System assigned managed identity** section, select **Off**.

    :::image type="content" source="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-status-off.png" alt-text="Screenshot that shows the Identity page, to disable the system assigned managed identity of an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-status-off.png":::

4. Select **Save**.

    :::image type="content" source="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-status-off-save.png" alt-text="Screenshot that shows the Save button after having disabled the system assigned managed identity of an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-status-off-save.png":::

5. When the process completes, a notification informs you that the system assigned managed identity is disabled.

    :::image type="content" source="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-notification.png" alt-text="Screenshot that shows the notification informing that the system assigned managed identity is disabled." lightbox="./media/how-to-configure-managed-identities/disable-system-assigned-managed-identity-notification.png":::

### [CLI](#tab/cli-disable-system-assigned-existing)

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

## Steps to show currently assigned

### [Portal](#tab/portal-show-system-assigned-existing)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-server.png":::

2. In the resource menu, select **Overview**

    :::image type="content" source="./media/how-to-configure-managed-identities/overview.png" alt-text="Screenshot that shows the Overview page of an Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/overview.png":::

3. Select **JSON View**.

    :::image type="content" source="./media/how-to-configure-managed-identities/json-view.png" alt-text="Screenshot that shows how to select JSON View on an instance of Azure Database for PostgreSQL flexible server." lightbox="./media/how-to-configure-managed-identities/json-view.png":::

4. In the **Resource JSON** panel that opens, find the **identity** property and, inside it, you can find the **principalId** and **tenantId** for the system assigned managed identity.

    :::image type="content" source="./media/how-to-configure-managed-identities/system-assigned-managed-identity-details.png" alt-text="Screenshot that shows where to find the principalId and tenantId of the system assigned managed identity." lightbox="./media/how-to-configure-managed-identities/system-assigned-managed-identity-details.png":::

### [CLI](#tab/cli-show-system-assigned-existing)


```azurecli-interactive
# Show the system assigned managed identity
resourceGroup=<resource-group>
server=<server>
az postgres flexible-server identity list --resource-group $resourceGroup --server-name $server --query "{principalId:principalId, tenantId:tenantId}" --output table
```

---

## Steps to verify in Microsoft Entra ID

### [Portal](#tab/portal-verify-system-assigned-existing)

Using the [Azure portal](https://portal.azure.com/):

1. Locate the **Enterprise Applications** service in the portal, if you don't have it open. One way to do it is by typing its name in the search bar. When the service with the matching name is shown, select it.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-enterprise-applications.png" alt-text="Screenshot that shows how to search for the Enterprise applications service using the search bar in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-enterprise-applications.png":::

2. Choose  **Application Type == Managed Identity**.

3. Provide the name of your instance of Azure Database for PostgreSQL flexible server in the **Search by application name or object ID** text box.

    :::image type="content" source="./media/how-to-configure-managed-identities/search-managed-identity.png" alt-text="Screenshot that shows how to search for a managed identity using the Enterprise applications service interface in the Azure portal." lightbox="./media/how-to-configure-managed-identities/search-managed-identity.png":::

### [CLI](#tab/cli-verify-system-assigned-existing)


```azurecli-interactive
# Verify the system assigned managed identity
server=<server>
az ad sp list --display-name $server
```

---

## Related content

- [User assigned managed identity](how-to-configure-managed-identities-user-assigned.md).
