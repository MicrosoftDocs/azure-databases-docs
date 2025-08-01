---
title: $near
titleSuffix: Overview of the $near operator in Azure Cosmos DB for MongoDB (vCore)
description: The $near operator returns documents with location fields that are near a specified point, sorted by distance.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $near

The `$near` operator returns documents whose location field is near a specified point, sorted by distance. It requires a '2dsphere' index and returns documents from nearest to farthest.

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

| Parameter | Description |
|-----------|-------------|
| `location field` | The field containing the GeoJSON Point |
| `$geometry` | GeoJSON Point object specifying the center point |
| `$maxDistance` | Optional. Maximum distance in meters from the center point |
| `$minDistance` | Optional. Minimum distance in meters from the center point |

## Prerequisite

For better performance, start with creating the required `2dsphere` index.

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

## Examples

### Example 1: Basic Proximity Search

The example demonstrates operator usage to find the two closest stores to a specific geographic point (70.1272, 69.7296) using geospatial search.

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
}).limit(2)
```

The query searches the stores collection for locations closest to the given point and returns them in ascending order of distance. It's used for "finding nearest locations" functionality in applications like store locators or delivery services.

```json
{
   "_id": "3882eb86-5dd6-4701-9640-f670ccb67859",
   "name": "Fourth Coffee | DJ Equipment Stop - Schuppestad",
   "location": { "lat": 69.4923, "lon": 70.1851 }
 },
 {
   "_id": "bbec6d3e-1666-45b4-8803-8b7ef8544845",
   "name": "First Up Consultants | Baby Products Bargains - South Keenan",
   "location": { "lat": 69.2158, "lon": 70.3328 }
 }
```

### Example 2: Using Both Min and Max Distance

The aggregation query finds stores within a specific distance range from a point [70.3328, 69.2158] and calculates their distances in kilometers.

```javascript
db.stores.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [70.3328, 69.2158]
      },
      distanceField: "distance",
      minDistance: 20,
      maxDistance: 200,
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
  },
  { $limit: 2 }
])
```

The query searches in a "donut-shaped" search area - finding stores that are at least 20 meters away but no more than 200 meters from the specified point, perfect for scenarios like "find stores in nearby cities but not in the immediate area.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
