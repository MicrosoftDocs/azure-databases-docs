---
title: $geometry (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $geometry operator specifies a GeoJSON geometry for geospatial queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $geometry (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$geometry` operator specifies a GeoJSON geometry object for geospatial queries. It's used within other geospatial operators to define shapes and points for spatial calculations.

## Syntax

```javascript
{
  $geometry: {
    type: <GeoJSON type>,
    coordinates: <coordinates>
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | String | GeoJSON object type (Point, Polygon, MultiPolygon, etc.) |
| `coordinates` | Array | Coordinates defining the GeoJSON object |

## Examples

Create the required 2dsphere index:

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### Example 1: Point Geometry
Find stores near First Up Consultants Watch Mart (46.2917, -62.6354):

```javascript
db.stores.find({
  'location': {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [46.2917, -62.6354]
      }
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 2: Polygon Geometry
Find stores within a polygon around Wide World Importers Headphone Corner (-82.5543, -65.105):

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-85.0, -67.0],
          [-85.0, -63.0],
          [-80.0, -63.0],
          [-80.0, -67.0],
          [-85.0, -67.0]  // Close the polygon
        ]]
      }
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 3: MultiPolygon Geometry
Find stores in multiple regions:

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $geometry: {
        type: "MultiPolygon",
        coordinates: [
          [[ // First polygon (around Northwind Traders)
            [120.0, -13.0],
            [120.0, -10.0],
            [125.0, -10.0],
            [125.0, -13.0],
            [120.0, -13.0]
          ]],
          [[ // Second polygon (around First Up Consultants)
            [44.0, -64.0],
            [44.0, -61.0],
            [48.0, -61.0],
            [48.0, -64.0],
            [44.0, -64.0]
          ]]
        ]
      }
    }
  }
}, {
  name: 1,
  location: 1
})
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]