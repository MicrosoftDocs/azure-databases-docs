---
title: $geoWithin (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $geoWithin operator selects documents whose location field is completely within a specified geometry.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $geoWithin (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$geoWithin` operator selects documents whose location field falls completely within a specified geometry. This operator supports various shape operators including `$box`, `$polygon`, `$center`, and `$geometry`.

## Syntax

The syntax for the `$geoWithin` operator varies based on the shape being used:

```javascript
// Using $box
{
  <location field>: {
    $geoWithin: {
      $box: [ [ <bottom left coordinates> ], [ <upper right coordinates> ] ]
    }
  }
}

// Using $center
{
  <location field>: {
    $geoWithin: {
      $center: [ [ <x>, <y> ], <radius> ]
    }
  }
}

// Using $geometry
{
  <location field>: {
    $geoWithin: {
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
| `location field` | Field | The field containing the location coordinates |
| `$box` | Array | Two sets of coordinates defining opposite corners of a box |
| `$center` | Array | Center point coordinates and radius in degrees |
| `$geometry` | Object | GeoJSON object defining the boundary |

## Examples

First, ensure you have a 2dsphere index:

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### Example 1: Using $box
Find stores within a rectangular area around the home entertainment store:

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $box: [
        [65.0, 65.0],    // Bottom left corner
        [75.0, 75.0]     // Top right corner
      ]
    }
  }
}, {
  name: 1,
  location: 1
})
```

This query will return stores including "Proseware, Inc. | Home Entertainment Hub" (located at 70.1272, 69.7296).

### Example 2: Using $center
Find stores within a circular radius of Wide World Importers:

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $center: [
        [-82.5543, -65.105],  // Center point (Wide World Importers location)
        5                     // Radius in degrees
      ]
    }
  }
}, {
  name: 1,
  location: 1
})
```

### Example 3: Using $geometry
Find stores within a polygon area:

```javascript
db.stores.find({
  'location': {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-85.0, -70.0],
          [-85.0, -60.0],
          [-75.0, -60.0],
          [-75.0, -70.0],
          [-85.0, -70.0]
        ]]
      }
    }
  }
}, {
  name: 1,
  location: 1
})
```

To analyze the results more thoroughly:

```javascript
db.stores.aggregate([
  {
    $match: {
      'location': {
        $geoWithin: {
          $geometry: {
            type: "Polygon",
            coordinates: [[
              [-85.0, -70.0],
              [-85.0, -60.0],
              [-75.0, -60.0],
              [-75.0, -70.0],
              [-85.0, -70.0]
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

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
