---
title: Build a Python console app
description: Connect to an Azure DocumentDB cluster by using a Python console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 07/21/2025
ms.custom:
  - devx-track-python
  - build-2025
ai-usage: ai-assisted
# Customer Intent: As a database developer, I want to build a Python console application to quickly and securely connect to and query my database and collections.
---

# Build a Python console app with Azure DocumentDB

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

This guide walks you through building a Python console application to connect to an Azure DocumentDB cluster. You configure your development environment, authenticate using the `azure.identity` package from the Azure SDK for Python, and perform operations such as creating, querying, and updating documents.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `root` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-connect-role-based-access-control.md).

- Latest version of [Python](https://www.python.org).

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. Create a new directory for your project and set up a virtual environment.

    ```bash
    mkdir mongodb-app
    cd mongodb-app
    python -m venv .venv
    ```

1. Activate the virtual environment.

    ```bash
    # On Windows
    .venv\Scripts\activate
    
    # On macOS/Linux
    source .venv/bin/activate
    ```

1. Create a new Python file for your application.

    ```bash
    touch app.py
    ```
    
1. Install the `azure.identity` library for Azure authentication.

    ```bash
    pip install azure.identity
    ```
    
1. Install the `pymongo` driver for Python.
    
    ```bash
    pip install pymongo
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. Import the necessary modules at the top of your Python file.

    ```python
    from azure.identity import DefaultAzureCredential
    from pymongo import MongoClient
    from pymongo.auth_oidc import OIDCCallback, OIDCCallbackContext, OIDCCallbackResult
    ```

1. Create a custom class that implements the MongoDB OpenID Connect (OIDC) callback interface.

    ```python
    class AzureIdentityTokenCallback(OIDCCallback):
        def __init__(self, credential):
            self.credential = credential
    
        def fetch(self, context: OIDCCallbackContext) -> OIDCCallbackResult:
            token = self.credential.get_token(
                "https://ossrdbms-aad.database.windows.net/.default").token
            return OIDCCallbackResult(access_token=token)
    ```

1. Set your cluster name variable.

    ```python
    clusterName = "<azure-documentdb-cluster-name>"
    ```

1. Create an instance of DefaultAzureCredential and set up the authentication properties.

    ```python
    credential = DefaultAzureCredential()
    authProperties = {"OIDC_CALLBACK": AzureIdentityTokenCallback(credential)}
    ```

1. Create a MongoDB client configured with Microsoft Entra authentication.

    ```python
    client = MongoClient(
        f"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/",
        connectTimeoutMS=120000,
        tls=True,
        retryWrites=True,
        authMechanism="MONGODB-OIDC",
        authMechanismProperties=authProperties
    )
    
    print("Client created")
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. Get a reference to your database.

    ```python
    database = client.get_database("<database-name>")
    
    print("Database pointer created")
    ```

1. Get a reference to your collection.

    ```python
    collection = database.get_collection("<container-name>")
    
    print("Collection pointer created")
    ```

1. Create a document and **upsert** it into the collection with `collection.update_one`.

    ```python
    new_document = {
        "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "category": "gear-surf-surfboards",
        "name": "Yamba Surfboard",
        "quantity": 12,
        "price": 850.00,
        "clearance": False,
    }
    
    filter = {
        "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    }
    payload = {
        "$set": new_document
    }
    result = collection.update_one(filter, payload, upsert=True)
    ```

1. Use `collection.find_one` to retrieve a specific document from the collection.

    ```python
    filter = {
        "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "category": "gear-surf-surfboards"
    }
    existing_document = collection.find_one(filter)
    print(f"Read document _id:\t{existing_document['_id']}")
    ```

1. Query for multiple documents with `collection.find` that matches a filter.

    ```python
    filter = {
        "category": "gear-surf-surfboards"
    }
    matched_documents = collection.find(filter)
    
    for document in matched_documents:
        print(f"Found document:\t{document}")
    ```

## Related content

- [Microsoft Entra authentication overview](how-to-connect-role-based-access-control.md)
- [Python web application template](quickstart-python.md)
- [Microsoft Entra configuration for cluster](how-to-connect-role-based-access-control.md)
