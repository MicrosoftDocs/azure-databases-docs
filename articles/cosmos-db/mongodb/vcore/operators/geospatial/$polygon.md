---
title: $polygon (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $polygon operator defines a polygon for geospatial queries, allowing you to find locations within an irregular shape.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $polygon (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$polygon` operator defines a polygon for geospatial queries, allowing you to find locations within an irregular shape. This is particularly useful for querying locations within complex geographical boundaries.

## Syntax

The syntax for the `$polygon` operator is as follows:

```javascript
{
  <location field>: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [
          [[<longitude1>, <latitude1>], ..., [<longitudeN>, <latitudeN>], [<longitude1>, <latitude1>]]
        ]
      }
    }
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `location field` | Field | The field containing the geospatial data |
| `coordinates` | Array | An array of coordinate pairs forming the polygon. The first and last points must be identical to close the polygon |

## Example

Using the `stores` collection, let's find stores within a triangular region formed by three store locations:

```javascript
db.stores.find({
  location: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [-141.9922, 16.8331],  // VanArsdel Picture Frame Store
          [-112.7858, -29.1866], // First Up Consultants Microphone Bazaar
          [-38.4071, -47.2548],  // Fabrikam Car Accessory Outlet
          [-141.9922, 16.8331]   // Close the polygon by repeating first point
        ]]
      }
    }
  }
},
{
  name: 1,
  location: 1
})
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]