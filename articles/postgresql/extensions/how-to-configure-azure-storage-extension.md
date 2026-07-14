---
title: Configure the Azure Storage Extension in Azure Database for PostgreSQL Flexible Server
description: Learn how to configure the Azure Storage extension in an Azure Database for PostgreSQL flexible server to import and export data.
#customer intent: As a user, I want to configure the Azure Storage extension in my Azure Database for PostgreSQL flexible server, so that I can import and export data between PostgreSQL and Azure Storage.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 07/10/2026
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: reference
ms.update-cycle: 365-days
---

# Configure the Azure Storage extension in Azure Database for PostgreSQL flexible server

To use the Azure Storage extension, complete the following steps:

1. [Identify Azure Storage accounts](#identify-the-azure-storage-accounts)
1. [Choose type of authorization](#choose-type-of-authorization)
1. [Load the extension's library](#load-the-extensions-library)
1. [Allow list the extension](#allow-list-the-extension)
1. [Create the extension](#create-the-extension)
1. [Initialize encryption key to encrypt sensitive credentials](#initialize-encryption-key-to-encrypt-sensitive-credentials)
1. [Use the extension to import and export data](#use-the-extension-to-import-and-export-data)

## Identify the Azure Storage accounts

Identify the Azure Storage accounts that you want users of the extension to interact with, to import data from or export data to.

## Choose type of authorization

Decide which type of authorization you want to use for the requests made against the blob service of each of those Azure Storage accounts. The `azure_storage` extension supports authorization by using Shared Key, and authorization by using Microsoft Entra ID.

Of these two types of authorization, Microsoft Entra ID provides superior security and ease of use over Shared Key, and is the one Microsoft recommends.

To meet the prerequisites needed in each case, follow the instructions in the corresponding sections:
- [Authorization with Microsoft Entra ID](#to-use-authorization-with-microsoft-entra-id), or
- [Authorization with Shared Key](#to-use-authorization-with-shared-key).

### To use authorization with Microsoft Entra ID

1. Enable [Firewall rules in Azure Database for PostgreSQL](../security/security-firewall-rules.md) on your Azure Database for PostgreSQL flexible server.
1. [Restart PostgreSQL engine](../configure-maintain/how-to-restart-server.md), after enabling a system assigned managed identity on it.
1. [Assign role-based access control (RBAC) permissions for access to blob data](/azure/storage/blobs/assign-azure-role-data-access) on the Azure Storage account to the system assigned managed identity of your Azure Database for PostgreSQL flexible server.

#### Enable System Assigned Managed Identity

# [Portal](#tab/portal-storage-extension-enable-sami)

:::image type="content" source="media/how-to-configure-azure-storage-extension/enable-system-assigned-managed-identity-portal.png" alt-text="Screenshot of enabling System Assigned Managed Identity." lightbox="media/how-to-configure-azure-storage-extension/enable-system-assigned-managed-identity-portal.png":::

# [CLI](#tab/cli-storage-extension-enable-sami)

[!INCLUDE [no-native-cli-support](../includes/no-native-cli-support.md)]

```azurecli-interactive
az rest \
  --method patch \
  --url https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<flexible_server_resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<flexible_server_name>?api-version=2025-08-01 \
  --body '{"identity":{"type":"SystemAssigned"}}'
```

# [REST API](#tab/rest-storage-extension-enable-sami)

Using the [Servers - Update](/rest/api/postgresql/servers/update) REST API.

---

### To use authorization with Shared Key

1. [Confirm that storage account allows access to its key](#confirm-that-storage-account-allows-access-to-its-key)
1. [Fetch one of the two access keys of the storage account](#fetch-one-of-the-two-access-keys-of-the-storage-account)

#### Confirm that storage account allows access to its key

Your Azure Storage account must have **Allow storage account key access** enabled (that is, it can't have its [AllowSharedKeyAccess](/azure/storage/common/shared-key-authorization-prevent) property set to **false**).

##### [Portal](#tab/portal-storage-extension-confirm-storage-account)

:::image type="content" source="media/how-to-configure-azure-storage-extension/allow-shared-key-access-enabled-portal.png" alt-text="Screenshot of confirming that Allow storage account key access is enabled." lightbox="media/how-to-configure-azure-storage-extension/allow-shared-key-access-enabled-portal.png":::

##### [CLI](#tab/cli-storage-extension-confirm-storage-account)

```azurecli-interactive
az storage account update \
  --resource-group <storage_account_resource_group> \
  --name <account_name> \
  --allow-shared-key-access true
```

##### [REST API](#tab/rest-storage-extension-confirm-storage-account)

Using [Storage Accounts - Update](/rest/api/storagerp/storage-accounts/update) REST API.

---

#### Fetch one of the two access keys of the storage account

To pass it to the [azure_storage.account_add](reference-azure-storage-extension.md#azure_storageaccount_add) function, [fetch either of the two access keys](/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys) of the Azure Storage account.

##### [Portal](#tab/portal-storage-extension-fetch-access-key)

:::image type="content" source="media/how-to-configure-azure-storage-extension/copy-access-key-portal.png" alt-text="Screenshot of copying storage account access key." lightbox="media/how-to-configure-azure-storage-extension/copy-access-key-portal.png":::

##### [CLI](#tab/cli-storage-extension-fetch-access-key)

```azurecli-interactive
az storage account keys list \
  --resource-group <storage_account_resource_group> \
  --account-name <account_name> \
  --query [0].value \
  --output tsv
```

##### [REST API](#tab/rest-storage-extension-fetch-access-key)

Using [Storage Accounts - List Keys](/rest/api/storagerp/storage-accounts/list-keys) REST API.

---

## Load the extension's library

Configure your server to load the `azure_storage` binary module when it starts.

### [Portal](#tab/portal-storage-extension-load-library)

:::image type="content" source="media/how-to-configure-azure-storage-extension/shared-preload-libraries-portal.png" alt-text="Screenshot of selecting azure_storage in shared_preload_libraries in parameters." lightbox="media/how-to-configure-azure-storage-extension/shared-preload-libraries-portal.png":::
Because the `shared_preload_libraries` parameter is static, you must restart the server for a change to take effect:
:::image type="content" source="media/how-to-configure-azure-storage-extension/save-and-restart-shared-preload-libraries-portal.png" alt-text="Screenshot of dialog that pops up when changing shared_preload_libraries, to save and restart." lightbox="media/how-to-configure-azure-storage-extension/save-and-restart-shared-preload-libraries-portal.png":::

### [CLI](#tab/cli-storage-extension-load-library)

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group>
  --server-name <server>
  --name shared_preload_libraries \
  --source user-override \
  --value azure_storage,$(az postgres flexible-server parameter show \
                            --resource-group <resource_group> \
                            --server-name <server> \
                            --name shared_preload_libraries \
                            --query value \
                            --output tsv)
```
Because the `shared_preload_libraries` parameter is static, you must restart the server for a change to take effect:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server>
```

### [REST API](#tab/rest-storage-extension-load-library)

Use the [Configurations - Put](/rest/api/postgresql/configurations/put) REST API.

Because the `shared_preload_libraries` parameter is static, you must restart the server for a change to take effect. To restart the server, use the [Server - Restart](/rest/api/postgresql/servers/restart) REST API.

---

## Allow list the extension

Add the extension to the allow list so that users can run `CREATE EXTENSION`, `DROP EXTENSION`, `ALTER EXTENSION`, and `COMMENT ON EXTENSION`.

### [Azure portal](#tab/portal-storage-extension-allow-list-extension)

:::image type="content" source="media/how-to-configure-azure-storage-extension/azure-extensions-portal.png" alt-text="Screenshot of selecting azure_storage in azure.extensions in parameters." lightbox="media/how-to-configure-azure-storage-extension/azure-extensions-portal.png":::

### [CLI](#tab/cli-extension-allow-list-extension)

```azurecli-interactive
az postgres flexible-server parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name azure.extensions \
  --source user-override \
  --value azure_storage,$(az postgres flexible-server parameter show \
                            --resource-group <resource_group>
                            --server-name <server> \
                            --name azure.extensions \
                            --query value \
                            --output tsv)
```

### [REST API](#tab/rest-extension-allow-list-extension)

Use the [Configurations - Put](/rest/api/postgresql/configurations/put) REST API.

---

## Create the extension

Use the client of your preference, such as [PostgreSQL for Visual Studio Code (Preview)](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql), [psql](https://www.postgresql.org/docs/current/app-psql.html), or [PgAdmin](https://www.pgadmin.org/), to connect to the database where you want to use the Azure Storage extension.

To create all SQL objects (tables, types, functions, views, and so on) with which you can use the `azure_storage` extension to interact with instances of Azure Storage accounts, execute the following statement:

```sql
CREATE EXTENSION azure_storage;
```

## Initialize encryption key to encrypt sensitive credentials

Use the client of your preference, such as [PostgreSQL for Visual Studio Code (Preview)](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql), [psql](https://www.postgresql.org/docs/current/app-psql.html), or [PgAdmin](https://www.pgadmin.org/), to connect to the database where you want to use the Azure Storage extension.

To initialize the encryption key for all sensitive credentials used to authenticate with the different Azure storage accounts, run the following statement:

> [!NOTE]  
> Make sure you change `<strong passphrase>` to your own strong secret.

```sql
ALTER DATABASE <database_with_created_extension> SET azure_storage.credential_encryption_key = '<strong_passphrase>';
```

If you create the extension in multiple databases, you must initialize the value of `azure_storage.credential_encryption_key` at the database level, so all sensitive credentials kept in that database are encrypted by using the same key.

To set the value of `azure_storage.credential_encryption_key`, you must be member of the `azure_storage_admin` role. Then connect to the server, in the context of the database where you created the extension. In that context, execute `ALTER DATABASE <database_with_created_extension> SET azure_storage.credential_encryption_key = '<strong passphrase>';` to initialize the encryption key that's used to encrypt all Azure storage account credentials that the extension keeps in the catalog of that database. After running this command, you must disconnect and reconnect to the database again, so that the override value takes effect. You should also invoke the `azure_storage.account_encrypt_existing_credentials()` function so that the credentials of existing accounts that were never encrypted before by using any other key are encrypted by using this key. To do so, execute `SELECT azure_storage.account_encrypt_existing_credentials();`.

Although possible, don't try to use other statements like `ALTER ROLE` or `ALTER ROLE IN DATABASE` to set the value of `azure_storage.credential_encryption_key`.

If you change the value of `azure_storage.credential_encryption_key`, you must manually add again, by using `azure_storage.account_add`, all storage accounts for which you provided a sensitive credential (an access key or a SAS token) that was encrypted by using the previous value. Currently, the extension doesn't support automatic rollover of encryption key.

## Use the extension to import and export data

Now you're ready to add the storage accounts with which you want to interact (using the `azure_storage.account_add` function). Then you can import data stored in files in Azure Storage accounts, by using the `azure_storage.blob_get` function or the `COPY FROM` statement, or you can export data from PostgreSQL into files in an Azure Storage account, by using the `azure_storage.blob_put` function or the `COPY TO` statement.

Check out the list of quickstart examples:

- [Create an Azure Storage account and populate it with data](quickstart-azure-storage-extension.md#create-an-azure-storage-account-and-populate-it-with-data)
- [Create a table in which data is loaded](quickstart-azure-storage-extension.md#create-a-table-in-which-to-load-data)
- [Add access key of storage account](quickstart-azure-storage-extension.md#add-access-key-of-storage-account)
- [Grant access to a user or role on the Azure Blob storage reference](quickstart-azure-storage-extension.md#grant-access-to-a-user-or-role-on-the-azure-blob-storage-reference)
- [List all blobs in a container](quickstart-azure-storage-extension.md#list-all-blobs-in-a-container)
- [List blobs with a specific name prefix](quickstart-azure-storage-extension.md#list-blobs-with-a-specific-name-prefix)
- [Import data using a COPY FROM statement](quickstart-azure-storage-extension.md#import-data-by-using-a-copy-from-statement)
- [Export data using a COPY TO statement](quickstart-azure-storage-extension.md#export-data-by-using-a-copy-to-statement)
- [Read content from a blob](quickstart-azure-storage-extension.md#read-content-from-a-blob)
- [Read, filter, and modify content read from a blob](quickstart-azure-storage-extension.md#read-filter-and-modify-content-read-from-a-blob)
- [Read content from file with custom options (headers, column delimiters, escape characters)](quickstart-azure-storage-extension.md#read-content-from-file-with-custom-options-headers-column-delimiters-escape-characters)
- [Use the decoder option](quickstart-azure-storage-extension.md#use-the-decoder-option)
- [Compute aggregations over the content of a blob](quickstart-azure-storage-extension.md#compute-aggregations-over-the-content-of-a-blob)
- [Write content to a blob](quickstart-azure-storage-extension.md#write-content-to-a-blob)
- [List all the references to Azure storage accounts](quickstart-azure-storage-extension.md#list-all-the-references-to-azure-storage-accounts)
- [Revoke access from a user or role on the Azure Blob storage reference](quickstart-azure-storage-extension.md#revoke-access-from-a-user-or-role-on-the-azure-blob-storage-reference)
- [Remove reference to storage account](quickstart-azure-storage-extension.md#remove-reference-to-storage-account)

In case you need to review all functions offered by the extension and all the details about each of them, review the full reference:

- [azure_storage.account_add](reference-azure-storage-extension.md#azure_storageaccount_add)
- [azure_storage.account_options_managed_identity](reference-azure-storage-extension.md#azure_storageaccount_options_managed_identity)
- [azure_storage.account_options_credentials](reference-azure-storage-extension.md#azure_storageaccount_options_credentials)
- [azure_storage.account_options](reference-azure-storage-extension.md#azure_storageaccount_options)
- [azure_storage.account_remove](reference-azure-storage-extension.md#azure_storageaccount_remove)
- [azure_storage.account_user_add](reference-azure-storage-extension.md#azure_storageaccount_user_add)
- [azure_storage.account_user_remove](reference-azure-storage-extension.md#azure_storageaccount_user_remove)
- [azure_storage.account_list](reference-azure-storage-extension.md#azure_storageaccount_list)
- [azure_storage.blob_list](reference-azure-storage-extension.md#azure_storageblob_list)
- [azure_storage.blob_get](reference-azure-storage-extension.md#azure_storageblob_get)
- [azure_storage.blob_put](reference-azure-storage-extension.md#azure_storageblob_put)
- [azure_storage.options_csv_get](reference-azure-storage-extension.md#azure_storageoptions_csv_get)
- [azure_storage.options_copy](reference-azure-storage-extension.md#azure_storageoptions_copy)
- [azure_storage.options_tsv](reference-azure-storage-extension.md#azure_storageoptions_tsv)
- [azure_storage.options_binary](reference-azure-storage-extension.md#azure_storageoptions_binary)

And, if you need to do some troubleshooting, review the [list of errors](../troubleshoot/troubleshoot-azure-storage-extension.md) that the extension can produce, and the context in which they can be raised.

> [!IMPORTANT]  
> For authentication types that require an Azure Storage account access key, remember that your Azure Storage access keys are similar to a root password for your storage account. Always protect them. Use Azure Key Vault to manage and rotate your keys securely. The `azure_storage` extension stores those keys in a table `azure_storage.accounts`, which members of the `pg_read_all_data` role can read.

## Related content

- [Quickstart examples for the Azure Storage extension in Azure Database for PostgreSQL](quickstart-azure-storage-extension.md)
- [Troubleshoot the Azure Storage extension in Azure Database for PostgreSQL](../troubleshoot/troubleshoot-azure-storage-extension.md)
- [Reference of functions provided by the Azure Storage extension in Azure Database for PostgreSQL](reference-azure-storage-extension.md)
- [Azure storage extension in Azure Database for PostgreSQL](concepts-storage-extension.md)
- [Extensions and modules](concepts-extensions.md)
