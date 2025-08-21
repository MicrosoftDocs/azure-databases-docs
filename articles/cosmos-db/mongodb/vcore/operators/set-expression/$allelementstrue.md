---
  title: $allElementsTrue
  titleSuffix: Overview of the $allElementsTrue operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $allElementsTrue operator returns true if all elements in an array evaluates to true.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $allElementsTrue

The `$allElementsTrue` operator evaluates an array as a set. It returns `true` if no element in the array has a value of `false` or equivalent to `false` (like `null`, `0`, or `undefined`). If any element evaluates to a value of `false` or the equivalent, the operator returns `false`.

## Syntax

```javascript
{
  $allElementsTrue: [ <array> ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| `array` | An array of expressions to evaluate. If the array is empty, `$allElementsTrue` returns `true`. |

## JSON example

The following JSON sample from the `stores` dataset can help you understand how to use this operator.

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

### Example: Determine if all the discount percentages are higher than zero

The aggregation query determines if all the discount percentages in each promotion event are greater than zero.

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
