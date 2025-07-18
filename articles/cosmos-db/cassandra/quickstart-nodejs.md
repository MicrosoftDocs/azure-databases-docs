---
title: 'Quickstart: Node.js & TypeScript library'
titleSuffix: Azure Cosmos DB for Apache Cassandra
description: Create a new Azure Cosmos DB for Apache Cassandra account and connect using the Node.js library and TypeScript in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: quickstart-sdk
ms.devlang: typescript
ms.custom: devx-track-js, devx-track-ts, sfi-ropc-nochange
ms.date: 07/18/2025
zone_pivot_groups: azure-devlang-nodejs
---

# Quickstart: Azure Cosmos DB for Apache Cassandra client library for Node.js

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Cassandra client library for Node.js to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Node.js client library, connect to the account, perform common operations, and query your final sample data.

[API reference documentation](https://docs.datastax.com/en/developer/nodejs-driver/index.html) | [Library source code](https://github.com/datastax/nodejs-driver) | [Package (npm)](https://www.npmjs.com/package/cassandra-driver)

## Prerequisites

[!INCLUDE[Prerequisites - Quickstart developer](../includes/prerequisites-quickstart-developer.md)]

- Node.js 22 or newer

## Setting up

First, set up the account and development environment for this guide. This section walks you through the process of creating an account, getting its credentials, and then preparing your development environment.

### Create an account

[!INCLUDE[Section - Quickstart provision](includes/section-quickstart-provision.md)]

### Get credentials

[!INCLUDE[Section - Quickstart credentials](includes/section-quickstart-credentials.md)]

### Prepare development environment

Then, configure your development environment with a new project and the client library. This step is the last required prerequisite before moving on to the rest of this guide.

::: zone pivot="programming-language-js"

1. Start in an empty folder.

1. Initialize a new module.

    ```bash
    npm init es6 --yes
    ```

1. Install the `cassandra-driver` package from Node Package Manager (npm).

    ```bash
    npm install --save cassandra-driver
    ```

1. Create the **index.js** file.

:::zone-end

::: zone pivot="programming-language-ts"

1. Start in an empty folder.

1. Initialize a new module.

    ```bash
    npm init es6 --yes
    ```

1. Install the `typescript` package from Node Package Manager (npm).

    ```bash
    npm install --save-dev typescript
    ```

1. Install the `tsx` package from npm.

    ```bash
    npm install --save-dev tsx
    ```

1. Install the `cassandra-driver` package from npm.

    ```bash
    npm install --save cassandra-driver
    ```

1. Initialize the TypeScript project using the compiler (`tsc`).

    ```bash
    npx tsc --init --target es2017 --module es2022 --moduleResolution nodenext
    ```

1. Create the **index.ts** file.

:::zone-end

## Object model

| | Description |
| --- | --- |
| **`Client`** | Represents the a specific connection to a cluster |
| **`Mapper`** | Cassandra Query Language (CQL) client used to run queries |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

::: zone pivot="programming-language-js"

1. Open the **index.js** file in your integrated development environment (IDE).

1. Import the following types from the `cassandra-driver` module:

    - `cassandra`
    - `cassandra.Client`
    - `cassandra.mapping.Mapper`
    - `cassandra.auth.PlainTextAuthProvider`

    ```javascript
    import cassandra from 'cassandra-driver';
    
    const { Client } = cassandra;
    const { Mapper } = cassandra.mapping;
    const { PlainTextAuthProvider } = cassandra.auth;
    ```

1. Create string constant variables for the credentials collected earlier in this guide. Name the variables `username`, `password`, and `contactPoint`.

    ```javascript
    const username = '<username>';
    const password = '<password>';
    const contactPoint = '<contact-point>';
    ```

1. Create another string variable for the region where you created your Azure Cosmos DB for Apache Cassandra account. Name this variable `region`.

    ```javascript
    const region = '<azure-region>';
    ```

1. Create a new `PlainTextAuthProvider` object with the credentials specified in the previous steps.

    ```javascript
    let authProvider = new PlainTextAuthProvider(
        username,
        password
    );
    ```

1. Create a `Client` object using the credential and configuration variables created in the previous steps.

    ```javascript
    let client = new Client({
        contactPoints: [`${contactPoint}:10350`],
        authProvider: authProvider,
        localDataCenter: region,
        sslOptions: {
            secureProtocol: 'TLSv1_2_method'
        },
    });
    ```

1. Asynchronously connect to the cluster.

    ```javascript
    await client.connect();
    ```

1. Create a new mapper targeting the `cosmicworks` keyspace and `product` table. Name the mapper `Product`.

    ```javascript
    const mapper = new Mapper(client, {
        models: {
            'Product': {
                tables: ['product'],
                keyspace: 'cosmicworks'
            }
        }
    });
    ```

1. Generate a mapper instance using the `forModel` function and the `Product` mapper name.

    ```javascript
    const productMapper = mapper.forModel('Product');
    ```

:::zone-end

::: zone pivot="programming-language-ts"

1. Open the **index.ts** file in your integrated development environment (IDE).

1. Import the following types from the `cassandra-driver` module:

    - `cassandra.auth`
    - `cassandra.mapping`
    - `cassandra.types`
    - `cassandra.Client`
    - `cassandra.ClientOptions`
    - `cassandra.mapping.Mapper`
    - `cassandra.auth.PlainTextAuthProvider`

    ```typescript
    import { auth, mapping, types, Client, ClientOptions } from 'cassandra-driver';
    
    const { Mapper } = mapping;
    const { PlainTextAuthProvider } = auth;
    ```

1. Create string constant variables for the credentials collected earlier in this guide. Name the variables `username`, `password`, and `contactPoint`.

    ```typescript
    const username: string = '<username>';
    const password: string = '<password>';
    const contactPoint: string = '<contact-point>';
    ```

1. Create another string variable for the region where you created your Azure Cosmos DB for Apache Cassandra account. Name this variable `region`.

    ```typescript
    const region: string = '<azure-region>';
    ```

1. Create a new `PlainTextAuthProvider` object with the credentials specified in the previous steps.

    ```typescript
    let authProvider = new PlainTextAuthProvider(
        username,
        password
    );
    ```

1. Create an anonymous object with options that ensures that you're using the transport layer security (TLS) 1.2 protocol.

    ```typescript
    let sslOptions = {
        secureProtocol: 'TLSv1_2_method'
    };
    ```

1. Create a `ClientOptions` object using the credential and configuration variables created in the previous steps.

    ```typescript
    let clientOptions: ClientOptions = {
        contactPoints: [`${contactPoint}:10350`],
        authProvider: authProvider,
        localDataCenter: region,
        sslOptions: sslOptions
    };
    ```

1. Create a `Client` object using the `clientOptions` variable in the constructor.

    ```typescript
    let client = new Client(clientOptions);
    ```

1. Asynchronously connect to the cluster.

    ```typescript
    await client.connect();
    ```

1. Create a new mapper targeting the `cosmicworks` keyspace and `product` table. Name the mapper `Product`.

    ```typescript
    const mapper = new Mapper( client, {
        models: {
            'Product': {
                tables: ['product'],
                keyspace: 'cosmicworks'
            }
        }
    });
    ```

1. Generate a mapper instance using the `forModel` function and the `Product` mapper name.

    ```typescript
    const productMapper = mapper.forModel('Product');
    ```

:::zone-end

### Upsert data

Next, upsert new data into a table. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the table.

::: zone pivot="programming-language-js"

1. Create a new object in a variable named `product`.

    ```javascript
    const product = {
        id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        name: 'Yamba Surfboard',
        category: 'gear-surf-surfboards',
        quantity: 12,
        price: 850.00,
        clearance: false
    };
    ```

1. Asynchronously invoke the `insert` function passing in the `product` variable created in the previous step.

    ```javascript
    await productMapper.insert(product);
    ```

:::zone-end

::: zone pivot="programming-language-ts"

1. Define a new interface named `Product` with fields corresponding to the table created earlier in this guide.

    | | Type |
    | --- | --- |
    | **`Id`** | `string` |
    | **`Name`** | `string` |
    | **`Category`** | `string` |
    | **`Quantity`** | `int` |
    | **`Price`** | `decimal` |
    | **`Clearance`** | `bool` |

    ```typescript
    interface Product {
        id: string;
        name: string;
        category: string;
        quantity: number;
        price: number;
        clearance: boolean;
    }
    ```

    > [!TIP]
    > In Node.js, you can create this type in another file or create it at the end of the existing file.

1. Create a new object of type `Product`. Store the object in a variable named `product`.

    ```typescript
    const product: Product = {
        id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        name: 'Yamba Surfboard',
        category: 'gear-surf-surfboards',
        quantity: 12,
        price: 850.00,
        clearance: false
    };
    ```

1. Asynchronously invoke the `insert` function passing in the `product` variable created in the previous step.

    ```typescript
    await productMapper.insert(product);
    ```

:::zone-end

### Read data

Then, read data that was previously upserted into the table.

::: zone pivot="programming-language-js"

1. Create an anonymous object named `filter`. In this object, include a property named `id` with the same value as the product created earlier in this guide.

    ```javascript
    const filter = {
        id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb'
    };
    ```

1. Invoke the `get` function of the mapper passing in the `filter` variable. Store the result in a variable named `matchedProduct`.

    ```javascript
    let matchedProduct = await productMapper.get(filter);
    ```

:::zone-end

::: zone pivot="programming-language-ts"

1. Create an anonymous object named `filter`. In this object, include a property named `id` with the same value as the product created earlier in this guide.

    ```typescript
    const filter = {
        id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb'
    };
    ```

1. Invoke the `get` function of the mapper passing in the `filter` variable. Store the result in a variable named `matchedProduct` of type `Product`.

    ```typescript
    let matchedProduct: Product = await productMapper.get(filter);
    ```

:::zone-end

### Query data

Finally, use a query to find all data that matches a specific filter in the table.

::: zone pivot="programming-language-js"

1. Create a new string variable named `query` with a CQL query that matches items with the same `category` field.

    ```javascript
    const query = `
    SELECT
        *
    FROM
        cosmicworks.product
    WHERE
        category = :category ALLOW FILTERING;
    `;
    ```

1. Create an anonymous object named `params`. In this object, include a property named `category` with the same value as the product created earlier in this guide.

    ```javascript
    const params = {
        category: 'gear-surf-surfboards'
    };
    ```

1. Asynchronously invoke the `execute` function passing in both the `query` and `params` variables as arguments. Store the result's `rows` property as a variable named `matchedProducts`.

    ```javascript
    let { rows: matchedProducts } = await client.execute(query, params);
    ```

1. Iterate over the query results by invoking the `foreach` method on the array of products.

    ```javascript
    matchedProducts.forEach(product => {
        // Do something here with each result
    });
    ```

:::zone-end

::: zone pivot="programming-language-ts"

1. Create a new string variable named `query` with a CQL query that matches items with the same `category` field.

    ```typescript
    const query: string = `
    SELECT
        *
    FROM
        cosmicworks.product
    WHERE
        category = :category ALLOW FILTERING;
    `;
    ```

1. Create an anonymous object named `params`. In this object, include a property named `category` with the same value as the product created earlier in this guide.

    ```typescript
    const params = {
        category: 'gear-surf-surfboards'
    };
    ```

1. Asynchronously invoke the `execute` function passing in both the `query` and `params` variables as arguments. Store the result in a variable named `result` of type `types.ResultSet`.

    ```typescript
    let result: types.ResultSet = await client.execute(query, params);
    ```

1. Store the result's `rows` property as a variable named `matchedProducts` of type `Product[]`.

    ```typescript
    let matchedProducts: Product[] = result.rows;
    ```

1. Iterate over the query results by invoking the `foreach` method on the array of products.

    ```typescript
    matchedProducts.forEach((product: Product) => {
        // Do something here with each result
    });
    ```

:::zone-end

## Run the code

Run the newly created application using a terminal in your application directory.

::: zone pivot="programming-language-js"

```bash
node index.js
```

:::zone-end

::: zone pivot="programming-language-ts"

```bash
npx tsx index.ts
```

:::zone-end

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-credentials.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Cassandra](introduction.md)
