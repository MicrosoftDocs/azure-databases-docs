---
title: $sqrt usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $sqrt operator returns the square root of a number.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/27/2024
---

# $sqrt

The `$sqrt` operator in MongoDB is used to return the square root of a specified number. It is commonly used in aggregation pipelines to perform mathematical calculations on numeric fields within documents.

## Syntax

```shell
{ $sqrt: <expression> }
```

## Parameters  

| | Description |
| --- | --- |
| **`<expression>`**| Any valid expression that resolves to a number. |

## Example(s)

### Example 1: Calculate the square root of a specific sales value

The following example demonstrates how to calculate the square root of the `fullSales` value within a document.

```json
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

### Example 2: Calculate the square root of total sales by category

This example shows how to calculate the square root of the `totalSales` for each sales category.

```json
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

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]