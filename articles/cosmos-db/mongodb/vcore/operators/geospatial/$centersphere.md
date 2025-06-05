---
title: $centerSphere (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $centerSphere operator specifies a circle using spherical geometry for $geoWithin queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $centerSphere (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$centerSphere` operator specifies a circle using spherical geometry for `$geoWithin` queries. This operator is particularly useful for geographic calculations that need to account for Earth's spherical shape.

## Syntax

The syntax for the `$centerSphere` operator is as follows:

```javascript
{
  $geoWithin: {
    $centerSphere: [ [ <x>, <y> ], <radius in radians> ]
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `<x>` | number | The longitude of the circle's center point |
| `<y>` | number | The latitude of the circle's center point |
| `<radius in radians>` | number | The radius of the sphere in radians (divide distance in kilometers by 6371 to convert to radians) |

## Example

Let's find all stores within approximately 1000 kilometers (radius ≈ 0.157 radians) of the Wide World Importers Headphone Corner store location. This query can help identify nearby stores for regional marketing campaigns or supply chain optimization.

```javascript
// Convert 1000km to radians: 1000/6371 ≈ 0.157
db.stores.find({
  "location": {
    $geoWithin: {
      $centerSphere: [[-82.5543, -65.105], 0.157]
    }
  }
})
```

This query will return stores like:

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "location": {
    "lat": -51.3041,
    "lon": -166.0838
  },
  // ... other fields
}
```

## Important Notes

* The `$centerSphere` operator calculates distances using spherical geometry, making it more accurate for Earth-based calculations than `$center`.
* The radius must be specified in radians.
* Coordinates should be specified in the order: [longitude, latitude].
* If the geographic buffer extends beyond a UTM zone or crosses the international dateline, the results may be inaccurate or unpredictable.

## Example with Distance Conversion

Here's an example showing how to find stores within a 500km radius:

```javascript
// Convert 500km to radians: 500/6371 ≈ 0.0785
db.stores.find({
  "location": {
    $geoWithin: {
      $centerSphere: [[-141.9922, 16.8331], 0.0785]
    }
  }
})
```

This query uses the "VanArsdel, Ltd." store location as the center point and searches for stores within approximately 500km.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
