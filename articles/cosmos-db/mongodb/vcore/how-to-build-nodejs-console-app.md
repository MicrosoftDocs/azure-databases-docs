---
title: Build a Node.js console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a Node.js console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-js
ai-usage: ai-generated
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a Node.js console app with Azure Cosmos DB for MongoDB vCore

[!INCLUDE[Developer console app selector](includes/build-console-app-dev-selector.md)]

[!INCLUDE[Console app introduction](includes/console-app-introduction.md)]

This guide uses the open-source `mongodb` package from npm.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prereq-existing-cluster.md)]

[!INCLUDE[Prerequisite - Azure CLI](includes/prereq-azure-cli.md)]

- Latest version of [TypeScript](https://www.typescriptlang.org).

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
    npm install @azure/identity
    ```
    
1. TODO
    
    ```bash
    npm install mongodb
    ```

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

1. TODO

    ```typescript
    import { AccessToken, DefaultAzureCredential, TokenCredential } from '@azure/identity';
    import { Collection, Db, Filter, FindCursor, MongoClient, OIDCCallbackParams, OIDCResponse, UpdateFilter, UpdateOptions, UpdateResult, WithId } from 'mongodb';
    ```

1. TODO

    ```typescript
    const AzureIdentityTokenCallback = async (params: OIDCCallbackParams, credential: TokenCredential): Promise<OIDCResponse> => {
        const tokenResponse: AccessToken | null = await credential.getToken(['https://ossrdbms-aad.database.windows.net/.default']);
        return {
            accessToken: tokenResponse?.token || '',
            expiresInSeconds: (tokenResponse?.expiresOnTimestamp || 0) - Math.floor(Date.now() / 1000)
        };
    };
    ```

1. TODO

    ```typescript
    const clusterName: string = '<azure-cosmos-db-mongodb-vcore-cluster-name>';
    ```

1. TODO

    ```typescript
    const credential: TokenCredential = new DefaultAzureCredential();
    ```

1. TODO

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
    }
    );
    
    console.log('Client created');
    ```

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

1. TODO

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

1. TODO

    ```typescript
    const database: Db = client.db('<database-name>');
    
    console.log('Database pointer created');
    ```

1. TODO

    ```typescript
    const collection: Collection<Product> = database.collection<Product>('<collection-name>');
    
    console.log('Collection pointer created');
    ```

1. TODO

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

1. TODO

    ```typescript
    var query: Filter<Product> = {
        _id: 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
        category: 'gear-surf-surfboards'
    };
    
    var response: WithId<Product> | null = await collection.findOne(query);
    
    var read_item: Product = response as Product;
    
    console.log(`Read document _id:\t${read_item._id}`);
    ```

1. TODO

    ```typescript
    var query: Filter<Product> = {
        category: 'gear-surf-surfboards'
    };
    
    var response: FindCursor<WithId<Product>> = await collection.find(query);
    
    for await (const document of response) {
        console.log(`Found document:\t${JSON.stringify(document)}`);
    }
    ```

1. TODO

    ```typescript
    await client.close();
    ```

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [TODO](about:blank)
