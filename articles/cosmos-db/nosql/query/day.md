---
title: DAY
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the value of the day for the provided date and time.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# DAY (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the value of the day for the provided date and time.

## Syntax

```nosql
DAY(<date_time>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`date_time`** | A date/time value. |

## Return types

Returns a numeric value that is a positive integer.

## Examples

The following example shows the results of using this function on different date values.

```nosql
SELECT VALUE {
    "case1": DAY("2024-01-10"),
    "case2": DAY("2000-12-12T10:00:00"),
    "case3": DAY("1989-03-03T12:12:12.1234567Z")
}
```

```json
[
    {
        "case1": 10,
        "case2": 12,
        "case3": 3
    }
]
```

## Remarks

- This function behaves the same as the DateTimePart function when the day is specified.
- This function benefits from the use of a [range index](../../index-policy.md#includeexclude-strategy).

## Related content

- [System functions](system-functions.yml)
- [`YEAR`](year.md)
- [`MONTH`](month.md)
- [`DATETIMEPART`](datetimepart.md)
