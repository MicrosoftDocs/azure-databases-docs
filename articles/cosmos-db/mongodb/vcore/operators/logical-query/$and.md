---
title: $and
titleSuffix: Overview of the $and operator
description: The $and operator joins multiple query clauses and returns documents that match all specified conditions.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $and

The `$and` operator performs a logical AND operation on an array of expressions and retrieves documents that satisfy all the expressions.

## Syntax

```javascript
{
    $and: [{
        < expression1 >
    }, {
        < expression2 >
    }, ..., {
        < expressionN >
    }]
}
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `expression` | An array of expressions that must all be true for a document to be included in the results |

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

### Example 1: Basic AND operation

To find store that satisfies having more than 10 full time staff and fewer than 15 part time staff, run a query with the $and operator with both the conditions specified. Lastly, project only the name and staff fields in the resulting documents.

```javascript
db.stores.find({
    $and: [{
        "staff.employeeCount.fullTime": {
            $gt: 10
        }
    }, {
        "staff.employeeCount.partTime": {
            $lt: 15
        }
    }]
}, {
    "name": 1,
    "staff": 1
})
```

The first three results returned by this query are:

```json
[
    {
        "_id": "e60c807b-d31c-4903-befb-5d608f260ba3",
        "name": "Wide World Importers | Appliance Emporium - Craigfort",
        "staff": {
            "totalStaff": {
                "fullTime": 11,
                "partTime": 8
            }
        }
    },
    {
        "_id": "70032165-fded-47b4-84a3-8d9c18a4d1e7",
        "name": "Northwind Traders | Picture Frame Bazaar - Lake Joesph",
        "staff": {
            "totalStaff": {
                "fullTime": 14,
                "partTime": 0
            }
        }
    },
    {
        "_id": "dda2a7d2-6984-40cc-bbea-4cbfbc06d8a3",
        "name": "Contoso, Ltd. | Home Improvement Closet - Jaskolskiview",
        "staff": {
            "totalStaff": {
                "fullTime": 16,
                "partTime": 8
            }
        }
    }
]

```

### Example 2: Complex AND operation

To find stores with sales over $100,000 with both "Game Controllers" and "Home Theater Projectors" in their sales categories, run a query to combine all three conditions using the $and operator. Lastly, project only the name and sales fields from the stores in the result set.

```javascript
db.stores.find({
    $and: [{
        "sales.totalSales": {
            $gt: 100000
        }
    }, {
        "sales.salesByCategory.categoryName": "Game Controllers"
    }, {
        "sales.salesByCategory.categoryName": "Home Theater Projectors"
    }]
}, {
    "name": 1,
    "sales": 1
})
```

The first two results returned by this query are:

```json
[
    {
        "_id": "43863d56-645e-4a37-b1d5-a8947312f78d",
        "name": "Fabrikam, Inc. | Home Entertainment Shop - East Justice",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Business Projectors",
                    "totalSales": 42294
                },
                {
                    "categoryName": "Blu-ray Players",
                    "totalSales": 32544
                },
                {
                    "categoryName": "Home Theater Projectors",
                    "totalSales": 14581
                },
                {
                    "categoryName": "Projector Cases",
                    "totalSales": 11074
                },
                {
                    "categoryName": "Game Controllers",
                    "totalSales": 38025
                }
            ],
            "totalSales": 138518
        }
    },
    {
        "_id": "a6a66f47-95a0-40f7-9283-1de7ec1165dd",
        "name": "VanArsdel, Ltd. | Home Entertainment Market - New Sigmundmouth",
        "sales": {
            "salesByCategory": [
                {
                    "categoryName": "Game Controllers",
                    "totalSales": 28627
                },
                {
                    "categoryName": "Home Theater Systems",
                    "totalSales": 7659
                },
                {
                    "categoryName": "Home Theater Projectors",
                    "totalSales": 41420
                },
                {
                    "categoryName": "VR Games",
                    "totalSales": 15060
                },
                {
                    "categoryName": "PC Games",
                    "totalSales": 42499
                },
                {
                    "categoryName": "Nintendo Switch Games",
                    "totalSales": 27581
                }
            ],
            "totalSales": 162846
        }
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
