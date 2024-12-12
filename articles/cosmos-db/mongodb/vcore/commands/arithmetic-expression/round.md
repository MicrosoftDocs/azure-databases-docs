---
title: $round usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $round operator rounds a number to a specified decimal place.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/27/2024
---

# $round

The `$round` operator in MongoDB is used to round a number to a specified decimal place. It is particularly useful in aggregations where numerical precision is important, such as financial calculations or statistical analysis.

## Syntax

```json
{ $round: [ <number>, <place> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<number>`** | The number to be rounded. |
| **`<place>`** | The decimal place to which the number should be rounded. |

## Example(s)

### Round the latitude and longitude values

```json
db.collection.aggregate([
  {
    $project: {
      roundedLat: { $round: ["$location.lat", 1] },
      roundedLon: { $round: ["$location.lon", 1] }
    }
  }
])
```

### Round the total sales to the nearest thousand

```json
db.collection.aggregate([
  {
    $project: {
      roundedSales: { $round: ["$sales.fullSales", -3] }
    }
  }
])
```

### Round the discount percentages to the nearest integer

```json
db.collection.aggregate([
  {
    $unwind: "$promotionEvents"
  },
  {
    $unwind: "$promotionEvents.discounts"
  },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      categoryName: "$promotionEvents.discounts.categoryName",
      roundedDiscount: { $round: ["$promotionEvents.discounts.discountPercentage", 0] }
    }
  }
])
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](migration-options.md).
- Get started by [creating an account](../quickstart-portal.md).