---
title: Quickstart - Go driver
description: Learn how to use Azure DocumentDB (with MongoDB compatibility) to build NoSQL solutions using Go. Start building applications today!
author: seesharprun
ms.author: sidandrews
ms.topic: quickstart-sdk
ms.devlang: golang
ms.date: 10/14/2025
ms.custom:
  - sfi-ropc-nochange
ai-usage: ai-generated
---

# Quickstart: Use Azure DocumentDB with MongoDB driver for Go

[!INCLUDE[Developer Quickstart selector](includes/selector-quickstart-dev.md)]

In this quickstart, you create a basic Azure DocumentDB application using Go. Azure DocumentDB is a NoSQL data store that allows applications to store documents in the cloud and access them using official MongoDB drivers. This guide shows how to create documents and perform basic tasks in your Azure DocumentDB cluster using Go.

[API reference](https://www.mongodb.com/docs/drivers/go/current/) | [Source code](https://github.com/mongodb/mongo-go-driver) | [Package (Go)](https://pkg.go.dev/go.mongodb.org/mongo-driver)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prerequisite-quickstart-dev.md)]

- Golang 1.18 or later

## Create an Azure DocumentDB cluster

[!INCLUDE[Section - Create cluster](includes/section-create-cluster.md)]

## Get cluster credentials

[!INCLUDE[Section - Get credentials](includes/section-get-credentials.md)]

## Initialize the project

Create a new Go module in your current directory.

1. Start in an empty directory.

1. Open a terminal in the current directory.

1. Initialize a new Go module.

    ```console
    go mod init azure-documentdb-go-quickstart
    ```

### Install the client library

The client library is available through Go, as the `go.mongodb.org/mongo-driver/v2/mongo` module.

1. Install the MongoDB Go driver using `go get`.

    ```console
    go get go.mongodb.org/mongo-driver/v2/mongo
    ```

1. Create a new Go file named `main.go` for your application code.

1. Import the required packages into your application code:

    ```go
    import (
        "context"
        "fmt"
        "log"
        "time"
    
        "go.mongodb.org/mongo-driver/v2/bson"
        "go.mongodb.org/mongo-driver/v2/mongo"
        "go.mongodb.org/mongo-driver/v2/mongo/options"
    )
    ```

## Object model

| Name | Description |
| --- | --- |
| `mongo.Client` | Type used to connect to MongoDB. |
| `mongo.Database` | Represents a database in the cluster. |
| `mongo.Collection` | Represents a collection within a database in the cluster. |

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

    ```go
    func main() {
        // Connection string for Azure DocumentDB cluster
        connectionString := "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
        
        // Create client options
        clientOptions := options.Client().ApplyURI(connectionString)
    ```
    
1. Connect to the MongoDB client and verify the connection.

    ```go
        // Create a new client and connect to the server
        ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
        defer cancel()
        
        client, err := mongo.Connect(ctx, clientOptions)
        if err != nil {
            log.Fatal(err)
        }
        defer client.Disconnect(ctx)
        
        // Ping the primary
        err = client.Ping(ctx, nil)
        if err != nil {
            log.Fatal(err)
        }
        
        fmt.Println("Successfully connected and pinged Azure DocumentDB")
    ```

### Get a collection

Now, get your database and collection. If the database and collection doesn't already exist, use the driver to create it for you automatically.

1. Get a reference to the database.

    ```go
        // Get database reference
        database := client.Database("adventureworks")
        fmt.Println("Connected to database:", database.Name())
    ```
    
1. Get a reference to the collection within the database.

    ```go
        // Get collection reference
        collection := database.Collection("products")
        fmt.Println("Connected to collection:", collection.Name())
    ```

### Create a document

Then, create a couple of new documents within your collection. Upsert the documents to ensure that it replaces any existing documents if they already exist with the same unique identifier.

1. Define a product type and create sample product documents.

    ```go
        type Product struct {
            ID       string  `bson:"_id,omitempty"`
            Name     string  `bson:"name"`
            Category string  `bson:"category"`
            Quantity int     `bson:"quantity"`
            Price    float64 `bson:"price"`
            Sale     bool    `bson:"sale"`
        }
        
        // Create sample products
        products := []Product{
            {
                ID:       "00000000-0000-0000-0000-000000004018",
                Name:     "Windry Mittens",
                Category: "apparel-accessories-gloves-and-mittens",
                Quantity: 121,
                Price:    35.00,
                Sale:     false,
            },
            {
                ID:       "00000000-0000-0000-0000-000000004318",
                Name:     "Niborio Tent",
                Category: "gear-camp-tents",
                Quantity: 140,
                Price:    420.00,
                Sale:     true,
            },
        }
    ```
    
1. Insert the documents using upsert operations.

    ```go
        // Insert documents with upsert
        for _, product := range products {
            filter := bson.M{"_id": product.ID}
            update := bson.M{"$set": product}
            opts := options.Update().SetUpsert(true)
            
            result, err := collection.UpdateOne(ctx, filter, update, opts)
            if err != nil {
                log.Fatal(err)
            }
            
            if result.UpsertedID != nil {
                fmt.Printf("Inserted document with ID: %v\n", result.UpsertedID)
            } else {
                fmt.Printf("Updated document with ID: %s\n", product.ID)
            }
        }
    ```

### Retrieve a document

Next, perform a point read operation to retrieve a specific document from your collection.

1. Define the filter to find a specific document by ID.

    ```go
        // Retrieve a specific document by ID
        filter := bson.M{"_id": "00000000-0000-0000-0000-000000004018"}
        var retrievedProduct Product
    ```
    
1. Execute the query and decode the result.

    ```go
        err = collection.FindOne(ctx, filter).Decode(&retrievedProduct)
        if err != nil {
            log.Fatal(err)
        }
        
        fmt.Printf("Retrieved product: %+v\n", retrievedProduct)
    ```

### Query documents

Finally, query multiple documents using the MongoDB Query Language (MQL).

1. Define a query to find documents matching specific criteria.

    ```go
        // Query for products on sale
        queryFilter := bson.M{"sale": true}
        cursor, err := collection.Find(ctx, queryFilter)
        if err != nil {
            log.Fatal(err)
        }
        defer cursor.Close(ctx)
    ```
    
1. Iterate through the cursor to retrieve all matching documents.

    ```go
        fmt.Println("Products on sale:")
        for cursor.Next(ctx) {
            var product Product
            if err := cursor.Decode(&product); err != nil {
                log.Fatal(err)
            }
            fmt.Printf("- %s: $%.2f (Category: %s)\n", product.Name, product.Price, product.Category)
        }
        
        if err := cursor.Err(); err != nil {
            log.Fatal(err)
        }
    }
    ```

## Explore your data using Visual Studio Code

[!INCLUDE[Section - Visual Studio Code extension](includes/section-quickstart-visual-studio-code-extension.md)]

## Clean up resources

[!INCLUDE[Section - Delete cluster](includes/section-delete-cluster.md)]

## Related content

- [What is Azure DocumentDB?](overview.md)
