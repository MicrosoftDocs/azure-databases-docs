---
title: VectorDistance
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that return the similarity score between two vectors for one or more items in a container.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/22/2024
ms.custom: query-reference, build-2024, ignite-2024
---

# VectorDistance (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the similarity score between two specified vectors.

## Syntax

```nosql
VectorDistance(<vector_expr_1>, <vector_expr_2>, <bool_expr>, <obj_expr>)  
```

## Arguments

| Parameter | Description |
| --- | --- |
| **`vector_expr_1`** | An array of `float32` or smaller. |
| **`vector_expr_2`** | An array of `float32` or smaller. |
| **`bool_expr`** | An optional boolean specifying how the computed value is used in an ORDER BY expression. If `true`, then brute force is used. A value of `false` uses any index defined on the vector property, if it exists. Default value is `false`. |
|**`obj_expr`**| An optional JSON formatted object literal used to specify options for the vector distance calculation. Valid items include `distanceFunction`, `dataType`, and `searchListSizeMultiplier`. |

Supported parameters for the optional `obj_expr`

| Parameter | Description |
| --- | --- | 
| **`distanceFunction`** | The metric used to compute distance/similarity. |
| **`dataType`** | The data type of the vectors. `float32`, `int8`, `uint8` values. Default value is `float32`. |
| **`searchListSizeMultiplier`** | An integer specifying the size of the search list when conducting a vector search on the DiskANN index.  Increasing this may improve accuracy at the expense of RU cost and latency. Min=1, Default=10, Max=100. |
| **`quantizedVectorListMultiplier`** | An integer specifying the size of the search list when conducting a vector search on the quantizedFlat index.  Increasing this may improve accuracy at the expense of RU cost and latency. Min=1, Default=5, Max=100. |



Supported metrics for `distanceFunction` are:

- [`cosine`](https://en.wikipedia.org/wiki/Cosine_similarity), which has values from `-1` (least similar) to `+1` (most similar).  
- [`dotproduct`](https://en.wikipedia.org/wiki/Dot_product), which has values from `-∞` (`-inf`) (least similar) to `+∞` (`+inf`) (most similar).
- [`euclidean`](https://en.wikipedia.org/wiki/Euclidean_distance), which has values from `0` (most similar) to `+∞` (`+inf`) (least similar).

## Return types

Returns a numeric expression that enumerates the similarity score between two expressions.

## Examples

This first example shows a top 10 vector search query with only the required arguments. One property is projected, along with the score returned by `VectorDistance`. Then, we user an `ORDER BY` clause to sort `VectorDistance` scores in order from most similar to least.

```nosql
SELECT TOP 10 c.name, VectorDistance(c.vector1, <query_vector>)
FROM c
ORDER BY VectorDistance(c.vector1, <query_vector>)
```

This next example also includes optional arguments for `VectorDistance`

```nosql
SELECT TOP 10 c.name, VectorDistance(c.vector1, <query_vector>, true, {'distanceFunction':'cosine', 'dataType':'float32'})
FROM c
ORDER BY VectorDistance(c.vector1, <query_vector>, true, {'distanceFunction':'cosine', 'dataType':'float32'})
```

>[!IMPORTANT]
> Always use a `TOP N` clause in the `SELECT` statement of a query. Otherwise the vector search will try to return many more results and the query will cost more RUs and have higher latency than necessary.

## Remarks

- This function requires enabling the [Azure Cosmos DB NoSQL Vector Search feature](../vector-search.md#enable-the-vector-indexing-and-search-feature).
- This function benefits from a [vector index](../../index-policy.md#vector-indexes)
- If `false` is given as the optional `bool_expr`, then the vector index defined on the path is used, if one exists. If no index is defined on the vector path, then this function reverts to full scan and incurs higher RU charges and higher latency than if using a vector index.
- When `VectorDistance` is used in an `ORDER BY` clause, no direction needs to be specified for the `ORDER BY` as the results are always sorted in order of most similar (first) to least similar (last) based on the similarity metric used.
- The result is expressed as a similarity score.

## Related content

- [System functions](system-functions.yml)
- [Setup Azure Cosmos DB for NoSQL for vector search](../vector-search.md).
- [vector index](../../index-policy.md#vector-indexes)
