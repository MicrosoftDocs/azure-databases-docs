---
title: $multiply (Aggregation Expression)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $multiply operator in Azure Cosmos DB for MongoDB vCore calculates the product of numerical expressions.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $multiply (aggregation expression)

The `$multiply` operator calculates the product of numerical expressions and is supported in aggregation operations. It's a useful tool for deriving calculated fields or performing arithmetic within aggregation pipelines.

## Syntax

```javascript
{
  $multiply: [ <expression1>, <expression2>, ... ]
}
```

- **`<expression1>`**: A valid expression that resolves to a number.
- **`<expression2>`**: A valid expression that resolves to a number.
- **`...`**: Additional expressions, each resolving to a number.

## Example

### Example 1: Multiply a field by a constant

This example demonstrates how to double the value of the `fullSales` field:

```javascript
db.collection.aggregate([
  {
    $project: {
      sales: 1,
      doubleSales: { $multiply: ["$sales.fullSales", 2] }
    }
  }
])
```

The result includes the original `sales` field and a new field `doubleSales` that is twice the value of `sales.fullSales`. It will produce the following output:
```json
[
  { "_id": 1, "sales": { "fullSales": 100 }, "doubleSales": 200 },
  { "_id": 2, "sales": { "fullSales": 250 }, "doubleSales": 500 },
  { "_id": 3, "sales": { "fullSales": 400 }, "doubleSales": 800 }
]
```

### Example 2: Calculate total discounts during a promotion

This example calculates the total discount for a promotion in the "DJ Turntables" category:

```javascript
db.collection.aggregate([
  {
    $project: {
      promotionEvents: 1,
      totalDiscount: {
        $multiply: [
          { $arrayElemAt: ["$promotionEvents.discounts.discountPercentage", 0] },
          "$sales.salesByCategory.totalSales"
        ]
      }
    }
  }
])
```

The `totalDiscount` field is derived by multiplying the first discount percentage from the `promotionEvents` array with the `totalSales` value. It will produce the following output:
```json
[
  {
    "_id": 4,
    "promotionEvents": {
      "discounts": [{ "discountPercentage": 0.10 }]
    },
    "sales": { "salesByCategory": { "totalSales": 5000 } },
    "totalDiscount": 500
  },
  {
    "_id": 5,
    "promotionEvents": {
      "discounts": [{ "discountPercentage": 0.15 }]
    },
    "sales": { "salesByCategory": { "totalSales": 10000 } },
    "totalDiscount": 1500
  }
]
```

### Example 3: Compute area of a rectangle

This example calculates the area of a rectangle given its `width` and `height`:

```javascript
db.collection.aggregate([
  {
    $project: {
      width: 1,
      height: 1,
      area: { $multiply: ["$dimensions.width", "$dimensions.height"] }
    }
  }
])
```

The resulting `area` field is the product of the rectangle's `width` and `height`. It will produce the following output:
```json
[
  { "_id": 6, "dimensions": { "width": 5, "height": 10 }, "area": 50 },
  { "_id": 7, "dimensions": { "width": 8, "height": 12 }, "area": 96 },
  { "_id": 8, "dimensions": { "width": 3, "height": 7 }, "area": 21 }
]
```

## Limitations

- The `$multiply` operator works only with numerical expressions. Using it with non-numerical values result in an error.
- Be cautious of overflow or precision issues when working with large numbers or floating-point arithmetic.

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]