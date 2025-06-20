---
  title: $expr (evaluation query)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $expr operator allows the use of aggregation expressions within the query language, enabling complex field comparisons and calculations.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $expr (evaluation query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$expr` operator allows the use of aggregation expressions within the query language, which enables us to compare fields from the same document, perform calculations, and use aggregation operators in find operations. The `$expr` operator is useful for complex field comparisons that can't be achieved with traditional query operators.

## Syntax

The syntax for the `$expr` operator is as follows:

```javascript
{
  $expr: { <aggregation expression> }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<aggregation expression>`** | Any valid aggregation expression that evaluates to a boolean value. The expression includes field comparisons, arithmetic operations, conditional expressions, and other aggregation operators. |

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
      }
    ]
  },
  "storeOpeningDate": ISODate("2024-09-23T13:45:01.480Z"),
  "lastUpdated": ISODate("2025-06-11T11:06:57.922Z"),
  "status": "active",
  "category": "high-volume",
  "priority": 1,
  "reviewDate": ISODate("2025-06-11T11:10:50.276Z")
}
```

### Example 1: Compare full-time and part-time staff

The example retrieves stores with the number of full-time employees greater than part-time employees.

```javascript
db.stores.find({"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  $expr: {
    $gt: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"]
  }
})
```

The query compares two fields within the same document and returns the document if the condition is met (full-time staff count exceeds part-time staff count).

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
      }
    ]
  },
  "storeOpeningDate": ISODate("2024-09-23T13:45:01.480Z"),
  "lastUpdated": ISODate("2025-06-11T11:06:57.922Z"),
  "status": "active",
  "category": "high-volume",
  "priority": 1,
  "reviewDate": ISODate("2025-06-11T11:10:50.276Z")
}
```

### Example 2: Conditional logic with store location

The example demonstrates the conditional logic usage with $expr pulling stores in the southern hemisphere where the staff efficiency ratio (sales per employee) exceeds 2000.

```javascript
db.stores.find({{"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  $expr: {
    $and: [
      { $gte: ["$location.lat", 70.1272] },
      {
        $gt: [
          {
            $divide: [
              "$sales.totalSales",
              { $add: ["$staff.employeeCount.fullTime", "$staff.employeeCount.partTime"] }
            ]
          },
          2000
        ]
      }
    ]
  }
}).limit(1)
```

The query combines location-based filtering with a calculated efficiency metric, demonstrating the power of `$expr` for complex business logic.

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
      }
    ]
  },
  "storeOpeningDate": ISODate("2024-09-23T13:45:01.480Z"),
  "lastUpdated": ISODate("2025-06-11T11:06:57.922Z"),
  "status": "active",
  "category": "high-volume",
  "priority": 1,
  "reviewDate": ISODate("2025-06-11T11:10:50.276Z")
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
