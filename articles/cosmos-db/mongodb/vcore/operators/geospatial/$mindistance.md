---
title: $minDistance (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $minDistance operator specifies the minimum distance that must exist between two points in a geospatial query.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $minDistance (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$minDistance` operator is used in geospatial queries to specify the minimum distance (in meters) that must exist between two points. It's useful for finding locations outside a certain radius.

## Syntax

The syntax for the `$minDistance` operator is as follows:

```javascript
{
  <location field>: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [<longitude>, <latitude>]
      },
      $minDistance: <distance in meters>
    }
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `location field` | Field | The field containing the geospatial data |
| `coordinates` | Array | An array of [longitude, latitude] specifying the center point |
| `$minDistance` | Number | Minimum distance in meters from the center point |

## Example

Using the `stores` collection, let's find stores that are at least 500 kilometers away from the Proseware Home Entertainment Hub:

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [69.7296, 70.1272]  // Proseware Home Entertainment Hub location
      },
      $minDistance: 500000  // 500 kilometers in meters
    }
  }
},
{
  name: 1,
  location: 1
})
```

This query will return stores like:
- Fourth Coffee Turntable Boutique
- Wide World Importers Headphone Corner
And other stores beyond the 500km radius.



## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
