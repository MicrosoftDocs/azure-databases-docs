---
title: Build a Node.js console app
description: Connect to an Azure DocumentDB cluster by using a Node.js console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 07/21/2025
ms.custom:
  - devx-track-js
  - build-2025
ai-usage: ai-assisted
zone_pivot_groups: azure-devlang-nodejs
# Customer Intent: As a database developer, I want to build a Node.js console application to quickly and securely connect to and query my database and collections.
---

# Build a Node.js console app with Azure DocumentDB

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

This guide helps you build a Node.js console application to connect to an Azure DocumentDB cluster. You prepare your development environment, use the `@azure/identity` package from the Azure SDK for JavaScript to authenticate, and perform common operations on documents in the database.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `root` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-connect-role-based-access-control.md).

- Latest long-term support (LTS) version of [Node](https://nodejs.org)

::: zone pivot="programming-language-js"

:::zone-end

::: zone pivot="programming-language-ts"

- Latest version of [TypeScript](https://www.typescriptlang.org).

:::zone-end

## Configure your console application

Next, create a new console application project and import the necessary libraries to authenticate to your cluster.

1. Create a new directory for your project and initialize it with `npm init`.

    ```bash
    mkdir mongodb-app
    cd mongodb-app
    npm init -y
    ```

1. Set up TypeScript in your project.

    ```bash
    npm install typescript ts-node @types/node --save-dev
    npx tsc --init
    ```

1. Create the main **app.ts** TypeScript file for your application.

    ```bash
    touch app.ts
    ```
    
1. Install the `@azure/identity` library for authentication.

    ```bash
    npm install @azure/identity
    ```
    
1. Install the `mongodb` library.
    
    ```bash
    npm install mongodb
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

::: zone pivot="programming-language-js"

1. Import the necessary modules at the top of your JavaScript file.

    ```javascript
    import { MongoClient } from 'mongodb';
    import { DefaultAzureCredential } from '@azure/identity';
    ```

1. Create a token callback function that obtains tokens from the `TokenCredential` instance when required.

    ```javascript
    const azureIdentityTokenCallback = async (_, credential) => {
        const tokenResponse = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
    
        if (!tokenResponse || !tokenResponse.token) {
            throw new Error('Failed to retrieve a valid access token.');
        }
    
        return {
            accessToken: tokenResponse.token,
            expiresInSeconds: Math.floor((tokenResponse.expiresOnTimestamp - Date.now()) / 1000),
        };
    };
    ```

1. Set your cluster name variable to connect to your Azure DocumentDB cluster.

    ```javascript
    const clusterName = '<azure-documentdb-cluster-name>';
    ```

1. Create an instance of `DefaultAzureCredential`.

    ```javascript
    const credential = new DefaultAzureCredential();
    ```

1. Create a MongoDB client configured with OpenID Connect (OIDC) authentication.

    ```javascript
    client = new MongoClient(`mongodb+srv://${clusterName}.global.mongocluster.cosmos.azure.com/`, {
        connectTimeoutMS: 120000,
        tls: true,
        retryWrites: true,
        authMechanism: 'MONGODB-OIDC',
        authMechanismProperties: {
            OIDC_CALLBACK: (params) => azureIdentityTokenCallback(params, credential),
            ALLOWED_HOSTS: ['*.azure.com']
        }
    });
    
    console.log('Client created');
    ```

:::zone-end

::: zone pivot="programming-language-ts"

1. Import the necessary modules at the top of your TypeScript file.

    ```typescript
    import { AccessToken, DefaultAzureCredential, TokenCredential } from '@azure/identity';
    import { Collection, Db, Filter, FindCursor, MongoClient, OIDCCallbackParams, OIDCResponse, UpdateFilter, UpdateOptions, UpdateResult, WithId } from 'mongodb';
    ```

1. Create a token callback function that obtains tokens from the `TokenCredential` instance when required.

    ```typescript
    const AzureIdentityTokenCallback = async (params: OIDCCallbackParams, credential: TokenCredential): Promise<OIDCResponse> => {
        const tokenResponse: AccessToken | null = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
        return {
            accessToken: tokenResponse?.token || '',
            expiresInSeconds: (tokenResponse?.expiresOnTimestamp || 0) - Math.floor(Date.now() / 1000)
        };
    };
    ```

1. Set your cluster name variable to connect to your Azure DocumentDB cluster.

    ```typescript
    const clusterName: string = '<azure-documentdb-cluster-name>';
    ```

1. Create an instance of `DefaultAzureCredential`.

    ```typescript
    const credential: TokenCredential = new DefaultAzureCredential();
    ```

1. Create a MongoDB client configured with OpenID Connect (OIDC) authentication.

    ```typescript
    const client = new MongoClient(
        `mongodb+srv://${clusterName}.global.mongocluster.cosmos.azure.com/`, {
        connectTimeoutMS: 120000,
        tls: true,
        retryWrites: true,
        authMechanism: 'MONGODB-OIDC',
        authMechanismProperties: {
            OIDC_CALLBACK: (params: OIDCCallbackParams) => AzureIdentityTokenCallback(params, credential),
            ALLOWED_HOSTS: ['*.azure.com']
        }
    });
    
    console.log('Client created');
    ```

:::zone-end

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

::: zone pivot="programming-language-js"

1. Get a reference to your database by name.

    ```javascript
    const databaseName = process.env.SETTINGS__DATABASENAME ?? 'cosmicworks';
    
    console.log('Database pointer created');
    ```

1. Get a reference to your collection.

    ```javascript
    const collectionName = process.env.SETTINGS__COLLECTIONNAME ?? 'products';
    
    console.log('Collection pointer created');
    ```

1. Create a document using `collection.updateOne` and **upsert** it into the collection.

    ```javascript
    const filter = { _id: request.params._id };
    const payload = {
        $set: document
    };
    const options = {
        upsert: true
    };

    var response = await collection.updateOne(filter, payload, options);
    
    if (response.acknowledged) {
        console.log(`Documents upserted count:\t${response.matchedCount}`);
    }
    ```

1. Use `collection.findOne` to get a specific document from the collection.

    ```javascript
    const filter = { _id: request.params.id };

    var document = await collection.findOne(filter, options);
    
    console.log(`Read document _id:\t${document._id}`);
    ```

1. Query for multiple documents matching a filter using `collection.find`.

    ```javascript
    var filter = {
        category: 'gear-surf-surfboards'
    };

    var documents = collection.find(filter);
    
    for await (const document of documents) {
        console.log(`Found document:\t${JSON.stringify(document)}`);
    }
    ```

1. Close the MongoDB client connection when done.

    ```javascript
    await client.close();
    ```

:::zone-end

::: zone pivot="programming-language-ts"

1. Get a reference to your database by name.

    ```typescript
    const database: Db = client.db('<database-name>');
    
    console.log('Database pointer created');
    ```

1. Get a reference to your collection.

    ```typescript
    const collection: Collection<Product> = database.collection<Product>('<collection-name>');
    
    console.log('Collection pointer created');
    ```

1. Define an interface to represent your product documents.

    ```typescript
    interface Product {
        _id: string;
        category: string;
        name: string;
        quantity: number;
        price: number;
        clearance: boolean;
    }
    ```

1. Create a document using `collection.updateOne` and **upsert** it into the collection.

    ```typescript
    var document: Product = {
        _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        category: 'gear-surf-surfboards',
        name: 'Yamba Surfboard',
        quantity: 12,
        price: 850.00,
        clearance: false
    };
    
    var query: Filter<Product> = {
        _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb'
    };
    var payload: UpdateFilter<Product> = {
        $set: document
    };
    var options: UpdateOptions = {
        upsert: true
    };
    var response: UpdateResult<Product> = await collection.updateOne(query, payload, options);
    
    if (response.acknowledged) {
        console.log(`Documents upserted count:\t${response.matchedCount}`);
    }
    ```

1. Use `collection.findOne` to get a specific document from the collection.

    ```typescript
    var query: Filter<Product> = {
        _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        category: 'gear-surf-surfboards'
    };
    
    var response: WithId<Product> | null = await collection.findOne(query);
    
    var read_item: Product = response as Product;
    
    console.log(`Read document _id:\t${read_item._id}`);
    ```

1. Query for multiple documents matching a filter using `collection.find`.

    ```typescript
    var query: Filter<Product> = {
        category: 'gear-surf-surfboards'
    };
    
    var response: FindCursor<WithId<Product>> = collection.find(query);
    
    for await (const document of response) {
        console.log(`Found document:\t${JSON.stringify(document)}`);
    }
    ```

1. Close the MongoDB client connection when done.

    ```typescript
    await client.close();
    ```

:::zone-end

## Related content

- [Microsoft Entra authentication overview](how-to-connect-role-based-access-control.md)
- [Node.js web application template](quickstart-nodejs.md)
- [Microsoft Entra configuration for cluster](how-to-connect-role-based-access-control.md)
