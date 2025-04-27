---
title: Build a Python console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Python console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-python
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a Python console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/build-console-app-dev-selector.md)]

[!INCLUDE[Console app introduction](includes/console-app-introduction.md)]

This guide uses the open-souce `pymongo` package from PyPI.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- Latest version of [Python](https://www.python.org).

## Grant your identity access

[!INCLUDE[Console app identity access](includes/console-app-identity-access.md)]

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. TODO

    ```bash

    ```

1. TODO

    ```bash

    ```

1. TODO

    ```bash

    ```
    
1. TODO

    ```bash
    pip install azure.identity
    ```
    
1. TODO
    
    ```bash
    pip install pymongo
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. TODO

    ```python
    from azure.identity import DefaultAzureCredential
    from pymongo import MongoClient
    from pymongo.auth_oidc import OIDCCallback, OIDCCallbackContext, OIDCCallbackResult
    ```

1. TODO

    ```python
    class AzureIdentityTokenCallback(OIDCCallback):
        def __init__(self, credential):
            self.credential = credential
    
        def fetch(self, context: OIDCCallbackContext) -> OIDCCallbackResult:
            token = self.credential.get_token(
                "https://ossrdbms-aad.database.windows.net/.default").token
            return OIDCCallbackResult(access_token=token)
    ```

1. TODO

    ```python
    clusterName = "<azure-cosmos-db-mongodb-vcore-cluster-name>"
    ```

1. TODO

    ```python
    credential = DefaultAzureCredential()
    authProperties = {"OIDC_CALLBACK": AzureIdentityTokenCallback(credential)}
    ```

1. TODO

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

1. TODO

    ```python
    database = client.get_database("<database-name>")
    
    print("Database pointer created")
    ```

1. TODO

    ```python
    collection = database.get_collection("<container-name>")
    
    print("Collection pointer created")
    ```

1. TODO

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

1. TODO

    ```python
    filter = {
        "_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "category": "gear-surf-surfboards"
    }
    existing_document = collection.find_one(filter)
    print(f"Read document _id:\t{existing_document['_id']}")
    ```

1. TODO

    ```python
    filter = {
        "category": "gear-surf-surfboards"
    }
    matched_documents = collection.find(filter)
    
    for document in matched_documents:
        print(f"Found document:\t{document}")
    ```

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [TODO](about:blank)
