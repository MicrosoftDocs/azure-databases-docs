---

title: Quickstart - Vector Search with Node.js
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to use vector search in Azure Cosmos DB for MongoDB (vCore) using the Node.js client library. This quickstart demonstrates how to store and query vector data efficiently.
author: diberry
ms.author: diberry
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 09/08/2025
ms.custom: devx-track-js, devx-track-ts, devx-track-dotnet, devx-track-extended-azdevcli
appliesto:
  - ✅ MongoDB (vCore)
# CustomerIntent: As a developer, I want to learn how to use vector search in Node.js applications with Azure Cosmos DB for MongoDB (vCore).
---
# Quickstart: Vector Search with Node.js in Azure Cosmos DB for MongoDB (vCore)

In this quickstart, you learn how to use vector search in Azure Cosmos DB for MongoDB (vCore) using the Node.js client library. This quickstart demonstrates how to store and query vector data efficiently. 

The data for this quickstart is provided for you in a JSON file that includes pre-computed vectors using `text-embedding-ada-002` model. This hotel dataset is a sample dataset provided by Microsoft for learning purposes. It includes various attributes of hotels, such as their names, locations, descriptions, and vector embeddings.

The [sample code](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/mongo-vcore-vector-search-typescript) is available on GitHub.

## Prerequisites

