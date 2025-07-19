---
title: $maxN
titleSuffix: Overview of the $maxN operator
description: Retrieves the top N values based on a specified filtering criteria
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $maxN

The `$maxN` operator is used to retrieve the top N values for a field based on a specified filtering critieria. 

## Syntax

```javascript
$maxN: {
    input: < field or expression > ,
    n: < number of values to retrieve >
}
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`input`** | Specifies the field or expression to evaluate for maximum values. |
| **`n`** | Specifies the number of maximum values to retrieve. Must be a positive integer. |

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

### Example 1: Retrieve top 2 sales categories

The following query retrieves the top 2 sales categories with the highest sales volume:

```javascript
db.stores.aggregate([{
        $project: {
            topSalesCategories: {
                $maxN: {
                    input: "$sales.salesByCategory",
                    n: 2
                }
            }
        }
    },
    {
        $limit: 4
    }
])
```

This query returns the following results:

```json
[
    {
        "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
        "topSalesCategories": [
            {
                "categoryName": "Photo Albums",
                "totalSales": 17676
            }
        ]
    },
    {
        "_id": "b5c9f932-4efa-49fd-86ba-b35624d80d95",
        "topSalesCategories": [
            {
                "categoryName": "Rulers",
                "totalSales": 35346
            }
        ]
    },
    {
        "_id": "5c882644-f86f-433f-b45e-88e2015825df",
        "topSalesCategories": [
            {
                "categoryName": "iPads",
                "totalSales": 39014
            },
            {
                "categoryName": "Unlocked Phones",
                "totalSales": 49969
            }
        ]
    },
    {
        "_id": "cba62761-10f8-4379-9eea-a9006c667927",
        "topSalesCategories": [
            {
                "categoryName": "Ultrabooks",
                "totalSales": 41654
            },
            {
                "categoryName": "Toner Refill Kits",
                "totalSales": 10726
            }
        ]
    }
]
```

### Example 2: Using `$maxN` in `$setWindowFields`

To retrieve the top N discounts for "Laptops" in 2023 per city:

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    // Match only "Laptops" discounts from year 2023
    {
        $match: {
            "promotionEvents.discounts.categoryName": "Laptops",
            "promotionEvents.promotionalDates.startDate.Year": 2023
        }
    },
    // Group by city and collect top N max discounts
    {
        $group: {
            _id: "$city",
            topDiscounts: {
                $maxN: {
                    input: "$promotionEvents.discounts.discountPercentage",
                    n: 3 // Change this to however many top discounts you want
                }
            }
        }
    }
])
```

The first three results returned by this query are:

```json
[
    {
        "_id": "Lake Margareteland",
        "topDiscounts": [
            18
        ]
    },
    {
        "_id": "Horacetown",
        "topDiscounts": [
            13
        ]
    },
    {
        "_id": "D'Amoreside",
        "topDiscounts": [
            9
        ]
    }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
