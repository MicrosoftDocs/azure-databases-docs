---
title: $floor
titleSuffix: Overview of the $floor operator in Azure Cosmos DB for MongoDB (vCore)
description: The $floor operator returns the largest integer less than or equal to the specified number
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/05/2025
---

# $floor

The `$floor` operator returns the largest integer less than or equal to the specified number.

## Syntax

```javascript
{
  $floor: <number>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<number>`** | Any valid expression that resolves to a number. |

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

### Example 1 - Calculate the floor of total sales and discounts

To calculate the floor of the average sales volume for a given store and the floor of sales per category, run a query using the $floor operator to return the desired results.

```javascript
db.stores.aggregate([{
        $match: {
            _id: "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"
        }
    },
    {
        $project: {
            name: 1,
            averageSalesFloor: {
                $floor: {
                    $divide: [
                        "$sales.totalSales",
                        {
                            $size: "$sales.salesByCategory"
                        }
                    ]
                }
            },
            categoriesWithFloorSales: {
                $map: {
                    input: "$sales.salesByCategory",
                    as: "category",
                    in: {
                        categoryName: "$$category.categoryName",
                        floorSales: {
                            $floor: "$$category.totalSales"
                        }
                    }
                }
            }
        }
    }
])
```

This query returns the following result:

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "averageSalesFloor": 30372,
    "categoriesWithFloorSales": [
      {
        "categoryName": "Sound Bars",
        "floorSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "floorSales": 45004
      },
      {
        "categoryName": "Game Controllers",
        "floorSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "floorSales": 28946
      },
      {
        "categoryName": "VR Games",
        "floorSales": 32272
      }
    ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]


