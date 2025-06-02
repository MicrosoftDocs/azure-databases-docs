---
title: $add (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $add operator adds numbers together or adds numbers and dates.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $add (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$add` operator adds numbers together or adds numbers and dates. When adding numbers and dates, the numbers are interpreted as milliseconds.

## Syntax

The syntax for the `$add` operator is as follows:

```javascript
{ $add: [ <expression1>, <expression2>, ... ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<expression>`** | Any valid expression that resolves to numbers or dates. The expressions can be any combination of numbers and dates. |

## Example

Let's understand the usage with sample data from the dataset to calculate total staff (full-time plus part-time) and add a projection of next year's staff with 2 another employees.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      currentTotalStaff: {
        $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
      },
      projectedNextYearStaff: {
        $add: [
          "$staff.totalStaff.fullTime",
          "$staff.totalStaff.partTime",
          2
        ]
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
  "currentTotalStaff": 39,
  "projectedNextYearStaff": 41
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]