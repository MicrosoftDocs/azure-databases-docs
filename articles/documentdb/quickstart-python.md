---
title: Quickstart - Python driver
description: Learn how to use Azure DocumentDB (with MongoDB compatibility) to build NoSQL solutions using Python. Start building applications today!
author: seesharprun
ms.author: sidandrews
ms.devlang: python
ms.topic: quickstart-sdk
ms.date: 10/14/2025
ms.custom:
  - sfi-ropc-nochange
ai-usage: ai-generated
---

# Quickstart: Use Azure DocumentDB with MongoDB driver for Python

[!INCLUDE[Developer Quickstart selector](includes/selector-quickstart-dev.md)]

In this quickstart, you create a basic Azure DocumentDB application using Python. Azure DocumentDB is a NoSQL data store that allows applications to store documents in the cloud and access them using official MongoDB drivers. This guide shows how to create documents and perform basic tasks in your Azure DocumentDB cluster using Python.

[API reference](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) | [Source code](https://github.com/mongodb/mongo-python-driver) | [Package (PyPI)](https://pypi.org/project/pymongo/)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prerequisite-quickstart-dev.md)]

- Python 3.12 or later

## Create an Azure DocumentDB cluster

[!INCLUDE[Section - Create cluster](includes/section-create-cluster.md)]

## Get cluster credentials

[!INCLUDE[Section - Get credentials](includes/section-get-credentials.md)]

## Initialize the project

Create a new Python project and set up a virtual environment in your current directory.

1. Start in an empty directory.

1. Open a terminal in the current directory.

1. Create and activate a virtual environment.

    ```console
    python -m venv venv
    venv\Scripts\activate
    ```

### Install the client library

The client library is available through PyPI, as the `pymongo` package.

1. Install the MongoDB Python driver using pip.

    ```console
    pip install pymongo
    ```

1. Create a new Python file named `main.py` for your application code.

1. Import the required modules into your application code:

    ```python
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    import sys
    ```

## Object model

| Name | Description |
| --- | --- |
| `MongoClient` | Type used to connect to MongoDB. |
| `Database` | Represents a database in the cluster. |
| `Collection` | Represents a collection within a database in the cluster. |

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

    ```python
    def main():
        try:
            # Connection string for Azure DocumentDB cluster
            connection_string = "mongodb+srv://<your-username>:<your-password>@<your-cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
            
            # Create a new client and connect to the server
            client = MongoClient(connection_string)
    ```
    
1. Connect to the MongoDB client and verify the connection.

    ```python
            # Ping the server to verify connection
            client.admin.command('ping')
            print("Successfully connected and pinged Azure DocumentDB")
    ```

### Get a collection

Now, get your database and collection. If the database and collection doesn't already exist, use the driver to create it for you automatically.

1. Get a reference to the database.

    ```python
            # Get database reference
            database = client["adventureworks"]
            print(f"Connected to database: {database.name}")
    ```
    
1. Get a reference to the collection within the database.

    ```python
            # Get collection reference
            collection = database["products"]
            print("Connected to collection: products")
    ```

### Create a document

Then, create a couple of new documents within your collection. Upsert the documents to ensure that it replaces any existing documents if they already exist with the same unique identifier.

1. Create sample product documents.

    ```python
            # Create sample products
            products = [
                {
                    "_id": "00000000-0000-0000-0000-000000004018",
                    "name": "Windry Mittens",
                    "category": "apparel-accessories-gloves-and-mittens",
                    "quantity": 121,
                    "price": 35.00,
                    "sale": False,
                },
                {
                    "_id": "00000000-0000-0000-0000-000000004318",
                    "name": "Niborio Tent",
                    "category": "gear-camp-tents",
                    "quantity": 140,
                    "price": 420.00,
                    "sale": True,
                }
            ]
    ```
    
1. Insert the documents using upsert operations.

    ```python
            # Insert documents with upsert
            for product in products:
                filter_doc = {"_id": product["_id"]}
                collection.replace_one(filter_doc, product, upsert=True)
                print(f"Upserted product: {product['name']}")
    ```

### Retrieve a document

Next, perform a point read operation to retrieve a specific document from your collection.

1. Define the filter to find a specific document by ID.

    ```python
            # Retrieve a specific document by ID
            filter_doc = {"_id": "00000000-0000-0000-0000-000000004018"}
    ```
    
1. Execute the query and retrieve the result.

    ```python
            retrieved_product = collection.find_one(filter_doc)
            
            if retrieved_product:
                print(f"Retrieved product: {retrieved_product['name']} - ${retrieved_product['price']}")
            else:
                print("Product not found")
    ```

### Query documents

Finally, query multiple documents using the MongoDB Query Language (MQL).

1. Define a query to find documents matching specific criteria.

    ```python
            # Query for products on sale
            sale_filter = {"sale": True}
            sale_products = list(collection.find(sale_filter))
    ```
    
1. Iterate through the results to display the matching documents.

    ```python
            print("Products on sale:")
            for product in sale_products:
                print(f"- {product['name']}: ${product['price']:.2f} (Category: {product['category']})")
                
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        finally:
            client.close()

    if __name__ == "__main__":
        main()
    ```

## Explore your data using Visual Studio Code

[!INCLUDE[Section - Visual Studio Code extension](includes/section-quickstart-visual-studio-code-extension.md)]

## Clean up resources

[!INCLUDE[Section - Delete cluster](includes/section-delete-cluster.md)]

## Related content

- [What is Azure DocumentDB?](overview.md)


