---
title: $nor (Logical Query) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $nor operator performs a logical NOR operation on an array of expressions, selecting documents that fail all specified expressions.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $nor (Logical Query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$nor` operator performs a logical NOR operation on an array of expressions and selects documents that fail all the specified expressions.

## Syntax

```javascript
{ $nor: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expression` | Array | An array of expressions, all of which must be false for a document to be included |

## Examples

### Example 1: Basic NOR Operation

Find stores that neither have more than 15 full-time staff nor more than 20 part-time staff:

```javascript
db.stores.find({
  $nor: [
    { "staff.totalStaff.fullTime": { $gt: 15 } },
    { "staff.totalStaff.partTime": { $gt: 20 } }
  ]
})
```

This produces the following output:

```javascript
      {
        eventName: 'Steal the Show Sale',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 7, Day: 1 }
        },
        discounts: [
          { categoryName: 'Charms', discountPercentage: 10 },
          { categoryName: 'Bracelets', discountPercentage: 13 }
        ]
      }
```

### Example 2: Complex NOR Operation

Find stores that don't have any of these conditions: total sales over 100000, sales of "Digital Watches", or promotions in September 2024:

```javascript
db.stores.find({
  $nor: [
    { "sales.totalSales": { $gt: 100000 } },
    { "sales.salesByCategory.categoryName": "Digital Watches" },
    {
      "promotionEvents": {
        $elemMatch: {
          "promotionalDates.startDate.Month": 9,
          "promotionalDates.startDate.Year": 2024
        }
      }
    }
  ]
})
```

This produces the following output:

```javascript
  {
    _id: 'binary-test',
    name: 'Test Store',
    logo: Binary(Buffer.from("627566666572", "hex"), 0),
    signature: Binary(Buffer.from("74657374", "hex"), 0)
  }
```

### Example 3: NOR with Multiple Field Conditions

Find stores that don't meet any of these location and staff criteria:

```javascript
db.stores.find({
  $nor: [
    { "location.lat": { $gt: 0 } },
    { "staff.totalStaff.fullTime": { $lt: 10 } },
    { "sales.totalSales": { $gt: 50000 } }
  ]
})
```
This produces the following output:

```javascript
  {
    _id: 'db5051a8-17d1-4b01-aa2f-31e64623e5ac',
    name: 'First Up Consultants | Watch Mart - Port Zack',
    location: { lat: -62.6354, lon: 46.2917 },
    staff: { totalStaff: { fullTime: 12, partTime: 9 } },
    sales: {
      totalSales: 6118,
      salesByCategory: [ { categoryName: 'Digital Watches', totalSales: 6118 } ]
    },
    promotionEvents: [
      {
        eventName: 'Incredible Bargain Blitz',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 6, Day: 30 }
        },
        discounts: [
          {
            categoryName: 'Chronograph Watches',
            discountPercentage: 13
          },
          { categoryName: 'Diving Watches', discountPercentage: 21 }
        ]
      },
      {
        eventName: 'Fantastic Deals Festival',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 9, Day: 29 }
        },
        discounts: [
          { categoryName: 'Digital Watches', discountPercentage: 25 },
          { categoryName: 'Pilot Watches', discountPercentage: 17 }
        ]
      }
    ]
  }
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]