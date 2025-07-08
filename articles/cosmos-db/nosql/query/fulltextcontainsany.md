---
title: FullTextContainsAny
titleSuffix: Azure Cosmos DB for NoSQL
description: An Azure Cosmos DB for NoSQL system function for full text search, finding any of the specified terms in a path.
author: jcodella
ms.author: jacodel
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: reference
ms.devlang: nosql
ms.date: 11/04/2024
ms.custom:
  - query-reference
  - ingite-2024
  - build-2025
---

# FullTextContainsAny (NoSQL query)

[!INCLUDE[NoSQL](../../includes/appliesto-nosql.md)]

Returns a boolean indicating whether any of the provided string expressions are contained in a specified property path.

## Syntax


```nosql
FullTextContainsAny(<property_path>, <string_expr1>, <string_expr2>, ...)  
```

## Arguments

| | Description |
| --- | --- |
| **`property_path`** | The property path to search. |
| **`string_expr1`** | A string to find. |
| **`string_expr1`** | A  string to find. |

## Return types

Returns a boolean expression.  

## Examples

This example returns all documents that contain either "search phrase" or "keyword" in the path `c.text`, projects the path, and returns only the TOP 10.

```nosql
SELECT TOP 10 c.text
FROM c
WHERE FullTextContainsAny(c.text, "search phrase", "keyword")
```

This example returns all documents that contain  "keyword1", "keyword2", or "keyword3" in the path `c.text`.

```nosql
SELECT *
FROM c
WHERE FullTextContainsAny(c.text, "keyword1", "keyword2", "keyword3") 
```

## Remarks

- This function requires enrollment in the [Azure Cosmos DB NoSQL Full Text Search feature](../../gen-ai/full-text-search.md)
- This function benefits from a [Full Text Index](../../index-policy.md)
  
## Related content

- [System functions](system-functions.yml)
- [Setup Full Text Search in Azure Cosmos DB for NoSQL](../../gen-ai/full-text-search.md)
- [Full Text Index](../../index-policy.md)
