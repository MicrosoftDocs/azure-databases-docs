---
title: Get started using Python
description: Get started developing a Python application that works with Azure Cosmos DB for NoSQL. This article helps you learn how to set up a project and configure access to an Azure Cosmos DB for NoSQL endpoint.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: python
ms.topic: how-to
ms.date: 09/02/2025
ms.custom: devx-track-python, devguide-python, cosmos-db-dev-journey, devx-track-azurepowershell, devx-track-azurecli
ai-usage: ai-assisted
appliesto:
  - ✅ NoSQL
---

# Get started with Azure Cosmos DB for NoSQL using Python

This article explains how to connect to Azure Cosmos DB for NoSQL using the Python SDK. After connecting, perform operations on databases, containers, and items.

[Package (PyPi)](https://pypi.org/project/azure-cosmos/) | [API reference](/python/api/azure-cosmos/azure.cosmos) | [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos) | [Give feedback](https://github.com/Azure/azure-sdk-for-python/issues)

## Prerequisites

- An Azure account with an active subscription. Learn how to [create an account for free](https://azure.microsoft.com/free).
- Azure Cosmos DB for NoSQL account. Learn how to [create an API for NoSQL account](how-to-create-account.md).
- [Python 3.7 or later](https://www.python.org/downloads/).
- [Azure Command-Line Interface (CLI)](/cli/azure/) or [Azure PowerShell](/powershell/azure/).

## Set up your project

Create an environment for the Python code.

### [Virtual environment](#tab/env-virtual)

Use a [virtual environment](/azure/developer/python/configure-local-development-environment#configure-python-virtual-environment) to install Python packages in isolation without affecting your system.

Install the Azure Cosmos DB for NoSQL Python SDK in your virtual environment.

```bash
pip install azure-cosmos
```

### [Dev container](#tab/env-container)

A [dev container](https://containers.dev/) is a preconfigured environment for running Python code.

To run a dev container, use:

- **Visual Studio Code**: Clone the repository to your local machine and open the folder with the [Dev containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

- **GitHub Codespaces**: Open the repository in your browser with a [GitHub codespace](https://docs.github.com/en/codespaces/overview).

Install the Azure Cosmos DB for NoSQL Python SDK in the dev container.

```bash
pip install azure-cosmos
```

---

### Create the Python application

In your environment, create a new *app.py* file and add this code:

:::code language="python" source="~/cosmos-db-nosql-python-samples/003-how-to/app.py" id="imports":::

The preceding code imports modules used in the rest of the article.

## Connect to Azure Cosmos DB for NoSQL

To connect to the Azure Cosmos DB API for NoSQL, create an instance of the [`CosmosClient`](/python/api/azure-cosmos/azure.cosmos.cosmosclient) class. This class is the starting point to perform all operations against databases.

To connect to your API for NoSQL account using Microsoft Entra, use a security principal. The exact type of principal depends on where you host your application code. The following table is a quick reference guide.

| Where the application runs | Security principal
|--|--|---|
| Local machine (developing and testing) | User identity or service principal |
| Azure | Managed identity |
| Servers or clients outside of Azure | Service principal |

### Import Azure.Identity

The **`azure-identity`** package provides core authentication functionality shared across all Azure SDK libraries.

Import the [`azure-identity`](https://pypi.org/project/azure-identity/) package into your environment.

```bash
pip install azure-identity
```

### Create CosmosClient with default credential implementation

If you're testing on a local machine or running your application on Azure services with managed identity support, obtain an OAuth token by creating a [``DefaultAzureCredential``](/python/api/azure-identity/azure.identity.defaultazurecredential) instance.

In your *app.py* file:

- Get the endpoint for your account and set it as the environment variable `COSMOS_ENDPOINT`.

- Import the [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential) and create an instance of it.

- Create a new instance of the **CosmosClient** class with the **ENDPOINT** and **credential** as parameters.

:::code language="python" source="~/cosmos-db-nosql-python-samples/003-how-to/app_aad_default.py" id="credential":::

> [!IMPORTANT]
> For details on adding the correct role to enable `DefaultAzureCredential`, see [Configure role-based access control with Microsoft Entra ID for your Azure Cosmos DB account](how-to-connect-role-based-access-control.md#grant-data-plane-role-based-access). In particular, see the section on creating roles and assigning them to a principal ID.

## Build your application

As you build your application, your code primarily interacts with four types of resources:

- The API for NoSQL account, which is the unique top-level namespace for your Azure Cosmos DB data.

- Databases, which organize the containers in your account.

- Containers, which contain a set of individual items in your database.

- Items, which represent a JSON document in your container.

This diagram shows the relationship between these resources.

:::image type="complex" source="media/how-to-dotnet-get-started/resource-hierarchy.svg" alt-text="Diagram of the Azure Cosmos DB hierarchy including accounts, databases, containers, and items." border="false":::
    Hierarchical diagram showing an Azure Cosmos DB account at the top. The account has two child database nodes. One of the database nodes includes two child container nodes. The other database node includes a single child container node. That single container node has three child item nodes.
:::image-end:::

One or more associated Python classes represents type of resource. This list shows the most common classes for synchronous programming. (There are similar classes for asynchronous programming under the [azure.cosmos.aio](/python/api/azure-cosmos/azure.cosmos.aio) namespace.)

| Class | Description |
|---|---|
| [``CosmosClient``](/python/api/azure-cosmos/azure.cosmos.cosmosclient) | This class provides a client-side logical representation for the Azure Cosmos DB service. The client object configures and executes requests against the service. |
| [``DatabaseProxy``](/python/api/azure-cosmos/azure.cosmos.databaseproxy) | An interface to a database that could, or couldn't, exist in the service yet. This class shouldn't be instantiated directly. Instead, use the CosmosClient [get_database_client](/python/api/azure-cosmos/azure.cosmos.cosmosclient#azure-cosmos-cosmosclient-get-database-client) method. |
| [``ContainerProxy``](/python/api/azure-cosmos/azure.cosmos.containerproxy) | An interface to interact with a specific Cosmos DB container. This class shouldn't be instantiated directly. Instead, use the DatabaseProxy [get_container_client](/python/api/azure-cosmos/azure.cosmos.database.databaseproxy#azure-cosmos-database-databaseproxy-get-container-client) method to get an existing container, or the [create_container](/python/api/azure-cosmos/azure.cosmos.database.databaseproxy#azure-cosmos-database-databaseproxy-create-container) method to create a new container. |

These guides show how to use each of these classes to build your application.

| Guide | Description |
|--|---|
| [Create a database](how-to-python-create-database.md) | Create a database. |
| [Create container](how-to-python-create-container.md) | Create a container. |

## See also

- [PyPi](https://pypi.org/project/azure-cosmos/)
- [API reference](/python/api/azure-cosmos/azure.cosmos)
- [Library source code](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos)
- [Give feedback](https://github.com/Azure/azure-sdk-for-python/issues)

## Next steps

> [!div class="nextstepaction"]
> [Create a database in Azure Cosmos DB for NoSQL using Python](how-to-python-create-database.md)
