---
title: $divide (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $divide operator divides two numbers and returns the quotient.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $divide (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$divide` operator divides two numbers and returns the quotient. The operator returns an error if the divisor is zero.

## Syntax

The syntax for the `$divide` operator is as follows:

```javascript
{ $divide: [ <dividend>, <divisor> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<dividend>`** | Any valid expression that resolves to a number to be divided. |
| **`<divisor>`** | Any valid expression that resolves to a nonzero number to divide by. |

## Example

Let's understand the usage with sample data from the `stores` dataset to calculate the average sales per staff member and percentage of full-time staff.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      averageSalesPerStaff: {
        $divide: [
          "$sales.totalSales",
          { $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"] }
        ]
      },
      fullTimeStaffPercentage: {
        $multiply: [{
          $divide: [
            "$staff.totalStaff.fullTime",
            { $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"] }
          ]
        }, 100]
      }
    }
  }
])
```

This produces the following output:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "averageSalesPerStaff": 3893.95,
  "fullTimeStaffPercentage": 48.72
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]