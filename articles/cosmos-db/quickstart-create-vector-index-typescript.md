---
title: Quickstart - Create a vector index with TypeScript
description: Learn how to create a vector index in Azure Cosmos DB for NoSQL using the Azure Resource Manager SDK and TypeScript, then insert documents and run vector similarity queries.
author: diberry
ms.author: diberry
ms.reviewer: sidandrews
ms.devlang: typescript
ms.topic: quickstart-sdk
ms.date: 03/13/2026
ms.service: azure-cosmos-db
ms.subservice: nosql
ai-usage: ai-assisted
ms.custom:
  - devx-track-ts
  - devx-track-ts-ai
  - devx-track-data-ai
# CustomerIntent: As a developer, I want to create a container with a vector index using TypeScript so I can store and query embeddings efficiently.
---

# Quickstart: Create a vector index in Azure Cosmos DB for NoSQL with TypeScript

In this quickstart, you create a container with a vector index using the Azure Resource Manager SDK for TypeScript. You then insert documents with embeddings and run vector similarity queries. This sample demonstrates the complete workflow: provisioning Azure resources, creating a container with vector indexing via the control plane (ARM SDK), and using the data plane (Cosmos DB SDK) to insert and query data.

Find the [sample code](https://github.com/Azure-Samples/cosmos-db-vector-samples/tree/main/nosql-create-index-typescript) on GitHub.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/).
- [Node.js LTS](https://nodejs.org/)
- [Azure CLI](/cli/azure/install-azure-cli)
- [Git](https://git-scm.com/downloads)
- Azure subscription with access to [Azure OpenAI Service](https://aka.ms/oai/access)

## Clone the repository

Clone the sample repository and navigate to the TypeScript sample directory:

```bash
git clone https://github.com/Azure-Samples/cosmos-db-vector-samples.git
cd cosmos-db-vector-samples/nosql-create-index-typescript
```

## Overview: What you'll build

This sample demonstrates a three-layer architecture for creating and using vector indexes in Azure Cosmos DB:

| Layer | Tool | What it does |
|---|---|---|
| **Azure CLI script** | `scripts/create-resources.sh` | Creates resource group, Azure OpenAI, Cosmos DB account, database, and RBAC assignments |
| **Configuration** | `src/config.ts` | Loads and validates environment variables into a typed configuration object |
| **Control plane** | `src/control-plane.ts` using `@azure/arm-cosmosdb` | Creates container with vector index and data-plane RBAC using Azure Resource Manager SDK |
| **Data plane** | `src/data-plane.ts` using `@azure/cosmos` and `openai` | Inserts documents with embeddings and runs vector similarity queries |

The workflow:
1. Create a container with a vector index (DiskANN or Quantized flat) via ARM SDK
2. Create a custom data-plane RBAC role definition and assignment
3. Verify embedding dimensions match between OpenAI model and container configuration
4. Bulk insert 50 hotel documents with pre-computed embeddings
5. Run a vector similarity query using `VectorDistance()` function

## Create Azure resources

Sign in to Azure CLI:

```bash
az login
```

Run the setup script to create all required Azure resources:

```bash
chmod +x scripts/create-resources.sh
./scripts/create-resources.sh
```

The script creates:
- Resource group
- Azure Cosmos DB for NoSQL account
- Database named `Hotels`
- Azure OpenAI account with `text-embedding-3-small` deployment
- Role assignments:
  - **Contributor** (control plane access)
  - **Cognitive Services OpenAI User** (embedding generation)
  - **Cosmos DB Built-in Data Contributor** (data access)

The script outputs environment variables that you need for the `.env` file. Copy the `.env` values from the script output or use the generated `.env` file.

## Configure environment variables

Copy the sample environment file and update it with your values:

```bash
cp sample.env .env
```

Your `.env` file should look like this:

```ini
AZURE_TOKEN_CREDENTIALS=AzureCliCredential
AZURE_SUBSCRIPTION_ID="your-subscription-id"
AZURE_RESOURCE_GROUP="cosmos-vector-rg"
AZURE_LOCATION="eastus2"
AZURE_USER_PRINCIPAL_ID="your-user-object-id"
AZURE_COSMOSDB_ACCOUNT_NAME="db-vector-unique-suffix"
AZURE_COSMOSDB_ENDPOINT="https://db-vector-unique-suffix.documents.azure.com:443/"
AZURE_COSMOSDB_DATABASENAME="Hotels"
AZURE_COSMOSDB_CONTAINER_NAME="hotels_diskann"
AZURE_OPENAI_ENDPOINT="https://your-openai-account.openai.azure.com/"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small"
AZURE_OPENAI_EMBEDDING_API_VERSION="2024-08-01-preview"
VECTOR_INDEX_TYPE="diskANN"
EMBEDDED_FIELD="DescriptionVector"
EMBEDDING_DIMENSIONS="1536"
DATA_FILE_WITH_VECTORS="../data/HotelsData_toCosmosDB_Vector.json"
```

The `VECTOR_INDEX_TYPE` can be either `diskANN` or `quantizedFlat`.

## Review the code

### Orchestrator: index.ts

The main orchestrator imports configuration from `config.ts`, validates environment variables, and coordinates the control plane and data plane operations:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-create-index-typescript/src/index.ts" :::

### Configuration: config.ts

The configuration module loads environment variables and provides a typed `SampleConfig` interface used by all modules:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-create-index-typescript/src/config.ts" :::

### Control plane: Create container with vector index

The control plane uses the Azure Resource Manager SDK (`@azure/arm-cosmosdb`) to create a container with a vector index. The vector index is **immutable** — you must define it at container creation time.

### [DiskANN](#tab/tab-diskann)

DiskANN is optimized for large-scale vector search with high recall and low latency. It uses disk-based indexing for memory efficiency:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-create-index-typescript/src/control-plane.ts" range="1-150" :::

The DiskANN configuration in the vector embedding policy:

```typescript
{
  vectorEmbeddings: [
    {
      path: "/DescriptionVector",
      dataType: "float32",
      dimensions: 1536,
      distanceFunction: "cosine"
    }
  ]
}
```

And the indexing policy:

```typescript
{
  indexingMode: "consistent",
  vectorIndexes: [
    {
      path: "/DescriptionVector",
      type: "diskANN"
    }
  ]
}
```

### [Quantized flat](#tab/tab-quantizedflat)

Quantized flat indexing uses quantization to reduce memory footprint while maintaining good accuracy. It's suitable for smaller datasets or scenarios where memory efficiency is critical:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-create-index-typescript/src/control-plane.ts" range="1-150" :::

The Quantized flat configuration in the vector embedding policy:

```typescript
{
  vectorEmbeddings: [
    {
      path: "/DescriptionVector",
      dataType: "float32",
      dimensions: 1536,
      distanceFunction: "cosine"
    }
  ]
}
```

And the indexing policy:

```typescript
{
  indexingMode: "consistent",
  vectorIndexes: [
    {
      path: "/DescriptionVector",
      type: "quantizedFlat"
    }
  ]
}
```

---

The control plane also creates a custom RBAC role definition for data plane access and assigns it to the current user.

### Data plane: Insert and query documents

The data plane uses the Cosmos DB SDK (`@azure/cosmos`) to insert documents and run queries:

:::code language="typescript" source="~/cosmos-db-vector-samples/nosql-create-index-typescript/src/data-plane.ts" :::

Key operations:
- **Verify dimensions**: Ensure the OpenAI model's embedding dimensions match the container configuration
- **Bulk insert**: Use `executeBulkOperations` to efficiently insert documents with pre-computed embeddings
- **Vector query**: Use the `VectorDistance()` SQL function to find similar documents based on cosine similarity

## Authenticate with Azure CLI

This sample uses `DefaultAzureCredential` with a pinned credential type for predictable authentication:

```typescript
new DefaultAzureCredential()
```

The `.env` file sets `AZURE_TOKEN_CREDENTIALS=AzureCliCredential`, which tells `DefaultAzureCredential` to use only Azure CLI credentials. This approach:
- Ensures consistent authentication across all SDK clients
- Works seamlessly after `az login`
- Avoids credential chain ambiguity in local development

Before running the sample, sign in with Azure CLI:

```bash
az login
```

## Build and run

Install dependencies:

```bash
npm install
```

Run the sample:

### [DiskANN](#tab/tab-diskann)

Ensure your `.env` file has:

```ini
VECTOR_INDEX_TYPE="diskANN"
AZURE_COSMOSDB_CONTAINER_NAME="hotels_diskann"
```

Run the sample:

```bash
npm start
```

### [Quantized flat](#tab/tab-quantizedflat)

Update your `.env` file to:

```ini
VECTOR_INDEX_TYPE="quantizedFlat"
AZURE_COSMOSDB_CONTAINER_NAME="hotels_quantizedflat"
```

Run the sample:

```bash
npm start
```

---

## Expected output

### [DiskANN](#tab/tab-diskann)

```output
======================================================================
Azure Cosmos DB — Create Container with Vector Index via ARM SDK
======================================================================

=== Step 1: Create Container with Vector Index ===
  Container:         hotels_diskann
  Dimensions:        1536
  Distance function: cosine
  Created in 10.4s
  Vector index is IMMUTABLE — cannot be changed after creation

=== Step 2: Create Data-Plane RBAC Access ===
  Creating role definition...
  Role definition created
  Assigning role to current user...
  Role assigned to principal: 419095a2-f637-4729-925a-460252bafc17

  Waiting 15 s for RBAC propagation...

=== Step 3: Verify Embedding Dimensions ===
  Model:    text-embedding-3-small
  Actual:   1536
  Expected: 1536
  Dimensions match

=== Step 4: Insert Documents ===
  Loaded 50 documents (embeddings already included)
  Inserting 50 items using executeBulkOperations...
  Bulk insert completed in 35.63s
  Inserted: 50/50 | Failed: 0 | RU: 6805.25

=== Step 5: Vector Similarity Query ===
  Query:   "hotel near the ocean"
  Latency: 392ms | RU: 5.21 | Results: 3
    1. Oceanfront hotel overlooking the beach... (similarity: 0.5268)
    2. New Luxury Hotel for the vacation... (similarity: 0.5176)
    3. AAA Four Diamond Resort... (similarity: 0.4229)

======================================================================
Complete — container, vector index, and RBAC created
======================================================================
```

### [Quantized flat](#tab/tab-quantizedflat)

```output
======================================================================
Azure Cosmos DB — Create Container with Vector Index via ARM SDK
======================================================================

=== Step 1: Create Container with Vector Index ===
  Container:         hotels_quantizedflat
  Dimensions:        1536
  Distance function: cosine
  Created in 9.8s
  Vector index is IMMUTABLE — cannot be changed after creation

=== Step 2: Create Data-Plane RBAC Access ===
  Creating role definition...
  Role definition created
  Assigning role to current user...
  Role assigned to principal: 419095a2-f637-4729-925a-460252bafc17

  Waiting 15 s for RBAC propagation...

=== Step 3: Verify Embedding Dimensions ===
  Model:    text-embedding-3-small
  Actual:   1536
  Expected: 1536
  Dimensions match

=== Step 4: Insert Documents ===
  Loaded 50 documents (embeddings already included)
  Inserting 50 items using executeBulkOperations...
  Bulk insert completed in 33.21s
  Inserted: 50/50 | Failed: 0 | RU: 6805.25

=== Step 5: Vector Similarity Query ===
  Query:   "hotel near the ocean"
  Latency: 378ms | RU: 5.19 | Results: 3
    1. Oceanfront hotel overlooking the beach... (similarity: 0.5268)
    2. New Luxury Hotel for the vacation... (similarity: 0.5176)
    3. AAA Four Diamond Resort... (similarity: 0.4229)

======================================================================
Complete — container, vector index, and RBAC created
======================================================================
```

---

## Clean up resources

When you're done with the sample, delete the Azure resources to avoid incurring charges:

```bash
chmod +x scripts/delete-resources.sh
./scripts/delete-resources.sh
```

This script deletes the resource group and all resources within it.

## Related content

- [Vector search in Azure Cosmos DB for NoSQL](vector-search.md)
- [Vector indexing overview](vector-indexing.md)
- [VectorDistance system function](query/vectordistance.md)
- [Azure OpenAI Service embeddings](/azure/ai-services/openai/concepts/understand-embeddings)
