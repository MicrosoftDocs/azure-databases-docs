---

title: Quickstart - Azure Cosmos DB vector search with Java
description: Use this quickstart to implement vector search in Azure Cosmos DB with Java. Store and query hotel data with embeddings.
author: diberry
ms.author: diberry
ms.reviewer: jcodella
ms.devlang: java
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: quickstart-sdk
ms.date: 03/26/2026
ai-usage: ai-assisted
ms.custom:
  - devx-track-extended-java
  - devx-track-extended-java-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Java applications with Azure Cosmos DB.
---

# Quickstart: Vector search with Java in Azure Cosmos DB

Use vector search in Azure Cosmos DB with the Java client library. Store and query vector data efficiently in your applications.

This quickstart uses a sample hotel dataset in a JSON file with vectors from the **text-embedding-3-small** model. The dataset includes hotel names, locations, descriptions, and vector embeddings.

Find the sample code with resource provisioning on [GitHub](https://github.com/Azure-Samples/cosmos-db-vector-samples).

## Prerequisites

- An Azure subscription
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

- An existing **Azure Cosmos DB** resource data plane access
  - If you don't have a resource, create a [new resource](https://portal.azure.com/#create/Microsoft.DocumentDB)
  - [Firewall configured to allow access to your client IP address](how-to-configure-firewall.md)
  - Role-based access control (RBAC) roles assigned:
    - **Cosmos DB Built-in Data Contributor** (data plane)
    - Role ID: `00000000-0000-0000-0000-000000000002`

- [Azure OpenAI resource](/azure/ai-foundry/openai/how-to/create-resource?pivots=cli#create-a-resource)
  - Custom domain configured
  - Role-based access control (RBAC) role assigned:
    - **Cognitive Services OpenAI User**
    - Role ID: `5e0bd9bd-7b93-4f28-af87-19fc36ad61bd`
  - `text-embedding-3-small` model deployed

- [Visual Studio Code](https://code.visualstudio.com/download)
  - [Cosmos DB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb)

- [Java 21+](/java/openjdk/download)
- [Maven 3.8+](https://maven.apache.org/download.cgi)

## Create data file with vectors

1. Create a new data directory for the hotels data file:

    ### [Linux/macOS](#tab/tab-data-linux)

    ```bash
    mkdir data
    ```

    ### [Windows](#tab/tab-data-windows)

    ```powershell
    New-Item -ItemType Directory -Force -Path data
    ```

    ---

1. Download the [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json) to your `data` directory:

    ### [Linux/macOS](#tab/tab-curl-linux)

    ```bash
    curl -o data/HotelsData_toCosmosDB_Vector.json https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json
    ```

    ### [Windows](#tab/tab-curl-windows)

    ```powershell
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json" -OutFile "data/HotelsData_toCosmosDB_Vector.json"
    ```

    ---

## Create a Java project

1. Create a new sibling directory for your project, at the same level as the data directory, and open it in Visual Studio Code:

    ```bash
    mkdir vector-search-quickstart
    cd vector-search-quickstart
    code .
    ```

1. Create a `pom.xml` file in the project root with the Maven configuration:

    :::code language="xml" source="~/cosmos-db-vector-samples/nosql-vector-search-java/pom.xml" :::

    Key dependencies:

    * **azure-identity** - Azure authentication library for passwordless (managed identity) connections
    * **azure-cosmos** - Azure Cosmos DB client library for database operations
    * **azure-ai-openai** - Azure OpenAI SDK for generating embeddings
    * **slf4j-nop** - Suppresses noisy SDK logging at runtime

1. Create the source directory structure:

    ### [Linux/macOS](#tab/tab-mkdir-linux)

    ```bash
    mkdir -p src/main/java/com/example/cosmos/vectorsearch
    ```

    ### [Windows](#tab/tab-mkdir-windows)

    ```powershell
    New-Item -ItemType Directory -Force -Path src\main\java\com\example\cosmos\vectorsearch | Out-Null
    ```

    ---

1. Create a `.env` file in your project root for environment variables:

    ```ini
    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    AZURE_OPENAI_EMBEDDING_API_VERSION=2024-08-01-preview
    AZURE_OPENAI_EMBEDDING_ENDPOINT=

    # Cosmos DB configuration
    AZURE_COSMOSDB_ENDPOINT=

    # Data file
    DATA_FILE_WITH_VECTORS=../data/HotelsData_toCosmosDB_Vector.json
    FIELD_TO_EMBED=Description
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536

    # Vector search algorithm: diskann or quantizedflat
    VECTOR_ALGORITHM=diskann
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL
    - `AZURE_COSMOSDB_ENDPOINT`: Your Azure Cosmos DB endpoint URL

    > [!NOTE]
    > The Java sample uses `System.getenv()` to read environment variables. You must export these variables in your shell session or use `azd env get-values` to set them. The `.env` file serves as a reference template — it is not loaded automatically by the application.

## Understand the document schema

Before building the application, understand how vectors are stored in Azure Cosmos DB documents. Each hotel document contains:

- **Standard fields**: `HotelId`, `HotelName`, `Description`, `Category`, etc.
- **Vector field**: `DescriptionVector` - an array of 1536 floating-point numbers representing the semantic meaning of the hotel description

Here's a simplified example of a hotel document structure:

```jsonc
{
  "HotelId": "1",
  "HotelName": "Stay-Kay City Hotel",
  "Description": "This classic hotel is fully-refurbished...",
  "Rating": 3.6,
  "DescriptionVector": [
    -0.04886505,
    -0.02030743,
    0.01763356,
    ...
    // 1536 dimensions total
  ]
}
```

**Key points about storing embeddings:**

- **Vector arrays** are stored as standard JSON arrays in your documents
- **Vector policy** defines the path (`/DescriptionVector`), data type (`float32`), dimensions (1536), and distance function (cosine)
- **Indexing policy** creates a vector index on the vector field for efficient similarity search
- The vector field should be **excluded from standard indexing** to optimize insertion performance

These policies are defined in the Bicep templates for the [distance metrics](#distance-metrics) for this sample project. For more information on vector policies and indexing, see [Vector search in Azure Cosmos DB](./vector-search.md).



## Create code files for vector search

Create two Java source files in the `src/main/java/com/example/cosmos/vectorsearch` directory:

### [Linux/macOS](#tab/tab-touch-linux)

```bash
touch src/main/java/com/example/cosmos/vectorsearch/VectorSearch.java
touch src/main/java/com/example/cosmos/vectorsearch/Utils.java
```

### [Windows](#tab/tab-touch-windows)

```powershell
New-Item -ItemType File -Path src/main/java/com/example/cosmos/vectorsearch/VectorSearch.java | Out-Null
New-Item -ItemType File -Path src/main/java/com/example/cosmos/vectorsearch/Utils.java | Out-Null
```

---

## Create code for vector search

Paste the following code into the `VectorSearch.java` file.

:::code language="java" source="~/cosmos-db-vector-samples/nosql-vector-search-java/src/main/java/com/example/cosmos/vectorsearch/VectorSearch.java" :::

This code:

- Configures either a `DiskANN` or `quantizedFlat` vector algorithm from the `VECTOR_ALGORITHM` environment variable.
- Connects to Azure OpenAI and Azure Cosmos DB using passwordless authentication.
- Loads pre-vectorized hotel data from a JSON file.
- Inserts data into the appropriate container.
- Generates an embedding for a natural-language query (`quintessential lodging near running trails, eateries, retail`).
- Executes a `VectorDistance` SQL query to retrieve the top 5 most semantically similar hotels ranked by similarity score.
- Handles errors for missing clients, invalid algorithm selection, and non-existent containers/databases.

## Understand the code: Generate embeddings with Azure OpenAI

The code creates embeddings for query text:

```java
EmbeddingsOptions options = new EmbeddingsOptions(
    List.of(queryText) // Array of description strings to embed
);
Embeddings embeddings = openAIClient.getEmbeddings(model, options);
List<Float> queryVector = embeddings.getData().get(0).getEmbedding();
```

This Azure OpenAI SDK call converts text like "quintessential lodging near running trails" into a 1536-dimension vector that captures its semantic meaning. For more details on generating embeddings, see [Azure OpenAI embeddings documentation](/azure/ai-foundry/openai/how-to/embeddings).

## Understand the code: Store vectors in Azure Cosmos DB

All documents with vector arrays are inserted at scale using the [`executeBulkOperations`](/java/api/com.azure.cosmos.cosmoscontainer) method in `Utils.insertData()`. Each document is mapped to a bulk create operation using the `PartitionKeyBuilder` with each document's partition key value. The utility tracks inserted, skipped, and failed counts along with total RU consumption.

This inserts hotel documents including their pre-generated `DescriptionVector` arrays into the container. You can safely pass in all the document data, and the client library handles the batch processing and retries for you.

## Understand the code: Run vector similarity search

The code performs a vector search using the `VectorDistance` function:

```java
String queryText = String.format(
    "SELECT TOP 5 c.HotelName, c.Description, c.Rating, " +
    "VectorDistance(c.%s, @embedding) AS SimilarityScore " +
    "FROM c ORDER BY VectorDistance(c.%s, @embedding)",
    embeddedField, embeddedField
);

SqlQuerySpec querySpec = new SqlQuerySpec(queryText,
    new SqlParameter("@embedding", queryVector));

CosmosPagedIterable<ObjectNode> results = container.queryItems(
    querySpec, new CosmosQueryRequestOptions(), ObjectNode.class);
```

This code builds a parameterized SQL query that uses the VectorDistance function to compare the query's embedding vector (@embedding) against each document's stored vector field (`DescriptionVector`), returning the top 5 hotels with their name and similarity score, ordered from most similar to least similar. The query embedding is passed as a parameter to avoid injection and comes from a prior Azure OpenAI embeddings call.

**What this query returns:**

- Top 5 most similar hotels based on vector distance
- Hotel properties: `HotelName`, `Description`, `Rating`
- `SimilarityScore`: A numeric value indicating how similar each hotel is to your query
- Results ordered from most similar to least similar

For more information on the `VectorDistance` function, see [VectorDistance documentation](vector-search.md#perform-vector-search-with-queries-using-vectordistance).

## Create utility functions

Paste the following code into `Utils.java`:

:::code language="java" source="~/cosmos-db-vector-samples/nosql-vector-search-java/src/main/java/com/example/cosmos/vectorsearch/Utils.java" :::

This utility class provides these **key** functions:

- `createOpenAIClient` / `createCosmosClient`: Create clients for Azure OpenAI and Azure Cosmos DB using passwordless authentication via DefaultAzureCredential. Enable RBAC on both resources and sign in to Azure CLI
- `insertData`: Inserts data in batches into an Azure Cosmos DB container using bulk operations and tracks inserted, skipped, and failed counts along with total RU consumption
- `printSearchResults`: Prints the results of a vector search, including the score and hotel name
- `validateFieldName`: Validates that a field name exists in the data to prevent injection

## Authenticate with Azure CLI

Sign in to Azure CLI before you run the application so the app can access Azure resources securely.

```azurecli
az login
```

The code uses your local developer authentication to access Azure Cosmos DB and Azure OpenAI with `createOpenAIClient` and `createCosmosClient` from `Utils.java`. These functions rely on [DefaultAzureCredential](/java/api/com.azure.identity.defaultazurecredential) from **azure-identity**, which walks an ordered chain of credential providers and resolves to Azure CLI credentials for local development. Learn more about how to [Authenticate Java apps to Azure services using the Azure Identity library](/azure/developer/java/sdk/authentication/overview).

## Build and run the application

Build and run the application with Maven:

### [DiskANN](#tab/tab-diskann)

Linux/macOS:

```bash
VECTOR_ALGORITHM=diskann mvn compile exec:java
```

Windows:

```cmd
set VECTOR_ALGORITHM=diskann && mvn compile exec:java
```

### [Quantized flat](#tab/tab-quantizedflat)

Linux/macOS:

```bash
VECTOR_ALGORITHM=quantizedflat mvn compile exec:java
```

Windows:

```cmd
set VECTOR_ALGORITHM=quantizedflat && mvn compile exec:java
```

---

The app logging and output show:

- Data insertion status
- Vector index creation 
- Search results with hotel names and similarity scores

### [DiskANN](#tab/tab-diskann)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-java/output/diskann.txt" :::

### [Quantized flat](#tab/tab-quantizedflat)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-java/output/quantizedflat.txt" :::

---


## Distance metrics

Azure Cosmos DB supports three distance functions for vector similarity:

| Distance Function | Score Range | Interpretation | Best For |
|------------------|-------------|----------------|----------|
| **Cosine** (default) | 0.0 to 1.0 | Higher scores (closer to 1.0) indicate greater similarity | General text similarity, Azure OpenAI embeddings (used in this quickstart) |
| **Euclidean** (L2) | 0.0 to ∞ | Lower = more similar | Spatial data, when magnitude matters |
| **Dot Product** | -∞ to +∞ | Higher = more similar | When vector magnitudes are normalized |

The distance function is set in the **vector embedding policy** when creating the container. This is provided in the [infrastructure](https://github.com/Azure-Samples/cosmos-db-vector-samples/blob/main/infra/database.bicep) in the sample repository. It is defined as part of the container definition.


### [DiskANN](#tab/tab-diskann)

```bicep
{
    name: 'hotels_diskann'
    partitionKeyPaths: [
        '/HotelId'
    ]
    indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
        {
            path: '/*'
        }
        ]
        excludedPaths: [
        {
            path: '/_etag/?'
        }
        {
            path: '/DescriptionVector/*'
        }
        ]
        vectorIndexes: [
        {
            path: '/DescriptionVector'
            type: 'diskANN'
        }
        ]
    }
    vectorEmbeddingPolicy: {
        vectorEmbeddings: [
        {
            path: '/DescriptionVector'
            dataType: 'float32'
            dimensions: 1536
            distanceFunction: 'cosine'
        }
        ]
    }
}
```

### [Quantized flat](#tab/tab-quantizedflat)

```bicep
{
    name: 'hotels_quantizedflat'
    partitionKeyPaths: [
        '/HotelId'
    ]
    indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
        {
            path: '/*'
        }
        ]
        excludedPaths: [
        {
            path: '/_etag/?'
        }
        {
            path: '/DescriptionVector/*'
        }
        ]
        vectorIndexes: [
        {
            path: '/DescriptionVector'
            type: 'quantizedFlat'
        }
        ]
    }
    vectorEmbeddingPolicy: {
        vectorEmbeddings: [
        {
            path: '/DescriptionVector'
            dataType: 'float32'
            dimensions: 1536
            distanceFunction: 'cosine'
        }
        ]
    }
}
```

---

This Bicep code defines an Azure Cosmos DB container configuration for storing hotel documents with vector search capabilities.

| Property | Description |
|----------|-------------|
| `partitionKeyPaths` | Partitions documents by `HotelId` for distributed storage. |
| `indexingPolicy` | Configures automatic indexing on all document properties (`/*`) except the system `_etag` field and the `DescriptionVector` array to optimize write performance. Vector fields don't need standard indexing because they use a specialized `vectorIndexes` configuration instead. |
| `vectorIndexes` | Creates either a DiskANN or quantizedFlat index on the `/DescriptionVector` path for efficient similarity searches. |
| `vectorEmbeddingPolicy` | Defines the vector field's characteristics: `float32` data type with 1536 dimensions (matching the `text-embedding-3-small` model output) and cosine as the distance function to measure similarity between vectors during queries. |

## Interpret similarity scores

In the example output using **cosine similarity**:

- **0.4991** (Royal Cottage Resort) - Highest similarity, best match for "lodging near running trails, eateries, retail"
- **0.4388** (Roach Motel) - Lower similarity, still relevant but less matching
- Scores closer to **1.0** indicate stronger semantic similarity
- Scores near **0** indicate little similarity

> [!IMPORTANT]
> - Absolute score values depend on your embedding model and data
> - Focus on **relative ranking** rather than absolute thresholds
> - Azure OpenAI embeddings work best with cosine similarity

For detailed information on distance functions, see [What are distance functions?](./gen-ai/distance-functions.md)

## View and manage data in Visual Studio Code

1. Select the [Cosmos DB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) in Visual Studio Code to connect to your Azure Cosmos DB account.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-vector-store-java/visual-studio-code-extension.png" alt-text="Screenshot of Visual Studio Code showing the Azure Cosmos DB extension with Hotels database items and a JSON document editor." lightbox="./media/quickstart-vector-store-java/visual-studio-code-extension.png":::

## Clean up resources

[!INCLUDE [Clean up resources](./includes/clean-up-resources.md)]

## Related content

- [Vector search in Azure Cosmos DB](gen-ai/vector-search-overview.md)
- [Document Indexer for Azure Cosmos DB (preview)](gen-ai/document-indexer.md)
- [Vector embeddings in Azure Cosmos DB](gen-ai/vector-embeddings.md)
- [Azure RBAC built-in roles](/azure/role-based-access-control/built-in-roles)

