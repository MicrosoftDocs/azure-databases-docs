---
title: Exact Nearest Neighbor Vector Search for Precise Retrieval
description: ENN Vector Search performs an exhaustive distance calculation across all indexed vectors to guarantee retrieval of the closest neighbors based on a specified distance metric.
author: khelanmodi
ms.author: khelanmodi
ms.topic: concept-article
ms.date: 03/27/2025
---

# Exact Nearest Neighbor (ENN) Vector search for precise retrieval

Exact Nearest Neighbor (ENN) Vector Search performs an exhaustive distance calculation across all indexed vectors to guarantee the retrieval of the closest neighbors based on a specified distance metric.​ ENN is supported on all cluster tiers at no additional cost and requires no registration.

## What Is Exact Nearest Neighbor (ENN) Vector Search?

ENN Vector Search conducts a comprehensive comparison between the query vector and every vector in the dataset. This approach ensures:​
- **Guaranteed Accuracy**: Retrieves the true nearest neighbors as per the chosen distance metric (e.g., Euclidean distance, cosine similarity).​
- **Increased Computational Load**: Due to its exhaustive nature, ENN is more resource-intensive and may result in longer query times, especially with large datasets.​

Conversely, Approximate Nearest Neighbor (ANN) search uses [indexing](./vector-search.md) techniques such as Hierarchical Navigable Small World (HNSW), Inverted File (IVF), or DiskANN to expedite searches. While ANN offers faster response times and better scalability, it may not always return the absolute nearest neighbors.​

## When Should You Use ENN Vector Search?

Consider using ENN Vector Search in the following scenarios:
- **High Accuracy Requirements**: ​For applications where precise top-k results are critical—such as sensitive recommendation systems or scientific research—ENN ensures maximum accuracy.​
- **Manageable Dataset Size**: When dealing with smaller datasets or when performance constraints are less stringent, the exhaustive nature of ENN is feasible.​
- **Low Selectivity Filtering**: If applying filters that result in a relatively small subset of data, ENN can efficiently perform exhaustive comparisons within this subset.​

**For example**: In a large dataset containing millions of documents categorized by tenants, performing a vector search within a specific tenant (comprising a few thousand vectors) can be effectively handled by ENN.​

## How to Use ENN Vector Search

Before using ENN Vector Search, ensure that a [vector index](./vector-search.md) (e.g., IVF, HNSW, DiskANN) is created for the relevant path. If a vector index already exists, there's no need to rebuild it when switching between search methods, since ENN operates independently of these indexes during query execution.​

To enable ENN, set `"exact": true` in your query. For example:

```javascript
{
  "$search": {
    "cosmosSearch": {
      "path": "myVectorField",
      "exact": true,               // Enables ENN
      "query": [0.2, 0.4, 0.9],    // Query vector
      "k": 10,                     // Number of results to return
      "filter": {
        "tenant_id": { "$eq": "tenant123" }
      }
    }
  }
}
```

## Combining ENN Vector Search with Filters

ENN Vector Search can be combined with attribute or geospatial filters to narrow the scope of the search to a specific subset of data. After applying the filter, the search engine performs exhaustive distance calculations on the filtered subset, returning the top-k nearest neighbors that meet the filter criteria.​

### Use Case Scenario

A client maintains a collection of approximately 300,000 documents, each containing a vector field, a `tenant_id` field (representing thousands of tenants), and other attributes. They observed that ANN vector searches with a `tenant_id` filter were slow.​

By switching to ENN Vector Search while maintaining the same filter, the client achieved a **50% improvement in query performance** and attained **100% recall accuracy**.​

## FAQs 
### How Does ENN Perform at Scale?
- **Performance on Large Datasets**: ENN may be slower for large datasets without selective filtering due to the necessity of evaluating every vector.​
- **Higher Computational Cost**: ENN involves comparing the query vector to all (or filtered) vectors, leading to increased resource usage for a large dataset.

### ANN vs ENN: What’s the Difference?

- **Exact Nearest Neighbor (ENN) Vector Search** offers 100% accuracy by exhaustively comparing the query vector to all indexed vectors, making it suitable for applications requiring precise results or when dealing with smaller datasets or filtered subsets.
- **Approximate Nearest Neighbor (ANN) Search** utilizes specialized indexing techniques to provide faster responses and better scalability for large datasets, though it may slightly compromise on accuracy.

## Next step

> [!div class="nextstepaction"]
> [Create a lifetime free-tier cluster for Azure DocumentDB](free-tier.md)
