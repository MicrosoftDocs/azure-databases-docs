---
title: Get started with Azure Cosmos DB for Table using .NET
description: Get started developing a .NET application that works with Azure Cosmos DB for Table. This article helps you learn how to set up a project and configure access to an Azure Cosmos DB for Table endpoint.
author: sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: csharp
ms.topic: how-to
ms.date: 07/06/2022
ms.custom: devx-track-csharp, devguide-csharp, cosmos-db-dev-journey, devx-track-dotnet
---

# Get started with Azure Cosmos DB for Table using .NET

This article shows you how to connect to Azure Cosmos DB for Table using the .NET SDK. Once connected, you can perform operations on tables and items.

[Package (NuGet)](https://www.nuget.org/packages/Azure.Data.Tables/) | [Samples](samples-dotnet.md) | [API reference](/dotnet/api/azure.data.tables) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables/Azure.Data.Tables) | [Give Feedback](https://github.com/Azure/azure-sdk-for-net/issues) |

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).
- Azure Cosmos DB for Table account. [Create a API for Table account](how-to-create-account.md).
- [.NET 6.0 or later](https://dotnet.microsoft.com/download)
- [Azure Command-Line Interface (CLI)](/cli/azure/) or [Azure PowerShell](/powershell/azure/)

## Set up your project

Create a new .NET application by using the [``dotnet new``](/dotnet/core/tools/dotnet-new) command with the **console** template.

```dotnetcli
dotnet new console
```

Import the [Azure.Data.Tables](https://www.nuget.org/packages/Azure.Data.Tables) NuGet package using the [``dotnet add package``](/dotnet/core/tools/dotnet-add-package) command.

```dotnetcli
dotnet add package Azure.Data.Tables
```

Build the project with the [``dotnet build``](/dotnet/core/tools/dotnet-build) command.

```dotnetcli
dotnet build
```

## Connect to Azure Cosmos DB for Table

To connect to the API for Table of Azure Cosmos DB, create an instance of the [``TableServiceClient``](/dotnet/api/azure.data.tables.tableserviceclient) class. This class is the starting point to perform all operations against tables.

To connect to your API for NoSQL account using Microsoft Entra, use a security principal. The exact type of principal will depend on where you host your application code. The table below serves as a quick reference guide.

| Where the application runs | Security principal
|--|--|---|
| Local machine (developing and testing) | User identity or service principal |
| Azure | Managed identity |
| Servers or clients outside of Azure | Service principal |

### Import Azure.Identity

The **Azure.Identity** NuGet package contains core authentication functionality that is shared among all Azure SDK libraries.

Import the [Azure.Identity](https://www.nuget.org/packages/Azure.Identity) NuGet package using the ``dotnet add package`` command.

```dotnetcli
dotnet add package Azure.Identity
```

Rebuild the project with the ``dotnet build`` command.

```dotnetcli
dotnet build
```

In your code editor, add using directives for ``Azure.Core`` and ``Azure.Identity`` namespaces.

```csharp
using Azure.Core;
using Azure.Identity;
```

### Create CosmosClient with default credential implementation

If you're testing on a local machine, or your application will run on Azure services with direct support for managed identities, obtain an OAuth token by creating a [``DefaultAzureCredential``](/dotnet/api/azure.identity.defaultazurecredential) instance.

For this example, we saved the instance in a variable of type [``TokenCredential``](/dotnet/api/azure.core.tokencredential) as that's a more generic type that's reusable across SDKs.

```csharp
// Credential class for testing on a local machine or Azure services
TokenCredential credential = new DefaultAzureCredential();
```

Create a new instance of the **CosmosClient** class with the ``COSMOS_ENDPOINT`` environment variable and the **TokenCredential** object as parameters.

```csharp
// New instance of TableServiceClient class using Microsoft Entra
TableServiceClient client = new(
    endpoint: Environment.GetEnvironmentVariable("COSMOS_ENDPOINT")!,
    tokenCredential: credential
);
```

## Build your application

As you build your application, your code will primarily interact with four types of resources:

- The API for Table account, which is the unique top-level namespace for your Azure Cosmos DB data.

- Tables, which contain a set of individual items in your account.

- Items, which represent an individual item in your table.

The following diagram shows the relationship between these resources.

:::image type="complex" source="media/how-to-dotnet-get-started/resource-hierarchy.svg" alt-text="Diagram of the Azure Cosmos DB hierarchy including accounts, tables, and items." border="false":::
    Hierarchical diagram showing an Azure Cosmos DB account at the top. The account has two child table nodes. One of the table nodes includes two child items.
:::image-end:::

Each type of resource is represented by one or more associated .NET classes or interfaces. Here's a list of the most common types:

| Class | Description |
|---|---|
| [``TableServiceClient``](/dotnet/api/azure.data.tables.tableserviceclient) | This client class provides a client-side logical representation for the Azure Cosmos DB service. The client object is used to configure and execute requests against the service. |
| [``TableClient``](/dotnet/api/azure.data.tables.tableclient) | This client class is a reference to a table that may, or may not, exist in the service yet. The table is validated server-side when you attempt to access it or perform an operation against it. |
| [``ITableEntity``](/dotnet/api/azure.data.tables.itableentity) | This interface is the base interface for any items that are created in the table or queried from the table. This interface includes all required properties for items in the API for Table. |
| [``TableEntity``](/dotnet/api/azure.data.tables.tableentity) | This class is a generic implementation of the ``ITableEntity`` interface as a dictionary of key-value pairs. |

The following guides show you how to use each of these classes to build your application.

| Guide | Description |
|--|---|
| [Create a table](how-to-dotnet-create-table.md) | Create tables |
| [Create an item](how-to-dotnet-create-item.md) | Create items |
| [Read an item](how-to-dotnet-read-item.md) | Read items |

## See also

- [Package (NuGet)](https://www.nuget.org/packages/Azure.Data.Tables/)
- [Samples](samples-dotnet.md)
- [API reference](/dotnet/api/azure.data.tables)
- [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/tables/Azure.Data.Tables)
- [Give Feedback](https://github.com/Azure/azure-sdk-for-net/issues)

## Next steps

Now that you've connected to an API for Table account, use the next guide to create and manage tables.

> [!div class="nextstepaction"]
> [Create a table in Azure Cosmos DB for Table using .NET](how-to-dotnet-create-table.md)
