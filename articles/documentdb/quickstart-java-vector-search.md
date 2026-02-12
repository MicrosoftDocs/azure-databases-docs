---
title: Quickstart - Vector Search with Java
description: Learn how to use vector search in Azure DocumentDB with Java. Store and query vector data efficiently in your applications.
author: diberry
ms.author: diberry
ms.reviewer: khelanmodi
ms.devlang: java
ms.topic: quickstart-sdk
ms.date: 02/12/2026
ai-usage: ai-assisted
ms.custom:
  - devx-track-java
  - devx-track-java-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to learn how to use vector search in Java applications with Azure DocumentDB.
---

# Quickstart: Vector search with Java in Azure DocumentDB

Learn to use vector search in Azure DocumentDB with the Java MongoDB driver to store and query vector data efficiently.

This quickstart provides a guided tour of key vector search techniques using a [Java sample app](https://github.com/Azure-Samples/documentdb-samples/tree/main/ai/vector-search-java) on GitHub.

The app uses a sample hotel dataset in a JSON file with pre-calculated vectors from the `text-embedding-3-small` model, though you can also generate the vectors yourself. The hotel data includes hotel names, locations, descriptions, and vector embeddings.

## Prerequisites

[!INCLUDE[Prerequisites - Vector Search Quickstart](includes/prerequisite-quickstart-vector-search-model.md)]

- [Java 21](/java/openjdk/download) or later

- [Maven 3.6](https://maven.apache.org/download.cgi) or later


## Create data file with vectors

1. Create a new data directory for the hotels data file:

    ```bash
    mkdir data
    ```

1. Copy the `Hotels_Vector.json` [raw data file with vectors](https://raw.githubusercontent.com/Azure-Samples/documentdb-samples/refs/heads/main/ai/data/Hotels_Vector.json) to your `data` directory.

## Create a Java project

1. Create a new sibling directory for your project, at the same level as the data directory, and open it in Visual Studio Code:

    ```bash
    mkdir vector-search-quickstart
    mkdir vector-search-quickstart/src
    code vector-search-quickstart
    ```

1. Create a `pom.xml` file in the project root with the following content:

    :::code language="xml" source="~/documentdb-samples/ai/vector-search-java/pom.xml" :::

    The app uses the following Maven dependencies specified in the []`pom.xml`:
    
    - [`mongodb-driver-sync`](https://mvnrepository.com/artifact/org.mongodb/mongodb-driver-sync): Official MongoDB Java driver for database connectivity and operations
    - [`azure-identity`](https://mvnrepository.com/artifact/com.azure/azure-identity): Azure Identity library for passwordless authentication with Microsoft Entra ID
    - [`azure-ai-openai`](https://mvnrepository.com/artifact/com.azure/azure-ai-openai): Azure OpenAI client library to communicate with AI models and create vector embeddings
    - [`jackson-databind`](https://mvnrepository.com/artifact/tools.jackson.core/jackson-databind): JSON serialization and deserialization library
    

1. Create a `.env` file in your project root for environment variables:

    ```ini
    # Azure OpenAI Embedding Settings
    AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
    AZURE_OPENAI_EMBEDDING_ENDPOINT=
    EMBEDDING_SIZE_BATCH=16

    # Azure DocumentDB configuration
    MONGO_CLUSTER_NAME=
    AZURE_MANAGED_IDENTITY_PRINCIPAL_ID=

    # Data file
    DATA_FILE_WITH_VECTORS=../data/Hotels_Vector.json
    EMBEDDED_FIELD=DescriptionVector
    EMBEDDING_DIMENSIONS=1536
    LOAD_SIZE_BATCH=50
    ```

    Replace the placeholder values in the `.env` file with your own information:
    - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI resource endpoint URL.
    - `MONGO_CLUSTER_NAME`: Your Azure DocumentDB resource name.

1. Load the environment variables:

    ```bash
    set -a && source .env && set +a
    ```

1. The project structure should look like this:

    ```plaintext
    data
    └── Hotels_Vector.json
    vector-search-quickstart
    ├── .env
    ├── pom.xml
    └── src
    ```

## Add code for vector search

#### [DiskANN](#tab/tab-diskann)

Create a `DiskAnn.java` file in the `src` directory and paste in the following code:

:::code language="java" source="~/documentdb-samples/ai/vector-search-java/src/main/java/com/azure/documentdb/samples/DiskAnn.java" :::

#### [IVF](#tab/tab-ivf)

Create an `IVF.java` file in the `src` directory and paste in the following code:

:::code language="java" source="~/documentdb-samples/ai/vector-search-java/src/main/java/com/azure/documentdb/samples/IVF.java" :::

#### [HNSW](#tab/tab-hnsw)

Create an `HNSW.java` file in the `src` directory and paste in the following code:

:::code language="java" source="~/documentdb-samples/ai/vector-search-java/src/main/java/com/azure/documentdb/samples/HNSW.java" :::

---

This code performs the following tasks:

- Creates a passwordless connection to Azure DocumentDB using `DefaultAzureCredential` and the MongoDB OIDC mechanism
- Creates an Azure OpenAI client for generating embeddings
- Drops and recreates the collection, then loads hotel data from the JSON file in batches
- Creates standard indexes and a vector index with algorithm-specific options
- Generates an embedding for a sample query and runs an aggregation search pipeline
- Prints the top five matching hotels with similarity scores

## Authenticate to Azure

Sign in to Azure before you run the application so it can access Azure resources securely.

> [!NOTE]
> Ensure your signed-in identity has the required data plane roles on both the Azure DocumentDB account and the Azure OpenAI resource.

```bash
az login
```

## Build and run the application

Load the environment variables, compile, and run:

```bash
mvn clean compile
```

#### [DiskANN](#tab/tab-diskann)

Run DiskANN (Disk-based Approximate Nearest Neighbor) search:

```bash
mvn exec:java -Dexec.mainClass="com.azure.documentdb.samples.DiskAnn"
```

DiskANN is optimized for large datasets that don't fit in memory, efficient disk-based storage, and a good balance of speed and accuracy.

Example output:

:::code language="output" source="~/documentdb-samples/ai/vector-search-java/output/diskann.txt" :::

#### [IVF](#tab/tab-ivf)

Run IVF (Inverted File) search:

```bash
mvn exec:java -Dexec.mainClass="com.azure.documentdb.samples.IVF"
```

IVF clusters vectors by similarity and provides fast search through cluster centroids. It offers configurable accuracy vs speed trade-offs for large vector datasets.

Example output:

:::code language="output" source="~/documentdb-samples/ai/vector-search-java/output/ivf.txt" :::

#### [HNSW](#tab/tab-hnsw)

Run HNSW (Hierarchical Navigable Small World) search:

```bash
mvn exec:java -Dexec.mainClass="com.azure.documentdb.samples.HNSW"
```

HNSW provides excellent search performance with high recall rates using a hierarchical graph structure, making it suitable for real-time applications.

Example output:

:::code language="output" source="~/documentdb-samples/ai/vector-search-java/output/hnsw.txt" :::

---

## View and manage data in Visual Studio Code

1. Install the [DocumentDB extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb) and [Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack) in Visual Studio Code.
1. Connect to your Azure DocumentDB account using the DocumentDB extension.
1. View the data and indexes in the Hotels database.

    :::image type="content" source="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" lightbox="./media/quickstart-nodejs-vector-search/visual-studio-code-documentdb.png" alt-text="Screenshot of DocumentDB extension showing the DocumentDB collection.":::

## Clean up resources

Delete the resource group, Azure DocumentDB cluster, and Azure OpenAI resource when you no longer need them to avoid unnecessary costs.

## Related content

- [Vector store in Azure DocumentDB](vector-search.md)
- [Support for geospatial queries](geospatial-support.md)
