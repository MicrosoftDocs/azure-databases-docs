---
title: Exact Nearest Neighbor Vector Search for Precise Retrieval
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: ENN Vector Search performs an exhaustive distance calculation across all indexed vectors to guarantee the retrieval of the closest neighbors based on a specified distance metric.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 27/03/2025
appliesto:
  - ✅ MongoDB vCore
---

## Overview

This document outlines the **Exact Nearest Neighbor (ENN) Vector Search** feature, detailing its functionality, appropriate use cases compared to Approximate Nearest Neighbor (ANN) search, and implementation guidelines.


ENN Vector Search performs an exhaustive distance calculation across all indexed vectors to guarantee the retrieval of the closest neighbors based on a specified distance metric.

## What Is Exact Nearest Neighbor (ENN) Vector Search?

ENN Vector Search, activated by setting `"exact": true` in the query, conducts a comprehensive comparison between the query vector and every vector in the dataset. This approach ensures:

- **Guaranteed Accuracy**: Retrieves the true nearest neighbors as per the chosen distance metric (e.g., Euclidean distance, cosine similarity).
- **Increased Computational Load**: Due to the exhaustive nature of the search, it is more resource-intensive and may result in longer query times, especially with large datasets.

In contrast, Approximate Nearest Neighbor (ANN) search, typically set with `"exact": false`, utilizes indexing techniques such as Hierarchical Navigable Small World (HNSW), Inverted File (IVF), or DiskANN to expedite searches. While ANN offers faster response times and better scalability, it may not always return the absolute nearest neighbors.

## When Should You Use ENN Vector Search?

Consider using ENN Vector Search in the following scenarios:

1. **High Accuracy Requirements**: For applications where precise top-k results are critical, such as in sensitive recommendation systems or scientific research, ENN ensures maximum precision.

2. **Manageable Dataset Size**: When dealing with smaller datasets or when performance constraints are less stringent, the exhaustive nature of ENN is feasible.

3. **Low Selectivity Filtering**: If applying filters that result in a relatively small subset of data, ENN can efficiently perform exhaustive comparisons within this subset.

   *Example*: In a large dataset containing millions of documents categorized by tenants, performing a vector search within a specific tenant (comprising a few thousand vectors) can be effectively handled by ENN.

## How to Use ENN Vector Search

Prior to utilizing ENN Vector Search, ensure that a vector index (e.g., IVF, HNSW, DiskANN) is created for the relevant path, similar to the setup for ANN searches. However, note that ENN does not rely on these indexes during query execution.

To enable ENN, set `"exact": true` in your query. For example:

```json
{
  "$search": {
    "cosmosSearch": {
      "path": "myVectorField",
      "exact": true,               ← This enables ENN
      "query": [0.2, 0.4, 0.9],    ← Your input vector
      "k": 10,                     ← Number of results
      "filter": {
        "tenant_id": { "$eq": "tenant123" }
      }
    }
  }
}
```

**Parameters**:

- **`exact` (boolean)**:
  - *Optional* (defaults to `false` if not specified).
  - `false`: Executes an Approximate Nearest Neighbor (ANN) search.
  - `true`: Executes an Exact Nearest Neighbor (ENN) search.

- **`k` (integer)**:
  - Specifies the number of results to return.

- **`filter`**:
  - *Optional*. Defines criteria to narrow down the search scope.

## Combining ENN Vector Search with Filters

ENN Vector Search can be integrated with attribute or geospatial filters to limit the candidate set. After applying the filter, the search engine performs exhaustive distance calculations on the filtered subset, returning the top-k nearest neighbors that meet the filter criteria.

## Use Case Scenario

A client maintains a collection of approximately 300,000 documents, each containing a vector field, a `tenant_id` field (representing thousands of tenants), and other attributes. They observed that ANN vector searches with a `tenant_id` filter were slow.

By switching to ENN Vector Search with the same filter, the query performance improved by a factor of 50, and recall accuracy reached 100%, as ENN provides exact nearest neighbor results.


## Limitation 
- ENN may be slower and more resource-intensive for large datasets without selective filtering due to the necessity of evaluating every vector.
Slower on large datasets (unless heavily filtered).

Higher computational cost — compares to all (or filtered) vectors.

## Summary

- **Exact Nearest Neighbor (ENN) Vector Search** offers 100% accuracy by exhaustively comparing the query vector to all indexed vectors, making it suitable for applications requiring precise results or when dealing with smaller datasets or filtered subsets.

- **Approximate Nearest Neighbor (ANN) Search** utilizes specialized indexing techniques to provide faster responses and better scalability for large datasets, though it may slightly compromise on accuracy.

Choose ENN Vector Search when exact nearest neighbors are essential, or when the dataset size or filtering conditions make the performance overhead acceptable. For larger datasets where speed is prioritized, consider using ANN methods. 

## Related content

- [.NET RAG Pattern retail reference solution](https://github.com/Azure/Vector-Search-AI-Assistant-MongoDBvCore)
- [.NET tutorial - recipe chatbot](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/C%23/CosmosDB-MongoDBvCore)
- [C# RAG pattern - Integrate OpenAI Services with Cosmos](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/C%23/CosmosDB-MongoDBvCore)
- [Python RAG pattern - Azure product chatbot](https://github.com/microsoft/AzureDataRetrievalAugmentedGenerationSamples/tree/main/Python/CosmosDB-MongoDB-vCore)
- [Python notebook tutorial - Vector database integration through LangChain](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db)
- [Python notebook tutorial - LLM Caching integration through LangChain](https://python.langchain.com/docs/integrations/vectorstores/azure_cosmos_db/)
- [Python - LlamaIndex integration](https://docs.llamaindex.ai/en/stable/examples/vector_stores/AzureCosmosDBMongoDBvCoreDemo.html)
- [Python - Semantic Kernel memory integration](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/memory/azure_cosmosdb)

## Next step

> [!div class="nextstepaction"]
> [Create a lifetime free-tier vCore cluster for Azure Cosmos DB for MongoDB](free-tier.md)