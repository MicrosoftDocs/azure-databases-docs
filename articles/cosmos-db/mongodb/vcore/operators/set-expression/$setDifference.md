---
  title: $setDifference returns a set with elements that exist in the first set but not in the second set.
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $setDifference operator returns a set with elements that exist in the first set but not in the second set.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/09/2025
---

# $setDifference (set expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$setDifference` operator returns a set with elements that exist in the first set but not in the second set. It treats arrays as sets, ignoring duplicate values and element order.

## Syntax

The syntax for the `$setDifference` operator is as follows:

```javascript
{
  $setDifference: [ <array1>, <array2> ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`array1`** | The first array to compare. Elements unique to this array are returned. |
| **`array2`** | The second array to compare against. Elements that exist in both arrays are excluded from the result. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "sales": {
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
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        },
        {
          "categoryName": "Media Players",
          "discountPercentage": 21
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 22
        }
      ]
    }
  ]
}
```

### Example 1: Find categories sold but not discounted

The example checks for product categories with sales data but aren't providing any discounts.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      soldCategories: "$sales.salesByCategory.categoryName",
      discountedCategories: {
        $reduce: {
          input: "$promotionEvents",
          initialValue: [],
          in: {
            $concatArrays: ["$$value", "$$this.discounts.categoryName"]
          }
        }
      }
    }
  },
  {
    $project: {
      name: 1,
      soldCategories: 1,
      discountedCategories: 1,
      categoriesWithoutDiscounts: {
        $setDifference: ["$soldCategories", "$discountedCategories"]
      }
    }
  }
])
```

The query output shows categories which are sold but never discounted.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "soldCategories": [
    "Sound Bars",
    "Home Theater Projectors",
    "Game Controllers",
    "Remote Controls",
    "VR Games"
  ],
  "discountedCategories": [
    "DVD Players",
    "Projector Lamps",
    "Media Players",
    "Blu-ray Players",
    "Home Theater Systems",
    "Televisions"
  ],
  "categoriesWithoutDiscounts": [
    "Sound Bars",
    "Home Theater Projectors",
    "Game Controllers",
    "Remote Controls",
    "VR Games"
  ]
}
```

### Example 2: Compare staff distribution types

Find the difference between two hypothetical staff requirement lists.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      requiredSkills: ["Sales", "Customer Service", "Technical Support", "Inventory Management"],
      availableSkills: ["Sales", "Customer Service", "Marketing", "Administration"],
      missingSkills: {
        $setDifference: [
          ["Sales", "Customer Service", "Technical Support", "Inventory Management"],
          ["Sales", "Customer Service", "Marketing", "Administration"]
        ]
      }
    }
  }
])
```

The query returns the skills that are required but not available.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "requiredSkills": [
    "Sales",
    "Customer Service", 
    "Technical Support",
    "Inventory Management"
  ],
  "availableSkills": [
    "Sales",
    "Customer Service",
    "Marketing",
    "Administration"
  ],
  "missingSkills": [
    "Technical Support",
    "Inventory Management"
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]