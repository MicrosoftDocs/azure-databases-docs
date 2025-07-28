---
title: $minDistance
titleSuffix: Overview of the $minDistance operator in Azure Cosmos DB for MongoDB (vCore)
description: The $minDistance operator specifies the minimum distance that must exist between two points in a geospatial query.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $minDistance

The `$minDistance` operator is used in geospatial queries to specify the minimum distance (in meters) that must exist between two points. It's useful for finding locations outside a certain radius.

## Syntax

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

| Parameter | Description |
|-----------|------|-------------|
| `location field` | The field containing the geospatial data |
| `coordinates` | An array of [longitude, latitude] specifying the center point |
| `$minDistance` | Minimum distance in meters from the center point |

## Example

Using the `stores` collection, let's find stores that are at least 500 kilometers away from point coordinate [69.7296, 70.1272].

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
}).limit(2)
```

The query returns the two stores at least 500Km away from the provided coordinates.

```json
 {
   "_id": "9d9d768b-4daf-4126-af15-a963bd3b88aa",
   "name": "First Up Consultants | Perfume Gallery - New Verniceshire",
   "location": { "lat": 36.0762, "lon": 98.7799 }
 },
 {
   "_id": "76b03913-37e3-4779-b3b8-0f654c1ae3e7",
   "name": "Fabrikam, Inc. | Turntable Depot - Schinnershire",
   "location": { "lat": 37.5534, "lon": 81.6805 }
 }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
