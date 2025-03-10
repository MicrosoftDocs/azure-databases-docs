---
title: |
  Tutorial: Python Integration with MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: In this tutorial, create a Python application that connects to a vCore cluster in Azure Cosmos DB for MongoDB and performs CRUD (Create, Read, Update, Delete) operations on documents within a collection.
author: saireddymicrosoft
ms.author: saireddymicrosoft
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: begginer-guide
ms.date: 03/10/2025
# CustomerIntent: As a developer, I want to connect to Azure Cosmos DB for MongoDB (vCore) from my Python application, so I can efficiently perform CRUD operations and manage my database.
---

# Python Integration with MongoDB vCore

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

### Prerequisites for the Local Machine Environment
- Windows.
    - Windows 10 or later (Operating System)
    - Install Python (preferably 3. x) if you do not already have it, from the [python official website](https://www.python.org/downloads/).

- macOS:
    - Operating system: macOS Catalina or later. 
    - Homebrew: It is recommended to use Homebrew for installing required software. For installing required software use Homebrew First, install homebrew (if not already installed). 
        ```shell
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
    - Install Python Using Homebrew
        ```shell
        brew install python
        ```
    - We can directly download Python according to requirements:
        - Python: Install Python (preferably version 3.x) from the [python official website](https://www.python.org/downloads/).

- Linux:
    - Supported Distributions: Debian/Ubuntu, RHEL/CentOS.
    - Python Installation:
        ```shell
        sudo apt-get install python3 python3-pip
        ```
## Setting up Azure Cosmos DB for MongoDB using Python (Installation)
### Setting up with pip (Python)
- To use Azure Cosmos DB for MongoDB in Python, you need to install the pymongo library.
- Install PyMongo using pip 
    ```shell
    pip install pymongo
    ```
- Sample Code to Connect to Cosmos DB: 
    ```python
        from pymongo import MongoClient

        uri = "your_cosmos_db_connection_string"
        client = MongoClient(uri)

        try:
            client.admin.command('ping')
            print("Connected successfully to Azure Cosmos DB for MongoDB")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client.close()

    ```
    
    > [!NOTE]
    > Replace uri with your Mongo Connection String. Avoid hardcoding sensitive data; use environment variables instead.
## Python CRUD operations using Azure Cosmos DB (Mongo DB API - vCore)
The example will include:
- **Create**: Adding new documents to the collection.
- **Read**: Querying documents from a collection.
- **Update**: Updates documents in a collection.
- **Delete**: Deleting documents from a collection.

### Example Python Code for CRUD Operations
Below is a Python script that demonstrates CRUD operations on Azure Cosmos DB using the MongoDB API : 

```python
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Replace with your Cosmos DB connection string
connection_string = "<your_connection_string>"

# Create a MongoClient instance
client = MongoClient(connection_string)

# Access the specific database and collection
db = client['myDatabase']  # Replace 'myDatabase' with your database name
collection = db['myCollection']  # Replace 'myCollection' with your collection name

# --------------------------------------------------------
# CREATE Operation: Insert a new document
# --------------------------------------------------------

def create_document():
    document = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    # Insert the document into the collection
    result = collection.insert_one(document)
    print(f"Inserted document with ID: {result.inserted_id}")

# --------------------------------------------------------
# READ Operation: Query for a document by a specific field
# --------------------------------------------------------

def read_document():
    query = {'name': 'John Doe'}
    # Find a document based on the query
    result = collection.find_one(query)
    if result:
        print(f"Found document: {result}")
    else:
        print("Document not found.")

# --------------------------------------------------------
# UPDATE Operation: Update a document by its ID
# --------------------------------------------------------

def update_document():
    # Specify the query to find the document
    query = {'name': 'John Doe'}
    new_values = {"$set": {'age': 31}}

    # Update the document
    result = collection.update_one(query, new_values)
    if result.matched_count > 0:
        print(f"Matched {result.matched_count} document(s). Updated {result.modified_count} document(s).")
    else:
        print("No document matched the query.")

# --------------------------------------------------------
# DELETE Operation: Delete a document by its ID
# --------------------------------------------------------

def delete_document():
    # Specify the query to find the document to delete
    query = {'name': 'John Doe'}
    
    # Delete the document
    result = collection.delete_one(query)
    if result.deleted_count > 0:
        print(f"Deleted {result.deleted_count} document(s).")
    else:
        print("No document matched the query.")

# --------------------------------------------------------
# Main Execution Flow
# --------------------------------------------------------

if __name__ == "__main__":
    print("Performing CRUD Operations on Cosmos DB (MongoDB API)...")

    # Create a document
    create_document()

    # Read a document
    read_document()

    # Update the document
    update_document()

    # Read the document again to confirm update
    read_document()

    # Delete the document
    delete_document()

    # Try reading again after deletion
    read_document()
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

