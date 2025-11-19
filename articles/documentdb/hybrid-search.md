---
title: Hybrid Search in Azure DocumentDB
description: Overview of hybrid search in Azure DocumentDB.
author: khelanmodi
ms.author: khelanmodi
ms.topic: how-to
ms.date: 4/30/2025
ms.custom:
  - build-2025
---

# Hybrid search in Azure DocumentDB

Azure DocumentDB now supports a powerful hybrid search capability that combines vector search with full-text search scoring using the Reciprocal Rank Fusion (RRF) function.

## What is hybrid search?

Hybrid search leverages the strengths of both vector-based and traditional keyword-based search methods to deliver more relevant and accurate search results. This is achieved by combining vector embeddings and text data within the same documents:
- **Vector search**: Utilizes machine learning models to understand the semantic meaning of queries and documents. This allows for more context-aware search results, especially useful for complex queries where traditional keyword search might fall short. For efficient vector similarity search, Azure DocumentDB offers three `cosmosSearch` compatible [vector indices](./vector-search.md#perform-vector-similarity-search): HNSW, IVF, and DiskANN.
- **Full-text search**: Azure DocumentDB uses `$text` operator for full-text search.

The results from vector search and full-text search are then combined to return final search results benefiting from the strengths of both search approaches:
  - **Enhanced Relevance**: By combining semantic understanding with keyword matching, hybrid search can deliver more relevant results for a wide range of queries.
  - **Improved Accuracy**: The RRF function ensures that the most pertinent results from both search methods are prioritized.
  - **Versatility**: Suitable for various use cases including recommendation systems, semantic search, and personalized content discovery.

## How to use hybrid search

1.  Create a collection to store your data, including both text content and vector embeddings.
2.  Create a [vector index](./vector-search.md#perform-vector-similarity-search) on your vector embedding field using the `cosmosSearch` operator.
3.  Create a full-text index on your text field using the standard index creation commands with the `$text` type.
4.  Use the aggregation pipeline with the `$search` operator (for vector search) and the `$text` operator (for full-text search), followed by steps to implement Reciprocal Rank Fusion to combine the scores using the `$unionWith` operator.

## Configure indexes for hybrid search
### Create a vector index

```javascript
db.runCommand({
  "createIndexes": "yourCollectionName",
  "indexes": [
    {
      "key": {
        "vectorField": "cosmosSearch"
      },
      "name": "vectorIndex",
      "cosmosSearchOptions": {
        "kind": "vector-diskann", // "vector-ivf" , "vector-hnsw"
        "similarity": "cosine", //  "l2"
        "dimensions": 3072 // Max 16,000
      }
    }
  ]
});
```

### Create a full-text index

```javascript
db.runCommand({
  "createIndexes": "yourCollectionName",
  "indexes": [
    {
      "key": {
        "textField": "text"
      },
      "name": "fullTextIndex"
    }
  ]
});
```

## Perform hybrid search 

```javascript
db.hybrid_col.aggregate([
  { $search: { cosmosSearch: { path: "vector", vector: [0.1, 0.2, 0.3], k: 5 } } },  // Vector search
  { $group: { _id: null, vectorResults: { $push: "$$ROOT" } } },
  { $unwind: { path: "$vectorResults", includeArrayIndex: "vectorRank" } },
  { $addFields: { vs_score: { $divide: [1, { $add: ["$vectorRank", 1, 1] }] } } },
  { $project: { _id: "$vectorResults._id", title: "$vectorResults.text", vs_score: 1 } },
  { $unionWith: {
    coll: "hybrid_col",
    pipeline: [
      { $match: { $text: { $search: "cat" } } },
      { $addFields: { textScore: { $meta: "textScore" } } },
      { $group: { _id: null, textResults: { $push: "$$ROOT" } } },
      { $unwind: { path: "$textResults", includeArrayIndex: "textRank" } },
      { $addFields: { fts_score: { $divide: [1, { $add: ["$textRank", 10, 1] }] } } },
      { $project: { _id: "$_id", title: "$text", fts_score: 1 } }
    ]
  }},
  { $group: {
    _id: "$title",
    finalScore: { $max: { $add: [{ $ifNull: ["$vs_score", 0] }, { $ifNull: ["$fts_score", 0] }] } }
  }},
  { $sort: { finalScore: -1 } }
])
```

In this example, the first `$search` stage performs a vector similarity search on the vector field for the query vector `[0.1, 0.2, 0.3]`, returning the top five most similar documents (`k: 5`). The `$group` stage then groups all the vector search results into a single document with an array called `vectorResults`. Following this, the `$unwind` stage deconstructs the `vectorResults` array, creating a separate document for each result and adding its rank (`vectorRank`). The subsequent `$addFields` stage calculates the Reciprocal Rank Fusion (RRF) score for each vector search result based on its rank. The `$project` stage then selects the `_id`, `title`, and the calculated `vs_score` from the vector search results.

Moving on to the text search phase, the `$unionWith` stage combines the results of the vector search pipeline with those of a separate full-text search pipeline. In the full-text search phase, the `$match` stage with the `$text` operator performs a full-text search for the term "cat" in the text field. The `$addFields` stage retrieves the relevance score (`textScore`) assigned by the `$text` operator. Similar to the vector search results, the `$group` stage groups all full-text search results, and the `$unwind` stage deconstructs the `textResults` array, adding the rank (`textRank`). A different penalty (10) is used here, which can be tuned. The `$project` stage selects the `_id`, `title`, and `fts_score` from the full-text search results. After combining the results, the `$group` stage groups documents by their `title`.

Finally, the `$project` stage calculates the `finalScore` for each document by taking the maximum of its vector RRF score (`vs_score`) and its full-text RRF score (`fts_score`). `$ifNull` handles cases where a document might only be present in one of the search results.

## Limitations
- Azure DocumentDB's full-text search currently only supports BM25 ranking in gated preview.
- Currently, there is no single, dedicated command to perform a hybrid search directly. You need to construct the hybrid search query using the aggregation pipeline as demonstrated in the examples above.

## Next steps
> [!div class="nextstepaction"]
> [Create a lifetime free-tier cluster for Azure DocumentDB](free-tier.md)
