---
title: $polygon
titleSuffix: Overview of the $polygon operator in Azure Cosmos DB for MongoDB (vCore)
description: The $polygon operator defines a polygon for geospatial queries, allowing you to find locations within an irregular shape.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $polygon

The `$polygon` operator defines a polygon for geospatial queries, allowing you to find locations within an irregular shape. The operator is useful for querying locations within complex geographical boundaries.

## Syntax

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

| Parameter | Description |
|-----------|-------------|
| `location field` | The field containing the geospatial data |
| `coordinates` | An array of coordinate pairs forming the polygon. The first and last points must be identical to close the polygon |

## Example

The query retrieves stores that fall inside a custom polygon region based on the coordinates provided.

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
}).limit(2)
```

The query returns two stores lying within the region.s

```json
{
    "_id": "4a417727-a002-4c80-a01f-bc9526b300a5",
    "name": "Northwind Traders | Bed and Bath Deals - East Duane",
    "location": {
      "type": "Point",
      "coordinates": [-46.1444, -60.9697]
    }
  },
  {
    "_id": "1e27040c-7242-4970-8893-e5738e1bc1ca",
    "name": "Northwind Traders | Seasonal Decoration Bazaar - Cassidyberg",
    "location": {
      "type": "Point",
      "coordinates": [-44.3617, -81.2186]
    }
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
