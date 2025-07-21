---
title: $not
titleSuffix: Overview of the $not operator
description: The $not operator performs a logical NOT operation on a specified expression, selecting documents that do not match the expression.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $not

The `$not` operator performs a logical NOT operation on a specified expression and selects documents that do not match the expression.

## Syntax

```javascript
{
    field: {
        $not: {
            < operator - expression >
        }
    }
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `operator-expression` | The expression to negate |

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

### Example 1: Basic NOT operation

To find stores with either less than or more than 5 full time staff, run a query using the $not operator on the fullTime staff count. Then, project only the name and staff fields from the stores in the result set.

```javascript
 db.stores.find({
     "staff.totalStaff.fullTime": {
         $not: {
             $eq: 5
         }
     }
 }, {
     "name": 1,
     "staff": 1
 })
```

The first two results returned by this query are:

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
        "staff": {
            "totalStaff": {
                "fullTime": 9,
                "partTime": 18
            }
        }
    },
    {
        "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
        "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
        "staff": {
            "totalStaff": {
                "fullTime": 7,
                "partTime": 6
            }
        }
    }
]
```

### Example 2: Complex NOT operation

To find stores without promotional events with 20% discounts, run a query with the $not operator on the discountPercentage field. Then project only the name and promotionEvents fields from the stores in the result set.

```javascript
db.stores.find({
    "promotionEvents.discounts.discountPercentage": {
        $not: {
            $eq: 20
        }
    }
}, {
    "name": 1,
    "promotionEvents": 1
})
```

The first document returned by this query is:

```json
[
    {
        "_id": "70032165-fded-47b4-84a3-8d9c18a4d1e7",
        "name": "Northwind Traders | Picture Frame Bazaar - Lake Joesph",
        "promotionEvents": [
            {
                "eventName": "Super Saver Fiesta",
                "promotionalDates": {
                    "startDate": {
                        "Year": 2024,
                        "Month": 9,
                        "Day": 21
                    },
                    "endDate": {
                        "Year": 2024,
                        "Month": 10,
                        "Day": 1
                    }
                },
                "discounts": [
                    {
                        "categoryName": "Picture Hanging Supplies",
                        "discountPercentage": 13
                    },
                    {
                        "categoryName": "Shadow Boxes",
                        "discountPercentage": 9
                    }
                ]
            }
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
