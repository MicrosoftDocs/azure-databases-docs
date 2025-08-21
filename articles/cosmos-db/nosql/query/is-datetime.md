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

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/is-datetime/query.sql" highlight="2-9":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/is-datetime/result.json":::

## Remarks

- A valid DateTime string must begin with four digits for the year (YYYY) followed by a dash "-" e.g. 2023-
- A valid DateTime string must then have a two digit month followed by a dash "-" e.g. 2023-03-
- A valid DateTime string must then have a two digit day e.g. 2023-03-06
- A valid DateTime string may end with the two digit day and be valid without a time
- It may also end after the day of the month with "Z" and still be valid e.g. 2023-03-06Z
- If the DateTime string includes time, the day of the month may either be followed by a space or "T" time designator e.g. 2023-03-06 15:29:00Z or 2023-03-06T15:29:00Z
- Any other character besides space or "T" is invalid
- After the time designator character, there must be a 2 digit hour followed by ":" colon time separator
- Followed by a 2 digit minute portion followed by ":" colon time separator
- Followed by a 2 digit second portion which may conclude a valid DateTime string e.g. 2023-03-06T15:29:59
- The seconds may also be followed by "Z" UTC signifier and be valid e.g. 2023-03-06T15:29:59Z
- If there are fractional seconds, they must be preceded with a "."
- To be valid this "." Fractional seconds designator must be followed with at minimum one digit and maximum of 7 digits e.g. 2023-03-06T15:29:59.9 or 2023-03-06T15:29:59.9Z or 2023-03-06T15:29:59.1234567 or 2023-03-06T15:29:59.1234567Z
- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`IS_STRING`](is-string.md)
- [`IS_NUMBER`](is-number.md)
