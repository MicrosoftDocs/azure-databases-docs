---

title: Quickstart - Vector Search with .NET
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to use vector search in Azure Cosmos DB for MongoDB vCore with .NET. Store and query vector data efficiently in your applications. 
author: alexwolfmsft
ms.author: alexwolf
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.devlang: csharp
ms.topic: quickstart-sdk
ms.date: 09/11/2025
ms.custom: devx-track-dotnet, devx-track-dotnet-ai
appliesto:
  - ✅ MongoDB (vCore)
# CustomerIntent: As a developer, I want to learn how to use vector search in .NET applications with Azure Cosmos DB for MongoDB (vCore).
---
# Quickstart: Vector search with .NET in Azure Cosmos DB for MongoDB (vCore)

Learn to use vector search in Azure Cosmos DB for MongoDB (vCore) with the .NET MongoDB driver to store and query vector data efficiently.

This quickstart provides a guided tour of key vector search techniques using a [.NET sample app](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/mongo-vcore-vector-search-dotnet) on GitHub.

The app uses a sample hotel dataset in a JSON file with pre-calculated vectors from the `text-embedding-ada-002` model, though you can also generate the vectors yourself. The hotel data includes hotel names, locations, descriptions, and vector embeddings.

## Prerequisites

[!INCLUDE[Prerequisites - Azure subscription](includes/prereq-azure-subscription.md)]
- [Visual Studio Code](https://code.visualstudio.com/download) or [Visual Studio](https://visualstudio.microsoft.com/)
    - [DocumentDB extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
    - [C# extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp)
- [Azure CLI](/cli/azure/install-azure-cli)
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- [Azure OpenAI resource](/azure/ai-foundry/openai) with:
    - [Role Based Access Control (RBAC) enabled](/azure/developer/ai/keyless-connections)
    - `text-embedding-ada-002` model deployed
- [Cosmos DB for MongoDB (vCore) resource](quickstart-portal.md) with:
    - [Role Based Access Control (RBAC) enabled](how-to-configure-entra-authentication.md)
    - Firewall configured for your IP address

## App dependencies

The app uses the following NuGet packages:

- [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity): Azure Identity library for passwordless authentication with Microsoft Entra ID
- [`Azure.AI.OpenAI`](https://www.nuget.org/packages/Azure.AI.OpenAI): Azure OpenAI client library to communicate with AI models and create vector embeddings
- [`Microsoft.Extensions.Configuration`](https://www.nuget.org/packages/Microsoft.Extensions.Configuration): Configuration management for app settings
- [`MongoDB.Driver`](https://www.nuget.org/packages/MongoDB.Driver): Official MongoDB .NET driver for database connectivity and operations
- [`Newtonsoft.Json`](https://www.nuget.org/packages/Newtonsoft.Json): Popular JSON serialization and deserialization library

## Configure and run the app

Complete the following steps to configure the app with your own values and run searches against your Azure Cosmos DB for MongoDB (vCore) cluster.

### Configure the app

Update the `appsettings.json` placeholder values with your own:

:::code language="json" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-dotnet/appsettings.json" :::

### Authenticate to Azure

The sample app uses passwordless authentication via `DefaultAzureCredential` and Microsoft Entra ID. [Sign in to Azure using a supported tool](/dotnet/azure/sdk/authentication/credential-chains?tabs=dac#defaultazurecredential-overview) such as the Azure CLI or Azure PowerShell before you run the application so it can access Azure resources securely.

> [!NOTE]
> Ensure your signed-in identity has the required data plane roles on both the Azure Cosmos DB for MongoDB (vCore) account and the Azure OpenAI resource.

### [Azure CLI](#tab/azure-cli)

```bash
az login
```

### [Azure Developer CLI](#tab/azure-developer-cli)

```bash
azd auth login
```

### [Azure PowerShell](#tab/azure-powershell)

```powershell
Connect-AzAccount
```

---

### Build and run the project

The sample app populates vectorized sample data in a MongoDB collection and lets you run different types of search queries. 

#### [DiskANN](#tab/tab-diskann)

1. Use the `dotnet run` command to start the app:

    ```bash
    dotnet run
    ```
    
    The app prints a menu for you to select database and search options:
    
    ```output
    === Cosmos DB Vector Samples Menu ===
    Please enter your choice (0-5):
    1. Create embeddings for data
    2. Show all database indexes
    3. Run IVF vector search
    4. Run HNSW vector search
    5. Run DiskANN vector search
    0. Exit
    ```

1. Type `5` and press enter.

    After the app populates the database and runs the search, you see the top five hotels that match the selected vector search query and their similarity scores.
    
    The app logging and output show:
    - Collection creation and data insertion status
    - Vector index creation confirmation
    - Search results with hotel names, locations, and similarity scores
    
    Example output (shortened for brevity):
    
    ```output
    MongoDB client initialized with passwordless authentication
    Starting DiskANN vector search workflow
    Collection is empty, loading data from file
    Successfully loaded 50 documents into collection
    Creating vector index 'vectorIndex_diskann'
    Vector index 'vectorIndex_diskann' is ready for DiskANN search
    Executing DiskANN vector search for top 5 results
    
    Search Results (5 found using DiskANN):
    1. Roach Motel (Similarity: 0.8399)
    2. Royal Cottage Resort (Similarity: 0.8385)
    3. Economy Universe Motel (Similarity: 0.8360)
    4. Foot Happy Suites (Similarity: 0.8354)
    5. Country Comfort Inn (Similarity: 0.8346)
    ```

#### [IVF](#tab/tab-ivf)

1. Use the `dotnet run` command to start the app:

    ```bash
    dotnet run
    ```
    
    The app prints a menu for you to select database and search options:
    
    ```output
    === Cosmos DB Vector Samples Menu ===
    Please enter your choice (0-5):
    1. Create embeddings for data
    2. Show all database indexes
    3. Run IVF vector search
    4. Run HNSW vector search
    5. Run DiskANN vector search
    0. Exit
    ```

1. Type `3` and press enter.

    After the app populates the database and runs the search, you see the top five hotels that match the selected vector search query and their similarity scores.
    
    The app logging and output show:
    - Collection creation and data insertion status
    - Vector index creation confirmation
    - Search results with hotel names, locations, and similarity scores
    
    Example output (shortened for brevity):
    
    ```output
    MongoDB client initialized with passwordless authentication
    Starting IVF vector search workflow
    Collection is empty, loading data from file
    Successfully loaded 50 documents into collection
    Creating vector index 'vectorIndex_ivf'
    Vector index 'vectorIndex_ivf' is ready for IVF search
    Executing IVF vector search for top 5 results
    
    Search Results (5 found using IVF):
    1. Roach Motel (Similarity: 0.8399)
    2. Royal Cottage Resort (Similarity: 0.8385)
    3. Economy Universe Motel (Similarity: 0.8360)
    4. Foot Happy Suites (Similarity: 0.8354)
    5. Country Comfort Inn (Similarity: 0.8346)
    ```

#### [HNSW](#tab/tab-hnsw)

1. Use the `dotnet run` command to start the app:

    ```bash
    dotnet run
    ```
    
    The app prints a menu for you to select database and search options:
    
    ```output
    === Cosmos DB Vector Samples Menu ===
    Please enter your choice (0-5):
    1. Create embeddings for data
    2. Show all database indexes
    3. Run IVF vector search
    4. Run HNSW vector search
    5. Run DiskANN vector search
    0. Exit
    ```

1. Type `4` and press enter.

    After the app populates the database and runs the search, you see the top five hotels that match the selected vector search query and their similarity scores.
    
    The app logging and output show:
    - Collection creation and data insertion status
    - Vector index creation confirmation
    - Search results with hotel names, locations, and similarity scores
    
    Example output (shortened for brevity):
    
    ```output
    MongoDB client initialized with passwordless authentication
    Starting HNSW vector search workflow
    Collection is empty, loading data from file
    Successfully loaded 50 documents into collection
    Creating vector index 'vectorIndex_hnsw'
    Vector index 'vectorIndex_hnsw' is ready for HNSW search
    Executing HNSW vector search for top 5 results
    
    Search Results (5 found using HNSW):
    1. Roach Motel (Similarity: 0.8399)
    2. Royal Cottage Resort (Similarity: 0.8385)
    3. Economy Universe Motel (Similarity: 0.8360)
    4. Foot Happy Suites (Similarity: 0.8354)
    5. Country Comfort Inn (Similarity: 0.8346)
    ```

----

## Explore the app code

The following sections provide details about the most important services and code in the sample app. [Visit the GitHub repo](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/mongo-vcore-vector-search-dotnet) to explore the full app code.

### Explore the search service

The `VectorSearchService` orchestrates an end‑to‑end vector similarity search using IVF, HNSW, and DiskANN search techniques with Azure OpenAI embeddings.

:::code language="csharp" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-dotnet/services/vectorsearchservice.cs" :::

In the preceding code, the `VectorSearchService` performs the following tasks:

- Determines the collection and index names based on the requested algorithm
- Creates or gets the MongoDB collection and loads JSON data if it's empty
- Builds the algorithm-specific index options (IVF / HNSW / DiskANN) and ensures the vector index exists
- Generates an embedding for the configured query via Azure OpenAI
- Constructs and runs the aggregation search pipeline
- Deserializes and prints the results

### Explore the Azure Cosmos DB for MongoDB (vCore) service

The `MongoDbService` manages interactions with Azure Cosmos DB for MongoDB (vCore) to handle tasks like loading data, vector index creation, index listing, and bulk inserts for hotel vector search.

:::code language="csharp" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-dotnet/services/MongoDbService.cs" :::

In the preceding code, the `MongoDbService` performs the following tasks:

- Reads configuration and builds a passwordless client with Azure credentials
- Provides database or collection references on demand
- Creates a vector search index only if it doesn't already exist
- Lists all non-system databases, their collections, and each collection's indexes
- Inserts sample data if the collection is empty and adds supporting indexes

## View and manage data in Visual Studio Code

1. Install the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) and [C# extension](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp) in Visual Studio Code.
1. Connect to your Azure Cosmos DB account using the DocumentDB extension.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" lightbox="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" alt-text="Screenshot of DocumentDB extension showing the Cosmos DB Mongo (vCore) collection.":::

## Clean up resources

Delete the resource group, Azure Cosmos DB for MongoDB (vCore) cluster, and Azure OpenAI resource when you no longer need them to avoid unnecessary costs.

## Related content

- [Vector store in Azure Cosmos DB for MongoDB vCore](vector-search.md)
- [Support for geospatial queries](geospatial-support.md)
- [How to build a .NET console app](how-to-build-dotnet-console-app.md)
- [.NET MongoDB Driver documentation](https://docs.mongodb.com/drivers/csharp/)
