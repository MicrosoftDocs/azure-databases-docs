---
title: $box
titleSuffix: Overview of the $box operator in Azure Cosmos DB for MongoDB (vCore)
description: The $box operator defines a rectangular area for geospatial queries using coordinate pairs.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $box

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

| Parameter | Description |
|-----------|-------------|
| `location field`| The field containing the geospatial data |
| `lower_left`| An array of [longitude, latitude] specifying the bottom-left corner |
| `upper_right`| An array of [longitude, latitude] specifying the top-right corner |

## Example

Using the `stores` collection, let's find stores within a rectangular region:

```javascript
db.stores.find(
  {
    location: {
      $geoWithin: {
        $box: [
          [-142.0012, -51.3041],  // Lower left corner
          [123.3403, 70.1272]     // Upper right corner
        ]
      }
    }
  },
  {
    name: 1,
    location: 1
  }
).limit(2)
```

This query returns all stores that fall within the rectangular region defined by these coordinates.

```json
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "location": {
      "lat": 61.3945,
      "lon": -3.6196
    }
  },
  {
    "_id": "44fdb9b9-df83-4492-8f71-b6ef648aa312",
    "name": "Fourth Coffee | Storage Solution Gallery - Port Camilla",
    "location": {
      "lat": 78.3889,
      "lon": 0.6784
    }
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
