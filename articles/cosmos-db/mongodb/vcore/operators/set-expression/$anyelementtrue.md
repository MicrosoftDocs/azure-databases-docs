---
  title: $anyElementsTrue (set expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $anyElementsTrue operator returns true if any element evaluates to true in an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/09/2025
---

# $anyElementTrue (set expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$anyElementTrue` operator evaluates an array as a set and returns `true` if any element in the array is `true` or equivalent to `true`. If all elements evaluate to `false`, `null`, `0`, or `undefined`, the operator returns `false`.

## Syntax

The syntax for the `$anyElementTrue` operator is as follows:

```javascript
{
  $anyElementTrue: [ <array> ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`array`** | An array of expressions to evaluate. If the array is empty, `$anyElementTrue` returns `false`. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

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
  }
}
```

### Example 1: Check if any sales category exceeds target

This example allows checking if any sales category exceeds a target of 40,000 in sales.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      salesByCategory: "$sales.salesByCategory",
      hasHighPerformingCategory: {
        $anyElementTrue: [
          {
            $map: {
              input: "$sales.salesByCategory",
              as: "category",
              in: { $gt: ["$$category.totalSales", 40000] }
            }
          }
        ]
      }
    }
  }
])
```

The query returns `true` for `hasHighPerformingCategory` field as sales for one of the categories is beyond 40,000.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
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
  ],
  "hasHighPerformingCategory": true
}
```

### Example 2: Check if any promotion event has high discounts

This example allows checking if any promotion event offers discounts above 20%.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  { $unwind: "$promotionEvents" },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      hasHighDiscount: {
        $anyElementTrue: [
          {
            $map: {
              input: "$promotionEvents.discounts",
              as: "discount",
              in: { $gte: ["$$discount.discountPercentage", 20] }
            }
          }
        ]
      }
    }
  }
])
```

The query returns `true` considering we have at least one promotion event with discounts above 20%.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "eventName": "Massive Markdown Mania",
  "hasHighDiscount": true
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]