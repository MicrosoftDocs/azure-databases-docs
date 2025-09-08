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
zone_pivot_groups: azure-devlang-nodejs
appliesto:
  - ✅ MongoDB (vCore)
# CustomerIntent: As a developer, I want to learn how to use vector search in Node.js applications with Azure Cosmos DB for MongoDB (vCore).
---
# Quickstart: Vector Search with Node.js in Azure Cosmos DB for MongoDB (vCore)

In this quickstart, you learn how to use vector search in Azure Cosmos DB for MongoDB (vCore) using the Node.js client library. This quickstart demonstrates how to store and query vector data efficiently. 

The data for this quickstart is provided for you in a JSON file that includes pre-computed vectors using `text-embedding-ada-002` model. This hotel dataset is a sample dataset provided by Microsoft for learning purposes. It includes various attributes of hotels, such as their names, locations, descriptions, and vector embeddings.

The [sample code](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/typescript-mongo-vcore) is available on GitHub.

## Prerequisites

[!INCLUDE[Prerequisites - Azure subscription](includes/prereq-azure-subscription.md)]
- [Visual Studio Code](https://code.visualstudio.com/download).
- [Azure CLI](/cli/azure/install-azure-cli)
- [Node.js LTS](https://nodejs.org/download/)
- [TypeScript](https://www.typescriptlang.org/download): You can globally install TypeScript using npm:

   ```bash
   npm install -g typescript
   ```
- [Azure OpenAI resource](/azure/ai-foundry/openai)
    - With deployment of `text-embedding-ada-002` model
- [MongoDB vCore resource](quickstart-portal.md) with:
    - vector search enabled
    - firewall configured to allow your IP address

[!INCLUDE[Prerequisites - Azure Developer CLI](../includes/prereq-dev-quickstart.md)]

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
    npm install mongodb @azure/identity openai uuid dotenv
    ```

    - mongodb - MongoDB Node.js driver
    - @azure/identity - Azure Identity library for authentication
    - openai - OpenAI client library
    - uuid - Library to generate unique identifiers
    - dotenv - Library to manage environment variables

1. Create a `.env` file in the root of your project to store environment variables:

    ```ini
    # OpenAI configuration
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
    AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
    AZURE_OPENAI_EMBEDDING_KEY=
    AZURE_OPENAI_EMBEDDING_ENDPOINT=

    # MongoDB configuration
    MONGO_CONNECTION_STRING=
    MONGO_DB_NAME=HotelSet
    MONGO_COLLECTION_NAME=hotels
    INDEX_NAME=vectorSearchIndex

    # Data file
    DATA_FILE_WITH_VECTORS=.HotelsData_toCosmosDB_Vector.json
    EMBEDDED_FIELD=text_embedding_ada_002
    EMBEDDING_DIMENSIONS=1536
    ```

    Update these values in the `.env` file with your own information:

    - `AZURE_OPENAI_EMBEDDING_KEY`: The key for your Azure OpenAI resource.
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: The endpoint URL for your Azure OpenAI resource.
    - `MONGO_CONNECTION_STRING`: The connection string for your MongoDB vCore resource.


#### [IVF](#tab/tab-ivf)

1. Edit the `package.json` file to add the following scripts:

    ```json
    "scripts": { 
        "build": "tsc",
        "start:ivf": "node --env-file .env dist/ivf.js"
    }
    ```

#### [HNSW](#tab/tab-hnsw)

1. Edit the `package.json` file to add the following scripts:

    ```json
    "scripts": { 
        "build": "tsc",
        "start:hnsw": "node --env-file .env dist/hnsw.js"
    }
    ```

### [DiskANN](#tab/tab-diskann)

1. Edit the `package.json` file to add the following scripts:

    ```json
    "scripts": { 
        "build": "tsc",
        "start:diskann": "node --env-file .env dist/diskann.js"
    }
    ```

----

1. Add a `tsconfig.json` file to configure TypeScript:

    :::code language="json" source="~/cosmos-db-vector-samples/typescript-mongo-vcore/tsconfig.json" :::

1. Create a `src` directory for your TypeScript files:

   ```bash
   mkdir src
   ```

1. Copy the `HotelsData_toCosmosDB_Vector.json` [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json) to the root of your project.


#### [IVF](#tab/tab-ivf)

1. Create a new file named `ivf.ts` in the `src` directory for the IVF index implementation:

   ```bash
   touch src/ivf.ts
   ```

#### [HNSW](#tab/tab-hnsw)

   Create a new file named `hnsw.ts` in the `src` directory for the HNSW index implementation:

   ```bash
   touch src/hnsw.ts
   ```

### [DiskANN](#tab/tab-diskann)

   Create a new file named `diskann.ts` in the `src` directory for the DiskANN index implementation:

   ```bash
   touch src/diskann.ts
   ```

----

## Create code for vector search

Copy the following code into the code file you just created.

#### [IVF](#tab/tab-ivf)

:::code language="typescript" source="~/cosmos-db-vector-samples/typescript-mongo-vcore/src/ivf.ts" :::

#### [HNSW](#tab/tab-hnsw)

:::code language="typescript" source="~/cosmos-db-vector-samples/typescript-mongo-vcore/src/hnsw.ts" :::

### [DiskANN](#tab/tab-diskann)

:::code language="typescript" source="~/cosmos-db-vector-samples/typescript-mongo-vcore/src/diskann.ts" :::

----

This code completes the following:

- Includes utility functions to connect to the MongoDB database, create the vector index, load data with vectors, and perform vector searches. 
- Creates a configuration object to manage environment variables.
- Creates clients for Azure OpenAI and Azure Cosmos DB for MongoDB in vCore architecture.
- Connects to the MongoDB database, creates a database, collection, inserts data, and creates standard indexes.
- Creates a vector index using the specified index type (IVF, HNSW, or DiskANN).
- Creates an embedding for a sample query text using the OpenAI client. The query is at the top of the file and available for you to change.
- Performs a vector search using the created embedding and prints the results.

## Create utility functions

1. Create a new file named `utils.ts` in the `src` directory for utility functions:

   ```bash
   touch src/utils.ts
   ```

1. Copy the following code into `utils.ts`:

    :::code language="typescript" source="~/cosmos-db-vector-samples/typescript-mongo-vcore/src/utils.ts" :::

This utility module exports the following functionality:

- `JsonData`: Interface for the structure of the data being handled.
- `scoreProperty`: The location of the score in the query results based on vector search method.
- `getClients`: Function to create and return clients for Azure OpenAI and Azure Cosmos DB for MongoDB in vCore architecture.
- `readFileReturnJson`: Function to read a JSON file and return its contents as an array of `JsonData` objects.
- `writeFileJson`: Function to write an array of `JsonData` objects to a JSON file.
- `insertData`: Function to `insertMany` data in batches into a specified MongoDB collection. Create standard indexes on specified fields.
- `printSearchResults`: Function to print the results of a vector search, including the score and Hotel name.

## Run the application

1. Build the TypeScript files:

   ```bash
   npm run build
   ```

1. Run the application:

#### [IVF](#tab/tab-ivf)

```bash
npm run start:ivf
```

#### [HNSW](#tab/tab-hnsw)

```bash
npm run start:hnsw
```

### [DiskANN](#tab/tab-diskann)

```bash
npm run start:diskann
```

----

The output includes the top 5 hotels that match the vector search query, along with their similarity scores.

## Clean up resources

When no longer needed, delete the resource group, MongoDB vCore account, and Azure OpenAI resource to avoid incurring further costs.

## Related content

- [Vector store in Azure Cosmos DB for MongoDB vCore](vector-search.md)
- [Support for Geospatial Queries](geospatial-support.md)