---
title: Copy data with pg_azure_storage extension in Azure Database for PostgreSQL - Flexible Server
description: Learn how to use the pg_azure_storage extension in Azure Database for PostgreSQL - Flexible Server to import and export data
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 10/31/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: reference
ms.custom:
  - ignite-2023
---

# How to import and export data using pg_azure_storage extension in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The [pg_azure_storage](./concepts-storage-extension.md) extension allows you to import or export data in multiple file formats, directly between Azure Storage accounts and an instance of Azure Database for PostgreSQL Flexible Server.

Examples of data export and import using this extension can be found in the [Examples](#examples) section of this article.

To use the `pg_azure_storage` extension on your Azure Database for PostgreSQL flexible server instance, you need to add the extension to the `shared_preload_libraries`, and also add it to the `azure.extensions` server parameter, as described in [how to use PostgreSQL extensions](./concepts-extensions.md#how-to-use-postgresql-extensions). 

Because `shared_preload_library` is a static server parameter, it requires a restart of the server for the change to take effect.

Once the server has been restarted, connect to your instance of PostgreSQL using the client of your preference (ie psql, pgAdmin, etc). Confirm that `SHOW azure.extensions;`, and `SHOW shared_preload_libraries;`, both include the value `azure_storage` in the list of the comma-separated values returned by each of the `SHOW` statements.

Only then you can install the extension, by connecting to your target database, and running the [CREATE EXTENSION](https://www.postgresql.org/docs/current/static/sql-createextension.html) statement. You need to repeat the command separately for each database in which you want the extension to be available.

```sql
CREATE EXTENSION azure_storage;
```

## Permissions

Your Azure blob storage access keys are similar to a root password for your storage account. Always be careful to protect your access keys. Use Azure Key Vault to manage and rotate your keys securely. The account key is stored in a table that is accessible only by the superuser.

Users granted the `azure_storage_admin` role can interact with this table using the following functions:
* account_add
* account_list
* account_remove
* account_user_add
* account_user_remove

The `azure_storage_admin` role is, by default, granted to the `azure_pg_admin` role.

## azure_storage.account_add

Function that allows adding a storage account and its associated access key, to the list of storage accounts that the `pg_azure_storage` extension can access.

If a previous invocation of this function already added the reference to this storage account, it doesn't add a new entry but instead updates the access key of the existing entry.

> [!NOTE]  
> This function doesn't validate if the referred account name exists or if it's accessible with the access key provided. However, it validates that the name of the storage account is valid, according to the naming validation rules imposed on Azure storage accounts.

```sql
azure_storage.account_add(account_name_p text, account_key_p text);
```

### Permissions

Must be a member of `azure_storage_admin`.

### Arguments

#### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### account_key_p

`text` the value of one of the access keys for the storage account. Your Azure blob storage access keys are similar to a root password for your storage account. Always be careful to protect your access keys. Use Azure Key Vault to manage and rotate your keys securely. The account key is stored in a table that is accessible only by the superuser. Users granted the `azure_storage_admin` role can interact with this table via functions. To see which storage accounts are added, use the function [account_list](#azure_storageaccount_list).

## azure_storage.account_remove

Function that allows removing a storage account and its associated access key from the list of storage accounts that the `pg_azure_storage` extension can access.

```sql
azure_storage.account_remove(account_name_p text);
```

### Permissions

Must be a member of `azure_storage_admin`.

### Arguments

#### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

## azure_storage.account_user_add

Function that allows granting a PostgreSQL user or role access to a storage account through the functions provided by the `pg_azure_storage` extension.

> [!NOTE]  
> The execution of this function only succeeds if the storage account, whose name is being passed as the first argument, was already created using [account_add](#azure_storageaccount_add), and if the user or role, whose name is passed as the second argument, already exists.

```sql
azure_storage.account_add(account_name_p text, user_p regrole);
```

### Permissions

Must be a member of `azure_storage_admin`.

### Arguments

#### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### user_p

`regrole` the name of a PostgreSQL user or role available on the server.

## azure_storage.account_user_remove

Function that allows revoking a PostgreSQL user or role access to a storage account through the functions provided by the `pg_azure_storage` extension.

> [!NOTE]
> The execution of this function only succeeds if the storage account whose name is being passed as the first argument has already been created using [account_add](#azure_storageaccount_add), and if the user or role whose name is passed as the second argument still exists.
> When a user or role is dropped from the server, by executing `DROP USER | ROLE`, the permissions that were granted on any reference to Azure storage accounts are also automatically eliminated.

```sql
azure_storage.account_remove(account_name_p text, user_p regrole);
```

### Permissions

Must be a member of `azure_storage_admin`.

### Arguments

#### account_name_p

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### user_p

`regrole` the name of a PostgreSQL user or role available on the server.

## azure_storage.account_list

Function that lists the names of the storage accounts that were configured via the [account_add](#azure_storageaccount_add) function, together with the PostgreSQL users or roles that are granted permissions to interact with that storage account through the functions provided by the `pg_azure_storage` extension.

```sql
azure_storage.account_list();
```

### Permissions

Must be a member of `azure_storage_admin`.

### Arguments

This function doesn't take any arguments.

### Return type

`TABLE(account_name text, allowed_users regrole[])` a two-column table with the list of Azure blob storage accounts added, and the list of PostgreSQL users or roles that are granted access to it.

## azure_storage.blob_list

Function that lists the names and other properties (size, lastModified, eTag, contentType, contentEncoding, and contentHash) of blobs stored in the given container of the referred storage account.

```sql
azure_storage.blob_list(account_name text, container_name text, prefix text DEFAULT ''::text);
```

### Permissions

User or role invoking this function must be added to the allowed list for the `account_name` referred, by executing [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of `azure_storage_admin` are automatically allowed to reference all Azure Storage accounts whose references were added using [azure_storage.account_add](#azure_storageaccount_add).

### Arguments

#### account_name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### container_name

`text` the name of a container. A container organizes a set of blobs, similar to a directory in a file system. A storage account can include an unlimited number of containers, and a container can store an unlimited number of blobs.
A container name must be a valid Domain Name System (DNS) name, as it forms part of the unique URI used to address the container or its blobs.
When naming a container, make sure to follow [these rules](/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names).

The URI for a container is similar to:
`https://myaccount.blob.core.windows.net/mycontainer`

#### prefix

`text` when specified, the function returns the blobs whose names begin with the value provided in this parameter. Defaults to an empty string.

### Return type

`TABLE(path text, bytes bigint, last_modified timestamp with time zone, etag text, content_type text, content_encoding text, content_hash text)` a table with one record per blob returned, including the full name of the blob, and some other properties.

#### path

`text` the full name of the blob.

#### bytes

`bigint` the size of blob in bytes.

#### last_modified

`timestamp with time zone`the date and time the blob was last modified. Any operation that modifies the blob, including an update of the blob's metadata or properties, changes the last-modified time of the blob.

#### etag

`text` the ETag property is used for optimistic concurrency during updates. It isn't a timestamp as there's another property called Timestamp that stores the last time a record was updated. For example, if you load an entity and want to update it, the ETag must match what is currently stored. Setting the appropriate ETag is important because if you have multiple users editing the same item, you don't want them overwriting each other's changes.

#### content_type

`text` the content type specified for the blob. The default content type is `application/octet-stream`.

#### content_encoding

`text` the Content-Encoding property of a blob that Azure Storage allows you to define. For compressed content, you could set the property to be Gzip. When the browser accesses the content, it automatically decompresses the content.

#### content_hash

`text` the hash used to verify the integrity of the blob during transport. When this header is specified, the storage service checks the provided hash with one computed from content. If the two hashes don't match, the operation fails with error code 400 (Bad Request).


## azure_storage.blob_get

Function that allows importing data. It downloads one or more files from a blob container in an Azure Storage account. Then it translates the contents into rows, which can be consumed and processed with SQL language constructs. This function adds support to filter and manipulate the data fetched from the blob container before importing it.

> [!NOTE]  
> Before trying to access the container for the referred storage account, this function checks if the names of the storage account and container passed as arguments are valid according to the naming validation rules imposed on Azure storage accounts. If either of them is invalid, an error is raised.

```sql
azure_storage.blob_get(account_name text, container_name text, path text, decoder text DEFAULT 'auto'::text, compression text DEFAULT 'auto'::text, options jsonb DEFAULT NULL::jsonb);
```

There's an overloaded version of this function, which accepts a `rec` parameter that allows you to conveniently define the output format record.

```sql
azure_storage.blob_get(account_name text, container_name text, path text, rec anyelement, decoder text DEFAULT 'auto'::text, compression text DEFAULT 'auto'::text, options jsonb DEFAULT NULL::jsonb);
```

### Permissions

User or role invoking this function must be added to the allowed list for the `account_name` referred, by executing [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of `azure_storage_admin` are automatically allowed to reference all Azure Storage accounts whose references were added using [azure_storage.account_add](#azure_storageaccount_add).

### Arguments

#### account_name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### container_name

`text` the name of a container. A container organizes a set of blobs, similar to a directory in a file system. A storage account can include an unlimited number of containers, and a container can store an unlimited number of blobs.
A container name must be a valid Domain Name System (DNS) name, as it forms part of the unique URI used to address the container or its blobs.
When naming a container, make sure to follow [these rules](/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names).

The URI for a container is similar to:
`https://myaccount.blob.core.windows.net/mycontainer`

#### path

`text` the full name of the blob.

#### rec

`anyelement` the definition of the record output structure.

#### decoder

`text` the specification of the blob format. Can be set to any of the following values:

| **Format** | **Default** | **Description** |
| --- | --- | --- |
| `auto` | `true`      | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.csv` or `.csv.gz`, it assumes `csv`. If ends with `.tsv` or `.tsv.gz`, it assumes it's `tsv`. If ends with `.json`, `.json.gz`, `.xml`, `.xml.gz`, `.txt`, or `.txt.gz`, it assumes it's `text`. |
| `csv` | | Comma-separated values format used by PostgreSQL COPY. |
| `tsv` | | Tab-separated values, the default PostgreSQL COPY format. |
| `binary` | | Binary PostgreSQL COPY format. |
| `text` \| `xml` \| `json` | | A file containing a single text value. |

#### compression

`text` the specification of compression type. Can be set to any of the following values:

| **Format** | **Default** | **Description**                                                                                                                                                                      |
| --- | --- | --- |
| `auto` | `true` | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.gz`, it assumes it's `gzip`. Otherwise, it assumes it's `none`. |
| `gzip` | | Forces using gzip decoder to decompress the blob. |
| `none` | | Forces to treat the blob as one which doesn't require decompression. |

The extension doesn't support any other compression types.

#### options

`jsonb` the settings that define handling of custom headers, custom separators, escape characters, etc. `options` affects the behavior of this function in a way similar to how the options you can pass to the [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command in PostgreSQL affect its behavior.

### Return type

`SETOF record` 
`SETOF  anyelement`

## azure_storage.blob_put

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

### Permissions

User or role invoking this function must be added to the allowed list for the `account_name` referred, by executing [azure_storage.account_user_add](#azure_storageaccount_user_add). Members of `azure_storage_admin` are automatically allowed to reference all Azure Storage accounts whose references were added using [azure_storage.account_add](#azure_storageaccount_add).

### Arguments

#### account_name

`text` the name of the Azure blob storage account that contains all of your objects: blobs, files, queues, and tables. The storage account provides a unique namespace that is accessible from anywhere in the world over HTTPS.

#### container_name

`text` the name of a container. A container organizes a set of blobs, similar to a directory in a file system. A storage account can include an unlimited number of containers, and a container can store an unlimited number of blobs.
A container name must be a valid Domain Name System (DNS) name, as it forms part of the unique URI used to address the container or its blobs.
When naming a container, make sure to follow [these rules](/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names).

The URI for a container is similar to:
`https://myaccount.blob.core.windows.net/mycontainer`

#### path

`text` the full name of the blob.

#### tuple

`record` the definition of the record output structure.

#### encoder

`text` the specification of the blob format. Can be set to any of the following values:

| **Format** | **Default** | **Description** |
| --- | --- | --- |
| `auto` | `true`      | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.csv` or `.csv.gz`, it assumes  it's `csv`. If ends with `.tsv` or `.tsv.gz`, it assumes it's `tsv`. If ends with `.json`, `.json.gz`, `.xml`, `.xml.gz`, `.txt`, or `.txt.gz`, it assumes it's `text`. |
| `csv` | | Comma-separated values format used by PostgreSQL COPY. |
| `tsv` | | Tab-separated values, the default PostgreSQL COPY format. |
| `binary` | | Binary PostgreSQL COPY format. |
| `text` \| `xml` \| `json` | | A file containing a single text value. |

#### compression

`text` the specification of compression type. Can be set to any of the following values:

| **Format** | **Default** | **Description**                                                                                                                                                                      |
| --- | --- | --- |
| `auto` | `true` | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.gz`, it assumes it's `gzip`. Otherwise, it assumes it's `none`. |
| `gzip` | | Forces using gzip decoder to decompress the blob. |
| `none` | | Forces to treat the blob as one which doesn't require decompression. |

The extension doesn't support any other compression types.

#### options

`jsonb` the settings that define handling of custom headers, custom separators, escape characters, etc. `options` affects the behavior of this function in a way similar to how the options you can pass to the [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command in PostgreSQL affect its behavior.

### Return type

`SETOF record` 
`SETOF  anyelement`

## azure_storage.options_csv_get

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a csv file.

```sql
azure_storage.options_csv_get(delimiter text DEFAULT NULL::text, null_string text DEFAULT NULL::text, header boolean DEFAULT NULL::boolean, quote text DEFAULT NULL::text, escape text DEFAULT NULL::text, force_not_null text[] DEFAULT NULL::text[], force_null text[] DEFAULT NULL::text[], content_encoding text DEFAULT NULL::text);
```

### Arguments

#### delimiter

`text` the character that separates columns within each row (line) of the file. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY delimiter must be a single one-byte character` error.

#### null_string

`text` the string that represents a null value. The default is \N (backslash-N) in text format, and an unquoted empty string in CSV format. You might prefer an empty string even in text format for cases where you don't want to distinguish nulls from empty strings.

#### header

`boolean` flag that indicates if  the file contains a header line with the names of each column in the file. On output, the initial line contains the column names from the table.

#### quote

`text` the quoting character to be used when a data value is quoted. The default is double-quote. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY quote must be a single one-byte character` error.

#### escape

`text` the character that should appear before a data character that matches the QUOTE value. The default is the same as the QUOTE value (so that the quoting character is doubled if it appears in the data). It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY escape must be a single one-byte character` error.

#### force_not_null

`text[]` don't match the specified columns' values against the null string. In the default case where the null string is empty, it means that empty values are read as zero-length strings rather than nulls, even when they aren't quoted.

#### force_null

`text[]` match the specified columns' values against the null string, even if quoted, and if a match is found, set the value to NULL. In the default case where the null string is empty, it converts a quoted empty string into NULL.

#### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

### Return type

`jsonb`

## azure_storage.options_copy

Function that acts as a utility function, which can be called as a parameter within `blob_get`. It acts as a helper function for [options_csv_get](#azure_storageoptions_csv_get), [options_tsv](#azure_storageoptions_tsv), and [options_binary](#azure_storageoptions_binary).

```sql
azure_storage.options_copy(delimiter text DEFAULT NULL::text, null_string text DEFAULT NULL::text, header boolean DEFAULT NULL::boolean, quote text DEFAULT NULL::text, escape text DEFAULT NULL::text, force_quote text[] DEFAULT NULL::text[], force_not_null text[] DEFAULT NULL::text[], force_null text[] DEFAULT NULL::text[], content_encoding text DEFAULT NULL::text);
```

### Arguments

#### delimiter

`text` the character that separates columns within each row (line) of the file. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY delimiter must be a single one-byte character` error.

#### null_string

`text` the string that represents a null value. The default is \N (backslash-N) in text format, and an unquoted empty string in CSV format. You might prefer an empty string even in text format for cases where you don't want to distinguish nulls from empty strings.

#### header

`boolean` flag that indicates if  the file contains a header line with the names of each column in the file. On output, the initial line contains the column names from the table.

#### quote

`text` the quoting character to be used when a data value is quoted. The default is double-quote. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY quote must be a single one-byte character` error.

#### escape

`text` the character that should appear before a data character that matches the QUOTE value. The default is the same as the QUOTE value (so that the quoting character is doubled if it appears in the data). It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY escape must be a single one-byte character` error.

#### force_quote

`text[]` forces quoting to be used for all non-NULL values in each specified column. NULL output is never quoted. If * is specified, non-NULL values are quoted in all columns.

#### force_not_null

`text[]` don't match the specified columns' values against the null string. In the default case where the null string is empty, it means that empty values are read as zero-length strings rather than nulls, even when they aren't quoted.

#### force_null

`text[]` match the specified columns' values against the null string, even if quoted, and if a match is found, set the value to NULL. In the default case where the null string is empty, it converts a quoted empty string into NULL.

#### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

### Return type

`jsonb`

## azure_storage.options_tsv

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a tsv file.

```sql
azure_storage.options_tsv(delimiter text DEFAULT NULL::text, null_string text DEFAULT NULL::text, content_encoding text DEFAULT NULL::text);
```

### Arguments

#### delimiter

`text` the character that separates columns within each row (line) of the file. It must be a single 1-byte character. Although this function supports delimiters of any number of characters, if you try to use more than a single 1-byte character, PostgreSQL reports back a `COPY delimiter must be a single one-byte character` error.

#### null_string

`text` the string that represents a null value. The default is \N (backslash-N) in text format, and an unquoted empty string in CSV format. You might prefer an empty string even in text format for cases where you don't want to distinguish nulls from empty strings.

#### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

### Return type

`jsonb`

## azure_storage.options_binary

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a binary file.

```sql
azure_storage.options_binary(content_encoding text DEFAULT NULL::text);
```

### Arguments

#### content_encoding

`text` name of the encoding with which the file is encoded. If the option is omitted, the current client encoding is used.

### Return type

`jsonb`

## Examples

You must meet the following prerequistes before you can run the following examples:

1. Create an Azure Storage account.
   To create an Azure Storage account, if you don't have one already, customize the values of `<resource_group>`, `<location>`, `<storage_account>`, and `<blob_container>`, and run the following Azure CLI command:
   ```azurecli
   resource_group=<resource_group>
   location=<location>
   storage_account=<storage_account>
   blob_container=<blob_container>
   az group create --name $resource_group --location $location
   az storage account create --resource-group $resource_group --name $storage_account --location $location --sku Standard_LRS --kind BlobStorage --public-network-access enabled --access-tier hot
   ```
1. Create a blob container.
   To create the blob container, run the following Azure CLI:
   ```azurecli
   az storage container create --account-name $storage_account --name $blob_container -o tsv
   ```
1. Fetch one of the two access keys assigned to the storage account. Make sure you copy the value of your access_key as you need to pass it as an argument to [account_add](#azure_storageaccount_add) in a subsequent step.
   To fetch the first of the two access keys, run the following Azure CLI command:
   ```azurecli
   access_key=$(az storage account keys list --resource-group $resource_group --account-name $storage_account --query [0].value)
   echo "Following is the value of your access key:"
   echo $access_key
   ```
1. Download the file with the data set that is used during the examples, and upload it to your blob container.
   To download the file with the data set, run the following Azure CLI command:
   ```azurecli   
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
> You can list containers or the blobs stored in them for a specific storage account, but only if your PostgreSQL user or role is granted permission on on the reference to that storage account by using [account_user_add](#azure_storageaccount_user_add). Members of the `azure_storage_admin` role are granted this privilege over all Azure Storage accounts that have been added using [azure_storage.account_add](#azure_storageaccount_add). By default, only members of `azure_pg_admin` are granted the `azure_storage_admin` role.

### Create table in which data is loaded

Let's create the table into which we import the contents of the CSV file that we uploaded to the storage account. To do so, connect to your instance of Azure Database for PostgreSQL flexible server using `PgAdmin`, `psql`, or the client of your preference, and execute the following statement:

```sql
CREATE TABLE IF NOT EXISTS public.events
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

This example illustrates how to add a reference to a storage account, together with the access key of that storage account which is required to access its content via the functionality provided by the `pg_azure_storage` extension in your instance of Azure Database for PostgreSQL flexible server.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

Similarly, `<access_key>` must be set to the value you fetched from your storage account.

```sql
SELECT azure_storage.account_add('<storage_account>', '<access_key>');
```
> [!TIP]  
> If you want to retrieve the storage account name and one of its access keys from the Azure portal, search for your storage account, in the resource menu select **Access keys**, copy the **Storage account name** and copy the **Key** from **key1** section (you have to select **Show** next to the key first).

### Remove reference to storage account

This example illustrates how to remove any reference to a storage account, so that no user in the current database can use the `pg_azure_storage` extension functionality to access that storage account.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

```sql
SELECT azure_storage.account_remove('<storage_account>');
```

### Grant access to a user or role on the Azure Blob storage reference

This example illustrates how to grant access to a user or role named `<regular_user>`, so that such PostgreSQL user can use the `pg_azure_storage` extension to access the blobs stored in containers hosted by the referred Azure storage account.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<regular_user>` must be set to the name of an existing user or role.

```sql
SELECT * FROM azure_storage.account_user_add('<storage_account>', '<regular_user>');
```

### List all the references to Azure storage accounts

This example illustrates how to find out which Azure storage accounts the `pg_azure_storage` extension can reference in this database, together with the type of authentication that is used to access each storage account, and which users or roles are granted permission, via the [account_user_add](#azure_storageaccount_user_add) function, to access that Azure storage account through the functionality provided by the extension.

```sql
SELECT * FROM azure_storage.account_list();
```

### Revoke access from a user or role on the Azure Blob storage reference

This example illustrates how to revoke access from a user or role named `<regular_user>`, so that such PostgreSQL user can't use the `pg_azure_storage` extension to access the blobs stored in containers hosted by the referred Azure storage account. 

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<regular_user>` must be set to the name of an existing user or role.

```sql
SELECT * FROM azure_storage.account_user_remove('<storage_account>', '<regular_user>');
```

### List all blobs in a container

This example illustrates how to list all existing blobs inside container `<container_name>` of storage account `<storage_account>`.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_list('<storage_account>','<blob_container>');
```

### List the objects with specific blob name prefix

This example illustrates how to list all existing blobs inside container `<blob_container>` of storage account `<storage_account>`, whose blob name begins with `<blob_name_prefix>`.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

`<blob_name_prefix>` should be set to the whatever prefix you want the blobs enumerated to include in their names. If you want to return all blobs, you can set this parameter to an empty string or don't even specify a value for this parameter, in which case the value defaults to an empty string.

```sql
SELECT * FROM azure_storage.blob_list('<storage_account>','<blob_container>','<blob_name_prefix>');
```

Alternatively, you can use the following syntax:

```sql
SELECT * FROM azure_storage.blob_list('<storage_account>','<blob_container>') WHERE path LIKE '<blob_name_prefix>%';
```

### Read content from a blob in a container

The `blob_get` function retrieves the contents of one specific blob (`events.csv` in this case), in the referred container `<blob_container>` of the `<storage_account>` storage. In order for `blob_get` to know how to parse the data you can pass a value in the form `NULL::table_name`, where `table_name` refers to a table whose schema matches that of the blob being read. In the example, it refers to the `events` table we created at the very beginning.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

`<blob_name_prefix>` should be set to the whatever prefix you want the blobs enumerated to include in their names. If you want to return all blobs, you can set this parameter to an empty string or don't even specify a value for this parameter, in which case the value defaults to an empty string.

```sql
SELECT * FROM azure_storage.blob_get
        ('<storage_account>'
        ,'<blob_container>'
        ,'events.csv'
        , NULL::events)
LIMIT 5;
```

Alternatively, you can explicitly define the schema of the result using the `AS` clause after the [blob_get](#azure_storageblob_get) function.

```sql
SELECT * FROM azure_storage.blob_get('<storage_account>','<blob_container>','events.csv.gz')
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

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_get
        ('<storage_account>'
        ,'<blob_container>'
        ,'events_blob_without_extension'
        , NULL::events
        , decoder := 'csv')
LIMIT 5;
```

### Use compression with decoder option

This example shows how to enforce using the gzip compression on a gzip compressed blob whose name doesn't end with a .gz extension.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_get
        ('<storage_account>'
        ,'<blob_container>'
        ,'events_compressed'
        , NULL::events
        , decoder := 'csv'
        , compression := 'gzip')
LIMIT 5;
```

### Import filtered content and modify before loading from csv format object

This example illustrates the possibility to filter and modify the content imported from the blob, before loading that into a SQL table.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT concat('P-',event_id::text) FROM azure_storage.blob_get
        ('<storage_account>'
        ,'<blob_container>'
        ,'events.csv'
        , NULL::events)
WHERE event_type='PushEvent'
LIMIT 5;
```

### Query content from file with headers, custom separators, escape characters

This example illustrates how you can use custom separators and escape characters, by passing the result of [options_copy](#azure_storageoptions_copy) to the `options` argument.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_get
        ('<storage_account>'
        ,'<blob_container>'
        ,'events_pipe.csv'
        ,NULL::events
        ,options := azure_storage.options_csv_get(delimiter := '|' , header := 'true')
        );
```

### Aggregation query over the contents of a blob

This example illustrates how you can do aggregation operations over information that is stored in a blob container, without the need to import the contents of the blob into PostgreSQL tables.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT event_type, COUNT(*) FROM azure_storage.blob_get
        ('<storage_account>'
        ,'<blob_container>'
        ,'events.csv'
        , NULL::events)
GROUP BY event_type
ORDER BY 2 DESC
LIMIT 5;
```

### Write content to a blob in a container

The `blob_put` function composes the contents of one specific blob (`eventscopy.csv` in this case), and uploads it to the referred container `<blob_container>` of the `<storage_account>` storage. This example uses `blob_get` to construct a set of five rows, which are then passed to the `blob_put` aggregate function which uploads them as a blob named `eventscopy.csv`.

`<storage_account>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<blob_container>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT azure_storage.blob_put
        ('<storage_account>'
        ,'<blob_container>'
        ,'eventscopy.csv'
        , top_5_events)
FROM (SELECT * FROM azure_storage.blob_get
                     ('<storage_account>'
                     ,'<blob_container>'
                     ,'events.csv'
                     , NULL::events) LIMIT 5) AS top_5_events;
```

## Related content

- [Import and export data using Azure Storage in Azure Database for PostgreSQL - Flexible Server](concepts-storage-extension.md)