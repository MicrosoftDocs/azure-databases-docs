---
title: $maxDistance (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $maxDistance operator specifies the maximum distance that can exist between two points in a geospatial query.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 02/12/2025
---

# $maxDistance (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$maxDistance` operator is used in geospatial queries to specify the maximum distance (in meters) that can exist between two points. It's commonly used with `$near` to find locations within a certain radius.

## Syntax

The syntax for the `$maxDistance` operator is as follows:

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

| Parameter | Type | Description |
|-----------|------|-------------|
| `location field` | Field | The field containing the geospatial data |
| `coordinates` | Array | An array of [longitude, latitude] specifying the center point |
| `$maxDistance` | Number | Maximum distance in meters from the center point |

## Example

Using the `stores` collection, let's find all stores within 10 Km of the "VanArsdel Picture Frame Store":

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-141.9922, 16.8331]  // VanArsdel Picture Frame Store location
      },
      $maxDistance: 10000  // 10 kilometers in meters
    }
  }
},
{
  name: 1,
  location: 1
})
```

This query returns stores like:
- First Up Consultants Microphone Bazaar
- Fabrikam Car Accessory Outlet and other stores within the 10 Km radius.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]