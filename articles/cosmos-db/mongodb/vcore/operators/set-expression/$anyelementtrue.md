---
  title: $anyElementsTrue
  titleSuffix: Overview of the $allElementsTrue operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $anyElementsTrue operator returns a value of true if any element in an array is evaluated to have a value of true.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $anyElementTrue

The `$anyElementTrue` operator evaluates an array as a set and returns a value of `true` if any element in the array is `true` (or equivalent to `true`). If all the elements are evaluated to have a value of `false`, `null`, `0`, or `undefined`, the operator returns a value of `false`.

## Syntax

```javascript
{
  $anyElementTrue: [ <array> ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| `array` | An array of expressions that you want to evaluate. If the array is empty, `$anyElementTrue` returns a value of `false`. |

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

### Example 1: Determine if any sales category exceeds a target

This following example helps you determine if any sales category exceeds a target. In this case, the target is 40,000 in sales.

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

The query returns a value of `true` for the `hasHighPerformingCategory` field, because sales for one of the categories is over 40,000.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "salesByCategory": [
    {
      "categoryName": "Sound Bars",
      "totalSales": 2120,
      "lastUpdated": "2025-06-11T11:10:34.414Z"
    },
    null,
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

### Example 2: Determine whether any promotion event has high discounts

The following example helps you determine if any promotion event offers discounts over 20%.

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

The query returns a value of `true`, because there's at least one promotion event with discounts over 20%.

```json
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Massive Markdown Mania",
    "hasHighDiscount": true
    },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Fantastic Deal Days",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Discount Delight Days",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Super Sale Spectacular",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Grand Deal Days",
    "hasHighDiscount": true
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Major Bargain Bash",
    "hasHighDiscount": true
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
