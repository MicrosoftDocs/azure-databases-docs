---
title: SETDIFFERENCE
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a set containing only the elements from the first input set that are not in the second input set with no duplicates.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# SETDIFFERENCE (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a set containing only the elements from the first input set that are not in the second input set with no duplicates.

## Syntax

```nosql
SETDIFFERENCE(<arr_expr1>, <arr_expr2>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`arr_expr1`** | The first array expression. |
| **`arr_expr2`** | The second array expression. |

## Return types

Returns an array expression.

## Examples

The following example shows the results of using this function to find set differences between arrays.

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/setdifference/query.sql" highlight="2-7":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/setdifference/result.json":::

## Remarks

- This system function will not utilize the index.

## Related content

- [System functions](system-functions.yml)
- [`SETINTERSECT`](setintersect.md)
- [`SETUNION`](setunion.md)
