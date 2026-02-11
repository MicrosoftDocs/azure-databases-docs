---

title: Quickstart - Vector Search with Node.js
description: Learn how to use vector search in Azure Cosmos DB with Node.js. Store and query vector data efficiently. Get started now.
author: diberry
ms.author: diberry
ms.reviewer: jcodella
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 02/11/2026
ai-usage: ai-assisted
ms.custom:
  - devx-track-ts
  - devx-track-ts-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Node.js applications with Azure Cosmos DB.
---

# Quickstart: Vector search with Node.js in Azure Cosmos DB

Use vector search in Azure Cosmos DB with the Node.js client library. Store and query vector data efficiently in your applications.

This quickstart uses a sample hotel dataset in a JSON file with vectors from the **text-embedding-3-small** model. The dataset includes hotel names, locations, descriptions, and vector embeddings.

Find the sample code with resource provisioning on [GitHub](https://github.com/Azure-Samples/cosmos-db-vector-samples).

## Prerequisites

- An Azure subscription
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

- An existing **Azure Cosmos DB for NoSQL** resource data plane access
  - If you don't have a resource, create a [new resource](https://portal.azure.com/#create/Microsoft.DocumentDB)
  - [Firewall configured to allow access to your client IP address](how-to-configure-firewall.md)
  - Role Based Access Control (RBAC) roles assigned: 
  
      - **Cosmos DB Built-in Data Contributor** (data plane) 
      - Role ID: `00000000-0000-0000-0000-000000000002`
      


- [Azure OpenAI resource](/azure/ai-foundry/openai/how-to/create-resource?view=foundry-classic&pivots=cli#create-a-resource)
  - Custom domain configured

  - Role Based Access Control (RBAC) role assigned:
    - **Cognitive Services OpenAI User**
    - Role ID: `5e0bd9bd-7b93-4f28-af87-19fc36ad61bd`

  - `text-embedding-3-small` model deployed

- [Visual Studio Code](https://code.visualstudio.com/download)
  - [Cosmos DB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb)

- [Node.js LTS](https://nodejs.org/download/)
- [TypeScript](https://www.typescriptlang.org/download): Install TypeScript globally:

    ```bash
    npm install -g typescript
    ```

## Create data file with vectors

1. Create a new data directory for the hotels data file:

    ```bash
    mkdir data
    ```

1. Copy the [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json) to your `data` directory.

## Create a Node.js project

1. Create a new sibling directory for your project, at the same level as the data directory, and open it in Visual Studio Code:

    ```bash
    mkdir vector-search-quickstart
    code vector-search-quickstart
    ```

1. In the terminal, initialize a Node.js project:

    ```bash
    npm init -y
    npm pkg set type="module"
    ```

1. Install the required packages:

    ```bash
    npm install @azure/identity @azure/cosmos openai
    npm install @types/node --save-dev
    ```

    * **@azure/identity** - Azure authentication library for passwordless (managed identity) connections
    * **@azure/cosmos** - Azure Cosmos DB client library for database operations
    * **openai** - OpenAI SDK for generating embeddings with Azure OpenAI
    * **@types/node** (dev) - TypeScript type definitions for Node.js APIs

1. Create a `.env` file in your project root for environment variables:

    ```ini
    # Identity for local developer authentication with Azure CLI
    AZURE_TOKEN_CREDENTIALS=AzureCliCredential

    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
    AZURE_OPENAI_EMBEDDING_ENDPOINT=

    # Cosmos DB configuration
    AZURE_COSMOSDB_ENDPOINT=

    # Data file
    DATA_FILE_WITH_VECTORS=../data/HotelsData_toCosmosDB_Vector.json
    FIELD_TO_EMBED=Description
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL
    - `AZURE_COSMOSDB_ENDPOINT`: Your Cosmos DB endpoint URL

1. Add a `tsconfig.json` file to configure TypeScript:

    :::code language="json" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/tsconfig.json" :::


## Understand the document schema

Before building the application, understand how vectors are stored in Cosmos DB documents. Each hotel document contains:

- **Standard fields**: `HotelId`, `HotelName`, `Description`, `Category`, etc.
- **Vector field**: `DescriptionVector` - an array of 1536 floating-point numbers representing the semantic meaning of the hotel description

Here's a simplified example of a hotel document structure:

```json
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

For more information on vector policies and indexing, see [Vector search in Azure Cosmos DB for NoSQL](./vector-search.md).

## Create npm scripts

Edit the `package.json` file and add these scripts:

### [DiskANN](#tab/tab-diskann)

Use these scripts to compile TypeScript files and run the DiskANN index implementation.

```json
"scripts": { 
    "build": "tsc",
    "start:diskann": "set VECTOR_ALGORITHM=diskann && node --env-file .env dist/vector-search.js"
}
```

#### [Quantized flat](#tab/tab-quantizedflat)

Use these scripts to compile TypeScript files and run the Quantized flat index implementation.

```json
"scripts": { 
    "build": "tsc",
    "start:quantizedflat": "set VECTOR_ALGORITHM=quantizedflat && node --env-file .env dist/vector-search.js"
}
```

    
----

## Create code files for vector search


Create a `src` directory for your TypeScript files. Add two files: `vector-search.ts` and `utils.ts` for the DiskANN index implementation:

```bash
mkdir src    
touch src/vector-search.ts
touch src/utils.ts
```

## Create code for vector search


Paste the following code into the `vector-search.ts` file.

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/src/vector-search.ts" :::

This code configures either a `DiskANN` or `quantizedFlat` vector algorithm from environment variables, connects to Azure OpenAI and Cosmos DB using passwordless authentication, loads pre-vectorized hotel data from a JSON file, inserts it into the appropriate container, then generates an embedding for a natural-language query (`quintessential lodging near running trails, eateries, retail`) and executes a VectorDistance SQL query to retrieve the top 5 most semantically similar hotels ranked by similarity score. 

Error handling covers missing clients, invalid algorithm selection, and non-existent containers/databases.

### Understand the code: Generate embeddings with Azure OpenAI

The code creates embeddings for query text:

```typescript
const createEmbeddedForQueryResponse = await aiClient.embeddings.create({
    model, // OpenAI embedding model, e.g. "text-embedding-3-small"
    input  // Array of description strings to embed, e.g. ["quintessential lodging near running trails"]
});
```

This OpenAI API call for [client.embeddings.create](https://platform.openai.com/docs/guides/embeddings#how-to-get-embeddings) converts text like "quintessential lodging near running trails" into a 1536-dimension vector that captures its semantic meaning. For more details on generating embeddings, see [Azure OpenAI embeddings documentation](/azure/ai-foundry/openai/how-to/embeddings).

### Understand the code: Store vectors in Cosmos DB

All documents with vector arrays are inserted at scale using the [`executeBulkOperations`](/javascript/api/%40azure/cosmos/items#@azure-cosmos-items-executebulkoperations) function:

```typescript
const response = await container.items.executeBulkOperations(operations);
```

This inserts hotel documents including their pre-generated `DescriptionVector` arrays into the container. You can safely pass in all the document data, and the client library handles the batch processing and retries for you. 

### Understand the code: Run vector similarity search

The code performs a vector search using the `VectorDistance` function:

```typescript
const queryText = `SELECT TOP 5 c.HotelName, c.Description, c.Rating, VectorDistance(c.${safeEmbeddedField}, @embedding) AS SimilarityScore FROM c ORDER BY VectorDistance(c.${safeEmbeddedField}, @embedding)`;

const queryResponse = await container.items
    .query({
        query: queryText,
        parameters: [
            { name: "@embedding", value: createEmbeddedForQueryResponse.data[0].embedding }
        ]
    })
    .fetchAll();
```

This code builds a parameterized SQL query that uses the VectorDistance function to compare the query's embedding vector (@embedding) against each document's stored vector field (`DescriptionVector`), returning the top 5 hotels with their name and similarity score, ordered from most similar to least similar. The query embedding is passed as a parameter to avoid injection and comes from a prior Azure OpenAI embeddings.create call.

**What this query returns:**

- Top 5 most similar hotels based on vector distance
- Hotel properties: `HotelName`, `Description`, `Rating`
- `SimilarityScore`: A numeric value indicating how similar each hotel is to your query
- Results ordered from most similar to least similar

For more information on the `VectorDistance` function, see [VectorDistance documentation](vector-search.md#perform-vector-search-with-queries-using-vectordistance).

## Create utility functions

Paste the following code into `utils.ts`:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/src/utils.ts" :::

This utility module provides these **key** functions:

- `getClientsPasswordless`: Creates and returns clients for Azure OpenAI and Azure Cosmos DB using passwordless authentication. Enable RBAC on both resources and sign in to Azure CLI
- `insertData`: Inserts data in batches into a Cosmos DB container and creates standard indexes on specified fields
- `printSearchResults`: Prints the results of a vector search, including the score and hotel name
- `validateFieldName`: Validates that a field name exists in the data
- `getBulkOperationRUs`: Estimates the Request Units (RUs) for bulk operations based on the number of documents and vector dimensions

## Authenticate with Azure CLI

Sign in to Azure CLI before you run the application so the app can access Azure resources securely.

```bash
az login
```

The code uses your local developer authentication to access Azure Cosmos DB and Azure OpenAI with the `getClientsPasswordless` function from `utils.ts`. When you set `AZURE_TOKEN_CREDENTIALS=AzureCliCredential`, this setting tells the function to use Azure CLI credentials for authentication _deterministically_. The function relies on [DefaultAzureCredential](/javascript/api/@azure/identity/defaultazurecredential) from **@azure/identity** to find your Azure credentials in the environment. Learn more about how to [Authenticate JavaScript apps to Azure services using the Azure Identity library](/azure/developer/javascript/sdk/authentication/overview).

## Build and run the application

Build the TypeScript files, then run the application:

### [DiskANN](#tab/tab-diskann)

```bash
npm run build
npm run start:diskann
```

#### [Quantized flat](#tab/tab-quantizedflat)

```bash
npm run build
npm run start:quantizedflat
```

----

The app logging and output show:

- Data insertion status
- Vector index creation 
- Search results with hotel names and similarity scores

### [DiskANN](#tab/tab-diskann)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/output/diskann.txt" :::

#### [Quantized flat](#tab/tab-quantizedflat)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/output/quantizedflat.txt" :::

----


### Distance metrics

Azure Cosmos DB for NoSQL supports three distance functions for vector similarity:

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

#### [Quantized flat](#tab/tab-quantizedflat)

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

This Bicep code defines an Azure Cosmos DB container configuration for storing hotel documents with vector search capabilities. The `partitionKeyPaths` specifies that documents are partitioned by `HotelId` for distributed storage. The `indexingPolicy` configures automatic indexing on all document properties (/*) except the system `_etag` field and the `DescriptionVector` array to optimize write performance—vector fields don't need standard indexing because they use a specialized `vectorIndexes` configuration instead. The `vectorIndexes` section creates either a DiskANN or quantizedFlat index on the `/DescriptionVector` path for efficient similarity searches. Finally, the `vectorEmbeddingPolicy` defines the vector field's characteristics: `float32` data type with 1536 dimensions (matching the `text-embedding-3-small` model output) and cosine as the distance function to measure similarity between vectors during queries.

### Interpreting similarity scores

In the example output using **cosine similarity**:

- **0.4991** (Royal Cottage Resort) - Highest similarity, best match for "lodging near running trails, eateries, retail"
- **0.4388** (Roach Motel) - Lower similarity, still relevant but less matching
- Scores closer to **1.0** indicate stronger semantic similarity
- Scores near **0** indicate little similarity
- Negative scores indicate dissimilarity (rare with well-formed embeddings)

**Important notes:**

- Absolute score values depend on your embedding model and data
- Focus on **relative ranking** rather than absolute thresholds
- Azure OpenAI embeddings work best with cosine similarity

For detailed information on distance functions, see [What are distance functions?](./gen-ai/distance-functions.md)

## View and manage data in Visual Studio Code

1. Select the [Cosmos DB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb) in Visual Studio Code to connect to your Azure Cosmos DB account.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-vector-store-nodejs/visual-studio-code-azure-cosmos-db-extension.png" lightbox="./media/quickstart-vector-store-nodejs/visual-studio-code-azure-cosmos-db-extension.png" alt-text="Screenshot of Cosmos DB extension showing the Cosmos DB container.":::

## Clean up resources

Delete the resource group, Cosmos DB account, and Azure OpenAI resource when you don't need them to avoid extra costs.

## Related content

- [Vector search in Azure Cosmos DB](gen-ai/vector-search-overview.md)
- [Document Indexer for Azure Cosmos DB (preview)](gen-ai/document-indexer.md)
- [Vector embeddings in Azure Cosmos DB](gen-ai/vector-embeddings.md)
- [Azure RBAC built-in roles](/azure/role-based-access-control/built-in-roles)