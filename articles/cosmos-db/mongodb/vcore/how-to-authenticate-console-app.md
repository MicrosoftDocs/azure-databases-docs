---
title: Authenticate to a console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/25/2025
ms.custom: devx-track-js, devx-track-python, devx-track-dotnet, devx-track-extended-azdevcli
zone_pivot_groups: programming-languages-set-documentdb
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Connect to Azure Cosmos DB for MongoDB vCore with Microsoft Entra authentication

In this guide, you build a console application to connect to an existing Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to configure the cluster for Microsoft Entra authentication and then to connect to the same cluster using the identity that you're currently signed-in with.

:::zone pivot="programming-language-csharp"

This guide uses the open-source `MongoDB.Driver` library from NuGet.

:::zone-end

:::zone pivot="programming-language-ts"

This guide uses the open-source `mongodb` package from npm.

:::zone-end

:::zone pivot="programming-language-python"

This guide uses the open-souce `pymongo` package from PyPI.

:::zone-end

:::zone pivot="programming-language-java

:::zone-end

:::zone pivot="programming-language-go

:::zone-end

:::zone pivot="programming-language-rust

:::zone-end

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.

- The latest version of the [Azure CLI](/cli/azure) in [Azure Cloud Shell](/azure/cloud-shell).
  - If you prefer to run CLI reference commands locally, sign in to the Azure CLI by using the [`az login`](/cli/azure/reference-index#az-login) command.

:::zone pivot="programming-language-csharp"

- Latest version of [.NET](/dotnet).

:::zone-end
:::zone pivot="programming-language-ts"

- Latest version of [TypeScript](https://www.typescriptlang.org).

:::zone-end
:::zone pivot="programming-language-python"

- Latest version of [Python](https://www.python.org).

:::zone-end

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
    > For example, if your parent account is named `example-account` and your principal ID was `aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb`, the name of the resource would be:
    >
    > ```json
    > "example-account/users/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
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

:::zone pivot="programming-language-csharp"

1. In an empty directory, create a new .NET console application.

    ```dotnetcli
    dotnet new console
    ```

1. Import the `Azure.Identity` package from NuGet.

    ```dotnetcli
    dotnet add package Azure.Identity
    ```

1. Next, import the `MongoDB.Driver` package.

    ```dotnetcli
    dotnet add package MongoDB.Driver
    ```

1. Build the .NET project

    ```dotnetcli
    dotnet build
    ```

:::zone-end

:::zone pivot="programming-language-ts"

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

:::zone-end

:::zone pivot="programming-language-python"

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

:::zone-end

:::zone pivot="programming-language-java

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

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.15.4</version>
    </dependency>
    ```
    
1. TODO
    
    ```xml
    <dependency>
        <groupId>org.mongodb</groupId>
        <artifactId>mongodb-driver-sync</artifactId>
        <version>5.4.0</version>
    </dependency>
    ```

:::zone-end

:::zone pivot="programming-language-go

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
    
    ```
    
1. TODO
    
    ```bash
    
    ```

:::zone-end

:::zone pivot="programming-language-rust

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
    
    ```
    
1. TODO
    
    ```bash
    
    ```

:::zone-end

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

:::zone pivot="programming-language-csharp"

1. In the *Program.cs* file, add using blocks for these `Azure.Identity` and `MongoDB.Driver` namespaces.

    ```csharp
    using Azure.Identity;
    using MongoDB.Driver;
    ```

1. Create a new class in a separate file that implements all required members of the `MongoDB.Driver.Authentication.Oidc.IOidcCallback` interface.

    ```csharp
    using Azure.Core;
    using MongoDB.Driver.Authentication.Oidc;
    
    internal sealed class AzureIdentityTokenHandler(
        TokenCredential credential,
        string tenantId
    ) : IOidcCallback
    {
        private readonly string[] scopes = ["https://ossrdbms-aad.database.windows.net/.default"];
    
        public OidcAccessToken GetOidcAccessToken(OidcCallbackParameters parameters, CancellationToken cancellationToken)
        {
            AccessToken token = credential.GetToken(
                new TokenRequestContext(scopes, tenantId: tenantId),
                cancellationToken
            );
    
            return new OidcAccessToken(token.Token, token.ExpiresOn - DateTimeOffset.UtcNow);
        }
    
        public async Task<OidcAccessToken> GetOidcAccessTokenAsync(OidcCallbackParameters parameters, CancellationToken cancellationToken)
        {
            AccessToken token = await credential.GetTokenAsync(
                new TokenRequestContext(scopes, parentRequestId: null, tenantId: tenantId),
                cancellationToken
            );
    
            return new OidcAccessToken(token.Token, token.ExpiresOn - DateTimeOffset.UtcNow);
        }
    }
    ```

    > [!TIP]
    > For illustrative purposes, this class is named `AzureIdentityTokenHandler`. You can name this class anything you'd like. The rest of this guide assumes the class is named `AzureIdentityTokenHandler`.

1. Go back to the editor for the *Program.cs* file.

1. Create a string variable with the name of your existing cluster. Then, use that variable to create a new instance of type `MongoUrl` using `MongoUrl.Create`

    ```csharp
    string accountName = "<azure-cosmos-db-mongodb-vcore-account-name>";
    
    MongoUrl url = MongoUrl.Create($"mongodb+srv://{accountName}.global.mongocluster.cosmos.azure.com/");
    ```

1. Configure a new `MongoSettings` instance using the `MongoUrl` created in the previous steps and the standard best practice configuration for Azure Cosmos DB for MongoDB vCore.

    ```csharp
    MongoClientSettings settings = MongoClientSettings.FromUrl(url);
    
    settings.UseTls = true;
    settings.RetryWrites = false;
    settings.MaxConnectionIdleTime = TimeSpan.FromMinutes(2);
    ```

1. Create a new credential of type `DefaultAzureCredential`.

    ```csharp
    DefaultAzureCredential credential = new();
    ```

    > [!TIP]
    > You can use any credential of type `TokenCredential` here. `DefaultAzureCredential` is the most frictionless option for early development scenarios.

1. Create a new instance of your class that implements `IOidcCallback` and configure it with the **tenant ID** you recorded earlier in this guide.

    ```csharp
    string tenantId = "<microsoft-entra-tenant-id>";
    
    AzureIdentityTokenHandler tokenHandler = new(credential, tenantId);
    ```

1. Configure the credential for your settings using `MongoCredential.CreateOidcCredential` and passing in your custom handler callback implementation.

    ```csharp
    settings.Credential = MongoCredential.CreateOidcCredential(tokenHandler);
    ```

1. Freeze the settings and then create a new instance of `MongoClient`.

    ```csharp
    settings.Freeze();
    
    MongoClient client = new(settings);

    Console.WriteLine("Client created");
    ```
    
:::zone-end

:::zone pivot="programming-language-ts"

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
    const accountName: string = '<azure-cosmos-db-mongodb-vcore-account-name>';
    ```

1. TODO

    ```typescript
    const credential: TokenCredential = new DefaultAzureCredential();
    ```

1. TODO

    ```typescript
    const client = new MongoClient(
        `mongodb+srv://${accountName}.global.mongocluster.cosmos.azure.com/`, {
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

:::zone-end

:::zone pivot="programming-language-python"

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
    accountName = "<azure-cosmos-db-mongodb-vcore-account-name>"
    ```

1. TODO

    ```python
    credential = DefaultAzureCredential()
    authProperties = {"OIDC_CALLBACK": AzureIdentityTokenCallback(credential)}
    ```

1. TODO

    ```python
    client = MongoClient(
        f"mongodb+srv://{accountName}.global.mongocluster.cosmos.azure.com/",
        connectTimeoutMS=120000,
        tls=True,
        retryWrites=True,
        authMechanism="MONGODB-OIDC",
        authMechanismProperties=authProperties
    )
    
    print("Client created")
    ```

:::zone-end

:::zone pivot="programming-language-java

1. TODO

    ```java
    import java.util.concurrent.TimeUnit;
    
    import org.bson.Document;
    import org.bson.conversions.Bson;
    
    import com.azure.core.credential.TokenCredential;
    import com.azure.core.credential.TokenRequestContext;
    import com.azure.identity.DefaultAzureCredentialBuilder;
    import com.mongodb.MongoClientSettings;
    import com.mongodb.MongoCredential;
    import com.mongodb.MongoCredential.OidcCallbackContext;
    import com.mongodb.MongoCredential.OidcCallbackResult;
    import com.mongodb.client.MongoClient;
    import com.mongodb.client.MongoClients;
    import com.mongodb.client.MongoCollection;
    import com.mongodb.client.MongoDatabase;
    import com.mongodb.client.model.Filters;
    import com.mongodb.client.model.ReplaceOptions;
    import com.mongodb.client.result.UpdateResult;
    ```

1. TODO

    ```java
    TokenCredential credential = new DefaultAzureCredentialBuilder().build();

    MongoCredential.OidcCallback oidcCallback = new MongoCredential.OidcCallback() {
        @Override
        public OidcCallbackResult onRequest(OidcCallbackContext context) {
            TokenRequestContext tokenRequestContext = new TokenRequestContext()
                    .addScopes("https://ossrdbms-aad.database.windows.net/.default");
            String token = credential.getTokenSync(tokenRequestContext).getToken();
            return new OidcCallbackResult(token);
        }
    };

    MongoCredential mongoCredential = MongoCredential.createOidcCredential(null)
            .withMechanismProperty("OIDC_CALLBACK", oidcCallback);

    String accountName = "<azure-cosmos-db-mongodb-vcore-cluster-name>";
    String host = accountName + ".global.mongocluster.cosmos.azure.com";

    MongoClientSettings settings = MongoClientSettings.builder()
            .applyToClusterSettings(builder -> builder
                    .srvHost(host))
            .applyToSocketSettings(builder -> builder
                    .connectTimeout(2, TimeUnit.MINUTES))
            .applyToSslSettings(builder -> builder
                    .enabled(true))
            .retryWrites(true)
            .credential(mongoCredential)
            .build();

    MongoClient client = MongoClients.create(settings);

    System.out.println("Client created");
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

:::zone-end

:::zone pivot="programming-language-go

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

:::zone-end

:::zone pivot="programming-language-rust

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

:::zone-end

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

:::zone pivot="programming-language-csharp"

1. Represent your documents by creating a custom record type in its own file.

    ```csharp
    public record Product(
        string id,
        string category,
        string name,
        int quantity,
        decimal price,
        bool clearance
    );
    ```

    > [!TIP]
    > For illustrative purposes, this struct is named `Product`. The rest of this guide assumes you have this struct already defined.

1. Return back to the *Program.cs* file.

1. Get a pointer to your database using `MongoClient.GetDatabase`.

    ```csharp
    string databaseName = "<database-name>";
    
    IMongoDatabase database = client.GetDatabase(databaseName);

    Console.WriteLine("Database pointer created"); 
    ```

1. Then, use the database pointer to get a pointer to your collection using `IMongoDatabase.GetCollection<>`.

    ```csharp
    string collectionName = "<collection-name>";
    
    IMongoCollection<Product> collection = database.GetCollection<Product>(collectionName);

    Console.WriteLine("Collection pointer created"); 
    ```

1. Create and **upsert** two documents using the `IMongoCollection<>.ReplaceOneAsync` method.

    ```csharp
    Product classicSurfboard = new(
        id: "bbbbbbbb-1111-2222-3333-cccccccccccc",
        category: "gear-surf-surfboards",
        name: "Kiama Classic Surfboard",
        quantity: 25,
        price: 790.00m,
        clearance: false
    );
    
    Product paddleKayak = new(
        id: "cccccccc-2222-3333-4444-dddddddddddd",
        category: "gear-paddle-kayaks",
        name: "Lastovichka Paddle Kayak",
        quantity: 10,
        price: 599.99m,
        clearance: true
    );
    
    await collection.ReplaceOneAsync<Product>(
        doc => doc.id == classicSurfboard.id,
        classicSurfboard,
        new ReplaceOptions { IsUpsert = true }
    );
    
    Console.WriteLine($"Upserted document:\t{classicSurfboard.id}");
    
    await collection.ReplaceOneAsync<Product>(
        doc => doc.id == paddleKayak.id,
        paddleKayak,
        new ReplaceOptions { IsUpsert = true }
    );
    
    Console.WriteLine($"Upserted document:\t{paddleKayak.id}");
    ```

1. Read a single document from the collection using `IMongoCollection<>.Find` and `IFindFluent<,>.SingleAsync`. Use a filter to specify the specific document you would like to find.

    ```csharp
    Product document = await collection.Find(
        doc => doc.id == "cccccccc-2222-3333-4444-dddddddddddd"
    ).SingleAsync();
    
    Console.WriteLine($"Found document:\t{document.name}");
    ```

1. Query for all documents that match a filter using the same `Find` method. Use a filter to define a specific property (like `category`) and a specific value (like `gear-surf-surfboards`). Enumerate the results using `IFindFluent<,>.ToListAsync`.

    ```csharp
    List<Product> documents = await collection.Find(
        doc => doc.category == "gear-surf-surfboards"
    ).ToListAsync();
    
    foreach (Product doc in documents)
    {
        Console.WriteLine($"Queried document:\t{doc}");
    }
    ```

1. Delete a specific document from the collection using `IMongoCollection<>.DeleteOneAsync` and a filter.

    ```csharp
    await collection.DeleteOneAsync(
        doc => doc.id == "bbbbbbbb-1111-2222-3333-cccccccccccc"
    );
    
    Console.WriteLine($"Deleted document");
    ```

1. **Save** all of the code files in the project.

1. Run the project using `dotnet run`

    ```csharp
    dotnet run
    ```

1. Observe the output from the running application.

    ```output
    Client created
    Database pointer created
    Collection pointer created
    Upserted document:      bbbbbbbb-1111-2222-3333-cccccccccccc
    Upserted document:      cccccccc-2222-3333-4444-dddddddddddd
    Found document: Lastovichka Paddle Kayak
    Queried document:       Product { id = bbbbbbbb-1111-2222-3333-cccccccccccc, category = gear-surf-surfboards, name = Kiama Classic Surfboard, quantity = 25, price = 790.00, clearance = False }
    Deleted document
    ```

:::zone-end

:::zone pivot="programming-language-ts"

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

:::zone-end

:::zone pivot="programming-language-python"

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

:::zone-end

:::zone pivot="programming-language-java

1. TODO

    ```java
    MongoDatabase database = client.getDatabase("<database-name>");

    System.out.println("Database pointer created");

    MongoCollection<Document> collection = database.getCollection("<collection-name>");

    System.out.println("Collection pointer created");

    Document document = new Document()
            .append("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb")
            .append("category", "gear-surf-surfboards")
            .append("name", "Yamba Surfboard")
            .append("quantity", 12)
            .append("price", 850.00)
            .append("clearance", false);

    Bson match = Filters.eq("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb");

    ReplaceOptions options = new ReplaceOptions().upsert(true);
    UpdateResult result = collection.replaceOne(match, document, options);

    System.out.println("Document upserted with _id:\\t" + result.getUpsertedId().asString().getValue());

    Bson filter = Filters.eq("_id", "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb");

    collection.find(filter).forEach(doc -> {
        System.out.println("Read document _id:\\t" + doc.toJson());
    });

    Bson query = Filters.eq("category", "gear-surf-surfboards");

    collection.find(query).forEach(doc -> {
        System.out.println("Found document:\\t" + doc.toJson());
    });

    client.close();

    System.out.println("Client closed");
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

1. TODO

    ```java
    
    ```

:::zone-end

:::zone pivot="programming-language-go

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

1. TODO

    ```go
    
    ```

:::zone-end

:::zone pivot="programming-language-rust

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

1. TODO

    ```rust
    
    ```

:::zone-end

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)

:::zone pivot="programming-language-csharp"

- [.NET web application template](quickstart-dotnet.md)

:::zone-end

:::zone pivot="programming-language-ts"

- [TODO](about:blank)

:::zone-end

:::zone pivot="programming-language-python"

- [TODO](about:blank)

:::zone-end

:::zone pivot="programming-language-java"

- [TODO](about:blank)

:::zone-end

:::zone pivot="programming-language-go"

- [TODO](about:blank)

:::zone-end

:::zone pivot="programming-language-rust"

- [TODO](about:blank)

:::zone-end
