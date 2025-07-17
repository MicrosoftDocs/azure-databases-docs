---
  title: $bottomN
  titleSuffix: Overview of the $tbottomN operator
  description: The $bottomN operator returns the last N documents from the result sorted by one or more fields
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $bottomN

The $bottomN operator sorts documents on one more fields specified by the query and returns the last N documents matching the filtering criteria.

## Syntax

The syntax for the `$bottomN` operator is as follows:

```javascript
{
    $bottomN: {
        output: [listOfFields],
        sortBy: {
            <fieldName>: < sortOrder >
        },
        n: < numDocumentsToReturn >
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`listOfFields`** | The list of fields to be returned for the last document in the result set|
| **`fieldName`** | The field to use for sorting the result set|
| **`sortOrder`** | 1 or -1. 1 implies sorting in ascending order of the value of the field while -1 implies sorting in descending order of the values of the field|
| **`n`** | The number of documents to return from the bottom of the sorted result set |

## Example

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

### Example 1: Find the bottom two stores by total sales

To determine the two stores in the Boulder Innovations company with the lowest sales, run a query to retrieve stores within the "Boulder Innovations" company, sort the resulting documents in descending order of total sales and return the last two documents from the sorted result set.

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": ["Boulder Innovations"]
        }
    }
}, {
    "$group": {
        "_id": "$company",
        "bottomSales": {
            "$bottomN": {
                "output": ["$company", "$sales"],
                "sortBy": {
                    "sales.revenue": -1
                },
                "n": 2
            }
        }
    }
}])
```

This query produces the following output:

```json
[
  {
    "_id": "Boulder Innovations",
    "bottomSales": [
        [
            "Boulder Innovations",
            {
                "salesByCategory": [
                    {
                        "categoryName": "Yoga Mats",
                        "totalSales": 119
                    }
                ],
                "revenue": 119
            }
        ],
        [
            "Boulder Innovations",
            {
                "salesByCategory": [
                    {
                        "categoryName": "Portable Turntables",
                        "totalSales": 162
                    }
                ],
                "revenue": 162
            }
        ]
    ]
}
]
```

### Example 2: Find the bottom two categories by total sales within each store
To determine the two lowest performing categories by total sales within each store, run a query to retrieve documents with at least two sales categories, sort the categories in descending order of total sales and finally return the bottom two categories per store.

```javascript
db.stores.aggregate([{
    $unwind: "$sales.salesByCategory"
}, {
    $match: {
        "sales.salesByCategory.totalSales": {
            $exists: true
        }
    }
}, {
    $group: {
        _id: "$_id",
        storeName: {
            $first: "$name"
        },
        categoryCount: {
            $sum: 1
        },
        bottomTwoCategories: {
            $bottomN: {
                n: 2,
                sortBy: {
                    "sales.salesByCategory.totalSales": -1
                },
                output: {
                    categoryName: "$sales.salesByCategory.categoryName",
                    totalSales: "$sales.sale"
                }
            }
        }
    }
}, {
    $match: {
        categoryCount: {
            $gte: 2
        }
    }
}])
```

The first two results returned by this query are:

```json
[
    {
        "_id": "86e9df70-b5ae-4078-856e-d5b8c6e3ecb7",
        "storeName": "Boulder Innovations | Health Food Boutique - Clementinabury",
        "categoryCount": 2,
        "bottomTwoCategories": [
            {
                "categoryName": "Herbal Teas",
                "totalSales": null
            },
            {
                "categoryName": "Protein Bars",
                "totalSales": null
            }
        ]
    },
    {
        "_id": "9bb70b69-2f26-41cf-90c9-2c42c7023dad",
        "storeName": "Lakeshore Retail | Home Office Corner - New Bartholome",
        "categoryCount": 2,
        "bottomTwoCategories": [
            {
                "categoryName": "Desk Lamps",
                "totalSales": null
            },
            {
                "categoryName": "Office Accessories",
                "totalSales": null
            }
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
