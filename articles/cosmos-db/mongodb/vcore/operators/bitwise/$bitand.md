---
title: $bitAnd (bitwise expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $bitAnd operator performs a bitwise AND operation on integer values and returns the result as an integer.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $bitAnd (bitwise expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bitAnd` operator performs a bitwise AND operation on integer values. It compares each bit of the first operand to the corresponding bit of the second operand. If both bits are 1, the corresponding result bit is set to 1. Otherwise, the corresponding result bit is set to 0.

## Syntax

The syntax for the `$bitAnd` operator is as follows:

```javascript
{
  $bitAnd: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`expression1, expression2, ...`** | Expressions that evaluate to integers. The `$bitAnd` operator performs a bitwise AND operation on all provided expressions. |

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

Perform a bitwise AND operation on staff numbers to create permission flags.

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

This will produce the following output:

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    fullTimeStaff: 20,
    partTimeStaff: 19,
    staffPermissionFlag: 16
  }
]
```

The bitwise AND of 19 (10011 in binary) and 20 (10100 in binary) equals 16 (10000 in binary).

### Example 2: Using `$bitAnd` with discount percentages

Apply bitwise AND operations on discount percentages to create combined discount flags.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  { $unwind: "$promotionEvents" },
  { $match: {"promotionEvents.eventName": "Discount Delight Days"} },
  { $unwind: "$promotionEvents.discounts" },
  {
    $project: {
      name: 1,
      eventName: "$promotionEvents.eventName",
      categoryName: "$promotionEvents.discounts.categoryName",
      discountPercentage: "$promotionEvents.discounts.discountPercentage",
      discountFlag: {
        $bitAnd: ["$promotionEvents.discounts.discountPercentage", 31]
      }
    }
  }
])
```

This will produce the following output:

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    eventName: 'Discount Delight Days',
    categoryName: 'Game Controllers',
    discountPercentage: 22,
    discountFlag: 22
  },
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    eventName: 'Discount Delight Days',
    categoryName: 'Home Theater Projectors',
    discountPercentage: 23,
    discountFlag: 23
  },
  .
  .
  .
]
```

The bitwise AND operation with 31 (11111 in binary) extracts the lower 5 bits of each discount percentage.

### Example 3: Multiple value `$bitAnd`

Perform bitwise AND operation on multiple numeric fields.

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

This will produce the following output:

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    combinedFlag: 16
  }
]
```

The operation performs bitwise AND on 19, 20, and 255, resulting in 16.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
