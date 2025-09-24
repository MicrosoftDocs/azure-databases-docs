---
title: SETDIFFERENCE
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a set containing only the elements from the first input set that aren't in the second input set with no duplicates.
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

Returns a set containing only the elements from the first input set that aren't in the second input set with no duplicates.

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

```nosql
SELECT VALUE {
    "case1": SETDIFFERENCE([1, 2, 3], [1, 2, 6, 7]),
    "case2": SETDIFFERENCE([1, 2, 6, 7], [1, 2, 3]),
    "case3": SETDIFFERENCE([1, 2, 3, 4], [1, 2, 3, 4, 5, 6]),
    "case4": SETDIFFERENCE([], [1, 2, 3]),
    "case5": SETDIFFERENCE([1, 2, 3], []),
    "case6": SETDIFFERENCE([1, 1, 1, 1], [2, 3, 4])
}
```

```json
[
    {
        "case1": [3],
        "case2": [6, 7],
        "case3": [],
        "case4": [],
        "case5": [1, 2, 3],
        "case6": [1]
    }
]
```

## Remarks

- This system function won't utilize the index.

## Related content

- [System functions](system-functions.yml)
- [`SETINTERSECT`](setintersect.md)
- [`SETUNION`](setunion.md)
