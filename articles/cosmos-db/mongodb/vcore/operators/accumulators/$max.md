---
title: $max
titleSuffix: Overview of the $max operator in Azure Cosmos DB for MongoDB (vCore)
description: The $max operator returns the maximum value from a set of input values.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $max

The `$max` operator returns the maximum value of a set of input values. The max operator is particularly useful in identifying the highest value in a dataset, such as maximum sales, discounts, and other numerical comparisons.

## Syntax
```javascript
$max: <expression>
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`<expression>`** | Any valid expression that resolves to a value. The `$max` operator evaluates this expression to determine the maximum value. |

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

### Example 1: Calculate the highest sales by category

To calculate the highest sales within each category, first run a query to group all documents by sales category. Then run a $max query to retrieve the highest sales within each category across all stores.

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $group: {
            _id: "$sales.salesByCategory.categoryName",
            maxSales: {
                $max: "$sales.salesByCategory.totalSales"
            }
        }
    }
])
```

The first five results returned by this query are:

```json
[
    {
        "_id": "Christmas Trees",
        "maxSales": 49697
    },
    {
        "_id": "Nuts",
        "maxSales": 48020
    },
    {
        "_id": "Camping Tables",
        "maxSales": 48568
    },
    {
        "_id": "Music Theory Books",
        "maxSales": 46133
    },
    {
        "_id": "Fortified Wine",
        "maxSales": 49912
    }
]
```

### Example 2: Using `$max` in `$bucket`

To retrieve the highest sales within buckets of sales boundaries:

```javascript
db.stores.aggregate([{
    $bucket: {
        groupBy: "$sales.totalSales",
        boundaries: [0, 1000, 5000, 10000],
        default: "Other",
        output: {
            maxSales: {
                $max: "$sales.totalSales"
            }
        }
    }
}])
```

This query would return the following document.

```json
[
    {
        "_id": 1000,
        "maxSales": 4996
    },
    {
        "_id": "Other",
        "maxSales": 404106
    },
    {
        "_id": 0,
        "maxSales": 995
    },
    {
        "_id": 5000,
        "maxSales": 9999
    }
]
```

### Example 3: Using `$max` in `$setWindowFields`

To get the highest discount for laptops in 2023, first run a query to unwind just promotion events and filter on the chosen category. Then partition the resulting documents by company and calculate the highest discount percentage within each resulting partition. 

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    // Filter only Laptops category and events in 2023
    {
        $match: {
            "promotionEvents.promotionalDates.startDate.Year": 2023,
            "promotionEvents.discounts.categoryName": "Laptops"
        }
    },
    // Use $setWindowFields to calculate average discount by city
    {
        $setWindowFields: {
            partitionBy: "$company",
            output: {
                maxDiscount: {
                    $max: "$promotionEvents.discounts.discountPercentage",
                    window: {
                        documents: ["unbounded", "unbounded"]
                    }
                }
            }
        }
    },
    // Group by city to return one result per city
    {
        $group: {
            _id: "$company",
            maxDiscount: {
                $first: "$maxDiscount"
            }
        }
    }
])
```

The first five results returned by this query are:

```json
[
    {
        "_id": "Boulder Innovations",
        "maxDiscount": 24
    },
    {
        "_id": "VanArsdel, Ltd.",
        "maxDiscount": 24
    },
    {
        "_id": "Proseware, Inc.",
        "maxDiscount": 24
    },
    {
        "_id": "Fabrikam, Inc.",
        "maxDiscount": 23
    },
    {
        "_id": "Contoso, Ltd.",
        "maxDiscount": 24
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
