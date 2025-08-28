---
title: Get started with Azure Cosmos DB for NoSQL using Python
description: Get started developing a Python application that works with Azure Cosmos DB for NoSQL. This article helps you learn how to set up a project and configure access to an Azure Cosmos DB for NoSQL endpoint.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: python
ms.topic: how-to
ms.date: 08/28/2025
ms.custom: devx-track-python, devguide-python, cosmos-db-dev-journey, devx-track-azurepowershell, devx-track-azurecli
---

# Get started with Azure Cosmos DB for NoSQL using Python

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

This article shows you how to connect to Azure Cosmos DB for NoSQL using the Python SDK. Once connected, you can perform operations on databases, containers, and items.

[Package (PyPi)](https://pypi.org/project/azure-cosmos/) | [API reference](/python/api/azure-cosmos/azure.cosmos) | [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos) | [Give Feedback](https://github.com/Azure/azure-sdk-for-python/issues)

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).
- Azure Cosmos DB for NoSQL account. [Create a API for NoSQL account](how-to-create-account.md).
- [Python 3.7 or later](https://www.python.org/downloads/)
- [Azure Command-Line Interface (CLI)](/cli/azure/) or [Azure PowerShell](/powershell/azure/)

## Set up your project

Create an environment that you can run Python code in.

### [Virtual environment](#tab/env-virtual)

With a [virtual environment](/azure/developer/python/configure-local-development-environment#configure-python-virtual-environment), you can install Python packages in an isolated environment without affecting the rest of your system.

Install the Azure Cosmos DB for NoSQL Python SDK in the virtual environment.

```bash
pip install azure-cosmos
```

### [Dev container](#tab/env-container)

A [dev container](https://containers.dev/) is a pre-configured environment that you can use to run Python code.

To run a dev container, you can use:

- **Visual Studio Code**: Clone this repo to your local machine and open the folder using the [Dev containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

- **GitHub Codespaces**: Open this repo in the browser with a [GitHub codespace](https://docs.github.com/en/codespaces/overview).

Install the Azure Cosmos DB for NoSQL Python SDK in the dev container.

```bash
pip install azure-cosmos
```

---

### Create the Python application

In your environment, create a new *app.py* file and add the following code to it:

:::code language="python" source="~/cosmos-db-nosql-python-samples/003-how-to/app.py" id="imports":::

The preceding code imports modules that you'll use in the rest of the article.

## Connect to Azure Cosmos DB for NoSQL

To connect to the API for NoSQL of Azure Cosmos DB, create an instance of the [`CosmosClient`](/python/api/azure-cosmos/azure.cosmos.cosmosclient) class. This class is the starting point to perform all operations against databases.

To connect to your API for NoSQL account using Microsoft Entra, use a security principal. The exact type of principal will depend on where you host your application code. The table below serves as a quick reference guide.

| Where the application runs | Security principal
|--|--|---|
| Local machine (developing and testing) | User identity or service principal |
| Azure | Managed identity |
| Servers or clients outside of Azure | Service principal |

### Import Azure.Identity

The **azure-identity** package contains core authentication functionality that is shared among all Azure SDK libraries.

Import the [azure-identity](https://pypi.org/project/azure-identity/) package into your environment.

```bash
pip install azure-identity
```

### Create CosmosClient with default credential implementation

If you're testing on a local machine, or your application will run on Azure services with direct support for managed identities, obtain an OAuth token by creating a [``DefaultAzureCredential``](/python/api/azure-identity/azure.identity.defaultazurecredential) instance.

In your *app.py*:

- Get the endpoint to connect to your account and set that as the environment variable `COSMOS_ENDPOINT`.

- Import the [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential) and create an instance of it.

- Create a new instance of the **CosmosClient** class with the **ENDPOINT** and **credential** as parameters.

:::code language="python" source="~/cosmos-db-nosql-python-samples/003-how-to/app_aad_default.py" id="credential":::

> [!IMPORTANT]
> For details on how to add the correct role to enable `DefaultAzureCredential` to work, see [Configure role-based access control with Microsoft Entra ID for your Azure Cosmos DB account](security/how-to-grant-data-plane-role-based-access.md). In particular, see the section on creating roles and assigning them to a principal ID.

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

Each type of resource is represented by one or more associated Python classes. Here's a list of the most common classes for synchronous programming. (There are similar classes for asynchronous programming under the [azure.cosmos.aio](/python/api/azure-cosmos/azure.cosmos.aio) namespace.)

| Class | Description |
|---|---|
| [``CosmosClient``](/python/api/azure-cosmos/azure.cosmos.cosmosclient) | This class provides a client-side logical representation for the Azure Cosmos DB service. The client object is used to configure and execute requests against the service. |
| [``DatabaseProxy``](/python/api/azure-cosmos/azure.cosmos.databaseproxy) | An interface to a database that may, or may not, exist in the service yet. This class shouldn't be instantiated directly. Instead you should use the CosmosClient [get_database_client](/python/api/azure-cosmos/azure.cosmos.cosmosclient#azure-cosmos-cosmosclient-get-database-client) method. |
| [``ContainerProxy``](/python/api/azure-cosmos/azure.cosmos.containerproxy) | An interface to interact with a specific Cosmos DB container. This class shouldn't be instantiated directly. Instead, use the DatabaseProxy [get_container_client](/python/api/azure-cosmos/azure.cosmos.database.databaseproxy#azure-cosmos-database-databaseproxy-get-container-client) method to get an existing container, or the [create_container](/python/api/azure-cosmos/azure.cosmos.database.databaseproxy#azure-cosmos-database-databaseproxy-create-container) method to create a new container. |

The following guides show you how to use each of these classes to build your application.

| Guide | Description |
|--|---|
| [Create a database](how-to-python-create-database.md) | Create databases |
| [Create container](how-to-python-create-container.md) | Create containers |

## See also

- [PyPi](https://pypi.org/project/azure-cosmos/)
- [API reference](/python/api/azure-cosmos/azure.cosmos)
- [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos)
- [Give Feedback](https://github.com/Azure/azure-sdk-for-python/issues)

## Next steps

> [!div class="nextstepaction"]
> [Create a database in Azure Cosmos DB for NoSQL using Python](how-to-python-create-database.md)
