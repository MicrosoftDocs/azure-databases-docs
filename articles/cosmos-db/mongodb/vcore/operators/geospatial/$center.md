---
title: $center
titleSuffix: Overview of the $center operator in Azure Cosmos DB for MongoDB (vCore)
description: The $center operator specifies a circle using legacy coordinate pairs for $geoWithin queries.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 07/25/2025
---

# $center

The `$center` operator specifies a circle using legacy coordinate pairs to be used in `$geoWithin` queries. It defines a circle for a geospatial query on a flat, Euclidean plane.

## Syntax

```javascript
{
  $geoWithin: {
    $center: [ [ <x>, <y> ], <radius> ]
  }
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<x>` | The x-coordinate of the circle's center point |
| `<y>` | The y-coordinate of the circle's center point |
| `<radius>` | The radius of the circle in the same units as the coordinates |

## Examples

Consider this sample document from the stores collection.

```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### Example 1 - Search within a 50-degree radius

Let's find all stores within a 50-degree radius of 'First Up Consultants Microphone Bazaar' using our `stores` dataset. This query retrieves stores within a 50-degree radius of the First Up Consultants Microphone Bazaar location.

```javascript
db.stores.find(
  {
    location: {
      $geoWithin: {
        $center: [[-112.7858, -29.1866], 50]
      }
    }
  },
  {
    name: 1,
    city: 1,
    location: 1,
    _id: 0
  }
).limit(2)
```

The first two results returned by this query are:

```json
[
  {
    "name": "Contoso, Ltd. | Baby Products Corner - Port Jerrold",
    "location": { "lat": -72.7709, "lon": -24.3031 },
    "city": "Port Jerrold"
  },
  {
    "name": "VanArsdel, Ltd. | Smart Home Closet - Trystanport",
    "location": { "lat": -64.5509, "lon": -28.7144 },
    "city": "Trystanport"
  }
]
```

> [!IMPORTANT]
> The `$center` operator works on a flat, Euclidean plane.
>
> For more accurate Earth-like spherical calculations, use `$centerSphere` instead.
>
> The radius is specified in the same units as the coordinate system being used.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]

