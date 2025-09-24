---
title: NOW
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a datetime string representing either the current UTC time or the result of adding a specified numeric offset to it.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# NOW (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a datetime string representing either the current UTC time or the result of adding a specified numeric offset to it.

## Syntax

```nosql
NOW(<date_time_part>, <numeric_expr>)
NOW()
```  

## Arguments

| | Description |
| --- | --- |
| **`date_time_part` *(Optional)*** | A string representing a part of an ISO 8601 date format specification. This part is used to indicate which aspect of the date to modify by the related numeric expression. |
| **`numeric_expr` *(Optional)*** | The value to add to the current datetime. |

## Return types

Returns a string expression.

## Examples

The following example shows various uses of the NOW function with and without time modifications.
Assume the current datetime is 2024-10-14T14:20:30.6668888Z.

```nosql
SELECT VALUE {
    "case1": NOW(),
    "case2": NOW("yyyy", 1),
    "case3": NOW("yyyy", -1),
    "case4": NOW("ss", 30),
    "case5": NOW("ms", 4)
}
```

```json
[
    {
        "case1": "2024-10-14T14:20:30.6668888Z",
        "case2": "2025-10-14T14:20:30.6668888Z",
        "case3": "2023-10-14T14:20:30.6668888Z",
        "case4": "2024-10-14T14:21:00.6668888Z",
        "case5": "2024-10-14T14:20:30.6708888Z"
    }
]
```

## Remarks

- This function performs a full scan.
- The ISO 8601 date format specifies valid date and time parts to use with this function:
  - **Year**: year, yyyy, yy
  - **Month**: month, mm, m
  - **Day**: day, dd, d
  - **Hour**: hour, hh
  - **Minute**: minute, mi, n
  - **Second**: second, ss, s
  - **Millisecond**: millisecond, ms
  - **Microsecond**: microsecond, mcs
  - **Nanosecond**: nanosecond, ns

## Related content

- [System functions](system-functions.yml)
- [`AGO`](ago.md)
