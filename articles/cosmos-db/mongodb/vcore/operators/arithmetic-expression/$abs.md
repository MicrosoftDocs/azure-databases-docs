---
title: $abs (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $abs operator returns the absolute value of a number.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $abs (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$abs` operator returns the absolute value of a number. It removes any negative sign from a number, making it positive.

## Syntax

The syntax for the `$abs` operator is as follows:

```javascript
{ $abs: <number> }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a number. If the expression resolves to null or refers to a missing field, $abs returns null. |

## Example

Let's understand the usage with sample data from the `stores` dataset.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      "salesByCategory": {
        $map: {
          input: "$sales.salesByCategory",
          as: "category",
          in: {
            categoryName: "$$category.categoryName",
            totalSales: "$$category.totalSales",
            differenceFromAverage: {
              $abs: { 
                $subtract: [
                  "$$category.totalSales",
                  { $avg: "$sales.salesByCategory.totalSales" }
                ]
              }
            }
          }
        }
      }
    }
  }
])
```

This will produce output showing the absolute difference between each category's sales and the average sales:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "salesByCategory": [
    {
      "categoryName": "Sound Bars",
      "totalSales": 2120,
      "differenceFromAverage": 28252.8
    },
    {
      "categoryName": "Home Theater Projectors",
      "totalSales": 45004,
      "differenceFromAverage": 14631.2
    },
    {
      "categoryName": "Game Controllers",
      "totalSales": 43522,
      "differenceFromAverage": 13149.2
    },
    {
      "categoryName": "Remote Controls",
      "totalSales": 28946,
      "differenceFromAverage": 1426.8
    },
    {
      "categoryName": "VR Games",
      "totalSales": 32272,
      "differenceFromAverage": 1899.2
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]