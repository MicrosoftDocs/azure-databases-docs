---
title: $box (geospatial) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $box operator defines a rectangular area for geospatial queries using coordinate pairs.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $box (geospatial)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$box` operator defines a rectangular area for geospatial queries using two coordinate pairs. It's useful for finding locations within a rectangular geographical boundary.

## Syntax

The syntax for the `$box` operator is as follows:

```javascript
{
  <location field>: {
    $geoWithin: {
      $box: [
        [<lower_left_longitude>, <lower_left_latitude>],
        [<upper_right_longitude>, <upper_right_latitude>]
      ]
    }
  }
}
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `location field` | Field | The field containing the geospatial data |
| `lower_left` | Array | An array of [longitude, latitude] specifying the bottom-left corner |
| `upper_right` | Array | An array of [longitude, latitude] specifying the top-right corner |

## Example

Using the `stores` collection, let's find stores within a rectangular region:

```javascript
db.stores.find({
  location: {
    $geoWithin: {
      $box: [
        [-142.0012, -51.3041],  // Lower left corner (First Up Consultants location)
        [123.3403, 70.1272]     // Upper right corner (Northwind Traders location)
      ]
    }
  }
},
{
  name: 1,
  location: 1
})
```

This query will return all stores that fall within the rectangular region defined by these coordinates.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]