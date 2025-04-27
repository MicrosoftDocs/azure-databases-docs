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

In this guide, you build a console application to connect to an existing Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to configure the cluster for Microsoft Entra authentication and then to connect to the same cluster using the identity that you're currently signed-in with.

This guide uses the open-source `mongodb` package from npm.

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.
- The latest version of the [Azure CLI](/cli/azure) in [Azure Cloud Shell](/azure/cloud-shell).
  - If you prefer to run CLI reference commands locally, sign in to the Azure CLI by using the [`az login`](/cli/azure/reference-index#az-login) command.
- Latest version of [TypeScript](https://www.typescriptlang.org).

## Grant your identity access

First, get the unique identifier for your currently signed-in identity. Then, use the Azure CLI to configure your existing cluster to support Microsoft Entra authentication directly with your identity.

1. Get the details for the currently logged-in account using `az ad signed-in-user`.

    ```azurecli-interactive
    az ad signed-in-user show
    ```    

1. The command outputs a JSON response containing various fields. 

    ```json
    {
      "@odata.context": "<https://graph.microsoft.com/v1.0/$metadata#users/$entity>",
      "businessPhones": [],
      "displayName": "Kai Carter",
      "givenName": "Kai",
      "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
      "jobTitle": "Senior Sales Representative",
      "mail": "<kai@adventure-works.com>",
      "mobilePhone": null,
      "officeLocation": "Redmond",
      "preferredLanguage": null,
      "surname": "Carter",
      "userPrincipalName": "<kai@adventure-works.com>"
    }
    ```

1. Record the value of the `id` property. This property is the unique identifier for your principal and is sometimes referred to as the **principal ID**. You use this value in the next series of steps.

1. Now, get the `authConfig` property from your existing cluster using `az resource show`.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --query "properties.authConfig" \
        --latest-include-preview
    ```

1. Observe the output. If Microsoft Entra authentication isn't configured, the output includes only the `NativeAuth` value in the `allowedModes` array.

    ```json
    {
      "allowedModes": [
        "NativeAuth"
      ]
    }
    ```

1. Create a new JSON file named *properties.json*. In the file, define the new value for the `authConfig` property.

    ```json
    {
      "authConfig": {
        "allowedModes": [
          "MicrosoftEntraID",
          "NativeAuth"
        ]
      }
    }
    ```    

1. Then, update the existing cluster with an HTTP `PATCH` operation by adding the `MicrosoftEntraID` value to `allowedModes`.

    ```azurecli-interactive
    az resource patch
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --properties @properties.json \
        --latest-include-preview
    ```
    
1. Validate that the configuration was successful by using `az resource show` again and observing the `properties.authConfig` property.

    ```azurecli-interactive
    az resource show \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters" \
        --latest-include-preview
    ```

1. Now, create a new JSON file named *user.json*. In this file, define a user to register for Microsoft Entra authentication.

    ```json
    {
      "identityProvider": {
        "type": "MicrosoftEntraID",
        "properties": {
          "principalType": "User"
        }
      },
      "roles": [
        {
          "db": "admin",
          "role": "dbOwner"
        }
      ]
    }
    ```

    > [!TIP]
    > If you're registering a service principal, like a managed identity, you would replace the `identityProvider.properties.principalType` property's value with `ServicePrincipal`.

1. Use `az resource create` to create a new resource of type `Microsoft.DocumentDB/mongoClusters/users`. Compose the name of the resource by concatenating the **name of the parent cluster** and the **principal ID** of your identity.

    ```azurecli-interactive
    az resource create \
        --resource-group "<resource-group-name>" \
        --name "<azure-cosmos-db-mongodb-vcore-cluster-name>/users/<principal-id>" \
        --resource-type "Microsoft.DocumentDB/mongoClusters/users" \
        --properties @user.json \
        --latest-include-preview
    ```

    > [!NOTE]
    > For example, if your parent resource is named `example-cluster` and your principal ID was `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`, the name of the resource would be:
    >
    > ```json
    > "example-cluster/users/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
    > ```
    >

1. Get the details for the currently logged-in Azure subscription using `az account show`.

    ```azurecli-interactive
    az account show
    ```    

1. The command outputs a JSON response containing various fields. 

    ```json
    {
      "environmentName": "AzureCloud",
      "homeTenantId": "eeeeffff-4444-aaaa-5555-bbbb6666cccc",
      "id": "dddd3d3d-ee4e-ff5f-aa6a-bbbbbb7b7b7b",
      "isDefault": true,
      "managedByTenants": [],
      "name": "example-azure-subscription",
      "state": "Enabled",
      "tenantId": "eeeeffff-4444-aaaa-5555-bbbb6666cccc",
      "user": {
        "cloudShellID": true,
        "name": "kai@adventure-works.com",
        "type": "user"
      }
    }
    ```

1. Record the value of the `tenantId` property. This property is the unique identifier for your Microsoft Entra tenant and is sometimes referred to as the **tenant ID**. You use this value in steps within a subsequent section.

> [!TIP]
> These same steps can be followed to configure Microsoft Entra authentication for a managed identity, workload identity, application identity, or service principal.

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
