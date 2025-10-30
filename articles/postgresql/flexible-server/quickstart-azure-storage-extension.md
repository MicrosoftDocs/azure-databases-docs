---
title: Quickstart Examples for Azure Storage Extension
description: Learn how to use the Azure Storage extension in Azure Database for PostgreSQL to import and export data.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 06/26/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: reference
ms.custom:
- ignite-2024
- sfi-image-nochange
---

# Quickstart examples for the Azure Storage extension in Azure Database for PostgreSQL 

Following is a list of examples to help you learn how to use the Azure Storage extension.

## Create an Azure Storage account and populate it with data

1. Create an Azure Storage account.
   To create an Azure Storage account, if you don't have one already, customize the values of `<resource_group>`, `<location>`, `<account_name>`, and `<container_name>`, and run the following Azure CLI command:
   ```azurecli-interactive
   random_suffix=$(tr -dc 'a-z0-9' </dev/urandom | head -c8)
   resource_group="resource-group-$random_suffix"
   location="eastus2"
   storage_account="storageaccount$random_suffix"
   blob_container="container-$random_suffix"
   az group create --name $resource_group --location $location
   az storage account create --resource-group $resource_group --name $storage_account --location $location --sku Standard_LRS --kind BlobStorage --public-network-access enabled --access-tier hot
   echo "Take note of the storage account name, which you'll have to replace in subsequent examples, whenever you find a reference to <account_name>:"
   echo $storage_account
   echo "Take note of the container name, which you'll have to replace in subsequent examples, whenever you find a reference to <container_name>:"
   echo $blob_container
   ```
1. Create a blob container.
   To create the blob container, run the following Azure CLI:
   ```azurecli-interactive
   az storage container create --account-name $storage_account --name $blob_container -o tsv
   ```
