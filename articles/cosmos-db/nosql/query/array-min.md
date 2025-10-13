---
title: ARRAY_MIN
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the minimal value of elements in the specified array expression.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# ARRAY_MIN (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the minimal value of elements in the specified array expression.

## Syntax

```nosql
ARRAY_MIN(<array_expr>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`array_expr`** | An array expression. |

## Return types

Returns a numeric/boolean/string expression.

## Examples

The following example shows the results of using this function on arrays with different data types.

```nosql
SELECT VALUE {
    "case1": ARRAY_MIN([1, 2, 3, 4]),
    "case2": ARRAY_MIN(['abc', 'ABC', 'aBc', 'AbC']),
    "case3": ARRAY_MIN([true, false]),
    "case4": ARRAY_MIN([null, null]),
    "case5": ARRAY_MIN([12, 'abc', true, false, null, undefined])
}
```

```json
[
    {
        "case1": 1,
        "case2": "ABC",
        "case3": false,
        "case4": null,
        "case5": null
    }
]
```

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
- [`ARRAY_MAX`](array-max.md)
- [`ARRAY_AVG`](array-avg.md)
