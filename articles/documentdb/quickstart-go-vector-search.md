---
title: Quickstart - Vector Search with Go
description: Learn how to use vector search in Azure DocumentDB with Go. Store and query vector data efficiently in your applications. 
author: PatAltimore
ms.author: patricka
ms.reviewer: khelanmodi
ms.devlang: golang
ms.topic: quickstart-sdk
ms.date: 02/19/2026
ai-usage: ai-assisted
ms.custom: devx-track-go, devx-track-go-ai, devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Go applications with Azure DocumentDB
---
# Quickstart: Vector search with Go in Azure DocumentDB

Use vector search in Azure DocumentDB with the Go client library. Store and query vector data efficiently.

This quickstart uses a sample hotel dataset in a JSON file with pre-calculated vectors from the `text-embedding-3-small` model. The dataset includes hotel names, locations, descriptions, and vector embeddings.

Find the [sample code](https://github.com/Azure-Samples/documentdb-samples/tree/main/ai/vector-search-go) on GitHub.

## Prerequisites

[!INCLUDE[Prerequisites - Vector Search Quickstart](includes/prerequisite-quickstart-vector-search-model.md)]

- [Go](https://golang.org/dl/) version 1.24 or later

## Create data file with vectors

1. Create a new data directory for the hotels data file:

    ```bash
    mkdir data
    ```

1. Copy the `Hotels_Vector.json` [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/documentdb-samples/refs/heads/main/ai/data/Hotels_Vector.json) to your `data` directory.


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
    go get go.mongodb.org/mongo-driver
    go get github.com/Azure/azure-sdk-for-go/sdk/azcore
    go get github.com/Azure/azure-sdk-for-go/sdk/azidentity
    go get github.com/openai/openai-go/v3
    go get github.com/joho/godotenv
    ```

    - `go.mongodb.org/mongo-driver`: MongoDB Go driver
    - `github.com/Azure/azure-sdk-for-go/sdk/azcore`: Azure SDK core utilities for HTTP pipelines and auth
    - `github.com/Azure/azure-sdk-for-go/sdk/azidentity`: Azure Identity library for passwordless token-based authentication
    - `github.com/openai/openai-go/v3`: OpenAI Go client library to create vectors
    - `github.com/joho/godotenv`: Environment variable loading from .env files

1. Create a `.env` file in your project root for environment variables:

    ```ini
    # Identity for local developer authentication with Azure CLI
    AZURE_TOKEN_CREDENTIALS=AzureCliCredential

    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
    AZURE_OPENAI_EMBEDDING_ENDPOINT=<AZURE_OPENAI_ENDPOINT>
    EMBEDDING_SIZE_BATCH=16

    # Azure DocumentDB configuration
    MONGO_CLUSTER_NAME=<DOCUMENTDB_NAME>

    # Data file
    DATA_FILE_WITH_VECTORS=../data/Hotels_Vector.json
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536
    LOAD_SIZE_BATCH=50
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL
    - `MONGO_CLUSTER_NAME`: Your Azure DocumentDB resource name

    You should always prefer passwordless authentication, but it requires additional setup. For more information on setting up managed identity and the full range of your authentication options, see [Authenticate Go apps to Azure services by using the Azure Identity library](/azure/developer/go/sdk/authentication/authentication-overview).

## Create Go source files for vector search

Continue the project by creating code files for vector search. 

### [DiskANN](#tab/tab-diskann)

Create a `src` directory for your Go files. Add two files: `diskann.go` and `utils.go` for the DiskANN index implementation:

```bash
mkdir src    
touch src/diskann.go
touch src/utils.go
```

When you are done, the project structure should look like this:

```plaintext
data
│── Hotels_Vector.json
vector-search-quickstart
├── .env
├── go.mod
├── src
│   ├── diskann.go
│   └── utils.go
```

#### [IVF](#tab/tab-ivf)

Create a `src` directory for your Go files. Add two files: `ivf.go` and `utils.go` for the IVF index implementation:

```bash
mkdir src
touch src/ivf.go
touch src/utils.go
```

When you are done, the project structure should look like this:

```plaintext
data
│── Hotels_Vector.json
vector-search-quickstart
├── .env
├── go.mod
├── src
│   ├── ivf.go
│   └── utils.go
```

#### [HNSW](#tab/tab-hnsw)

Create a `src` directory for your Go files. Add two files: `hnsw.go` and `utils.go` for the HNSW index implementation:

```bash
mkdir src
touch src/hnsw.go
touch src/utils.go
```

When you are done, the project structure should look like this:

```plaintext
data
│── Hotels_Vector.json
vector-search-quickstart
├── .env
├── go.mod
├── src
│   ├── hnsw.go
│   └── utils.go
```

----

## Create code for vector search

### [DiskANN](#tab/tab-diskann)

Add the following code to the `src/diskann.go` file:

:::code language="go" source="~/documentdb-samples/ai/vector-search-go/src/diskann.go" :::

#### [IVF](#tab/tab-ivf)

Add the following code to the `src/ivf.go` file:

:::code language="go" source="~/documentdb-samples/ai/vector-search-go/src/ivf.go" :::

#### [HNSW](#tab/tab-hnsw)

Add the following code to the `src/hnsw.go` file:

:::code language="go" source="~/documentdb-samples/ai/vector-search-go/src/hnsw.go" :::

----

This main module provides these features:

- Includes utility functions
- Creates a configuration struct for environment variables
- Creates clients for Azure OpenAI and Azure DocumentDB
- Connects to MongoDB, creates a database and collection, inserts data, and creates standard indexes
- Creates a vector index using IVF, HNSW, or DiskANN
- Creates an embedding for a sample query text using the OpenAI client. You can change the query in the main function
- Runs a vector search using the embedding and prints the results

## Create utility functions

Add the following code to `src/utils.go`:

:::code language="go" source="~/documentdb-samples/ai/vector-search-go/src/utils.go" :::

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

The code uses your local developer authentication to access Azure DocumentDB and Azure OpenAI. When you set `AZURE_TOKEN_CREDENTIALS=AzureCliCredential`, this setting tells the function to use Azure CLI credentials for authentication _deterministically_. The authentication relies on [DefaultAzureCredential](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity#DefaultAzureCredential) from **azidentity** to find your Azure credentials in the environment. Learn more about how to [Authenticate Go apps to Azure services by using the Azure Identity library](/azure/developer/go/sdk/authentication/authentication-overview).

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

#### [HNSW](#tab/tab-hnsw)

```bash
go mod tidy
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
Attempting OIDC authentication...
OIDC authentication successful!

Loading data from ../data/Hotels_Vector.json...
Loaded 50 documents

Inserting data into collection 'hotels_diskann'...
Getting token with scope: https://ossrdbms-aad.database.windows.net/.default
Successfully obtained token
Starting batch insertion of 50 documents...
Batch 1 completed: 50 documents inserted
Insertion completed: 50 inserted, 0 failed
Creating DiskANN vector index on field 'DescriptionVector'...
No existing vector indexes found to drop
DiskANN vector index created successfully
Waiting for index to be ready...
Performing DiskANN vector search for: 'quintessential lodging near running trails, eateries, retail'

Search Results (showing top 5):
================================================================================
1. HotelName: Royal Cottage Resort, Score: 0.4991
2. HotelName: Country Comfort Inn, Score: 0.4785
3. HotelName: Nordick's Valley Motel, Score: 0.4635
4. HotelName: Economy Universe Motel, Score: 0.4461
5. HotelName: Roach Motel, Score: 0.4388

DiskANN demonstration completed successfully!
```

#### [IVF](#tab/tab-ivf)

```console
Starting IVF vector search demonstration...

Initializing MongoDB and Azure OpenAI clients...
Attempting OIDC authentication...
OIDC authentication successful!

Loading data from ../data/Hotels_Vector.json...
Loaded 50 documents

Preparing collection 'hotels_ivf'...
Getting token with scope: https://ossrdbms-aad.database.windows.net/.default
Successfully obtained token
Cleared 50 existing documents from collection
Starting batch insertion of 50 documents...
Batch 1 completed: 50 documents inserted
Insertion completed: 50 inserted, 0 failed

Creating IVF vector index...
Creating IVF vector index on field 'DescriptionVector'...
Dropping existing vector index: hnsw_index_DescriptionVector
Dropped 1 existing vector index(es)
IVF vector index created successfully
Waiting for index clustering to complete...
Performing IVF vector search for: 'quintessential lodging near running trails, eateries, retail'

Search Results (showing top 5):
================================================================================
1. HotelName: Royal Cottage Resort, Score: 0.4991
2. HotelName: Country Comfort Inn, Score: 0.4785
3. HotelName: Nordick's Valley Motel, Score: 0.4635
4. HotelName: Economy Universe Motel, Score: 0.4461
5. HotelName: Roach Motel, Score: 0.4388

IVF demonstration completed successfully!
```

#### [HNSW](#tab/tab-hnsw)

```console
Starting HNSW vector search demonstration...

Initializing MongoDB and Azure OpenAI clients...
Attempting OIDC authentication...
OIDC authentication successful!

Loading data from ../data/Hotels_Vector.json...
Loaded 50 documents

Preparing collection 'hotels_hnsw'...
Getting token with scope: https://ossrdbms-aad.database.windows.net/.default
Successfully obtained token
Cleared 50 existing documents from collection
Starting batch insertion of 50 documents...
Batch 1 completed: 50 documents inserted
Insertion completed: 50 inserted, 0 failed

Creating HNSW vector index...
Creating HNSW vector index on field 'DescriptionVector'...
Dropping existing vector index: diskann_index_DescriptionVector
Dropped 1 existing vector index(es)
HNSW vector index created successfully
Waiting for index to be ready...
Performing HNSW vector search for: 'quintessential lodging near running trails, eateries, retail'

Search Results (showing top 5):
================================================================================
1. HotelName: Royal Cottage Resort, Score: 0.4991
2. HotelName: Country Comfort Inn, Score: 0.4785
3. HotelName: Nordick's Valley Motel, Score: 0.4635
4. HotelName: Economy Universe Motel, Score: 0.4461
5. HotelName: Roach Motel, Score: 0.4388

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