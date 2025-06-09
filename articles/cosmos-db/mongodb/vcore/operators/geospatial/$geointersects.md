---
title: $geoIntersects (geospatial operator) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $geoIntersects operator selects documents whose location field intersects with a specified GeoJSON object.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $geoIntersects (geospatial operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$geoIntersects` operator selects documents whose location field intersects with a specified GeoJSON object. This operator is useful when you want to find stores that intersect with a specific geographical area.

## Syntax

The syntax for the `$geoIntersects` operator is as follows:

```javascript
{
  <location field>: {
    $geoIntersects: {
      $geometry: {
        type: <GeoJSON type>,
        coordinates: <coordinates>
      }
    }
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `location field` | Field | The field containing the GeoJSON object |
| `type` | String | The GeoJSON object type (for example, "Polygon", "MultiPolygon") |
| `coordinates` | Array | The coordinates defining the GeoJSON object |

## Example

First, let's create a 2dsphere index for the location field:

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

Now, let's find stores that intersect with a specific polygon area using the `stores` collection. This polygon encompasses several store locations from our dataset:

```javascript
db.stores.find({
  'location': {
    $geoIntersects: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-150.0, 50.0],    // Northwest corner
          [-150.0, 70.0],    // Northeast corner
          [-130.0, 70.0],    // Southeast corner
          [-130.0, 50.0],    // Southwest corner
          [-150.0, 50.0]     // Back to start to close polygon
        ]]
      }
    }
  }
}, {
  name: 1,
  "location": 1
})
```

This query returns stores like:
- "First Up Consultants | Bed and Bath Center - South Amir" (located at 60.7954, -142.0012)

To demonstrate with actual data points, here's a query that finds all stores within this region:

```javascript
// First, let's see what stores we found
db.stores.aggregate([
  {
    $match: {
      'location': {
        $geoIntersects: {
          $geometry: {
            type: "Polygon",
            coordinates: [[
              [-150.0, 50.0],
              [-150.0, 70.0],
              [-130.0, 70.0],
              [-130.0, 50.0],
              [-150.0, 50.0]
            ]]
          }
        }
      }
    }
  },
  {
    $project: {
      name: 1,
      location: 1,
      _id: 0
    }
  }
])
```

The query returns stores whose locations intersect with the specified polygon area in Alaska/Northern Canada region. This is useful for:
- Finding stores within a specific geographical boundary
- Identifying service coverage areas
- Planning delivery routes


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
