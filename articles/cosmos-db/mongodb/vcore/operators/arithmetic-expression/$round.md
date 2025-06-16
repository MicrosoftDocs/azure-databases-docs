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

The `$round` operator is used to round a number to a specified decimal place. It's useful in aggregations where numerical precision is important, such as financial calculations or statistical analysis.

## Syntax

```javascript
{ $round: [ <number>, <place> ] }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<number>`** | The number to be rounded. |
| **`<place>`** | The decimal place to which the number should be rounded. |

## Example

### Round the latitude and longitude values

```javascript
db.collection.aggregate([
  {
    $project: {
      roundedLat: { $round: ["$location.lat", 1] },
      roundedLon: { $round: ["$location.lon", 1] }
    }
  }
])
```

This rounds the latitude and longitude values to one decimal place for better readability:
```json
[
  { "_id": 1, "location": { "lat": 37.774929, "lon": -122.419416 }, "roundedLat": 37.8, "roundedLon": -122.4 },
  { "_id": 2, "location": { "lat": 40.712776, "lon": -74.005974 }, "roundedLat": 40.7, "roundedLon": -74.0 }
]
```

### Round the total sales to the nearest thousand

```javascript
db.collection.aggregate([
  {
    $project: {
      roundedSales: { $round: ["$sales.fullSales", -3] }
    }
  }
])
```

This rounds total sales to the nearest thousand, which is useful for financial reporting:
```json
[
  { "_id": 3, "sales": { "fullSales": 25400 }, "roundedSales": 25000 },
  { "_id": 4, "sales": { "fullSales": 127500 }, "roundedSales": 128000 }
]
```

### Round the discount percentages to the nearest integer

```javascript
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

This rounds discount percentages to the nearest whole number, which is helpful for display and pricing adjustments:
```json
[
  {
    "_id": 5,
    "eventName": "Black Friday",
    "categoryName": "Electronics",
    "roundedDiscount": 20
  },
  {
    "_id": 6,
    "eventName": "Holiday Sale",
    "categoryName": "Clothing",
    "roundedDiscount": 15
  }
]
```


## Related content
[!INCLUDE[Related content](../includes/related-content.md)]