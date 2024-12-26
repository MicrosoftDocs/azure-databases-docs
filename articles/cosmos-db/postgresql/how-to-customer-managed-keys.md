---
title: How to enable encryption with customer-managed keys in Azure Cosmos DB for PostgreSQL.
description: Steps to enable data encryption with customer-managed keys.
ms.author: akashrao
author: akashraokm
ms.service: azure-cosmos-db
ms.subservice: postgresql
ms.topic: how-to
ms.date: 01/03/2024
---
# Enable data encryption with customer-managed keys in Azure Cosmos DB for PostgreSQL

[!INCLUDE [PostgreSQL](../includes/appliesto-postgresql.md)]

## Prerequisites

- An existing Azure Cosmos DB for PostgreSQL account.
  - If you have an Azure subscription, [create a new account](../nosql/how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.
  - Alternatively, you can [try Azure Cosmos DB free](../try-free.md) before you commit.

## Enable data encryption with customer-managed keys

> [!IMPORTANT]
> Create all the following resources in the same region where your Azure Cosmos DB for PostgreSQL cluster will be deployed.

1. Create a user-assigned managed identity. Currently, Azure Cosmos DB for PostgreSQL only supports user-assigned managed identities.

1. Create an Azure Key Vault and add an access policy to the created User-Assigned Managed Identity with the following key permissions: Get, Unwrap Key, and Wrap Key.

1. Generate a key in the key vault (supported key types: RSA 2048, 3071, 4096).

1. Select the customer-managed key encryption option during the creation of the Azure Cosmos DB for PostgreSQL cluster and select the appropriate user-assigned managed identity, key vault, and key created in steps 1, 2, and 3.

## Detailed steps

### User-assigned managed identity

1. Search for **Managed identities** in the global search bar.

   ![Screenshot of Managed Identities in Azure portal.](media/how-to-customer-managed-keys/user-assigned-managed-identity.png)


1. Create a new user assigned managed identity in the same region as your Azure Cosmos DB for PostgreSQL cluster.

   ![Screenshot of User assigned managed Identity page in Azure portal.](media/how-to-customer-managed-keys/user-assigned-managed-identity-provisioning.png)


Learn more about [user-assigned managed identity](/azure/active-directory/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp#create-a-user-assigned-managed-identity).

### Key Vault

Using customer-managed keys with Azure Cosmos DB for PostgreSQL requires you to set two properties on the Azure Key Vault instance that you plan to use to host your encryption keys: Soft Delete and Purge Protection.

1. If you create a new Azure Key Vault instance, enable these properties during creation:

   [ ![Screenshot of Key Vault's properties.](media/how-to-customer-managed-keys/key-vault-soft-delete.png) ](media/how-to-customer-managed-keys/key-vault-soft-delete.png#lightbox)
 
1. If you're using an existing Azure Key Vault instance, you can verify that these properties are enabled by looking at the Properties section on the Azure portal. If any of these properties aren’t enabled, see the "Enabling soft delete" and "Enabling Purge Protection" sections in one of the following articles.

   * How to use [soft-delete with PowerShell.](/azure/key-vault/general/key-vault-recovery)
   * How to use [soft-delete with Azure CLI.](/azure/key-vault/general/key-vault-recovery)

1. The key Vault must be set with 90 days for **Days to retain deleted vaults**. If the existing key Vault is configured with a lower number, you'll need to create a new key vault as this setting can't be modified after creation.

   > [!IMPORTANT]
   > Your Azure Key Vault instance must allow public access from all networks.

### Add an Access Policy to the Key Vault

1. From the Azure portal, go to the Azure Key Vault instance that you plan to use to host your encryption keys. Select Access configuration from the left menu. 
Make sure <b>Vault access policy</b> is selected under Permission model and then select Go to access policies.

   [ ![Screenshot of Key Vault's access configuration.](media/how-to-customer-managed-keys/access-policy.png) ](media/how-to-customer-managed-keys/access-policy.png#lightbox)

1. Select + Create.

1. In the Permissions Tab under the Key permissions drop-down menu, select Get, Unwrap Key, and Wrap Key permissions.

   [ ![Screenshot of Key Vault's permissions settings.](media/how-to-customer-managed-keys/access-policy-permissions.png) ](media/how-to-customer-managed-keys/access-policy-permissions.png#lightbox)

1. In the Principal Tab, select the User Assigned Managed Identity you created in prerequisite step.

1. Navigate to Review + create select Create.

### Create / Import Key

1. From the Azure portal, go to the Azure Key Vault instance that you plan to use to host your encryption keys.

1. Select Keys from the left menu and then select +Generate/Import.

   [ ![Screenshot of Key generation page.](media/how-to-customer-managed-keys/create-key.png) ](media/how-to-customer-managed-keys/create-key.png#lightbox)

1. The customer-managed key to be used for encrypting the DEK can only be asymmetric RSA Key type. All RSA Key sizes 2048, 3072 and 4096 are supported.

1. The key activation date (if set) must be a date and time in the past. The expiration date (if set) must be a future date and time.

1. The key must be in the Enabled state.

1. If you're importing an existing key into the key vault, make sure to provide it in the supported file formats (`.pfx`, `.byok`, `.backup`).

1. If you're manually rotating the key, the old key version shouldn't  be deleted for at least 24 hours.

### Enable CMK encryption during the provisioning of a new cluster

   # [Portal](#tab/portal)

   1. During the provisioning of a new Azure Cosmos DB for PostgreSQL cluster, after providing the necessary information under Basics and Networking tabs, navigate to the **Encryption** tab.
     [ ![Screenshot of Encrytion configuration page.](media/how-to-customer-managed-keys/encryption-tab.png)](media/how-to-customer-managed-keys/encryption-tab.png#lightbox)

   1. Select **Customer-managed key** under **Data encryption key** option.

   1. Select the user assigned managed identity created in the previous section.
     
   1. Select the key vault created in the previous step, which has the access policy to the user managed identity selected in the previous step.

   1. Select the key created in the previous step, and then select **Review + create**.

   1. Once the cluster is created, verify that CMK encryption is enabled by navigating to the **Data Encryption** blade of the Azure Cosmos DB for PostgreSQL cluster in the Azure portal.
      ![Screenshot of data encryption tab.](media/how-to-customer-managed-keys/data-encryption-tab-note.png)

   > [!NOTE]
   > Data encryption can only be configured during the creation of a new cluster and can't be updated on an existing cluster. A workaround for updating the encryption configuration on an existing cluster is to perform a [cluster restore](./howto-restore-portal.md) and configure the data encryption during the creation of the newly restored cluster.

   # [ARM Template](#tab/arm)
 ```json
    {
        "$schema": "http://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "serverGroupName": {
                "type": "string"
            },
            "location": {
                "type": "string"
            },
            "administratorLoginPassword": {
                "type": "secureString"
            },
            "previewFeatures": {
                "type": "bool"
            },
            "postgresqlVersion": {
                "type": "string"
            },
            "coordinatorVcores": {
                "type": "int"
            },
            "coordinatorStorageSizeMB": {
                "type": "int"
            },
            "numWorkers": {
                "type": "int"
            },
            "workerVcores": {
                "type": "int"
            },
            "workerStorageSizeMB": {
                "type": "int"
            },
            "enableHa": {
                "type": "bool"
            },
            "enablePublicIpAccess": {
                "type": "bool"
            },
            "serverGroupTags": {
                "type": "object"
            },
            "userAssignedIdentityUrl": {
                "type": "string"
            },
            "encryptionKeyUrl": {
                "type": "string"
            }
        },
        "variables": {},
        "resources": [
            {
                "name": "[parameters('serverGroupName')]",
                "type": "Microsoft.DBforPostgreSQL/serverGroupsv2",
                "kind": "CosmosDBForPostgreSQL",
                "apiVersion": "2020-10-05-privatepreview",
                "identity":
                {
                    "type": "UserAssigned",
                    "userAssignedIdentities":
                    {
                        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/yogkuleuapcmkmarlintest/providers/Microsoft.ManagedIdentity/userAssignedIdentities/marlincmktesteus2euapuai1": {}
                    }
                },
                "location": "[parameters('location')]",
                "tags": "[parameters('serverGroupTags')]",
                "properties": {
                    "createMode": "Default",
                    "administratorLogin": "citus",
                    "administratorLoginPassword": "[parameters('administratorLoginPassword')]",
                    "backupRetentionDays": 35,
                    "enableMx": false,
                    "enableZfs": false,
                    "previewFeatures": "[parameters('previewFeatures')]",
                    "postgresqlVersion": "[parameters('postgresqlVersion')]",
                    "dataencryption":
                    {
                        "primaryKeyUri": "[parameters('encryptionKeyUrl')]",
                        "primaryUserAssignedIdentityId": "[parameters('userAssignedIdentityUrl')]",
                        "type": "AzureKeyVault"
                    },
                    "serverRoleGroups": [
                        {
                            "name": "",
                            "role": "Coordinator",
                            "serverCount": 1,
                            "serverEdition": "GeneralPurpose",
                            "vCores": "[parameters('coordinatorVcores')]",
                            "storageQuotaInMb": "[parameters('coordinatorStorageSizeMB')]",
                            "enableHa": "[parameters('enableHa')]"
                        },
                        {
                            "name": "",
                            "role": "Worker",
                            "serverCount": "[parameters('numWorkers')]",
                            "serverEdition": "MemoryOptimized",
                            "vCores": "[parameters('workerVcores')]",
                            "storageQuotaInMb": "[parameters('workerStorageSizeMB')]",
                            "enableHa": "[parameters('enableHa')]",
                            "enablePublicIpAccess": "[parameters('enablePublicIpAccess')]"
                        }
                    ]
                },
                "dependsOn": []
            }
        ],
        "outputs": {}
    }
 ```
---

### High availability

   When CMK encryption is enabled on the primary cluster, all HA standby nodes are automatically encrypted by the primary cluster’s key.

### Changing encryption configuration by performing a PITR

Encryption configuration can be changed from service-managed encryption to customer-managed encryption or vice versa while performing a cluster restore operation (PITR - point-in-time restore).

# [Portal](#tab/portal)

  1. Navigate to the **Data encryption** blade, and select **Initiate restore operation**. Alternatively, you can perform PITR by selecting the **Restore** option in the **Overview** blade.
   [ ![Screenshot of PITR.](media/how-to-customer-managed-keys/point-in-time-restore.png)](media/how-to-customer-managed-keys/point-in-time-restore.png#lightbox)

  1. You can change/configure the data encryption on the **Encryption** tab of the cluster restore page.

# [ARM Template](#tab/arm)

 ```json
    {
        "$schema": "http://schema.management.azure.com/schemas/2014-04-01-preview/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "location": {
                "type": "string"
            },
            "sourceLocation": {
                "type": "string"
            },
            "subscriptionId": {
                "type": "string"
            },
            "resourceGroupName": {
                "type": "string"
            },
            "serverGroupName": {
                "type": "string"
            },
            "sourceServerGroupName": {
                "type": "string"
            },
            "restorePointInTime": {
                "type": "string"
            },
            "encryptionKeyUrl": {
                "type": "string"
            },
            "userAssignedIdentityUrl": {
                "type": "string"
            }
        },
        "variables": {
            "api": "2020-02-14-privatepreview"
        },
        "resources": [
            {
                "apiVersion": "2020-10-05-privatepreview",
                "location": "[parameters('location')]",
                "name": "[parameters('serverGroupName')]",
                "identity":
                {
                    "type": "UserAssigned",
                    "userAssignedIdentities":
                    {
                        "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/yogkuleuapcmkmarlintest/providers/Microsoft.ManagedIdentity/userAssignedIdentities/marlincmktesteus2euapuai1": {}
                    }
                },
                "properties": {
                    "createMode": "PointInTimeRestore",
                    "sourceServerGroupName": "[parameters('sourceServerGroupName')]",
                    "pointInTimeUTC": "[parameters('restorePointInTime')]",
                    "sourceLocation": "[parameters('location')]",
                    "sourceSubscriptionId": "[parameters('subscriptionId')]",
                    "sourceResourceGroupName": "[parameters('resourceGroupName')]",
                    "enableMx": false,
                    "enableZfs": false,
                    "dataencryption":
                    {
                        "primaryKeyUri": "[parameters('encryptionKeyUrl')]",
                        "primaryUserAssignedIdentityId": "[parameters('userAssignedIdentityUrl')]",
                        "type": "AzureKeyVault"
                    },
                }
                "type": "Microsoft.DBforPostgreSQL/serverGroupsv2"
            }
        ]
    }
 ```
---

### Monitor the customer-managed key in Key Vault

To monitor the database state, and to enable alerting for the loss of transparent data encryption protector access, configure the following Azure features:

* [Azure Resource Health](/azure/service-health/resource-health-overview): An inaccessible database that has lost access to the Customer Key shows as "Inaccessible" after the first connection to the database has been denied.

* [Activity log](/azure/service-health/alerts-activity-log-service-notifications-portal): When access to the Customer Key in the customer-managed Key Vault fails, entries are added to the activity log. You can reinstate access as soon as possible, if you create alerts for these events.

* [Action groups](/azure/azure-monitor/alerts/action-groups): Define these groups to send you notifications and alerts based on your preference.

## Next steps

- Learn about [data encryption with customer-managed keys](./concepts-customer-managed-keys.md)
- Check out [CMK limits and limitations](./reference-limits.md#storage) in Azure Cosmos DB for PostgreSQL
