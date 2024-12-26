---
title: Configure customer-managed keys on existing accounts
titleSuffix: Azure Cosmos DB
description: Store customer-managed keys in Azure Key Vault to use for encryption in your existing Azure Cosmos DB account with access control.
author: dileepraotv-github
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 08/17/2023
ms.author: turao
ms.devlang: azurecli
---

# Configure customer-managed keys for your existing Azure Cosmos DB account with Azure Key Vault

[!INCLUDE[NoSQL, MongoDB, Gremlin, Table](includes/appliesto-nosql-mongodb-gremlin-table.md)]

Enabling a second layer of encryption for data at rest using [Customer Managed Keys](./how-to-setup-customer-managed-keys.md) while creating a new Azure Cosmos DB account has been Generally available for some time now. As a natural next step, we now have the capability to enable CMK on existing Azure Cosmos DB accounts.

This feature eliminates the need for data migration to a new account to enable CMK. It helps to improve customers’ security and compliance posture.

Enabling CMK kicks off a background, asynchronous process to encrypt all the existing data in the account, while new incoming data are encrypted before persisting. There's no need to wait for the asynchronous operation to succeed. The enablement process consumes unused/spare RUs so that it doesn't affect your read/write workloads. You can refer to this [link](./how-to-setup-customer-managed-keys.md?tabs=azure-powershell#how-do-customer-managed-keys-influence-capacity-planning) for capacity planning once your account is encrypted. 

## Get started by enabling CMK on your existing accounts

> [!IMPORTANT]
> Go through the prerequisites section thoroughly. These are important considerations.

### Prerequisites

All the prerequisite steps needed while configuring Customer Managed Keys for new accounts is applicable to enable CMK on your existing account. Refer to the steps [here](./how-to-setup-customer-managed-keys.md?tabs=azure-portal#prerequisites)

> [!NOTE]
> It is important to note that enabling encryption on your Azure Cosmos DB account will add a small overhead to your document's ID, limiting the maximum size of the document ID to 990 bytes instead of 1024 bytes. If your account has any documents with IDs larger than 990 bytes, the encryption process will fail until those documents are deleted.
 
To verify if your account is compliant, you can use the provided console application [hosted here](https://github.com/AzureCosmosDB/Cosmos-DB-Non-CMK-to-CMK-Migration-Scanner) to scan your account. Make sure that you are using the endpoint from your 'sqlEndpoint' account property, no matter the API selected. 

If you wish to disable server-side validation for this during migration, please contact support.

### Steps to enable CMK on your existing account

To enable CMK on an existing account, update the account with an ARM template setting a Key Vault key identifier in the keyVaultKeyUri property – just like you would when enabling CMK on a new account. This step can be done by issuing a PATCH call with the following payload:

```
    {
        "properties": {
        "keyVaultKeyUri": "<key-vault-key-uri>"
        }
    }
```

The output of this CLI command for enabling CMK waits for the completion of encryption of data.

```azurecli
    az cosmosdb update --name "testaccount" --resource-group "testrg" --key-uri "https://keyvaultname.vault.azure.net/keys/key1"
```

### Steps to enable CMK on your existing Azure Cosmos DB account with Continuous backup or Analytical store account

For enabling CMK on existing account that has continuous backup and point in time restore enabled, we need to follow some extra steps. Follow step 1 to step 5 and then follow instructions to enable CMK on existing account.



1. Configure managed identity to your cosmos account [Configure managed identities with Microsoft Entra ID for your Azure Cosmos DB account](./how-to-setup-managed-identity.md)

1. Update cosmos account to set default identity to point to managed identity added in previous step

    **For System managed identity :**
    ```
    az cosmosdb update--resource-group $resourceGroupName --name $accountName --default-identity "SystemAssignedIdentity"
    ```

    **For User managed identity  :**

    ```
    az cosmosdb update -n $sourceAccountName -g $resourceGroupName --default-identity "UserAssignedIdentity=/subscriptions/00000000-0000-0000-0000-00000000/resourcegroups/MyRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/MyID"
    ```

1. Configure Keyvault as given in documentation [here](./how-to-setup-customer-managed-keys.md?tabs=azure-cli#configure-your-azure-key-vault-instance) 

1. Add [access policy](./how-to-setup-customer-managed-keys.md?tabs=azure-cli#using-a-managed-identity-in-the-azure-key-vault-access-policy) in the keyvault for the default identity that is set in previous step 

1. Update cosmos account to set keyvault uri, this update triggers enabling CMK on account   
    ```
    az cosmosdb update --name $accountName --resource-group $resourceGroupName --key-uri $keyVaultKeyURI  
    ```
## Known limitations

- We don't support enabling CMK on existing Azure Cosmos DB for Apache Cassandra accounts.
- Enabling CMK is available only at a Cosmos DB account level and not at collections.
- We don't support enabling CMK on existing accounts that are enabled for Materialized Views and [all versions and deletes change feed mode](nosql/change-feed-modes.md#all-versions-and-deletes-change-feed-mode-preview).
- Ensure account must not have documents with large IDs greater than 990 bytes before enabling CMK. If not, you'll get an error due to max supported limit of 1024 bytes after encryption.
- During encryption of existing data, [control plane](./audit-control-plane-logs.md) actions such as "add region" is blocked. These actions are unblocked and can be used right after the encryption is complete.

## Monitor the progress of the resulting encryption

Enabling CMK on an existing account is an asynchronous operation that kicks off a background task that encrypts all existing data. As such, the REST API request to enable CMK provides in its response an "Azure-AsyncOperation" URL. Polling this URL with GET requests return the status of the overall operation, which eventually Succeed. This mechanism is fully described in [this](/azure/azure-resource-manager/management/async-operations) article.

The Cosmos DB account can continue to be used and data can continue to be written without waiting for the asynchronous operation to succeed. CLI command for enabling CMK waits for the completion of encryption of data.

In order to allow an existing Cosmos DB account to use to CMK, a scan needs to be done to ensure that the account doesn't have "Large IDs". A "Large ID" is a document id that exceeds 990 characters length. This scan is mandatory for the CMK migration and it is done by Microsoft automatically. During this process you may see an error.

ERROR: (InternalServerError) Unexpected error on document scan for CMK Migration. Please retry the operation. 

This happens when the scan process uses more RUs than the ones provisioned on the collection, throwing a 429 error. A solution for this problem will be to temporarily bump their RUs significantly. Alternatively, you could make use of the provided console application [hosted here](https://github.com/AzureCosmosDB/Cosmos-DB-Non-CMK-to-CMK-Migration-Scanner) in order to scan their collections.

> [!NOTE]
> If you wish to disable server-side validation for this during migration, please contact support. This is advisable only if you are sure that there are no Large IDs. If Large ID is encountered during encryption, the process will stop till the Large Id document has been addressed.

If you have further questions, reach out to Microsoft Support.

## FAQs

**What are the factors on which the encryption time depends?**

Enabling CMK is an asynchronous operation and depends on sufficient unused RUs being available. We suggest enabling CMK during off-peak hours and if applicable you can increase RUs before hand, to speed up encryption. It's also a direct function of data size.

**Do we need to brace ourselves for downtime?**

Enabling CMK kicks off a background, asynchronous process to encrypt all the data. There's no need to wait for the asynchronous operation to succeed. The Azure Cosmos DB account is available for reads and writes and there's no need for a downtime.

**Can you bump up the RU’s once CMK has been triggered?**

It's suggested to bump up the RUs before you trigger CMK. Once CMK is triggered, then some control plane operations are blocked till the encryption is complete. This block may prevent the user from increasing the RU’s once CMK is triggered.

In order to allow an existing Cosmos DB account to use to CMK, a Large ID scan is done mandatory by Microsoft automatically to address one of the known limitations listed earlier. This process also consumes additional RUs and its a good idea to bump up the RU's significantly to avoid error 429. 

**Is there a way to reverse the encryption or disable encryption after triggering CMK?**

Once the data encryption process using CMK is triggered, it can't be reverted. 

**Will enabling encryption using CMK on existing account have an impact on data size and read/writes?**

As you would expect, by enabling CMK there's a slight increase in data size and RUs to accommodate extra encryption/decryption processing.

**Should you back up the data before enabling CMK?**

Enabling CMK doesn't pose any threat of data loss.

**Are old backups taken as a part of periodic backup encrypted?**

No. Old periodic backups aren't encrypted. Newly generated backups after CMK enabled is encrypted.

**What is the behavior on existing accounts that are enabled for Continuous backup?**

When CMK is turned on, the encryption is turned on for continuous backups as well. Once CMK is turned on, all restored accounts going forward will be CMK enabled.

**What is the behavior if CMK is enabled on PITR enabled account and we restore account to the time CMK was disabled?**

In this case CMK is explicitly enabled on the restored target account for the following reasons: 
- Once CMK is enabled on the account, there's no option to disable CMK. 
- This behavior is in line with the current design of restore of CMK enabled account with periodic backup

**What happens when user revokes the key while CMK migration is in-progress?**

The state of the key is checked when CMK encryption is triggered. If the key in Azure Key vault is in good standing, the encryption is started and the process completes without further check. Even if the key is revoked, or Azure key vault is deleted or unavailable, the encryption process succeeds. 

**Can we enable CMK encryption on our existing production account?**

Yes. Go through the prerequisite section thoroughly. We recommend testing all scenarios first on nonproduction accounts and once you're comfortable you can consider production accounts.

## Next steps

* Learn more about [data encryption in Azure Cosmos DB](database-encryption-at-rest.md).
* You can choose to add a second layer of encryption with your own keys, to learn more, see the [customer-managed keys](how-to-setup-cmk.md) article.
* For more information about Microsoft certifications, see the [Azure Trust Center](https://azure.microsoft.com/support/trust-center/).
