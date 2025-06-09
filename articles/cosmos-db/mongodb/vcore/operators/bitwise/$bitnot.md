---
title: $bitNot (bitwise expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $bitNot operator performs a bitwise NOT operation on integer values and returns the result as an integer.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $bitNot (bitwise expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bitNot` operator performs a bitwise NOT operation on integer values. It inverts all the bits of the operand, turning 1s into 0s and 0s into 1s. The result is the bitwise complement of the input value.

## Syntax

The syntax for the `$bitNot` operator is as follows:

```javascript
{
  $bitNot: <expression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`expression`** | An expression that evaluates to an integer. The `$bitNot` operator performs a bitwise NOT operation on this value. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
  "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
  "location": {
    "lat": -29.1866,
    "lon": -112.7858
  },
  "staff": {
    "totalStaff": {
      "fullTime": 14,
      "partTime": 8
    }
  },
  "sales": {
    "totalSales": 83865,
    "salesByCategory": [
      {
        "categoryName": "Lavalier Microphones",
        "totalSales": 44174
      },
      {
        "categoryName": "Wireless Microphones",
        "totalSales": 39691
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Incredible Savings Showcase",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 29
        }
      },
      "discounts": [
        {
          "categoryName": "Condenser Microphones",
          "discountPercentage": 20
        },
        {
          "categoryName": "Microphone Stands",
          "discountPercentage": 17
        }
      ]
    }
  ]
}
```

### Example 1: Basic bitwise NOT operation

Perform a bitwise NOT operation on staff numbers to create inverted flags.

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  {
    $project: {
      name: 1,
      fullTimeStaff: "$staff.totalStaff.fullTime",
      partTimeStaff: "$staff.totalStaff.partTime",
      invertedFullTime: {
        $bitNot: "$staff.totalStaff.fullTime"
      },
      invertedPartTime: {
        $bitNot: "$staff.totalStaff.partTime"
      }
    }
  }
])
```

This will produce the following output:

```json
[
  {
    _id: '26afb024-53c7-4e94-988c-5eede72277d5',
    name: 'First Up Consultants | Microphone Bazaar - South Lexusland',
    fullTimeStaff: 14,
    partTimeStaff: 8,
    invertedFullTime: -15,
    invertedPartTime: -9
  }
]
```

The bitwise NOT of 14 results in -15, and the bitwise NOT of 8 results in -9. This is due to two's complement representation where ~n = -(n+1).

### Example 2: Using $bitNot with Discount Percentages

Apply bitwise NOT operations on discount percentages.

```javascript
db.stores.aggregate([
  { $match: {"_id": "26afb024-53c7-4e94-988c-5eede72277d5"} },
  { $unwind: "$promotionEvents" },
  { $match: {"promotionEvents.eventName": "Incredible Savings Showcase"} },
  { $unwind: "$promotionEvents.discounts" },
  {
    $project: {
      name: 1,
      eventName: "$promotionEvents.eventName",
      categoryName: "$promotionEvents.discounts.categoryName",
      discountPercentage: "$promotionEvents.discounts.discountPercentage",
      invertedDiscount: {
        $bitNot: "$promotionEvents.discounts.discountPercentage"
      }
    }
  }
])
```

This will produce the following output:

```json
[
  {
    _id: '26afb024-53c7-4e94-988c-5eede72277d5',
    name: 'First Up Consultants | Microphone Bazaar - South Lexusland',
    eventName: 'Incredible Savings Showcase',
    categoryName: 'Condenser Microphones',
    discountPercentage: 20,
    invertedDiscount: -21
  },
  {
    _id: '26afb024-53c7-4e94-988c-5eede72277d5',
    name: 'First Up Consultants | Microphone Bazaar - South Lexusland',
    eventName: 'Incredible Savings Showcase',
    categoryName: 'Microphone Stands',
    discountPercentage: 17,
    invertedDiscount: -18
  }
]
```

The bitwise NOT operation inverts all bits: 20 becomes -21 and 17 becomes -18.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]