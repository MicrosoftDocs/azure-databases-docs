---
title: ARRAY_MEDIAN
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the median value of elements in the specified array expression.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# ARRAY_MEDIAN (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the median value of elements in the specified array expression.

## Syntax

```nosql
ARRAY_MEDIAN(<array_expr>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`array_expr`** | An array expression. |

## Return types

Returns a numeric expression.

## Examples

The following example shows the results of using this function on arrays with numeric values.

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/array-median/query.sql" highlight="2-6":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/array-median/result.json":::

## Remarks

- The elements in array can only be number.
- Any undefined values are ignored.
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`ARRAY_AVG`](array-avg.md)
- [`ARRAY_MAX`](array-max.md)
