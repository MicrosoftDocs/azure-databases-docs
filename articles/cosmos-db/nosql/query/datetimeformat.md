---
title: DATETIMEFORMAT
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function that formats a datetime value based on the specified format string.
author: seesharprun
ms.author: sidandrews
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 08/21/2025
ms.custom: query-reference
---

# DATETIMEFORMAT (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Formats a datetime value based on the specified format string.

## Syntax

```nosql
DATETIMEFORMAT(<date_time>, <string_expr>)  
```  

## Arguments

| | Description |
| --- | --- |
| **`date_time`** | The datetime value to format. |
| **`string_expr`** | The format string includes one or more of the supported format specifiers and other characters. |

## Return types

Returns a string expression.

## Examples

The following example shows different formatting options for datetime values.

:::code language="nosql" source="~/cosmos-db-nosql-query-samples/scripts/datetimeformat/query.sql" highlight="2-5":::

:::code language="json" source="~/cosmos-db-nosql-query-samples/scripts/datetimeformat/result.json":::

## Remarks

- This function performs a full scan.

## Related content

- [System functions](system-functions.yml)
- [`DATETIMEPART`](datetimepart.md)
