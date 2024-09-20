---
title: $geointersects (geospatial)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $geointersects operator to select documents with geospatial data that intersects with a specified geometry.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/11/2024
---

# $geoIntersects (Geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$geoIntersects` operator is used to select documents with geospatial data that intersects with a specified geometry. This operator is particularly useful for querying documents that contain location data and determining if those locations intersect with a given shape or area. Common use cases include finding all stores, landmarks, or other points of interest within a specified region.

## Syntax

The syntax for the `$geoIntersects` operator is as follows:

```javascript
{
  <field>: {
    $geoIntersects: {
      $geometry: {
        type: <GeoJSON object type>,
        coordinates: <coordinates>
      }
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field in the document that contains the geospatial data. |
| **`$geometry`** | Specifies the GeoJSON object to compare against the geospatial data in the document. |
| **`type`** | The type of GeoJSON object (e.g., `Point`, `Polygon`, `LineString`). |
| **`count`** | The coordinates of the GeoJSON object. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
