---
title: Quickstart - C# driver
description: Learn how to use Azure DocumentDB (with MongoDB compatibility) to build NoSQL solutions using NET/C#. Start building applications today!
author: seesharprun
ms.author: sidandrews
ms.topic: quickstart-sdk
ms.devlang: csharp
ms.date: 10/14/2025
ms.custom:
  - sfi-ropc-nochange
ai-usage: ai-generated
---

# Quickstart: Use Azure DocumentDB with MongoDB driver for C#

[!INCLUDE[Developer Quickstart selector](includes/selector-quickstart-dev.md)]

In this quickstart, you create a basic Azure DocumentDB application using C#. Azure DocumentDB is a NoSQL data store that allows applications to store documents in the cloud and access them using official MongoDB drivers. This guide shows how to create documents and perform basic tasks in your Azure DocumentDB cluster using C#.

[API reference](https://www.mongodb.com/docs/drivers/csharp/current/) | [Source code](https://github.com/mongodb/mongo-csharp-driver) | [Package (NuGet)](https://www.nuget.org/packages/MongoDB.Driver)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prerequisite-quickstart-dev.md)]

- .NET 10.0 or later

## Create an Azure DocumentDB cluster

[!INCLUDE[Section - Create cluster](includes/section-create-cluster.md)]

## Get cluster credentials

[!INCLUDE[Section - Get credentials](includes/section-get-credentials.md)]

## Initialize the project

Create a new .NET console application project in your current directory.

1. Start in an empty directory.

1. Open a terminal in the current directory.

1. Create a new .NET console application.

    ```dotnetcli    
    dotnet new console
    ```

1. Build the project to ensure it was created successfully.

    ```dotnetcli    
    dotnet build
    ```

### Install the client library

The client library is available through NuGet, as the `MongoDB.Driver` package.

1. Install the MongoDB .NET driver using the NuGet package manager.

    ```dotnetcli    
    dotnet add package MongoDB.Driver
    ```

1. Open and review the **azure-documentdb-dotnet-quickstart.csproj** file to validate that the package reference exists.

1. Import the required namespaces into your application code:

    ```csharp
    using System;
    using System.Collections.Generic;
    using System.Threading.Tasks;
    using MongoDB.Bson;
    using MongoDB.Bson.Serialization.Attributes;
    using MongoDB.Driver;
    ```

## Object model

| Name | Description |
| --- | --- |
| `MongoClient` | Type used to connect to MongoDB. |
| `IMongoDatabase` | Represents a database in the cluster. |
| `IMongoCollection<T>` | Represents a collection within a database in the cluster. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Retrieve a document](#retrieve-a-document)
- [Query documents](#query-documents)

The code in this application connects to a database named `adventureworks` and a collection named `products`. The `products` collection contains details such as name, category, quantity, a unique identifier, and a sale flag for each product. The code samples here perform the most common operations when working with a collection.

### Authenticate the client

First, connect to the client using a basic connection string.

1. Create the main method and set up the connection string. Replace `<your-cluster-name>`, `<your-username>`, and `<your-password>` with your actual cluster information.

    ```csharp
    class Program
    {
        static async Task Main(string[] args)
        {
            // Connection string for Azure DocumentDB cluster
            string connectionString = "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000";
            
            // Create MongoDB client settings
            var settings = MongoClientSettings.FromConnectionString(connectionString);
    ```
    
1. Create the MongoDB client and verify the connection.

    ```csharp
            // Create a new client and connect to the server
            var client = new MongoClient(settings);
            
            // Ping the server to verify connection
            var database = client.GetDatabase("admin");
            var pingCommand = new BsonDocument("ping", 1);
            await database.RunCommandAsync<BsonDocument>(pingCommand);
            
            Console.WriteLine("Successfully connected and pinged Azure DocumentDB");
    ```

### Get a collection

Now, get your database and collection. If the database and collection doesn't already exist, use the driver to create it for you automatically.

1. Get a reference to the database.

    ```csharp
            // Get database reference
            var adventureWorksDatabase = client.GetDatabase("adventureworks");
            Console.WriteLine($"Connected to database: {adventureWorksDatabase.DatabaseNamespace.DatabaseName}");
    ```
    
1. Get a reference to the collection within the database.

    ```csharp
            // Get collection reference
            var productsCollection = adventureWorksDatabase.GetCollection<Product>("products");
            Console.WriteLine($"Connected to collection: products");
    ```

### Create a document

Then, create a couple of new documents within your collection. Upsert the documents to ensure that it replaces any existing documents if they already exist with the same unique identifier.

1. Define a Product class and create sample product documents.

    ```csharp
            // Create sample products
            var products = new List<Product>
            {
                new Product
                {
                    Id = "00000000-0000-0000-0000-000000004018",
                    Name = "Windry Mittens",
                    Category = "apparel-accessories-gloves-and-mittens",
                    Quantity = 121,
                    Price = 35.00m,
                    Sale = false
                },
                new Product
                {
                    Id = "00000000-0000-0000-0000-000000004318",
                    Name = "Niborio Tent",
                    Category = "gear-camp-tents",
                    Quantity = 140,
                    Price = 420.00m,
                    Sale = true
                }
            };
    ```
    
1. Insert the documents using upsert operations.

    ```csharp
            // Insert documents with upsert
            foreach (var product in products)
            {
                var filter = Builders<Product>.Filter.Eq(p => p.Id, product.Id);
                var options = new ReplaceOptions { IsUpsert = true };
                
                await productsCollection.ReplaceOneAsync(filter, product, options);
                Console.WriteLine($"Upserted product: {product.Name}");
            }
    ```

1. Add the Product class definition at the end of your Program.cs file.

    ```csharp
    public class Product
    {
        [BsonId]
        [BsonElement("_id")]
        public string Id { get; set; }
        
        [BsonElement("name")]
        public string Name { get; set; }
        
        [BsonElement("category")]
        public string Category { get; set; }
        
        [BsonElement("quantity")]
        public int Quantity { get; set; }
        
        [BsonElement("price")]
        public decimal Price { get; set; }
        
        [BsonElement("sale")]
        public bool Sale { get; set; }
    }
    ```

### Retrieve a document

Next, perform a point read operation to retrieve a specific document from your collection.

1. Define the filter to find a specific document by ID.

    ```csharp
            // Retrieve a specific document by ID
            var filter = Builders<Product>.Filter.Eq(p => p.Id, "00000000-0000-0000-0000-000000004018");
    ```
    
1. Execute the query and retrieve the result.

    ```csharp
            var retrievedProduct = await productsCollection.Find(filter).FirstOrDefaultAsync();
            
            if (retrievedProduct != null)
            {
                Console.WriteLine($"Retrieved product: {retrievedProduct.Name} - ${retrievedProduct.Price}");
            }
            else
            {
                Console.WriteLine("Product not found");
            }
    ```

### Query documents

Finally, query multiple documents using the MongoDB Query Language (MQL).

1. Define a query to find documents matching specific criteria.

    ```csharp
            // Query for products on sale
            var saleFilter = Builders<Product>.Filter.Eq(p => p.Sale, true);
            var saleProducts = await productsCollection.Find(saleFilter).ToListAsync();
    ```
    
1. Iterate through the results to display the matching documents.

    ```csharp
            Console.WriteLine("Products on sale:");
            foreach (var product in saleProducts)
            {
                Console.WriteLine($"- {product.Name}: ${product.Price:F2} (Category: {product.Category})");
            }
        }
    }
    ```

## Explore your data using Visual Studio Code

[!INCLUDE[Section - Visual Studio Code extension](includes/section-quickstart-visual-studio-code-extension.md)]

## Clean up resources

[!INCLUDE[Section - Delete cluster](includes/section-delete-cluster.md)]

## Related content

- [What is Azure DocumentDB?](overview.md)
