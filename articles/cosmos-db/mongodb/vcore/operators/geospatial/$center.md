---
title: $center
titleSuffix: Overview of the $center operator in Azure Cosmos DB for MongoDB (vCore)
description: The $center operator specifies a circle using legacy coordinate pairs for $geoWithin queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $center

The `$center` operator specifies a circle using legacy coordinate pairs to be used in `$geoWithin` queries. It defines a circle for a geospatial query on a flat, Euclidean plane.

## Syntax

```javascript
{
  $geoWithin: {
    $center: [ [ <x>, <y> ], <radius> ]
  }
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<x>` | The x-coordinate of the circle's center point |
| `<y>` | The y-coordinate of the circle's center point |
| `<radius>` | The radius of the circle in the same units as the coordinates |

## Example

Let's find all stores within a 50-degree radius of 'First Up Consultants Microphone Bazaar' using our `stores` dataset.

```javascript
db.stores.find(
  {
    location: {
      $geoWithin: {
        $center: [[-112.7858, -29.1866], 50]
      }
    }
  },
  {
    name: 1,
    city: 1,
    location: 1,
    _id: 0
  }
).limit(2)
```

The query returns stores within 50-degree radius of the First Up Consultants Microphone Bazaar location, which could be useful for analyzing market coverage or planning delivery routes.

```json
  {
    "name": "Contoso, Ltd. | Baby Products Corner - Port Jerrold",
    "location": { "lat": -72.7709, "lon": -24.3031 },
    "city": "Port Jerrold"
  },
  {
    "name": "VanArsdel, Ltd. | Smart Home Closet - Trystanport",
    "location": { "lat": -64.5509, "lon": -28.7144 },
    "city": "Trystanport"
  }
```

> [!IMPORTANT]
> The `$center` operator works on a flat, Euclidean plane.
>
> For more accurate Earth-like spherical calculations, use `$centerSphere` instead.
>
> The radius is specified in the same units as the coordinate system being used.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
