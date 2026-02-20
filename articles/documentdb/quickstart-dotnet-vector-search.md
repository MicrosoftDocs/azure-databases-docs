---

title: Quickstart - Vector Search with .NET
description: Learn how to use vector search in Azure DocumentDB with .NET. Store and query vector data efficiently in your applications. 
author: alexwolfmsft
ms.author: alexwolf
ms.reviewer: khelanmodi
ms.devlang: csharp
ms.topic: quickstart-sdk
ms.date: 02/20/2026
ai-usage: ai-assisted
ms.custom:
  - devx-track-dotnet
  - devx-track-dotnet-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in .NET applications with Azure DocumentDB.
---

# Quickstart: Vector search with .NET in Azure DocumentDB

Learn to use vector search in Azure DocumentDB with the .NET MongoDB driver to store and query vector data efficiently.

This quickstart provides a guided tour of key vector search techniques using a [.NET sample app](https://github.com/Azure-Samples/documentdb-samples/tree/main/ai/vector-search-dotnet) on GitHub.

The app uses a sample hotel dataset in a JSON file with pre-calculated vectors from the `text-embedding-3-small` model, though you can also generate the vectors yourself. The hotel data includes hotel names, locations, descriptions, and vector embeddings.

## Prerequisites

[!INCLUDE[Prerequisites - Vector Search Quickstart](includes/prerequisite-quickstart-vector-search-model.md)]

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later

    - [C# extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp)

## App dependencies

The app uses the following NuGet packages:

- [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity): Azure Identity library for passwordless authentication with Microsoft Entra ID
- [`Azure.AI.OpenAI`](https://www.nuget.org/packages/Azure.AI.OpenAI): Azure OpenAI client library to communicate with AI models and create vector embeddings
- [`Microsoft.Extensions.Configuration`](https://www.nuget.org/packages/Microsoft.Extensions.Configuration): Configuration management for app settings
- [`MongoDB.Driver`](https://www.nuget.org/packages/MongoDB.Driver): Official MongoDB .NET driver for database connectivity and operations
- [`Newtonsoft.Json`](https://www.nuget.org/packages/Newtonsoft.Json): Popular JSON serialization and deserialization library

## Configure and run the app

Complete the following steps to configure the app with your own values and run searches against your Azure DocumentDB cluster.

### Configure the app

Update the `appsettings.json` placeholder values with your own:

:::code language="json" source="~/documentdb-samples/ai/vector-search-dotnet/appsettings.json" :::

### Authenticate to Azure

The sample app uses passwordless authentication via `DefaultAzureCredential` and Microsoft Entra ID. [Sign in to Azure using a supported tool](/dotnet/azure/sdk/authentication/credential-chains?tabs=dac#defaultazurecredential-overview) such as the Azure CLI or Azure PowerShell before you run the application so it can access Azure resources securely.

> [!NOTE]
> Ensure your signed-in identity has the required data plane roles on both the Azure DocumentDB account and the Azure OpenAI resource.

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
    === DocumentDB Vector Samples Menu ===
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
    1. Royal Cottage Resort (Similarity: 0.4991)
    2. Country Comfort Inn (Similarity: 0.4786)
    3. Nordick's Valley Motel (Similarity: 0.4635)
    4. Economy Universe Motel (Similarity: 0.4461)
    5. Roach Motel (Similarity: 0.4388)
    ```

#### [IVF](#tab/tab-ivf)

1. Use the `dotnet run` command to start the app:

    ```bash
    dotnet run
    ```
    
    The app prints a menu for you to select database and search options:
    
    ```output
    === DocumentDB Vector Samples Menu ===
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
    1. Royal Cottage Resort (Similarity: 0.4991)
    2. Country Comfort Inn (Similarity: 0.4786)
    3. Nordick's Valley Motel (Similarity: 0.4635)
    4. Economy Universe Motel (Similarity: 0.4461)
    5. Roach Motel (Similarity: 0.4388)
    ```

#### [HNSW](#tab/tab-hnsw)

1. Use the `dotnet run` command to start the app:

    ```bash
    dotnet run
    ```
    
    The app prints a menu for you to select database and search options:
    
    ```output
    === DocumentDB Vector Samples Menu ===
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
    1. Royal Cottage Resort (Similarity: 0.4991)
    2. Country Comfort Inn (Similarity: 0.4786)
    3. Nordick's Valley Motel (Similarity: 0.4635)
    4. Economy Universe Motel (Similarity: 0.4461)
    5. Roach Motel (Similarity: 0.4388)
    ```

---

## Explore the app code

The following sections provide details about the most important services and code in the sample app. [Visit the GitHub repo](https://github.com/Azure-Samples/documentdb-samples/tree/main/ai/vector-search-dotnet) to explore the full app code.

### Explore the search service

The `VectorSearchService` orchestrates an end‑to‑end vector similarity search using IVF, HNSW, and DiskANN search techniques with Azure OpenAI embeddings.

:::code language="csharp" source="~/documentdb-samples/ai/vector-search-dotnet/services/vectorsearchservice.cs" :::

In the preceding code, the `VectorSearchService` performs the following tasks:

- Determines the collection and index names based on the requested algorithm
- Creates or gets the MongoDB collection and loads JSON data if it's empty
- Builds the algorithm-specific index options (IVF / HNSW / DiskANN) and ensures the vector index exists
- Generates an embedding for the configured query via Azure OpenAI
- Constructs and runs the aggregation search pipeline
- Deserializes and prints the results

### Explore the Azure DocumentDB service

The `MongoDbService` manages interactions with Azure DocumentDB to handle tasks like loading data, vector index creation, index listing, and bulk inserts for hotel vector search.

:::code language="csharp" source="~/documentdb-samples/ai/vector-search-dotnet/services/MongoDbService.cs" :::

In the preceding code, the `MongoDbService` performs the following tasks:

- Reads configuration and builds a passwordless client with Azure credentials
- Provides database or collection references on demand
- Creates a vector search index only if it doesn't already exist
- Lists all non-system databases, their collections, and each collection's indexes
- Inserts sample data if the collection is empty and adds supporting indexes

## View and manage data in Visual Studio Code

1. Install the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) and [C# extension](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp) in Visual Studio Code.
1. Connect to your Azure DocumentDB account using the DocumentDB extension.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" lightbox="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" alt-text="Screenshot of DocumentDB extension showing the DocumentDB collection.":::

## Clean up resources

Delete the resource group, Azure DocumentDB cluster, and Azure OpenAI resource when you no longer need them to avoid unnecessary costs.

## Related content

- [Vector store in Azure DocumentDB](vector-search.md)
- [Support for geospatial queries](geospatial-support.md)
