---
title: $ln (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $ln operator calculates the natural logarithm of a number and returns the result.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $ln (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$ln` operator calculates the natural logarithm (base e) of a number and returns the result.

## Syntax

The syntax for the `$ln` operator is as follows:

```javascript
{ $ln: <number> }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a positive number. |

## Example

Let's understand the usage with sample data from the `stores` dataset to analyze sales growth rates.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      salesGrowthMetrics: {
        $map: {
          input: "$sales.salesByCategory",
          as: "category",
          in: {
            categoryName: "$$category.categoryName",
            salesValue: "$$category.totalSales",
            naturalLog: { $ln: "$$category.totalSales" }
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
  "salesGrowthMetrics": [
    {
      "categoryName": "Sound Bars",
      "salesValue": 2120,
      "naturalLog": 7.659
    },
    {
      "categoryName": "Home Theater Projectors",
      "salesValue": 45004,
      "naturalLog": 10.714
    },
    {
      "categoryName": "Game Controllers",
      "salesValue": 43522,
      "naturalLog": 10.681
    },
    {
      "categoryName": "Remote Controls",
      "salesValue": 28946,
      "naturalLog": 10.273
    },
    {
      "categoryName": "VR Games",
      "salesValue": 32272,
      "naturalLog": 10.382
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]