---
title: $or (Logical Query) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $or operator joins query clauses with a logical OR, returning documents that match at least one specified condition.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $or (logical query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$or` operator performs a logical OR operation on an array of expressions and selects documents that satisfy at least one of the expressions.

## Syntax

```javascript
{ $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expression` | Array | An array of expressions, where at least one must be true for a document to be included |

## Examples

### Example 1: Basic OR Operation

Find stores that either have more than 15 full-time staff or more than 20 part-time staff:

```javascript
db.stores.find({
  $or: [
    { "staff.totalStaff.fullTime": { $gt: 15 } },
    { "staff.totalStaff.partTime": { $gt: 20 } }
  ]
})
```

Output:

```javascript
  {
    _id: 'd924d148-9e01-4ab1-91d6-9daccb12a4dd',
    name: 'Fourth Coffee | Home Entertainment Gallery - East Adellahaven',
    location: { lat: -86.4872, lon: 130.9398 },
    staff: { totalStaff: { fullTime: 16, partTime: 14 } },
    sales: {
      totalSales: 179639,
      salesByCategory: [
        { categoryName: 'Home Theater Systems', totalSales: 18707 },
        { categoryName: 'Xbox Games', totalSales: 48276 },
        { categoryName: 'Sound Bars', totalSales: 43142 },
        { categoryName: 'Projector Mounts', totalSales: 43358 },
        { categoryName: 'Televisions', totalSales: 11325 },
        { categoryName: 'Streaming Devices', totalSales: 14831 }
      ]
    },
    promotionEvents: [
      {
        eventName: 'Massive Deal Mania',
        promotionalDates: {
          startDate: { Year: 2024, Month: 9, Day: 21 },
          endDate: { Year: 2024, Month: 9, Day: 29 }
        },
        discounts: [
          {
            categoryName: 'Home Theater Projectors',
            discountPercentage: 16
          },
          { categoryName: 'TV Mounts', discountPercentage: 17 },
          { categoryName: 'Projector Lamps', discountPercentage: 24 },
          { categoryName: 'Sound Bars', discountPercentage: 8 },
          { categoryName: 'Media Players', discountPercentage: 14 },
          {
            categoryName: 'Nintendo Switch Games',
            discountPercentage: 22
          }
        ]
      }
    ]
  }..
```


### Example 2: Complex OR Operation

Find stores that either have total sales over 100000 or have promotions with discounts greater than 20%:

```javascript
db.stores.find({
  $or: [
    { "sales.totalSales": { $gt: 100000 } },
    { "promotionEvents.discounts.discountPercentage": { $gt: 20 } }
  ]
})
```

Output:

```javascript
      {
        eventName: 'Bargain Blitz Bash',
        promotionalDates: {
          startDate: { Year: 2024, Month: 3, Day: 25 },
          endDate: { Year: 2024, Month: 4, Day: 3 }
        },
        discounts: [
          { categoryName: 'Pet Carriers', discountPercentage: 22 },
          { categoryName: 'Pet Collars', discountPercentage: 11 }
        ]
      },
      {
        eventName: 'Clearance Carnival',
        promotionalDates: {
          startDate: { Year: 2024, Month: 6, Day: 23 },
          endDate: { Year: 2024, Month: 6, Day: 30 }
        },
        discounts: [
          { categoryName: 'Cat Litter', discountPercentage: 18 },
          { categoryName: 'Pet Beds', discountPercentage: 8 }
        ]
      }..
```

### Example 3: OR with Multiple Conditions and Arrays

Find stores that match any of these criteria: sell electronics, have high staff count, or have specific promotional events:

```javascript
db.stores.find({
  $or: [
    { "sales.salesByCategory.categoryName": { $in: ["Game Controllers", "Sound Bars", "Home Theater Projectors"] } },
    {
      $and: [
        { "staff.totalStaff.fullTime": { $gt: 10 } },
        { "staff.totalStaff.partTime": { $gt: 15 } }
      ]
    },
    {
      "promotionEvents": {
        $elemMatch: {
          "eventName": "Super Sale Spectacular",
          "discounts.discountPercentage": { $gt: 15 }
        }
      }
    }
  ]
})
```

## Performance Considerations

   - Each condition in the `$or` array is evaluated independently
   - Use indexes when possible for better performance
   - Consider the order of conditions for optimal execution
   - Use `$in` instead of `$or` for multiple equality checks on the same field
   - Keep the number of `$or` conditions reasonable


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
