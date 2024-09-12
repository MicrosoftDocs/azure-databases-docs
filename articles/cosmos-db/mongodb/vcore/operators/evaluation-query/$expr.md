---
title: $expr (evaluation query)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $expr operator allows the use of aggregation expressions within the query language.
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/11/2024
---

# $expr (Evaluation Query)

The `$expr` operator allows the use of aggregation expressions within the query language. This enables more complex queries by allowing field comparisons, arithmetic operations, and other expressions directly within the query. Use cases for `$expr` include filtering documents based on computed values, comparing fields within the same document, and performing operations that would otherwise require a separate aggregation pipeline.

## Syntax

The basic syntax for using the `$expr` operator is as follows:

```javascript
{
  $expr: { <expression> }
}
```

### Parameters

| | Description |
| --- | --- |
| **`expression`** | An aggregation expression that evaluates to a boolean. The expression can include field paths, arithmetic operations, logical operations, and more. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
