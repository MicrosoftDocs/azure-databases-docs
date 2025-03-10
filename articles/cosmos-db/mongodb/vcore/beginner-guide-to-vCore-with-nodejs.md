---
title: |
  Tutorial: Node js Integration with MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: In this tutorial, create a Node js application that connects to a vCore cluster in Azure Cosmos DB for MongoDB and performs CRUD (Create, Read, Update, Delete) operations on documents within a collection.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 10/03/2025
# CustomerIntent: As a developer, I want to connect to Azure Cosmos DB for MongoDB (vCore) from my Node js application, so I can efficiently perform CRUD operations and manage my database.
---

# Node js Integration with MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

## Prerequisites for Different Environments 
Before proceeding with installation, ensure you have all the necessary prerequisites for your environment, including the setup of Azure resources.

### Azure Account and Cosmos DB Account Setup Prerequisites

1. Login to Azure Portal.
1. Create New Resource: Azure Cosmos DB:
    - Click on "Create a resource".
    - Type in the search bar “Azure Cosmos DB”. Click on “create account” to configure an Azure Cosmos DB account.
    - Click on "Create". 
1. Choose MongoDB API:
    - Choose “MongoDB” as the API option under "Create Azure Cosmos DB Account" blade.
1. Configure settings:
    - choose "vCore" under "Capacity" and click Create.
    - fill the details (Subscription, Resource Group,Cluster Name, Admin Username, Password, etc.) in the blank fields.
    - Review and create the account.
1. Copy Connection String:
    - After creation, go to your Cosmos DB account in Azure.
    - Navigate to "Connection String" and copy the connection string for later use.

> [Create vCore resources - Azure Portal](quickstart-portal.md)  

### Local Machine Environment Prerequisites
1. Windows.
    - Operating System: Windows 10 or later.
    - Node.js: Download and install Node.js, which includes NPM, from [Node.js official website](https://nodejs.org/en).
1. macOS:
    - Operating System: macOS Catalina or later. 
    - Homebrew: It is recommended to use Homebrew for installing required software. Install Homebrew if not already present. 
        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
    - Install Node js Using Homebrew
        ```shell
        brew install node
    - We can directly download node js as per requirements:
        - Node.js: Download and install Node.js, which includes NPM, from Node.js official website [node js official website](https://nodejs.org/en).    	 
- Linux:
    - Supported Distributions: Debian/Ubuntu, RHEL/CentOS.
    - Node js Installation:
        ```shell
        sudo apt-get install nodejs npm        
        ```
## Setting up Azure Cosmos DB for MongoDB using Node js   
### Setting up with NPM  (Node.js)
- To interact with Azure Cosmos DB for MongoDB using Node.js, the MongoDB package is required.
- Install PyMongo using pip 
    ```shell
    npm install mongodb
    ```
- Sample Code to Connect to Cosmos DB: 
    ```js
    const { MongoClient } = require('mongodb');

    async function main() {
    const uri = "your_cosmos_db_connection_string";
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    
    try {
        await client.connect();
        console.log("Connected successfully to Azure Cosmos DB for MongoDB");
    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
    }

    main().catch(console.error);
    ```
    > [!NOTE]
    > Replace uri with your Mongo Connection String. Avoid hardcoding sensitive data; use environment variables instead.


## Node.js CRUD Operations with Azure Cosmos DB (MongoDB API - vCore) 
The example will include:
- Create: Inserting new documents into a collection.
- Read: Querying documents from a collection.
- Update: Updating documents in a collection.
- Delete: Deleting documents from a collection.

### Example Node.js Code for CRUD Operations
Below is a Node.js script that demonstrates CRUD operations on Azure Cosmos DB using the MongoDB API  

```js
const { MongoClient } = require('mongodb');

// Replace with your Cosmos DB connection string
const connectionString = "<your_connection_string>";

async function main() {
    // Create a new MongoClient instance
    const client = new MongoClient(connectionString);

    try {
        // Connect to the MongoDB server
        await client.connect();
        console.log("Connected to Cosmos DB successfully.");

        // Access the database and collection
        const db = client.db('myDatabase'); // Replace 'myDatabase' with your database name
        const collection = db.collection('myCollection'); // Replace 'myCollection' with your collection name

        // CREATE Operation: Insert a new document
        const createDocument = async () => {
            const document = {
                name: 'John Doe',
                age: 30,
                city: 'New York'
            };

            const result = await collection.insertOne(document);
            console.log(`Inserted document with ID: ${result.insertedId}`);
        };
        
        // READ Operation: Query for a document by a specific field
        const readDocument = async () => {
            const query = { name: 'John Doe' };
            const result = await collection.findOne(query);

            if (result) {
                console.log(`Found document: ${JSON.stringify(result)}`);
            } else {
                console.log("Document not found.");
            }
        };

        // UPDATE Operation: Update a document by its ID
        const updateDocument = async () => {
            const query = { name: 'John Doe' };
            const update = {
                $set: { age: 31 }
            };

            const result = await collection.updateOne(query, update);
            console.log(`Matched ${result.matchedCount} document(s). Updated ${result.modifiedCount} document(s).`);
        };

        // DELETE Operation: Delete a document by its ID       
        const deleteDocument = async () => {
            const query = { name: 'John Doe' };

            const result = await collection.deleteOne(query);
            console.log(`Deleted ${result.deletedCount} document(s).`);
        };

        // Execute CRUD operations
        await createDocument();
        await readDocument();
        await updateDocument();
        await readDocument();
        await deleteDocument();
        await readDocument(); // Try reading after deletion

    } catch (err) {
        console.error("Error performing CRUD operations:", err);
    } finally {
        await client.close();
    }
}

// Execute the main function
main().catch(console.error);
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

