---
title: Configure Data Encryption
description: Learn how to configure data encryption in an Azure Database for PostgreSQL flexible server instance.
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

# Configure data encryption in Azure Database for PostgreSQL

This article provides step-by-step instructions to configure data encryption for an Azure Database for PostgreSQL flexible server instance.

> [!IMPORTANT]
> The only point at which you can decide if you want to use a system managed key or a customer managed key for data encryption, is at server creation. Once you make that decision and create the server, you can't switch between the two options.

In this article, you learn how to create a new server and configure its data encryption options. For existing servers, whose data encryption is configured to use customer managed encryption key, you learn:
- How to select a different user assigned managed identity with which the service accesses the encryption key.
- How to specify a different encryption key or how to rotate the encryption key currently used for data encryption.

To learn about data encryption in the context of Azure Database for PostgreSQL, see the [data encryption](../security/security-data-encryption.md).

## Configure data encryption with system managed key during server provisioning

### [Portal](#tab/portal-system-managed-server-provisioning)

Using the [Azure portal](https://portal.azure.com/):

1. During provisioning of a new Azure Database for PostgreSQL flexible server instance, data encryption is configured in the **Security** tab. For **Data encryption key**, select the **Service-managed key** radio button.

    :::image type="content" source="media/security-configure-data-encryption/create-server-system-assigned.png" alt-text="Screenshot that shows how to select the system managed encryption key during server provisioning." lightbox="media/security-configure-data-encryption/create-server-system-assigned.png":::

1. If you enable geo-redundant backup storage to be provisioned together with the server, the aspect of the **Security** tab changes slightly because the server uses two separate encryption keys. One for the primary region in which you're deploying your server, and one for the paired region to which the server backups are asynchronously replicated.

    :::image type="content" source="media/security-configure-data-encryption/create-server-system-assigned-geo-redundant.png" alt-text="Screenshot that shows how to select the system managed encryption key during server provisioning, when the server is enabled for geo-redundant backup storage." lightbox="media/security-configure-data-encryption/create-server-system-assigned-geo-redundant.png":::

### [CLI](#tab/cli-system-managed-server-provisioning)

You can enable data encryption with system assigned encryption key, while provisioning a new server, via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> ...
```

> [!NOTE]  
> There's no special parameter in the previous command to specify that the server must be created with system assigned key for data encryption. The reason being that data encryption with system assigned key is the default option.
> Also, notice that you must complete the command provided with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

---

## Configure data encryption with customer managed key during server provisioning

### [Portal](#tab/portal-customer-managed-server-provisioning)

Using the [Azure portal](https://portal.azure.com/):

1. [Create one user assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities), if you don't have one yet. If your server has geo-redundant backups enabled, you need to create to different identities. Each of those identities is used to access each of the two data encryption keys.

> [!NOTE]  
> Although it isn't required, to maintain regional resiliency, we recommend that you create the user managed identity in the same region as your server. And if your server has geo-backup redundancy enabled, we recommend that the second user managed identity, used to access the data encryption key for geo-redundant backups, is created in the [paired region](/azure/reliability/cross-region-replication-azure) of the server.

1. [Create one Azure Key Vault](/azure/key-vault/general/quick-create-portal) or [create one Managed HSM](/azure/key-vault/managed-hsm/quick-create-cli), if you don't have one key store created yet. Make sure that you meet the [requirements](../security/security-data-encryption.md#cmk-requirements). Also, follow the [recommendations](../security/security-data-encryption.md#recommendations) before you configure the key store, and before you create the key and assign the required permissions to the user assigned managed identity. If your server has geo-redundant backups enabled, you need to create a second key store. That second key store is used to keep the data encryption key with which your backups copied to the [paired region](/azure/reliability/cross-region-replication-azure) of the server are encrypted.

> [!NOTE]  
> The key store used to keep the data encryption key must be deployed in the same region as your server. And if your server has geo-backup redundancy enabled, the key store that keeps the data encryption key for geo-redundant backups must be created in the [paired region](/azure/reliability/cross-region-replication-azure) of the server.

1. [Create one key in your key store](/azure/key-vault/keys/quick-create-portal). If your server has geo-redundant backups enabled, you need one key on each of the key stores. With one of these keys, we encrypt all your server's data (including all system and user databases, temporary files, server logs, write-ahead log segments, and backups). With the second key, we encrypt the copies of the backups which are asynchronously copied over the [paired region](/azure/reliability/cross-region-replication-azure) of your server.

1. During provisioning of a new Azure Database for PostgreSQL flexible server instance, data encryption is configured in the **Security** tab. For **Data encryption key**, select the **Customer-managed key** radio button.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned.png" alt-text="Screenshot that shows how to select the customer managed encryption key during server provisioning." lightbox="media/security-configure-data-encryption/create-server-customer-assigned.png":::

1. If you enable geo-redundant backup storage to be provisioned together with the server, the aspect of the **Security** tab changes slightly because the server uses two separate encryption keys. One for the primary region in which you're deploying your server, and one for the paired region to which the server backups are asynchronously replicated.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-geo-redundant.png" alt-text="Screenshot that shows how to select the customer managed encryption key during server provisioning, when the server is enabled for geo-redundant backup storage." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-geo-redundant.png":::

1. In **User assigned managed identity**, select **Change identity**.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-change-identity.png" alt-text="Screenshot that shows how to select the user assigned managed identity to access the data encryption key for the data of the server location." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-change-identity.png":::

1. Among the list of user assigned managed identities, select the one you want your server to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-select-identity.png" alt-text="Screenshot that shows how to select the user assigned managed identity with which the server accesses the data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-select-identity.png":::

1. Select **Add**.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-add-identity.png" alt-text="Screenshot that shows the location of the Add button to assign the identity with which the server accesses the data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-add-identity.png":::

1. Select **Use automatic key version update**, if you prefer to let the service automatically update the reference to the most current version of the chosen key, whenever the current version is rotated manually or automatically. To understand the benefits of using automatic key version updates, see [automatic key version update](../security/security-data-encryption.md#cmk-key-version-updates).

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-version-less.png" alt-text="Screenshot that shows how to enable automatic key version updates." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-version-less.png":::

1. Select **Select a key**.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-select-key.png" alt-text="Screenshot that shows how to select a data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-select-key.png":::

1. **Subscription** is automatically populated with the name of the subscription on which your server is about to be created. The key store that keeps the data encryption key must exist in the same subscription as the server.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-subscription.png" alt-text="Screenshot that shows how to select the subscription in which the key store should exist." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-subscription.png":::

1. In **Key store type**, select the radio button corresponding to the type of key store in which you plan to store the data encryption key. In this example, we choose **Key vault**, but the experience is similar if you choose **Managed HSM**.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-store-type.png" alt-text="Screenshot that shows how to select the type of store that keeps the data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-store-type.png":::

1. Expand **Key vault** (or **Managed HSM**, if you selected that storage type), and select the instance where the data encryption key exists.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-vault.png" alt-text="Screenshot that shows how to select the key store that keeps the data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-vault.png":::

    > [!NOTE]  
    > When you expand the dropdown box, it shows **No available items**. It takes a few seconds until it lists all the instances of key vault which are deployed in the same region as the server.
    
1. Expand **Key**, and select the name of the key that you want to use for data encryption.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-key.png" alt-text="Screenshot that shows how to select the data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-key.png":::

1. If you didn't select **Use automatic key version update**, you must also select a specific version of the key. To do that, expand **Version**, and select the identifier of the version of the key that you want to use for data encryption.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-version.png" alt-text="Screenshot that shows how to select the version to use of the data encryption key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-version.png":::

1. Select **Select**.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-select.png" alt-text="Screenshot that shows how to select the chose key." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-select.png":::

1. Configure all other settings of the new server and select **Review + create**.

    :::image type="content" source="media/security-configure-data-encryption/create-server-customer-assigned-key-review-create.png" alt-text="Screenshot that shows how to complete creation of server." lightbox="media/security-configure-data-encryption/create-server-customer-assigned-key-review-create.png":::

### [CLI](#tab/cli-customer-managed-server-provisioning)

You can enable data encryption with user assigned encryption key, while provisioning a new server, via the [az postgres flexible-server create](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-create) command.

If your server doesn't have geo-redundant backups enabled:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --geo-redundant-backup Disabled \
  --identity <managed_identity_to_access_primary_encryption_key> \
  --key <resource_identifier_of_primary_encryption_key> ...
```

> [!NOTE]  
> The previous command needs to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

If your server has geo-redundant backups enabled:

```azurecli-interactive
az postgres flexible-server create \
  --resource-group <resource_group> \
  --name <server> \
  --geo-redundant-backup Enabled \
  --identity <managed_identity_to_access_primary_encryption_key> \
  --key <resource_identifier_of_primary_encryption_key> \
  --backup-identity <managed_identity_to_access_geo_backups_encryption_key> \
  --backup-key <resource_identifier_of_geo_backups_encryption_key> ...
```

> [!NOTE]  
> The previous command needs to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the provisioned server.

---

## Configure data encryption with customer managed key on existing servers

The only point at which you can decide if you want to use a system managed key or a customer managed key for data encryption, is at server creation. Once you make that decision and create the server, you can't switch between the two options. The only alternative, if you want to change from one to the other, requires [restoring any of the backups available of server onto a new server](../backup-restore/how-to-restore-latest-restore-point.md). While configuring the restore, you're allowed to change the data encryption configuration of the new server.

For existing servers that were deployed with data encryption using a customer managed key, you're allowed to do several configuration changes. Things that can be changed are the references to the keys used for encryption, and references to the user assigned managed identities used by the service to access the keys kept in the key stores.

You must update references that your Azure Database for PostgreSQL flexible server instance has to a key:
- When the key stored in the key store is rotated, either manually or automatically, and your Azure Database for PostgreSQL flexible server instance is pointing to a specific version of the key. If you're pointing to a key, but not to a specific version of the key (that's when you have **Use automatic key version update** enabled), then the service will take care of automatically reference the most current version of the key, whenever they key is manually or automatically rotated.
- When you want to use the same or a different key stored in a different key store.

