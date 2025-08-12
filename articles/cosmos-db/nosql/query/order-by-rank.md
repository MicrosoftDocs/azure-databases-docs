---
title: ORDER BY RANK
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL clause that specifies a sort order by ranking of scoring functions.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/22/2024
ms.custom: query-reference
---

# ORDER BY RANK (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

The optional ``ORDER BY RANK`` clause sorts scoring functions by their rank. It's used specifically for scoring functions like `VectorDistance`, `FullTextScore`, and `RRF`.

## Syntax

```nosql
ORDER BY RANK <scoring function>
```  

## Arguments

| | Description |
| --- | --- |
| **``<scoring function>``** | Specifies a scoring function like `VectorDistance`, `FullTextScore`, or RRF. |

> [!NOTE]
> For more information on scalar expressions, see [scalar expressions](scalar-expressions.md).

## Examples

This is a simple example showing how to use `FullTextScore` with `ORDER BY RANK` to sort from highest relevancy to lowest relevancy.

```nosql
SELECT TOP 10 c.text
FROM c
ORDER BY RANK FullTextScore(c.text, "keyword")
```

This next example shows use `RRF` in the `ORDER BY RANK` clause to combine `VectorDistance` similarity scores with `FullTextScore` BM25 scores to execute a hybrid search

```nosql
SELECT TOP 10 c.text
FROM c
WHERE FullTextContains(c.text, "keyword1")
ORDER BY RANK RRF(FullTextScore(c.text, "keyword1", "keyword2"), VectorDistance(c.vector, [1,2,3]))
```

## Remarks  

- This function requires enrollment in the [Azure Cosmos DB NoSQL Full Text Search preview feature](../../gen-ai/full-text-search.md)
- This function requires a [Full Text Index](../../index-policy.md)
- Hybrid Search also requires enrollment in [Azure Cosmos DB NoSQL Vector Search](../vector-search.md)

## Related content
- [``RRF`` system function](rrf.md)
- [``FullTextScore`` system function](fulltextscore.md)
- [``VectorDistance`` system function](vectordistance.md)
- [``OFFSET LIMIT`` clause](offset-limit.md)
