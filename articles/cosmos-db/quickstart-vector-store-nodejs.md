---

title: Quickstart - Vector Search with Node.js
description: Learn how to use vector search in Azure Cosmos DB with Node.js. Store and query vector data efficiently. Get started now.
author: diberry
ms.author: diberry
ms.reviewer: jcodella
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 02/05/2026
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

- An existing Cosmos DB resource
  - If you don't have a resource, create a [new resource](https://docs.azure.cn/en-us/cosmos-db/nosql/quickstart-portal)
  - Role Based Access Control (RBAC) roles assigned:
    - **Cosmos DB Built-in Data Contributor** (data plane) - Role ID: `00000000-0000-0000-0000-000000000002`
    - **DocumentDB Account Contributor** (control plane)
  - [Firewall configured to allow access to your client IP address]()

- [Azure OpenAI resource](/azure/ai-foundry/openai/how-to/create-resource?view=foundry-classic&pivots=cli#create-a-resource)
  - Custom domain configured
  - Role Based Access Control (RBAC) role assigned:
    - **Cognitive Services OpenAI User**
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
    EMBEDDING_SIZE_BATCH=16

    # Cosmos DB configuration
    COSMOSDB_ENDPOINT=

    # Data file
    DATA_FILE_WITH_VECTORS=../data/HotelsData_toCosmosDB_Vector.json
    FIELD_TO_EMBED=Description
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536
    LOAD_SIZE_BATCH=50
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL
    - `COSMOSDB_ENDPOINT`: Your Cosmos DB endpoint URL

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
    "start:diskann": "node --env-file .env dist/diskann.js"
}
```

#### [Quantized flat](#tab/tab-quantized-flat)

Use these scripts to compile TypeScript files and run the Quantized flat index implementation.

```json
"scripts": { 
    "build": "tsc",
    "start:quantized-flat": "node --env-file .env dist/quantized-flat.js"
}
```

#### [Flat](#tab/tab-flat)

Use these scripts to compile TypeScript files and run the Flat index implementation.

```json
"scripts": { 
    "build": "tsc",
    "start:flat": "node --env-file .env dist/flat.js"
}
```
    
----

## Create code files for vector search

### [DiskANN](#tab/tab-diskann)

Create a `src` directory for your TypeScript files. Add two files: `diskann.ts` and `utils.ts` for the DiskANN index implementation:

```bash
mkdir src    
touch src/diskann.ts
touch src/utils.ts
```

#### [Quantized flat](#tab/tab-quantized-flat)

Create a `src` directory for your TypeScript files. Add two files: `quantizedFlat.ts` and `utils.ts` for the Quantized flat index implementation:

```bash
mkdir src
touch src/quantizedFlat.ts
touch src/utils.ts
```

#### [Flat](#tab/tab-flat)

Create a `src` directory for your TypeScript files. Add two files: `flat.ts` and `utils.ts` for the Flat index implementation:

```bash
mkdir src
touch src/flat.ts
touch src/utils.ts
```

----


## Create code for vector search

### [DiskANN](#tab/tab-diskann)

Paste the following code into the `diskann.ts` file.

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/src/diskann.ts" :::

#### [Quantized flat](#tab/tab-quantized-flat)

Paste the following code into the `quantizedFlat.ts` file.
:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/src/quantizedFlat.ts" :::

#### [Flat](#tab/tab-flat)

Paste the following code into the `flat.ts` file.

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/src/flat.ts" :::

----


### Understand the code: Generate embeddings with Azure OpenAI

The code creates embeddings for query text:

```typescript
const createEmbeddedForQueryResponse = await aiClient.embeddings.create({
    model: config.deployment,
    input: [config.query]
});
```

This converts text like "quintessential lodging near running trails" into a 1536-dimension vector that captures its semantic meaning. For more details on generating embeddings, see [Azure OpenAI embeddings documentation](/azure/ai-foundry/openai/how-to/embeddings).

### Understand the code: Store vectors in Cosmos DB

Documents with vector arrays are inserted using the `insertData` utility function:

```typescript
const insertSummary = await insertData(config, container, data.slice(0, config.batchSize));
```

This inserts hotel documents including their pre-generated `DescriptionVector` arrays into the container.

### Understand the code: Run vector similarity search

The code performs a vector search using the `VectorDistance` function:

```typescript
const { resources, requestCharge } = await container.items
    .query({
        query: `SELECT TOP 5 c.HotelName, c.Description, c.Rating, VectorDistance(c.${safeEmbeddedField}, @embedding) AS SimilarityScore FROM c ORDER BY VectorDistance(c.${safeEmbeddedField}, @embedding)`,
        parameters: [
            { name: "@embedding", value: createEmbeddedForQueryResponse.data[0].embedding }
        ]
    })
    .fetchAll();
