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

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/now/query.sql" highlight="2-6":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/now/result.json":::

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
