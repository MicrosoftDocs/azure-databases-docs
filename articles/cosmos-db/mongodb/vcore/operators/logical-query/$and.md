---
title: $and (logical query)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $and operator  is used to perform a logical AND operation on an array of one or more expressions and selects the documents that satisfy all the expressions in the array.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/11/2024
---

# $and (Logical Query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$and` operator is used to perform a logical AND operation on an array of one or more expressions and selects the documents that satisfy all the expressions in the array. It's particularly useful when you need to match documents against multiple criteria simultaneously.

## Syntax

The syntax for the `$and` operator is:

```javascript
{
  "$and": [
    { <expression1> },
    { <expression2> },
    ...
  ]
}
```

## Parameter

| | Description |
| --- | --- |
| **`expression1, expression2, ...`** | These are the individual query expressions that must all be true for a document to match. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
