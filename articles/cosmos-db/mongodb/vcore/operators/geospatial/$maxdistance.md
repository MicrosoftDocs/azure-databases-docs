---
title: $maxDistance
titleSuffix: Overview of the $maxDistance operator in Azure Cosmos DB for MongoDB (vCore)
description: The $maxDistance operator specifies the maximum distance that can exist between two points in a geospatial query.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $maxDistance

The `$maxDistance` operator is used in geospatial queries to specify the maximum distance (in meters) that can exist between two points. It pairs well with `$near` for radius-based location searches.

## Syntax

```javascript
{
  <location field>: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [<longitude>, <latitude>]
      },
      $maxDistance: <distance in meters>
    }
  }
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `location field` | The field containing the geospatial data |
| `coordinates` | An array of [longitude, latitude] specifying the center point |
| `$maxDistance`| Maximum distance in meters from the center point |

## Example

Using the `stores` collection, let's find all stores within 10Km of the Point coordinate.

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-77.9951,-62.7339]
      },
      $maxDistance: 10000  // 10 kilometers in meters
    }
  }
},
{
  name: 1,
  location: 1
}).limit(2)
```

The query returns only one store that falls within 10Km of the coordinate provided.

```json
{
   "_id": "66fd4cdd-ffc3-44b6-81d9-6d5e9c1f7f9a",
   "name": "Trey Research | Health Food Center - North Michelle",
   "location": { "lat": -77.9951, "lon": -62.7339 }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
