---
title: $pow (as arithmetic expression operator) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The `$pow` operator raises a number to the specified exponent.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $pow (as arithmetic expression operator) usage on Azure Cosmos DB for MongoDB (vCore)

The `$pow` operator is used to raise a number to a specified exponent. This can be useful in various scenarios where mathematical computations are required within your documents. 

## Syntax

```javascript
{ $pow: [ <number>, <exponent> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | The base number to be raised to the exponent. |
| **`<exponent>`** | The exponent to raise the base number to. |

## Example(s)

### Example 1: Calculate the square of a number

Suppose you want to calculate the square of the `fullSales` field in the `sales` document.

```javascript
db.collection.aggregate([
  {
    $project: {
      fullSalesSquare: { $pow: [ "$sales.fullSales", 2 ] }
    }
  }
])
```

This output shows that the `fullSalesSquare` field contains the square of `fullSales`.
```json
[
  { "_id": 1, "sales": { "fullSales": 10 }, "fullSalesSquare": 100 },
  { "_id": 2, "sales": { "fullSales": 20 }, "fullSalesSquare": 400 },
  { "_id": 3, "sales": { "fullSales": 30 }, "fullSalesSquare": 900 }
]
```

### Example 2: Calculate a power of a specific category's total sales

If you want to calculate `totalSales` raised to the power of 3 for the "DJ Headphones" category:

```javascript
db.collection.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  },
  {
    $match: { "sales.salesByCategory.categoryName": "DJ Headphones" }
  },
  {
    $project: {
      totalSalesCubed: { $pow: [ "$sales.salesByCategory.totalSales", 3 ] }
    }
  }
])
```

This output shows the `totalSales` value raised to the power of 3 for the "DJ Headphones" category:
```json
[
  {
    "_id": 4,
    "category": "DJ Headphones",
    "sales": { "salesByCategory": { "totalSales": 5 } },
    "totalSalesCubed": 125
  },
  {
    "_id": 5,
    "category": "DJ Headphones",
    "sales": { "salesByCategory": { "totalSales": 10 } },
    "totalSalesCubed": 1000
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]