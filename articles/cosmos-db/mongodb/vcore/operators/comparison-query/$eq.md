---
title: $eq (Comparison Query)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $eq operator matches documents where the value of a field is equal to a specified value.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/11/2024
---

# $eq (Comparison Query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$eq` operator is used to match documents where the value of a field is equal to a specified value. This operator is particularly useful for filtering documents based on exact matches. It can be used in various query contexts, such as finding documents with specific field values, filtering arrays, and more.

## Syntax

The syntax for the `$eq` operator is as follows:

```javascript
{ field: { $eq: value } }
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field to be compared. |
| **`count`** | The value to compare against. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
