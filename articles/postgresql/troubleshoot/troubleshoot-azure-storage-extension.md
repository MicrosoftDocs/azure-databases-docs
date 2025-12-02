---
title: Troubleshoot the Azure Storage Extension
description: Learn how to troubleshoot the Azure Storage extension in Azure Database for PostgreSQL flexible server to import and export data.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 11/03/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: reference
ms.custom:
- ignite-2024
- sfi-image-nochange
---

# Troubleshoot the Azure Storage extension in Azure Database for PostgreSQL 

Following is the list of errors that the Azure Storage extension can return. It also explains the reasons why or the circumstances in which they can be raised. 

### ERROR: azure_storage: Permission is not sufficient to perform requested operation

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) and the System Assigned Managed Identity isn't granted the adequate data plane roles or permissions (typically a minimum of **Storage Blob Data Contributor** for azure_storage.blob_put, and a minimum of **Storage Blob Data Reader** for the other two functions).

It might be the case that you already granted the minimum required permissions, but they aren't yet in effect. It can take a few minutes until those permissions propagate.

### ERROR: azure_storage: missing storage credentials

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) and the credentials with which you want the extension to authenticate with the storage account aren't registered using `azure_storage.account_add`.

### ERROR: azure_storage: internal error while connecting

When the instance of flexible server can't reach the target storage account. This situation can happen in the following cases:
- The storage account doesn't exist.
- Networking configuration doesn't allow traffic originated from the instance of flexible server to reach the storage account. For example, when the instance of flexible server is deployed with public access networking, and the storage account is only accessible via private endpoints.

### ERROR:  azure_storage: current user <user_or_role> isn't allowed to use storage account <account_name>

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) with a user or role that isn't member of `azure_storage_admin` and isn't granted permissions, using `azure_storage.account_user_add`, to use the referred storage account.

### ERROR:  azure_storage: Query is not supported while copying data to blob storage

When executing a COPY TO statement for which the source is a query. Azure Storage extension doesn't support this syntax. It only supports the syntax on which the source of the COPY TO be a relation. As a workaround, you can implement a view with the query as its definition, and rewrite the COPY TO statement to be sourced on the view.

### ERROR:  azure_storage: could not infer file encoding from extension: '<extension>', use a supported extension [csv, csv.gz, tsv, tsv.gz, json, json.gz, xml, xml.gz, txt, txt.gz, parquet], or specify the decoder argument if you are using blob_get or format if using COPY FROM/TO 

When <extension> doesn't correspond to one of the extensions from which Azure Storage extension supports inferring the encoder and compression algorithm (for `blob_put` and `COPY TO`) or decoder and decompression algorithm (for `blob_get` and `COPY FROM`) that must be used. Either specify one of the supported values for automatic inference, or don't use `auto` but force specific type of encoder + compression or decoder + decompression.

### ERROR:  azure_storage: can only use text encoder with a single column

When the tuples passed to `blob_put` consist of more than one column and the encoder is inferred as `text`, or manually set to `text`.

### ERROR:  azure_storage: can only use text decoder with a single column

When the tuples read from the blob by `blob_get` consist of more than one column and the encoder is inferred as `text`, or is manually set to `text`.

### ERROR:  azure_storage: container with the given name does not exist

The name of the container passed through the `container_name` parameter of the `blob_get` function doesn't exist in the referred storage account.

### ERROR:  azure_storage: blob with the given name does not exist

The name of the blob passed through the `path` parameter of the `blob_get` function doesn't exist in the referred container in the storage account.

## Related content

- [Reference](../extension-module/reference-azure-storage-extension.md).
- [Azure Storage extension](../extension-module/concepts-storage-extension.md).
- [Configure the Azure Storage extension](../extension-module/how-to-configure-azure-storage-extension.md).
- [Quickstart examples](../extension-module/quickstart-azure-storage-extension.md).
- [Extensions and modules](../extensions/concepts-extensions.md).
