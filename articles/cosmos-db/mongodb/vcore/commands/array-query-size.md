---
title: Operator - $size (array query)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $size operator is used to query documents where an array field has a specified number of elements.
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# Operator: `$size` (array query)

The `$size` operator in Azure Cosmos DB for MongoDB vCore is used to query documents where an array field has a specified number of elements. This operator is useful when you need to find documents based on the size of an array field, such as finding documents with some items in a list.

## Syntax

```javascript
db.collection.find({ <field>: { $size: <number> } })
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`** | The field that contains the array. |
| **`<number>`** | The number of elements the array should have. |

## Examples

Here are a few examples of this operator in use.

### Finding documents with a specific number of promotional events

To find documents where the `promotionEvents` array has exactly one promotion event only.

```javascript
db.stores.find({ "promotionEvents": { $size: 1 } })
```

### Finding documents with a specific number of discounts in a promotion event

To find documents where the first promotion event (`promotionEvents.0.discounts`) has exactly two discounts.

```javascript
db.stores.find({ "promotionEvents.0.discounts": { $size: 2 } })
```

## Related content

- [`$elemMatch` (array query)](array-query-elemmatch.md)
