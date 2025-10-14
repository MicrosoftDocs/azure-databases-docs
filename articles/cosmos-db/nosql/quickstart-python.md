---
title: Quickstart - Azure SDK for Python
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy a Python Flask web application that uses the Azure SDK for Python to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: python
ms.topic: quickstart-sdk
ms.date: 06/11/2025
ms.custom: devx-track-python, devx-track-extended-azdevcli
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Python library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for Python

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for NoSQL application using the Azure SDK for Python. Azure Cosmos DB for NoSQL is a schemaless data store allowing applications to store unstructured data in the cloud. Query data in your containers and perform common operations on individual items using the Azure SDK for Python.

[API reference documentation](/python/api/overview/azure/cosmos-readme) | [Library source code](https://github.com/azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos) | [Package (PyPI)](https://pypi.org/project/azure-cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- Python 3.12

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for NoSQL account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-nosql-python-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the Azure Cosmos DB account using `azd up`. The Bicep templates also deploy a sample web application.

    ```azurecli
    azd up
    ```

1. During the provisioning process, select your subscription, desired location, and target resource group. Wait for the provisioning process to complete. The process can take **approximately five minutes**.

1. Once the provisioning of your Azure resources is done, a URL to the running web application is included in the output.

    ```output
    Deploying services (azd deploy)
    
      (✓) Done: Deploying service web
    - Endpoint: <https://[container-app-sub-domain].azurecontainerapps.io>
    
    SUCCESS: Your application was provisioned and deployed to Azure in 5 minutes 0 seconds.
    ```

1. Use the URL in the console to navigate to your web application in the browser. Observe the output of the running app.

:::image type="content" source="media/quickstart-python/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through the Python Package Index, as the `azure-cosmos` library.

1. Open a terminal and navigate to the `/src` folder.

    ```bash
    cd ./src
    ```

1. If not already installed, install the `azure-cosmos` package using `pip install`.

    ```bash
    pip install azure-cosmos
    ```

1. Also, install the `azure-identity` package if not already installed.

    ```bash
    pip install azure-identity
    ```

1. Open and review the **src/requirements.txt** file to validate that the `azure-cosmos` and `azure-identity` entries both exist.

### Import libraries

Import the `DefaultAzureCredential` and `CosmosClient` types into your application code.

```python
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
```

## Object model

| Name | Description |
| --- | --- |
| [`CosmosClient`](/python/api/azure-cosmos/azure.cosmos.cosmos_client.cosmosclient) | This class is the primary client class and is used to manage account-wide metadata or databases. |
| [`DatabaseProxy`](/python/api/azure-cosmos/azure.cosmos.database.databaseproxy) | This class represents a database within the account. |
| [`ContainerProxy`](/python/api/azure-cosmos/azure.cosmos.container.containerproxy) | This class is primarily used to perform read, update, and delete operations on either the container or the items stored within the container. |
| [`PartitionKey`](/python/api/azure-cosmos/azure.cosmos.partition_key.partitionkey) | This class represents a logical partition key. This class is required for many common operations and queries. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a container](#get-a-container)
- [Create an item](#create-an-item)
- [Get an item](#read-an-item)
- [Query items](#query-items)

The sample code in the template uses a database named `cosmicworks` and container named `products`. The `products` container contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The container uses the `/category` property as a logical partition key.

### Authenticate the client

This sample creates a new instance of the `CosmosClient` type and authenticates using a `DefaultAzureCredential` instance.

```python
credential = DefaultAzureCredential()

client = CosmosClient(url="<azure-cosmos-db-nosql-account-endpoint>", credential=credential)
```

### Get a database

Use `client.get_database_client` to retrieve the existing database named *`cosmicworks`*.

```python
database = client.get_database_client("cosmicworks")
```

### Get a container

Retrieve the existing *`products`* container using `database.get_container_client`.

```python
container = database.get_container_client("products")
```

### Create an item

Build a new object with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale. Create an item in the container using `container.upsert_item`. This method "upserts" the item effectively replacing the item if it already exists.

```python
new_item = {
    "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    "category": "gear-surf-surfboards",
    "name": "Yamba Surfboard",
    "quantity": 12,
    "sale": False,
}

created_item = container.upsert_item(new_item)
```

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.read_item` to efficiently retrieve the specific item.

```python
existing_item = container.read_item(
    item="aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    partition_key="gear-surf-surfboards",
)
```

### Query items

Perform a query over multiple items in a container using `container.GetItemQueryIterator`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

```python
queryText = "SELECT * FROM products p WHERE p.category = @category"

results = container.query_items(
    query=queryText,
    parameters=[
        dict(
            name="@category",
            value="gear-surf-surfboards",
        )
    ],
    enable_cross_partition_query=False,
)
```

Loop through the results of the query.

```python
items = [item for item in results]

output = json.dumps(items, indent=True)
```

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your NoSQL data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting items
- Importing bulk data from other sources
- Managing databases and containers

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for NoSQL data](../visual-studio-code-extension.md?pivots=api-nosql).

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Node.js Quickstart](quickstart-nodejs.md)
- [Java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)
- [Rust Quickstart](quickstart-go.md)
