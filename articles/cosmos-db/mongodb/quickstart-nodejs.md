---
title: Quickstart - Node.js
titleSuffix: Azure Cosmos DB for MongoDB
description: Deploy a .NET web application that uses the client library for Node.js to interact with Azure Cosmos DB for MongoDB data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 04/08/2025
ms.custom: devx-track-js, devx-track-ts, devx-track-dotnet, devx-track-extended-azdevcli, sfi-image-nochange
zone_pivot_groups: azure-devlang-nodejs
appliesto:
- ✅ MongoDB
# CustomerIntent: As a developer, I want to learn the basics of the Node.js library so that I can build applications with Azure Cosmos DB for MongoDB.
---

# Quickstart: Use Azure Cosmos DB for MongoDB with Node.js

[!INCLUDE[Developer Quickstart selector](includes/quickstart-dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for MongoDB application using Python. Azure Cosmos DB for MongoDB is a schemaless data store allowing applications to store unstructured documents in the cloud with MongoDB libraries. You learn how to create documents and perform basic tasks within your Azure Cosmos DB resource using Python.

[Library source code](https://github.com/mongodb/node-mongodb-native) | [Package (npm)](https://www.npmjs.com/package/mongodb) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- Node.js 22 or newer

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-mongodb-nodejs-quickstart
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

The client library is available through npm, as the `mongodb` package.

::: zone pivot="programming-language-ts"

1. Open a terminal and navigate to the `/src/ts` folder.

    ```bash
    cd ./src/ts
    ```

1. If not already installed, install the `mongodb` package using `npm install`.

    ```bash
    npm install --save mongodb
    ```

1. Open and review the **src/ts/package.json** file to validate that the `mongodb` entry exists.

::: zone-end

::: zone pivot="programming-language-js"

1. Open a terminal and navigate to the `/src/js` folder.

    ```bash
    cd ./src/js
    ```

1. If not already installed, install the `mongodb` package using `npm install`.

    ```bash
    npm install --save mongodb
    ```

1. Open and review the **src/js/package.json** file to validate that the `mongodb` entry exists.

::: zone-end

### Import libraries

::: zone pivot="programming-language-js"

Import the `MongoClient` type into your application code.

```javascript
import { MongoClient } from 'mongodb';
```

:::zone-end

::: zone pivot="programming-language-js"

Import all required types into your application code.

```typescript
import { Collection, Db, Filter, FindCursor, MongoClient, UpdateFilter, UpdateOptions, UpdateResult, WithId } from 'mongodb';
```

:::zone-end

## Object model

| Name | Description |
| --- | --- |
| [`MongoClient`](https://www.mongodb.com/docs/drivers/node/current/quick-start/connect-to-mongodb/) | Type used to connect to MongoDB. |
| `Database` | Represents a database in the account. |
| `Collection` | Represents a collection within a database in the account. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Get a document](#read-a-document)
- [Query documents](#query-documents)

The sample code in the template uses a database named `cosmicworks` and collection named `products`. The `products` collection contains details such as name, category, quantity, and a unique identifier for each product. The collection uses the `/category` property as a shard key.

### Authenticate the client

This sample creates a new instance of the `MongoClient` type.

::: zone pivot="programming-language-ts"

```typescript
const connectionString = "<azure-cosmos-db-for-mongodb-connection-string>";

const client = new MongoClient(connectionString);
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const connectionString = "<azure-cosmos-db-for-mongodb-connection-string>";

const client = new MongoClient(connectionString);
```

::: zone-end

### Get a database

This sample creates an instance of the `Db` type using the `db` function of the `MongoClient` type.

::: zone pivot="programming-language-ts"

```typescript
const database: Db = client.db("<database-name>");
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const database = client.db("<database-name>");
```

::: zone-end

### Get a collection

This sample creates an instance of the `Collection` type using the `collection` function of the `Db` type.

::: zone pivot="programming-language-ts"

This function has a generic parameter that uses the `Product` type defined in an interface.

```typescript
const collection: Collection<Product> = database.collection<Product>("<collection-name>");
```

```typescript
export interface Product {
    _id: string;
    category: string;
    name: string;
    quantity: number;
    price: number;
    clearance: boolean;
}
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const collection = database.collection("<collection-name>");
```

::: zone-end

### Create a document

Create a document in the collection using `collection.updateOne`. This method "upserts" the item effectively replacing the item if it already exists.

::: zone pivot="programming-language-ts"

```typescript
var document: Product = {
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    category: 'gear-surf-surfboards',
    name: 'Yamba Surfboard',
    quantity: 12,
    price: 850.00,
    clearance: false
};

var query: Filter<Product> = {
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    category: 'gear-surf-surfboards'
};
var payload: UpdateFilter<Product> = {
    $set: document
};
var options: UpdateOptions = {
    upsert: true
};
var response: UpdateResult<Product> = await collection.updateOne(query, payload, options);
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
var document = {
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    category: 'gear-surf-surfboards',
    name: 'Yamba Surfboard',
    quantity: 12,
    price: 850.00,
    clearance: false
};

const query = {
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    category: 'gear-surf-surfboards'
};
const payload = {
    $set: document
};
const options = {
    upsert: true,
    new: true
};
var response = await collection.updateOne(query, payload, options);
```

::: zone-end

### Read a document

Perform a point read operation by using both the unique identifier (`id`) and shard key fields. Use `collection.findOne` to efficiently retrieve the specific item.

::: zone pivot="programming-language-ts"

```typescript
var query: Filter<Product> = { 
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb', 
    category: 'gear-surf-surfboards' 
};

var response: WithId<Product> | null = await collection.findOne(query);
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
var query = { 
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb', 
    category: 'gear-surf-surfboards' 
};

var response = await collection.findOne(query);
```

::: zone-end

### Query documents

Perform a query over multiple items in a container using `collection.find`. This query finds all items within a specified category (shard key).

::: zone pivot="programming-language-ts"

```typescript
var query: Filter<Product> = { 
    category: 'gear-surf-surfboards' 
};

var response: FindCursor<WithId<Product>> = await collection.find(query);
```

```typescript
for await (const item of response) {
    // Do something with each item
}
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
var query = { 
    category: 'gear-surf-surfboards' 
};

var response = await collection.find(query);
```

```javascript
for await (const item of response) {
    // Do something with each item
}
```

::: zone-end

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your MongoDB data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting documents
- Importing bulk data from other sources
- Managing databases and collections

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for MongoDB data](../visual-studio-code-extension.md?pivots=api-mongodb&tabs=MongoDB).

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down --force --purge
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Python Quickstart](quickstart-python.md)
