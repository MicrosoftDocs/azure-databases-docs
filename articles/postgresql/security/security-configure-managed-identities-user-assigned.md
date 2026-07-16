---
title: User Assigned Managed Identity in Azure Database for PostgreSQL Flexible Server
description: This article describes how to configure user assigned managed identities of an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to associate user assigned managed identities with an existing Azure Database for PostgreSQL flexible server, so that I can manage access to Azure resources securely.
author: Tameika-MSFT
ms.author: talawren
ms.reviewer: maghan
ms.date: 07/14/2026
ms.service: azure-database-postgresql
ms.subservice: security
ms.topic: how-to
---

# User assigned managed identities in Azure Database for PostgreSQL flexible server

This article provides step-by-step instructions to add or remove user assigned managed identities to an Azure Database for PostgreSQL flexible server.

## Steps to assign to existing servers

This article assumes you created the user assigned managed identities that you want to associate to an existing Azure Database for PostgreSQL flexible server.

For more information, see [how to manage user assigned managed identities in Microsoft Entra ID](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities).

You can associate as many user assigned managed identities as you want to an Azure Database for PostgreSQL flexible server.

### [Portal](#tab/portal-associate-user-assigned-existing)

The portal doesn't support associating user assigned managed identities to an Azure Database for PostgreSQL flexible server.

### [CLI](#tab/cli-associate-user-assigned-existing)

Use the [az postgres flexible-server identity assign](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-assign) command to associate a user assigned identity with a server.

```azurecli-interactive
az postgres flexible-server identity assign \
  --resource-group <resource_group> \
  --server-name <server> \
  --identity <identity>
```

---

## Steps to remove from existing servers

The service supports dissociating user assigned managed identities that are associated to an Azure Database for PostgreSQL flexible server.

An exception to that rule is any of the user assigned managed identities that you designate as the ones to access the encryption keys for data encryption. This case is only possible on servers that you deploy with [data encryption using customer managed keys](../security/security-data-encryption.md).

### [Portal](#tab/portal-dissociate-user-assigned-existing)

The portal doesn't support dissociating user assigned managed identities from an Azure Database for PostgreSQL flexible server.

### [CLI](#tab/cli-dissociate-user-assigned-existing)

Use the [az postgres flexible-server identity remove](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-remove) command to dissociate a user assigned identity from a server.

```azurecli-interactive
az postgres flexible-server identity remove \
  --resource-group <resource_group> \
  --server-name <server> \
  --identity <identity>
```

If you try to remove a user assigned managed identity that you use to access a data encryption key, you get the following error:

```output
Cannot remove identity <identity> because it's used for data encryption.
```

---

## Steps to show currently assigned

### [Portal](#tab/portal-show-user-assigned)

Use the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server.

1. In the resource menu, select **Overview**.

    :::image type="content" source="./media/security-configure-managed-identities-user-assigned/overview.png" alt-text="Screenshot showing the Overview page of an Azure Database for PostgreSQL flexible server." lightbox="./media/security-configure-managed-identities-user-assigned/overview.png":::

1. Select **JSON View**.

   :::image type="content" source="media/security-configure-managed-identities-system-assigned/json-view.png" alt-text="Screenshot showing how to select JSON View on an Azure Database for PostgreSQL flexible server." lightbox="media/security-configure-managed-identities-system-assigned/json-view.png":::

1. In the **Resource JSON** panel that opens, find the **identity** property. Inside it, you can find the **userAssignedIdentities**. That object consists of one or more key/value pairs, where each key represents the resource identifier of one user assigned managed identity. The corresponding value includes the **principalId** and **clientId** associated with that managed identity.

    :::image type="content" source="./media/security-configure-managed-identities-user-assigned/user-assigned-managed-identity-details.png" alt-text="Screenshot that shows where to find the userAssignedManagedIdentities object for a server." lightbox="./media/security-configure-managed-identities-user-assigned/user-assigned-managed-identity-details.png":::

### [CLI](#tab/cli-show-user-assigned)

Use the [az postgres flexible-server identity list](/cli/azure/postgres/flexible-server/identity#az-postgres-flexible-server-identity-list) command to list all associated user assigned managed identities with a server.

```azurecli-interactive
az postgres flexible-server identity list \
  --resource-group <resource_group> \
  --server-name <server> \
  --query "userAssignedIdentities"
```

---

## Related content

- [System assigned managed identity](security-configure-managed-identities-system-assigned.md)
