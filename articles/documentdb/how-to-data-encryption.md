---
title: Configure encryption at rest with customer-managed key in Azure DocumentDB
description: Learn how to configure encryption of data in Azure DocumentDB databases using service-managed and customer-managed encryption keys.
author: abinav2307
ms.author: abramees
ms.topic: how-to
ms.date: 10/13/2025
---

# Configure customer-managed key (CMK) for data encryption at rest for an Azure DocumentDB cluster

In this article, you learn how to configure [customer-managed key (CMK)](./database-encryption-at-rest.md) for data encryption at rest in Azure DocumentDB. The steps in this guide configure a new Azure DocumentDB cluster, a replica cluster, or a restored cluster. CMK setup uses customer-managed key stored in an Azure Key Vault and user-assigned managed identity. 

## Prerequisites

[!INCLUDE[Prerequisite - Azure subscription](includes/prerequisite-azure-subscription.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

## Prepare user-assigned managed identity and Azure Key Vault

To configure customer-managed key encryption on your Azure DocumentDB for MonogDB cluster, you need a user-assigned managed identity, an Azure Key Vault instance, and permissions properly configured.

> [!IMPORTANT]  
> User-assigned managed identity and Azure Key Vault instance used to configure CMK should be in the same Azure region where Azure DocumentDB cluster is hosted and all belong to the same [Microsoft tenant](/entra/identity-platform/developer-glossary#tenant).

Using the [Azure portal](https://portal.azure.com/):

1. [Create one user-assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities#create-a-user-assigned-managed-identity) in the cluster region, if you don't have one yet. 

1. [Create one Azure Key Vault](/azure/key-vault/general/quick-create-portal) in the cluster region, if you don't have one key store created yet. Make sure that you meet the [requirements](./database-encryption-at-rest.md#cmk-requirements). Also, follow the [recommendations](./database-encryption-at-rest.md#considerations) before you configure the key store, and before you create the key and assign the required permissions to the user-assigned managed identity. 

1. [Create one key in your key store](/azure/key-vault/keys/quick-create-portal#add-a-key-to-key-vault). 

1. Grant user-assigned managed identity permissions to the Azure Key Vault instance as outlined in [the requirements](./database-encryption-at-rest.md#cmk-requirements). 

## Configure data encryption with customer-managed key during cluster provisioning

### [Portal](#tab/portal-steps)

1. During provisioning of a new Azure DocumentDB cluster, service-managed or customer-managed keys for cluster data encryption is configured in the **Encryption** tab. Select the **Customer-managed key** for **Data encryption**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-with-customer-assigned-key.png" alt-text="Screenshot that shows how to select the customer-managed encryption key during cluster provisioning." lightbox="media/how-to-data-encryption/create-cluster-with-customer-assigned-key.png":::

1. In **User-assigned managed identity** section select **Change identity**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-customer-managed-key-select-managed-identity.png" alt-text="Screenshot that shows how to select the user-assigned managed identity to access the data encryption key." lightbox="media/how-to-data-encryption/create-cluster-customer-managed-key-select-managed-identity.png":::

1. In the list of user-assigned managed identities, select the one you want your cluster to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-with-customer-assigned-key.png" alt-text="Screenshot that shows how to select the user-assigned managed identity, which the cluster uses to access the data encryption key." lightbox="media/how-to-data-encryption/create-cluster-with-customer-assigned-key.png":::

1. Select **Add**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-customer-managed-key-add-managed-identity.png" alt-text="Screenshot that shows the location of the Add button to assign the identity, which the cluster uses to access the data encryption key." lightbox="media/how-to-data-encryption/create-cluster-customer-managed-key-add-managed-identity.png":::

1. In the **Key selection method**, choose **Select a key** .

1. In the **Key** section, select **Change key** .

    :::image type="content" source="media/how-to-data-encryption/create-cluster-customer-managed-key-change-key.png" alt-text="Screenshot that shows how to open the window to change the encryption key." lightbox="media/how-to-data-encryption/create-cluster-customer-managed-key-change-key.png":::

1. In the **Select a key** pane select the Azure Key Vault in the **Key vault** and encryption key in the **Key**, and confirm your choices by selecting **Select**.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-customer-managed-key-select-encryption-key.png" alt-text="Screenshot that shows how to select another encryption key." lightbox="media/how-to-data-encryption/create-cluster-customer-managed-key-select-encryption-key.png":::

    > [!IMPORTANT]  
    > Selected Azure Key Vault instance should be in the same Azure region where Azure DocumentDB cluster is going to be hosted.
    
1. Confirm selected user-assigned managed identity and encryption key on the **Encryption** tab and select **Review + create** to create cluster.

    :::image type="content" source="media/how-to-data-encryption/create-cluster-customer-managed-key-encryption-tab-with-selections.png" alt-text="Screenshot that shows completed Encryption tab and review + create button for cluster creation completion." lightbox="media/how-to-data-encryption/create-cluster-customer-managed-key-encryption-tab-with-selections.png":::

#### [REST APIs](#tab/rest-apis)

You can enable data encryption with user-assigned encryption key, while provisioning a new cluster, via an `az rest` command.

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

    > [!NOTE]  
    > The `keyEncryptionKeyUrl` should contain the key name but shouldn't contain [a specific key version](./database-encryption-at-rest.md#cmk-key-version-updates).
    
1. Run the following Azure CLI command to make a REST API call to create an Azure DocumentDB cluster. Replace placeholders in the variables section and the file name for the `--body` parameter in the `az rest` command line with the actual values. 

    ```powershell
    # Define your variables
    $randomIdentifier = (New-Guid).ToString().Substring(0,8)
    $subscriptionId="00000000-0000-0000-0000-000000000000"
    $resourceGroup="DocumentDB"
    $mongoClustersName="msdocscr$randomIdentifier"
        
    # Execute the az rest command to make REST API call
    az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-09-01 --body  @jsonFileFromThePreviousStep.json
    ```
    
---

## Update data encryption settings on cluster with CMK enabled

For existing clusters that were deployed with data encryption using a customer-managed key, you can do several configuration changes. You can change the key vault where the encryption key is stored and the encryption key used as a customer-managed key. You can also change the user-assigned managed identity used by the service to access the encryption key kept in the key store.

#### [Portal](#tab/portal-steps)

1. On the cluster sidebar, under **Settings**, select **Data encryption**.

1. In **User-assigned managed identity** section select **Change identity**.

    :::image type="content" source="media/how-to-data-encryption/cluster-management-user-assigned-managed-identity.png" alt-text="Screenshot that shows how to change the user-assigned managed identity to access the data encryption key on an existing cluster." lightbox="media/how-to-data-encryption/cluster-management-user-assigned-managed-identity.png":::

1. In the list of user-assigned managed identities, select the one you want your cluster to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/how-to-data-encryption/cluster-management-user-assigned-managed-identity-selection.png" alt-text="Screenshot that shows how to select the new user-assigned managed identity, which the cluster uses to access the data encryption key on existing cluster." lightbox="media/how-to-data-encryption/cluster-management-user-assigned-managed-identity-selection.png":::

1. Select **Add**.

1. In the **Key selection method**, choose **Select a key** .

1. In the **Key**, choose **Change key**.

    :::image type="content" source="media/how-to-data-encryption/cluster-management-encryption-key-change.png" alt-text="Screenshot that shows how to open the encryption key selection panel on an existing cluster." lightbox="media/how-to-data-encryption/cluster-management-encryption-key-change.png":::

1. In the **Select a key** pane select the Azure Key Vault in the **Key vault** and encryption key in the **Key**, and confirm your choices by selecting **Select**.

    :::image type="content" source="media/how-to-data-encryption/cluster-management-encryption-key-selection.png" alt-text="Screenshot that shows how to select new key vault and encryption key in that key vault to be used as a customer-managed key on an existing cluster." lightbox="media/how-to-data-encryption/cluster-management-encryption-key-selection.png":::

    > [!IMPORTANT]  
    > Selected Azure Key Vault instance should be in the same Azure region where Azure DocumentDB cluster is hosted.
    
1. Confirm selected user-assigned managed identity and encryption key on the **Data encryption** page and select **Save** to confirm your selections and create replica cluster.

    :::image type="content" source="media/how-to-data-encryption/cluster-management-save-changes.png" alt-text="Screenshot that shows the location of Save button for data encryption configuration changes on an existing cluster." lightbox="media/how-to-data-encryption/cluster-management-save-changes.png":::
 
#### [REST APIs](#tab/rest-apis)

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
    > [!NOTE]  
    > The `keyEncryptionKeyUrl` should contain the key name but shouldn't contain [a specific key version](./database-encryption-at-rest.md#cmk-key-version-updates).

1. Run the following Azure CLI command to make a REST API call to create an Azure DocumentDB cluster. Replace placeholders in the variables section and the file name for the `--body` parameter in the `az rest` command line with the actual values. 
    
    ```powershell
    # Define your variables
    $subscriptionId="00000000-0000-0000-0000-000000000000"
    $resourceGroup="resourceGroupName"
    $mongoClustersName="clusterName"
        
    # Execute the az rest command to make REST API call
    az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-09-01 --body  @jsonFileFromThePreviousStep.json
    ```
---

Whether you want to only change the user-assigned managed identity used to access the key, or you want to only change the key used for data encryption, or you want to change both at the same time, you're required to provide all parameters listed in the JSON file.

If the key or the user-assigned managed identity specified don't exist, you get the error.

Identities passed as parameters, if they exist and are valid, are automatically added to the list of user-assigned managed identities associated with your Azure DocumentDB cluster. This is the case even if the command later fails with some other error. 

## Change data encryption mode on existing clusters

The only point at which you can decide if you want to use a service-managed key or a customer-managed key (CMK) for data encryption, is at cluster creation time. Once you make that decision and create the cluster, you can't switch between the two options. To create a copy of your Azure DocumentDB cluster with a different encryption option, you can either [create a replica cluster](#enable-or-disable-customer-managed-key-cmk-data-encryption-during-replica-cluster-creation) or [perform a cluster restore](#enable-or-disable-customer-managed-key-cmk-data-encryption-during-cluster-restore) and select the new encryption mode during replica cluster or restored cluster creation.

### Enable or disable customer-managed key (CMK) data encryption during replica cluster creation

Follow these steps to create a replica cluster with CMK or SMK data encryption to enable or disable CMK on a replica cluster.

#### [Portal](#tab/portal-steps)

1. On the cluster sidebar, under **Settings**, select **Global distribution**.

1. Select **Add new read replica**.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster.png" alt-text="Screenshot that shows how to create a replica cluster for an existing one." lightbox="media/how-to-data-encryption/create-replica-cluster.png":::

1. Provide a replica cluster name in the **Read replica** name field.

1. Select a region in the **Read replica region**. The replica cluster is hosted in the selected Azure region.

    > [!NOTE]  
    > Replica cluster is always created in the same Azure subscription and resource group as its primary (read-write) cluster.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-name-and-region.png" alt-text="Screenshot that shows how to enter the replica cluster name and select Azure region for it." lightbox="media/how-to-data-encryption/create-replica-cluster-name-and-region.png":::

1. In **Data encryption** section, select the **Customer-managed key** to enable CMK or **Service-managed key** to disable CMK on the replica cluster.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-data-encryption-mode-selection.png" alt-text="Screenshot that shows how to select the customer-managed encryption key or service-managed encryption key during replica cluster creation." lightbox="media/how-to-data-encryption/create-replica-cluster-data-encryption-mode-selection.png":::

1. In **User-assigned managed identity** section select **Change identity**.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-user-assigned-managed-identity.png" alt-text="Screenshot that shows how to select the user-assigned managed identity to access the data encryption key during replica cluster creation." lightbox="media/how-to-data-encryption/create-replica-cluster-user-assigned-managed-identity.png":::

1. In the list of user-assigned managed identities, select the one you want your cluster to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-user-assigned-managed-identity-selection.png" alt-text="Screenshot that shows how to select the user-assigned managed identity, which the cluster uses to access the data encryption key, during replica cluster creation." lightbox="media/how-to-data-encryption/create-replica-cluster-user-assigned-managed-identity-selection.png":::

1. Select **Add**.

1. In the **Key selection method**, choose **Select a key** .

1. In the **Key**, choose **Change key**.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-encryption-key.png" alt-text="Screenshot that shows how to open the encryption key selection panel during replica cluster creation." lightbox="media/how-to-data-encryption/create-replica-cluster-encryption-key.png":::

1. In the **Select a key** pane select the Azure Key Vault in the **Key vault** and encryption key in the **Key**, and confirm your choices by selecting **Select**.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-key-vault-and-encryption-key-selection.png" alt-text="Screenshot that shows how to select key vault and encryption key in that key vault to be used as a customer-managed key during replica cluster creation." lightbox="media/how-to-data-encryption/create-replica-cluster-key-vault-and-encryption-key-selection.png":::

1. Confirm selected user-assigned managed identity and encryption key on the **Global distribution** page and select **Save** to confirm your selections and create replica cluster.

    :::image type="content" source="media/how-to-data-encryption/create-replica-cluster-confirmation-screen.png" alt-text="Screenshot that shows the location of Save button for replica cluster creation." lightbox="media/how-to-data-encryption/create-replica-cluster-confirmation-screen.png":::
 
#### [REST APIs](#tab/rest-apis)

To create a replica cluster with CMK enabled in the same region, follow these steps.

1. Create a JSON file with the following content. Replace placeholders that start with `$` sign with the actual values and save the file.

    ```json
    {
            "identity": {
                "type": "UserAssigned",
                "userAssignedIdentities": {
                  "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/$userAssignedIdentityName": {}
                }
              },
          "location": "$targetRegionName",
              "properties": {
              	"createMode": "GeoReplica",
                    "replicaParameters": {
                      "sourceResourceId": "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/$sourceClusterName",
                      "sourceLocation": "sourceRegionName"
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

    > [!NOTE]  
    > The `keyEncryptionKeyUrl` should contain the key name but shouldn't contain [a specific key version](./database-encryption-at-rest.md#cmk-key-version-updates).
    
1. Run the following Azure CLI command to make a REST API call to create an Azure DocumentDB cluster. Replace placeholders in the variables section and the file name for the `--body` parameter in the `az rest` command line with the actual values. 

    ```powershell
    # Define your variables
    $subscriptionId="00000000-0000-0000-0000-000000000000"
    $resourceGroup="resourceGroupName"
    $mongoClustersName="clusterName"
        
    # Execute the az rest command to make REST API call
    az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-09-01 --body  @jsonFileFromThePreviousStep.json
    ```
---

### Enable or disable customer-managed key (CMK) data encryption during cluster restore

The restore process creates a new cluster with the same configuration in the same Azure region, subscription, and resource group as the original. Follow these steps to create a restored cluster with CMK or SMK enabled.

#### [Portal](#tab/portal-steps)

1. Select an existing Azure DocumentDB cluster.
1. On the cluster sidebar, under **Settings**, select **Point In Time Restore**.
1. Select a date and provide a time (in UTC time zone) in the date and time fields.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-date-time.png" alt-text="Screenshot that shows how to select date and time for the cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-date-time.png":::

1. Enter a cluster name in the **Restore target cluster name** field. 

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-name.png" alt-text="Screenshot that shows how to enter cluster name for the cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-cluster-name.png":::

1. Enter a cluster admin name for the restored cluster in the **Admin user name** field.
1. Enter a password for the admin role in the **Password** and **Confirm password** fields.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-administrator-name-and-password.png" alt-text="Screenshot that shows how to administrative user name and  cluster name for the cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-cluster-administrator-name-and-password.png":::

1. In **Data encryption** section, select the **Customer-managed key** to enable CMK. If you need to have CMK disabled on the restored cluster, select **Service-managed key**.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-data-encryption-mode.png" alt-text="Screenshot that shows how to enable data encryption with customer-managed key for restored cluster." lightbox="media/how-to-data-encryption/cluster-restore-cluster-data-encryption-mode.png":::

1. In **User-assigned managed identity** section select **Change identity**.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-user-assigned-change-identity-selection.png" alt-text="Screenshot that shows how to select the user-assigned managed identity to access the data encryption key during cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-cluster-user-assigned-change-identity-selection.png":::

1. In the list of user-assigned managed identities, select the one you want your cluster to use to access the data encryption key stored in an Azure Key Vault.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-user-assigned-managed-identity-add.png" alt-text="Screenshot that shows how to select the user-assigned managed identity, which the cluster uses to access the data encryption key, during cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-cluster-user-assigned-managed-identity-add.png":::

1. Select **Add**.

1. In the **Key selection method**, choose **Select a key** .

1. In the **Key**, choose **Change key**.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-encryption-key.png" alt-text="Screenshot that shows how to open the encryption key selection panel during cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-cluster-encryption-key.png":::

1. In the **Select a key** pane select the Azure Key Vault in the **Key vault** and encryption key in the **Key**, and confirm your choices by selecting **Select**.

    :::image type="content" source="media/how-to-data-encryption/cluster-restore-cluster-key-vault-and-encryption-key-selection.png" alt-text="Screenshot that shows how to select key vault and encryption key in that key vault to be used as a customer-managed key during cluster restore." lightbox="media/how-to-data-encryption/cluster-restore-cluster-key-vault-and-encryption-key-selection.png":::

1. Select **Submit** to initiate cluster restore.

#### [REST APIs](#tab/rest-apis)

To restore a cluster with CMK enabled, follow these steps.

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
                  "userName": "$adminName"
                },
          	"createMode": "PointInTimeRestore",
                "restoreParameters": {
                  "pointInTimeUTC": "yyyy-mm-ddThh:mm:ssZ",
                  "sourceResourceId": "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/$restoredClusterName"
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

    > [!NOTE]  
    > The `keyEncryptionKeyUrl` should contain the key name but shouldn't contain [a specific key version](./database-encryption-at-rest.md#cmk-key-version-updates).

1. Run the following Azure CLI command to make a REST API call to create an Azure DocumentDB cluster. Replace placeholders in the variables section and the file name for the `--body` parameter in the `az rest` command line with the actual values. 

    ```powershell
    # Define your variables
    $subscriptionId="00000000-0000-0000-0000-000000000000"
    $resourceGroup="resourceGroupName"
    $mongoClustersName="clusterName"
        
    # Execute the az rest command to make REST API call
    az rest --method "PUT" --url https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.DocumentDB/mongoClusters/${mongoClustersName}?api-version=2025-09-01 --body  @jsonFileFromThePreviousStep.json
    ```

---

Once restored cluster is created, review the list of [post-restore tasks](./how-to-restore-cluster.md#post-restore-tasks).

## Related content

- [Learn about data encryption at rest in Azure DocumentDB](./database-encryption-at-rest.md)
- [Troubleshoot CMK setup](./how-to-database-encryption-troubleshoot.md)
- Check out [CMK limitations](./limitations.md#customer-managed-key-data-encryption-limitations)
- [Migrate data to Azure DocumentDB](./migration-options.md)
