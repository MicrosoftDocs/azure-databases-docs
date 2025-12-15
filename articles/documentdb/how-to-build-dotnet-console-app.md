---
title: Build a .NET console app
description: Connect to an Azure DocumentDB cluster by using a .NET console application in your preferred developer language.
author: seesharprun
ms.author: sidandrews
ms.reviewer: nlarin
ms.topic: how-to
ms.date: 07/21/2025
ms.custom:
  - devx-track-dotnet
  - build-2025
ai-usage: ai-assisted
# Customer Intent: As a database developer, I want to build a .NET console application to quickly and securely connect to and query my database and collections.
---

# Build a .NET console app with Azure DocumentDB

[!INCLUDE[Developer console app selector](includes/selector-build-console-app-dev.md)]

This guide demonstrates how to build a .NET console application to connect to an Azure DocumentDB cluster. You set up your development environment, use the `Azure.Identity` library from the Azure SDK for .NET to authenticate, and interact with the database to create, query, and update documents.

## Prerequisites

[!INCLUDE[Prerequisite - Existing cluster](includes/prerequisite-existing-cluster.md)]

[!INCLUDE[External - Azure CLI prerequisites](~/reusable-content/azure-cli/azure-cli-prepare-your-environment-no-header.md)]

- Microsoft Entra authentication configured for the cluster with your identity granted `root` role.

    - To enable Microsoft Entra authentication, [review the configuration guide](how-to-connect-role-based-access-control.md).

- Latest version of [.NET](/dotnet).

## Retrieve Microsoft Entra tenant metadata

To retrieve an access token using the `TokenCredential` class in `Azure.Identity`, you need the unique identifier for the Microsoft Entra tenant. In this prerequisite step, use the Azure CLI to retrieve and record the `tenantId` value.

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
    string clusterName = "<azure-documentdb-cluster-name>";
    
    MongoUrl url = MongoUrl.Create($"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/");
    ```

1. Configure a new `MongoSettings` instance using the `MongoUrl` created in the previous steps and the standard best practice configuration for Azure DocumentDB.

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

- [Microsoft Entra authentication overview](how-to-connect-role-based-access-control.md)
- [.NET web application template](quickstart-dotnet.md)
- [Microsoft Entra configuration for cluster](how-to-connect-role-based-access-control.md)
