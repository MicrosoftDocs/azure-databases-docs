---
title: $log (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $log operator calculates the logarithm of a number in the specified base.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $log (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$log` operator calculates the logarithm of a number in the specified base.

## Syntax

The syntax for the `$log` operator is as follows:

```javascript
{ $log: [ <number>, <base> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a positive number. |
| **`<base>`** | Any valid expression that resolves to a positive number to be used as the logarithm base. |

## Example

Let's understand the usage with sample data from the `stores` dataset to calculate sales metrics using different logarithmic bases.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      categoryAnalysis: {
        $map: {
          input: "$sales.salesByCategory",
          as: "category",
          in: {
            categoryName: "$$category.categoryName",
            sales: "$$category.totalSales",
            logBase2: { $log: ["$$category.totalSales", 2] },
            logBase10: { $log: ["$$category.totalSales", 10] }
          }
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
  "categoryAnalysis": [
    {
      "categoryName": "Sound Bars",
      "sales": 2120,
      "logBase2": 11.051,
      "logBase10": 3.326
    },
    {
      "categoryName": "Home Theater Projectors",
      "sales": 45004,
      "logBase2": 15.458,
      "logBase10": 4.653
    },
    {
      "categoryName": "Game Controllers",
      "sales": 43522,
      "logBase2": 15.410,
      "logBase10": 4.639
    },
    {
      "categoryName": "Remote Controls",
      "sales": 28946,
      "logBase2": 14.822,
      "logBase10": 4.462
    },
    {
      "categoryName": "VR Games",
      "sales": 32272,
      "logBase2": 14.977,
      "logBase10": 4.509
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]