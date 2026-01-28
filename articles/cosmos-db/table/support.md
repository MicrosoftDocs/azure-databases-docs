---
title: Azure Table Storage Support
titleSuffix: Azure Cosmos DB for Table
description: Discover how Azure Cosmos DB for Table and Azure Table Storage share the same data model and operations. Learn how to integrate both for scalable table storage.
ms.author: sidandrews
author: seesharprun
ms.reviewer: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: how-to
ms.devlang: csharp
ms.date: 08/20/2025
ai-usage: ai-assisted
---

# Use Azure Cosmos DB for Table and Azure Table Storage

Azure Cosmos DB for Table and Azure Table Storage use the same table data model and operations, so you can build scalable applications easily. This article shows how to use both services together for efficient table storage management.

> [!NOTE]
> The *serverless capacity mode* is available on Azure Cosmos DB API for Table. For more information, see [Azure Cosmos DB serverless](../serverless.md).

[!INCLUDE [storage-table-cosmos-comparison](../includes/storage-table-cosmos-comparison.md)]

## Azure SDKs

The Azure software development kits (SDKs) provide libraries for multiple programming languages, enabling developers to interact with Azure Cosmos DB for Table and Azure Table Storage seamlessly.

### Current release

These SDK packages work with both Azure Cosmos DB for Table and Table Storage.

| | Package | Source Code |
| --- | --- | --- |
| **.NET** | [NuGet - `Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) | [`azure-sdk-for-net/sdk/tables/Azure.Data.Tables`](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables/Azure.Data.Tables) |
| **Python** | [PyPI - `azure-data-tables`](https://pypi.org/project/azure-data-tables/) | [`azure-sdk-for-python/sdk/tables/azure-data-tables`](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/tables/azure-data-tables) |
| **JavaScript/TypeScript** | [npm - `@azure/data-tables`](https://www.npmjs.com/package/@azure/data-tables) | [`azure-sdk-for-js/sdk/tables/data-tables`](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/tables/data-tables) |
| **Java** | [Maven - `azure-data-tables`](https://mvnrepository.com/artifact/com.azure/azure-data-tables) | [`azure-sdk-for-java/sdk/tables/azure-data-tables`](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/tables/azure-data-tables) |
| **Go** | [pkg.go.dev - `aztables`](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables) | [`azure-sdk-for-go/sdk/data/aztables`](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/data/aztables) |
| **C++** | [vcpkg - `azure-data-tables-cpp`](https://vcpkg.io/en/package/azure-data-tables-cpp) | [`azure-sdk-for-cpp/sdk/tables/azure-data-tables`](https://github.com/Azure/azure-sdk-for-cpp/tree/main/sdk/tables/azure-data-tables) |

### Prior releases

These SDK packages work only with Azure Cosmos DB for Table.

- **.NET**. [`Azure.Data.Tables`](https://www.nuget.org/packages/Azure.Data.Tables/) is available on NuGet. The Azure Tables client library targets either Table Storage or Azure Cosmos DB for Table service endpoints with no code changes.

- **Python**. [`azure-cosmosdb-table`](https://pypi.org/project/azure-cosmosdb-table/) is available from PyPi. This SDK connects with both Table Storage and Azure Cosmos DB for Table.

- **JavaScript/TypeScript**. [`azure-storage`](https://www.npmjs.com/package/azure-storage) is available on npm.js. This Azure Storage SDK connects to Azure Cosmos DB accounts using the API for Table.

- **Java**. [Microsoft Azure Storage Client SDK for Java](https://mvnrepository.com/artifact/com.microsoft.azure/azure-storage) is available on Maven. This Azure Storage SDK connects to Azure Cosmos DB accounts using the API for Table.

- **C++**. [Azure Storage Client Library for C++](https://github.com/Azure/azure-storage-cpp/) lets you build applications for Azure Storage.

- **Ruby**. [Azure Storage Table Client Library for Ruby](https://github.com/azure/azure-storage-ruby/tree/master/table) provides a Ruby package to access Azure storage Table services.

- **PHP**. [Azure Storage Table PHP Client Library](https://github.com/Azure/azure-storage-php/tree/master/azure-storage-table) provides a PHP client library to access Azure storage Table services.

- **PowerShell**. [`AzureRmStorageTable` PowerShell module](https://www.powershellgallery.com/packages/AzureRmStorageTable) has cmdlets to work with storage Tables.
