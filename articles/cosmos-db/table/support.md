---
title: Azure Table Storage Support
titleSuffix: Azure Cosmos DB for Table
description: Discover how Azure Cosmos DB for Table and Azure Table Storage share the same data model and operations. Learn how to integrate both for scalable table storage.
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
author: seesharprun
ms.topic: how-to
ms.devlang: csharp
ms.date: 08/21/2025
appliesto:
  - ✅ Table
---

# Use Azure Cosmos DB for Table and Azure Table Storage

Azure Cosmos DB for Table and Azure Table Storage share the same table data model and operations, making it easy to build scalable applications. This article explains how to use both services together for efficient table storage management.

> [!NOTE]
> The *serverless capacity mode* is now available on Azure Cosmos DB API for Table. For more information, see [Azure Cosmos DB serverless](../serverless.md).

[!INCLUDE [storage-table-cosmos-comparison](../includes/storage-table-cosmos-comparison.md)]

## Azure SDKs

### Current release

The following SDK packages work with both the Azure Cosmos DB for Table and Table Storage.

| Language | Package | Source Code |
| --- | --- | --- |
| **.NET** | [NuGet \| Azure.Data.Tables](https://www.nuget.org/packages/Azure.Data.Tables/) | [azure-sdk-for-net/sdk/tables/Azure.Data.Tables](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables/Azure.Data.Tables) |
| **Python** | [PyPI \| azure-data-tables](https://pypi.org/project/azure-data-tables/) | [azure-sdk-for-python/sdk/tables/azure-data-tables](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/tables/azure-data-tables) |
| **JavaScript/TypeScript** | [npm \| @azure/data-tables](https://www.npmjs.com/package/@azure/data-tables) | [azure-sdk-for-js/sdk/tables/data-tables](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/tables/data-tables) |
| **Java** | [Maven \| azure-data-tables](https://mvnrepository.com/artifact/com.azure/azure-data-tables) | [azure-sdk-for-java/sdk/tables/azure-data-tables](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/tables/azure-data-tables) |
| **Go** | [pkg.go.dev \| aztables](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/data/aztables) | [azure-sdk-for-go/sdk/data/aztables](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/data/aztables) |
| **C++** | [vcpkg \| azure-data-tables-cpp](https://vcpkg.io/en/package/azure-data-tables-cpp) | [azure-sdk-for-cpp/sdk/tables/azure-data-tables](https://github.com/Azure/azure-sdk-for-cpp/tree/main/sdk/tables/azure-data-tables) |

### Prior releases

The following SDK packages work only with Azure Cosmos DB for Table.

- **.NET**. [Azure.Data.Tables](https://www.nuget.org/packages/Azure.Data.Tables/) available on NuGet. The Azure Tables client library can seamlessly target either Table Storage or Azure Cosmos DB for Table service endpoints with no code changes.

- **Python**. [azure-cosmosdb-table](https://pypi.org/project/azure-cosmosdb-table/) available from PyPi. This SDK connects with both Table Storage and Azure Cosmos DB for Table.

- **JavaScript/TypeScript**. [azure-storage](https://www.npmjs.com/package/azure-storage) package available on npm.js. This Azure Storage SDK has the ability to connect to Azure Cosmos DB accounts using the API for Table.

- **Java**. [Microsoft Azure Storage Client SDK for Java](https://mvnrepository.com/artifact/com.microsoft.azure/azure-storage) on Maven. This Azure Storage SDK has the ability to connect to Azure Cosmos DB accounts using the API for Table.

- **C++**. [Azure Storage Client Library for C++](https://github.com/Azure/azure-storage-cpp/). This library enables you to build applications against Azure Storage.

- **Ruby**. [Azure Storage Table Client Library for Ruby](https://github.com/azure/azure-storage-ruby/tree/master/table). This project provides a Ruby package that makes it easy to access Azure storage Table services.

- **PHP**. [Azure Storage Table PHP Client Library](https://github.com/Azure/azure-storage-php/tree/master/azure-storage-table). This project provides a PHP client library that makes it easy to access Azure storage Table services.

- **PowerShell**. [AzureRmStorageTable PowerShell module](https://www.powershellgallery.com/packages/AzureRmStorageTable). This PowerShell module has cmdlets to work with storage Tables.

## Next steps

- [Create a container in Azure Cosmos DB for Table](how-to-create-container.md)
