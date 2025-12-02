---
title: Function Reference for Azure Storage Extension
description: Learn everything about the functions provided by the Azure Storage extension in Azure Database for PostgreSQL.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 08/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: reference
ms.custom:
- ignite-2024
- sfi-image-nochange
---

# Reference of functions provided by the Azure Storage extension in Azure Database for PostgreSQL 

Following is the list of functions provided by the Azure Storage extension:

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
| `auto` | `true`      | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.parquet`, it assumes `parquet`. If ends with `.csv` or `.csv.gz`, it assumes `csv`. If ends with `.tsv` or `.tsv.gz`, it assumes `tsv`. If ends with `.json`, `.json.gz`, `.xml`, `.xml.gz`, `.txt`, or `.txt.gz`, it assumes `text`. |
| `binary` | | Binary PostgreSQL COPY format. |
| `csv` | | Comma-separated values format used by PostgreSQL COPY. |
| `parquet` | | Parquet format. |
| `text` \| `xml` \| `json` | | A file containing a single text value. |
| `tsv` | | Tab-separated values, the default PostgreSQL COPY format. |

##### compression

`text` the specification of compression type. Can be set to any of the following values:

| **Format** | **Default** | **Description**                                                                                                                                                                      |
| --- | --- | --- |
| `auto` | `true` | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.gz`, it assumes `gzip`. Otherwise, it assumes `none`. |
| `brotli` | | Forces using brotli compression algorithm to compress the blob. Only supported by `parquet` encoder.|
| `gzip` | | Forces using gzip compression algorithm to compress the blob. |
| `lz4` | | Forces using lz4 compression algorithm to compress the blob.  Only supported by `parquet` encoder.|
| `none` | | Forces to not compress the blob. |
| `snappy` | | Forces using snappy compression algorithm to compress the blob.  Only supported by `parquet` encoder.|
| `zstd` | | Forces using zstd compression algorithm to compress the blob.  Only supported by `parquet` encoder.|

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
| `binary` | | Binary PostgreSQL COPY format. |
| `csv` | | Comma-separated values format used by PostgreSQL COPY. |
| `parquet` | | Parquet format. |
| `text` \| `xml` \| `json` | | A file containing a single text value. |
| `tsv` | | Tab-separated values, the default PostgreSQL COPY format. |

##### compression

`text` the specification of compression type. Can be set to any of the following values:

| **Format** | **Default** | **Description**                                                                                                                                                                      |
| --- | --- | --- |
| `auto` | `true` | Infers the value based on the last series of characters assigned to the name of the blob. If the blob name ends with `.gz`, it assumes `gzip`. Otherwise, it assumes `none`. |
| `brotli` | | Forces using brotli compression algorithm to compress the blob. Only supported by `parquet` encoder.|
| `gzip` | | Forces using gzip compression algorithm to compress the blob. |
| `lz4` | | Forces using lz4 compression algorithm to compress the blob.  Only supported by `parquet` encoder.|
| `none` | | Forces to not compress the blob. |
| `snappy` | | Forces using snappy compression algorithm to compress the blob.  Only supported by `parquet` encoder.|
| `zstd` | | Forces using zstd compression algorithm to compress the blob.  Only supported by `parquet` encoder.|

The extension doesn't support any other compression types.

##### options

`jsonb` the settings that define handling of custom headers, custom separators, escape characters, etc. `options` affects the behavior of this function in a way similar to how the options you can pass to the [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command in PostgreSQL affect its behavior.

#### Return type

`VOID`

### azure_storage.options_copy

Function that acts as a utility function, which can be called as a parameter within `blob_get`. It acts as a helper function for [options_parquet](#azure_storageoptions_parquet), [options_csv_get](#azure_storageoptions_csv_get), [options_tsv](#azure_storageoptions_tsv), and [options_binary](#azure_storageoptions_binary).

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

### azure_storage.options_parquet

Function that acts as a utility function, which can be called as a parameter within `blob_get`, and is useful for decoding the content of a parquet file.

```sql
azure_storage.options_parquet();
```

#### Permissions

Any user or role can invoke this function.

#### Arguments

#### Return type

`jsonb`

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

## Related content

- [Azure Storage extension](concepts-storage-extension.md).
- [Configure the Azure Storage extension](how-to-configure-azure-storage-extension.md).
- [Quickstart examples](quickstart-azure-storage-extension.md).
- [Troubleshoot errors](../troubleshoot/troubleshoot-azure-storage-extension.md).
- [Extensions and modules](../extensions/concepts-extensions.md).