[!INCLUDE[Prerequisites - Azure subscription](includes/prereq-azure-subscription.md)]
- [Visual Studio Code](https://code.visualstudio.com/download)
    - [DocumentDB extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
- [Azure CLI](/cli/azure/install-azure-cli)
- [Node.js LTS](https://nodejs.org/download/)
- [TypeScript](https://www.typescriptlang.org/download): You can globally install TypeScript using npm:

   ```bash
   npm install -g typescript
   ```

- [Azure OpenAI resource](/azure/ai-foundry/openai)
    - Authentication enabled for Role Based Access Control (RBAC).
    - With deployment of `text-embedding-ada-002` model.
- [MongoDB vCore resource](quickstart-portal.md) with:
    - Authentication enabled for Role Based Access Control (RBAC).
    - Vector search enabled.
    - Firewall configured to allow your IP address.

## Create a Node.js project

1. Create a new directory for your project, and open it in Visual Studio Code:

   ```bash
   mkdir vector-search-quickstart
   code vector-search-quickstart
   ```

1. In the terminal, initialize a new Node.js project:

   ```bash
   npm set init.type module
   npm init -y
   ```

1. Install the required packages:

   ```bash
    npm install mongodb @azure/identity openai @types/node
    ```

    - `mongodb`: MongoDB Node.js driver.
    - `@azure/identity`: Azure Identity library for passwordless authentication.
    - `openai`: OpenAI client library to create vectors of the query.
    - `@types/node`: Type definitions for Node.js.

1. Create a `.env` file in the root of your project to store environment variables for password authentication used in this article:

    ```ini
    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
    AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
    AZURE_OPENAI_EMBEDDING_ENDPOINT=
    EMBEDDING_SIZE_BATCH=16

    # MongoDB configuration
    MONGO_CLUSTER_NAME=

    # Data file
    DATA_FILE_WITH_VECTORS=.HotelsData_toCosmosDB_Vector.json
    EMBEDDED_FIELD=text_embedding_ada_002
    EMBEDDING_DIMENSIONS=1536
    LOAD_SIZE_BATCH=100
    ```

    Update these values in the `.env` file with your own information:

    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: The endpoint URL of your Azure OpenAI resource.
    - `MONGO_CLUSTER_NAME`: The resource name of your MongoDB vCore resource.


    
1. Add a `tsconfig.json` file to configure TypeScript:

    :::code language="json" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-typescript/tsconfig.json" :::



1. Copy the `HotelsData_toCosmosDB_Vector.json` [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json) to the root of your project.

## Create npm scripts

Edit the `package.json` file to add the following scripts:

#### [IVF](#tab/tab-ivf)


    ```json
    "scripts": { 
        "build": "tsc",
        "start:ivf": "node --env-file .env dist/ivf.js"
    }
    ```

#### [HNSW](#tab/tab-hnsw)


    ```json
    "scripts": { 
        "build": "tsc",
        "start:hnsw": "node --env-file .env dist/hnsw.js"
    }
    ```

### [DiskANN](#tab/tab-diskann)


    ```json
    "scripts": { 
        "build": "tsc",
        "start:diskann": "node --env-file .env dist/diskann.js"
    }
    ```
    
----

## Create code files for vector search

#### [IVF](#tab/tab-ivf)

Create a `src` directory for your TypeScript files then create 2 files named `ivf.ts` and `utils.ts` in the `src` directory for the IVF index implementation:

```bash
mkdir src
touch src/ivf.ts
touch src/utils.ts
```

#### [HNSW](#tab/tab-hnsw)

Create a `src` directory for your TypeScript files then create 2 files named `ivf.ts` and `utils.ts` in the `src` directory for the IVF index implementation:

```bash
mkdir src
touch src/hnsw.ts
touch src/utils.ts
```

### [DiskANN](#tab/tab-diskann)

Create a `src` directory for your TypeScript files then create 2 files named `ivf.ts` and `utils.ts` in the `src` directory for the IVF index implementation:

```bash
mkdir src    
touch src/diskann.ts
touch src/utils.ts
```

----

## Create code for vector search


#### [IVF](#tab/tab-ivf)

Copy the following code into the `ivf.ts` file you created.

:::code language="typescript" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-typescript/src/ivf.ts" :::

#### [HNSW](#tab/tab-hnsw)

Copy the following code into the `hnsw.ts` file you created.

:::code language="typescript" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-typescript/src/hnsw.ts" :::

### [DiskANN](#tab/tab-diskann)

Copy the following code into the `diskann.ts` file you created.

:::code language="typescript" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-typescript/src/diskann.ts" :::

----

This code completes the following:

- Includes utility functions to simplify tasks. 
- Creates a configuration object to manage environment variables.
- Creates clients for Azure OpenAI and Azure Cosmos DB for MongoDB in vCore architecture.
- Connects to the MongoDB database, creates a database, collection, inserts data, and creates standard indexes.
- Creates a vector index using the specified index type (IVF, HNSW, or DiskANN).
- Creates an embedding for a sample query text using the OpenAI client. The query is at the top of the file and available for you to change.
- Performs a vector search using the created embedding and prints the results.

## Create utility functions

Copy the following code into `utils.ts`:

:::code language="typescript" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-typescript/src/utils.ts" :::

This utility module exports the following functionality:

- `JsonData`: Interface for the structure of the data being handled.
- `scoreProperty`: The location of the score in the query results based on vector search method.
- `getClients`: Function to create and return clients for Azure OpenAI and Azure Cosmos DB for MongoDB in vCore architecture.
- `getClientsPasswordless`: Function to create and return clients for Azure OpenAI and Azure Cosmos DB for MongoDB in vCore architecture using passwordless authentication. You must have enabled RBAC authentication on both resources to use this function and have the Azure CLI installed and be logged in.
- `readFileReturnJson`: Function to read a JSON file and return its contents as an array of `JsonData` objects.
- `writeFileJson`: Function to write an array of `JsonData` objects to a JSON file.
- `insertData`: Function to `insertMany` data in batches into a specified MongoDB collection. Create standard indexes on specified fields.
- `printSearchResults`: Function to print the results of a vector search, including the score and Hotel name.

## Authenticate with Azure CLI

Before running the application, authenticate with Azure CLI to ensure that your application can access the Azure resources securely.

```bash
az login
```

## Build and run the application

Build the TypeScript files and run the application:

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

### [DiskANN](#tab/tab-diskann)

```bash
npm run build
npm run start:diskann
```

----

The output includes the top 5 hotels that match the vector search query, along with their similarity scores.

## View and manage data in Visual Studio Code

1. Open the `src` folder in Visual Studio Code.
2. Use the DocumentDB extension for Visual Studio Code to connect to your Azure Cosmos DB account.
3. Install the MongoDB extension for Visual Studio Code for enhanced functionality.

## Clean up resources

When no longer needed, delete the resource group, MongoDB vCore account, and Azure OpenAI resource to avoid incurring further costs.

## Related content

- [Vector store in Azure Cosmos DB for MongoDB vCore](vector-search.md)
- [Support for Geospatial Queries](geospatial-support.md)