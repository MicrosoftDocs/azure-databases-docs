---
title: |
  Tutorial: Java Integration with MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: In this tutorial, create a Java application that connects to a vCore cluster in Azure Cosmos DB for MongoDB and performs CRUD (Create, Read, Update, Delete) operations on documents within a collection.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 10/03/2025
# CustomerIntent: As a developer, I want to connect to Azure Cosmos DB for MongoDB (vCore) from my Java application, so I can efficiently perform CRUD operations and manage my database.
---

# Java Integration with MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

## Prerequisites for Different Environments 
Before proceeding with installation, ensure you have all the necessary prerequisites for your environment, including the setup of Azure resources.

### Azure Account and Cosmos DB Account Setup Prerequisites

1. Login to Azure Portal.
1. Create a new Cosmos DB resource:
    - Go to "Create a resource".
    - Search for "Azure Cosmos DB". Follow the instructions to create an Azure Cosmos DB account.
    - Select "Create". 
1. Choose MongoDB API:
    - In the "Create Azure Cosmos DB Account" blade, select "MongoDB" as the API.
1. Configure settings:
    - Choose the "vCore" option under "Capacity" and click Create.
    - Fill in the required fields (Subscription, Resource Group, Cluster Name, Admin Username, Password, etc).
    - Review and create the account.
1. Get Connection String:
    - After creation, go to your Cosmos DB account.
    - Navigate to "Connection String" and copy the connection string for later use.

> [Create vCore resources - Azure Portal](quickstart-portal.md)    

### Local Machine Environment Prerequisites
- Windows.
    - Operating System: Windows 10 or later.
    - Java: Install Java Development Kit (JDK) from [Oracle’s website](https://www.oracle.com/java/technologies/downloads/?er=221886).
- macOS:
    - Operating System: macOS Catalina or later. 
    - Homebrew: It is recommended to use Homebrew for installing required software. Install Homebrew if not already present. 
        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```  
    - Install Java Using Homebrew
        ```shell
        brew install openjdk
        ```          
    - We can directly download Java as per requirements:
        - Java JDK: Install Java Development Kit (JDK) from [Oracle’s website](https://www.oracle.com/java/technologies/downloads/?er=221886).

 - Linux:
    - Supported Distributions: Debian/Ubuntu, RHEL/CentOS.
    - Java Installation:
        ```shell
        sudo apt-get install openjdk-11-jdk
        ```         
## Setting up Azure Cosmos DB for MongoDB using Java (Installation)
### Installing with Java Package Manager (Maven)
To interact with Azure Cosmos DB for MongoDB using Java, add the MongoDB Java driver to your project.
- Add MongoDB Dependency Using Maven, Add the following dependency to your pom.xml file:
    ```xml
    <dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongodb-driver-sync</artifactId>
    <version>4.5.0</version>
    </dependency>

    ```
- Sample Code to Connect to Cosmos DB: 
    ```java
    import com.mongodb.ConnectionString;
    import com.mongodb.MongoClientSettings;
    import com.mongodb.client.MongoClient;
    import com.mongodb.client.MongoClients;

    public class CosmosDBConnection {
        public static void main(String[] args) {
            String uri = "your_cosmos_db_connection_string";
            ConnectionString connectionString = new ConnectionString(uri);
            MongoClientSettings settings = MongoClientSettings.builder()
                    .applyConnectionString(connectionString)
                    .build();
            try (MongoClient mongoClient = MongoClients.create(settings)) {
                System.out.println("Connected successfully to Azure Cosmos DB for MongoDB");
            }
        }
    }
    ```
    > [!NOTE]
    > Replace uri with your Mongo Connection String. Avoid hardcoding sensitive data; use environment variables instead.



## Java CRUD Operations with Azure Cosmos DB (MongoDB API - vCore) 
The example will include:
- Create: Inserting new documents into a collection.
- Read: Querying documents from a collection.
- Update: Updating documents in a collection.
- Delete: Deleting documents from a collection.

### Example Java Code for CRUD Operations
Below is a Java script that demonstrates CRUD operations on Azure Cosmos DB using the MongoDB API : 

```Java
import com.mongodb.client.*;
import org.bson.Document;

public class CosmosDBExample {
    public static void main(String[] args) {
        // Replace with your Cosmos DB connection string
        String connectionString = "<your_connection_string>";

        // Create a MongoClient instance
        MongoClient client = MongoClients.create(connectionString);

        // Access the database and collection
        MongoDatabase database = client.getDatabase("myDatabase");  // Replace with your database name
        MongoCollection<Document> collection = database.getCollection("myCollection");  // Replace with your collection name

        // CREATE Operation: Insert a new document
        createDocument(collection);
        // READ Operation: Query for a document by a specific field
        readDocument(collection);
        // UPDATE Operation: Update a document by its field
        updateDocument(collection);
        // DELETE Operation: Delete a document by its field
        deleteDocument(collection);
        // Close the MongoDB client connection
        client.close();
    }
    // CREATE Operation: Insert a new document
    private static void createDocument(MongoCollection<Document> collection) {
        Document document = new Document("name", "John Doe")
                .append("age", 30)
                .append("city", "New York");

        // Insert the document into the collection
        collection.insertOne(document);
        System.out.println("Inserted document with name: John Doe");
    }

    // READ Operation: Query for a document by a specific field
    private static void readDocument(MongoCollection<Document> collection) {
        Document query = new Document("name", "John Doe");

        // Find a document based on the query
        FindIterable<Document> result = collection.find(query);
        result.forEach(doc -> System.out.println("Found document: " + doc.toJson()));
    }

    // UPDATE Operation: Update a document by its field
    private static void updateDocument(MongoCollection<Document> collection) {
        Document query = new Document("name", "John Doe");
        Document update = new Document("$set", new Document("age", 31));

        // Update the document
        UpdateResult result = collection.updateOne(query, update);
        System.out.println("Matched " + result.getMatchedCount() + " document(s). Updated " + result.getModifiedCount() + " document(s).");
    }

    // DELETE Operation: Delete a document by its field
    private static void deleteDocument(MongoCollection<Document> collection) {
        Document query = new Document("name", "John Doe");

        // Delete the document
        DeleteResult result = collection.deleteOne(query);
        System.out.println("Deleted " + result.getDeletedCount() + " document(s).");
    }
}
```

Detailed Explanation

1. Create Operation: Insert Documents
    - The create_document() method creates a new document into the MongoDB collection. To add a single document to the collection, we use the insert_one() method. The printed inserted_id after the document gets inserted.
1. Read Operation: Querying Documents
    - The read_document() function reads using the find_one() method It asks for a document where the name field equals 'John Doe'. If the document is found, it prints the result.
1. Update Operation: Modifying Documents
    - The update_document() method updates documents. Using the method update_one() we can update one of the documents that match the given query. In this case, we use $set to update the age field to 31.
        - Matched Count: Number of documents that matched the query.
        - Modified Count: Number of documents that were actually modified.
1.	Delete Operation: Removing Documents
    - The delete_document() function deletes a document from the collection based on a query. The delete_one() method is used to delete a single document that matches the query.
        - The deleted_count tells how many documents were deleted.
     
