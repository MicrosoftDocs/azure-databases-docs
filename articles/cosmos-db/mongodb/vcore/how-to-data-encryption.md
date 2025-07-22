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

1. [Create one Azure Key Vault](/azure/key-vault/general/quick-create-portal), if you don't have one key store created yet. Make sure that you meet the [requirements](./database-encryption-at-rest.md#cmk-requirements). Also, follow the [recommendations](./database-encryption-at-rest.md#considerations) before you configure the key store, and before you create the key and assign the required permissions to the user-assigned managed identity. 

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

You can enable data encryption with user-assigned encryption key, while provisioning a new cluster, via an az rest command.

1. Create a JSON file with the following content. Replace placeholders that start with `$` sign with the actual values and save the file.

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
1. Run the following Azure CLI command to make a REST API call to create an Azure Cosmos DB for MongoDB vCore cluster. Replace placeholders in the variables section and the file name for the `--body` parameter in the `az rest` command line with the actual values. 

    ```powershell
    # Define your variables
    $randomIdentifier = (New-Guid).ToString().Substring(0,8)
    $subscriptionId="00000000-0000-0000-0000-000000000000"
    $resourceGroup="AzureCosmosDB"
    $mongoClustersName="msdocscr$randomIdentifier"
    $locationName="westus"
    
    # Execute the az rest command to make REST API call
    az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-07-01-preview --body  @jsonFileFromThePreviousStep.json
    ```
    
---

## Update settings for encryption on cluster with CMK

For existing clusters that were deployed with data encryption using a customer-managed key, you can do several configuration changes. Things that can be changed are the references to the keys used for encryption, and references to the user-assigned managed identities used by the service to access the keys kept in the key stores.

You must update references that your Azure Cosmos DB for MongoDB vCore cluster has to a key:
- When the key stored in the key store is rotated either manually or automatically. 
- When you want to use the same or a different key stored in a different key store.

You must update the user-assigned managed identities which are used by your Azure Cosmos DB for MongoDB vCore cluster to access the encryption keys:
- Whenever you want to use a different identity.

You can change user-assigned managed identity and encryption key for data encryption on an existing cluster via a REST API call.

1. Create a JSON file with the following content. Replace placeholders that start with `$` sign with the actual values and save the file.

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
1. Run the following Azure CLI command to make a REST API call to create an Azure Cosmos DB for MongoDB vCore cluster. Replace placeholders in the variables section and the file name for the `--body` parameter in the `az rest` command line with the actual values. 

    ```powershell
    # Define your variables
    $subscriptionId="00000000-0000-0000-0000-000000000000"
    $resourceGroup="resourceGroupName"
    $mongoClustersName="clusterName"
    $locationName="regionName"
    
    # Execute the az rest command to make REST API call
    az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-07-01-preview --body  @jsonFileFromThePreviousStep.json
    ```

Whether you want to only change the user-assigned managed identity used to access the key, or you want to only change the key used for data encryption, or you want to change both at the same time, you're required to provide all parameters listed in the JSON file.

If the key or the user-assigned managed identity specified don't exist, you get the error.

Identities passed as parameters, if they exist and are valid, are automatically added to the list of user-assigned managed identities associated with your Azure Cosmos DB for MongoDB vCore cluster. This is the case even if the command later fails with some other error. 

## Change data encryption mode on existing clusters

The only point at which you can decide if you want to use a service-managed key or a customer-managed key (CMK) for data encryption, is at cluster creation time. Once you make that decision and create the cluster, you can't switch between the two options. To create a copy of your Azure Cosmos DB for MongoDB vCore cluster with a different encryption option, you can either create a replica cluster or perform a cluster restore and select the new encryption mode during replica cluster or restored cluster creation.

## Limitations

The following are the current limitations for configuring the customer-managed key in an Azure Cosmos DB for MongoDB vCore:

- The instance of Azure Key Vault where you plan to store the encryption key and user-assigned managed identity must be in the same region and in the same Microsoft tenant as the Azure Cosmos DB for MongoDB vCore cluster.
- After you configure customer-managed key encryption, you can't revert back to system-managed key.

## Related content

- [Learn about data encryption at rest in Azure Cosmos DB for MongoDB vCore](./database-encryption-at-rest.md)
- [Migrate data to Azure Cosmos DB for MongoDB vCore](./migration-options.md)