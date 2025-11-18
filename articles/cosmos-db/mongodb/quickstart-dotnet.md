---
title: Quickstart - .NET
titleSuffix: Azure Cosmos DB for MongoDB
description: Deploy a .NET web application that uses the client library for .NET to interact with Azure Cosmos DB for MongoDB data in this quickstart.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.devlang: csharp
ms.topic: quickstart-sdk
ms.date: 04/08/2025
ms.custom: devx-track-csharp, devx-track-dotnet, devx-track-extended-azdevcli, sfi-image-nochange
appliesto:
- ✅ MongoDB
# CustomerIntent: As a developer, I want to learn the basics of the .NET library so that I can build applications with Azure Cosmos DB for MongoDB.
---

# Quickstart: Use Azure Cosmos DB for MongoDB with .NET

[!INCLUDE[Developer Quickstart selector](includes/quickstart-dev-selector.md)]

In this quickstart, you deploy a basic Azure Cosmos DB for MongoDB application using Python. Azure Cosmos DB for MongoDB is a schemaless data store allowing applications to store unstructured documents in the cloud with MongoDB libraries. You learn how to create documents and perform basic tasks within your Azure Cosmos DB resource using Python.

[Library source code](https://github.com/mongodb/mongo-csharp-driver) | [Package (NuGet)](https://www.nuget.org/packages/MongoDB.Driver) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- Azure Developer CLI
- Docker Desktop
- .NET SDK 9.0

If you don't have an Azure account, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Initialize the project

Use the Azure Developer CLI (`azd`) to create an Azure Cosmos DB for Table account and deploy a containerized sample application. The sample application uses the client library to manage, create, read, and query sample data.

1. Open a terminal in an empty directory.

1. If you're not already authenticated, authenticate to the Azure Developer CLI using `azd auth login`. Follow the steps specified by the tool to authenticate to the CLI using your preferred Azure credentials.

    ```azurecli
    azd auth login
    ```

1. Use `azd init` to initialize the project.

    ```azurecli
    azd init --template cosmos-db-mongodb-dotnet-quickstart
    ```

1. During initialization, configure a unique environment name.

1. Deploy the Azure Cosmos DB account using `azd up`. The Bicep templates also deploy a sample web application.

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

:::image type="content" source="media/quickstart-dotnet/running-application.png" alt-text="Screenshot of the running web application.":::

### Install the client library

The client library is available through NuGet, as the `MongoDB.Driver` package.

1. Open a terminal and navigate to the `/src/web` folder.

    ```bash
    cd ./src/web
    ```

1. If not already installed, install the `MongoDB.Driver` package using `dotnet add package`.

    ```bash
    dotnet add package MongoDB.Driver
    ```

1. Open and review the **src/web/Microsoft.Samples.Cosmos.MongoDB.Quickstart.Web.csproj** file to validate that the `MongoDB.Driver` entry exists.

### Import libraries

Import the `MongoDB.Driver` namespace into your application code.

```csharp
using MongoDB.Driver;
```

## Object model

| Name | Description |
| --- | --- |
| [`MongoClient`](https://www.mongodb.com/docs/drivers/csharp/current/quick-start/) | Type used to connect to MongoDB. |
| `Database` | Represents a database in the account. |
| `Collection` | Represents a collection within a database in the account. |

## Code examples

- [Authenticate the client](#authenticate-the-client)
- [Get a database](#get-a-database)
- [Get a collection](#get-a-collection)
- [Create a document](#create-a-document)
- [Get a document](#read-a-document)
- [Query documents](#query-documents)

The sample code in the template uses a database named `cosmicworks` and collection named `products`. The `products` collection contains details such as name, category, quantity, and a unique identifier for each product. The collection uses the `/category` property as a shard key.

### Authenticate the client

This sample creates a new instance of the `MongoClient` class.

```csharp
string connectionString = "<azure-cosmos-db-for-mongodb-connection-string>";

MongoClient client = new(connectionString);
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

Create a document in the collection using `collection.ReplaceOneAsync<>` with the generic `Product` type parameter. This method "upserts" the item effectively replacing the item if it already exists.

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
    d => d.id == document.id,
    document,
    new ReplaceOptions { IsUpsert = true }
);
```

### Read a document

Perform a point read operation by using both the unique identifier (`id`) and shard key fields. Use `collection.FindAsync<>` with the generic `Product` type parameter to efficiently retrieve the specific item.

```csharp
IAsyncCursor<Product> documents = await collection.FindAsync<Product>(
    d => d.id == "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb" && d.category == "gear-surf-surfboards"
);

Product? document = await documents.SingleOrDefaultAsync();
```

### Query documents

Perform a query over multiple items in a container using `collection.AsQueryable()` and language-integrated query (LINQ). This query finds all items within a specified category (shard key).

```csharp
IQueryable<Product> documents = collection.AsQueryable().Where(
    d => d.category == "gear-surf-surfboards"
);

foreach (Product document in await documents.ToListAsync())
{
    // Do something with each item
}
```

### Explore your data

Use the Visual Studio Code extension for Azure Cosmos DB to explore your MongoDB data. You can perform core database operations including, but not limited to:

- Performing queries using a scrapbook or the query editor
- Modifying, updating, creating, and deleting documents
- Importing bulk data from other sources
- Managing databases and collections

For more information, see [How-to use Visual Studio Code extension to explore Azure Cosmos DB for MongoDB data](../visual-studio-code-extension.md?pivots=api-mongodb&tabs=MongoDB).

## Clean up resources

When you no longer need the sample application or resources, remove the corresponding deployment and all resources.

```azurecli
azd down --force --purge
```

## Related content

- [Node.js Quickstart](quickstart-nodejs.md)
- [Python Quickstart](quickstart-python.md)
