---
title: FullTextContains
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function for full text search in a specific property path.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 11/04/2024
ms.custom: query-reference, ingite-2024
---

# FullTextContains (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a boolean indicating whether the keyword string expression is contained in a specified property path.

## Syntax

```nosql
FullTextContains(<property_path>, <string_expr>)  
```

## Arguments

| | Description |
| --- | --- |
| **`property_path`** | The property path to search. |
| **`string_expr`** | The string to find. |

## Return types

Returns a boolean expression.  

## Examples

This is a simple query returning 10 results that contain "search phrase" in the `c.text` property. 

```nosql
SELECT TOP 10 *
FROM c
WHERE FullTextContains(c.text, "search phrase")
```

This next example shows logical operators used for ensuring multiple keywords or phrases are included. 

```nosql
SELECT *
FROM c
WHERE FullTextContains(c.text, "keyword1") AND  FullTextContains(c.text, "keyword2")
```

## Remarks

- This function requires enrollment in the [Azure Cosmos DB NoSQL Full Text Search feature](../../gen-ai/full-text-search.md)
- This function benefits from a [Full Text Index](../../index-policy.md)

## Related content

- [System functions](system-functions.yml)
- [Setup Full Text Search in Azure Cosmos DB for NoSQL](../../gen-ai/full-text-search.md)
- [Full Text Index](../../index-policy.md)
