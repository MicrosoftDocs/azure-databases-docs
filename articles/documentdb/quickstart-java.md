---
title: Quickstart - Java driver
description: Learn how to use Azure DocumentDB (with MongoDB compatibility) to build NoSQL solutions using Java. Start building applications today!
author: seesharprun
ms.author: sidandrews
ms.topic: quickstart-sdk
ms.devlang: java
ms.date: 10/14/2025
ms.custom:
  - sfi-ropc-nochange
ai-usage: ai-generated
---

# Quickstart: Use Azure DocumentDB with MongoDB driver for Java

[!INCLUDE[Developer Quickstart selector](includes/selector-quickstart-dev.md)]

In this quickstart, you create a basic Azure DocumentDB application using Java. Azure DocumentDB is a NoSQL data store that allows applications to store documents in the cloud and access them using official MongoDB drivers. This guide shows how to create documents and perform basic tasks in your Azure DocumentDB cluster using Java.

[API reference](https://www.mongodb.com/docs/drivers/java/sync/current/) | [Source code](https://github.com/mongodb/mongo-java-driver) | [Package (Maven)](https://mvnrepository.com/artifact/org.mongodb/mongodb-driver-sync)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prerequisite-quickstart-dev.md)]

- Java 21 or later

## Create an Azure DocumentDB cluster

[!INCLUDE[Section - Create cluster](includes/section-create-cluster.md)]

## Get cluster credentials

[!INCLUDE[Section - Get credentials](includes/section-get-credentials.md)]

## Initialize the project

Create a new Maven project in your current directory.

1. Start in an empty directory.

1. Open a terminal in the current directory.

1. Create a new Maven project using the quickstart archetype.

    ```console
    mvn archetype:generate -DgroupId=com.example -DartifactId=azure-documentdb-java-quickstart -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
    ```

1. Navigate to the generated project directory.

    ```console
    cd azure-documentdb-java-quickstart
    ```

1. Build the project to ensure it was created successfully.

    ```console
    mvn compile
    ```

### Install the client library

The client library is available through Maven, as the `mongodb-driver-sync` artifact.

1. Add the MongoDB Java driver dependency to your `pom.xml` file.

    ```xml
    <dependency>
        <groupId>org.mongodb</groupId>
        <artifactId>mongodb-driver-sync</artifactId>
        <version>5.2.0</version>
    </dependency>
    ```

1. Open and review the **pom.xml** file to validate that the dependency entry exists.

1. Import the required packages into your application code:

    ```java
    import com.mongodb.client.MongoClient;
    import com.mongodb.client.MongoClients;
    import com.mongodb.client.MongoCollection;
    import com.mongodb.client.MongoDatabase;
    import com.mongodb.client.model.Filters;
    import com.mongodb.client.model.ReplaceOptions;
    import org.bson.Document;
    import org.bson.conversions.Bson;

    import java.util.Arrays;
    import java.util.List;
    ```

## Object model

| Name | Description |
| --- | --- |
| `MongoClient` | Type used to connect to MongoDB. |
| `MongoDatabase` | Represents a database in the cluster. |
| `MongoCollection<Document>` | Represents a collection within a database in the cluster. |

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

    ```java
    public class App {
        public static void main(String[] args) {
            // Connection string for Azure DocumentDB cluster
            String connectionString = "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000";
    ```
    
1. Create the MongoDB client and verify the connection.

    ```java
            // Create a new client and connect to the server
            try (MongoClient mongoClient = MongoClients.create(connectionString)) {
                
                // Ping the server to verify connection
                MongoDatabase database = mongoClient.getDatabase("admin");
                database.runCommand(new Document("ping", 1));
                
                System.out.println("Successfully connected and pinged Azure DocumentDB");
    ```

### Get a collection

Now, get your database and collection. If the database and collection doesn't already exist, use the driver to create it for you automatically.

1. Get a reference to the database.

    ```java
                // Get database reference
                MongoDatabase adventureWorksDatabase = mongoClient.getDatabase("adventureworks");
                System.out.println("Connected to database: " + adventureWorksDatabase.getName());
    ```
    
1. Get a reference to the collection within the database.

    ```java
                // Get collection reference
                MongoCollection<Document> productsCollection = adventureWorksDatabase.getCollection("products");
                System.out.println("Connected to collection: products");
    ```

### Create a document

Then, create a couple of new documents within your collection. Upsert the documents to ensure that it replaces any existing documents if they already exist with the same unique identifier.

1. Create sample product documents using the Document class.

    ```java
                // Create sample products
                List<Document> products = Arrays.asList(
                    new Document("_id", "00000000-0000-0000-0000-000000004018")
                        .append("name", "Windry Mittens")
                        .append("category", "apparel-accessories-gloves-and-mittens")
                        .append("quantity", 121)
                        .append("price", 35.00)
                        .append("sale", false),
                    new Document("_id", "00000000-0000-0000-0000-000000004318")
                        .append("name", "Niborio Tent")
                        .append("category", "gear-camp-tents")
                        .append("quantity", 140)
                        .append("price", 420.00)
                        .append("sale", true)
                );
    ```
    
1. Insert the documents using upsert operations.

    ```java
                // Insert documents with upsert
                for (Document product : products) {
                    Bson filter = Filters.eq("_id", product.getString("_id"));
                    ReplaceOptions options = new ReplaceOptions().upsert(true);
                    
                    productsCollection.replaceOne(filter, product, options);
                    System.out.println("Upserted product: " + product.getString("name"));
                }
    ```

### Retrieve a document

Next, perform a point read operation to retrieve a specific document from your collection.

1. Define the filter to find a specific document by ID.

    ```java
                // Retrieve a specific document by ID
                Bson filter = Filters.eq("_id", "00000000-0000-0000-0000-000000004018");
    ```
    
1. Execute the query and retrieve the result.

    ```java
                Document retrievedProduct = productsCollection.find(filter).first();
                
                if (retrievedProduct != null) {
                    System.out.println("Retrieved product: " + retrievedProduct.getString("name") + 
                                     " - $" + retrievedProduct.getDouble("price"));
                } else {
                    System.out.println("Product not found");
                }
    ```

### Query documents

Finally, query multiple documents using the MongoDB Query Language (MQL).

1. Define a query to find documents matching specific criteria.

    ```java
                // Query for products on sale
                Bson saleFilter = Filters.eq("sale", true);
    ```
    
1. Iterate through the cursor to retrieve all matching documents.

    ```java
                System.out.println("Products on sale:");
                for (Document product : productsCollection.find(saleFilter)) {
                    System.out.printf("- %s: $%.2f (Category: %s)%n",
                        product.getString("name"),
                        product.getDouble("price"),
                        product.getString("category"));
                }
                
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
                e.printStackTrace();
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