You must update the user assigned managed identities which are used by your Azure Database for PostgreSQL flexible server instance to access the encryption keys whenever you want to use a different identity.

### [Portal](#tab/portal-customer-managed-server-existing)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Database for PostgreSQL flexible server instance.

1. In the resource menu, under **Security**, select **Data encryption**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-data-encryption.png" alt-text="Screenshot that shows how to get to the Data encryption for an existing server." lightbox="media/security-configure-data-encryption/existing-server-data-encryption.png":::

1. To change the user assigned managed identity with which the server accesses the key store in which the key is kept, expand the **User assigned managed identity** dropdown, and select any of the identities available.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-select-managed-identity.png" alt-text="Screenshot that shows how to select one of the user assigned managed identities associated to the server." lightbox="media/security-configure-data-encryption/existing-server-select-managed-identity.png":::

    > [!NOTE]  
    > Identities shown in the combo-box are only the ones that your Azure Database for PostgreSQL flexible server instance was assigned.
    > Although it isn't required, to maintain regional resiliency, we recommend that you select user managed identities in the same region as your server. And if your server has geo-backup redundancy enabled, we recommend that the second user managed identity, used to access the data encryption key for geo-redundant backups, exists in the [paired region](/azure/reliability/cross-region-replication-azure) of the server.

