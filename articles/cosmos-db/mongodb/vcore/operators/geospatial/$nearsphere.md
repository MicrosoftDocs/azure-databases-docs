---
title: $nearSphere
titleSuffix: Overview of the $nearSphere operator in Azure Cosmos DB for MongoDB (vCore)
description: The $nearSphere operator returns documents whose location fields are near a specified point on a sphere, sorted by distance on a spherical surface.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $nearSphere

The `$nearSphere` operator returns documents with location fields near a specified point on a sphere, calculating distances using spherical geometry. The operator is more accurate for Earth-based calculations than `$near`.

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

| Parameter | Description |
|-----------|-------------|
| `location field` | The field containing the GeoJSON Point |
| `$geometry` | GeoJSON Point object specifying the center point |
| `$maxDistance` | Optional. Maximum distance in meters on a spherical surface |
| `$minDistance` | Optional. Minimum distance in meters on a spherical surface |

## Examples

For better performance, start with creating the required `2dsphere` index.

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### Example 1: Basic Spherical Search

The example uses the `$nearSphere` operator to find documents in the stores collection that are closest to the Point (-141.9922, 16.8331) on a spherical (Earth-like) surface.

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
}).limit(2)
```

The query returns stores sorted closest to farthest from defined Point.

```json
  {
    "_id": "643b2756-c22d-4063-9777-0945b9926346",
    "name": "Contoso, Ltd. | Outdoor Furniture Corner - Pagacfort",
    "location": {
      "type": "Point",
      "coordinates": [152.1353, -89.8688]
    }
  },
  {
    "_id": "daa71e60-75d4-4e03-8b45-9df59af0811f",
    "name": "First Up Consultants | Handbag Corner - South Salvatore",
    "location": {
      "type": "Point",
      "coordinates": [150.2305, -89.8431]
    }
  }
```

### Example 2: Complex Distance Analysis

The example helps to find and analyze stores between 20 meter and 200 meter from Point (65.3765, -44.8674).

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [65.3765, -44.8674]
      },
      distanceField: "sphericalDistance",
      minDistance: 20,
      maxDistance: 200,
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
  },
  {
    $limit: 2
  }
])
```

The query searches in a "donut-shaped" search area - finding stores that are at least 20 meters away but no more than 200 meters from the specified point, perfect for scenarios like "find stores in nearby cities but not in the immediate area.

Key difference between the operator `$nearSphere` and `$near`.

* Former uses spherical geometry for distance calculations.
* Former is more accurate for Earth-based distance calculations.
* Former is better for applications requiring precise global distance calculations

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
