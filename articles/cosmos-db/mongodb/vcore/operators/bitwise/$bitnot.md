---
title: $bitNot
titleSuffix: Overview of the $bitNot operator in Azure Cosmos DB for MongoDB (vCore)
description: The $bitNot operator performs a bitwise NOT operation on integer values and returns the result as an integer.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/03/2025
---

# $bitNot

The `$bitNot` operator performs a bitwise NOT operation on integer values. It inverts all the bits of the operand, turning 1s into 0s and 0s into 1s. The result is the bitwise complement of the input value.

## Syntax

```javascript
{
  $bitNot: <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | An expression that evaluates to an integer. The `$bitNot` operator performs a bitwise NOT operation on this value. |

## Examples

Consider this sample document from the stores collection.

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

The example aggregation query performs a bitwise inversion on the staff count fields for a specific store document. The inverted values can be used for special permission flags, feature toggles, or bitmask operations. The bitwise NOT of 14 results are -15, and the bitwise NOT of 8 results in -9. The observed result is due to two's complement representation where ~n = -(n+1).

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

This query returns the following result.

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "fullTimeStaff": 14,
    "partTimeStaff": 8,
    "invertedFullTime": -15,
    "invertedPartTime": -9
  }
]
```

### Example 2: Using $bitNot with discount percentages

The example aggregation query extracts and processes discount information for a specific store and applies a bitwise NOT operation on each discount percentage. The bitwise NOT operation inverts all bits: 20 becomes -21 and 17 becomes -18.

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

This query returns the following results:

```json
[
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "eventName": "Incredible Savings Showcase",
    "categoryName": "Microphone Stands",
    "discountPercentage": 17,
    "invertedDiscount": -18
  },
  {
    "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
    "name": "First Up Consultants | Microphone Bazaar - South Lexusland",
    "eventName": "Incredible Savings Showcase",
    "categoryName": "Condenser Microphones",
    "discountPercentage": 20,
    "invertedDiscount": -21
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
