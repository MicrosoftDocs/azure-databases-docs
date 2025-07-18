---
title: 'Quickstart: Node.js library'
titleSuffix: Azure Cosmos DB for Apache Gremlin
description: Create a new Azure Cosmos DB for Apache Gremlin account and connect using the Node.js library, JavaScript, and TypeScript in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.topic: quickstart-sdk
ms.devlang: typescript
ms.custom: devx-track-js, devx-track-ts, sfi-ropc-nochange
ms.date: 07/21/2025
ai-usage: ai-generated
zone_pivot_groups: azure-devlang-nodejs
---

# Quickstart: Azure Cosmos DB for Apache Gremlin client library for Node.js

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

Get started with the Azure Cosmos DB for Apache Gremlin client library for Node.js to store, manage, and query unstructured data. Follow the steps in this guide to create a new account, install a Node.js client library, connect to the account, perform common operations, and query your final sample data.

[Library source code](https://github.com/apache/tinkerpop/tree/master/gremlin-javascript/src/main/javascript/gremlin-javascript) | [Package (npm)](https://www.npmjs.com/package/gremlin)

## Prerequisites

[!INCLUDE[Prerequisites - Quickstart developer](../includes/prerequisites-quickstart-developer.md)]

- Node.js 22 or newer

## Setting up

First, set up the account and development environment for this guide. This section walks you through the process of creating an account, getting its credentials, and then preparing your development environment.

### Create an account

[!INCLUDE[Section - Setting up](includes/section-quickstart-provision.md)]

### Get credentials

[!INCLUDE[Section - Get credentials](includes/section-quickstart-credentials.md)]

### Prepare development environment

Then, configure your development environment with a new project and the client library. This step is the last required prerequisite before moving on to the rest of this guide.

::: zone pivot="programming-language-js"

1. Start in an empty folder.

1. Initialize a new module.

    ```bash
    npm init es6 --yes
    ```


1. Install the `gremlin` package from Node Package Manager (npm).

    ```bash
    npm install --save gremlin
    ```

1. Create the *index.js* file.

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

1. Install the `gremlin` package from npm.

    ```bash
    npm install --save gremlin 
    ```

1. Initialize the TypeScript project using the compiler (`tsc`).

    ```bash
    npx tsc --init --target es2017 --module es2022 --moduleResolution nodenext
    ```

1. Create the *index.ts* file.

:::zone-end

## Object model

| | Description |
| --- | --- |
| **`DriverRemoteConnection`** | Represents the connection to the Gremlin server |
| **`GraphTraversalSource`** | Used to construct and execute Gremlin traversals |

## Code examples

- [Authenticate client](#authenticate-client)
- [Upsert data](#upsert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

:::zone pivot="programming-language-js"

1. Open the *index.js* file in your integrated development environment (IDE).

1. Import the `gremlin` package and required types:

    ```javascript
    import gremlin from 'gremlin';
    const { DriverRemoteConnection } = gremlin.driver;
    const { Graph } = gremlin.structure;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname`, `primaryKey`, `database`, and `collection`.

    ```javascript
    const hostname = '<endpoint>';
    const primaryKey = '<key>';
    ```

1. Create a Gremlin connection and traversal source using the credentials and configuration variables created in the previous steps.

    ```javascript
    const authenticator = new gremlin.driver.auth.PlainTextSaslAuthenticator(
        '/dbs/cosmicworks/colls/product',
        primaryKey
    );
    const connection = new DriverRemoteConnection(
        `wss://${hostname}:443/gremlin`,
        { authenticator, traversalsource: 'g', rejectUnauthorized: true }
    );
    const graph = new Graph();
    const g = graph.traversal().withRemote(connection);
    ```

:::zone-end


:::zone pivot="programming-language-ts"

1. Open the *index.ts* file in your integrated development environment (IDE).

1. Import the `gremlin` package and required types:

    ```typescript
    import gremlin from 'gremlin';
    const { DriverRemoteConnection } = gremlin.driver;
    const { Graph } = gremlin.structure;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname`, `primaryKey`, `database`, and `collection`.

    ```typescript
    const hostname: string = '<endpoint>';
    const primaryKey: string = '<key>';
    ```

1. Create a Gremlin connection and traversal source using the credentials and configuration variables created in the previous steps.

    ```typescript
    const authenticator = new gremlin.driver.auth.PlainTextSaslAuthenticator(
        '/dbs/cosmicworks/colls/product',
        primaryKey
    );
    const connection = new DriverRemoteConnection(
        `wss://${hostname}:443/gremlin`,
        { authenticator, traversalsource: 'g', rejectUnauthorized: true }
    );
    const graph = new Graph();
    const g = graph.traversal().withRemote(connection);
    ```

:::zone-end


### Upsert data

Next, upsert new data into the graph. Upserting ensures that the data is created or replaced appropriately depending on whether the same data already exists in the graph.

:::zone pivot="programming-language-js"

1. Add a vertex (upsert data) for a product:

    ```javascript
    await g.addV('product')
        .property('id', 'surfboard1')
        .property('name', 'Kiama classic surfboard')
        .property('category', 'surf')
        .property('price', 699.99)
        .next();
    ```

1. Add another product vertex:

    ```javascript
    await g.addV('product')
        .property('id', 'surfboard2')
        .property('name', 'Montau Turtle Surfboard')
        .property('category', 'surf')
        .property('price', 799.99)
        .next();
    ```

1. Create an edge between the two products:

    ```javascript
    await g.V('surfboard2').addE('replaces').to(g.V('surfboard1')).next();
    ```

:::zone-end


:::zone pivot="programming-language-ts"

1. Add a vertex (upsert data) for a product:

    ```typescript
    await g.addV('product')
        .property('id', 'surfboard1')
        .property('name', 'Kiama classic surfboard')
        .property('category', 'surf')
        .property('price', 699.99)
        .next();
    ```

1. Add another product vertex:

    ```typescript
    await g.addV('product')
        .property('id', 'surfboard2')
        .property('name', 'Montau Turtle Surfboard')
        .property('category', 'surf')
        .property('price', 799.99)
        .next();
    ```

1. Create an edge between the two products:

    ```typescript
    await g.V('surfboard2').addE('replaces').to(g.V('surfboard1')).next();
    ```

:::zone-end


### Read data

Then, read data that was previously upserted into the graph.

:::zone pivot="programming-language-js"

1. Read a vertex by ID:

    ```javascript
    const result = await g.V('surfboard1').next();
    console.log(result.value);
    ```

1. Read all vertices:

    ```javascript
    const allVertices = await g.V().toList();
    allVertices.forEach(item => console.log(item));
    ```

:::zone-end


:::zone pivot="programming-language-ts"

1. Read a vertex by ID:

    ```typescript
    const result = await g.V('surfboard1').next();
    console.log(result.value);
    ```

1. Read all vertices:

    ```typescript
    const allVertices = await g.V().toList();
    allVertices.forEach(item => console.log(item));
    ```

:::zone-end


### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

:::zone pivot="programming-language-js"

1. Query for all products in the 'surf' category:

    ```javascript
    const surfProducts = await g.V().hasLabel('product').has('category', 'surf').toList();
    surfProducts.forEach(item => console.log(item));
    ```

1. Query for all products that replace another product:

    ```javascript
    const replaces = await g.V().hasLabel('product').outE('replaces').inV().toList();
    replaces.forEach(item => console.log(item));
    ```

:::zone-end


:::zone pivot="programming-language-ts"

1. Query for all products in the 'surf' category:

    ```typescript
    const surfProducts = await g.V().hasLabel('product').has('category', 'surf').toList();
    surfProducts.forEach(item => console.log(item));
    ```

1. Query for all products that replace another product:

    ```typescript
    const replaces = await g.V().hasLabel('product').outE('replaces').inV().toList();
    replaces.forEach(item => console.log(item));
    ```

:::zone-end

## Run the code

Run the newly created application using a terminal in your application directory.

:::zone pivot="programming-language-js"

```bash
node index.js
```

:::zone-end

:::zone pivot="programming-language-ts"

```bash
npx tsx index.ts
```

:::zone-end

## Clean up resources

[!INCLUDE[Section - Quickstart cleanup](includes/section-quickstart-cleanup.md)]

## Next step

> [!div class="nextstepaction"]
> [Overview of Azure Cosmos DB for Apache Gremlin](introduction.md)
