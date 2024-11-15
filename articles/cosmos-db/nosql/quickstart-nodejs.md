---
title: Quickstart - Node.js client library
titleSuffix: Azure Cosmos DB for NoSQL
description: Deploy a Node.js Express web application that uses the Azure SDK for Node.js to interact with Azure Cosmos DB for NoSQL data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 11/18/2024
ms.custom: devx-track-js, devx-track-ts, devx-track-extended-azdevcli
zone_pivot_groups: azure-cosmos-db-quickstart-env
appliesto:
  - ✅ NoSQL
# CustomerIntent: As a developer, I want to learn the basics of the Node.js library so that I can build applications with Azure Cosmos DB for NoSQL.
---

# Quickstart: Azure Cosmos DB for NoSQL library for Node.js

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

Get started with the Azure Cosmos DB for NoSQL client library for Node.js to query data in your containers and perform common operations on individual items. Follow these steps to deploy a minimal solution to your environment using the Azure Developer CLI.

[API reference documentation](/javascript/api/overview/azure/cosmos-readme) | [Library source code](https://github.com/azure/azure-sdk-for-js/tree/main/sdk/cosmosdb/cosmos) | [Package (npm)](https://www.npmjs.com/package/@azure/cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

[!INCLUDE[Developer Quickstart prerequisites](includes/quickstart/dev-prereqs.md)]

## Setting up

Deploy this project's development container to your environment. Then, use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for NoSQL account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

::: zone pivot="devcontainer-codespace"

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://codespaces.new/azure-samples/cosmos-db-nosql-nodejs-quickstart?template=false&quickstart=1&azure-portal=true)

::: zone-end

[!INCLUDE[Developer Quickstart setup](includes/quickstart/dev-setup.md)]

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

[!INCLUDE[Developer Quickstart sample explanation](includes/quickstart/dev-sample-primer.md)]

### Authenticate the client

[!INCLUDE[Developer Quickstart authentication explanation](includes/quickstart/dev-auth-primer.md)]

This sample creates a new instance of the `CosmosClient` type and authenticates using a `DefaultAzureCredential` instance.

### [JavaScript](#tab/javascript)

```javascript
const credential = new DefaultAzureCredential();

const client = new CosmosClient({
    '<azure-cosmos-db-nosql-account-endpoint>',
    aadCredentials: credential
});
```

### [TypeScript](#tab/typescript)

```typescript
const credential: TokenCredential = new DefaultAzureCredential();

const client = new CosmosClient({
    '<azure-cosmos-db-nosql-account-endpoint>',
    aadCredentials: credential
});
```

---

### Get a database

Use `client.database` to retrieve the existing database named *`cosmicworks`*.

### [JavaScript](#tab/javascript)

```javascript
const database = client.database('cosmicworks');
```

### [TypeScript](#tab/typescript)

```typescript
const database: Database = client.database('cosmicworks');
```

---

### Get a container

Retrieve the existing *`products`* container using `database.container`.

### [JavaScript](#tab/javascript)

```javascript
const container = database.container('products');
```

### [TypeScript](#tab/typescript)

```typescript
const container: Container = database.container('products');
```

---

### Create an item

Build a new object with all of the members you want to serialize into JSON. In this example, the type has a unique identifier, and fields for category, name, quantity, price, and sale. Create an item in the container using `container.items.upsert`. This method "upserts" the item effectively replacing the item if it already exists.

### [JavaScript](#tab/javascript)

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

### [TypeScript](#tab/typescript)

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

---

### Read an item

Perform a point read operation by using both the unique identifier (`id`) and partition key fields. Use `container.item` to get a pointer to an item and `item.read` to efficiently retrieve the specific item.

### [JavaScript](#tab/javascript)

```javascript
const id = 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb';
const partitionKey = 'gear-surf-surfboards';

let response = await container.item(id, partitionKey).read();
let read_item = response.resource;
```

### [TypeScript](#tab/typescript)

```typescript
const id = 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb';
const partitionKey = 'gear-surf-surfboards';

let response: ItemResponse<Product> = await container.item(id, partitionKey).read<Product>();
let read_item: Product = response.resource!;
```

---

### Query items

Perform a query over multiple items in a container using `container.items.query`. Find all items within a specified category using this parameterized query:

```nosql
SELECT * FROM products p WHERE p.category = @category
```

Fetch all of the results of the query using `query.fetchAll`. Loop through the results of the query.

### [JavaScript](#tab/javascript)

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

### [TypeScript](#tab/typescript)

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

---

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Java Quickstart](quickstart-java.md)
- [Python Quickstart](quickstart-python.md)
- [Go Quickstart](quickstart-go.md)
- [Rust Quickstart](quickstart-go.md)
