---
title: $ceil (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $ceil operator returns the smallest integer greater than or equal to the specified number.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $ceil (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$ceil` operator returns the smallest integer greater than or equal to the specified number.

## Syntax

The syntax for the `$ceil` operator is as follows:

```javascript
{ $ceil: <number> }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a number. If the expression resolves to null or refers to a missing field, $ceil returns null. |

## Example

Let's understand the usage with sample data from the `stores` dataset to calculate the ceiling value of average sales per staff member.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      totalStaff: {
        $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
      },
      ceiledAverageSalesPerStaff: {
        $ceil: {
          $divide: [
            "$sales.totalSales",
            { $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"] }
          ]
        }
      }
    }
  }
])
```

This will produce the following output:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "totalSales": 151864,
  "totalStaff": 39,
  "ceiledAverageSalesPerStaff": 3894
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]