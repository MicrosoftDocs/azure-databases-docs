---
title: Quickstart - Rust driver
description: Learn how to use Azure DocumentDB (with MongoDB compatibility) to build NoSQL solutions using Rust. Start building applications today!
author: seesharprun
ms.author: sidandrews
ms.topic: quickstart-sdk
ms.devlang: rust
ms.date: 10/14/2025
ms.custom:
  - sfi-ropc-nochange
ai-usage: ai-generated
---

# Quickstart: Use Azure DocumentDB with MongoDB driver for Rust

[!INCLUDE[Developer Quickstart selector](includes/selector-quickstart-dev.md)]

In this quickstart, you create a basic Azure DocumentDB application using Rust. Azure DocumentDB is a NoSQL data store that allows applications to store documents in the cloud and access them using official MongoDB drivers. This guide shows how to create documents and perform basic tasks in your Azure DocumentDB cluster using Rust.

[API reference](https://docs.rs/mongodb/latest/mongodb/) | [Source code](https://github.com/mongodb/mongo-rust-driver) | [Package (crates.io)](https://crates.io/crates/mongodb)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prerequisite-quickstart-dev.md)]

- Rust 1.70 or later

## Create an Azure DocumentDB cluster

[!INCLUDE[Section - Create cluster](includes/section-create-cluster.md)]

## Get cluster credentials

[!INCLUDE[Section - Get credentials](includes/section-get-credentials.md)]

## Initialize the project

Create a new Rust project in your current directory.

1. Start in an empty directory.

1. Open a terminal in the current directory.

1. Create a new Rust project using Cargo.

    ```console
    cargo new azure-documentdb-rust-quickstart
    cd azure-documentdb-rust-quickstart
    ```

### Install the client library

The client library is available through crates.io, as the `mongodb` crate.

1. Add the MongoDB Rust driver using Cargo.

    ```console
    cargo add mongodb
    ```

1. Add the `tokio` runtime for async operations.

    ```console
    cargo add tokio --features full
    ```

1. Add the `serde` crate for serialization support.

    ```console
    cargo add serde --features derive
    ```

1. Add the `futures` crate for async stream operations.

    ```console
    cargo add futures
    ```

1. Open the **src/main.rs** file for your application code.

1. Import the required modules into your application code:

    ```rust
    use futures::TryStreamExt;
    use mongodb::{
        bson::doc,
        options::ClientOptions,
        Client, Collection,
    };
    use serde::{Deserialize, Serialize};
    ```

## Object model

| Name | Description |
| --- | --- |
| `Client` | Type used to connect to MongoDB. |
| `Database` | Represents a database in the cluster. |
| `Collection<T>` | Represents a collection within a database in the cluster. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Retrieve a document](#retrieve-a-document)
- [Query documents](#query-documents)

The code in this application connects to a database named `adventureworks` and a collection named `products`. The `products` collection contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The code samples here perform the most common operations when working with a collection.

### Authenticate the client

First, connect to the client using a basic connection string.

1. Create the main async function and set up the connection string. Replace `<your-cluster-name>`, `<your-username>`, and `<your-password>` with your actual cluster information.

    ```rust
    #[tokio::main]
    async fn main() -> Result<(), Box<dyn std::error::Error>> {
        // Connection string for Azure DocumentDB cluster
        let connection_string = "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000";

        // Parse connection string into client options
        let client_options = ClientOptions::parse(connection_string).await?;
    ```

1. Create the MongoDB client and verify the connection.

    ```rust
        // Create a new client and connect to the server
        let client = Client::with_options(client_options)?;

        // Ping the server to verify connection
        client
            .database("admin")
            .run_command(doc! { "ping": 1 })
            .await?;

        println!("Successfully connected and pinged Azure DocumentDB");
    ```

### Get a collection

Now, get your database and collection. If the database and collection doesn't already exist, use the driver to create it for you automatically.

1. Get a reference to the database.

    ```rust
        // Get database reference
        let database = client.database("adventureworks");
        println!("Connected to database: {}", database.name());
    ```

1. Get a reference to the collection within the database.

    ```rust
        // Get collection reference
        let collection: Collection<Product> = database.collection("products");
        println!("Connected to collection: products");
    ```

### Create a document

Then, create a couple of new documents within your collection. Upsert the documents to ensure that it replaces any existing documents if they already exist with the same unique identifier.

1. Define a Product struct and create sample product documents.

    ```rust
        // Define Product struct for type-safe operations
        #[derive(Debug, Serialize, Deserialize)]
        struct Product {
            #[serde(rename = "_id")]
            id: String,
            name: String,
            category: String,
            quantity: i32,
            price: f64,
            sale: bool,
        }

        // Create sample products
        let products = vec![
            Product {
                id: "00000000-0000-0000-0000-000000004018".to_string(),
                name: "Windry Mittens".to_string(),
                category: "apparel-accessories-gloves-and-mittens".to_string(),
                quantity: 121,
                price: 35.00,
                sale: false,
            },
            Product {
                id: "00000000-0000-0000-0000-000000004318".to_string(),
                name: "Niborio Tent".to_string(),
                category: "gear-camp-tents".to_string(),
                quantity: 140,
                price: 420.00,
                sale: true,
            },
        ];
    ```

1. Insert the documents using upsert operations.

    ```rust
        // Insert documents with upsert
        for product in &products {
            let filter = doc! { "_id": &product.id };
            let update = doc! { "$set": mongodb::bson::to_document(product)? };

            let result = collection
                .update_one(filter, update)
                .upsert(true)
                .await?;

            if result.upserted_id.is_some() {
                println!("Inserted document with ID: {}", product.id);
            } else {
                println!("Updated document with ID: {}", product.id);
            }
        }
    ```

### Retrieve a document

Next, perform a point read operation to retrieve a specific document from your collection.

1. Define the filter to find a specific document by ID.

    ```rust
        // Retrieve a specific document by ID
        let filter = doc! { "_id": "00000000-0000-0000-0000-000000004018" };
    ```

1. Execute the query and retrieve the result.

    ```rust
        let retrieved_product = collection.find_one(filter).await?;

        match retrieved_product {
            Some(product) => println!("Retrieved product: {} - ${:.2}", product.name, product.price),
            None => println!("Product not found"),
        }
    ```

### Query documents

Finally, query multiple documents using the MongoDB Query Language (MQL).

1. Define a query to find documents matching specific criteria.

    ```rust
        // Query for products on sale
        let query_filter = doc! { "sale": true };
        let mut cursor = collection.find(query_filter).await?;
    ```

1. Iterate through the cursor to retrieve all matching documents.

    ```rust
        println!("Products on sale:");
        while let Some(product) = cursor.try_next().await? {
            println!(
                "- {}: ${:.2} (Category: {})",
                product.name, product.price, product.category
            );
        }

        Ok(())
    }
    ```

## Explore your data using Visual Studio Code

[!INCLUDE[Section - Visual Studio Code extension](includes/section-quickstart-visual-studio-code-extension.md)]

## Clean up resources

[!INCLUDE[Section - Delete cluster](includes/section-delete-cluster.md)]

## Related content

- [What is Azure DocumentDB?](overview.md)
