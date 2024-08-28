---
title: Operator - $elemMatch (array query)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $elemMatch operator is used to match documents that contain an array field with at least one element that matches all the specified query criteria.
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# Operator: `$elemMatch` (array query)

The `$elemMatch` operator in Azure Cosmos DB for MongoDB vCore is used to match documents that contain an array field with at least one element that matches all the specified query criteria. This operator is useful when you need to filter documents based on conditions within array elements.

## Syntax

```json
db.collection.find({ <field>: { $elemMatch: { <query1>, <query2>, ... } } })
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`** | The field in the document that contains the array to be queried. |
| **`<query1>, <query2>, ...`** | The conditions that at least one element in the array must satisfy. |

## Examples

Here are a few examples of this operator in use.

### Find stores with a specific sales category

Find stores where there's a sales category with a total sales amount greater than 35000.

```javascript
db.stores.find({
  "store.sales.salesByCategory": {
    $elemMatch: {
      totalSales: { $gt: 35000 }
    }
  }
}).limit(1);
```

### Find stores with specific promotion discount

Find stores where there's a promotion event with a discount of 20% or more on Laptops.

```javascript
db.stores.find({
  "store.promotionEvents.discounts": {
    $elemMatch: {
      categoryName: "Laptops",
      discountPercentage: { $gte: 20 }
    }
  }
});
```

## Related content

- [`$size` (array query)](array-query-size.md)
- [`$elemMatch` (projection)](projection-elemmatch.md)
