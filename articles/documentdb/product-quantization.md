---
title: Product Quantization
description: Learn how to use Product Quantization in Azure DocumentDB for efficient, scalable AI applications.
author: khelanmodi
ms.author: khelanmodi
ms.topic: concept-article
ms.date: 4/30/2025
ms.update-cycle: 180-days
ms.collection:
  - ce-skilling-ai-copilot
ms.custom:
  - build-2025
---

# Product quantization for vector search in Azure DocumentDB

Product quantization (PQ) is a powerful technique in Azure DocumentDB that significantly compresses high-dimensional vector embeddings used in vector search. This compression reduces memory use and speeds up nearest-neighbor searches, improving efficiency for large vector datasets. While PQ offers benefits for speed and scale, it may come at the expense of accuracy.

## Benefits

- **Reduced Storage:** PQ greatly lowers the storage needed for vector indexes compared to full-precision (float32) vectors, leading to substantial cost savings for large datasets.
- **Faster Search:** Working with compressed vectors allows the system to calculate distances and find potential nearest neighbors much quicker than with full-precision vectors.
- **Improved Scalability:** Lower memory overhead enables scaling vector search to handle larger and higher-dimensional embeddings within your cluster.

## How it works

Product quantization divides the high-dimensional vector space into several lower-dimensional subspaces. Each subspace is then quantized independently using a clustering algorithm (typically k-means). The center of each cluster represents all vectors within it. Each original vector is then represented by a short code of the cluster IDs it belongs to in each subspace.

## Using Product quantization

To create a vector index with Product quantization, use the `createIndexes` command with `cosmosSearchOptions` specifying `"compression": "pq"` and `"kind" : "vector-diskann"`:
```json
{
    "createIndexes": "<collection_name>",
    "indexes": [
        {
            "name": "<index_name>",
            "key": {
                "<path_to_property>": "cosmosSearch"
            },
            "cosmosSearchOptions": {
                "kind": "vector-diskann",
                "similarity": "<string_value>", // "COS", "L2"
                "dimensions": <integer_value>, // Max 16,000
                "compression": "pq",
                "pqCompressedDims": <integer_value>, // Dimensions after compression (< original)
                "pqSampleSize": <integer_value>    // Samples for centroid generation
            }
        }
    ]
}
```

| Field              | Type    | Description                                                                |
|--------------------|---------|----------------------------------------------------------------------------|
| `compression`      | string  | Set to `"pq"` to enable Product quantization.                              |
| `pqCompressedDims` | integer | Dimensions after PQ compression (must be less than original dimensions). Automatically calculated if omitted. Range: 1-8000.                         |
| `pqSampleSize`     | integer | Number of sample vectors for PQ centroid training. Higher value means better quality but longer build time. Default: 1000. Range: 1000-100000. | 

> [!NOTE]
> Product quantization is currently supported only with the `vector-diskann` index type.

> [!NOTE]
> For best results, create a PQ index after your collection has data. If the collection is empty, the system uses random vectors for initial centroids. If the number of documents is less than `pqSampleSize`, the training data is padded with random data within the range of your existing vector data.

### How compressed dimensions are set

If you don't specify `pqCompressedDims`, it automatically determines based on the original vector `dimensions`:

| Original Dimension Range | `pqCompressedDims` |
|-----------------------|-----------------|
| [0 - 32)               | dimensions / 2     |
| [32 - 64)              | 16                 |
| [64 - 128)             | 32                 |
| [128 - 512)            | 64                 |
| [512 - 1536)           | 96                 |
| above 1536             | 128                |

### Create a PQ index 
```json
db.runCommand(
{
    "createIndexes": "your_vector_collection",
    "indexes": [
        {
            "key": { "v": "cosmosSearch" },
            "name": "diskann_pq_index",
            "cosmosSearchOptions": {
                "kind": "vector-diskann",
                "similarity": "COS",
                "dimensions": 1536,
                "compression": "pq",
                "pqCompressedDims": 96,
                "pqSampleSize": 2000
            }
        }
    ]
} )
```

## Improving search with Oversampling
PQ compression can lead to precision loss in distance calculations. To reduce this, Azure DocumentDB offers the `oversampling` parameter in the `$search` operator.

The `oversampling` factor (a float with a minimum of 1) specifies how many more candidate vectors to retrieve from the compressed index than `k` (the number of desired results). These extra candidates are used to refine the search using the original, full-precision vectors, improving the final top `k` accuracy. For instance, to get the top 10 (`k`=10) most similar vectors, a good **best practice** might be to set `oversampling` to a value like **1.5** or **2.0**. With `"oversampling": 1.5`, the system would first get 15 candidates from the index and then refine the top 10 using the full-precision data.

```json
{
    "$search": {
        "cosmosSearch": {
            "vector": <vector_to_search>,
            "path": "<path_to_property>",
            "k": <num_results_to_return>,
            "oversampling": <float_value> 
        },
    }
}
```

This code snippet demonstrates a vector search using the `$search` operator with Product quantization. It takes a `queryVector` as input and searches the `v` field. The query requests the top 10 most similar documents (`k: 10`), using an `oversampling` factor of 2.0, which retrieves 20 candidates improving the accuracy of the search over the compressed index.

```json
db.your_vector_collection.aggregate([
    {
        $search: {
            "cosmosSearch": {
                "vector": [0.1, 0.5, 0.9, ...],
                "path": "v",
                "k": 10,
                "oversampling": 2.0 // Retrieve 2 * 10 = 20 candidates for reranking
            },
            "returnStoredSource": true
        }
    }
])
```

## Half-Precision vs. Product quantization

Both [Half-Precision](./half-precision.md) and Product quantization (PQ) compress vector indexes in Azure DocumentDB, but they differ in how they achieve compression and affect search:

| Feature                 | Half-Precision                                   | Product quantization (PQ)                                      |
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

## Considerations for Product quantization
- **Precision vs. Compression:** Higher PQ compression leads to smaller indexes and faster search but greater precision loss. Experiment with `pqCompressedDims` and `oversampling` to find the right balance.
- **Index Build Time:** PQ index creation can take longer due to the centroid training process, influenced by `pqSampleSize`.
- **Data Distribution:** PQ works best when vector data has a clear cluster structure.

## Next steps
> [!div class="nextstepaction"]
> [Create a lifetime free-tier cluster for Azure DocumentDB](free-tier.md)
