---
title: RRF
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function Reciprocal Rank Fusion (RRF)
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 11/04/2024
ms.custom:
  - query-reference
  - ingite-2024
  - build-2025
---

# RRF (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

This system function is used to combine two or more scores provided by other functions.

## Syntax

```nosql
RRF(<function1>, <function2>, ..., <weights>)
```

## Arguments

| | Description |
| --- | --- |
| **`function1`** | A scoring function such as VectorDistance or FullTextScore. |
| **`function2`** | A scoring function such as VectorDistance or FullTextScore. |
| **`weights`** | An array of numbers defining an importance weight for each scoring function. |

## Examples

This is an example of Hybrid Search (vector similarity search + BM25 full text scoring).

```nosql
SELECT TOP 10 *
FROM c
ORDER BY RANK RRF(FullTextScore(c.text, "keyword"), VectorDistance(c.vector, [1,2,3]))
```

This example shows Hybrid Search where the FullTextScore is weighted twice as much as VectorDsitance.

```nosql
SELECT TOP 10 *
FROM c
ORDER BY RANK RRF(FullTextScore(c.text, "keyword"), VectorDistance(c.vector, [1,2,3]), [2,1])
```


This example shows fusion with two `FullTextScore` functions

```nosql
SELECT TOP 10 *
FROM c
ORDER BY RANK RRF(FullTextScore(c.text, "keyword1"), FullTextScore(c.text, "keyword2")
```

This example shows fusion with two `VectorDistance` functions

```nosql
SELECT TOP 5 *
FROM c
ORDER BY RANK RRF(VectorDistance(c.vector1, [1,2,3]),VectorDistance(c.vector2, [2,2,4]))
```

This example shows fusion with two `VectorDistance` functions


## Remarks

- This function requires enrollment in the [Azure Cosmos DB NoSQL Full Text Search feature](../../gen-ai/full-text-search.md).
- Hybrid Search also requires enrollment in [Azure Cosmos DB NoSQL Vector Search](../vector-search.md).
- This function requires a [Full Text Index](../../index-policy.md).
- This function can only be used in an `ORDER BY RANK` clause, and can't be combined with `ORDER BY` on other property paths.
- This function can’t be part of a projection (for example, `SELECT FullTextScore(c.text, "keyword") AS Score FROM c` is invalid.
  

## Related content

- [System functions](system-functions.yml)
- [Setup Full Text Search in Azure Cosmos DB for NoSQL](../../gen-ai/full-text-search.md).
- [Full Text Index](../../index-policy.md)
