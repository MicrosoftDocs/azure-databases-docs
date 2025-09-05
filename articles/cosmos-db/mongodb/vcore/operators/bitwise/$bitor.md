---
title: $bitOr
titleSuffix: Overview of the $bitOr operator in Azure Cosmos DB for MongoDB (vCore)
description: The $bitOr operator performs a bitwise OR operation on integer values and returns the result as an integer.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/03/2025
---

# $bitOr

The `$bitOr` operator performs a bitwise OR operation on integer values. It compares each bit of the first operand to the corresponding bit of the second operand. If either bit is 1, the corresponding result bit is set to 1. If both bits are 0, the corresponding result bit is set to 0.

## Syntax

```javascript
{
  $bitOr: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression1, expression2, ...`** | Expressions that evaluate to integers. The `$bitOr` operator performs a bitwise OR operation on all provided expressions. |

## Examples

Consider this sample document from the stores collection.

```json
{
  "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
  "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
  "location": {
    "lat": -47.2548,
    "lon": -38.4071
  },
  "staff": {
    "totalStaff": {
      "fullTime": 3,
      "partTime": 2
    }
  },
  "sales": {
    "totalSales": 31211,
    "salesByCategory": [
      {
        "categoryName": "Phone Mounts",
        "totalSales": 8911
      },
      {
        "categoryName": "Dash Cameras",
        "totalSales": 22300
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Super Saver Spectacular",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 25
        },
        "endDate": {
          "Year": 2024,
          "Month": 4,
          "Day": 1
        }
      },
      "discounts": [
        {
          "categoryName": "Car Chargers",
          "discountPercentage": 7
        },
        {
          "categoryName": "Dash Cameras",
          "discountPercentage": 11
        }
      ]
    }
  ]
}
```

### Example 1: Basic bitwise OR operation

The query performs a bitwise OR operation on the staff values of a specific store document to combine permission flags. The bitwise OR of 3 (011 in binary) and 2 (010 in binary) equals 3 (011 in binary).

```javascript
db.stores.aggregate([
  { $match: {"_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66"} },
  {
    $project: {
      name: 1,
      fullTimeStaff: "$staff.totalStaff.fullTime",
      partTimeStaff: "$staff.totalStaff.partTime",
      combinedStaffFlag: {
        $bitOr: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
      }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
    "fullTimeStaff": 3,
    "partTimeStaff": 2,
    "combinedStaffFlag": 3
  }
]
```

### Example 2: Multiple value bitwise OR with discount percentages

The example aggregation query extracts discount details for a specific promotion event and computes a bitwise flag combining discounts and staff values. The output shows the results of the aggregation query that calculates a combined bitwise flag for each discount in the event `Super Saver Spectacular`. The operation combines discount percentages with staff numbers using bitwise OR: 7|3|2 = 7 and 11|3|2 = 11.

```javascript
db.stores.aggregate([
  { $match: {"_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66"} },
  { $unwind: "$promotionEvents" },
  { $match: {"promotionEvents.eventName": "Super Saver Spectacular"} },
  {
    $project: {
      name: 1,
      eventName: "$promotionEvents.eventName",
      discountFlags: {
        $map: {
          input: "$promotionEvents.discounts",
          as: "discount",
          in: {
            categoryName: "$$discount.categoryName",
            discountPercentage: "$$discount.discountPercentage",
            combinedFlag: {
              $bitOr: [
                "$$discount.discountPercentage",
                "$staff.totalStaff.fullTime",
                "$staff.totalStaff.partTime"
              ]
            }
          }
        }
      }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
    "eventName": "Super Saver Spectacular",
    "discountFlags": [
      {
        "categoryName": "Car Chargers",
        "discountPercentage": 7,
        "combinedFlag": 7
      },
      {
        "categoryName": "Dash Cameras",
        "discountPercentage": 11,
        "combinedFlag": 11
      }
    ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
