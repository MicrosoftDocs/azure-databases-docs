---
  title: The `$allElementsTrue` operator returns true if all elements in an array evaluate to true (including empty array) else returns false.
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $elemMatch operator returns only the first element from an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $allElementsTrue (set expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$allElementsTrue` operator evaluates an array as a set and returns `true` if no element in the array is `false` or equivalent to `false` (such as `null`, `0`, or `undefined`). If any element evaluates to `false`, the operator returns `false`.

## Syntax

The syntax for the `$allElementsTrue` operator is as follows:

```javascript
{
  $allElementsTrue: [ <array> ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`array`** | An array of expressions to evaluate. If the array is empty, `$allElementsTrue` returns `true`. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Bath Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "Pillow Top Mattresses",
          "discountPercentage": 17
        },
        {
          "categoryName": "Bathroom Scales",
          "discountPercentage": 9
        }
      ]
    }
  ]
}
```

### Example 1: Check if all discount percentages are higher than zero

Suppose you want to verify that all discount percentages in a promotion event are greater than zero.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  { $unwind: "$promotionEvents" },
  {
    $project: {
      allDiscountsValid: {
        $allElementsTrue: [
          {
            $map: {
              input: "$promotionEvents.discounts.discountPercentage",
              as: "discount",
              in: { $gt: ["$$discount", 0] }
            }
          }
        ]
      }
    }
  }
])
```

The query shows whether all discount percentages are greater than zero.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "allDiscountsValid": true
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]