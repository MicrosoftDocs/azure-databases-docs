---
  title: $setIsSubset (set expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $setIsSubset operator determines if the first array is a subset of the second array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $setIsSubset (set expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$setIsSubset` operator returns a boolean value indicating whether the first array is a subset of the second array. It treats arrays as sets, meaning it ignores duplicates and element order. Returns `true` if all elements in the first array exist in the second array, otherwise `false`.

## Syntax

The syntax for the `$setIsSubset` operator is as follows:

```javascript
{
  $setIsSubset: [ <array1>, <array2> ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`<array1>`** | The array to check if it's a subset of array2. |
| **`<array2>`** | The array to check against. |

## Example

Let's understand the usage with sample json from `stores` dataset.

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
        },
        {
          "categoryName": "Towels",
          "discountPercentage": 5
        },
        {
          "categoryName": "Bathrobes",
          "discountPercentage": 5
        },
        {
          "categoryName": "Mattress Toppers",
          "discountPercentage": 6
        },
        {
          "categoryName": "Hand Towels",
          "discountPercentage": 9
        },
        {
          "categoryName": "Shower Heads",
          "discountPercentage": 5
        },
        {
          "categoryName": "Bedspreads",
          "discountPercentage": 19
        },
        {
          "categoryName": "Bath Mats",
          "discountPercentage": 21
        }
      ]
    }
  ]
}
```

### Example 1: Check if sales categories are subset of promotion categories

The example allows checking if all categories that the store sells are also included in their promotion discounts and vice versa.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      salesCategories: "$sales.salesByCategory.categoryName",
      promotionCategories: { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
      salesAreSubsetOfPromotions: {
        $setIsSubset: [
          "$sales.salesByCategory.categoryName",
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] }
        ]
      },
      promotionsAreSubsetOfSales: {
        $setIsSubset: [
          { $arrayElemAt: ["$promotionEvents.discounts.categoryName", 0] },
          "$sales.salesByCategory.categoryName"
        ]
      }
    }
  }
])
```

The query return categories covered under both Sales and promotion bracket and confirms that sales is subset of promotion category while same isn't true other way around.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "salesCategories": [
    "Mattress Toppers"
  ],
  "promotionCategories": [
    "Bath Accessories",
    "Pillow Top Mattresses",
    "Bathroom Scales",
    "Towels",
    "Bathrobes",
    "Mattress Toppers",
    "Hand Towels",
    "Shower Heads",
    "Bedspreads",
    "Bath Mats"
  ],
  "salesAreSubsetOfPromotions": true,
  "promotionsAreSubsetOfSales": false
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]