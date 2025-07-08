---
title: $center (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $center operator specifies a circle using legacy coordinate pairs for $geoWithin queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $center (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$center` operator specifies a circle using legacy coordinate pairs to be used in `$geoWithin` queries. It defines a circle for a geospatial query on a flat, Euclidean plane.

## Syntax

The syntax for the `$center` operator is as follows:

```javascript
{
  $geoWithin: {
    $center: [ [ <x>, <y> ], <radius> ]
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `<x>` | number | The x-coordinate of the circle's center point |
| `<y>` | number | The y-coordinate of the circle's center point |
| `<radius>` | number | The radius of the circle in the same units as the coordinates |

## Example

Let's find all stores within a 50-degree radius of a central point using our stores dataset. This query can help identify stores that are within a certain distance of a specific location.

```javascript
db.stores.find({
  "location": {
    $geoWithin: {
      $center: [[-112.7858, -29.1866], 50]
    }
  }
})
```

This query will return stores like:

```json
{
  "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
  "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele",
  "location": {
    "lat": -47.2548,
    "lon": -38.4071
  },
  // ... other fields
}
```

The query searches for stores within a 50-degree radius of the First Up Consultants Microphone Bazaar location, which could be useful for analyzing market coverage or planning delivery routes.

> [!Important]
> The `$center` operator works on a flat, Euclidean plane.
> 
> For more accurate Earth-like spherical calculations, use `$centerSphere` instead.
> 
> The radius is specified in the same units as the coordinate system being used.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
