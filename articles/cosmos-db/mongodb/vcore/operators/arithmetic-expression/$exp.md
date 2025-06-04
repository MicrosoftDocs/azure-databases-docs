---
title: $exp (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $exp operator raises e to the specified exponent and returns the result.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $exp (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$exp` operator raises Euler's number (e) to the specified exponent and returns the result. The mathematical constant e is approximately equal to 2.71828.

## Syntax

The syntax for the `$exp` operator is as follows:

```javascript
{ $exp: <exponent> }
```

## Parameters

| | Description |
| --- | --- |
| **`<exponent>`** | Any valid expression that resolves to a number. |

## Example

Let's understand the usage with sample data from the `stores` dataset to calculate exponential growth projections for sales.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      currentSales: "$sales.totalSales",
      projectedGrowth: {
        oneYear: {
          $multiply: [
            "$sales.totalSales",
            { $exp: 0.1 } // 10% growth rate
          ]
        },
        twoYears: {
          $multiply: [
            "$sales.totalSales",
            { $exp: 0.2 } // 20% growth rate
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
  "currentSales": 151864,
  "projectedGrowth": {
    "oneYear": 167809.93,
    "twoYears": 185304.95
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]