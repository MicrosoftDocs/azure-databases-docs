---
title: Perform Bulk Operations Using the Azure SDK for JavaScript
description: Learn how to perform bulk operations like import and update using the Azure SDK for JavaScript and Azure Cosmos DB for NoSQL.
author: sajeetharan
ms.author: sasinnat
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.devlang: javascript
ms.topic: how-to
ms.date: 05/12/2025
ms.custom:
  - devx-track-javascript
  - build-2025
appliesto:
  - NoSQL
---

# Perform bulk operations in Azure Cosmos DB for NoSQL using the Azure SDK for JavaScript

In this guide, use the `executeBulkOperations` feature in the Azure SDK for JavaScript to perform bulk create and update operations in Azure Cosmos DB for NoSQL. This feature adjusts per-partition concurrency, automatically handles retry logic for each individual operation, and performs large quantities (100+) of operations. This feature automatically adjusts concurrency dynamically by increasing when calls succeed without throttling and scaling back when throttling occurs.

## Prerequisites

- An existing Azure Cosmos DB for NoSQL account

  - If you don't have an existing account, [create a new account](quickstart-portal.md).

- Node.js 22.x or later

## Initialize your development environment

Start by creating a development environment with an initial project and all developer dependencies. For this project, you're going to install the [`@azure/cosmos`](https://www.npmjs.com/package/@azure/cosmos) from the [Azure SDK for JavaScript](https://github.com/azure/azure-sdk-for-js) as a development dependency.

1. Open a terminal in an empty folder.

1. Initialize a new Node.js project.

    ```bash
    npm init
    ```

1. Update your newly generated `package.json` file with this content.

    ```json
    {
      "main": "app.js",
      "scripts": {
        "start": "node app.js"
      }
    }
    ```

1. Install the `@azure/cosmos` package from Node Package Manager (npm).

    ```bash
    npm install --save @azure/cosmos
    ```

    > [!IMPORTANT]
    > The bulk execution feature is available in versions 4.3 or later of the `@azure/cosmos` library in the Azure SDK for JavaScript. If you're using an older version of the SDK, you must migrate to a newer version to use these features.

## Configure your connection and resources

Now, use the installed package to configure your connection to an existing Azure Cosmos DB for NoSQL account.

1. Import the `CosmosClient` type and the `BulkOperationType` and `PatchOperationType` supporting types.

    ```javascript
    const { BulkOperationType, PatchOperationType, CosmosClient } = require('@azure/cosmos');
    ```

1. Create a new instance of the `CosmosClient` class passing in the appropriate credentials for your account.

    ```javascript
    const client = new CosmosClient({
        endpoint: '<azure-cosmos-db-nosql-account-endpoint>',
        credential
    });
    ```

1. Create constants for pointers to your existing database and container resources.

    ```javascript
    const database = client.database('<database-name>');

    const container = database.container('<container-name>');
    ```    

## Create a multi-upsert operation in bulk

Start by performing a bulk operation that upserts two items. Both items are composed in an array of `OperationInput` items. `Upsert` and `Create` operations must include, at a minimum, the unique identifier (`id`) and **partition key** fields.

> [!NOTE]
> In this example, the partition key is the `/category` field.

1. Create two constants for items to upsert into the container.

    ```javascript
    const yambdaSurfboard = {
        id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        category: 'gear-surf-surfboards',
        name: 'Yamba Surfboard',
        quantity: 12,
        price: 850.0,
        clearance: false
    };

    const kiamaClassicSurfboard = {
        id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        category: 'gear-surf-surfboards',
        name: 'Kiama Classic Surfboard',
        quantity: 25,
        price: 790.0,
        clearance: true
    };
    ```

1. Create an array of operations using the `Upsert` operation for both items. Explicitly specify the `partitionKey` property and the item itself in the `resourceBody` property.

    ```javascript
    const upsertOperations = [
        {
            operationType: BulkOperationType.Upsert,
            partitionKey: 'gear-surf-surfboards',
            resourceBody: yambdaSurfboard
        },
        {
            operationType: BulkOperationType.Upsert,
            partitionKey: 'gear-surf-surfboards',
            resourceBody: kiamaClassicSurfboard
        }
    ];
    ```


## Parse the bulk operation response

Run and then review the response from the bulk operation. The response contains metadata about each operation.

1. Perform the operations in bulk using the `executeBulkOperations` method of the `items` property of your container.

    ```javascript
    const response = await container.items.executeBulkOperations(upsertOperations);
    
    console.log(response);
    ```

1. Parse the response object. The response contains a status code and `response` object for successful operations. Failed operations include an `error` object instead.

    ```bash
    npm run start
    ```
 
    > [!NOTE]
    > To minimize the size of the response payload, set `contentResponseOnWriteEnabled` to `false`. This flag is specific to bulk and batch features in the SDK.
    
    ```json
    [
      {
        operationInput: {
          operationType: 'Upsert',
          id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
          partitionKey: 'gear-surf-surfboards',
          resourceBody: { ... }
        },
        response: {
          statusCode: 201,
          eTag: '...',
          activityId: '...',
          requestCharge: 7.23,
          resourceBody: { ... },
          diagnostics: { ... },
          headers: { ... }
        }
      },
      ...
    ]
    ```    

## Perform more bulk operations

Optionally, you can perform other operations including `Read`, `Delete`, and `Patch`. All the operations used in this section must include the partition key field.

> [!TIP]
> The `Create` and `Upsert` operations require both the `id` and **partition key** fields. The remaining operations, `Read`, `Delete`, `Replace`, and `Patch` only require the **partition key** field. If the required fields aren't specified, the operation fails.

```javascript
const variousOperations = [
    {
        operationType: BulkOperationType.Read,
        id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        partitionKey: 'gear-surf-surfboards',
    },
    {
        operationType: BulkOperationType.Delete,
        id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        partitionKey: 'gear-surf-surfboards',
    },
    {
        operationType: BulkOperationType.Patch,
        id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        partitionKey: 'gear-surf-surfboards',
        resourceBody: {
            operations: [
                {
                    op: PatchOperationType.add,
                    path: '/onSale',
                    value: true
                }
            ],
        },
    }
]

const response = await container.items.executeBulkOperations(upsertOperations);
```

## Related content

- [Review Azure SDK for JavaScript best practices with Azure Cosmos DB for NoSQL](best-practices-javascript.md)
- [Deploy a JavaScript web application template](quickstart-nodejs.md?pivots=programming-language-js)
