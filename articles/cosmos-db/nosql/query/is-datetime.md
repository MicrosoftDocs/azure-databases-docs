---
title: IS_DATETIME
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns a boolean value indicating if the datetime string is valid.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# IS_DATETIME (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a boolean value indicating if the datetime string is valid.

## Syntax

```nosql
IS_DATETIME(<expr>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`expr`** | An expression to evaluate. |

## Return types

Returns a Boolean expression.

## Examples

The following example shows various uses of the IS_DATETIME function with different datetime formats.

```nosql
SELECT VALUE {
    "case1": IS_DATETIME("2024-12-12"),
    "case2": IS_DATETIME("2024-12-12Z"),
    "case3": IS_DATETIME("2024-12-12 20:21:25"),
    "case4": IS_DATETIME("2024-12-12T20:21:25Z"),
    "case5": IS_DATETIME("2024-12-12T20:21:25.123"),
    "case6": IS_DATETIME("2024-12-12 20:21:25.123Z"),
    "case7": IS_DATETIME("2024-12-12T20Z"),
    "case8": IS_DATETIME("2024-12-12 20:21:25.")
}
```

```json
[
    {
        "case1": true,
        "case2": true,
        "case3": true,
        "case4": true,
        "case5": true,
        "case6": true,
        "case7": false,
        "case8": false
    }
]
```

## Remarks

- A valid DateTime string must begin with four digits for the year (YYYY) followed by a dash `-` for example, 2023-
- A valid DateTime string must then have a two digit month followed by a dash `-` for example, 2023-03-
- A valid DateTime string must then have a two digit day, for example, 2023-03-06
- A valid DateTime string can end with the two digit day and be valid without a time
- It can also end after the day of the month with "Z" and still be valid, for example, 2023-03-06Z
- If the DateTime string includes time, the day of the month can include a space or "T" time designator for example, 2023-03-06 15:29:00Z or 2023-03-06T15:29:00Z
- Any other character besides space or "T" is invalid
- After the time designator character, there must be a two digit hour followed by `:` colon time separator, followed by a two digit minute portion followed by `:` colon time separator, followed by a two digit second portion, which can conclude a valid DateTime string, for example, 2023-03-06T15:29:59
- The seconds can also be followed by "Z" (UTC) and be valid, for example, 2023-03-06T15:29:59Z
- If there are fractional seconds, they must be preceded with a `.`
- To be valid this `.` Fractional seconds designator must be followed with at minimum one digit and maximum of seven digits, for example, 2023-03-06T15:29:59.9 or 2023-03-06T15:29:59.9Z or 2023-03-06T15:29:59.1234567 or 2023-03-06T15:29:59.1234567Z
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`IS_STRING`](is-string.md)
- [`IS_NUMBER`](is-number.md)
