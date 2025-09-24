---
title: LASTINDEXOF
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the starting position of the last occurrence of the second string expression within the first specified string expression, or -1 if the string isn't found.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# LASTINDEXOF (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the starting position of the last occurrence of the second string expression within the first specified string expression, or -1 if the string isn't found.

## Syntax

```nosql
LASTINDEXOF(<string_expr1>, <string_expr2> [, <numeric_expr>])  
```  

## Arguments

| | Description |
| --- | --- |
| **`string_expr1`** | A string expression to be searched. |
| **`string_expr2`** | A string expression to search for. |
| **`numeric_expr` *(Optional)*** | Optional numeric expression that sets the position the search starts. The search proceeds from position toward the beginning of this instance. The first position in `string_expr1` is 0. |

## Return types

Returns a numeric expression.

## Examples

The following example shows the results of using this function to find the last occurrence of substrings.

```nosql
SELECT VALUE {
    "case1": LASTINDEXOF("abcdeabc", "abc"),
    "case2": LASTINDEXOF("abcdeabc", "abc", 6),
    "case3": LASTINDEXOF("abcdeabc", "abc", 7),
    "case4": LASTINDEXOF("abcdeabc", "fg")
}
```

```json
[
    {
        "case1": 5,
        "case2": 0,
        "case3": 5,
        "case4": -1
    }
]
```

## Remarks

- This system function will not utilize the index.

## Related content

- [System functions](system-functions.yml)
- [`INDEX_OF`](index-of.md)
- [`CONTAINS`](contains.md)
