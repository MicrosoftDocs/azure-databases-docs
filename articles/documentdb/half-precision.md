---
title: Half-Precision Vector Support
description: Learn how to use half-precision vectors in Azure DocumentDB for more efficient and scalable AI applications.
author: khelanmodi
ms.author: khelanmodi
ms.topic: concept-article
ms.date: 4/24/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - build-2025
---

# Half-Precision vector indexing in Azure DocumentDB

## What is Half-Precision vector indexing?

Half-precision vector indexing allows you to store and index vector embeddings using 16-bit floating-point numbers instead of the standard 32-bit floats. This optimization leads to substantial reductions in both memory usage and storage costs, making it more feasible to work with larger datasets and higher-dimensional vectors. Furthermore, by optimizing data density, it can contribute to improved query performance in many vector search scenarios.

## Key Benefits

- **Increased Dimensionality Support:** With half-precision, you can now index vectors with up to **4,000 dimensions** (an increase from the previous limit of 2,000). 
- **Reduced Storage Footprint:** Storing vectors in a 16-bit format significantly decreases the amount of storage required compared to full-precision vectors. This can lead to considerable cost savings, especially for large-scale vector databases.
- **Configurable Performance vs. Precision:** To fine-tune your search results, we provide an **oversampling** parameter during query execution. This allows you to control the trade-off between retrieval speed and the potential impact of reduced precision.

## Creating a Half-Precision vector index

When defining a [vector index](./vector-search.md#perform-vector-similarity-search) for your collection, you can enable half-precision compression by specifying the `"compression": "half"` option within the `cosmosSearchOptions`.

```javascript
db.runCommand({
  "createIndexes": "<vector_collection_name>",
  "indexes": [
    {
      "key": { "<vector_field_name>": "cosmosSearch" },
      "name": "<index_name>",
      "cosmosSearchOptions": {
        "kind": "vector-hnsw", // or vector-ivf
        "similarity": "cos",
        "dimensions": integer_value, // max 4000
        "compression": "half"
      }
    }
  ]
});
```

## Improving search with Oversampling

When querying a vector index that utilizes half-precision compression, you can use the `oversampling` parameter within the `$search` aggregation stage. This parameter helps to mitigate any potential loss of precision introduced by the 16-bit representation.

The `oversampling` factor, allows you to retrieve more potential nearest neighbors from the half-precision index than the final number of results you want (`k`). These candidates are then compared using the original full-precision vectors to ensure higher accuracy in the final ranked results. 

For instance, to get the top 10 (`k`=10) most similar vectors, a good **best practice** might be to set `oversampling` to a value like **1.5** or **2.0**. With `"oversampling": 1.5`, the system would first get 15 candidates from the half-precision index and then refine the top 10 using the full-precision data.

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

## Half-Precision vs. Product Quantization

Both Half-Precision and [Product Quantization (PQ)](./product-quantization.md) compress vector indexes in Azure DocumentDB, but they differ in how they achieve compression and affect search:

| Feature                 | Half-Precision                                   | Product Quantization (PQ)                                      |
|-------------------------|---------------------------------------------------|-----------------------------------------------------------------|
| **Compression Method** | Reduces each vector dimension to 16 bits.         | Divides vector space into subspaces and quantizes each.          |
| **Max Dimensions** | Up to 4,000                                      | Up to 16,000                                                   |
| **Precision Change** | Slight loss due to lower bit depth.               | Potentially larger loss, configurable via `pqCompressedDims`.    |
| **Search Speed** | Moderate speed increase due to smaller index.     | Significant speed increase due to highly compressed vectors.   |
| **Index Build Time** | Relatively fast.                                | Can be longer due to centroid training (`pqSampleSize`).          |
| **Index Support** | HNSW, IVF.                                      | DiskANN.                                                      |
| **Configuration** | Simple, enable `compression: "half"`.            | More parameters: `pqCompressedDims`, `pqSampleSize`.          |
| **Oversampling Use** | Helps with minor precision loss.                  | Essential for recovering accuracy from larger compression.       |
| **Ideal Use Cases** | Moderate memory reduction, increased dimensions, acceptable precision trade-off. | Large datasets, high dimensions, fast search prioritized, precision managed with oversampling. |

## Next step

> [!div class="nextstepaction"]
> [Use lifetime free tier of Integrated Vector Database in Azure DocumentDB](free-tier.md)
