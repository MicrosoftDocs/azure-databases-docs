---

title: Quickstart - Vector Search with Node.js
description: Learn how to use vector search in Azure Cosmos DB with Node.js. Store and query vector data efficiently in your applications. 
author: diberry
ms.author: diberry
ms.reviewer: jcodella
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 02/03/2026
ai-usage: ai-assisted
ms.custom:
  - devx-track-ts
  - devx-track-ts-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Node.js applications with Azure Cosmos DB.
---

# Quickstart: Vector search with Node.js in Azure Cosmos DB

Use vector search in Azure Cosmos DB with the Node.js client library. Store and query vector data efficiently.

This quickstart uses a sample hotel dataset in a JSON file with vectors from the `text-embedding-3-small` model. The dataset includes hotel names, locations, descriptions, and vector embeddings.

Find the [sample code](https://github.com/azure-samples/cosmos-db-vector-samples/nosql-vector-search-typescript) on GitHub. 

[API reference documentation](/javascript/api/overview/azure/cosmos-readme) | [Library source code](https://github.com/azure/azure-sdk-for-js/tree/main/sdk/cosmosdb/cosmos) | [Package (npm)](https://www.npmjs.com/package/@azure/cosmos) | [Azure Developer CLI](/azure/developer/azure-developer-cli/overview)

## Prerequisites

- An Azure account. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
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
    npm install @azure/identity @azure/cosmos openai @types/node
    ```

    - `@azure/cosmos`: Azure Cosmos DB client library
    - `@azure/identity`: Azure Identity library for passwordless authentication
    - `openai`: OpenAI client library to create vectors
    - `@types/node`: Type definitions for Node.js

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

Create a `src` directory for your TypeScript files. Add two files: `quantized-flat.ts` and `utils.ts` for the Quantized flat index implementation:

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

This main module provides these features:

- Includes utility functions
- Creates a configuration object for environment variables
- Creates clients for Azure OpenAI and Cosmos DB
- Connects to Cosmos DB, creates a database and collection, inserts data, and creates standard indexes
- Creates a vector index using IVF, HNSW, or DiskANN
- Creates an embedding for a sample query text using the OpenAI client. You can change the query at the top of the file
- Runs a vector search using the embedding and prints the results

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

## View and manage data in Visual Studio Code

1. Select the [Cosmos DB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) in Visual Studio Code to connect to your Azure Cosmos DB account.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-vector-search-nodejs/visual-studio-code-azure-cosmos-db-extension.png" lightbox="./media/quickstart-vector-search-nodejs/visual-studio-code-azure-cosmos-db-extension.png" alt-text="Screenshot of Cosmos DB extension showing the Cosmos DB collection.":::

## Clean up resources

Delete the resource group, Cosmos DB account, and Azure OpenAI resource when you don't need them to avoid extra costs.

## Related content

- [Vector store in Azure Cosmos DB](vector-search.md)
- [Support for geospatial queries](geospatial-support.md)
