---
title: Configure the Azure Storage Extension in Azure HorizonDB
description: Learn how to configure the Azure Storage extension in an Azure HorizonDB to import and export data.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-horizondb
ms.subservice: extensions-modules
ms.topic: reference
ms.custom:
  - ignite-2024
  - ignite-2025
  - sfi-image-nochange
---

# Configure the Azure Storage extension for Azure HorizonDB (Preview)

You must follow these steps to be able to use the Azure Storage extension:

1. [Identify Azure Storage accounts](#identify-the-azure-storage-accounts)
1. [Choose type of authorization](#choose-type-of-authorization)
1. [Load the extension's library](#load-the-extensions-library)
1. [Allowlist the extension](#allowlist-the-extension)
1. [Create the extension](#create-the-extension)
1. [Use the extension to import and export data](#use-the-extension-to-import-and-export-data)

## Identify the Azure Storage accounts

Identify the Azure Storage accounts with which you want users of the extension to interact, to import data from or export data to.

## Choose type of authorization

For the time being the only type of authorization `azure_storage` extension can use for the requests made against the blob service of each of those Azure Storage accounts is based on Shared Key.

To meet the prerequisites, follow the instructions in the corresponding section:
- [Authorization with Shared Key](#use-authorization-with-shared-key).

<a id="to-use-authorization-with-microsoft-entra-id"></a>

### Use authorization with Shared Key

1. [Confirm that storage account allows access to its key](#confirm-that-storage-account-allows-access-to-its-key)
1. [Fetch one of the two access keys of the storage account](#fetch-one-of-the-two-access-keys-of-the-storage-account)

#### Confirm that storage account allows access to its key

Your Azure Storage account must have **Allow storage account key access** enabled (that is, it can't have its [AllowSharedKeyAccess](/azure/storage/common/shared-key-authorization-prevent) property set to **false**).

##### [Azure portal](#tab/portal-04)

:::image type="content" source="media/how-to-configure-azure-storage-extension/allow-shared-key-access-enabled-portal.png" alt-text="Screenshot of confirming that Allow storage account key access is enabled." lightbox="media/how-to-configure-azure-storage-extension/allow-shared-key-access-enabled-portal.png":::

##### [CLI](#tab/cli-04)

```azurecli-interactive
az storage account update \
  --resource-group <storage_account_resource_group> \
  --name <account_name> \
  --allow-shared-key-access true
```

##### [REST API](#tab/rest-04)

Using [Storage Accounts - Update](/rest/api/storagerp/storage-accounts/update) REST API.

---

#### Fetch one of the two access keys of the storage account

To pass it to the [azure_storage.account_add](reference-azure-storage-extension.md#azure_storageaccount_add) function, [fetch either of the two access keys](/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys) of the Azure Storage account.

##### [Azure portal](#tab/portal-05)

:::image type="content" source="media/how-to-configure-azure-storage-extension/copy-access-key-portal.png" alt-text="Screenshot of copying storage account access key." lightbox="media/how-to-configure-azure-storage-extension/copy-access-key-portal.png":::

##### [CLI](#tab/cli-05)

```azurecli-interactive
az storage account keys list \
  --resource-group <storage_account_resource_group> \
  --account-name <account_name> \
  --query [0].value \
  --output tsv
```

##### [REST API](#tab/rest-05)

Using [Storage Accounts - List Keys](/rest/api/storagerp/storage-accounts/list-keys) REST API.

---

## Load the extension's library

Configure your cluster so that it loads the `azure_storage` binary module when it's started.

For that, you have to [create a parameter group](../parameters/how-to-parameter-groups-create.md) that modifies the value of `shared_preload_libraries` and includes `azure_storage` in its value.

Then you have to [connect your cluster to that parameter group](../parameters/how-to-parameter-groups-connect.md) for the value to take effect.

Because `shared_preload_libraries` is a static parameter, it requires a restart of your cluster which occurs as soon as you connect the parameter group to the cluster.

<!--
### [Azure portal](#tab/portal-01)

:::image type="content" source="media/how-to-configure-azure-storage-extension/shared-preload-libraries-portal.png" alt-text="Screenshot of selecting azure_storage in shared_preload_libraries in Parameters." lightbox="media/how-to-configure-azure-storage-extension/shared-preload-libraries-portal.png":::
Because the `shared_preload_libraries` is static, the server must be restarted for a change to take effect:
:::image type="content" source="media/how-to-configure-azure-storage-extension/save-and-restart-shared-preload-libraries-portal.png" alt-text="Screenshot of dialog that pops up when changing shared_preload_libraries, to save and restart." lightbox="media/how-to-configure-azure-storage-extension/save-and-restart-shared-preload-libraries-portal.png":::

### [CLI](#tab/cli-01)

```azurecli-interactive
az postgres flexible-Parameter set \
  --resource-group <resource_group>
  --server-name <server>
  --name shared_preload_libraries \
  --source user-override \
  --value azure_storage,$(az postgres flexible-Parameter show \
                            --resource-group <resource_group> \
                            --server-name <server> \
                            --name shared_preload_libraries \
                            --query value \
                            --output tsv)
```
Because the `shared_preload_libraries` is static, the server must be restarted for a change to take effect:

```azurecli-interactive
az postgres flexible-server restart \
  --resource-group <resource_group> \
  --name <server>
```

### [REST API](#tab/rest-01)

Using [Configurations - Put](/rest/api/postgresql/configurations/put) REST API.

Because the `shared_preload_libraries` is static, the server must be restarted for a change to take effect. For restarting the server, you can use the [Server - Restart](/rest/api/postgresql/servers/restart) REST API.

---
-->

## Allowlist the extension

You must allowlist the extension so that users can run CREATE EXTENSION, DROP EXTENSION, ALTER EXTENSION, COMMENT ON EXTENSION.

For that, you have to [create a parameter group](../parameters/how-to-parameter-groups-create.md) that also modifies the value of `azure.extensions` and includes `azure_storage` in its value.

Then you have to [connect your cluster to that parameter group](../parameters/how-to-parameter-groups-connect.md) for the value to take effect.

Because `azure.extensions` is a dynamic parameter, it doesn't require a restart of your cluster, but the change is immediately effective as soon as you connect the parameter group to the cluster.

<!--
### [Azure portal](#tab/portal-02)

:::image type="content" source="media/how-to-configure-azure-storage-extension/azure-extensions-portal.png" alt-text="Screenshot of selecting azure_storage in azure.extensions in Parameters." lightbox="media/how-to-configure-azure-storage-extension/azure-extensions-portal.png":::

### [CLI](#tab/cli-02)

```azurecli-interactive
az postgres flexible-Parameter set \
  --resource-group <resource_group> \
  --server-name <server> \
  --name azure.extensions \
  --source user-override \
  --value azure_storage,$(az postgres flexible-Parameter show \
                            --resource-group <resource_group>
                            --server-name <server> \
                            --name azure.extensions \
                            --query value \
                            --output tsv)
```

### [REST API](#tab/rest-02)

Using [Configurations - Put](/rest/api/postgresql/configurations/put) REST API.

---
-->
## Create the extension

Use the client of your preference, like [PostgreSQL extension for Visual Studio Code](../development/vs-code-extension/vs-code-overview.md), [psql](https://www.postgresql.org/docs/current/app-psql.html), or [PgAdmin](https://www.pgadmin.org/), to connect to the database in which you want to use the Azure Storage extension.

To create all SQL objects (tables, types, functions, views, etc.) with which you can use the `azure_storage` extension to interact with instances of Azure Storage accounts, execute the following statement:

```sql
CREATE EXTENSION azure_storage;
```

## Use the extension to import and export data

Now you're ready to add the storage accounts with which you want to interact (using the `azure_storage.account_add` function). Then you can import data stored in files in Azure Storage accounts, by using the `azure_storage.blob_get` function or the `COPY FROM` statement, or you can export data from PostgreSQL into files in an Azure Storage account, by using the `azure_storage.blob_put` function or the `COPY TO` statement.

Check out the list of quickstart examples:

- [Create an Azure Storage account and populate it with data](quickstart-azure-storage-extension.md#create-an-azure-storage-account-and-populate-it-with-data)
- [Create a table in which data is loaded](quickstart-azure-storage-extension.md#create-a-table-in-which-data-is-loaded)
- [Add access key of storage account](quickstart-azure-storage-extension.md#add-access-key-of-storage-account)
- [Grant access to a user or role on the Azure Blob storage reference](quickstart-azure-storage-extension.md#grant-access-to-a-user-or-role-on-the-azure-blob-storage-reference)
- [List all blobs in a container](quickstart-azure-storage-extension.md#list-all-blobs-in-a-container)
- [List blobs with a specific name prefix](quickstart-azure-storage-extension.md#list-blobs-with-a-specific-name-prefix)
- [Import data using a COPY FROM statement](quickstart-azure-storage-extension.md#import-data-using-a-copy-from-statement)
- [Export data using a COPY TO statement](quickstart-azure-storage-extension.md#export-data-using-a-copy-to-statement)
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

> [!IMPORTANT]  
> For authentication types for which you must provide an Azure Storage account access key, notice that your Azure Storage access keys are similar to a root password for your storage account. Always be careful to protect them. Use Azure Key Vault to manage and rotate your keys securely. `azure_storage` extension stores those keys in a table `azure_storage.accounts`, which is readable by members of the `pg_read_all_data` role.

## Related content

- [Quickstart examples for Azure Storage extension in Azure HorizonDB (Preview)](quickstart-azure-storage-extension.md)
- [Reference of functions provided by the Azure Storage extension in Azure HorizonDB (Preview)](reference-azure-storage-extension.md)
- [Azure storage extension in Azure HorizonDB (Preview)](concepts-storage-extension.md)
- [Extensions and modules in Azure HorizonDB (Preview)](concepts-extensions.md)
