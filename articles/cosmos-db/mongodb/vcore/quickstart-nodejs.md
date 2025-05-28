---
title: Quickstart - Node.js driver
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Deploy a Node.js web application that uses the client library for JavaScript to interact with Azure Cosmos DB for MongoDB (vCore) data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 05/03/2025
ms.custom: devx-track-js, devx-track-ts, devx-track-dotnet, devx-track-extended-azdevcli
zone_pivot_groups: azure-devlang-nodejs
appliesto:
  - ✅ MongoDB (vCore)
# CustomerIntent: As a developer, I want to learn the basics of the Node.js library so that I can build applications with Azure Cosmos DB for MongoDB (vCore).
---

# Quickstart: Use Azure Cosmos DB for MongoDB vCore with MongoDB driver for Node.js

[!INCLUDE[Developer Quickstart selector](includes/selector-dev-quickstart.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for MongoDB application using Node.js. Azure Cosmos DB for MongoDB vCore is a schemaless data store allowing applications to store unstructured documents in the cloud with MongoDB libraries. You learn how to create documents and perform basic tasks within your Azure Cosmos DB resource using Node.js.

[Library source code](https://github.com/mongodb/node-mongodb-native) | [Package (npm)](https://www.npmjs.com/package/mongodb) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prereq-dev-quickstart.md)]

- Node.js 22 or newer

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for MongoDB vCore cluster and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-mongodb-vcore-nodejs-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the cluster using `azd up`. The Bicep templates also deploy a sample web application.

    ```azurecli
    azd up
    ```

1. During the provisioning process, select your subscription, desired location, and target resource group. Wait for the provisioning process to complete. The process can take **approximately ten minutes**.

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

1. If not already installed, install the `@azure/identity` package using `npm install`.

    ```bash
    npm install --save @azure/identity
    ```

1. Open and review the **src/ts/package.json** file to validate that both package entries exist.

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

1. If not already installed, install the `@azure/identity` package using `npm install`.

    ```bash
    npm install --save @azure/identity
    ```

1. Open and review the **src/js/package.json** file to validate that both package entries exist.

::: zone-end

### Import libraries

::: zone pivot="programming-language-js"

Import the following namespaces into your application code:

| | Package | Source |
| --- | --- | --- |
| **`TokenCredential`** | `@azure/identity` | Azure SDK for JavaScript |
| **`DefaultAzureCredential`** | `@azure/identity` | Azure SDK for JavaScript |
| **`MongoClient`** | `mongodb` | Official MongoDB driver for Node.js |

```javascript
import { DefaultAzureCredential, TokenCredential } from '@azure/identity';

import { MongoClient } from 'mongodb';
```

:::zone-end

::: zone pivot="programming-language-js"

Import all required types into your application code including, but not limited to:

| | Package | Source |
| --- | --- | --- |
| **`TokenCredential`** | `@azure/identity` | Azure SDK for JavaScript |
| **`DefaultAzureCredential`** | `@azure/identity` | Azure SDK for JavaScript |
| **`MongoClient`** | `mongodb` | Official MongoDB driver for Node.js |


```typescript
import { AccessToken, DefaultAzureCredential, TokenCredential } from '@azure/identity';

import { Collection, Db, Filter, FindCursor, MongoClient, OIDCCallbackParams, OIDCResponse, UpdateFilter, UpdateOptions, UpdateResult, WithId } from 'mongodb';
```

:::zone-end

## Object model

| Name | Description |
| --- | --- |
| MongoClient | Type used to connect to MongoDB. |
| `Database` | Represents a database in the cluster. |
| `Collection` | Represents a collection within a database in the cluster. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Get a document](#read-a-document)
- [Query documents](#query-documents)

The sample code in the template uses a database named `cosmicworks` and collection named `products`. The `products` collection contains details such as name, category, quantity, and a unique identifier for each product. The collection uses the `/category` property as a shard key.

### Authenticate the client

While Microsoft Entra authentication for Azure Cosmos DB for MongoDB vCore can use well known `TokenCredential` types, you must implement a custom token handler. This sample implementation can be used to create a `MongoClient` with support for standard Microsoft Entra authentication of many identity types.

::: zone pivot="programming-language-ts"

1. First, define a callback named `AzureIdentityTokenCallback` that takes in `OIDCCallbackParams` and `TokenCredential` and then asynchronously returns a `OIDCResponse`.

    ```typescript
    const AzureIdentityTokenCallback = async (params: OIDCCallbackParams, credential: TokenCredential): Promise<OIDCResponse> => {
        const tokenResponse: AccessToken | null = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
        return {
            accessToken: tokenResponse?.token || '',
            expiresInSeconds: (tokenResponse?.expiresOnTimestamp || 0) - Math.floor(Date.now() / 1000)
        };
    };
    ```

1. Define variables for your cluster name and token credential.

    ```typescript
    const clusterName: string = '<azure-cosmos-db-mongodb-vcore-cluster-name>';

    const credential: TokenCredential = new DefaultAzureCredential();
    ```

1. Build an instance of `MongoClient` using your cluster name, and the known best practice configuration options for Azure Cosmos DB for MongoDB vCore. Also, configure your custom authentication mechanism.

    ```typescript
    const client = new MongoClient(
        `mongodb+srv://${clusterName}.global.mongocluster.cosmos.azure.com/`, {
        connectTimeoutMS: 120000,
        tls: true,
        retryWrites: true,
        authMechanism: 'MONGODB-OIDC',
        authMechanismProperties: {
                OIDC_CALLBACK: (params: OIDCCallbackParams) => AzureIdentityTokenCallback(params, credential),
                ALLOWED_HOSTS: ['*.azure.com']
            }
        }
    );
    ```

::: zone-end

::: zone pivot="programming-language-js"

1. First, define a callback named `azureIdentityTokenCallback` that takes in parameters and a token credential and then asynchronously returns a response.

    ```javascript
    const azureIdentityTokenCallback = async (_, credential) => {
        const tokenResponse = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
    
        if (!tokenResponse || !tokenResponse.token) {
            throw new Error('Failed to retrieve a valid access token.');
        }
    
        return {
            accessToken: tokenResponse.token,
            expiresInSeconds: Math.floor((tokenResponse.expiresOnTimestamp - Date.now()) / 1000),
        };
    };
    ```

1. Define variables for your cluster name and token credential.

    ```javascript
    const clusterName = '<azure-cosmos-db-mongodb-vcore-cluster-name>';
    
    const credential = new DefaultAzureCredential();
    ```

1. Build an instance of `MongoClient` using your cluster name, and the known best practice configuration options for Azure Cosmos DB for MongoDB vCore. Also, configure your custom authentication mechanism.

    ```javascript
    client = new MongoClient(`mongodb+srv://${clusterName}.global.mongocluster.cosmos.azure.com/`, {
        connectTimeoutMS: 120000,
        tls: true,
        retryWrites: true,
        authMechanism: 'MONGODB-OIDC',
        authMechanismProperties: {
            OIDC_CALLBACK: (params) => azureIdentityTokenCallback(params, credential),
            ALLOWED_HOSTS: ['*.azure.com']
        }
    });

    await client.connect();
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

var response: FindCursor<WithId<Product>> = collection.find(query);
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

var response = collection.find(query);
```

```javascript
for await (const item of response) {
    // Do something with each item
}
```

::: zone-end

### Delete a document

Delete a document by sending a filter for the unique identifier of the document. Use `collection.deleteOne<>` to asynchronously remove the document from the collection.

::: zone pivot="programming-language-ts"

```typescript
var filter: Filter<Product> = { 
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb'
};

await collection.deleteOne(filter);
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const filter = {
    _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb'
};

await collection.deleteOne(filter);
```

::: zone-end

## Explore your data

[!INCLUDE[Section - Visual Studio Code extension exploration](includes/section-vscode-extension-explore.md)]

## Clean up resources

[!INCLUDE[Section - Quickstart clean up](includes/section-quickstart-clean-up.md)]

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Python Quickstart](quickstart-python.md)
