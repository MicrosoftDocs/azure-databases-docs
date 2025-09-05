---
title: $polygon
titleSuffix: Overview of the $polygon operator in Azure Cosmos DB for MongoDB (vCore)
description: The $polygon operator defines a polygon for geospatial queries, allowing you to find locations within an irregular shape.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/04/2025
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

### Example 1 - Search within a polygon

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

The first two results returned by this query are:

```json
[
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
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]

