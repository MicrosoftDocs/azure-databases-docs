---
title: Quickstart - Vector Search with Go
description: Learn how to use vector search in Azure DocumentDB with Go. Store and query vector data efficiently in your applications. 
author: PatAltimore
ms.author: patricka
ms.reviewer: khelanmodi
ms.devlang: golang
ms.topic: quickstart-sdk
ms.date: 12/02/2025
ms.custom: devx-track-go, devx-track-go-ai, devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Go applications with Azure DocumentDB
---
# Quickstart: Vector search with Go in Azure DocumentDB

Use vector search in Azure DocumentDB with the Go client library. Store and query vector data efficiently.

This quickstart uses a sample hotel dataset in a JSON file with vectors from the `text-embedding-ada-002` model. The dataset includes hotel names, locations, descriptions, and vector embeddings.

Find the [sample code](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/patricka-go/mongo-vcore-vector-search-go) on GitHub.

## Prerequisites

[!INCLUDE[Prerequisites - Vector Search Quickstart](includes/prerequisite-quickstart-vector-search.md)]

- [Go](https://golang.org/dl/) version 1.21 or later

## Create a Go project

1. Create a new directory for your project and open it in Visual Studio Code:

    ```bash
    mkdir vector-search-quickstart
    cd vector-search-quickstart
    code .
    ```

1. Initialize a Go module:

    ```bash
    go mod init vector-search-quickstart
    ```

1. Install the required Go packages:

    ```bash
    go get go.mongodb.org/mongo-driver/mongo
    go get go.mongodb.org/mongo-driver/bson
    go get github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai
    go get github.com/Azure/azure-sdk-for-go/sdk/azidentity
    go get github.com/joho/godotenv
    ```

    - `go.mongodb.org/mongo-driver`: MongoDB Go driver
    - `github.com/Azure/azure-sdk-for-go/sdk/azidentity`: Azure Identity library for passwordless token-based authentication
    - `github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai`: Azure OpenAI client library to create vectors
    - `github.com/joho/godotenv`: Environment variable loading from .env files

1. Create a `.env` file in your project root for environment variables:

    ```ini
    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
    AZURE_OPENAI_EMBEDDING_API_VERSION=2024-02-01
    AZURE_OPENAI_EMBEDDING_ENDPOINT=
    EMBEDDING_SIZE_BATCH=16

    # Azure DocumentDB configuration
    MONGO_CLUSTER_NAME=

    # Data file
    DATA_FILE_WITH_VECTORS=data/HotelsData_toCosmosDB_Vector.json
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536
    LOAD_SIZE_BATCH=100
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL
    - `MONGO_CLUSTER_NAME`: Your Azure DocumentDB resource name

    You should always prefer passwordless authentication, but it requires additional setup. For more information on setting up managed identity and the full range of your authentication options, see [Authenticate Go apps to Azure services by using the Azure Identity library](/azure/developer/go/sdk/authentication/authentication-overview).

1. Copy the `HotelsData_toCosmosDB_Vector.json` [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/cosmos-db-vector-samples/refs/heads/main/data/HotelsData_toCosmosDB_Vector.json) to your project root.

## Create Go source files for vector search

### [DiskANN](#tab/tab-diskann)

Create a `src` directory for your Go files. Add two files: `diskann.go` and `utils.go` for the DiskANN index implementation:

```bash
mkdir src    
touch src/diskann.go
touch src/utils.go
```

#### [IVF](#tab/tab-ivf)

Create a `src` directory for your Go files. Add two files: `ivf.go` and `utils.go` for the IVF index implementation:

```bash
mkdir src
touch src/ivf.go
touch src/utils.go
```

#### [HNSW](#tab/tab-hnsw)

Create a `src` directory for your Go files. Add two files: `hnsw.go` and `utils.go` for the HNSW index implementation:

```bash
mkdir src
touch src/hnsw.go
touch src/utils.go
```

----

## Create code for vector search

### [DiskANN](#tab/tab-diskann)

Add the following code to the `src/diskann.go` file:

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-go/src/diskann.go" :::

#### [IVF](#tab/tab-ivf)

Add the following code to the `src/ivf.go` file:

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-go/src/ivf.go" :::

#### [HNSW](#tab/tab-hnsw)

Add the following code to the `src/hnsw.go` file:

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-go/src/hnsw.go" :::

----

This main module provides these features:

- Includes utility functions
- Creates a configuration struct for environment variables
- Creates clients for Azure OpenAI and Azure DocumentDB
- Connects to DocumentDB, creates a database and collection, inserts data, and creates standard indexes
- Creates a vector index using IVF, HNSW, or DiskANN
- Creates an embedding for a sample query text using the OpenAI client. You can change the query in the main function
- Runs a vector search using the embedding and prints the results

## Create utility functions

Add the following code to `src/utils.go`:

:::code language="go" source="~/cosmos-db-vector-samples/mongo-vcore-vector-search-go/src/utils.go" :::

This utility module provides these features:

- `Config`: Configuration structure for environment variables
- `SearchResult`: Structure for search result documents with scores
- `HotelData`: Structure representing hotel documents
- `GetClients`: Creates and returns clients for Azure OpenAI and Azure DocumentDB
- `GetClientsPasswordless`: Creates and returns clients using passwordless authentication (OIDC). Enable RBAC on both resources and sign in to Azure CLI
- `ReadFileReturnJSON`: Reads a JSON file and returns its contents as a slice of maps
- `WriteFileJSON`: Writes data to a JSON file
- `InsertData`: Inserts data in batches into a MongoDB collection and creates standard indexes on specified fields
- `PrintSearchResults`: Prints the results of a vector search, including the score and hotel name
- `GenerateEmbedding`: Creates embeddings using Azure OpenAI

## Authenticate with Azure CLI

Sign in to Azure CLI before you run the application so it can access Azure resources securely.

```bash
az login
```

## Build and run the application

Build and run the Go application:

### [DiskANN](#tab/tab-diskann)

```bash
go mod tidy
go run src/diskann.go src/utils.go
```

#### [IVF](#tab/tab-ivf)

```bash
go mod tidy
go run src/ivf.go src/utils.go
```

```bash
go run src/hnsw.go src/utils.go
```

```bash
go mod tidy
go run src/ivf.go src/utils.go
```

#### [HNSW](#tab/tab-hnsw)

```bash
go run src/hnsw.go src/utils.go
```

----

The app logging and output show:

- Collection creation and data insertion status
- Vector index creation 
- Search results with hotel names and similarity scores

### [DiskANN](#tab/tab-diskann)

```console
Starting DiskANN vector search demonstration...

Initializing MongoDB and Azure OpenAI clients...
OIDC authentication successful!

Loading data from HotelsData_toCosmosDB_Vector.json...
Loaded 50 documents

Inserting data into collection 'vectorSearchCollection'...
Cleared 0 existing documents from collection
Starting batch insertion of 50 documents...
Created index on field: HotelId
Batch 1 completed: 50 documents inserted
Insertion completed: 50 inserted, 0 failed
Creating DiskANN vector index on field 'DescriptionVector'...
DiskANN vector index created successfully
Waiting for index to be ready...
Performing DiskANN vector search for: 'quintessential lodging near running trails, eateries, retail'

Search Results (showing top 5):
================================================================================
HotelName: Roach Motel, Score: 0.8399
HotelName: Royal Cottage Resort, Score: 0.8385
HotelName: Economy Universe Motel, Score: 0.8360
HotelName: Foot Happy Suites, Score: 0.8354
HotelName: Country Comfort Inn, Score: 0.8346

DiskANN demonstration completed successfully!
```

#### [IVF](#tab/tab-ivf)

```console
Starting IVF vector search demonstration...

Initializing MongoDB and Azure OpenAI clients...
OIDC authentication successful!

Loading data from HotelsData_toCosmosDB_Vector.json...
Loaded 50 documents

Preparing collection 'vectorSearchCollection'...
Cleared 0 existing documents from collection
Starting batch insertion of 50 documents...
Created index on field: HotelId
Batch 1 completed: 50 documents inserted
Insertion completed: 50 inserted, 0 failed

Creating IVF vector index...
IVF vector index created successfully
Waiting for index clustering to complete...
Performing IVF vector search for: 'quintessential lodging near running trails, eateries, retail'

Search Results (showing top 5):
================================================================================
HotelName: Roach Motel, Score: 0.8399
HotelName: Royal Cottage Resort, Score: 0.8385
HotelName: Economy Universe Motel, Score: 0.8360
HotelName: Foot Happy Suites, Score: 0.8354
HotelName: Country Comfort Inn, Score: 0.8346

IVF demonstration completed successfully!
```

#### [HNSW](#tab/tab-hnsw)

```console
Starting HNSW vector search demonstration...

Initializing MongoDB and Azure OpenAI clients...
OIDC authentication successful!

Loading data from HotelsData_toCosmosDB_Vector.json...
Loaded 50 documents

Preparing collection 'vectorSearchCollection'...
Cleared 0 existing documents from collection
Starting batch insertion of 50 documents...
Created index on field: HotelId
Batch 1 completed: 50 documents inserted
Insertion completed: 50 inserted, 0 failed

Creating HNSW vector index...
HNSW vector index created successfully
Waiting for index to be ready...
Performing HNSW vector search for: 'quintessential lodging near running trails, eateries, retail'

Search Results (showing top 5):
================================================================================
HotelName: Roach Motel, Score: 0.8399
HotelName: Royal Cottage Resort, Score: 0.8385
HotelName: Economy Universe Motel, Score: 0.8360
HotelName: Foot Happy Suites, Score: 0.8354
HotelName: Country Comfort Inn, Score: 0.8346

HNSW demonstration completed successfully!
```

----

## View and manage data in Visual Studio Code

1. Select the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) in Visual Studio Code to connect to your Azure DocumentDB account.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-go-vector-search/visual-studio-code-documentdb.png" lightbox="./media/quickstart-go-vector-search/visual-studio-code-documentdb.png" alt-text="Screenshot of DocumentDB extension showing the Azure DocumentDB collection.":::

## Clean up resources

Delete the resource group, DocumentDB account, and Azure OpenAI resource when you don't need them to avoid extra costs.

## Related content

- [Vector store in Azure DocumentDB](vector-search.md)
- [Support for geospatial queries](geospatial-support.md)