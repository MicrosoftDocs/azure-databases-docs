---
title: Quickstart - Node.js driver
description: Learn how to use Azure DocumentDB (with MongoDB compatibility) to build NoSQL solutions using Node.js and TypeScript or JavaScript. Start building applications today!
author: seesharprun
ms.author: sidandrews
ms.topic: quickstart-sdk
ms.devlang: typescript
ms.date: 10/14/2025
ms.custom:
  - sfi-ropc-nochange
defaultDevLang: typescript
dev_langs:
  - typescript
  - javascript
ai-usage: ai-generated
---

# Quickstart: Use Azure DocumentDB with MongoDB driver for Node.js

[!INCLUDE[Developer Quickstart selector](includes/selector-quickstart-dev.md)]

In this quickstart, you create a basic Azure DocumentDB application using Node.js. Azure DocumentDB is a NoSQL data store that allows applications to store documents in the cloud and access them using official MongoDB drivers. This guide shows how to create documents and perform basic tasks in your Azure DocumentDB cluster using Node.js.

[API reference](https://www.mongodb.com/docs/drivers/node/current/) | [Source code](https://github.com/mongodb/node-mongodb-native) | [Package (npm)](https://www.npmjs.com/package/mongodb)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prerequisite-quickstart-dev.md)]

- Node.js 22 or newer

## Create an Azure DocumentDB cluster

[!INCLUDE[Section - Create cluster](includes/section-create-cluster.md)]

## Get cluster credentials

[!INCLUDE[Section - Get credentials](includes/section-get-credentials.md)]

## Initialize the project

Create a new Node.js project in your current directory.

1. Start in an empty directory.

1. Open a terminal in the current directory.

1. Initialize a Node.js project.

    ```console
    npm init -y
    ```

1. Install TypeScript and initialize TypeScript configuration (optional for TypeScript support).

    ```console
    npm install -D typescript @types/node
    npx tsc --init
    ```

### Install the client library

The client library is available through npm, as the `mongodb` package.

1. Install the MongoDB Node.js driver using npm.

    ```console
    npm install mongodb
    ```

1. Open and review the **package.json** file to validate that the package entry exists.

1. Import the required modules into your application code:

    ```typescript
    import { MongoClient, Db, Collection, Document } from 'mongodb';
    ```

    ```javascript
    const { MongoClient } = require('mongodb');
    ```

## Object model

| Name | Description |
| --- | --- |
| `MongoClient` | Type used to connect to MongoDB. |
| `Db` | Represents a database in the cluster. |
| `Collection<Document>` | Represents a collection within a database in the cluster. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Retrieve a document](#retrieve-a-document)
- [Query documents](#query-documents)

The code in this application connects to a database named `adventureworks` and a collection named `products`. The `products` collection contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The code samples here perform the most common operations when working with a collection.

### Authenticate the client

First, connect to the client using a basic connection string.

1. Create the main function and set up the connection string. Replace `<your-cluster-name>`, `<your-username>`, and `<your-password>` with your actual cluster information.

    ```typescript
    async function main(): Promise<void> {
        // Connection string for Azure DocumentDB cluster
        const connectionString = "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000";
        
        // Create a new client and connect to the server
        const client = new MongoClient(connectionString);
    ```

    ```javascript
    async function main() {
        // Connection string for Azure DocumentDB cluster
        const connectionString = "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000";
        
        // Create a new client and connect to the server
        const client = new MongoClient(connectionString);
    ```
    
1. Connect to the MongoDB client and verify the connection.

    ```typescript
        try {
            // Connect to the MongoDB cluster
            await client.connect();
            
            // Ping the server to verify connection
            await client.db("admin").command({ ping: 1 });
            console.log("Successfully connected and pinged Azure DocumentDB");
    ```

    ```javascript
        try {
            // Connect to the MongoDB cluster
            await client.connect();
            
            // Ping the server to verify connection
            await client.db("admin").command({ ping: 1 });
            console.log("Successfully connected and pinged Azure DocumentDB");
    ```

### Get a collection

Now, get your database and collection. If the database and collection doesn't already exist, use the driver to create it for you automatically.

1. Get a reference to the database.

    ```typescript
            // Get database reference
            const database: Db = client.db("adventureworks");
            console.log(`Connected to database: ${database.databaseName}`);
    ```

    ```javascript
            // Get database reference
            const database = client.db("adventureworks");
            console.log(`Connected to database: ${database.databaseName}`);
    ```
    
1. Get a reference to the collection within the database.

    ```typescript
            // Get collection reference
            const collection: Collection<Document> = database.collection("products");
            console.log("Connected to collection: products");
    ```

    ```javascript
            // Get collection reference
            const collection = database.collection("products");
            console.log("Connected to collection: products");
    ```

### Create a document

Then, create a couple of new documents within your collection. Upsert the documents to ensure that it replaces any existing documents if they already exist with the same unique identifier.

1. Create sample product documents.

    ```typescript
            // Create sample products
            interface Product {
                _id: string;
                name: string;
                category: string;
                quantity: number;
                price: number;
                sale: boolean;
            }

            const products: Product[] = [
                {
                    _id: "00000000-0000-0000-0000-000000004018",
                    name: "Windry Mittens",
                    category: "apparel-accessories-gloves-and-mittens",
                    quantity: 121,
                    price: 35.00,
                    sale: false,
                },
                {
                    _id: "00000000-0000-0000-0000-000000004318",
                    name: "Niborio Tent",
                    category: "gear-camp-tents",
                    quantity: 140,
                    price: 420.00,
                    sale: true,
                }
            ];
    ```

    ```javascript
            // Create sample products
            const products = [
                {
                    _id: "00000000-0000-0000-0000-000000004018",
                    name: "Windry Mittens",
                    category: "apparel-accessories-gloves-and-mittens",
                    quantity: 121,
                    price: 35.00,
                    sale: false,
                },
                {
                    _id: "00000000-0000-0000-0000-000000004318",
                    name: "Niborio Tent",
                    category: "gear-camp-tents",
                    quantity: 140,
                    price: 420.00,
                    sale: true,
                }
            ];
    ```
    
1. Insert the documents using upsert operations.

    ```typescript
            // Insert documents with upsert
            for (const product of products) {
                const filter = { _id: product._id };
                const options = { upsert: true };
                
                await collection.replaceOne(filter, product, options);
                console.log(`Upserted product: ${product.name}`);
            }
    ```

    ```javascript
            // Insert documents with upsert
            for (const product of products) {
                const filter = { _id: product._id };
                const options = { upsert: true };
                
                await collection.replaceOne(filter, product, options);
                console.log(`Upserted product: ${product.name}`);
            }
    ```

### Retrieve a document

Next, perform a point read operation to retrieve a specific document from your collection.

1. Define the filter to find a specific document by ID.

    ```typescript
            // Retrieve a specific document by ID
            const filter = { _id: "00000000-0000-0000-0000-000000004018" };
    ```

    ```javascript
            // Retrieve a specific document by ID
            const filter = { _id: "00000000-0000-0000-0000-000000004018" };
    ```
    
1. Execute the query and retrieve the result.

    ```typescript
            const retrievedProduct = await collection.findOne(filter);
            
            if (retrievedProduct) {
                console.log(`Retrieved product: ${retrievedProduct.name} - $${retrievedProduct.price}`);
            } else {
                console.log("Product not found");
            }
    ```

    ```javascript
            const retrievedProduct = await collection.findOne(filter);
            
            if (retrievedProduct) {
                console.log(`Retrieved product: ${retrievedProduct.name} - $${retrievedProduct.price}`);
            } else {
                console.log("Product not found");
            }
    ```

### Query documents

Finally, query multiple documents using the MongoDB Query Language (MQL).

1. Define a query to find documents matching specific criteria.

    ```typescript
            // Query for products on sale
            const saleFilter = { sale: true };
            const saleProducts = await collection.find(saleFilter).toArray();
    ```

    ```javascript
            // Query for products on sale
            const saleFilter = { sale: true };
            const saleProducts = await collection.find(saleFilter).toArray();
    ```
    
1. Iterate through the results to display the matching documents.

    ```typescript
            console.log("Products on sale:");
            for (const product of saleProducts) {
                console.log(`- ${product.name}: $${product.price.toFixed(2)} (Category: ${product.category})`);
            }
            
        } catch (error) {
            console.error("An error occurred:", error);
        } finally {
            await client.close();
        }
    }

    main().catch(console.error);
    ```

    ```javascript
            console.log("Products on sale:");
            for (const product of saleProducts) {
                console.log(`- ${product.name}: $${product.price.toFixed(2)} (Category: ${product.category})`);
            }
            
        } catch (error) {
            console.error("An error occurred:", error);
        } finally {
            await client.close();
        }
    }

    main().catch(console.error);
    ```

## Explore your data using Visual Studio Code

[!INCLUDE[Section - Visual Studio Code extension](includes/section-quickstart-visual-studio-code-extension.md)]

## Clean up resources

[!INCLUDE[Section - Delete cluster](includes/section-delete-cluster.md)]

## Related content

- [What is Azure DocumentDB?](overview.md)


