---
title: ARRAY_SUM
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the sum value of elements in the specified array expression.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# ARRAY_SUM (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the sum value of elements in the specified array expression.

## Syntax

```nosql
ARRAY_SUM(<array_expr>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`array_expr`** | An array expression. |

## Return types

Returns a numeric expression.

## Examples

The following example shows the results of using this function on arrays with numeric values.

```nosql
SELECT VALUE {
    "case1": ARRAY_SUM([1, 2, 3, 4]),
    "case2": ARRAY_SUM([1, 2, 3, 4, undefined]),
    "case3": ARRAY_SUM(['abc', 'ABC', 'aBc', 'AbC']),
    "case4": ARRAY_SUM([12, 'abc', true, false, null, undefined])
}
```

```json
[
    {
        "case1": 10,
        "case2": 10
    }
]
```

## Remarks

- The elements in array can only be number.
- Any undefined values are ignored.
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`ARRAY_AVG`](array-avg.md)
- [`ARRAY_MAX`](array-max.md)
