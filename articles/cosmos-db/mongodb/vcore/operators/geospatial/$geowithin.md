---
title: $geoWithin
titleSuffix: Overview of the $geoWithin operator in Azure Cosmos DB for MongoDB (vCore)
description: The $geoWithin operator selects documents whose location field is completely within a specified geometry.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $geoWithin

The `$geoWithin` operator selects documents whose location field falls completely within a specified geometry. This operator supports various shape operators including `$box`, `$polygon`, `$center`, and `$geometry`.

## Syntax

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

| Parameter | Description |
|-----------|-------------|
| `location field` | The field containing the location coordinates |
| `$box` | Two sets of coordinates defining opposite corners of a box |
| `$center` | Center point coordinates and radius in degrees |
| `$geometry` | GeoJSON object defining the boundary |

## Examples

For getting better performance, ensure you have a 2dsphere index.

```javascript
db.stores.createIndex({ "location": "2dsphere" })
```

### Example 1: Using $box

The example finds stores that are located within a specific rectangular area on a map, defined by a box (bounding rectangle).

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
}).limit(2)
```

This query returns stores located within box [70.1272, 69.7296].

```json
 {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "location": {
      "lat": 70.1272,
      "lon": 69.7296,
      "address": "123 Entertainment Blvd",
      "city": "East Linwoodbury"
    }
  },
  {
    "_id": "fc286536-cb94-45aa-b975-7040fde04cf7",
    "name": "First Up Consultants | Medical Supply Corner - South Elnoraview",
    "location": {
      "lat": 72.2184,
      "lon": 68.9829
    }
  }
```

### Example 2: Using $center

The example uses a `$geoWithin` operator to find stores within a circular area defined by a center point and a radius.

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
}).limit(2)
```

The query returns the closest two matching stores.

```json
  {
    "_id": "3e962dd0-dffb-49d6-8a96-1d29fa1553d2",
    "name": "Tailwind Traders | Book Center - Lake Marlen",
    "location": { "lat": -85.4034, "lon": -65.9189 }
  },
  {
    "_id": "7e442816-be4c-4919-8f67-d1e9162a511f",
    "name": "Proseware, Inc. | Outdoor Furniture Bargains - North Obieberg",
    "location": { "lat": -84.1013, "lon": -69.5717 }
  }
```

### Example 3: Using $geometry

The query finds up to two stores whose location falls within the defined rectangular polygon.

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
}).limit(2)
```

The query returns two stores physically located inside the specified polygon area.

```json
  {
    "_id": "66fd4cdd-ffc3-44b6-81d9-6d5e9c1f7f9a",
    "name": "Trey Research | Health Food Center - North Michelle",
    "location": { "lat": -77.9951, "lon": -62.7339 }
  },
  {
    "_id": "ea3f775b-f977-4827-ada4-ca7fd8ed0cd4",
    "name": "VanArsdel, Ltd. | Outdoor Equipment Pantry - Port Aleenton",
    "location": { "lat": -76.4516, "lon": -67.2051 }
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
