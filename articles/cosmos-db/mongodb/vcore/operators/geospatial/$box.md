---
title: $box
titleSuffix: Overview of the $box operator in Azure Cosmos DB for MongoDB (vCore)
description: The $box operator defines a rectangular area for geospatial queries using coordinate pairs.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/04/2025
---

# $box

The `$box` operator defines a rectangular area for geospatial queries using two coordinate pairs. It's useful for finding locations within a rectangular geographical boundary.

## Syntax

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

### Example 1 - Find stores within a rectangular region

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

The first two results returned by this query are:

```json
[
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
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]

