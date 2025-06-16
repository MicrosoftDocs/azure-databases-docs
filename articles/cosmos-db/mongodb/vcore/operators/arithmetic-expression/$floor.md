---
title: $floor (arithmetic expression) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $floor operator returns the largest integer less than or equal to the specified number.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $floor (arithmetic expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$floor` operator returns the largest integer less than or equal to the specified number.

## Syntax

The syntax for the `$floor` operator is as follows:

```javascript
{ $floor: <number> }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a number. |

## Example

Let's understand the usage with sample data from the `stores` dataset to calculate floor values of average sales and discounts.

```javascript
db.stores.aggregate([
  { $match: { "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74" } },
  {
    $project: {
      name: 1,
      averageSalesFloor: {
        $floor: {
          $divide: [
            "$sales.totalSales",
            { $size: "$sales.salesByCategory" }
          ]
        }
      },
      categoriesWithFloorSales: {
        $map: {
          input: "$sales.salesByCategory",
          as: "category",
          in: {
            categoryName: "$$category.categoryName",
            floorSales: { $floor: "$$category.totalSales" }
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
  "averageSalesFloor": 30372,
  "categoriesWithFloorSales": [
    {
      "categoryName": "Sound Bars",
      "floorSales": 2120
    },
    {
      "categoryName": "Home Theater Projectors",
      "floorSales": 45004
    },
    {
      "categoryName": "Game Controllers",
      "floorSales": 43522
    },
    {
      "categoryName": "Remote Controls",
      "floorSales": 28946
    },
    {
      "categoryName": "VR Games",
      "floorSales": 32272
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]