---
title: CONTAINS_ANY_CS
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a boolean value indicating if the source string contains any strings from a list through case-sensitive search.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# CONTAINS_ANY_CS (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a boolean value indicating if the source string contains any strings from a list through case-sensitive search.

## Syntax

```nosql
CONTAINS_ANY_CS(<string_expr>, <expr1>, ... [,<exprN>])  
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

The following example shows various uses of the CONTAINS_ANY_CS function with case-sensitive matching.

```nosql
SELECT VALUE {
    "case1": CONTAINS_ANY_CS("Have a nice day!", "have", "nice", "day!"),
    "case2": CONTAINS_ANY_CS("Have a nice day!", "HAVE", "NICE", "DAY!"),
    "case3": CONTAINS_ANY_CS("Have a nice day!", "had", "nice", "day!"),
    "case4": CONTAINS_ANY_CS("Have a nice day!", undefined, "nice", "day!"),
    "case5": CONTAINS_ANY_CS("Have a nice day!", undefined, "had")
}
```

```json
[
    {
        "case1": true,
        "case2": false,
        "case3": true,
        "case4": true,
        "case5": undefined
    }
]
```

## Remarks

- This function is equivalent to `CONTAINS(<string_expr>, expr1, false) OR ... OR CONTAINS(<string_expr>, exprN, false)`.
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`CONTAINS_ANY_CI`](contains-any-ci.md)
- [`CONTAINS`](contains.md)
