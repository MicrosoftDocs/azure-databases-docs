---
title: User Assigned Managed Identity
description: This article describes how to configure user assigned managed identities of an Azure Database for PostgreSQL flexible server instance.
author: techlake
ms.author: hganten
ms.reviewer: maghan
ms.date: 08/08/2025
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
ms.custom:
  - horz-security
---

# User assigned managed identities

This article provides step-by-step instructions to add or remove user assigned managed identities to an Azure Database for PostgreSQL flexible server instance.

## Steps to assign to existing servers

This article assumes you created the user assigned managed identities that you want to associate to an existing instance of Azure Database for PostgreSQL flexible server.

For more information, see [how to manage user assigned managed identities in Microsoft Entra ID](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities).

You can associate as many user assigned managed identities as you want to an Azure Database for PostgreSQL flexible server instance.

### [Portal](#tab/portal-associate-user-assigned-existing)

There's no support to associate user assigned managed identities to an Azure Database for PostgreSQL flexible server instance via the portal.

### [CLI](#tab/cli-associate-user-assigned-existing)

You can associate a user assigned identity to an Azure Database for PostgreSQL flexible server instance via the [az postgres flexible-server identity assign](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-assign) command.

```azurecli-interactive
# Associate user assigned managed identity
resourceGroup=<resource-group>
server=<server>
identity=<identity>
az postgres flexible-server identity assign \
  --resource-group $resourceGroup \
  --server-name $server \
  --identity $identity
```

---

## Steps to remove from existing servers

The service supports dissociating user assigned managed identities which are associated to an Azure Database for PostgreSQL flexible server instance.

An exception to that rule is any of the user assigned managed identities that are designated as the ones that should be used to access the encryption keys. This case is only possible on servers that were deployed with [data encryption using customer managed keys](../security/security-data-encryption.md).

### [Portal](#tab/portal-dissociate-user-assigned-existing)

There's no support to dissociate user assigned managed identities from an Azure Database for PostgreSQL flexible server instance via the portal.

### [CLI](#tab/cli-dissociate-user-assigned-existing)

You can dissociate a user assigned identity from an Azure Database for PostgreSQL flexible server instance via the [az postgres flexible-server identity remove](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-remove) command.

```azurecli-interactive
# Dissociate user assigned managed identity
resourceGroup=<resource-group>
server=<server>
identity=<identity>
az postgres flexible-server identity remove \
  --resource-group $resourceGroup \
  --server-name $server \
  --identity $identity
```

If you try to remove a user assigned managed identity which is used to access a data encryption key, you get the following error:

```output
Cannot remove identity <identity> because it's used for data encryption.
```

---

## Steps to show currently assigned

### [Portal](#tab/portal-show-user-assigned)

Using the [Azure portal](https://portal.azure.com/):

1. Locate your server in the portal, if you don't have it open. One way to do it is by typing the name of the server in the search bar. When the resource with the matching name is shown, select that resource.

    :::image type="content" source="./media/security-configure-managed-identities-user-assigned/search-server.png" alt-text="Screenshot that shows how to search for a resource using the search bar in the Azure portal." lightbox="./media/security-configure-managed-identities-user-assigned/search-server.png":::

2. In the resource menu, under **Overview**, select **JSON View**.

    :::image type="content" source="./media/security-configure-managed-identities-user-assigned/json-view.png" alt-text="Screenshot that shows how to select JSON View on an Azure Database for PostgreSQL flexible server instance." lightbox="./media/security-configure-managed-identities-user-assigned/json-view.png":::

3. In the **Resource JSON** panel that opens, find the **identity** property and, inside it, you can find the **userAssignedIdentities**. That object consists of one or more key/value pairs, where each key represents the resource identifier of one user assigned managed identity, and their corresponding value is made of **principalId** and **clientId** associated to that managed identity.

    :::image type="content" source="./media/security-configure-managed-identities-user-assigned/user-assigned-managed-identity-details.png" alt-text="Screenshot that shows where to find the userAssignedManagedIdentities object for a server." lightbox="./media/security-configure-managed-identities-user-assigned/user-assigned-managed-identity-details.png":::

### [CLI](#tab/cli-show-user-assigned)

```azurecli-interactive
# List all associated user assigned managed identities
resourceGroup=<resource-group>
server=<server>
az postgres flexible-server identity list \
  --resource-group $resourceGroup \
  --server-name $server \
  --query "userAssignedIdentities"
```

---

## Related content

- [System assigned managed identity](security-configure-managed-identities-system-assigned.md)
