---
title: Get Started Using .NET
description: Get started developing a .NET application that works with Azure Cosmos DB for NoSQL. This article helps you learn how to set up a project and configure access to an Azure Cosmos DB for NoSQL endpoint.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: csharp
ms.topic: how-to
ms.date: 02/09/2026
ms.custom: devx-track-csharp, devguide-csharp, cosmos-db-dev-journey, devx-track-azurepowershell, devx-track-dotnet, devx-track-azurecli
appliesto:
  - ✅ NoSQL
---

# Get started with Azure Cosmos DB for NoSQL using .NET

This article shows you how to connect to Azure Cosmos DB for NoSQL using the .NET SDK. Once connected, you can perform operations on databases, containers, and items.

[Package (NuGet)](https://www.nuget.org/packages/Microsoft.Azure.Cosmos) | [API reference](/dotnet/api/microsoft.azure.cosmos) | [Library source code](https://github.com/Azure/azure-cosmos-dotnet-v3) | [Give Feedback](https://github.com/Azure/azure-cosmos-dotnet-v3/issues)

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).
- Azure Cosmos DB for NoSQL account. [Create a API for NoSQL account](how-to-create-account.md).
- [.NET 6.0 or later](https://dotnet.microsoft.com/download)
- [Azure Command-Line Interface (CLI)](/cli/azure/) or [Azure PowerShell](/powershell/azure/)

## Set up your project

Create a new .NET application by using the [``dotnet new``](/dotnet/core/tools/dotnet-new) command with the **console** template.

```dotnetcli
dotnet new console
```

Import the [Microsoft.Azure.Cosmos](https://www.nuget.org/packages/Microsoft.Azure.Cosmos) NuGet package using the [``dotnet add package``](/dotnet/core/tools/dotnet-add-package) command.

```dotnetcli
dotnet add package Microsoft.Azure.Cosmos
```

Also add the [Newtonsoft.Json](https://www.nuget.org/packages/Newtonsoft.Json) NuGet package, which is required by the Microsoft.Azure.Cosmos package.

```dotnetcli
dotnet add package Newtonsoft.Json
```

Build the project with the [``dotnet build``](/dotnet/core/tools/dotnet-build) command.

```dotnetcli
dotnet build
```

## Connect to Azure Cosmos DB for NoSQL

To connect to the API for NoSQL of Azure Cosmos DB, create an instance of the [`CosmosClient`](/dotnet/api/microsoft.azure.cosmos.cosmosclient) class. This class is the starting point to perform all operations against databases.

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

:::code language="csharp" source="~/cosmos-db-nosql-dotnet-samples/103-client-default-credential/Program.cs" id="using_identity_directives":::

### Create CosmosClient with default credential implementation

If you're testing on a local machine, or your application will run on Azure services with direct support for managed identities, obtain an OAuth token by creating a [``DefaultAzureCredential``](/dotnet/api/azure.identity.defaultazurecredential) instance.

For this example, we saved the instance in a variable of type [``TokenCredential``](/dotnet/api/azure.core.tokencredential) as that's a more generic type that's reusable across SDKs.

:::code language="csharp" source="~/cosmos-db-nosql-dotnet-samples/103-client-default-credential/Program.cs" id="credential":::

Create a new instance of the **CosmosClient** class with the ``COSMOS_ENDPOINT`` environment variable and the **TokenCredential** object as parameters.

:::code language="csharp" source="~/cosmos-db-nosql-dotnet-samples/103-client-default-credential/Program.cs" id="default_credential" highlight="4":::

## Build your application

As you build your application, your code will primarily interact with four types of resources:

- The API for NoSQL account, which is the unique top-level namespace for your Azure Cosmos DB data.

- Databases, which organize the containers in your account.

- Containers, which contain a set of individual items in your database.

- Items, which represent a JSON document in your container.

The following diagram shows the relationship between these resources.

:::image type="complex" source="media/how-to-dotnet-get-started/resource-hierarchy.svg" alt-text="Diagram of the Azure Cosmos DB hierarchy including accounts, databases, containers, and items." border="false":::
    Hierarchical diagram showing an Azure Cosmos DB account at the top. The account has two child database nodes. One of the database nodes includes two child container nodes. The other database node includes a single child container node. That single container node has three child item nodes.
:::image-end:::

Each type of resource is represented by one or more associated .NET classes. Here's a list of the most common classes:

| Class | Description |
|---|---|
| [``CosmosClient``](/dotnet/api/microsoft.azure.cosmos.cosmosclient) | This class provides a client-side logical representation for the Azure Cosmos DB service. The client object is used to configure and execute requests against the service. |
| [``Database``](/dotnet/api/microsoft.azure.cosmos.database) | This class is a reference to a database that may, or may not, exist in the service yet. The database is validated server-side when you attempt to access it or perform an operation against it. |
| [``Container``](/dotnet/api/microsoft.azure.cosmos.container) | This class is a reference to a container that also may not exist in the service yet. The container is validated server-side when you attempt to work with it. |

The following guides show you how to use each of these classes to build your application.

| Guide | Description |
|--|---|
| [Create a database](how-to-dotnet-create-database.md) | Create databases |
| [Create a container](how-to-dotnet-create-container.md) | Create containers |
| [Read an item](how-to-dotnet-read-item.md) | Point read a specific item |
| [Query items](how-to-dotnet-query-items.md) | Query multiple items |

## See also

- [Package (NuGet)](https://www.nuget.org/packages/Microsoft.Azure.Cosmos)
- [API reference](/dotnet/api/microsoft.azure.cosmos)
- [Library source code](https://github.com/Azure/azure-cosmos-dotnet-v3)
- [Give Feedback](https://github.com/Azure/azure-cosmos-dotnet-v3/issues)

## Next steps

> [!div class="nextstepaction"]
> [Create a database in Azure Cosmos DB for NoSQL using .NET](how-to-dotnet-create-database.md)
