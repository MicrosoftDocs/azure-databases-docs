---
title: ARRAY_AVG
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the average value of elements in the specified array expression.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# ARRAY_AVG (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the average value of elements in the specified array expression.

## Syntax

```nosql
ARRAY_AVG(<array_expr>)  
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
    "case1": ARRAY_AVG([1, 2, 3, 4]),
    "case2": ARRAY_AVG([1.0, 2.0, 3.3, 4.7]),
    "case3": ARRAY_AVG([1, -2.7, 3, -4, undefined]),
    "case4": ARRAY_AVG(['abc', 'ABC', 'aBc', 'AbC']),
    "case5": ARRAY_AVG([12, 'abc', true, false, null, undefined])
}
```

```json
[
    {
        "case1": 2.5,
        "case2": 2.75,
        "case3": -0.675
    }
]
```

## Remarks

- The elements in array can only be number.
- Any undefined values are ignored.
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`ARRAY_SUM`](array-sum.md)
- [`ARRAY_MEDIAN`](array-median.md)
