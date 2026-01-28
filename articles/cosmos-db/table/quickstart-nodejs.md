---
title: Quickstart - Azure SDK for Node.js
titleSuffix: Azure Cosmos DB for Table
description: Deploy a Node.js web application that uses the Azure SDK for Table to interact with Azure Cosmos DB for Table data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.reviewer: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 04/08/2025
ms.custom: devx-track-js, devx-track-ts, devx-track-extended-azdevcli
zone_pivot_groups: azure-devlang-nodejs
# CustomerIntent: As a developer, I want to learn the basics of the Node.js library so that I can build applications with Azure Cosmos DB for Table.
---

# Quickstart: Use Azure Cosmos DB for Table with Azure SDK for Node.js

[!INCLUDE[Developer Quickstart selector](includes/quickstart/dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for Table application using the Azure SDK for Node.js. Azure Cosmos DB for Table is a schemaless data store allowing applications to store structured table data in the cloud. You learn how to create tables, rows, and perform basic tasks within your Azure Cosmos DB resource using the Azure SDK for Node.js.

[API reference documentation](/javascript/api/%40azure/data-tables) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/tables/data-tables) | [Package (npm)](https://www.npmjs.com/package/@azure/data-tables) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

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
    azd init --template cosmos-db-table-nodejs-quickstart
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

::: zone-end

::: zone pivot="programming-language-ts"

:::image type="content" source="media/quickstart-nodejs/running-application-typescript.png" alt-text="Screenshot of the running web application.":::

::: zone-end

### Install the client library

The client library is available through npm, as the `@azure/data-tables` package.

::: zone pivot="programming-language-ts"

1. Open a terminal and navigate to the `/src/ts` folder.

    ```bash
    cd ./src/ts
    ```

1. If not already installed, install the `@azure/data-tables` package using `npm install`.

    ```bash
    npm install --save @azure/data-tables
    ```

1. Open and review the **src/ts/package.json** file to validate that the `@azure/data-tables` entry exists.

::: zone-end

::: zone pivot="programming-language-js"

1. Open a terminal and navigate to the `/src/js` folder.

    ```bash
    cd ./src/js
    ```

1. If not already installed, install the `@azure/data-tables` package using `npm install`.

    ```bash
    npm install --save @azure/data-tables
    ```

1. Open and review the **src/js/package.json** file to validate that the `@azure/data-tables` entry exists.

::: zone-end

### Import libraries

::: zone pivot="programming-language-js"

Import the `DefaultAzureCredential`, `TableServiceClient`, and `TableClient` types into your application code.

```javascript
import { DefaultAzureCredential } from '@azure/identity';
import { TableServiceClient, TableClient } from '@azure/data-tables';
```

:::zone-end

::: zone pivot="programming-language-js"

Import all required types into your application code.

```typescript
import { DefaultAzureCredential, TokenCredential } from '@azure/identity';
import { TableServiceClient, TableClient, TableEntityResult, GetTableEntityResponse, TableEntityResultPage, TableEntityQueryOptions } from '@azure/data-tables';
```

:::zone-end

## Object model

| Name | Description |
| --- | --- |
| [`TableServiceClient`](/javascript/api/@azure/data-tables/tableserviceclient) | This type is the primary client type and is used to manage account-wide metadata or databases. |
| [`TableClient`](/javascript/api/@azure/data-tables/tableclient) | This type represents the client for a table within the account. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a table](#get-a-table)
- [Create an entity](#create-an-entity)
- [Get an entity](#get-an-entity)
- [Query entities](#query-entities)

The sample code in the template uses a table named `cosmicworks-products`. The `cosmicworks-products` table contains details such as name, category, quantity, price, a unique identifier, and a sale flag for each product. The container uses a *unique identifier* as the row key and *category* as a partition key.

### Authenticate the client

This sample creates a new instance of the `TableServiceClient` type.

::: zone pivot="programming-language-ts"

```typescript
let client: TableServiceClient = new TableServiceClient("<azure-cosmos-db-table-account-endpoint>", "<credential>");
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const credential = new DefaultAzureCredential();

let client = new TableServiceClient("<azure-cosmos-db-table-account-endpoint>", credential);
```

::: zone-end

### Get a table

This sample creates an instance of the `TableClient` type using the `GetTableClient` function of the `TableServiceClient` type.

::: zone pivot="programming-language-ts"

```typescript
let table: TableClient = new TableClient("<azure-cosmos-db-table-account-endpoint>", "<azure-cosmos-db-table-name>", credential);
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
let table = new TableClient("<azure-cosmos-db-table-account-endpoint>", "<azure-cosmos-db-table-name>", credential);
```

::: zone-end

### Create an entity

::: zone pivot="programming-language-ts"

The easiest way to create a new entity in a table is to derive a new interface from `TableEntity` and then create a new object of that type.

```typescript
export interface Product extends TableEntity {
    name: string;
    quantity: number;
    price: number;
    clearance: boolean;
}
```

```typescript
const entity: Product = {
    rowKey: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    partitionKey: 'gear-surf-surfboards',
    name: 'Yamba Surfboard',
    quantity: 12,
    price: 850.00,
    clearance: false
};
```

::: zone-end

::: zone pivot="programming-language-js"

The easiest way to create a new item in a table is to build a JSON object.

```javascript
const entity = {
    rowKey: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    partitionKey: 'gear-surf-surfboards',
    name: 'Yamba Surfboard',
    quantity: 12,
    price: 850.00,
    clearance: false
};
```

::: zone-end

Create an entity in the table using the `upsertEntity` method from the `TableService` instance.

::: zone pivot="programming-language-ts"

```typescript
await table.upsertEntity<Product>(entity, "Replace"); 
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
await table.upsertEntity(entity, "Replace");
```

::: zone-end

### Get an entity

You can retrieve a specific entity from a table using the `getEntity` method, the **row key** for the entity, and **partition key** of the entity.

::: zone pivot="programming-language-ts"

```typescript
const response: GetTableEntityResponse<TableEntityResult<Product>> = await table.getEntity<Product>(partitionKey, rowKey);

const entity: Product = response as Product;
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const entity = await table.getEntity(partitionKey, rowKey);
```

::: zone-end

### Query entities

After you insert an entity, you can also run a query to get all entities that match a specific filter by using `listEntities` with an OData filter.

::: zone pivot="programming-language-ts"

```typescript
const partitionKey: string = 'gear-surf-surfboards';

const filter: string = odata`PartitionKey eq '${partitionKey}'`

const queryOptions: TableEntityQueryOptions = { filter: filter }

const entities: PagedAsyncIterableIterator<TableEntityResult<Product>, TableEntityResultPage<Product>> = table.listEntities<Product>({ queryOptions: queryOptions });
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
const partitionKey = 'gear-surf-surfboards';

const entities = table.listEntities({
    queryOptions: {
        filter: odata`PartitionKey eq '${partitionKey}'`
    }
});
```

::: zone-end

Parse the paginated results of the query by using an asynchronous `for await` loop on the paginated set of `entities`.

::: zone pivot="programming-language-ts"

```typescript
for await(const entity of entities) {
    // Do something
}
```

::: zone-end

::: zone pivot="programming-language-js"

```javascript
for await(const entity of entities) {
    // Do something
}
```

::: zone-end

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down
```

## Related content

- [.NET Quickstart](quickstart-dotnet.md)
- [Python Quickstart](quickstart-python.md)
- [Java Quickstart](quickstart-java.md)
- [Go Quickstart](quickstart-go.md)
