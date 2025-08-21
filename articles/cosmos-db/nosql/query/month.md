---
title: MONTH
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that returns the value of the month for the provided date and time.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# MONTH (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns the value of the month for the provided date and time.

## Syntax

```nosql
MONTH(<date_time>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`date_time`** | A date/time value. |

## Return types

Returns a numeric value that is a positive integer.

## Examples

The following example shows the results of using this function on different date values.

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/month/query.sql" highlight="2-4":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/month/result.json":::

## Remarks

- This function behaves the same as the DateTimePart function when the month is specified.
- This function benefits from the use of a [range index](../../index-policy.md#includeexclude-strategy).

## Related content

- [System functions](system-functions.yml)
- [`YEAR`](year.md)
- [`DAY`](day.md)
- [`DATETIMEPART`](datetimepart.md)
