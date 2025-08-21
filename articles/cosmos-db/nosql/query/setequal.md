---
title: SETEQUAL
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a boolean value indicating whether two sets are equal after removing duplicated elements.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# SETEQUAL (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a boolean value indicating whether two sets are equal after removing duplicated elements.

## Syntax

```nosql
SETEQUAL(<arr_expr1>, <arr_expr2>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`arr_expr1`** | The first array expression. |
| **`arr_expr2`** | The second array expression. |

## Return types

Returns a boolean expression.

## Examples

The following example shows the results of using this function to compare sets for equality.

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/setequal/query.sql" highlight="2-7":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/setequal/result.json":::

## Remarks

- This system function will not utilize the index.

## Related content

- [System functions](system-functions.yml)
- [`SETDIFFERENCE`](setdifference.md)
- [`SETINTERSECT`](setintersect.md)
