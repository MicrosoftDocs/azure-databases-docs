---
title: $or
titleSuffix: Overview of the $or operator in Azure Cosmos DB for MongoDB (vCore)
description: The $or operator joins query clauses with a logical OR and returns documents that match at least one of the specified conditions.
author: suvishodcitus
ms.author: suvishod
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/12/2025
---

# $or

The `$or` operator performs a logical OR operation on an array of expressions and retrieves documents that satisfy at least one of the specified conditions.

## Syntax

```javascript
{
    $or: [{
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
| `expression` | An array of expressions, where at least one must be true for a document to be included |

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

### Example 1: Basic OR operation

To find stores with more than 15 full-time staff or more than 20 part-time staff, run a query using the $or operator on both the conditions. Then, project only the name and staff fields from the stores in the result set.

```javascript
db.stores.find({
    $or: [{
        "staff.employeeCount.fullTime": {
            $gt: 15
        }
    }, {
        "staff.employeeCount.partTime": {
            $gt: 20
        }
    }]
}, {
    "name": 1,
    "staff": 1
})
```

The first two results returned by this query are:

```json
[
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "name": "First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort",
        "staff": {
            "employeeCount": {
                "fullTime": 20,
                "partTime": 18
            }
        }
    },
    {
        "_id": "e88f0096-4299-4944-9788-695c40786d97",
        "name": "Adatum Corporation | Handbag Shoppe - Lucienneberg",
        "staff": {
            "employeeCount": {
                "fullTime": 19,
                "partTime": 2
            }
        }
    }
]
```

### Example 2: Complex OR with multiple conditions and arrays

To find stores with more than 25 staff, and have promotional events for either Game Controllers, Sound Bars or Home Theater Projectors, first run a query with $or and $and operators on the specific conditions. Then project only the name, staff and promotionEvents fields from the stores in the result set.

```javascript
db.stores.find({
    $or: [{
        "sales.salesByCategory.categoryName": {
            $in: ["Game Controllers", "Sound Bars", "Home Theater Projectors"]
        }
    }, {
        $and: [{
            "staff.totalStaff.fullTime": {
                $gt: 10
            }
        }, {
            "staff.totalStaff.partTime": {
                $gt: 15
            }
        }]
    }, {
        "promotionEvents": {
            $elemMatch: {
                "eventName": "Super Sale Spectacular",
                "discounts.discountPercentage": {
                    $gt: 15
                }
            }
        }
    }]
}, {
    "name": 1,
    "staff": 1,
    "promotionEvents": 1
})
```

The first result returned by this query is:

```json
[
    {
        "_id": "83218150-9b41-49aa-98fe-8663fa8ee022",
        "name": "Trey Research | Home Entertainment Market - New Baby",
        "staff": {
            "employeeCount": {
                "fullTime": 20,
                "partTime": 3
            }
        },
        "promotionEvents": [
            {
                "eventName": "Super Saver Bash",
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
                        "categoryName": "Game Controllers",
                        "discountPercentage": 12
                    },
                    {
                        "categoryName": "Blu-ray Players",
                        "discountPercentage": 22
                    },
                    {
                        "categoryName": "Projector Mounts",
                        "discountPercentage": 5
                    },
                    {
                        "categoryName": "Home Theater Systems",
                        "discountPercentage": 25
                    },
                    {
                        "categoryName": "Game Accessories",
                        "discountPercentage": 9
                    },
                    {
                        "categoryName": "Projector Cases",
                        "discountPercentage": 15
                    }
                ]
            }
        ]
    }
]
```

## Performance Considerations

   - Each condition in the `$or` array is evaluated independently
   - Use indexes when possible for better performance
   - Consider the order of conditions for optimal execution
   - Use `$in` instead of `$or` for multiple equality checks on the same field
   - Keep the number of `$or` conditions reasonable


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
