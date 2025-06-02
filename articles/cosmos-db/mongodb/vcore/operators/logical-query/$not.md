---
title: $not (Logical Query) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $not operator performs a logical NOT operation on a specified expression, selecting documents that do not match the expression.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $not (logical query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$not` operator performs a logical NOT operation on a specified expression and selects documents that do not match the expression.

## Syntax

```javascript
{ field: { $not: { <operator-expression> } } }
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `operator-expression` | Expression | The expression to negate |

## Examples

### Example 1: Basic NOT operation

Find stores that don't have exactly 5 full-time staff:

```javascript
db.stores.find({
  "staff.totalStaff.fullTime": {
    $not: { $eq: 5 }
  }
})
```

Output:

```javascript
      {
        eventName: 'Unbeatable Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 7, Day: 2 }
        },
        discounts: [
          { categoryName: 'Cabinets', discountPercentage: 8 },
          { categoryName: 'Desks', discountPercentage: 22 }
        ]
      }
```

### Example 2: NOT with regular expression

Find stores whose names don't start with "First Up":

```javascript
db.stores.find({
  name: {
    $not: /^First Up/
  }
})
```

Output:

```javascript
  {
    _id: 'cac30620-fd99-4ee2-8329-c87980ab2b24',
    name: 'Contoso, Ltd. | Handbag Bargains - South Jovanny',
    location: { lat: 19.6816, lon: 18.6237 },
    staff: { totalStaff: { fullTime: 10, partTime: 19 } },
    sales: {
      totalSales: 56878,
      salesByCategory: [
        { categoryName: 'Mini Bags', totalSales: 20543 },
        { categoryName: 'Satchels', totalSales: 36335 }
      ]
    },
    promotionEvents: [
      {
        eventName: 'Price Slash Carnival',
        promotionalDates: {
          startDate: { Year: 2023, Month: 6, Day: 29 },
          endDate: { Year: 2023, Month: 7, Day: 8 }
        },
        discounts: [
          { categoryName: 'Messenger Bags', discountPercentage: 9 },
          { categoryName: 'Shoulder Bags', discountPercentage: 8 }
        ]
      },
      {
        eventName: 'Major Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2023, Month: 9, Day: 27 },
          endDate: { Year: 2023, Month: 10, Day: 5 }
        },
        discounts: [
          { categoryName: 'Hobo Bags', discountPercentage: 15 },
          { categoryName: 'Messenger Bags', discountPercentage: 9 }
        ]
      },
      {
        eventName: 'Unbeatable Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2023, Month: 12, Day: 26 },
          endDate: { Year: 2024, Month: 1, Day: 4 }
        },
        discounts: [
          { categoryName: 'Bucket Bags', discountPercentage: 22 },
          { categoryName: 'Shoulder Bags', discountPercentage: 10 }
        ]
      },
      {
        eventName: 'Big Bargain Blitz',
        promotionalDates: {
          startDate: { Year: 2024, Month: 3, Day: 25 },
          endDate: { Year: 2024, Month: 4, Day: 1 }
        },
        discounts: [
          { categoryName: 'Crossbody Bags', discountPercentage: 25 },
          { categoryName: 'Backpacks', discountPercentage: 19 }
        ]
      },
      {
        eventName: 'Clearance Carnival',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 6, Day: 30 }
        },
        discounts: [
          { categoryName: 'Bucket Bags', discountPercentage: 8 },
          { categoryName: 'Mini Bags', discountPercentage: 16 }
        ]
      },
      {
        eventName: 'Blowout Bargain Bash',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 9, Day: 29 }
        },
        discounts: [
          { categoryName: 'Hobo Bags', discountPercentage: 23 },
          { categoryName: 'Clutches', discountPercentage: 8 }
        ]
      }
    ]
  }
```
### Example 3: Complex NOT operation

Find stores that don't have any promotional events with exactly 20% discount:

```javascript
db.stores.find({
  "promotionEvents.discounts.discountPercentage": {
    $not: { $eq: 20 }
  }
})
```

Output:

```javascript
  {
    _id: 'f25b56da-2789-42f2-b844-3c88c7384307',
    name: 'Fourth Coffee | Home Decor Corner - Kavonshire',
    location: { lat: -82.8806, lon: 125.2905 },
    staff: { totalStaff: { fullTime: 19, partTime: 14 } },
    sales: {
      totalSales: 6485,
      salesByCategory: [ { categoryName: 'Picture Frames', totalSales: 6485 } ]
    },
    promotionEvents: [
      {
        eventName: 'Crazy Discount Days',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 10, Day: 1 }
        },
        discounts: [
          { categoryName: 'Mirrors', discountPercentage: 21 },
          { categoryName: 'Vases', discountPercentage: 15 }
        ]
      }
    ]
  }..
```

## Limitations

   - `$not` only accepts a single expression
   - Cannot directly contain another logical operator



## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
