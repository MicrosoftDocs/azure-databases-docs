---
title: $trunc Usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $trunc operator truncates a number to a specified decimal place.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $trunc

The `$trunc` operator is used to truncate a number to a specified decimal place. This operator is particularly useful in scenarios where you need to limit the precision of numerical data, such as financial calculations, reporting, or data normalization.

## Syntax

```javascript
{ $trunc: [ <number>, <place> ] }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<number>`** | The number to truncate. |
| **`<place>`** | The decimal place to truncate to. A positive value truncates to the right of the decimal point, and a negative value truncates to the left of the decimal point. |

## Example(s)

### Truncate Latitude

This example demonstrates how to use the `$trunc` operator to truncate the latitude value in the `location` field to 2 decimal places.

```javascript
db.collection.aggregate([
  {
    $project: {
      truncatedLat: { $trunc: ["$location.lat", 2] }
    }
  }
])
```

This truncates the lat value to two decimal places:
```json
[
  { "_id": 1, "location": { "lat": 37.774929 }, "truncatedLat": 37.77 },
  { "_id": 2, "location": { "lat": 40.712776 }, "truncatedLat": 40.71 }
]
```

### Truncate Sales

In this example, we truncate the `fullSales` value in the `sales` field to the nearest integer.

```javascript
db.collection.aggregate([
  {
    $project: {
      truncatedSales: { $trunc: ["$sales.fullSales", 0] }
    }
  }
])
```

This truncates fullSales to the nearest whole number by removing the decimal portion:
```json
[
  { "_id": 3, "sales": { "fullSales": 1234.56 }, "truncatedSales": 1234 },
  { "_id": 4, "sales": { "fullSales": 9876.99 }, "truncatedSales": 9876 }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]