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
ms.date: 11/29/2024
# CustomerIntent: As a developer, I want to connect to Azure Cosmos DB for MongoDB (vCore) from my Node js application, so I can efficiently perform CRUD operations and manage my database.
---

# Node js Integration with MongoDB vCore

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
	Replace uri with your Mongo Connection String.


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

1.	Create Operation: Inserting Documents
    - The createDocument function inserts a new document into the MongoDB collection using the insertOne() method. The document is inserted with fields name, age, and city. The insertedId of the inserted document is printed after the operation.
1.	Read Operation: Querying Documents
    - The readDocument function performs a query using findOne() to retrieve a document where the name field is 'John Doe'. If the document exists, it is printed to the console. If not, a message is shown indicating that no document was found.
1.	Update Operation: Modifying Documents
    - The updateDocument function updates an existing document. The updateOne() method is used to update a document that matches the query. In this case, we use the $set operator to change the age field to 31.
        - matchedCount: The number of documents that matched the query.
        - modifiedCount: The number of documents that were actually modified.
1.	Delete Operation: Removing Documents
    - The deleteDocument function deletes a document that matches the query. The deleteOne() method is used to remove a single document from the collection. The number of documents deleted (deletedCount) is printed after the operation.
