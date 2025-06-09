---
  title: $setIntersection returns the common elements that appear in all input arrays.
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $setIntersection operator returns the common elements that appear in all input arrays.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $setIntersection (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$setIntersection` operator returns an array containing the elements that appear in all of the input arrays. It treats arrays as sets, meaning it removes duplicates and ignores the order of elements.

## Syntax

The syntax for the `$setIntersection` operator is as follows:

```javascript
{
  $setIntersection: [ <array1>, <array2>, ... ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`<array1>, <array2>, ...`** | Two or more arrays to find the intersection of. Each array is treated as a set. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      },
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        },
        "endDate": {
          "Year": 2023,
          "Month": 7,
          "Day": 9
        }
      },
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        },
        {
          "categoryName": "Projector Lamps",
          "discountPercentage": 6
        },
        {
          "categoryName": "Media Players",
          "discountPercentage": 21
        },
        {
          "categoryName": "Blu-ray Players",
          "discountPercentage": 21
        },
        {
          "categoryName": "Home Theater Systems",
          "discountPercentage": 5
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 22
        }
      ]
    },
    {
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 12,
          "Day": 26
        },
        "endDate": {
          "Year": 2024,
          "Month": 1,
          "Day": 5
        }
      },
      "discounts": [
        {
          "categoryName": "Game Controllers",
          "discountPercentage": 22
        },
        {
          "categoryName": "Home Theater Projectors",
          "discountPercentage": 23
        },
        {
          "categoryName": "Sound Bars",
          "discountPercentage": 10
        },
        {
          "categoryName": "Media Players",
          "discountPercentage": 10
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 9
        },
        {
          "categoryName": "Projector Lamps",
          "discountPercentage": 24
        }
      ]
    }
  ]
}
```

### Example 1: Find common categories between sales and promotions

The example allows finding what product categories appear in both the sales data and promotion discounts for a store.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      salesCategories: "$sales.salesByCategory.categoryName",
      firstPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      secondPromotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
      commonSalesAndFirstPromotion: {
        $setIntersection: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] }
        ]
      },
      commonSalesAndSecondPromotion: {
        $setIntersection: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] }
        ]
      }
    }
  }
])
```

The query output shows which categories are common between sales and different promotion events.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "salesCategories": [
    "Sound Bars",
    "Home Theater Projectors",
    "Game Controllers",
    "Remote Controls",
    "VR Games"
  ],
  "firstPromotionCategories": [
    "DVD Players",
    "Projector Lamps",
    "Media Players",
    "Blu-ray Players",
    "Home Theater Systems",
    "Televisions"
  ],
  "secondPromotionCategories": [
    "Game Controllers",
    "Home Theater Projectors",
    "Sound Bars",
    "Media Players",
    "Televisions",
    "Projector Lamps"
  ],
  "commonSalesAndFirstPromotion": [],
  "commonSalesAndSecondPromotion": [
    "Sound Bars",
    "Home Theater Projectors",
    "Game Controllers"
  ]
}
```

### Example 2: Find categories common across multiple promotion events

The example allows us to find categories that appear in multiple promotion events.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      commonAcrossPromotions: {
        $setIntersection: [
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 2] }
        ]
      }
    }
  }
])
```

The query returns an empty array for `commonAcrossPromotions` as there are no common product category appearing across all the promotions.

```json
 {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "commonAcrossPromotions": []
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]