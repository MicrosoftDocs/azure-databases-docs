---
title: $geoIntersects
titleSuffix:  Overview of the $geoIntersects operator in Azure Cosmos DB for MongoDB (vCore)
description: The $geoIntersects operator selects documents whose location field intersects with a specified GeoJSON object.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $geoIntersects

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

| Parameter | Description |
|-----------|-------------|
| `location field` | The field containing the GeoJSON object |
| `type` | The GeoJSON object type (for example, "Polygon", "MultiPolygon") |
| `coordinates` | The coordinates defining the GeoJSON object |

## Example

For better performance, start with creating the required 2dsphere index.

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

Now, let's find stores that intersect with a specific polygon area using the `stores` collection. This polygon encompasses several store locations from our dataset.

```javascript
db.stores.find({
  'location': {
    $geoIntersects: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-80.0, -75.0],   // Bottom-left
          [-80.0, -70.0],   // Top-left
          [-55.0, -70.0],   // Top-right
          [-55.0, -75.0],   // Bottom-right
          [-80.0, -75.0]    // Close polygon
        ]]
      }
    }
  }
}, {
  "name": 1,
  "location": 1
}).limit(2)
```

This query returns stores, whose locations intersect with the Polygon contour defined by the coordinates.

```json
  {
    "_id": "6bba7117-d180-4584-b50c-a2f843e9c9ab",
    "name": "Wide World Importers | Craft Supply Mart - Heaneybury",
    "location": { "lat": -64.4843, "lon": -107.7003 },
    "city": "Heaneybury"
  },
  {
    "_id": "2fd37663-e0ff-41d0-9c5a-3aec86285daa",
    "name": "Relecloud | Cleaning Supply Closet - Patiencehaven",
    "location": { "lat": -70.6077, "lon": -105.9901 },
    "city": "Patiencehaven"
  }
```

The operator is useful for use cases like

- Finding stores within a specific geographical boundary
- Identifying service coverage areas
- Planning delivery routes

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
