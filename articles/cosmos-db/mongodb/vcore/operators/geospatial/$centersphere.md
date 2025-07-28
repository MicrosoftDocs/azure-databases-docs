---
title: $centerSphere
titleSuffix: Overview of the $centerSphere operator in Azure Cosmos DB for MongoDB (vCore)
description: The $centerSphere operator specifies a circle using spherical geometry for $geoWithin queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $centerSphere

The `$centerSphere` operator specifies a circle using spherical geometry for `$geoWithin` queries. This operator is useful for geographic calculations that need to account for Earth's spherical shape.

## Syntax

```javascript
{
  $geoWithin: {
    $centerSphere: [ [ <x>, <y> ], <radius in radians> ]
  }
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<x>` | The longitude of the circle's center point |
| `<y>` | The latitude of the circle's center point |
| `<radius in radians>` | The radius of the sphere in radians (divide distance in kilometers by 6371 to convert to radians) |

## Example

Let's find all stores within approximately 1,000 kilometers (radius ≈ 0.157 radians) of the Wide World Importers Headphone Corner store location. This query can help identify nearby stores for regional marketing campaigns or supply chain optimization.

```javascript
// Convert 1000km to radians: 1000/6371 ≈ 0.157
db.stores.find(
  {
    "location": {
      $geoWithin: {
        $centerSphere: [[-82.5543, -65.105], 0.157]
      }
    }
  },
  {
    _id: 0,
    name: 1,
    location: 1,
    city: 1
  }
).limit(2)
```

The query returns the nearest stores from Wide World Importers Headphone Corner location.

```json
  {
    "name": "Fourth Coffee | Electronics Bazaar - O'Keefeburgh",
    "location": { "lat": -64.5856, "lon": -115.5241 },
    "city": "O'Keefeburgh"
  },
  {
    "name": "Boulder Innovations | Footwear Outlet - West Sybleberg",
    "location": { "lat": -72.73, "lon": -60.2306 },
    "city": "West Sybleberg"
  }
```

> [!IMPORTANT]
> The `$centerSphere` operator calculates distances using spherical geometry, making it more accurate for Earth-based calculations than `$center`.
>
> The radius must be specified in radians.
>
> Coordinates should be specified in the order: [longitude, latitude].
>
> If the geographic buffer extends beyond a UTM zone or crosses the international dateline, the results may be inaccurate or unpredictable.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
