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
ms.date: 07/22/2025
ai-usage: ai-generated
zone_pivot_groups: azure-devlang-nodejs
---

# Quickstart: Azure Cosmos DB for Apache Gremlin client library for Node.js

[!INCLUDE[Quickstart developer selector](includes/selector-quickstart-developer.md)]

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

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

1. Install the `@types/node` package from npm.

    ```bash
    npm install --save-dev @types/node
    ```

1. Install the `@types/gremlin` package from npm.

    ```bash
    npm install --save-dev @types/gremlin
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
- [Insert data](#insert-data)
- [Read data](#read-data)
- [Query data](#query-data)

### Authenticate client

Start by authenticating the client using the credentials gathered earlier in this guide.

:::zone pivot="programming-language-js"

1. Open the *index.js* file in your integrated development environment (IDE).

1. Import the `gremlin` package and required types:

    ```javascript
    import gremlin from 'gremlin';
    const { Client, auth } = gremlin.driver;
    const { PlainTextSaslAuthenticator } = auth;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname` and `primaryKey`.

    ```javascript
    const hostname = '<host>';
    const primaryKey = '<key>';
    ```

1. Create an object of type `PlainTextSaslAuthenticator` using the credentials and configuration variables created in the previous steps. Store the object in a variable named `authenticator`.

    ```javascript
    const authenticator = new PlainTextSaslAuthenticator(
        '/dbs/cosmicworks/colls/products',
        primaryKey
    );
    ```

1. Create a `Client` object using the authenticator variable. Name the variable `client`.

    ```javascript
    const client = new Client(
        `wss://${hostname}.gremlin.cosmos.azure.com:443/`,
        {
            authenticator,
            traversalsource: 'g',
            rejectUnauthorized: true,
            mimeType: 'application/vnd.gremlin-v2.0+json'
        }
    );
    ```

:::zone-end

:::zone pivot="programming-language-ts"

1. Open the *index.ts* file in your integrated development environment (IDE).

1. Import the `gremlin` package and required types:

    ```typescript
    import gremlin from 'gremlin';
    const { Client, auth } = gremlin.driver;
    const { PlainTextSaslAuthenticator } = auth;
    ```

1. Create string variables for the credentials collected earlier in this guide. Name the variables `hostname` and `primaryKey`.

    ```typescript
    const hostname: string = '<host>';
    const primaryKey: string = '<key>';
    ```

1. Create an object of type `PlainTextSaslAuthenticator` using the credentials and configuration variables created in the previous steps. Store the object in a variable named `authenticator`.

    ```typescript
    const authenticator = new PlainTextSaslAuthenticator(
        '/dbs/cosmicworks/colls/products',
        primaryKey
    );
    ```

1. Create a `Client` object using the authenticator variable. Name the variable `client`.

    ```typescript
    const client = new Client(
        `wss://${hostname}.gremlin.cosmos.azure.com:443/`,
        {
            authenticator,
            traversalsource: 'g',
            rejectUnauthorized: true,
            mimeType: 'application/vnd.gremlin-v2.0+json'
        }
    );
    ```

:::zone-end

### Insert data

Next, insert new vertex and edge data into the graph. Before creating the new data, clear the graph of any existing data.

:::zone pivot="programming-language-js"

1. Run the `g.V().drop()` query to clear all vertices and edges from the graph.

    ```javascript
    await client.submit('g.V().drop()');
    ```

1. Create a Gremlin query that adds a vertex.

    ```javascript
    const insert_vertex_query = `
        g.addV('product')
            .property('id', prop_id)
            .property('name', prop_name)
            .property('category', prop_category)
            .property('quantity', prop_quantity)
            .property('price', prop_price)
            .property('clearance', prop_clearance)
    `;
    ```

1. Add a vertex for a single product.

    ```javascript
    await client.submit(insert_vertex_query, {
        prop_id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        prop_name: 'Yamba Surfboard',
        prop_category: 'gear-surf-surfboards',
        prop_quantity: 12,
        prop_price: 850.00,
        prop_clearance: false,
    });
    ```

1. Add two more vertices for two extra products.

    ```javascript
    await client.submit(insert_vertex_query, {
        prop_id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        prop_name: 'Montau Turtle Surfboard',
        prop_category: 'gear-surf-surfboards',
        prop_quantity: 5,
        prop_price: 600.00,
        prop_clearance: true,
    });

    await client.submit(insert_vertex_query, {
        prop_id: 'cccccccc-2222-3333-4444-dddddddddddd',
        prop_name: 'Noosa Surfboard',
        prop_category: 'gear-surf-surfboards',
        prop_quantity: 31,
        prop_price: 1100.00,
        prop_clearance: false,
    });
    ```

1. Create another Gremlin query that adds an edge.

    ```javascript
    const insert_edge_query = `
        g.V([prop_partition_key, prop_source_id])
            .addE('replaces')
            .to(g.V([prop_partition_key, prop_target_id]))
    `;
    ```

1. Add two edges.

    ```javascript
    await client.submit(insert_edge_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_source_id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        prop_target_id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    });

    await client.submit(insert_edge_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_source_id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        prop_target_id: 'cccccccc-2222-3333-4444-dddddddddddd',
    });
    ```

:::zone-end

:::zone pivot="programming-language-ts"

1. Run the `g.V().drop()` query to clear all vertices and edges from the graph.

    ```typescript
    await client.submit('g.V().drop()');
    ```

1. Create a Gremlin query that adds a vertex.

    ```typescript
    const insert_vertex_query: string = `
        g.addV('product')
            .property('id', prop_id)
            .property('name', prop_name)
            .property('category', prop_category)
            .property('quantity', prop_quantity)
            .property('price', prop_price)
            .property('clearance', prop_clearance)
    `;
    ```

1. Add a vertex for a single product.

    ```typescript
    await client.submit(insert_vertex_query, {
        prop_id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        prop_name: 'Yamba Surfboard',
        prop_category: 'gear-surf-surfboards',
        prop_quantity: 12,
        prop_price: 850.00,
        prop_clearance: false,
    });
    ```

1. Add two more vertices for two extra products.

    ```typescript
    await client.submit(insert_vertex_query, {
        prop_id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        prop_name: 'Montau Turtle Surfboard',
        prop_category: 'gear-surf-surfboards',
        prop_quantity: 5,
        prop_price: 600.00,
        prop_clearance: true,
    });

    await client.submit(insert_vertex_query, {
        prop_id: 'cccccccc-2222-3333-4444-dddddddddddd',
        prop_name: 'Noosa Surfboard',
        prop_category: 'gear-surf-surfboards',
        prop_quantity: 31,
        prop_price: 1100.00,
        prop_clearance: false,
    });
    ```

1. Create another Gremlin query that adds an edge.

    ```typescript
    const insert_edge_query: string = `
        g.V([prop_partition_key, prop_source_id])
            .addE('replaces')
            .to(g.V([prop_partition_key, prop_target_id]))
    `;
    ```

1. Add two edges.

    ```typescript
    await client.submit(insert_edge_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_source_id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        prop_target_id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    });

    await client.submit(insert_edge_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_source_id: 'bbbbbbbb-1111-2222-3333-cccccccccccc',
        prop_target_id: 'cccccccc-2222-3333-4444-dddddddddddd',
    });
    ```

:::zone-end

### Read data

Then, read data that was previously inserted into the graph.

:::zone pivot="programming-language-js"

1. Create a query that reads a vertex using the unique identifier and partition key value.

    ```javascript
    const read_vertex_query = 'g.V([prop_partition_key, prop_id])';
    ```

1. Then, read a vertex by supplying the required parameters.

    ```javascript
    let read_results = await client.submit(read_vertex_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    });

    let matched_item = read_results._items[0];
    ```

:::zone-end

:::zone pivot="programming-language-ts"

1. Create a query that reads a vertex using the unique identifier and partition key value.

    ```typescript
    const read_vertex_query: string = 'g.V([prop_partition_key, prop_id])';
    ```

1. Then, read a vertex by supplying the required parameters.

    ```typescript
    let read_results = await client.submit(read_vertex_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
    });

    let matched_item = read_results._items[0];
    ```

:::zone-end

### Query data

Finally, use a query to find all data that matches a specific traversal or filter in the graph.

:::zone pivot="programming-language-js"

1. Create a query that finds all vertices that traverse out from a specific vertex.

    ```javascript
    const find_vertices_query = `
        g.V().hasLabel('product')
            .has('category', prop_partition_key)
            .has('name', prop_name)
            .outE('replaces').inV()
    `;
    ```

1. Execute the query specifying the `Montau Turtle Surfboard` product.

    ```javascript
    let find_results = await client.submit(find_vertices_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_name: 'Montau Turtle Surfboard',
    });
    ```

1. Iterate over the query results.

    ```javascript
    for (const item of find_results._items) {
        // Do something here with each result
    }
    ```

:::zone-end

:::zone pivot="programming-language-ts"

1. Create a query that finds all vertices that traverse out from a specific vertex.

    ```typescript
    const find_vertices_query: string = `
        g.V().hasLabel('product')
            .has('category', prop_partition_key)
            .has('name', prop_name)
            .outE('replaces').inV()
    `;
    ```

1. Execute the query specifying the `Montau Turtle Surfboard` product.

    ```typescript
    let find_results = await client.submit(find_vertices_query, {
        prop_partition_key: 'gear-surf-surfboards',
        prop_name: 'Montau Turtle Surfboard',
    });
    ```

1. Iterate over the query results.

    ```typescript
    for (const item of find_results._items) {
        // Do something here with each result
    }
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
