---
title: $bitOr (bitwise expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $bitOr operator performs a bitwise OR operation on integer values and returns the result as an integer.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $bitOr (bitwise expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bitOr` operator performs a bitwise OR operation on integer values. It compares each bit of the first operand to the corresponding bit of the second operand. If either bit is 1, the corresponding result bit is set to 1. If both bits are 0, the corresponding result bit is set to 0.

## Syntax

The syntax for the `$bitOr` operator is as follows:

```javascript
{
  $bitOr: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| | Description |
| --- | --- |
| **`expression1, expression2, ...`** | Expressions that evaluate to integers. The `$bitOr` operator performs a bitwise OR operation on all provided expressions. |

## Example

Let's understand the usage with sample json from `stores` dataset.

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

Perform a bitwise OR operation on staff numbers to combine permission flags.

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

This will produce the following output:

```json
[
  {
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    fullTimeStaff: 3,
    partTimeStaff: 2,
    combinedStaffFlag: 3
  }
]
```

The bitwise OR of 3 (011 in binary) and 2 (010 in binary) equals 3 (011 in binary).

### Example 2: Using $bitOr with sales data

Apply bitwise OR operations on sales figures to create combined flags.

```javascript
db.stores.aggregate([
  { $match: {"_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66"} },
  { $unwind: "$sales.salesByCategory" },
  {
    $project: {
      name: 1,
      categoryName: "$sales.salesByCategory.categoryName",
      totalSales: "$sales.salesByCategory.totalSales",
      // Combine lower 8 bits of sales with a base flag (15 = 00001111)
      salesFlag: {
        $bitOr: [
          { $toInt: { $mod: ["$sales.salesByCategory.totalSales", 256] } },
          15
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
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    categoryName: 'Phone Mounts',
    totalSales: 8911,
    salesFlag: 207
  },
  {
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    categoryName: 'Dash Cameras',
    totalSales: 22300,
    salesFlag: 31
  }
]
```

### Example 3: Multiple value bitwise OR with discount percentages

Perform bitwise OR operation on multiple discount values.

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

This will produce the following output:

```json
[
  {
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    eventName: 'Super Saver Spectacular',
    discountFlags: [
      {
        categoryName: 'Car Chargers',
        discountPercentage: 7,
        combinedFlag: 7
      },
      {
        categoryName: 'Dash Cameras',
        discountPercentage: 11,
        combinedFlag: 11
      }
    ]
  }
]
```

The operation combines discount percentages with staff numbers using bitwise OR: 7|3|2 = 7 and 11|3|2 = 11.

### Example 4: Creating Permission Flags

Use bitwise OR to create permission flags by combining different access levels.

```javascript
db.stores.aggregate([
  { $match: {"_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66"} },
  {
    $project: {
      name: 1,
      // Create permission flags: 1=read, 2=write, 4=execute
      readPermission: 1,
      writePermission: 2,
      executePermission: 4,
      fullPermissions: {
        $bitOr: [1, 2, 4]
      },
      staffBasedPermissions: {
        $bitOr: [
          "$staff.totalStaff.fullTime",
          "$staff.totalStaff.partTime",
          8
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
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    fullPermissions: 7,
    staffBasedPermissions: 11
  }
]
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]