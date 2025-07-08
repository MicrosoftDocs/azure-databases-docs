---
  title: $literal (literal expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $literal operator returns the specified value without parsing it as an expression, allowing literal values to be used in aggregation pipelines.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $literal (literal expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$literal` operator returns the specified value without parsing it as an expression. This operator is useful when you need to include literal values that might otherwise be interpreted as field names, operators, or expressions in your aggregation pipeline. It ensures that the value is treated as a constant rather than being evaluated.

## Syntax

The syntax for the `$literal` operator is as follows:

```javascript
{
  $literal: <value>
}
```

## Parameters

| | Description |
| --- | --- |
| **`<value>`** | Any value that should be returned as-is without interpretation. This can be a string, number, boolean, array, object, or null. |

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
        }
      ]
    }
  ]
}
```

### Example 1: Adding literal status fields

The example demonstrates adding literal status information to store documents, including literal strings that might otherwise be interpreted as field names or operators.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      status: { $literal: "Active" },
      reviewStatus: { $literal: "$pending" },
      priority: { $literal: 1 },
      metadata: {
        $literal: {
          lastUpdated: "2024-06-13",
          source: "automated-system"
        }
      }
    }
  }
])
```

The query adds literal values to each store document. Note how `$pending` is treated as a literal string rather than a field reference.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "totalSales": 37701,
  "status": "Active",
  "reviewStatus": "$pending",
  "priority": 1,
  "metadata": {
    "lastUpdated": "2024-06-13",
    "source": "automated-system"
  }
}
```

### Example 2: Creating literal arrays and conditional values

This example shows how to use `$literal` with arrays and in conditional expressions to ensure values are not interpreted as operators.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      performanceCategory: {
        $cond: {
          if: { $gte: ["$sales.totalSales", 100000] },
          then: { $literal: "High Performer" },
          else: { $literal: "Standard" }
        }
      },
      tags: { $literal: ["$featured", "$promoted", "$new"] },
      searchKeywords: {
        $literal: {
          "$or": ["electronics", "entertainment"],
          "$and": ["home", "theater"]
        }
      }
    }
  }
])
```

The query creates literal arrays and objects that contain strings starting with `$`, which would normally be interpreted as operators or field references.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "totalSales": 160000,
  "performanceCategory": "High Performer",
  "tags": ["$featured", "$promoted", "$new"],
  "searchKeywords": {
    "$or": ["electronics", "entertainment"],
    "$and": ["home", "theater"]
  }
}
```

### Example 3: Literal null and boolean values

This example demonstrates using `$literal` with null values and booleans, especially useful when these values need to be explicitly set rather than computed.

```javascript
db.stores.aggregate([
  { $match: {"_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.salesByCategory.totalSales",
      specialOffer: { $literal: null },
      isOnline: { $literal: false },
      hasInventory: { $literal: true },
      calculationFormula: { $literal: "$multiply: [price, quantity]" },
      ratingSystem: {
        $literal: {
          min: 0,
          max: 5,
          default: null
        }
      }
    }
  }
])
```

The query adds explicit literal values including null, booleans, and strings that look like MongoDB expressions.

```json
{
  "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
  "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
  "totalSales": 17676,
  "specialOffer": null,
  "isOnline": false,
  "hasInventory": true,
  "calculationFormula": "$multiply: [price, quantity]",
  "ratingSystem": {
    "min": 0,
    "max": 5,
    "default": null
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
