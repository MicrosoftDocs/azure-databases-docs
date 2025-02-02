---
title: Import and Export Data Using azure_storage Extension in Azure Database for PostgreSQL - Flexible Server
description: Learn about the azure_storage extension in Azure Database for PostgreSQL - Flexible Server
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 11/18/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
ms.custom:
  - ignite-2023
---

# Import and export data using Azure Storage in Azure Database for PostgreSQL - Flexible Server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

You can import data that is being stored as blobs in Azure Storage accounts to insert it into tables in PostgreSQL. Or you can query, filter, transform or aggregate it, using the power of SQL language.

You can also export data stored in PostgreSQL tables onto blobs stored in any of your Azure Storage accounts.

To do so, you need to install the `azure_storage` extension in your instance of Azure Database for PostgreSQL Flexible Server, and use the functionality it incorporates.

## Azure Blob Storage

Azure Blob Storage is an object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Unstructured data is data that doesn't adhere to a particular data model or definition, such as text or binary data.

Blob Storage offers a hierarchy of three types of resources:

- The [storage account](/azure/storage/blobs/storage-blobs-introduction#storage-accounts) is an administrative entity that holds services for items like blobs, files, queues, tables, or disks.

  When you create a storage account in Azure, you get a unique namespace for your storage resources. That unique namespace forms part of the URL. The storage account name should be unique across all existing storage account names in Azure.

- A [container](/azure/storage/blobs/storage-blobs-introduction#containers) is inside a storage account. A container is like a folder where blobs are stored.

  You can define security policies and assign policies to the container. Those policies cascade to all the blobs in the container.

  A storage account can contain an unlimited number of containers. Each container can contain an unlimited number of blobs, up to the maximum storage account size of 500 TB.

  After you place a blob into a container that's inside a storage account, you can refer to the blob by using a URL in this format: `protocol://<storage_account_name>/blob.core.windows.net/<container_name>/<blob_name>`.

- A [blob](/azure/storage/blobs/storage-blobs-introduction#blobs) is a piece of data that resides in the container.

The following diagram shows the relationship between these resources.

:::image type="content" source="media/concepts-storage-extension/blob-1.png" alt-text="Diagram that shows an example of storage resources.":::

## Key benefits of storing data as blobs in Azure Blob Storage

Azure Blob Storage can provide following benefits:

- It's a scalable and cost-effective cloud storage solution. You can use it to store data of any size and scale up or down based on your needs.
- It provides layers of security to help protect your data, such as encryption at rest and in transit.
- It communicates with other Azure services and partner applications. It's a versatile solution for a wide range of use cases, such as backup and disaster recovery, archiving, and data analysis.
- It's a cost-effective solution for managing and storing massive amounts of data in the cloud, whether the organization is a small business or a large enterprise. You pay only for the storage that you need.

## Related content

- [Import and export data using azure_storage extension in Azure Database for PostgreSQL - Flexible Server](how-to-use-pg-azure-storage.md).
