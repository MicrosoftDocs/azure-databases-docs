---
title: $near (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $near operator returns documents with location fields that are near a specified point, sorted by distance.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $near (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$near` operator returns documents whose location field is near a specified point, sorted by distance. It requires a 2dsphere index and returns documents from nearest to farthest.

## Syntax

```javascript
{
  <location field>: {
    $near: {
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
| `$maxDistance` | Number | Optional. Maximum distance in meters from the center point |
| `$minDistance` | Number | Optional. Minimum distance in meters from the center point |

## Examples

Create the required 2dsphere index:

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### Example 1: Basic Proximity Search
Find stores near the Proseware Home Entertainment Hub location (70.1272, 69.7296), sorted by distance:

```javascript
db.stores.find({
  'location': {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [69.7296, 70.1272]  // [longitude, latitude]
      }
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 2: Using Maximum Distance
Find stores within 10 Km of First Up Consultants Microphone Bazaar (-112.7858, -29.1866):

```javascript
db.stores.find({
  'location': {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-112.7858, -29.1866]
      },
      $maxDistance: 10000  // 10 kilometers in meters
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 3: Using Both Min and Max Distance
Find stores between 10 and 50 Kms from Wide World Importers (-82.5543, -65.105):

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [-82.5543, -65.105]
      },
      distanceField: "distance",
      minDistance: 10000,    // 10 Km in meters
      maxDistance: 50000,    // 50 Km in meters,
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      location: 1,
      distanceKm: { $divide: ["$distance", 1000] },
      _id: 0
    }
  }
])
```

This returns stores with their distances from the specified point, such as:
* Distance to nearby stores in kilometers
* Only stores within the specified distance range
* Sorted from nearest to farthest

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]