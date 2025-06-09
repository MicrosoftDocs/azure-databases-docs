---
  title: $setEquals (set expression) operator returns `true` if two sets have the same distinct elements, regardless of order or duplicates.
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $setEquals operator returns true if two sets have the same distinct elements.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $setEquals (set expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$setEquals` operator returns `true` if two sets have the same distinct elements, regardless of order or duplicates. It treats arrays as sets, ignoring duplicate values and element order.

## Syntax

The syntax for the `$setEquals` operator is as follows:

```javascript
{
  $setEquals: [ <array1>, <array2>, ... ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`array1, array2, ...`** | Arrays to compare for equality. You can specify two or more arrays. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "sales": {
    "totalSales": 83865,
    "salesByCategory": [
      {
        "categoryName": "Lavalier Microphones",
        "totalSales": 44174
      },
      {
        "categoryName": "Wireless Microphones",
        "totalSales": 39691
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Cut Spectacular",
      "discounts": [
        {
          "categoryName": "Condenser Microphones",
          "discountPercentage": 5
        },
        {
          "categoryName": "Dynamic Microphones",
          "discountPercentage": 14
        }
      ]
    },
    {
      "eventName": "Bargain Bonanza",
      "discounts": [
        {
          "categoryName": "Streaming Microphones",
          "discountPercentage": 14
        },
        {
          "categoryName": "Microphone Stands",
          "discountPercentage": 14
        }
      ]
    }
  ]
}
```

### Example 1: Compare discount categories between events

The example allows checking if the two promotion events, offer discounts on the same categories.

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  {
    $project: {
      name: 1,
      event1Categories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      event2Categories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] },
      sameDiscountCategories: {
        $setEquals: [
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 1] }
        ]
      }
    }
  }
])
```

The query output compares the discount categories and returns false due to non matching values.

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "event1Categories": [
    "Condenser Microphones",
    "Dynamic Microphones"
  ],
  "event2Categories": [
    "Streaming Microphones",
    "Microphone Stands"
  ],
  "sameDiscountCategories": false
}
```

### Example 2: Compare staff requirements

This example allows checking if the two stores have the same staff structure requirements.

```javascript
db.stores.aggregate([
  { $match: {"_id": { $in: ["26afb024-53c7-4e94-988c-5eede72277d5", "f2a8c190-28e4-4e14-9d8b-0256e53dca66"] }} },
  {
    $group: {
      _id: null,
      stores: { $push: "$$ROOT" }
    }
  },
  {
    $project: {
      store1: { $arrayElemAt: ["$stores", 0] },
      store2: { $arrayElemAt: ["$stores", 1] },
      staffTypes1: ["fullTime", "partTime"],
      staffTypes2: ["fullTime", "partTime"],
      sameStaffStructure: {
        $setEquals: [
          ["fullTime", "partTime"],
          ["fullTime", "partTime"]
        ]
      }
    }
  }
])
```

The query returns `true` since both the stores have same staff structure.

```json
{
  "_id": null,
  "store1": {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland"
  },
  "store2": {
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele"
  },
  "staffTypes1": ["fullTime", "partTime"],
  "staffTypes2": ["fullTime", "partTime"],
  "sameStaffStructure": true
}
```

### Example 3: Compare sets with duplicates

Demonstrate that `$setEquals` ignores duplicates and order.

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  {
    $project: {
      name: 1,
      array1: ["Microphones", "Stands", "Microphones", "Accessories"],
      array2: ["Stands", "Accessories", "Microphones"],
      arraysEqual: {
        $setEquals: [
          ["Microphones", "Stands", "Microphones", "Accessories"],
          ["Stands", "Accessories", "Microphones"]
        ]
      }
    }
  }
])
```

The query returns `true` since both the provided arrays list same products in different sequence along with duplicates.

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "array1": ["Microphones", "Stands", "Microphones", "Accessories"],
  "array2": ["Stands", "Accessories", "Microphones"],
  "arraysEqual": true
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]