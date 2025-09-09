---
title: $bitAnd
titleSuffix: Overview of the $bitAnd operator in Azure Cosmos DB for MongoDB (vCore)
description: The $bitAnd operator performs a bitwise AND operation on integer values and returns the result as an integer.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/04/2025
---

# $bitAnd

The `$bitAnd` operator performs a `bitwise AND` operation on integer values. It compares each bit of the first operand to the corresponding bit of the second operand. If both bits are 1, the corresponding result bit is set to 1. Otherwise, the corresponding result bit is set to 0.

## Syntax

```javascript
{
  $bitAnd: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression1, expression2, ...`** | Expressions that evaluate to integers. The `$bitAnd` operator performs a bitwise AND operation on all provided expressions. |

## Examples

Consider this sample document from the stores collection.

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
  },
  "promotionEvents": [
    {
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 12,
          "Day": 26
        },
        "endDate": {
          "Year": 2024,
          "Month": 1,
          "Day": 5
        }
      },
      "discounts": [
        {
          "categoryName": "Game Controllers",
          "discountPercentage": 22
        },
        {
          "categoryName": "Home Theater Projectors",
          "discountPercentage": 23
        }
      ]
    }
  ]
}
```

### Example 1: Basic bitwise AND operation

The example aggregation pipeline retrieves staff information for a specific store and computes a `bitwise AND` between the number of full-time and part-time staff to create permission flags.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      fullTimeStaff: "$staff.totalStaff.fullTime",
      partTimeStaff: "$staff.totalStaff.partTime",
      staffPermissionFlag: {
        $bitAnd: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
      }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "fullTimeStaff": 19,
    "partTimeStaff": 20,
    "staffPermissionFlag": 16
  }
]
```

### Example 2: Multiple value `$bitAnd`

The example aggregation query checks bitwise permissions or combined flags based on multiple numeric fields for a single store.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      combinedFlag: {
        $bitAnd: [
          "$staff.totalStaff.fullTime",
          "$staff.totalStaff.partTime",
          255
        ]
      }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "combinedFlag": 16
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
