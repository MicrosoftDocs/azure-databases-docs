---
title: $nearSphere (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $nearSphere operator returns documents whose location fields are near a specified point on a sphere, sorted by distance on a spherical surface.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $nearSphere (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$nearSphere` operator returns documents with location fields near a specified point on a sphere, calculating distances using spherical geometry. This is more accurate for Earth-based calculations than `$near`.

## Syntax

```javascript
{
  <location field>: {
    $nearSphere: {
      $geometry: {
        type: "Point",
        coordinates: [<longitude>, <latitude>]
      },
      $maxDistance: <distance in meters>,
      $minDistance: <distance in meters>
    }
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `location field` | Field | The field containing the GeoJSON Point |
| `$geometry` | Object | GeoJSON Point object specifying the center point |
| `$maxDistance` | Number | Optional. Maximum distance in meters on a spherical surface |
| `$minDistance` | Number | Optional. Minimum distance in meters on a spherical surface |

## Examples

Create the required '2dsphere' index:

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### Example 1: Basic Spherical Search
Find stores near "VanArsdel Picture Frame Store" (-141.9922, 16.8331):

```javascript
db.stores.find({
  'location': {
    $nearSphere: {
      $geometry: {
        type: "Point",
        coordinates: [-141.9922, 16.8331]
      }
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 2: With Maximum Distance
Find stores within 20 KM of "Fabrikam Car Accessory Outlet" (-38.4071, -47.2548):

```javascript
db.stores.find({
  'location': {
    $nearSphere: {
      $geometry: {
        type: "Point",
        coordinates: [-38.4071, -47.2548]
      },
      $maxDistance: 20000  // 20 KM in meters
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 3: Complex Distance Analysis
Find and analyze stores between 20 and 100 Kms from Fourth Coffee Turntable Boutique (65.3765, -44.8674):

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [65.3765, -44.8674]
      },
      distanceField: "sphericalDistance",
      minDistance: 20000,     // 20 KM in meters
      maxDistance: 100000,    // 100 KM in meters
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      location: 1,
      distanceKm: { $divide: ["$sphericalDistance", 1000] },
      _id: 0
    }
  }
])
```

Key differences between `$nearSphere` and `$near`:
*  Uses spherical geometry for distance calculations
* More accurate for Earth-based distances
* Better for applications requiring precise global distance calculations

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
