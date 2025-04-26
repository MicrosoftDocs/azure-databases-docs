---
title: Build a .NET console app
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Connect to an Azure Cosmos DB for MongoDB (vCore) cluster by using a console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: how-to
ms.date: 04/28/2025
ms.custom: devx-track-dotnet
ai-usage: ai-assisted
appliesto:
  - ✅ MongoDB (vCore)
# Customer Intent: As a database owner, I want to use Mongo Shell to connect to and query my database and collections.
---

# Build a .NET console app with Azure Cosmos DB for MongoDB vCore

In this guide, you build a console application to connect to an existing Azure Cosmos DB for MongoDB vCore cluster. This guide covers the required steps to configure the cluster for Microsoft Entra authentication and then to connect to the same cluster using the identity that you're currently signed-in with.

This guide uses the open-source `MongoDB.Driver` library from NuGet.

After authenticating, you can use this library to interact with Azure Cosmos DB for MongoDB vCore using the same methods and classes you would typically use to interact with any other MongoDB or DocumentDB instance.

## Prerequisites

- An existing Azure Cosmos DB for MongoDB (vCore) cluster.
- The latest version of the [Azure CLI](/cli/azure) in [Azure Cloud Shell](/azure/cloud-shell).
  - If you prefer to run CLI reference commands locally, sign in to the Azure CLI by using the [`az login`](/cli/azure/reference-index#az-login) command.
- Latest version of [.NET](/dotnet).

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

## Connect to the cluster

Now, use the `Azure.Identity` library to get a `TokenCredential` to use to connect to your cluster. The official MongoDB driver has a special interface that must be implemented to obtain tokens from Microsoft Entra for use when connecting to the cluster.

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
    

## Perform common operations

Finally, use the official library to perform common tasks with databases, collections, and documents. Here, you use the same classes and methods you would use to interact with MongoDB or DocumentDB to manage your collections and items.

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

## Related content

- [Microsoft Entra authentication overview](entra-authentication.md)
- [.NET web application template](quickstart-dotnet.md)
