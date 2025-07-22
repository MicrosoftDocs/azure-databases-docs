---
title: Configure encryption at rest with customer-managed key in Azure Cosmos DB for MongoDB vCore
description: Learn how to configure encryption of data in Azure Cosmos DB for MongoDB vCore databases using service-managed and customer-managed encryption keys.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 07/13/2025
appliesto:
  - ✅ MongoDB (vCore)
---

# Configure customer-managed key for data encryption at rest for an Azure Cosmos DB for MongoDB vCore cluster

[!INCLUDE[MongoDB vCore](./includes/notice-customer-managed-key-preview.md)]

In this article, you learn how to configure [customer-managed key (CMK)](./database-encryption-at-rest.md) for data encryption at rest in Azure Cosmos DB for MongoDB vCore. The steps in this guide configure a new Azure Cosmos DB for MongoDB vCore cluster, a replica cluster, or a restored cluster with customer-managed key stored in an Azure Key Vault and user-assigned managed identity. 

## Prerequisites

[!INCLUDE[Prerequisite - Azure subscription](includes/prereq-azure-subscription.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

## Prepare user-assigned managed identity and Azure Key Vault (AKV)

To configure customer-managed key encryption on your Azure Cosmos DB for MonogDB vCore cluster you need a user-assigned managed identity, an Azure Key Vault instance, and permissions properly configured.

> [!IMPORTANT]  
> User-managed identity and Azure Key Vault instance used to configure CMK should be in the same Azure region where Azure Cosmos DB for MongoDB cluster is hosted and all belong to the same [Microsoft tenant](/entra/identity-platform/developer-glossary#tenant).

Using the [Azure portal](https://portal.azure.com/):

1. [Create one user-assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities#create-a-user-assigned-managed-identity), if you don't have one yet. 

1. [Create one Azure Key Vault](/azure/key-vault/general/quick-create-portal), if you don't have one key store created yet. Make sure that you meet the [requirements](./database-encryption-at-rest.md#cmk-requirements). Also, follow the [recommendations](./database-encryption-at-rest.md#considerations) before you configure the key store, and before you create the key and assign the required permissions to the user assigned managed identity. 

1. [Create one key in your key store](/azure/key-vault/keys/quick-create-portal#add-a-key-to-key-vault). 

1. Grant user-assigned managed identity permissions to the AKV instance as outlined in [the requirements](./database-encryption-at-rest.md#cmk-requirements). 

## Configure data encryption with customer-managed key during cluster provisioning

### [Portal](#tab/portal-customer-managed-cluster-provisioning)

1. During provisioning of a new Azure Cosmos DB for MongoDB vCore cluster, service-managed or customer-managed keys for cluster data encryption is configured in the **Encryption** tab. Select the **Customer-managed key** for **Data encryption**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-with-customer-assigned-key.png" alt-text="Screenshot that shows how to select the customer-managed encryption key during cluster provisioning.":::

1. In **User-assigned managed identity** section select **Change identity**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-cmk-select-managed-identity.png" alt-text="Screenshot that shows how to select the user-assigned managed identity to access the data encryption key.":::

1. In the list of user-assigned managed identities, select the one you want your cluster to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-with-customer-assigned-key.png" alt-text="Screenshot that shows how to select the user-assigned managed identity with which the cluster uses to access the data encryption key.":::

1. Select **Add**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-cmk-add-managed-identity.png" alt-text="Screenshot that shows the location of the Add button to assign the identity which the cluster uses to access the data encryption key.":::

1. In the **Key selection method** choose **Select a key** .

1. In the **Key** section select **Change key** .

    :::image type="content" source="media/how-to-data-encryption/create-cluster-cmk-change-key.png" alt-text="Screenshot that shows how to open the window for encryption key selection.":::

1. In the **Select a key** pane select the Azure Key Vault in the **Key vault**, encryption key in the **Key**, the key version to be used for encryption in the **Version**, and confirm your choices by selecting **Select**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-cmk-select-encryption-key.png" alt-text="Screenshot that shows how to open the window for encryption key selection.":::

1. Confirm selected user-assigned managed identity and encryption key on the **Encryption** tab and select **Review + create** to create cluster.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-cmk-encryption-tab-with-selections.png" alt-text="Screenshot that shows completed Encryption tab and review + create button for cluster creation completion.":::

### [CLI](#tab/cli-customer-managed-cluster-provisioning)

You can enable data encryption with user assigned encryption key, while provisioning a new cluster, via an az rest command.

1. Create a save a JSON file with the following content:

```json
{
    "identity": {
        "type": "UserAssigned",
        "userAssignedIdentities": {
          "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/$userAssignedIdentityName": {}
        }
      },
  "location": "$regionName",
      "properties": {
        "administrator": {
          "userName": "$adminName",
          "password": "$complexPassword"
        },
        "serverVersion": "8.0",
        "storage": {
          "sizeGb": 32
        },
        "compute": {
          "tier": "M40"
        },
        "sharding": {
          "shardCount": 1
        },
        "highAvailability": {
          "targetMode": "ZoneRedundantPreferred"
        },
      "encryption": {
          "customerManagedKeyEncryption": {
            "keyEncryptionKeyIdentity": {
              "identityType": "UserAssignedIdentity",
              "userAssignedIdentityResourceId": "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/$userAssignedIdentityName"
            },
            "keyEncryptionKeyUrl": "$encryptionKeyUrl"
          }
        }
      }
}
```
1. Run the following Azure CLI command to make a REST API call to create an Azure Cosmos DB for MongoDB vCore cluster:


```powershell
# Define your variables
$randomIdentifier = (New-Guid).ToString().Substring(0,8)
$subscriptionId="00000000-0000-0000-0000-000000000000"
$resourceGroup="AzureCosmosDB"
$mongoClustersName="msdocscr$randomIdentifier"
$locationName="westus"

# Execute the az rest command to make REST API call
az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-07-01-preview --body  --@jsonFileFromThePreviousStep.json
```

---

## Configure data encryption with customer-managed key on existing clusters

The only point at which you can decide if you want to use a service-managed key or a customer-managed key for data encryption, is at cluster creation. Once you make that decision and create the cluster, you can't switch between the two options. The only alternative, if you want to change from one to the other, requires [restoring any of the backups available of cluster onto a new cluster](how-to-restore-latest-restore-point.md). While configuring the restore, you're allowed to change the data encryption configuration of the new cluster.

For existing clusters that were deployed with data encryption using a customer-managed key, you're allowed to do several configuration changes. Things that can be changed are the references to the keys used for encryption, and references to the user assigned managed identities used by the service to access the keys kept in the key stores.

You must update references that your Azure Cosmos DB for MongoDB vCore cluster has to a key:
- When the key stored in the key store is rotated, either manually or automatically, and your Azure Cosmos DB for MongoDB vCore cluster is pointing to a specific version of the key. If you're pointing to a key, but not to a specific version of the key (that's when you have **Use automatic key version update** enabled), then the service will take care of automatically reference the most current version of the key, whenever they key is manually or automatically rotated.
- When you want to use the same or a different key stored in a different key store.

You must update the user assigned managed identities which are used by your Azure Cosmos DB for MongoDB vCore cluster to access the encryption keys:
- Whenever you want to use a different identity.

### [Portal](#tab/portal-customer-managed-cluster-existing)

Using the [Azure portal](https://portal.azure.com/):

1. Select your Azure Cosmos DB for MongoDB vCore cluster.

1. In the resource menu, under **Security**, select **Data encryption**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-data-encryption.png" alt-text="Screenshot that shows how to get to the Data encryption for an existing cluster." lightbox="media/how-to-data-encryption/existing-cluster-data-encryption.png":::

1. To change the user assigned managed identity with which the cluster accesses the key store in which the key is kept, expand the **User assigned managed identity** dropdown, and select any of the identities available.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-select-managed-identity.png" alt-text="Screenshot that shows how to select one of the user assigned managed identities associated to the cluster." lightbox="media/how-to-data-encryption/existing-cluster-select-managed-identity.png":::

    > [!NOTE]  
    > Identities shown in the combo-box are only the ones that your Azure Cosmos DB for MongoDB vCore cluster was assigned.
    > Although it isn't required, to maintain regional resiliency, we recommend that you select user managed identities in the same region as your cluster. And if your cluster has geo-backup redundancy enabled, we recommend that the second user managed identity, used to access the data encryption key for geo-redundant backups, exists in the [paired region](/azure/reliability/cross-region-replication-azure) of the cluster.

1. If the user assigned managed identity that you want to use to access the data encryption key isn't assigned to your Azure Cosmos DB for MongoDB vCore cluster, and it doesn't even exist as an Azure resource with its corresponding object in Microsoft Entra ID, you can create it by selecting **Create**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-create-new-managed-identity.png" alt-text="Screenshot that shows how to create a new user assigned managed identities in Azure and Microsoft Entra ID, automatically assign it to your Azure Cosmos DB for MongoDB vCore cluster, and use it to access the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-create-new-managed-identity.png":::

1. In the **Create user-assigned managed Identity** panel, complete the details of the user assigned managed identity that you want to create, and automatically assign to your Azure Cosmos DB for MongoDB vCore cluster to access the data encryption key.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-create-new-managed-identity-details.png" alt-text="Screenshot that shows how to provide the details for the new user assigned managed identity." lightbox="media/how-to-data-encryption/existing-cluster-create-new-managed-identity-details.png":::

1. If the user assigned managed identity that you want to use to access the data encryption key isn't assigned to your Azure Cosmos DB for MongoDB vCore cluster, but it does exist as an Azure resource with its corresponding object in Microsoft Entra ID, you can assign it by selecting **Select**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-select-existing-managed-identity.png" alt-text="Screenshot that shows how to select an existing user assigned managed identity in Azure and Microsoft Entra ID, automatically assign it to your Azure Cosmos DB for MongoDB vCore cluster, and use it to access the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-select-existing-managed-identity.png":::

1. Among the list of user assigned managed identities, select the one you want your cluster to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-select-existing-managed-identity-details.png" alt-text="Screenshot that shows how to select an existing user assigned managed identity to assign it to your Azure Cosmos DB for MongoDB vCore cluster, and use it to access the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-select-existing-managed-identity-details.png":::

1. Select **Add**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-select-existing-managed-identity-details-add.png" alt-text="Screenshot that shows how to add the selected user assigned managed identity." lightbox="media/how-to-data-encryption/existing-cluster-select-existing-managed-identity-details-add.png":::

1. Select **Use automatic key version update**, if you prefer to let the service automatically update the reference to the most current version of the chosen key, whenever the current version is rotated manually or automatically. To understand the benefits of using automatic key version updates, see [automatic key version update](concepts-data-encryption.md##CMK key version updates).

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-version-less.png" alt-text="Screenshot that shows how to enable automatic key version updates." lightbox="media/how-to-data-encryption/existing-cluster-version-less.png":::

1. If you rotate the key and don't have **Use automatic key version update** enabled. Or if you want to use a different key, you must update your Azure Cosmos DB for MongoDB vCore cluster, so that it points to the new key version or new key. To do that, you can copy the resource identifier of the key, and paste it in the **Key identifier** box.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-paste-key-identifier.png" alt-text="Screenshot that shows where to paste the resource identifier of the new key or new key version that the cluster must use for data encryption." lightbox="media/how-to-data-encryption/existing-cluster-paste-key-identifier.png":::

1. If the user accessing Azure portal has permissions to access the key stored in the key store, you can use an alternative approach to choose the new key or new key version. To do that, in **Key selection method**, select the **Select a key** radio button.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-select-key.png" alt-text="Screenshot that shows how to enable the user friendlier method to choose the data encryption key to use for data encryption." lightbox="media/how-to-data-encryption/existing-cluster-select-key.png":::

1. Select **Select key**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-select-key.png" alt-text="Screenshot that shows how to select a data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-select-key.png":::

1. **Subscription** is automatically populated with the name of the subscription on which your cluster is about to be created. The key store that keeps the data encryption key must exist in the same subscription as the cluster.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-subscription.png" alt-text="Screenshot that shows how to select the subscription in which the key store should exist." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-subscription.png":::

1. In **Key store type**, select the radio button corresponding to the type of key store in which you plan to store the data encryption key. In this example, we choose **Key vault**, but the experience is similar if you choose **Managed HSM**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-store-type.png" alt-text="Screenshot that shows how to select the type of store that keeps the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-store-type.png":::

1. Expand **Key vault** (or **Managed HSM**, if you selected that storage type), and select the instance where the data encryption key exists.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-vault.png" alt-text="Screenshot that shows how to select the key store that keeps the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-vault.png":::

    > [!NOTE]  
    > When you expand the dropdown box, it shows **No available items**. It takes a few seconds until it lists all the instances of key vault which are deployed in the same region as the cluster.

1. Expand **Key**, and select the name of the key that you want to use for data encryption.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-key.png" alt-text="Screenshot that shows how to select the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-key.png":::

1. If you didn't select **Use automatic key version update**, you must also select a specific version of the key. To do that, expand **Version**, and select the identifier of the version of the key that you want to use for data encryption.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-version.png" alt-text="Screenshot that shows how to select the version to use of the data encryption key." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-version.png":::

1. Select **Select**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-select.png" alt-text="Screenshot that shows how to select the chose key." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-select.png":::

1. Once satisfied with the changes made, select **Save**.

    :::image type="content" source="media/how-to-data-encryption/existing-cluster-customer-assigned-key-save.png" alt-text="Screenshot that shows how to save the changes made to data encryption configuration." lightbox="media/how-to-data-encryption/existing-cluster-customer-assigned-key-save.png":::

### [CLI](#tab/cli-customer-managed-cluster-existing)

You can configure data encryption with user assigned encryption key, for an existing cluster, via the [az postgres flexible-cluster update](/cli/azure/postgres/flexible-cluster#az-postgres-flexible-cluster-update) command.

```azurecli-interactive
az postgres flexible-cluster update \
  --resource-group <resource_group> \
  --name <cluster> \
  --identity <managed_identity_to_access_primary_encryption_key> \
  --key <resource_identifier_of_primary_encryption_key> ...
```

> [!NOTE]  
> The previous command might need to be completed with other parameters whose presence and values would vary depending on how you want to configure other features of the existing cluster.

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
Message: The operation could not be completed because the Azure Key Vault Key name '<key_vault_resource>' does not exist or User Assigned Identity does not have Get access to the Key (/azure/postgresql/flexible-cluster/concepts-data-encryption#requirements-for-configuring-data-encryption-for-azure-database-for-postgresql-flexible-cluster).
```

If your cluster has geo-redundant backups enabled, you can configure the key used for encryption of geo-redundant backups, and the identity used to access that key. To do so, you can use the `--backup-identity` and `--backup-key` parameters.

```azurecli-interactive
az postgres flexible-cluster update \
  --resource-group <resource_group> \
  --name <cluster> \
  --backup-identity <managed_identity_to_access_georedundant_encryption_key> \
  --backup-key <resource_identifier_of_georedundant_encryption_key> ...
```

If you pass the parameters `--backup-identity` and `--backup-key` to the `az postgres flexible cluster update` command, and refer to an existing cluster which doesn't have geo-redundant backup enabled, you get the following error:

```output
Geo-redundant backup is not enabled. You cannot provide Geo-location user assigned identity and keyvault key.
```

Identities passed to the `--identity` and `--backup-identity` parameters, if they exist and are valid, are automatically added to the list of user assigned managed identities associated to your Azure Cosmos DB for MongoDB vCore cluster. This is the case even if the command later fails with some other error. In such cases, you might want to use the [az postgres flexible-cluster identity](/cli/azure/postgres/flexible-cluster/identity) commands to list, assign, or remove user assigned managed identities assigned to your Azure Cosmos DB for MongoDB vCore cluster. To learn more about configuring user assigned managed identities in your Azure Cosmos DB for MongoDB vCore cluster, refer to [associate user assigned managed identities to existing clusters](how-to-configure-managed-identities.md#associate-user-assigned-managed-identities-to-existing-clusters), [dissociate user assigned managed identities to existing clusters](how-to-configure-managed-identities.md#dissociate-user-assigned-managed-identities-to-existing-clusters), and [show the associated user assigned managed identities](how-to-configure-managed-identities.md#show-the-associated-user-assigned-managed-identities).

---



## Related content

- [Learn about data encryption at rest in Azure Cosmos DB for MongoDB vCore](./database-encryption-at-rest.md)
- [Migrate data to Azure Cosmos DB for MongoDB vCore](./migration-options.md)