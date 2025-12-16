---
title: Get started with Azure Cosmos DB for NoSQL using JavaScript
description: Get started developing a JavaScript application that works with Azure Cosmos DB for NoSQL. This article helps you learn how to set up a project and configure access to an Azure Cosmos DB for NoSQL endpoint.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: javascript
ms.topic: how-to
ms.date: 10/01/2024
ms.custom: cosmos-db-dev-journey, devx-track-azurepowershell, devx-track-js, devx-track-azurecli
appliesto:
  - ✅ NoSQL
---

# Get started with Azure Cosmos DB for NoSQL using JavaScript

This article shows you how to connect to Azure Cosmos DB for NoSQL using the JavaScript SDK. Once connected, you can perform operations on databases, containers, and items.

[Package (npm)](https://www.npmjs.com/package/@azure/cosmos) | [API reference](/javascript/api/@azure/cosmos) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cosmosdb/cosmos) | [Give Feedback](https://github.com/Azure/azure-sdk-for-js/issues)

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).
- Azure Cosmos DB for NoSQL account. [Create a API for NoSQL account](how-to-create-account.md).
- [Node.js LTS](https://nodejs.org/)
- [Azure Command-Line Interface (CLI)](/cli/azure/) or [Azure PowerShell](/powershell/azure/)

## Set up your local project

1. Create a new directory for your JavaScript project in a bash shell.

    ```bash
    mkdir cosmos-db-nosql-javascript-samples && cd ./cosmos-db-nosql-javascript-samples
    ```

1. Create a new JavaScript application by using the [``npm init``](https://docs.npmjs.com/cli/v6/commands/npm-init) command with the **console** template.

    ```bash
    npm init -y
    ```

1. Install the required dependency for the Azure Cosmos DB for NoSQL JavaScript SDK.

    ```bash
    npm install @azure/cosmos
    ```

## Connect to Azure Cosmos DB for NoSQL

To connect to the API for NoSQL of Azure Cosmos DB, create an instance of the [`CosmosClient`](/javascript/api/@azure/cosmos/cosmosclient) class. This class is the starting point to perform all operations against databases.

To connect to your API for NoSQL account using the Microsoft Entra, use a security principal. The exact type of principal depends on where you host your application code. The table below serves as a quick reference guide.

| Where the application runs | Security principal
|--|--|---|
| Local machine (developing and testing) | User identity or service principal |
| Azure | Managed identity |
| Servers or clients outside of Azure | Service principal |

### Import @azure/identity

The **@azure/identity** npm package contains core authentication functionality that is shared among all Azure SDK libraries.

1. Import the [@azure/identity](https://www.npmjs.com/package/@azure/identity) npm package using the ``npm install`` command.

    ```bash
    npm install @azure/identity
    ```

1. In your code editor, add the dependencies.

    ```javascript
    const { DefaultAzureCredential } = require("@azure/identity");
    ```

### Create CosmosClient with default credential implementation

If you're testing on a local machine, or your application will run on Azure services with direct support for managed identities, obtain an OAuth token by creating a [``DefaultAzureCredential``](/javascript/api/@azure/identity/defaultazurecredential) instance. Then create a new instance of the **CosmosClient** class with the ``COSMOS_ENDPOINT`` environment variable and the **TokenCredential** object as parameters.

```javascript
const { CosmosClient } = require("@azure/cosmos");
const { DefaultAzureCredential } = require("@azure/identity");

const credential = new DefaultAzureCredential();

const cosmosClient = new CosmosClient({ 
    endpoint, 
    aadCredentials: credential
});
```

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

Each type of resource is represented by one or more associated classes. Here's a list of the most common classes:

| Class | Description |
|---|---|
| [``CosmosClient``](/javascript/api/@azure/cosmos/cosmosclient) | This class provides a client-side logical representation for the Azure Cosmos DB service. The client object is used to configure and execute requests against the service. |
| [``Database``](/javascript/api/@azure/cosmos/database) | This class is a reference to a database that may, or may not, exist in the service yet. The database is validated server-side when you attempt to access it or perform an operation against it. |
| [``Container``](/javascript/api/@azure/cosmos/container) | This class is a reference to a container that also may not exist in the service yet. The container is validated server-side when you attempt to work with it. |

The following guides show you how to use each of these classes to build your application.

| Guide | Description |
|--|---|
| [Create a database](how-to-javascript-create-database.md) | Create databases |
| [Create a container](how-to-javascript-create-container.md) | Create containers |
| [Create and read an item](how-to-javascript-create-item.md) | Point read a specific item |
| [Query items](how-to-javascript-query-items.md) | Query multiple items |

## See also

- [npm package](https://www.npmjs.com/package/@azure/cosmos)
- [API reference](/javascript/api/@azure/cosmos/)
- [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cosmosdb/cosmos)
- [Give Feedback](https://github.com/Azure/azure-sdk-for-js/issues)

## Next steps

> [!div class="nextstepaction"]
> [Create a database in Azure Cosmos DB for NoSQL using JavaScript](how-to-javascript-create-database.md)
