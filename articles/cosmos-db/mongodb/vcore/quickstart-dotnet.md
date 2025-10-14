---
title: Quickstart - .NET driver
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Deploy a .NET web application that uses the official MongoDB driver for .NET to interact with Azure Cosmos DB for MongoDB (vCore) data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.devlang: csharp
ms.topic: quickstart-sdk
ms.date: 06/11/2025
ms.custom: devx-track-csharp, devx-track-dotnet, devx-track-extended-azdevcli
appliesto:
  - ✅ MongoDB (vCore)
# CustomerIntent: As a developer, I want to learn the basics of the .NET library so that I can build applications with Azure Cosmos DB for MongoDB (vCore).
---

# Quickstart: Use Azure Cosmos DB for MongoDB vCore with MongoDB driver for .NET

[!INCLUDE[Developer Quickstart selector](includes/selector-dev-quickstart.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for MongoDB vCore application using .NET. Azure Cosmos DB for MongoDB vCore is a schemaless data store allowing applications to store unstructured documents in the cloud with MongoDB libraries. You learn how to create documents and perform basic tasks within your Azure Cosmos DB resource using .NET.

[Library source code](https://github.com/mongodb/mongo-csharp-driver) | [Package (NuGet)](https://www.nuget.org/packages/MongoDB.Driver) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

[!INCLUDE[Prerequisites - Developer Quickstart](includes/prereq-dev-quickstart.md)]

- .NET SDK 9.0

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for MongoDB vCore cluster and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-mongodb-vcore-dotnet-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the cluster using `azd up`. The Bicep templates also deploy a sample web application.

    ```azurecli
    azd up
    ```

1. During the provisioning process, select your subscription, desired location, and target resource group. Wait for the provisioning process to complete. The process can take **approximately five minutes**.

1. Once the provisioning of your Azure resources is done, a URL to the running web application is included in the output.

    ```output
    Deploying services (azd deploy)
    
      (✓) Done: Deploying service web
    - Endpoint: <https://[container-app-sub-domain].azurecontainerapps.io>
    
    SUCCESS: Your application was provisioned and deployed to Azure in 5 minutes 0 seconds.
    ```

1. Use the URL in the console to navigate to your web application in the browser. Observe the output of the running app.

:::image type="content" source="media/quickstart-dotnet/running-application.png" alt-text="Screenshot of the running sample dashboard web application.":::

### Install the client library

The client library is available through NuGet, as the `MongoDB.Driver` package. For Microsoft Entra authentication, use the `Azure.Identity` package from the Azure SDK for .NET.

1. Open a terminal and navigate to the `/src/web` folder.

    ```bash
    cd ./src/web
    ```

1. If not already installed, install the `MongoDB.Driver` package using `dotnet add package`.

    ```bash
    dotnet add package MongoDB.Driver
    ```

1. If not already installed, install the `Azure.Identity` package.

    ```bash
    dotnet add package Azure.Identity
    ```

1. Open and review the **src/api/Microsoft.Learn.AzureCosmosDBMongoDBQuickstart.Api.csproj** file to validate that both package entries exist.

### Import libraries

Import the following namespaces into your application code:

| | Package | Source |
| --- | --- | --- |
| **`Azure.Core`** | `Azure.Identity` | Azure SDK for .NET |
| **`Azure.Identity`** | `Azure.Identity` | Azure SDK for .NET |
| **`MongoDB.Driver`** | `MongoDB.Driver` | Official MongoDB driver for .NET |
| **`MongoDB.Driver.Authentication.Oidc`** | `MongoDB.Driver` | Official MongoDB driver for .NET |

```csharp
using Azure.Core;
using Azure.Identity;

using MongoDB.Driver;
using MongoDB.Driver.Authentication.Oidc;
```

## Object model

| Name | Description |
| --- | --- |
| `MongoClient` | Type used to connect to MongoDB. |
| `Database` | Represents a database on the cluster. |
| `Collection` | Represents a collection within a database on the cluster. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Get a document](#read-a-document)
- [Query documents](#query-documents)
- [Delete a document](#delete-a-document)

The sample code in the template uses a database named `cosmicworks` and collection named `products`. The `products` collection contains details such as name, category, quantity, and a unique identifier for each product. The collection uses the `/category` property as a shard key.

### Authenticate the client

While Microsoft Entra authentication for Azure Cosmos DB for MongoDB vCore can use well known `TokenCredential` types, you must implement a custom token handler. This sample implementation can be used to create a `MongoClient` with support for standard Microsoft Entra authentication of many identity types.

1. First, create a new class in a separate file that implements `IOidcCallback` interface.

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

1. Create a new instance of your custom handler class passing in a new instance of the `DefaultAzureCredential` type and your **tenant ID**.

    ```csharp
    DefaultAzureCredential credential = new();

    string tenantId = "<microsoft-entra-tenant-id>";
    
    AzureIdentityTokenHandler tokenHandler = new(credential, tenantId);
    ```

1. Build an instance of `MongoUrl` using the endpoint and scheme for your recently deployed Azure Cosmos DB for MongoDB vCore instance.

    ```csharp
    string clusterName = "<azure-cosmos-db-mongodb-vcore-cluster-name>";
    
    MongoUrl url = MongoUrl.Create($"mongodb+srv://{clusterName}.global.mongocluster.cosmos.azure.com/");
    ```

1. Configure your `MongoClient` instance using known best practice configuration options for Azure Cosmos DB for MongoDB vCore and the custom `IOidcCallback` implementation.

    ```csharp
    MongoClientSettings settings = MongoClientSettings.FromUrl(url);
    
    settings.UseTls = true;
    settings.RetryWrites = false;
    settings.MaxConnectionIdleTime = TimeSpan.FromMinutes(2);
    settings.Credential = MongoCredential.CreateOidcCredential(tokenHandler);
    settings.Freeze();
    
    MongoClient client = new(settings);
    ```

### Get a database

This sample creates an instance of the `IMongoDatabase` interface using the `GetDatabase` method of the `MongoClient` class.

```csharp
IMongoDatabase database = client.GetDatabase("<database-name>");
```

### Get a collection

This sample creates an instance of the generic `IMongoCollection<>` interface using the `GetCollection<>` generic method of the `IMongoDatabase` interface. The generic interface and method both uses a type named `Product` defined in another class.

```csharp
IMongoCollection<Product> collection = database.GetCollection<Product>("<collection-name>");
```

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

### Create a document

Create a document in the collection using `collection.ReplaceOneAsync<>` with the generic `Product` type parameter. This method "upserts" the document effectively replacing it if it already exists in the collection.

```csharp
Product document = new(
    id: "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    category: "gear-surf-surfboards",
    name: "Yamba Surfboard",
    quantity: 12,
    price: 850.00m,
    clearance: false
);

await collection.ReplaceOneAsync<Product>(
    doc => doc.id == document.id,
    document,
    new ReplaceOptions { IsUpsert = true }
);
```

### Read a document

Perform a read operation by using both the unique identifier (`id`) for the documents. Use `collection.FindAsync<>` with the generic `Product` type parameter to efficiently retrieve the specific document.

```csharp
Product? document = await collection.Find(
    doc => doc.id == "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
).SingleOrDefaultAsync();
```

### Query documents

Perform a query over multiple documents in a container using `collection.AsQueryable()` and language-integrated query (LINQ). This query finds all documents within a specified category (shard key).

```csharp
List<Product> documents = await collection.Find(
    filter: doc => doc.category == "gear-surf-surfboards"
).ToListAsync();

foreach (Product document in documents)
{
    // Do something with each document
}
```

### Delete a document

Delete a document by sending a filter for the unique identifier of the document. Use `collection.DeleteOneAsync<>` to asynchronously remove the document from the collection.

```csharp
await collection.DeleteOneAsync(
    doc => doc.id == "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb"
);
```

## Explore your data

[!INCLUDE[Section - Visual Studio Code extension exploration](includes/section-vscode-extension-explore.md)]

## Clean up resources

[!INCLUDE[Section - Quickstart clean up](includes/section-quickstart-clean-up.md)]

## Related content

- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
