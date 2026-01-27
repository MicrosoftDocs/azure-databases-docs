---

title: Quickstart - Vector Search with Node.js
description: Learn how to use vector search in Azure DocumentDB with Node.js. Store and query vector data efficiently in your applications. 
author: diberry
ms.author: diberry
ms.reviewer: khelanmodi
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 01/26/2026
ms.custom:
  - devx-track-ts
  - devx-track-ts-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Node.js applications with Azure DocumentDB.
---

# Quickstart: Vector search with Node.js in Azure DocumentDB

Use vector search in Azure DocumentDB with the Node.js client library. Store and query vector data efficiently.

This quickstart uses a sample hotel dataset in a JSON file with vectors from the `text-embedding-3-small` model. The dataset includes hotel names, locations, descriptions, and vector embeddings.

Find the [sample code](https://github.com/Azure-Samples/documentdb-samples/tree/main/mongo-vcore-vector-search-typescript) on GitHub. 

## Prerequisites

[!INCLUDE[Prerequisites - Vector Search Quickstart](includes/prerequisite-quickstart-vector-search-model.md)]

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

1. Copy the `Hotels_Vector.json` [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/documentdb-samples/refs/heads/main/ai/data/Hotels_Vector.json) to your `data` directory.


## Create a Node.js project

1. Create a new directory for your project and open it in Visual Studio Code:

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
    npm install mongodb @azure/identity openai @types/node
    ```

    - `mongodb`: MongoDB Node.js driver
    - `@azure/identity`: Azure Identity library for passwordless authentication
    - `openai`: OpenAI client library to create vectors
    - `@types/node`: Type definitions for Node.js

1. Create a `.env` file in your project root for environment variables:

    ```ini
    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
    AZURE_OPENAI_EMBEDDING_ENDPOINT=
    EMBEDDING_SIZE_BATCH=16

    # MongoDB configuration
    MONGO_CLUSTER_NAME=

    # Data file
    DATA_FILE_WITH_VECTORS=../data/Hotels_Vector.json
    FIELD_TO_EMBED=Description
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536
    LOAD_SIZE_BATCH=100
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL
    - `MONGO_CLUSTER_NAME`: Your resource name

1. Add a `tsconfig.json` file to configure TypeScript:

    :::code language="json" source="~/documentdb-samples/ai/vector-search-typescript/tsconfig.json" :::



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

#### [IVF](#tab/tab-ivf)

Use these scripts to compile TypeScript files and run the IVF index implementation.

```json
"scripts": { 
    "build": "tsc",
    "start:ivf": "node --env-file .env dist/ivf.js"
}
```

#### [HNSW](#tab/tab-hnsw)

Use these scripts to compile TypeScript files and run the HNSW index implementation.

```json
"scripts": { 
    "build": "tsc",
    "start:hnsw": "node --env-file .env dist/hnsw.js"
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

#### [IVF](#tab/tab-ivf)

Create a `src` directory for your TypeScript files. Add two files: `ivf.ts` and `utils.ts` for the IVF index implementation:

```bash
mkdir src
touch src/ivf.ts
touch src/utils.ts
```

#### [HNSW](#tab/tab-hnsw)

Create a `src` directory for your TypeScript files. Add two files: `hnsw.ts` and `utils.ts` for the HNSW index implementation:

```bash
mkdir src
touch src/hnsw.ts
touch src/utils.ts
```

----

## Create code for vector search

### [DiskANN](#tab/tab-diskann)

Paste the following code into the `diskann.ts` file.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-typescript/src/diskann.ts" :::

#### [IVF](#tab/tab-ivf)

Paste the following code into the `ivf.ts` file.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-typescript/src/ivf.ts" :::

#### [HNSW](#tab/tab-hnsw)

Paste the following code into the `hnsw.ts` file.

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-typescript/src/hnsw.ts" :::

----

This main module provides these features:

- Includes utility functions
- Creates a configuration object for environment variables
- Creates clients for Azure OpenAI and DocumentDB
- Connects to MongoDB, creates a database and collection, inserts data, and creates standard indexes
- Creates a vector index using IVF, HNSW, or DiskANN
- Creates an embedding for a sample query text using the OpenAI client. You can change the query at the top of the file
- Runs a vector search using the embedding and prints the results

## Create utility functions

Paste the following code into `utils.ts`:

:::code language="typescript" source="~/documentdb-samples/ai/vector-search-typescript/src/utils.ts" :::

This utility module provides these features:

- `JsonData`: Interface for the data structure
- `scoreProperty`: Location of the score in query results based on vector search method
- `getClients`: Creates and returns clients for Azure OpenAI and Azure DocumentDB
- `getClientsPasswordless`: Creates and returns clients for Azure OpenAI and Azure DocumentDB using passwordless authentication. Enable RBAC on both resources and sign in to Azure CLI
- `readFileReturnJson`: Reads a JSON file and returns its contents as an array of `JsonData` objects
- `writeFileJson`: Writes an array of `JsonData` objects to a JSON file
- `insertData`: Inserts data in batches into a MongoDB collection and creates standard indexes on specified fields
- `printSearchResults`: Prints the results of a vector search, including the score and hotel name

## Authenticate with Azure CLI

Sign in to Azure CLI before you run the application so it can access Azure resources securely.

```bash
az login
```

## Build and run the application

Build the TypeScript files, then run the application:

### [DiskANN](#tab/tab-diskann)

```bash
npm run build
npm run start:diskann
```

#### [IVF](#tab/tab-ivf)

```bash
npm run build
npm run start:ivf
```

#### [HNSW](#tab/tab-hnsw)

```bash
npm run build    
npm run start:hnsw
```

----

The app logging and output show:

- Collection creation and data insertion status
- Vector index creation 
- Search results with hotel names and similarity scores

### [DiskANN](#tab/tab-diskann)

:::code language="output" source="~/documentdb-samples/ai/vector-search-typescript/output/diskann.txt" :::

#### [IVF](#tab/tab-ivf)

:::code language="output" source="~/documentdb-samples/ai/vector-search-typescript/output/ivf.txt" :::
#### [HNSW](#tab/tab-hnsw)

:::code language="output" source="~/documentdb-samples/ai/vector-search-typescript/output/hnsw.txt" :::

----

## View and manage data in Visual Studio Code

1. Select the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) in Visual Studio Code to connect to your Azure DocumentDB account.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" lightbox="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" alt-text="Screenshot of DocumentDB extension showing the DocumentDB collection.":::

## Clean up resources

Delete the resource group, DocumentDB account, and Azure OpenAI resource when you don't need them to avoid extra costs.

## Related content

- [Vector store in Azure DocumentDB](vector-search.md)
- [Support for geospatial queries](geospatial-support.md)
