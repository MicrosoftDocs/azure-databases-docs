---
  title: $bitXor
  titleSuffix: Overview of the $bitXor operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $bitXor operator performs a bitwise XOR operation on integer values.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $bitXor

The `$bitXor` operator performs a bitwise exclusive OR (XOR) operation on integer values. The XOR operation returns 1 for each bit position where the corresponding bits of the operands are different, and 0 where they're the same.

## Syntax

```javascript
{
  $bitXor: [ <expression1>, <expression2>, ... ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression1, expression2, ...`** | Expressions that resolve to integer values. The operator performs XOR operations on these values in sequence. |

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

### Example 1: Basic XOR operation

This query uses an aggregation pipeline to calculate between full-time and part-time staff counts for a specific store. The resulting document contains the store details along with a computed field. The XOR operation between 19 (binary: 10011) and 20 (binary: 10100) results in 7 (binary: 00111).

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      fullTimeStaff: "$staff.totalStaff.fullTime",
      partTimeStaff: "$staff.totalStaff.partTime",
      staffXor: {
        $bitXor: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
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
    "staffXor": 7
  }
]
```

### Example 2: XOR with Multiple Values

The aggregation pipeline computes the bitwise XOR of all discount percentages for the `Discount Delight Days` event of a specific store. The resulting document represents the bitwise XOR calculation of all discount percentages for the `Discount Delight Days` event.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  { $unwind: "$promotionEvents" },
  { $match: { "promotionEvents.eventName": "Discount Delight Days" } },
  { $unwind: "$promotionEvents.discounts" },
  {
    $group: {
      _id: "$_id",
      name: { $first: "$name" },
      eventName: { $first: "$promotionEvents.eventName" },
      discountPercentages: { $push: "$promotionEvents.discounts.discountPercentage" }
    }
  },
  {
    $project: {
      name: 1,
      eventName: 1,
      discountPercentages: 1,
      xorResult: {
        $reduce: {
          input: {
            $map: {
              input: "$discountPercentages",
              as: "val",
              in: { $toLong: "$$val" }
            }
          },
          initialValue: { $toLong: 0 },
          in: { $bitXor: ["$$value", "$$this"] }
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
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "eventName": "Discount Delight Days",
    "discountPercentages": [22, 23, 10, 10, 9, 24],
    "xorResult": { "$numberLong": "16" }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
