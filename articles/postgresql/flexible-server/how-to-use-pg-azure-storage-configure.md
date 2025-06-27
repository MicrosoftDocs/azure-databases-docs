---
title: Configure the Azure Storage extension in Azure Database for PostgreSQL flexible server
description: Learn how to configure the Azure Storage extension in Azure Database for PostgreSQL flexible server to import and export data
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/26/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: reference
ms.custom:
- ignite-2024
- sfi-image-nochange
---

# Configure the Azure Storage extension in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You must follow these steps to be able to use the Azure Storage extension:

1. Identify Azure Storage accounts. 
2. Choose type of authorization.
3. Load the extension's library.
4. Allowlist the extension.
5. Connect to the database in which you want to use the extension, and create the extension.
6. Use the SQL functions created by the extension to leverage the capabilities supported by the extension.


## Identify the Azure Storage accounts

Identify the Azure Storage accounts with which you want users of the extension to interact with, to import data from or export data to.

## Choose type of authorization

Decide which type of authorization you want to use for the requests made against the blob service of each of those Azure Storage accounts. `azure_storage` extension supports [authorization with Shared Key](/rest/api/storageservices/authorize-with-shared-key), and [authorization with Microsoft Entra ID](/rest/api/storageservices/authorize-with-azure-active-directory). Of these two types of authorization, Microsoft Entra ID provides superior security and ease of use over Shared Key, and is the one Microsoft recommends. To meet the prerequisites needed in each case, follow the instructions in the corresponding sections:
    - [Authorization with Microsoft Entra ID](#to-use-authorization-with-microsoft-entra-id), or
    - [Authorization with Shared Key](#to-use-authorization-with-shared-key).

### To use authorization with Microsoft Entra ID

1. [Enable System Assigned Managed Identity](concepts-identity.md) on your instance of Azure Database for PostgreSQLflexible server.
2. [Restart the instance of Azure Database for PostgreSQLflexible server](how-to-restart-server.md), after enabling a system assigned managed identity on it.
3. [Assign role-based access control (RBAC) permissions for access to blob data](/azure/storage/blobs/assign-azure-role-data-access), on the Azure Storage account, to the System Assigned Managed Identity of your instance of Azure Database for PostgreSQLflexible server.

# [Azure portal](#tab/portal-03)

:::image type="content" source="media/how-to-use-pg-azure-storage/enable-system-assigned-managed-identity-portal.png" alt-text="Screenshot of enabling System Assigned Managed Identity." lightbox="media/how-to-use-pg-azure-storage/enable-system-assigned-managed-identity-portal.png":::

# [CLI](#tab/cli-03)

```azurecli-interactive
az rest \
  --method patch \
  --url https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/<flexible_server_resource_group>/providers/Microsoft.DBforPostgreSQL/flexibleServers/<flexible_server_name>?api-version=2024-08-01 \
  --body '{"identity":{"type":"SystemAssigned"}}'
```              

# [REST API](#tab/rest-03)

Using the [Servers - Update](/rest/api/postgresql/servers/update) REST API.

---

## Load the extension's library

 Configure your server so that it loads the `azure_storage` binary module when it's started.

### [Azure portal](#tab/portal-01)

:::image type="content" source="media/how-to-use-pg-azure-storage/shared-preload-libraries-portal.png" alt-text="Screenshot of selecting azure_storage in shared_preload_libraries in server parameters." lightbox="media/how-to-use-pg-azure-storage/shared-preload-libraries-portal.png":::
Because the `shared_preload_libraries` is static, the server must be restarted for a change to take effect:
:::image type="content" source="media/how-to-use-pg-azure-storage/save-and-restart-shared-preload-libraries-portal.png" alt-text="Screenshot of dialog that pops up when changing shared_preload_libraries, to save and restart." lightbox="media/how-to-use-pg-azure-storage/save-and-restart-shared-preload-libraries-portal.png":::

### [CLI](#tab/cli-01)

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

## Allowlist the extension

You must allowlist the extension so that you users can run CREATE EXTENSION, DROP EXTENSION, ALTER EXTENSION, COMMENT ON EXTENSION.

### [Azure portal](#tab/portal-02)

:::image type="content" source="media/how-to-use-pg-azure-storage/azure-extensions-portal.png" alt-text="Screenshot of selecting azure_storage in azure.extensions in server parameters." lightbox="media/how-to-use-pg-azure-storage/azure-extensions-portal.png":::

### [CLI](#tab/cli-02)

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

### [REST API](#tab/rest-02)

Using [Configurations - Put](/rest/api/postgresql/configurations/put) REST API.

---

5. Using the client of your preference (for example, psql, pgAdmin, etc.), connect to any database in your instance of Azure Database for PostgreSQLflexible server. To create all SQL objects (tables, types, functions, views, etc.) with which you can use the `azure_storage` extension to interact with instances of Azure Storage accounts, execute the following statement:
    ```sql
    CREATE EXTENSION azure_storage;
    ```
6. Using the `azure_storage.account_*` functions, add references to Azure Storage accounts that you want to let PostgreSQL users or roles access with the `azure_storage` extension. Those references include the name of the Azure Storage account being referenced, and the authentication type to use when interacting with the Azure Storage account. Depending on the authentication type selected you might need to also provide some other parameters, like the Azure Storage account access key or the SAS token.

> [!IMPORTANT]
> For authentication types for which you must provide an Azure Storage account access key, notice that your Azure Storage access keys are similar to a root password for your storage account. Always be careful to protect them. Use Azure Key Vault to manage and rotate your keys securely. `azure_storage` extension stores those keys in a table `azure_storage.accounts` that can be read by members of the `pg_read_all_data` role.

Users granted the `azure_storage_admin` role can interact with the `azure_storage.accounts` table using the following functions:
* [azure_storage.account_add](#azure_storageaccount_add)
* [azure_storage.account_list](#azure_storageaccount_list)
* [azure_storage.account_remove](#azure_storageaccount_remove)
* [azure_storage.account_user_add](#azure_storageaccount_user_add)
* [azure_storage.account_user_remove](#azure_storageaccount_user_remove)

The `azure_storage_admin` role is, by default, granted to the `azure_pg_admin` role.



### To use authorization with Shared Key

1. Your Azure Storage account must have **Allow storage account key access** enabled (that is, it can't have its [AllowSharedKeyAccess](/azure/storage/common/shared-key-authorization-prevent) property set to **false**).

# [Azure portal](#tab/portal-04)

:::image type="content" source="media/how-to-use-pg-azure-storage/AllowSharedKeyAccess-enabled-portal.png" alt-text="Screenshot of confirming that Allow storage account key access is enabled." lightbox="media/how-to-use-pg-azure-storage/AllowSharedKeyAccess-enabled-portal.png":::

# [CLI](#tab/cli-04)

```azurecli-interactive
az storage account update \
  --resource-group <storage_account_resource_group> \
  --name <account_name> \
  --allow-shared-key-access true
```

# [REST API](#tab/rest-04)

Using [Storage Accounts - Update](/rest/api/storagerp/storage-accounts/update) REST API.

---

2. To pass it to the [azure_storage.account_add](#azure_storageaccount_add) function, [fetch either of the two access keys](/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys) of the Azure Storage account.

# [Azure portal](#tab/portal-05)

:::image type="content" source="media/how-to-use-pg-azure-storage/copy-access-key-portal.png" alt-text="Screenshot of copying storage account access key." lightbox="media/how-to-use-pg-azure-storage/copy-access-key-portal.png":::

# [CLI](#tab/cli-05)

```azurecli-interactive
az storage account keys list \
  --resource-group <storage_account_resource_group> \
  --account-name <account_name> \
  --query [0].value \
  --output tsv
```

# [REST API](#tab/rest-05)

Using [Storage Accounts - List Keys](/rest/api/storagerp/storage-accounts/list-keys) REST API.

---

## Functions

### azure_storage.account_add

Function that allows adding a storage account, and its associated access key, to the list of storage accounts that the `azure_storage` extension can access.

If a previous invocation of this function already added the reference to this storage account, it doesn't add a new entry but instead updates the access key of the existing entry.

> [!NOTE]  
> This function doesn't validate if the referred account name exists or if it's accessible with the access key provided. However, it validates that the name of the storage account is valid, according to the naming validation rules imposed on Azure storage accounts.

```sql
azure_storage.account_add(account_name_p text, account_key_p text);
```

There's an overloaded version of this function, which accepts an `account_config` parameter that encapsulates the name of the referenced Azure Storage account, and all the required settings like authentication type, account type, or storage credentials.

```sql
azure_storage.account_add(account_config jsonb);
```

#### Permissions

Must be a member of `azure_storage_admin`.

#### Arguments

##### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### account_key_p

`text` the value of one of the access keys for the storage account. Your Azure blob storage access keys are similar to a root password for your storage account. Always be careful to protect your access keys. Use Azure Key Vault to manage and rotate your keys securely. The account key is stored in a table that is accessible only by the superuser. Users granted the `azure_storage_admin` role can interact with this table via functions. To see which storage accounts are added, use the function [azure_storage.account_list](#azure_storageaccount_list).

##### account_config

`jsonb` the name of the Azure Storage account and all the required settings like authentication type, account type, or storage credentials. We recommend the use of the utility functions [azure_storage.account_options_managed_identity](#azure_storageaccount_options_managed_identity), [azure_storage.account_options_credentials](#azure_storageaccount_options_credentials), or [azure_storage.account_options](#azure_storageaccount_options) to create any of the valid values that must be passed as this argument.

#### Return type

`VOID`

### azure_storage.account_options_managed_identity

Function that acts as a utility function, which can be called as a parameter within [azure_storage.account_add](#azure_storageaccount_add), and is useful to produce a valid value for the `account_config` argument, when using a system assigned managed identity to interact with the Azure Storage account.

```sql
azure_storage.account_options_managed_identity(name text, type azure_storage.storage_type);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### type

`azure_storage.storage_type` the value of one of the types of storage supported. Only supported value is `blob`.

#### Return type

`jsonb` 

### azure_storage.account_options_credentials

Function that acts as a utility function, which can be called as a parameter within [azure_storage.account_add](#azure_storageaccount_add), and is useful to produce a valid value for the `account_config` argument, when using an Azure Storage access key to interact with the Azure Storage account.

```sql
azure_storage.account_options_credentials(name text, credentials text, type azure_storage.storage_type);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### credentials

`text` the value of one of the access keys for the storage account. Your Azure blob storage access keys are similar to a root password for your storage account. Always be careful to protect your access keys. Use Azure Key Vault to manage and rotate your keys securely. The account key is stored in a table that is accessible only by the superuser. Users granted the `azure_storage_admin` role can interact with this table via functions. To see which storage accounts are added, use the function [azure_storage.account_list](#azure_storageaccount_list).

##### type

`azure_storage.storage_type` the value of one of the types of storage supported. Only supported value is `blob`.

#### Return type

`jsonb` 

### azure_storage.account_options

Function that acts as a utility function, which can be called as a parameter within [azure_storage.account_add](#azure_storageaccount_add), and is useful to produce a valid value for the `account_config` argument, when using an Azure Storage access key or a system assigned managed identity to interact with the Azure Storage account.

```sql
azure_storage.account_options(name text, auth_type azure_storage.auth_type, storage_type azure_storage.storage_type, credentials text DEFAULT NULL);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### auth_type

`azure_storage.auth_type` the value of one of the types of storage supported. Only supported values are `access-key`, and `managed-identity`.

##### storage_type

`azure_storage.storage_type` the value of one of the types of storage supported. Only supported value is `blob`.

##### credentials

`text` the value of one of the access keys for the storage account. Your Azure blob storage access keys are similar to a root password for your storage account. Always be careful to protect your access keys. Use Azure Key Vault to manage and rotate your keys securely. The account key is stored in a table that is accessible only by the superuser. Users granted the `azure_storage_admin` role can interact with this table via functions. To see which storage accounts are added, use the function [azure_storage.account_list](#azure_storageaccount_list).

#### Return type

`jsonb` 

### azure_storage.account_remove

Function that allows removing a storage account and its associated access key from the list of storage accounts that the `azure_storage` extension can access.

```sql
azure_storage.account_remove(account_name_p text);
```

#### Permissions

Must be a member of `azure_storage_admin`.

#### Arguments

##### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### Return type

`VOID` 

### azure_storage.account_user_add

Function that allows granting a PostgreSQL user or role access to a storage account through the functions provided by the `azure_storage` extension.

> [!NOTE]  
> The execution of this function only succeeds if the storage account, whose name is being passed as the first argument, was already created using [azure_storage.account_add](#azure_storageaccount_add), and if the user or role, whose name is passed as the second argument, already exists.

```sql
azure_storage.account_add(account_name_p text, user_p regrole);
```

#### Permissions

Must be a member of `azure_storage_admin`.

#### Arguments

##### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### user_p

`regrole` the name of a PostgreSQL user or role available on the server.

#### Return type

`VOID` 

### azure_storage.account_user_remove

Function that allows revoking a PostgreSQL user or role access to a storage account through the functions provided by the `azure_storage` extension.

> [!NOTE]
> The execution of this function only succeeds if the storage account whose name is being passed as the first argument has already been created using [azure_storage.account_add](#azure_storageaccount_add), and if the user or role whose name is passed as the second argument still exists.
> When a user or role is dropped from the server, by executing `DROP USER | ROLE`, the permissions that were granted on any reference to Azure Storage accounts are also automatically eliminated.

```sql
azure_storage.account_user_remove(account_name_p text, user_p regrole);
```

#### Permissions

Must be a member of `azure_storage_admin`.

#### Arguments

##### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### user_p

`regrole` the name of a PostgreSQL user or role available on the server.

#### Return type

`VOID` 

### azure_storage.account_list

Function that lists the names of the storage accounts that were configured via the [azure_storage.account_add](#azure_storageaccount_add) function, together with the PostgreSQL users or roles that are granted permissions to interact with that storage account through the functions provided by the `azure_storage` extension.

```sql
azure_storage.account_list();
```

#### Permissions

Must be a member of `azure_storage_admin`.

#### Arguments

This function doesn't take any arguments.

#### Return type

`TABLE(account_name text, auth_type azure_storage.auth_type, azure_storage_type azure_storage.storage_type, allowed_users regrole[])` a four-column table with the list of Azure Storage accounts added, the type of authentication used to interact with each account, the type of storage, and the list of PostgreSQL users or roles that are granted access to it.

### azure_storage.blob_list

Function that lists the names and other properties (size, lastModified, eTag, contentType, contentEncoding, and contentHash) of blobs stored in the given container of the referred storage account.

```sql
azure_storage.blob_list(account_name text, container_name text, prefix text DEFAULT ''::text);
```

#### Permissions

User or role invoking this function must be added to the allowed list for the `account_name` referred, by executing [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of `azure_storage_admin` are automatically allowed to reference all Azure Storage accounts whose references were added using [azure_storage.account_add](#azure_storageaccount_add).

#### Arguments

##### account_name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### container_name

`text` the name of a container. A container organizes a set of blobs, similar to a directory in a file system. A storage account can include an unlimited number of containers, and a container can store an unlimited number of blobs.
A container name must be a valid Domain Name System (DNS) name, as it forms part of the unique URI used to address the container or its blobs.
When naming a container, make sure to follow [these rules](/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names).

The URI for a container is similar to:
`https://myaccount.blob.core.windows.net/mycontainer`

##### prefix

`text` when specified, the function returns the blobs whose names begin with the value provided in this parameter. Defaults to an empty string.

#### Return type

`TABLE(path text, bytes bigint, last_modified timestamp with time zone, etag text, content_type text, content_encoding text, content_hash text)` a table with one record per blob returned, including the full name of the blob, and some other properties.

##### path

`text` the full name of the blob.

##### bytes

`bigint` the size of blob in bytes.

##### last_modified

`timestamp with time zone`the date and time the blob was last modified. Any operation that modifies the blob, including an update of the blob's metadata or properties, changes the last-modified time of the blob.

##### etag

`text` the ETag property is used for optimistic concurrency during updates. It isn't a timestamp as there's another property called Timestamp that stores the last time a record was updated. For example, if you load an entity and want to update it, the ETag must match what is currently stored. Setting the appropriate ETag is important because if you have multiple users editing the same item, you don't want them overwriting each other's changes.

##### content_type

`text` the content type specified for the blob. The default content type is `application/octet-stream`.

##### content_encoding

`text` the Content-Encoding property of a blob that Azure Storage allows you to define. For compressed content, you could set the property to be Gzip. When the browser accesses the content, it automatically decompresses the content.

##### content_hash

`text` the hash used to verify the integrity of the blob during transport. When this header is specified, the storage service checks the provided hash with one computed from content. If the two hashes don't match, the operation fails with error code 400 (Bad Request).


### azure_storage.blob_get

Function that allows importing data. It downloads a file from a blob container in an Azure Storage account. Then it translates the contents into rows, which can be consumed and processed with SQL language constructs. This function adds support to filter and manipulate the data fetched from the blob container before importing it.

> [!NOTE]  
> Before trying to access the container for the referred storage account, this function checks if the names of the storage account and container passed as arguments are valid according to the naming validation rules imposed on Azure storage accounts. If either of them is invalid, an error is raised.

```sql
azure_storage.blob_get(account_name text, container_name text, path text, decoder text DEFAULT 'auto'::text, compression text DEFAULT 'auto'::text, options jsonb DEFAULT NULL::jsonb);
```

There's an overloaded version of this function, which accepts a `rec` parameter that allows you to conveniently define the output format record.

```sql
azure_storage.blob_get(account_name text, container_name text, path text, rec anyelement, decoder text DEFAULT 'auto'::text, compression text DEFAULT 'auto'::text, options jsonb DEFAULT NULL::jsonb);
```

#### Permissions

User or role invoking this function must be added to the allowed list for the `account_name` referred, by executing [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of `azure_storage_admin` are automatically allowed to reference all Azure Storage accounts whose references were added using [azure_storage.account_add](#azure_storageaccount_add).

#### Arguments

##### account_name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### container_name

`text` the name of a container. A container organizes a set of blobs, similar to a directory in a file system. A storage account can include an unlimited number of containers, and a container can store an unlimited number of blobs.
A container name must be a valid Domain Name System (DNS) name, as it forms part of the unique URI used to address the container or its blobs.
When naming a container, make sure to follow [these rules](/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names).

The URI for a container is similar to:
`https://myaccount.blob.core.windows.net/mycontainer`

##### path

`text` the full name of the blob.

##### rec

`anyelement` the definition of the record output structure.

##### decoder

`text` the specification of the blob format. Can be set to any of the following values:

| **Format** | **Default** | **Description** |
| --- | --- | --- |
| `auto` | `true`      | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.csv` or `.csv.gz`, it assumes `csv`. If ends with `.tsv` or `.tsv.gz`, it assumes `tsv`. If ends with `.json`, `.json.gz`, `.xml`, `.xml.gz`, `.txt`, or `.txt.gz`, it assumes `text`. |
| `csv` | | Comma-separated values format used by PostgreSQL COPY. |
| `tsv` | | Tab-separated values, the default PostgreSQL COPY format. |
| `binary` | | Binary PostgreSQL COPY format. |
| `text` \| `xml` \| `json` | | A file containing a single text value. |

##### compression

`text` the specification of compression type. Can be set to any of the following values:

| **Format** | **Default** | **Description**                                                                                                                                                                      |
| --- | --- | --- |
| `auto` | `true` | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.gz`, it assumes `gzip`. Otherwise, it assumes `none`. |
| `gzip` | | Forces using gzip decoder to decompress the blob. |
| `none` | | Forces to treat the blob as one which doesn't require decompression. |

The extension doesn't support any other compression types.

##### options

`jsonb` the settings that define handling of custom headers, custom separators, escape characters, etc. `options` affects the behavior of this function in a way similar to how the options you can pass to the [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command in PostgreSQL affect its behavior.

#### Return type

`SETOF record` 
`SETOF  anyelement`

### azure_storage.blob_put

Function that allows exporting data, by uploading files to a blob container in an Azure Storage account. The content of the files is produced from rows in PostgreSQL.

> [!NOTE]  
> Before trying to access the container for the referred storage account, this function checks if the names of the storage account and container passed as arguments are valid according to the naming validation rules imposed on Azure storage accounts. If either of them is invalid, an error is raised.

```sql
azure_storage.blob_put(account_name text, container_name text, path text, tuple record)
RETURNS VOID;
```

There's an overloaded version of function, containing `encoder` parameter that allows you to specify the encoder to use when it can't be inferred from the extension of the `path` parameter, or when you want to override the one inferred.

```sql
azure_storage.blob_put(account_name text, container_name text, path text, tuple record, encoder text)
RETURNS VOID;
```

There's an overloaded version of function that also contains a `compression` parameter that allows you to specify the compression to use when it can't be inferred from the extension of the `path` parameter, or when you want to override the one inferred.

```sql
azure_storage.blob_put(account_name text, container_name text, path text, tuple record, encoder text, compression text)
RETURNS VOID;
```

There's an overloaded version of function that also contains an `options` parameter for handling custom headers, custom separators, escape characters etc. `options` works in similar fashion to the options that can be passed to the `COPY` command in PostgreSQL.

```sql
azure_storage.blob_put(account_name text, container_name text, path text, tuple record, encoder text, compression text, options jsonb)
RETURNS VOID;
```

#### Permissions

User or role invoking this function must be added to the allowed list for the `account_name` referred, by executing [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of `azure_storage_admin` are automatically allowed to reference all Azure Storage accounts whose references were added using [azure_storage.account_add](#azure_storageaccount_add).

#### Arguments

##### account_name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

##### container_name

`text` the name of a container. A container organizes a set of blobs, similar to a directory in a file system. A storage account can include an unlimited number of containers, and a container can store an unlimited number of blobs.
A container name must be a valid Domain Name System (DNS) name, as it forms part of the unique URI used to address the container or its blobs.
When naming a container, make sure to follow [these rules](/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names).

The URI for a container is similar to:
`https://myaccount.blob.core.windows.net/mycontainer`

##### path

`text` the full name of the blob.

##### tuple

`record` the definition of the record output structure.

##### encoder

`text` the specification of the blob format. Can be set to any of the following values:

| **Format** | **Default** | **Description** |
| --- | --- | --- |
| `auto` | `true`      | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.csv` or `.csv.gz`, it assumes  `csv`. If ends with `.tsv` or `.tsv.gz`, it assumes `tsv`. If ends with `.json`, `.json.gz`, `.xml`, `.xml.gz`, `.txt`, or `.txt.gz`, it assumes `text`. |
| `csv` | | Comma-separated values format used by PostgreSQL COPY. |
| `tsv` | | Tab-separated values, the default PostgreSQL COPY format. |
| `binary` | | Binary PostgreSQL COPY format. |
| `text` \| `xml` \| `json` | | A file containing a single text value. |

##### compression

`text` the specification of compression type. Can be set to any of the following values:

| **Format** | **Default** | **Description**                                                                                                                                                                      |
| --- | --- | --- |
| `auto` | `true` | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.gz`, it assumes `gzip`. Otherwise, it assumes `none`. |
| `gzip` | | Forces using gzip decoder to decompress the blob. |
| `none` | | Forces to treat the blob as one which doesn't require decompression. |

The extension doesn't support any other compression types.

##### options

`jsonb` the settings that define handling of custom headers, custom separators, escape characters, etc. `options` affects the behavior of this function in a way similar to how the options you can pass to the [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command in PostgreSQL affect its behavior.

#### Return type

`VOID`

### azure_storage.options_csv_get

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a csv file.

```sql
azure_storage.options_csv_get(delimiter text DEFAULT NULL::text, null_string text DEFAULT NULL::text, header boolean DEFAULT NULL::boolean, quote text DEFAULT NULL::text, escape text DEFAULT NULL::text, force_not_null text[] DEFAULT NULL::text[], force_null text[] DEFAULT NULL::text[], content_encoding text DEFAULT NULL::text);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### delimiter

`text` the character that separates columns within each row (line) of the file. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY delimiter must be a single one-byte character` error.

##### null_string

`text` the string that represents a null value. The default is \N (backslash-N) in text format, and an unquoted empty string in CSV format. You might prefer an empty string even in text format for cases where you don't want to distinguish nulls from empty strings.

##### header

`boolean` flag that indicates if  the file contains a header line with the names of each column in the file. On output, the initial line contains the column names from the table.

##### quote

`text` the quoting character to be used when a data value is quoted. The default is double-quote. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY quote must be a single one-byte character` error.

##### escape

`text` the character that should appear before a data character that matches the QUOTE value. The default is the same as the QUOTE value (so that the quoting character is doubled if it appears in the data). It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY escape must be a single one-byte character` error.

##### force_not_null

`text[]` don't match the specified columns' values against the null string. In the default case where the null string is empty, it means that empty values are read as zero-length strings rather than nulls, even when they aren't quoted.

##### force_null

`text[]` match the specified columns' values against the null string, even if quoted, and if a match is found, set the value to NULL. In the default case where the null string is empty, it converts a quoted empty string into NULL.

##### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

#### Return type

`jsonb`

### azure_storage.options_copy

Function that acts as a utility function, which can be called as a parameter within `blob_get`. It acts as a helper function for [options_csv_get](#azure_storageoptions_csv_get), [options_tsv](#azure_storageoptions_tsv), and [options_binary](#azure_storageoptions_binary).

```sql
azure_storage.options_copy(delimiter text DEFAULT NULL::text, null_string text DEFAULT NULL::text, header boolean DEFAULT NULL::boolean, quote text DEFAULT NULL::text, escape text DEFAULT NULL::text, force_quote text[] DEFAULT NULL::text[], force_not_null text[] DEFAULT NULL::text[], force_null text[] DEFAULT NULL::text[], content_encoding text DEFAULT NULL::text);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### delimiter

`text` the character that separates columns within each row (line) of the file. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY delimiter must be a single one-byte character` error.

##### null_string

`text` the string that represents a null value. The default is \N (backslash-N) in text format, and an unquoted empty string in CSV format. You might prefer an empty string even in text format for cases where you don't want to distinguish nulls from empty strings.

##### header

`boolean` flag that indicates if  the file contains a header line with the names of each column in the file. On output, the initial line contains the column names from the table.

##### quote

`text` the quoting character to be used when a data value is quoted. The default is double-quote. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY quote must be a single one-byte character` error.

##### escape

`text` the character that should appear before a data character that matches the QUOTE value. The default is the same as the QUOTE value (so that the quoting character is doubled if it appears in the data). It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY escape must be a single one-byte character` error.

##### force_quote

`text[]` forces quoting to be used for all non-NULL values in each specified column. NULL output is never quoted. If * is specified, non-NULL values are quoted in all columns.

##### force_not_null

`text[]` don't match the specified columns' values against the null string. In the default case where the null string is empty, it means that empty values are read as zero-length strings rather than nulls, even when they aren't quoted.

##### force_null

`text[]` match the specified columns' values against the null string, even if quoted, and if a match is found, set the value to NULL. In the default case where the null string is empty, it converts a quoted empty string into NULL.

##### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

#### Return type

`jsonb`

### azure_storage.options_tsv

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a tsv file.

```sql
azure_storage.options_tsv(delimiter text DEFAULT NULL::text, null_string text DEFAULT NULL::text, content_encoding text DEFAULT NULL::text);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### delimiter

`text` the character that separates columns within each row (line) of the file. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY delimiter must be a single one-byte character` error.

##### null_string

`text` the string that represents a null value. The default is \N (backslash-N) in text format, and an unquoted empty string in CSV format. You might prefer an empty string even in text format for cases where you don't want to distinguish nulls from empty strings.

##### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

#### Return type

`jsonb`

### azure_storage.options_binary

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a binary file.

```sql
azure_storage.options_binary(content_encoding text DEFAULT NULL::text);
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

##### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

#### Return type

`jsonb`

## Possible errors

### ERROR: azure_storage: Permission is no sufficient to perform requested operation

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) and the System Assigned Managed Identity is not granted the adequate data plane roles or permissions (typically a minimum of **Storage Blob Data Contributor** for azure_storage.blob_put, and a minimum of **Storage Blob Data Reader** for the other two functions).

It may also be the case that you have already granted the minimum required permissions but they are not yet in effect. It can take a few minutes until those permissions get propagated.

### ERROR: azure_storage: missing storage credentials

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) and the credentials with which you want the extension to authenticate with the storage account aren't registered using `azure_storage.account_add`.

### ERROR: azure_storage: internal error while connecting

When the instance of flexible server cannot reach the target storage account. That could happen in the following cases:
- The storage account doesn't exist.
- Networking configuration doesn't allow traffic originated from the instance of flexible server to reach the storage account. For example, when the instance of flexible server is deployed with public access networking, and the storage account is only accessible via private endpoints.

When the System Assigned Managed Identity is not enabled in the instance of flexible server.

### ERROR: azure_storage: storage credentials invalid format

When the System Assigned Managed Identity is enabled on the instance offlexible server, but the server has not been restarted after enabling it.

### ERROR:  azure_storage: current user <user_or_role> is not allowed to use storage account <account_name>

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) with a user or role which is not member of `azure_storage_admin` and is not granted permissions, using `azure_storage.account_user_add`, to use the referred storage account.

## Examples

You must meet the following prerequisites before you can run the following examples:

1. Create an Azure Storage account.
   To create an Azure Storage account, if you don't have one already, customize the values of `<resource_group>`, `<location>`, `<account_name>`, and `<container_name>`, and run the following Azure CLI command:
   ```azurecli-interactive
   resource_group=<resource_group>
   location=<location>
   storage_account=<account_name>
   blob_container=<container_name>
   az group create --name $resource_group --location $location
   az storage account create --resource-group $resource_group --name $storage_account --location $location --sku Standard_LRS --kind BlobStorage --public-network-access enabled --access-tier hot
   ```
1. Create a blob container.
   To create the blob container, run the following Azure CLI:
   ```azurecli-interactive
   az storage container create --account-name $storage_account --name $blob_container -o tsv
   ```
1. Fetch one of the two access keys assigned to the storage account. Make sure you copy the value of your access_key as you need to pass it as an argument to [azure_storage.account_add](#azure_storageaccount_add) in a subsequent step.
   To fetch the first of the two access keys, run the following Azure CLI command:
   ```azurecli-interactive
   access_key=$(az storage account keys list --resource-group $resource_group --account-name $storage_account --query [0].value)
   echo "Following is the value of your access key:"
   echo $access_key
   ```
1. Download the file with the data set that is used during the examples, and upload it to your blob container.
   To download the file with the data set, run the following Azure CLI command:
   ```azurecli-interactive   
   mkdir --parents azure_storage_examples
   cd azure_storage_examples
   curl -O https://examples.citusdata.com/tutorial/events.csv
   gzip -k events.csv
   cp events.csv events_blob_without_extension
   cp events.csv events_pipe.csv
   cp events.csv.gz events_compressed
   sed -i 's/,/|/g' events_pipe.csv
   az storage blob upload-batch --account-name $storage_account --destination $blob_container --source . --pattern "events*" --account-key $access_key --overwrite --output none --only-show-errors
   ```

> [!NOTE]  
> You can list containers or the blobs stored in them for a specific storage account, but only if your PostgreSQL user or role is granted permission on the reference to that storage account by using [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of the `azure_storage_admin` role are granted this privilege over all Azure Storage accounts that have been added using [azure_storage.account_add](#azure_storageaccount_add). By default, only members of `azure_pg_admin` are granted the `azure_storage_admin` role.

### Create table in which data is loaded

Let's create the table into which we import the contents of the CSV file that we uploaded to the storage account. To do so, connect to your instance of Azure Database for PostgreSQL flexible server using `PgAdmin`, `psql`, or the client of your preference, and execute the following statement:

```sql
CREATE TABLE IF NOT EXISTS events
        (
         event_id bigint
        ,event_type text
        ,event_public boolean
        ,repo_id bigint
        ,payload jsonb
        ,repo jsonb
        ,user_id bigint
        ,org jsonb
        ,created_at timestamp without time zone
        );
```

### Add access key of storage account

This example illustrates how to add a reference to a storage account, together with the access key of that storage account which is required to access its content via the functionality provided by the `azure_storage` extension in your instance of Azure Database for PostgreSQL flexible server.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

Similarly, `<access_key>` must be set to the value you fetched from your storage account.

```sql
SELECT azure_storage.account_add('<account_name>', '<access_key>');
```
> [!TIP]  
> If you want to retrieve the storage account name and one of its access keys from the Azure portal, search for your storage account, in the resource menu select **Access keys**, copy the **Storage account name** and copy the **Key** from **key1** section (you have to select **Show** next to the key first).

### Remove reference to storage account

This example illustrates how to remove any reference to a storage account, so that no user in the current database can use the `azure_storage` extension functionality to access that storage account.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

```sql
SELECT azure_storage.account_remove('<account_name>');
```

### Grant access to a user or role on the Azure Blob storage reference

This example illustrates how to grant access to a user or role named `<regular_user>`, so that such PostgreSQL user can use the `azure_storage` extension to access the blobs stored in containers hosted by the referred Azure storage account.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<regular_user>` must be set to the name of an existing user or role.

```sql
SELECT * FROM azure_storage.account_user_add('<account_name>', '<regular_user>');
```

### List all the references to Azure storage accounts

This example illustrates how to find out which Azure storage accounts the `azure_storage` extension can reference in this database, together with the type of authentication that is used to access each storage account, and which users or roles are granted permission, via the [azure_storage.account_user_add](#azure_storageaccount_user_add) function, to access that Azure storage account through the functionality provided by the extension.

```sql
SELECT * FROM azure_storage.account_list();
```

### Revoke access from a user or role on the Azure Blob storage reference

This example illustrates how to revoke access from a user or role named `<regular_user>`, so that such PostgreSQL user can't use the `azure_storage` extension to access the blobs stored in containers hosted by the referred Azure storage account. 

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<regular_user>` must be set to the name of an existing user or role.

```sql
SELECT * FROM azure_storage.account_user_remove('<account_name>', '<regular_user>');
```

### List all blobs in a container

This example illustrates how to list all existing blobs inside container `<container_name>` of storage account `<account_name>`.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_list('<account_name>','<container_name>');
```

### List the objects with specific blob name prefix

This example illustrates how to list all existing blobs inside container `<container_name>` of storage account `<account_name>`, whose blob name begins with `<blob_name_prefix>`.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

`<blob_name_prefix>` should be set to whatever prefix you want the blobs enumerated to include in their names. If you want to return all blobs, you can set this parameter to an empty string or don't even specify a value for this parameter, in which case the value defaults to an empty string.

```sql
SELECT * FROM azure_storage.blob_list('<account_name>','<container_name>','<blob_name_prefix>');
```

Alternatively, you can use the following syntax:

```sql
SELECT * FROM azure_storage.blob_list('<account_name>','<container_name>') WHERE path LIKE '<blob_name_prefix>%';
```

### Read content from a blob in a container

The `blob_get` function retrieves the contents of one specific blob (`events.csv` in this case), in the referred container `<container_name>` of the `<account_name>` storage. In order for `blob_get` to know how to parse the data you can pass a value in the form `NULL::table_name`, where `table_name` refers to a table whose schema matches that of the blob being read. In the example, it refers to the `events` table we created at the very beginning.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

`<blob_name>` should be set to the full path of the blob whose contents you want to read.

```sql
SELECT * FROM azure_storage.blob_get
        ('<account_name>'
        ,'<container_name>'
        ,'events.csv'
        , NULL::events)
LIMIT 5;
```

Alternatively, you can explicitly define the schema of the result using the `AS` clause after the [blob_get](#azure_storageblob_get) function.

```sql
SELECT * FROM azure_storage.blob_get('<account_name>','<container_name>','events.csv.gz')
AS res (
         event_id BIGINT
        ,event_type TEXT
        ,event_public BOOLEAN
        ,repo_id BIGINT
        ,payload JSONB
        ,repo JSONB
        ,user_id BIGINT
        ,org JSONB
        ,created_at TIMESTAMP WITHOUT TIME ZONE)
LIMIT 5;
```

### Use the decoder option

This example illustrates the use of the `decoder` option. Normally format is inferred from the extension of the file, but when the file content doesn't have a matching extension you can pass the decoder argument.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_get
        ('<account_name>'
        ,'<container_name>'
        ,'events_blob_without_extension'
        , NULL::events
        , decoder := 'csv')
LIMIT 5;
```

### Use compression with decoder option

This example shows how to enforce using the gzip compression on a gzip compressed blob whose name doesn't end with a .gz extension.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_get
        ('<account_name>'
        ,'<container_name>'
        ,'events_compressed'
        , NULL::events
        , decoder := 'csv'
        , compression := 'gzip')
LIMIT 5;
```

### Import filtered content and modify before loading from csv format object

This example illustrates the possibility to filter and modify the content imported from the blob, before loading that into a SQL table.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT concat('P-',event_id::text) FROM azure_storage.blob_get
        ('<account_name>'
        ,'<container_name>'
        ,'events.csv'
        , NULL::events)
WHERE event_type='PushEvent'
LIMIT 5;
```

### Query content from file with headers, custom separators, escape characters

This example illustrates how you can use custom separators and escape characters, by passing the result of [options_copy](#azure_storageoptions_copy) to the `options` argument.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_get
        ('<account_name>'
        ,'<container_name>'
        ,'events_pipe.csv'
        ,NULL::events
        ,options := azure_storage.options_csv_get(delimiter := '|' , header := 'true')
        );
```

### Aggregation query over the contents of a blob

This example illustrates how you can do aggregation operations over information that is stored in a blob container, without the need to import the contents of the blob into PostgreSQL tables.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT event_type, COUNT(*) FROM azure_storage.blob_get
        ('<account_name>'
        ,'<container_name>'
        ,'events.csv'
        , NULL::events)
GROUP BY event_type
ORDER BY 2 DESC
LIMIT 5;
```

### Import data using a COPY statement

The following example shows the import of data from a blob called `events.csv`  that resides in the blob container `<container_name>` in the Azure Storage account `<account_name>`, via the `COPY` command:

1. Create a table that matches the schema of the source file:

    ```sql
    CREATE TABLE IF NOT EXISTS events
            (
             event_id bigint
            ,event_type text
            ,event_public boolean
            ,repo_id bigint
            ,payload jsonb
            ,repo jsonb
            ,user_id bigint
            ,org jsonb
            ,created_at timestamp without time zone
            );
    ```

2. Use a `COPY` statement to copy data into the target table. Specify that the first row contains column headers.

    ```sql
    COPY events
    FROM 'https://<account_name>.blob.core.windows.net/<container_name>/events.csv'
    WITH (FORMAT 'csv', header);
    ```

### Write content to a blob in a container

The `blob_put` function composes the contents of one specific blob (`eventscopy.csv` in this case), and uploads it to the referred container `<container_name>` of the `<account_name>` storage. This example uses `blob_get` to construct a set of five rows, which are then passed to the `blob_put` aggregate function which uploads them as a blob named `eventscopy.csv`.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT azure_storage.blob_put
        ('<account_name>'
        ,'<container_name>'
        ,'eventscopy.csv'
        , top_5_events)
FROM (SELECT * FROM azure_storage.blob_get
                     ('<account_name>'
                     ,'<container_name>'
                     ,'events.csv'
                     , NULL::events) LIMIT 5) AS top_5_events;
```

### Export data using a COPY statement

The following example shows the export of data from a table called `events`, to a blob called `events_exported.csv` that resides in the blob container `<container_name>` in the Azure Storage account `<account_name>`, via the `COPY` command:

1. Create a table that matches the schema of the source file:

    ```sql
    CREATE TABLE IF NOT EXISTS events
            (
             event_id bigint
            ,event_type text
            ,event_public boolean
            ,repo_id bigint
            ,payload jsonb
            ,repo jsonb
            ,user_id bigint
            ,org jsonb
            ,created_at timestamp without time zone
            );
    ```

2. Load data into the table. Either run INSERT statements to populate it with several synthetic rows, or use the [Import data using a COPY statement](#import-data-using-a-copy-statement) example to populate it with the contents of the sample data set.

3. Use a `COPY` statement to copy data into the target table. Specify that the first row contains column headers.

   ```sql
   COPY events
   TO 'https://<account_name>.blob.core.windows.net/<container_name>/events_exported.csv'
   WITH (FORMAT 'csv', header);
   ```

## Related content

- [Import and export data using Azure Storage in Azure Database for PostgreSQL flexible server](concepts-storage-extension.md).
- [Extensions and modules](../extensions/concepts-extensions.md).
