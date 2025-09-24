---
title: CONTAINS_ALL_CI
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a boolean value indicating if the source string contains all strings from a list through case-insensitive search.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# CONTAINS_ALL_CI (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a boolean value indicating if the source string contains all strings from a list through case-insensitive search.

## Syntax

```nosql
CONTAINS_ALL_CI(<string_expr>, <expr1>, ... [,<exprN>])  
```  

## Arguments

| | Description |
| --- | --- |
| **`string_expr`** | The string expression to search in. |
| **`expr1`** | The first string expression to search for. |
| **`exprN` *(Optional)*** | Additional string expressions to search for. |

## Return types

Returns a Boolean expression.

## Examples

The following example shows various uses of the CONTAINS_ALL_CI function with case-insensitive matching.

```nosql
SELECT VALUE {
    "case1": CONTAINS_ALL_CI("Have a nice day!", "have", "nice", "day!"),
    "case2": CONTAINS_ALL_CI("Have a nice day!", "HAVE", "NICE", "DAY!"),
    "case3": CONTAINS_ALL_CI("Have a nice day!", "had", "nice", "day!"),
    "case4": CONTAINS_ALL_CI("Have a nice day!", undefined, "nice", "day!"),
    "case5": CONTAINS_ALL_CI("Have a nice day!", undefined, "had")
}
```

```json
[
    {
        "case1": true,
        "case2": true,
        "case3": false,
        "case4": undefined,
        "case5": false
    }
]
```

## Remarks

- This function is equivalent to `CONTAINS(<string_expr>, expr1, true) AND ... AND CONTAINS(<string_expr>, exprN, true)`.
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`CONTAINS_ALL_CS`](contains-all-cs.md)
- [`CONTAINS`](contains.md)