1. Fetch one of the two access keys assigned to the storage account. Make sure you copy the value of your access_key as you need to pass it as an argument to [azure_storage.account_add](./reference-azure-storage-extension.md#azure_storageaccount_add) in a subsequent step.
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
> You can list containers or the blobs stored in them for a specific storage account, but only if your PostgreSQL user or role is granted permission on the reference to that storage account by using [azure_storage.account_user_add](./reference-azure-storage-extension.md#azure_storageaccount_user_add). Members of the `azure_storage_admin` role are granted this privilege over all Azure Storage accounts that have been added using [azure_storage.account_add](./reference-azure-storage-extension.md#azure_storageaccount_add). By default, only members of `azure_pg_admin` are granted the `azure_storage_admin` role.

## Create a table in which data is loaded

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

## Prepare the extension for usage

Before proceeding, make sure that you:
1. [Load the extension's library](how-to-configure-azure-storage-extension.md#load-the-extensions-library)
1. [Allowlist the extension](how-to-configure-azure-storage-extension.md#allowlist-the-extension)
1. [Create the extension](how-to-configure-azure-storage-extension.md#create-the-extension)

## Add access key of storage account

This example illustrates how to add a reference to a storage account, together with the access key of that storage account which is required to access its content via the functionality provided by the `azure_storage` extension in your instance of Azure Database for PostgreSQL flexible server.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

Similarly, `<access_key>` must be set to the value you fetched from your storage account.

```sql
SELECT azure_storage.account_add('<account_name>', '<access_key>');
```
> [!TIP]  
> If you want to retrieve the storage account name and one of its access keys from the Azure portal, search for your storage account, in the resource menu select **Access keys**, copy the **Storage account name** and copy the **Key** from **key1** section (you have to select **Show** next to the key first).

## Grant access to a user or role on the Azure Blob storage reference

This example illustrates how to grant access to a user or role named `<regular_user>`, so that such PostgreSQL user can use the `azure_storage` extension to access the blobs stored in containers hosted by the referred Azure storage account.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<regular_user>` must be set to the name of an existing user or role.

```sql
SELECT * FROM azure_storage.account_user_add('<account_name>', '<regular_user>');
```

## List all blobs in a container

This example illustrates how to list all existing blobs inside container `<container_name>` of storage account `<account_name>`.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT * FROM azure_storage.blob_list('<account_name>','<container_name>');
```

## List blobs with a specific name prefix

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

## Import data using a COPY FROM statement

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

3. Execute the following `SELECT` statement to confirm that the data is loaded into the table.

    ```sql
    SELECT *
    FROM events
    LIMIT 100;
    ```

## Export data using a COPY TO statement

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

2. Load data into the table. Either run INSERT statements to populate it with several synthetic rows, or use the [Import data using a COPY FROM statement](#import-data-using-a-copy-from-statement) example to populate it with the contents of the sample data set.

3. Use a `COPY` statement to copy data into the target table. Specify that the first row contains column headers.

   ```sql
   COPY events
   TO 'https://<account_name>.blob.core.windows.net/<container_name>/events_exported.csv'
   WITH (FORMAT 'csv', header);
   ```

4. Execute the following `SELECT` statement to confirm that the blob exists in the storage account.

    ```sql
    SELECT * FROM azure_storage.blob_list('<account_name>','<container_name>') WHERE path = 'events_exported.csv';
    ```
    
## Read content from a blob

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

Alternatively, you can explicitly define the schema of the result using the `AS` clause after the [blob_get](./reference-azure-storage-extension.md#azure_storageblob_get) function.

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

## Read, filter, and modify content read from a blob

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

## Read content from file with custom options (headers, column delimiters, escape characters)

This example illustrates how you can use custom separators and escape characters, by passing the result of [options_copy](./reference-azure-storage-extension.md#azure_storageoptions_copy) to the `options` argument.

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

## Use the decoder option

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

## Use compression with decoder option

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

## Compute aggregations over the content of a blob

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


## Write content to a blob

The `blob_put` function composes the contents of one specific blob (`eventscopy.csv` in this case), and uploads it to the referred container `<container_name>` of the `<account_name>` storage. This example uses `blob_get` to construct a set of five rows, which are then passed to the `blob_put` aggregate function which uploads them as a blob named `eventscopy.csv`.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<container_name>` must be set to the name of your blob container. If you used the previous scripts, this value should match whatever value you set to the blob_container environment variable in those scripts.

```sql
SELECT azure_storage.blob_put
        ('<account_name>'
        ,'<container_name>'
        ,'eventscopy.csv'
        , top_5_events)
FROM (SELECT * FROM events) LIMIT 5) AS top_5_events;
```

## List all the references to Azure storage accounts

This example illustrates how to find out which Azure storage accounts the `azure_storage` extension can reference in this database, together with the type of authentication that is used to access each storage account, and which users or roles are granted permission, via the [azure_storage.account_user_add](./reference-azure-storage-extension.md#azure_storageaccount_user_add) function, to access that Azure storage account through the functionality provided by the extension.

```sql
SELECT * FROM azure_storage.account_list();
```

## Revoke access from a user or role on the Azure Blob storage reference

This example illustrates how to revoke access from a user or role named `<regular_user>`, so that such PostgreSQL user can't use the `azure_storage` extension to access the blobs stored in containers hosted by the referred Azure storage account. 

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

`<regular_user>` must be set to the name of an existing user or role.

```sql
SELECT * FROM azure_storage.account_user_remove('<account_name>', '<regular_user>');
```

## Remove reference to storage account

This example illustrates how to remove any reference to a storage account, so that no user in the current database can use the `azure_storage` extension functionality to access that storage account.

`<account_name>` must be set to the name of your storage account. If you used the previous scripts, this value should match whatever value you set to the storage_account environment variable in those scripts.

```sql
SELECT azure_storage.account_remove('<account_name>');
```

## Related content

- [Troubleshoot errors](troubleshoot-azure-storage-extension.md).
- [Reference](reference-azure-storage-extension.md).
- [Azure Storage extension](concepts-storage-extension.md).
- [Configure the Azure Storage extension](how-to-configure-azure-storage-extension.md).
- [Extensions and modules](../extensions/concepts-extensions.md).
