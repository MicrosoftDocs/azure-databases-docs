---
  title: $or returns true when at least one expression evaluates to true.
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $or operator returns true when at least one expression evaluates to true.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/13/2025
---

# $or (boolean expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$or` operator returns `true` when at least one expression evaluates to `true`. It performs a logical OR operation on an array of expressions. If all expressions evaluate to `false`, the entire `$or` expression returns `false`. This operator is useful for creating flexible conditions where any one of multiple criteria can be satisfied.

## Syntax

The syntax for the `$or` operator is as follows:

```javascript
{
  $or: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`<expression1>, <expression2>, ...`** | Two or more expressions to be evaluated. If any expression evaluates to `true`, the `$or` operation returns `true`. |

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

### Example 1: Identify stores with either high sales or large staff

The example finds stores that have either total sales greater than 50,000 or more than 25 total staff members.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      totalStaff: { 
        $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] 
      },
      qualifiesForProgram: {
        $or: [
          { $gt: ["$sales.totalSales", 50000] },
          { $gt: [{ $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }, 25] }
        ]
      }
    }
  },
  { $limit: 4 }
])
```

The query returns stores that meet either the sales or staffing criteria.

```json
  {
    "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
    "name": "Trey Research | Home Office Depot - Lake Freeda",
    "totalStaff": 31,
    "qualifiesForProgram": true
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "totalStaff": 27,
    "qualifiesForProgram": true
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "totalStaff": 13,
    "qualifiesForProgram": false
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "totalStaff": 2,
    "qualifiesForProgram": false
  }
```

### Example 2: Check for discount eligibility

The example determines if a store offers discounts that are either high percentage (>15%) or for specific popular categories.

```javascript
db.stores.aggregate([
  { $match: {"_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f"} },
  {
    $project: {
      _id: 1,
      name: 1,
      hasAttractiveDealOptions: {
        $or: [
          { $gt: [{ $max: "$promotionEvents.discounts.discountPercentage" }, 15] },
          { $in: ["Bath Accessories", "$promotionEvents.discounts.categoryName"] },
          { $in: ["Mattress Toppers", "$promotionEvents.discounts.categoryName"] }
        ]
      }
    }
  }
])
```

The query checks if the store has either high discount percentages or deals on popular categories.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "hasAttractiveDealOptions": true
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
