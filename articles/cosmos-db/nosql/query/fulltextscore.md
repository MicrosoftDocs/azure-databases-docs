---
title: FullTextScore
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function for full text score using BM25
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 11/04/2024
ms.custom: query-reference, ingite-2024
---

# FullTextScore (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

This function returns a BM25 score value that can only be used in an `ORDER BY RANK` clause to sort results from highest relevancy to lowest relevancy of the specified terms.

## Syntax

```nosql
FullTextScore(<property_path>, <string_expr1>, <string_expr2>, ... )  
```

## Arguments

| | Description |
| --- | --- |
| **`property_path`** | The property path to search. |
| **`string_expr1`** | The first term to find. |
| **`string_expr2`** | The second term to find. |


## Return types

Returns a BM25 scoring that can be used with `ORDER BY RANK` or `RRF`.

## Examples

This is a simple example showing how to use `FullTextScore` with `ORDER BY RANK` to sort from highest relevancy to lowest relevancy.

```nosql
SELECT TOP 10 c.text
FROM c
ORDER BY RANK FullTextScore(c.text, "keyword")
```

This next example shows use of both `FullTextScore` in the `ORDER BY RANK` clause, and `FullTextContains` in the `WHERE` clause.

```nosql
SELECT TOP 10 c.text
FROM c
WHERE FullTextContains(c.text, "keyword1")
ORDER BY RANK FullTextScore(c.text, "keyword1", "keyword2")
```

## Remarks

- This function requires enrollment in the [Azure Cosmos DB NoSQL Full Text Search feature](../../gen-ai/full-text-search.md).
- This function requires a [Full Text Index](../../index-policy.md).
- This function can only be used in an `ORDER BY RANK` clause, or as an argument in an `RRF` system function.
- This function can’t be part of a projection (for example, `SELECT FullTextScore(c.text, "keyword") AS Score FROM c` is invalid.

## Related content

- [System functions](system-functions.yml)
- [Setup Full Text Search in Azure Cosmos DB for NoSQL](../../gen-ai/full-text-search.md).
- [Full Text Index](../../index-policy.md)
