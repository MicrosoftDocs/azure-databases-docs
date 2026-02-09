---

title: Quickstart - CosmosDB vector search with .NET
description: Learn how to use vector search in Azure Cosmos DB with .NET. Store and query vector data efficiently in your applications. 
author: alexwolfmsft
ms.author: alexwolf
ms.reviewer: khelanmodi
ms.devlang: csharp
ms.topic: quickstart-sdk
ms.date: 02/06/2026
ms.custom:
  - devx-track-dotnet
  - devx-track-dotnet-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in .NET applications with Azure Cosmos DB.
---

# Quickstart: Vector search with .NET in Azure Cosmos DB

Learn to use vector search in Azure Cosmos DB to store and query vector data efficiently.

This quickstart provides a guided tour of key vector search techniques using a [.NET sample app](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/nosql-vector-search-dotnet) on GitHub.

The app uses a sample hotel dataset in a JSON file with pre-calculated vectors from the `text-embedding-3-small` model, though you can also generate the vectors yourself. The hotel data includes hotel names, locations, descriptions, and vector embeddings.

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- [C# extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp)

## App dependencies

The app uses the following NuGet packages:

- [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity): Azure Identity library for passwordless authentication with Microsoft Entra ID
- [`Azure.AI.OpenAI`](https://www.nuget.org/packages/Azure.AI.OpenAI): Azure OpenAI client library to communicate with AI models and create vector embeddings
- [`Microsoft.Extensions.Configuration`](https://www.nuget.org/packages/Microsoft.Extensions.Configuration): Configuration management for app settings
- [`Microsoft.Azure.Cosmos`](https://www.nuget.org/packages/Microsoft.Azure.Cosmos): Azure Cosmos DB client library for database connectivity and operations
- [`Newtonsoft.Json`](https://www.nuget.org/packages/Newtonsoft.Json): Popular JSON serialization and deserialization library

### Authenticate to Azure

The sample app uses passwordless authentication via `DefaultAzureCredential` and Microsoft Entra ID. [Sign in to Azure using a supported tool](/dotnet/azure/sdk/authentication/credential-chains?tabs=dac#defaultazurecredential-overview) such as the Azure CLI or Azure PowerShell before you run the application so it can access Azure resources securely.

> [!NOTE]
> Ensure your signed-in identity has the required data plane roles on both the Azure Cosmos DB account and the Azure OpenAI resource.

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

## Provision and configure the app resources

To run the .NET app, you'll need to provision the required Azure resources and configure the sample app to connect to them. This project is configured to use the Azure Developer CLI (`azd`) to provision the required Azure resources for you automatically.

### Provision the resources

To provision resources:

1. Open a terminal in the root folder of this repository (where `azure.yml` is located).
2. Run the following command:

    ```bash
    azd up
    ```

Follow the prompts to select your Azure subscription and environment.

**What is provisioned:**

* **Azure Cosmos DB for NoSQL**: Serverless account with the `Hotels` database and containers
* **Azure OpenAI**: Resource with deployments for:
  * Embedding model: `text-embedding-3-small`
  * Chat model: `gpt-4o-mini`
* **Managed Identity**: User-assigned identity for secure access.
* RBAC assignments for Keyless authentication.

### Configure the app

Update the `appsettings.json` placeholder values with your own:

:::code language="json" source="~/cosmos-db-vector-samples/nosql-vector-search-dotnet/appsettings.json" :::


## Build and run the project

The sample app populates vectorized sample data in a CosmosDB database and lets you run different types of search queries. Each query uses a different container within the database. 

#### [Flat](#tab/tab-flat)

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
    3. Run Flat vector search
    4. Run Quantized Flat vector search
    5. Run DiskANN vector search
    0. Exit
    ```

1. Type `3` and press enter.

    After the app populates the database and runs the search, you see the top five hotels that match the selected vector search query and their similarity scores.
    
    The app logging and output show:
    - Container creation and data insertion status
    - Vector index creation confirmation
    - Search results with hotel names, locations, and similarity scores
    
    Example output (shortened for brevity):
    
    ```output
    Starting Flat vector search workflow
    Container 'hotels_flat' checked
    Vector index ready.
    Executing Flat vector search for top 5 results
    
    Search Results (5 found using Flat):
    1. Royal Cottage Resort (Similarity: 0.4991)
    2. Country Comfort Inn (Similarity: 0.4786)
    3. Nordick's Valley Motel (Similarity: 0.4635)
    4. Economy Universe Motel (Similarity: 0.4461)
    5. Roach Motel (Similarity: 0.4388)
    ```

#### [QuantizedFlat](#tab/quantized-flat)

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
    3. Run Flat vector search
    4. Run Quantized Flat vector search
    5. Run DiskANN vector search
    0. Exit
    ```

1. Type `4` and press enter.

    After the app populates the database and runs the search, you see the top five hotels that match the selected vector search query and their similarity scores.
    
    The app logging and output show:
    - Container creation and data insertion status
    - Vector index creation confirmation
    - Search results with hotel names, locations, and similarity scores
    
    Example output (shortened for brevity):
    
    ```output
    Starting QuantizedFlat vector search workflow
    Container 'hotels_quantizedflat' checked
    Vector index ready.
    Executing QuantizedFlat vector search for top 5 results
    
    Search Results (5 found using QuantizedFlat):
    1. Royal Cottage Resort (Similarity: 0.4991)
    2. Country Comfort Inn (Similarity: 0.4786)
    3. Nordick's Valley Motel (Similarity: 0.4635)
    4. Economy Universe Motel (Similarity: 0.4461)
    5. Roach Motel (Similarity: 0.4388)
    ```

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
    3. Run Flat vector search
    4. Run Quantized Flat vector search
    5. Run DiskANN vector search
    0. Exit
    ```

1. Type `5` and press enter.

    After the app populates the database and runs the search, you see the top five hotels that match the selected vector search query and their similarity scores.
    
    The app logging and output show:
    - Container creation and data insertion status
    - Vector index creation confirmation
    - Search results with hotel names, locations, and similarity scores
    
    Example output (shortened for brevity):
    
    ```output
    Starting DiskANN vector search workflow
    Container 'hotels_quantizedflat' checked
    Vector index ready.
    Executing DiskANN vector search for top 5 results
    
    Search Results (5 found using HNSW):
    1. Royal Cottage Resort (Similarity: 0.4991)  
    2. Country Comfort Inn (Similarity: 0.4786)   
    3. Nordick's Valley Motel (Similarity: 0.4635)
    4. Economy Universe Motel (Similarity: 0.4461)
    5. Roach Motel (Similarity: 0.4388)
    ```

----

## Explore the app code

The following sections provide details about the most important services and code in the sample app. [Visit the GitHub repo](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/nosql-vector-search-dotnet) to explore the full app code.

### Explore the search service

The `VectorSearchService` orchestrates an end‑to‑end vector similarity search using IVF, HNSW, and DiskANN search techniques with Azure OpenAI embeddings.

:::code language="csharp" source="~/cosmos-db-vector-samples/nosql-vector-search-dotnet/services/vectorsearchservice.cs" :::

In the preceding code, the `VectorSearchService` performs the following tasks:

- Determines the container and index names based on the requested algorithm
- Creates or gets the Cosmos DB container and loads JSON data if it's empty
- Builds the algorithm-specific index options (IVF / HNSW / DiskANN) and ensures the vector index exists
- Generates an embedding for the configured query via Azure OpenAI
- Constructs and runs the aggregation search pipeline
- Deserializes and prints the results

### Explore the Azure Cosmos DB service

The `CosmosDBService` manages interactions with Azure Cosmos DB to handle tasks like loading data, vector index creation, index listing, and bulk inserts for hotel vector search.

:::code language="csharp" source="~/cosmos-db-vector-samples/nosql-vector-search-dotnet/services/CosmosDBService.cs" :::

In the preceding code, the `CosmosDBService` performs the following tasks:

- Reads configuration and builds a passwordless client with Azure credentials
- Provides database or container references on demand
- Creates a vector search index only if it doesn't already exist
- Lists all non-system databases, their containers, and each container's indexes
- Inserts sample data if the contaienr is empty and adds supporting indexes

## View and manage data in Visual Studio Code

1. Install the [CosmosDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-CosmosDB) and [C# extension](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp) in Visual Studio Code.
1. Connect to your Azure Cosmos DB account using the CosmosDB extension.
1. View the data and indexes in the Hotels database.

## Clean up resources

Delete the resource group, Azure Cosmos DB cluster, and Azure OpenAI resource when you no longer need them to avoid unnecessary costs.

## Related content

- [Vector store in Azure Cosmos DB](vector-search.md)
