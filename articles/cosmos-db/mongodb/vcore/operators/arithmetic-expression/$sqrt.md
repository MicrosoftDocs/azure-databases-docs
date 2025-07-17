---
title: $sqrt usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $sqrt operator returns the square root of a number.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $sqrt

The `$sqrt` operator is used to return the square root of a specified number. It is commonly used in aggregation pipelines to perform mathematical calculations on numeric fields within documents.

## Syntax

```javascript
{ $sqrt: <expression> }
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`<expression>`**| Any valid expression that resolves to a number. |

## Example(s)

### Example 1: Calculate the square root of a specific sales value

The following example demonstrates how to calculate the square root of the `fullSales` value within a document.

```javascript
db.collection.aggregate([
  {
    $project: {
      name: 1,
      fullSales: 1,
      sqrtFullSales: { $sqrt: "$sales.fullSales" }
    }
  }
])
```

This output includes the original fullSales value and its square root:
```json
[
  { "_id": 1, "name": "Store A", "sales": { "fullSales": 100 }, "sqrtFullSales": 10 },
  { "_id": 2, "name": "Store B", "sales": { "fullSales": 225 }, "sqrtFullSales": 15 },
  { "_id": 3, "name": "Store C", "sales": { "fullSales": 400 }, "sqrtFullSales": 20 }
]
```

### Example 2: Calculate the square root of total sales by category

This example shows how to calculate the square root of the `totalSales` for each sales category.

```javascript
db.collection.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  },
  {
    $project: {
      name: 1,
      categoryName: "$sales.salesByCategory.categoryName",
      totalSales: "$sales.salesByCategory.totalSales",
      sqrtTotalSales: { $sqrt: "$sales.salesByCategory.totalSales" }
    }
  }
])
```

This output calculates the square root of the totalSales for each sales category:
```json
[
  {
    "_id": 4,
    "name": "Electronics Store",
    "categoryName": "Laptops",
    "totalSales": 144,
    "sqrtTotalSales": 12
  },
  {
    "_id": 5,
    "name": "Fashion Outlet",
    "categoryName": "Shoes",
    "totalSales": 81,
    "sqrtTotalSales": 9
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]