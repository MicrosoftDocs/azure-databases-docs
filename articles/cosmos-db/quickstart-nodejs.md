---
title: Quickstart - Azure SDK for Node.js
description: Deploy a Node.js Express web application that uses the Azure SDK for Node.js to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 06/11/2025
ms.custom: devx-track-js, devx-track-ts, devx-track-extended-azdevcli
zone_pivot_groups: azure-devlang-nodejs
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Node.js library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Use Azure Cosmos DB for NoSQL with Azure SDK for Node.js

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for NoSQL application using the Azure SDK for Node.js. Azure Cosmos DB for NoSQL is a schemaless data store allowing applications to store unstructured data in the cloud. Query data in your containers and perform common operations on individual items using the Azure SDK for Node.js.

[API reference documentation](/javascript/api/overview/azure/cosmos-readme) | [Library source code](https://github.com/azure/azure-sdk-for-js/tree/main/sdk/cosmosdb/cosmos) | [Package (npm)](https://www.npmjs.com/package/@azure/cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- Node.js 22 or newer

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
    azd init --template cosmos-db-nosql-nodejs-quickstart
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

::: zone pivot="programming-language-js"

:::image type="content" source="media/quickstart-nodejs/running-application-javascript.png" alt-text="Screenshot of the running web application.":::

:::zone-end

::: zone pivot="programming-language-ts"

:::image type="content" source="media/quickstart-nodejs/running-application-typescript.png" alt-text="Screenshot of the running web application.":::

:::zone-end

### Install the client library

The client library is available through the Node Package Manager, as the `@azure/cosmos` package.

1. Open a terminal and navigate to the `/src` folder.

    ```bash
    cd ./src
    ```

1. If not already installed, install the `@azure/cosmos` package using `npm install`.

    ```bash
    npm install --save @azure/cosmos
    ```

1. Also, install the `@azure/identity` package if not already installed.

    ```bash
    npm install --save @azure/identity
    ```

1. Open and review the **src/package.json** file to validate that the `azure-cosmos` and `azure-identity` entries both exist.

### Import libraries

::: zone pivot="programming-language-js"

Import the `DefaultAzureCredential` and `CosmosClient` types into your application code.

```javascript
import { DefaultAzureCredential } from '@azure/identity';
import { CosmosClient } from '@azure/cosmos';
```

:::zone-end

::: zone pivot="programming-language-ts"

Import all required types into your application code.

```typescript
import { PagedAsyncIterableIterator } from '@azure/core-paging';
import { DefaultAzureCredential, TokenCredential } from '@azure/identity';
import { Container, CosmosClient, Database, FeedResponse, ItemResponse, SqlQuerySpec } from '@azure/cosmos';
```

:::zone-end

## Object model

| Name | Description |
| --- | --- |
| [`CosmosClient`](/javascript/api/@azure/cosmos/cosmosclient) | This class is the primary client class and is used to manage account-wide metadata or databases. |
| [`Database`](/javascript/api/@azure/cosmos/database) | This class represents a database within the account. |
| [`Container`](/javascript/api/@azure/cosmos/container) | This class is primarily used to perform read, update, and delete operations on either the container or the items stored within the container. |
| [`PartitionKey`](/javascript/api/@azure/cosmos/partitionkey) | This class represents a logical partition key. This class is required for many common operations and queries. |
| [`SqlQuerySpec`](/javascript/api/@azure/cosmos/sqlqueryspec) | This interface represents a SQL query and any query parameters. |

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

::: zone pivot="programming-language-js"

```javascript
const credential = new DefaultAzureCredential();

const client = new CosmosClient({
    endpoint: '<azure-cosmos-db-nosql-account-endpoint>',
    aadCredentials: credential
});
```

:::zone-end

::: zone pivot="programming-language-ts"

```typescript
const credential: TokenCredential = new DefaultAzureCredential();

const client = new CosmosClient({
    endpoint: '<azure-cosmos-db-nosql-account-endpoint>',
    aadCredentials: credential
});
```

:::zone-end

### Get a database

Use `client.database` to retrieve the existing database named *`cosmicworks`*.

::: zone pivot="programming-language-js"

```javascript
const database = client.database('cosmicworks');
```

:::zone-end

::: zone pivot="programming-language-ts"

```typescript
const database: Database = client.database('cosmicworks');
```

:::zone-end

### Get a container

Retrieve the existing *`products`* container using `database.container`.

::: zone pivot="programming-language-js"

```javascript
const container = database.container('products');
```

:::zone-end

::: zone pivot="programming-language-ts"

```typescript
const container: Container = database.container('products');
```

:::zone-end

### Create an item

Build a new object with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale. Create an item in the container using `container.items.upsert`. This method "upserts" the item effectively replacing the item if it already exists.

::: zone pivot="programming-language-js"

```javascript
const item = {
    'id': 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    'category': 'gear-surf-surfboards',
    'name': 'Yamba Surfboard',
    'quantity': 12,
    'price': 850.00,
    'clearance': false
};

let response = await container.items.upsert(item);
```

:::zone-end

::: zone pivot="programming-language-ts"

```typescript
const item: Product = {
    'id': 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    'category': 'gear-surf-surfboards',
    'name': 'Yamba Surfboard',
    'quantity': 12,
    'price': 850.00,
    'clearance': false
};

let response: ItemResponse<Product> = await container.items.upsert<Product>(item);
```

:::zone-end

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.item` to get a pointer to an item and `item.read` to efficiently retrieve the specific item.

::: zone pivot="programming-language-js"

```javascript
const id = 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb';
const partitionKey = 'gear-surf-surfboards';

let response = await container.item(id, partitionKey).read();
let read_item = response.resource;
```

:::zone-end

::: zone pivot="programming-language-ts"

```typescript
const id = 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb';
const partitionKey = 'gear-surf-surfboards';

let response: ItemResponse<Product> = await container.item(id, partitionKey).read<Product>();
let read_item: Product = response.resource!;
```

:::zone-end

### Query items

Perform a query over multiple items in a container using `container.items.query`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

Fetch all of the results of the query using `query.fetchAll`. Loop through the results of the query.

::: zone pivot="programming-language-js"

```javascript
const querySpec = {
    query: 'SELECT * FROM products p WHERE p.category = @category',
    parameters: [
        {
            name: '@category',
            value: 'gear-surf-surfboards'
        }
    ]
};

let response = await container.items.query(querySpec).fetchAll();
for (let item of response.resources) {
    // Do something
}
```

:::zone-end

::: zone pivot="programming-language-ts"

```typescript
const querySpec: SqlQuerySpec = {
    query: 'SELECT * FROM products p WHERE p.category = @category',
    parameters: [
        {
            name: '@category',
            value: 'gear-surf-surfboards'
        }
    ]
};

let response: FeedResponse<Product> = await container.items.query<Product>(querySpec).fetchAll();
for (let item of response.resources) {
    // Do something
}
```

:::zone-end

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your NoSQL data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting items
- Importing bulk data from other sources
- Managing databases and containers

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for NoSQL data](visual-studio-code-extension.md?pivots=api-nosql).

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Java Quickstart](quickstart-java.md)
- [Python Quickstart](quickstart-python.md)
- [Go Quickstart](quickstart-go.md)
- [Rust Quickstart](quickstart-go.md)