```

**What this query returns:**

- Top 5 most similar hotels based on vector distance
- Hotel properties: `HotelName`, `Description`, `Rating`
- `SimilarityScore`: A numeric value indicating how similar each hotel is to your query
- Results ordered from most similar to least similar

For more information on the `VectorDistance` function, see [VectorDistance documentation](vector-search.md#perform-vector-search-with-queries-using-vectordistance).

## Create utility functions

Paste the following code into `utils.ts`:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/src/utils.ts" :::

This utility module provides these features:

- `JsonData`: Interface for the data structure
- `getClients`: Creates and returns clients for Azure OpenAI and Azure Cosmos DB
- `getClientsPasswordless`: Creates and returns clients for Azure OpenAI and Azure Cosmos DB using passwordless authentication. Enable RBAC on both resources and sign in to Azure CLI
- `readFileReturnJson`: Reads a JSON file and returns its contents as an array of `JsonData` objects
- `writeFileJson`: Writes an array of `JsonData` objects to a JSON file
- `insertData`: Inserts data in batches into a Cosmos DB collection and creates standard indexes on specified fields
- `printSearchResults`: Prints the results of a vector search, including the score and hotel name
- `validateFieldName`: Validates that a field name exists in the data

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

#### [Quantized flat](#tab/tab-quantized-flat)

```bash
npm run build
npm run start:quantizedFlat
```

#### [Flat](#tab/tab-flat)

```bash
npm run build    
npm run start:flat
```

----

The app logging and output show:

- Collection creation and data insertion status
- Vector index creation 
- Search results with hotel names and similarity scores

### [DiskANN](#tab/tab-diskann)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/output/diskann.txt" :::

#### [Quantized flat](#tab/tab-quantized-flat)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/output/quantizedflat.txt" :::
#### [Flat](#tab/tab-flat)

:::code language="output" source="~/cosmos-db-vector-samples/nosql-vector-search-typescript/output/flat.txt" :::

----


### Distance metrics

Azure Cosmos DB for NoSQL supports three distance functions for vector similarity:

| Distance Function | Score Range | Interpretation | Best For |
|------------------|-------------|----------------|----------|
| **Cosine** (default) | 0.0 to 1.0 | Higher scores (closer to 1.0) indicate greater similarity | General text similarity, Azure OpenAI embeddings (used in this quickstart) |
| **Euclidean** (L2) | 0.0 to ∞ | Lower = more similar | Spatial data, when magnitude matters |
| **Dot Product** | -∞ to +∞ | Higher = more similar | When vector magnitudes are normalized |

The distance function is set in the **vector embedding policy** when creating the container:

```typescript
const vectorEmbeddingPolicy: VectorEmbeddingPolicy = {
    vectorEmbeddings: [
        {
            path: "/DescriptionVector",
            dataType: VectorEmbeddingDataType.Float32,
            dimensions: 1536,
            distanceFunction: VectorEmbeddingDistanceFunction.Cosine, // Can be Cosine, Euclidean, or DotProduct
        }
    ],
};
```

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

1. Select the [Cosmos DB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) in Visual Studio Code to connect to your Azure Cosmos DB account.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-vector-search-nodejs/visual-studio-code-azure-cosmos-db-extension.png" lightbox="./media/quickstart-vector-search-nodejs/visual-studio-code-azure-cosmos-db-extension.png" alt-text="Screenshot of Cosmos DB extension showing the Cosmos DB collection.":::

## Clean up resources

Delete the resource group, Cosmos DB account, and Azure OpenAI resource when you don't need them to avoid extra costs.

## Related content

- [Vector search in Azure Cosmos DB](gen-ai/vector-search-overview.md)
- [Document Indexer for Azure Cosmos DB (preview)](gen-ai/document-indexer.md)
- [Vector embeddings in Azure Cosmos DB](gen-ai/vector-embeddings.md)