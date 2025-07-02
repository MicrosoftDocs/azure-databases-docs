---
title: Troubleshoot the Azure Storage extension in Azure Database for PostgreSQL flexible server
description: Learn how to troubleshoot the Azure Storage extension in Azure Database for PostgreSQL flexible server to import and export data
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

# Troubleshoot the Azure Storage extension in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Following is the list of errors that the Azure Storage extension can return, and the reasons why, or the circumstances in which, they can be seen. 

### ERROR: azure_storage: Permission is no sufficient to perform requested operation

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) and the System Assigned Managed Identity isn't granted the adequate data plane roles or permissions (typically a minimum of **Storage Blob Data Contributor** for azure_storage.blob_put, and a minimum of **Storage Blob Data Reader** for the other two functions).

It may also be the case that you have already granted the minimum required permissions but they aren't yet in effect. It can take a few minutes until those permissions get propagated.

### ERROR: azure_storage: missing storage credentials

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) and the credentials with which you want the extension to authenticate with the storage account aren't registered using `azure_storage.account_add`.

### ERROR: azure_storage: internal error while connecting

When the instance of flexible server can't reach the target storage account. That could happen in the following cases:
- The storage account doesn't exist.
- Networking configuration doesn't allow traffic originated from the instance of flexible server to reach the storage account. For example, when the instance of flexible server is deployed with public access networking, and the storage account is only accessible via private endpoints.

When the System Assigned Managed Identity isn't enabled in the instance of flexible server.

### ERROR: azure_storage: storage credentials invalid format

When the System Assigned Managed Identity is enabled on the instance of flexible server, but the server hasn't been restarted after enabling it.

### ERROR:  azure_storage: current user <user_or_role> isn't allowed to use storage account <account_name>

When executing any of the functions that interact with Azure Storage (`azure_storage.blob_list`, `azure_storage.blob_get` or `azure_storage.blob_put`) with a user or role that isn't member of `azure_storage_admin` and isn't granted permissions, using `azure_storage.account_user_add`, to use the referred storage account.

## Related content

- [Import and export data using Azure Storage in Azure Database for PostgreSQL flexible server](concepts-storage-extension.md).
- [Extensions and modules](../extensions/concepts-extensions.md).
