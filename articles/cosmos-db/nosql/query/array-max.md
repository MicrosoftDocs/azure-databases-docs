---
title: ARRAY_MAX
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the maximal value of elements in the specified array expression.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# ARRAY_MAX (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the maximal value of elements in the specified array expression.

## Syntax

```nosql
ARRAY_MAX(<array_expr>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`array_expr`** | An array expression. |

## Return types

Returns a numeric/boolean/string expression.

## Examples

The following example shows the results of using this function on arrays with different data types.

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/array-max/query.sql" highlight="2-6":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/array-max/result.json":::

## Remarks

- The elements in array can be number, string, boolean, or null.
- Any undefined values are ignored.
- The following priority order is used (in descending order), when comparing different types of data:
  - string
  - number
  - boolean
  - null
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`ARRAY_MIN`](array-min.md)
- [`ARRAY_AVG`](array-avg.md)
