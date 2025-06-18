---
title: $log10 (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $log10 operator calculates the log base 10 of a number and returns the result.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $log10 (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$log10` operator calculates the logarithm base 10 of a number and returns the result.

## Syntax

The syntax for the `$log10` operator is as follows:

```javascript
{ $log10: <number> }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a positive number. |

## Example

Let's understand the usage with sample data from the `stores` dataset to analyze sales distribution using logarithmic scale.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      salesAnalysis: {
        $map: {
          input: "$sales.salesByCategory",
          as: "category",
          in: {
            categoryName: "$$category.categoryName",
            originalSales: "$$category.totalSales",
            logScale: { $log10: "$$category.totalSales" },
            magnitudeClass: {
              $switch: {
                branches: [
                  { case: { $lt: [{ $log10: "$$category.totalSales" }, 3] }, then: "Low" },
                  { case: { $lt: [{ $log10: "$$category.totalSales" }, 4] }, then: "Medium" },
                  { case: { $lt: [{ $log10: "$$category.totalSales" }, 5] }, then: "High" }
                ],
                default: "Very High"
              }
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
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "salesAnalysis": [
    {
      "categoryName": "Sound Bars",
      "originalSales": 2120,
      "logScale": 3.326,
      "magnitudeClass": "Medium"
    },
    {
      "categoryName": "Home Theater Projectors",
      "originalSales": 45004,
      "logScale": 4.653,
      "magnitudeClass": "High"
    },
    {
      "categoryName": "Game Controllers",
      "originalSales": 43522,
      "logScale": 4.639,
      "magnitudeClass": "High"
    },
    {
      "categoryName": "Remote Controls",
      "originalSales": 28946,
      "logScale": 4.462,
      "magnitudeClass": "High"
    },
    {
      "categoryName": "VR Games",
      "originalSales": 32272,
      "logScale": 4.509,
      "magnitudeClass": "High"
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]