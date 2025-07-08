---
title: $and (Logical Query) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $and operator joins query clauses with a logical AND, returning documents that match all specified conditions.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $and (Logical Query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$and` operator performs a logical AND operation on an array of expressions and selects the documents that satisfy all the expressions.

## Syntax

```javascript
{ $and: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expression` | Array | An array of expressions that must all be true for a document to be included in the results |

## Examples

### Example 1: Basic AND operation

Find stores with more than 10 full-time staff and more than 15 part-time staff:

```javascript
db.stores.find({
  $and: [
    { "staff.totalStaff.fullTime": { $gt: 10 } },
    { "staff.totalStaff.partTime": { $gt: 15 } }
  ]
})
```

### Example 2: Complex AND operation

Find stores that have total sales over 100000 and have both "Game Controllers" and "Home Theater Projectors" in their sales categories:

```javascript
db.stores.find({
  $and: [
    { "sales.totalSales": { $gt: 100000 } },
    { "sales.salesByCategory.categoryName": "Game Controllers" },
    { "sales.salesByCategory.categoryName": "Home Theater Projectors" }
  ]
})
```

### Example 3: Combining multiple conditions

Find stores that have promotional events in both June 2024 and September 2024 with discounts greater than 20%:

```javascript
db.stores.find({
  $and: [
    {
      "promotionEvents": {
        $elemMatch: {
          "promotionalDates.startDate.Month": 6,
          "promotionalDates.startDate.Year": 2024
        }
      }
    },
    {
      "promotionEvents": {
        $elemMatch: {
          "promotionalDates.startDate.Month": 9,
          "promotionalDates.startDate.Year": 2024,
          "discounts.discountPercentage": { $gt: 20 }
        }
      }
    }
  ]
})
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