1. If the user assigned managed identity that you want to use to access the data encryption key isn't assigned to your Azure Database for PostgreSQL flexible server instance, and it doesn't even exist as an Azure resource with its corresponding object in Microsoft Entra ID, you can create it by selecting **Create**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-create-new-managed-identity.png" alt-text="Screenshot that shows how to create a new user assigned managed identities in Azure and Microsoft Entra ID, automatically assign it to your Azure Database for PostgreSQL flexible server instance, and use it to access the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-create-new-managed-identity.png":::

1. In the **Create User Assigned Managed Identity** panel, complete the details of the user assigned managed identity that you want to create, and automatically assign to your Azure Database for PostgreSQL flexible server instance to access the data encryption key.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-create-new-managed-identity-details.png" alt-text="Screenshot that shows how to provide the details for the new user assigned managed identity." lightbox="media/security-configure-data-encryption/existing-server-create-new-managed-identity-details.png":::

1. If the user assigned managed identity that you want to use to access the data encryption key isn't assigned to your Azure Database for PostgreSQL flexible server instance, but it does exist as an Azure resource with its corresponding object in Microsoft Entra ID, you can assign it by selecting **Select**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-select-existing-managed-identity.png" alt-text="Screenshot that shows how to select an existing user assigned managed identity in Azure and Microsoft Entra ID, automatically assign it to your Azure Database for PostgreSQL flexible server instance, and use it to access the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-select-existing-managed-identity.png":::

