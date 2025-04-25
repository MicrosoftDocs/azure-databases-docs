---
title: Half-Precision Vector Support
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Learn how to use half-precision vectors in Azure Cosmos DB for MongoDB vCore for more efficient and scalable AI applications.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: concept-article
ms.date: 4/24/2025
ms.collection:
  - ce-skilling-ai-copilot
appliesto:
  - ✅ MongoDB vCore
---

# Half-Precision Vector Indexing in Azure Cosmos DB for MongoDB (vCore)

## What is Half-Precision Vector Indexing?

Half-precision vector indexing allows you to store and index vector embeddings using 16-bit floating-point numbers instead of the standard 32-bit floats. This optimization leads to substantial reductions in both memory usage and storage costs, making it more feasible to work with larger datasets and higher-dimensional vectors. Furthermore, by optimizing data density, it can contribute to improved query performance in many vector search scenarios.

## Key Benefits

- **Increased Dimensionality Support:** With half-precision, you can now index vectors with up to **4,000 dimensions**. 
- **Reduced Storage Footprint:** Storing vectors in a 16-bit format significantly decreases the amount of storage required compared to full-precision vectors. This can lead to considerable cost savings, especially for large-scale vector databases.
- **Configurable Performance vs. Precision:** To fine-tune your search results, we provide an **oversampling** parameter during query execution. This allows you to control the trade-off between retrieval speed and the potential impact of reduced precision.

## Creating a Half-Precision Vector Index

When defining a [vector index](./vector-search.md#perform-a-vector-search) for your collection, you can enable half-precision compression by specifying the `"compression": "half"` option within the `cosmosSearchOptions`.

```javascript
db.runCommand({
  "createIndexes": "<vector_collection_name>",
  "indexes": [
    {
      "key": { "<vector_field_name>": "cosmosSearch" },
      "name": "<index_name>",
      "cosmosSearchOptions": {
        "kind": "vector-hnsw",
        "similarity": "cos",
        "dimensions": integer_value, // max 4000
        "compression": "half"
      }
    }
  ]
});
```

## Improving Search with Oversampling

When querying a vector index that utilizes half-precision compression, you can use the `oversampling` parameter within the `$search` aggregation stage. This parameter helps to mitigate any potential loss of precision introduced by the 16-bit representation.

The `oversampling` factor, allows you to retrieve more potential nearest neighbors from the half-precision index than the final number of results you want (`k`). These candidates are then compared using the original full-precision vectors to ensure higher accuracy in the final ranked results. 

For instance, if you set `k` to 10 and `oversampling` to 1.5, the system will fetch 15 candidate vectors from the half-precision index and then rank the top 10 based on their full-precision values.

```javascript
db.collection.aggregate([
  {
    "$search": {
      "cosmosSearch": {
        "vector": query_vector,
        "path": path_to_property,
        "k":  num_results_to_return,
        "oversampling": double_value
      }
    }
  },
  {
    "$project": {
      "similarityScore": { "$meta": "searchScore" },
      "_id": 0
    }
  }
]);
```

> [!NOTE]
> The `oversampling` factor must be a **double** with a minimum value of `1.0`. This factor is only relevant for vector indexes created with `"compression": "half"`.
## Next step

> [!div class="nextstepaction"]
> [Use lifetime free tier of Integrated Vector Database in Azure Cosmos DB for MongoDB](free-tier.md)
