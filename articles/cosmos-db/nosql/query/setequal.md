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

```nosql
SELECT VALUE {
    "case1": SETEQUAL([1, 2, 3], [1, 2, 3]),
    "case2": SETEQUAL([1, 2, 3], [3, 2, 1]),
    "case3": SETEQUAL([1, 2, 3, 3], [1, 2, 2, 3, 1, 2]),
    "case4": SETEQUAL([], [1, 2, 3]),
    "case5": SETEQUAL([1, true, 'abc'], [true, 1, 'abc']),
    "case6": SETEQUAL([1, 1, 1, 1], [2, 3, 4])
}
```

```json
[
    {
        "case1": true,
        "case2": true,
        "case3": true,
        "case4": false,
        "case5": true,
        "case6": false
    }
]
```

## Remarks

- This system function will not utilize the index.

## Related content

- [System functions](system-functions.yml)
- [`SETDIFFERENCE`](setdifference.md)
- [`SETINTERSECT`](setintersect.md)