1. Among the list of user assigned managed identities, select the one you want your server to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-select-existing-managed-identity-details.png" alt-text="Screenshot that shows how to select an existing user assigned managed identity to assign it to your Azure Database for PostgreSQL flexible server instance, and use it to access the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-select-existing-managed-identity-details.png":::

1. Select **Add**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-select-existing-managed-identity-details-add.png" alt-text="Screenshot that shows how to add the selected user assigned managed identity." lightbox="media/security-configure-data-encryption/existing-server-select-existing-managed-identity-details-add.png":::

1. Select **Use automatic key version update**, if you prefer to let the service automatically update the reference to the most current version of the chosen key, whenever the current version is rotated manually or automatically. To understand the benefits of using automatic key version updates, see [automatic key version update](../security/security-data-encryption.md##CMK key version updates).

    :::image type="content" source="media/security-configure-data-encryption/existing-server-version-less.png" alt-text="Screenshot that shows how to enable automatic key version updates." lightbox="media/security-configure-data-encryption/existing-server-version-less.png":::

1. If you rotate the key and don't have **Use automatic key version update** enabled. Or if you want to use a different key, you must update your Azure Database for PostgreSQL flexible server instance, so that it points to the new key version or new key. To do that, you can copy the resource identifier of the key, and paste it in the **Key identifier** box.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-paste-key-identifier.png" alt-text="Screenshot that shows where to paste the resource identifier of the new key or new key version that the server must use for data encryption." lightbox="media/security-configure-data-encryption/existing-server-paste-key-identifier.png":::

1. If the user accessing Azure portal has permissions to access the key stored in the key store, you can use an alternative approach to choose the new key or new key version. To do that, in **Key selection method**, select the **Select a key** radio button.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-select-key.png" alt-text="Screenshot that shows how to enable the user friendlier method to choose the data encryption key to use for data encryption." lightbox="media/security-configure-data-encryption/existing-server-select-key.png":::

1. Select **Select key**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-select-key.png" alt-text="Screenshot that shows how to select a data encryption key." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-select-key.png":::

1. **Subscription** is automatically populated with the name of the subscription on which your server is about to be created. The key store that keeps the data encryption key must exist in the same subscription as the server.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-subscription.png" alt-text="Screenshot that shows how to select the subscription in which the key store should exist." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-subscription.png":::

1. In **Key store type**, select the radio button corresponding to the type of key store in which you plan to store the data encryption key. In this example, we choose **Key vault**, but the experience is similar if you choose **Managed HSM**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-store-type.png" alt-text="Screenshot that shows how to select the type of store that keeps the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-store-type.png":::

1. Expand **Key vault** (or **Managed HSM**, if you selected that storage type), and select the instance where the data encryption key exists.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-vault.png" alt-text="Screenshot that shows how to select the key store that keeps the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-vault.png":::

    > [!NOTE]  
    > When you expand the dropdown box, it shows **No available items**. It takes a few seconds until it lists all the instances of key vault which are deployed in the same region as the server.

1. Expand **Key**, and select the name of the key that you want to use for data encryption.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-key.png" alt-text="Screenshot that shows how to select the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-key.png":::

1. If you didn't select **Use automatic key version update**, you must also select a specific version of the key. To do that, expand **Version**, and select the identifier of the version of the key that you want to use for data encryption.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-version.png" alt-text="Screenshot that shows how to select the version to use of the data encryption key." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-version.png":::

1. Select **Select**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-select.png" alt-text="Screenshot that shows how to select the chose key." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-select.png":::

1. Once satisfied with the changes made, select **Save**.

    :::image type="content" source="media/security-configure-data-encryption/existing-server-customer-assigned-key-save.png" alt-text="Screenshot that shows how to save the changes made to data encryption configuration." lightbox="media/security-configure-data-encryption/existing-server-customer-assigned-key-save.png":::

### [CLI](#tab/cli-customer-managed-server-existing)

You can configure data encryption with user assigned encryption key, for an existing server, via the [az postgres flexible-server update](/cli/azure/postgres/flexible-server#az-postgres-flexible-server-update) command.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --identity <managed_identity_to_access_primary_encryption_key> \
  --key <resource_identifier_of_primary_encryption_key> ...
```

> [!NOTE]  
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing server.

Whether you want to only change the user assigned managed identity used to access the key, or you want to only change the key used for data encryption, or you want to change both at the same time, you're required to provide both parameters `--identity` and `--key` (or `--backup-identity` and `--backup-key` for geo-redundant backups). If you provide either one but not both, you get any of the following errors:

```output
User assigned identity and keyvault key need to be provided together. Please provide --identity and --key together.
```

```output
User assigned identity and keyvault key need to be provided together. Please provide --backup-identity and --backup-key together.
```

If the key pointed by the value passed to the `--key` parameter (or `--backup-key` for geo-redundant backups) doesn't exist, or if the user assigned managed identity whose resource identifier is passed to the `--identity` parameter (ore `--backup-identity` for geo-redundant backups) doesn't have the required permissions to access the key, you get the following error:

```output
Code: AzureKeyVaultKeyNameNotFound
Message: The operation could not be completed because the Azure Key Vault Key name '<key_vault_resource>' does not exist or User Assigned Identity does not have Get access to the Key (/azure/postgresql/flexible-server/concepts-data-encryption#requirements-for-configuring-data-encryption-for-azure-database-for-postgresql-flexible-server).
```

If your server has geo-redundant backups enabled, you can configure the key used for encryption of geo-redundant backups, and the identity used to access that key. To do so, you can use the `--backup-identity` and `--backup-key` parameters.

```azurecli-interactive
az postgres flexible-server update \
  --resource-group <resource_group> \
  --name <server> \
  --backup-identity <managed_identity_to_access_georedundant_encryption_key> \
  --backup-key <resource_identifier_of_georedundant_encryption_key> ...
```

If you pass the parameters `--backup-identity` and `--backup-key` to the `az postgres flexible server update` command, and refer to an existing server which doesn't have geo-redundant backup enabled, you get the following error:

```output
Geo-redundant backup is not enabled. You cannot provide Geo-location user assigned identity and keyvault key.
```

Identities passed to the `--identity` and `--backup-identity` parameters, if they exist and are valid, are automatically added to the list of user assigned managed identities associated to your Azure Database for PostgreSQL flexible server instance. This is the case even if the command later fails with some other error. In such cases, you might want to use the [az postgres flexible-server identity](/cli/azure/postgres/flexible-server/identity) commands to list, assign, or remove user assigned managed identities assigned to your Azure Database for PostgreSQL flexible server instance. To learn more about configuring user assigned managed identities in your Azure Database for PostgreSQL flexible server instance, refer to [associate user assigned managed identities to existing servers](../security/security-configure-managed-identities-system-assigned.md#associate-user-assigned-managed-identities-to-existing-servers), [dissociate user assigned managed identities to existing servers](../security/security-configure-managed-identities-system-assigned.md#dissociate-user-assigned-managed-identities-to-existing-servers), and [show the associated user assigned managed identities](../security/security-configure-managed-identities-system-assigned.md#show-the-associated-user-assigned-managed-identities).

---

## Related content

- [Data encryption](../security/security-data-encryption.md)
