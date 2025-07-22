---
  title: $firstN
  titleSuffix: Overview of the $firstN operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $firstN operator sorts documents on one or more fields specified by the query and returns the first N document matching the filtering criteria
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $firstN

The `$firstN` operator returns the first N values in a group according to the group's sorting order. If no sorting order is specified, the order is undefined.

## Syntax

```javascript
{
    $firstN: {
        input: [listOfFields],
        sortBy: {
            <fieldName>: <sortOrder>
        },
        n: <numDocumentsToReturn>
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`listOfFields`** | The list of fields to be returned for the first N documents in the result set|
| **`fieldName`** | The field to use for sorting the result set|
| **`sortOrder`** | 1 or -1. 1 implies sorting in ascending order of the value of the field while -1 implies sorting in descending order of the values of the field|
| **`n`** | The number of documents to return from the top of the sorted result set |

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

### Example 1: Get first three stores by total sales

To get the top three stores by total sales, run a query to sort all documents in descending order of sales.totalSales and return the first three documents from the sorted result set. 

```javascript
db.stores.aggregate([{
        $sort: {
            "sales.totalSales": -1
        }
    },
    {
        $group: {
            _id: null,
            topThreeStores: {
                $firstN: {
                    n: 3,
                    input: {
                        storeId: "$_id",
                        storeName: "$name",
                        totalSales: "$sales.totalSales"
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
        "_id": null,
        "topThreeStores": [
            {
                "storeId": "27d12c50-ef9b-4a1e-981f-2eb46bf68c70",
                "storeName": "Boulder Innovations | Electronics Closet - West Freddy",
                "totalSales": 404106
            },
            {
                "storeId": "ffe155dd-caa2-4ac1-8ec9-0342241a84a3",
                "storeName": "Lakeshore Retail | Electronics Stop - Vicentastad",
                "totalSales": 399426
            },
            {
                "storeId": "cba62761-10f8-4379-9eea-a9006c667927",
                "storeName": "Fabrikam, Inc. | Electronics Nook - East Verlashire",
                "totalSales": 374845
            }
        ]
    }
]
```

### Example 2: Get first two categories per store

To retrieve the first two categories by total sales within each store, run a query to sort all documents in descending order of sales.totalSales within the scope of each store and return the first two categories from the sorted result set per store.

```javascript
db.stores.aggregate([{
        $unwind: "$sales.salesByCategory"
    },
    {
        $match: {
            "sales.salesByCategory.totalSales": {
                $exists: true
            }
        }
    },
    {
        $sort: {
            "_id": 1,
            "sales.salesByCategory.totalSales": -1
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            categoryCount: {
                $sum: 1
            },
            firstTwoCategories: {
                $firstN: {
                    n: 2,
                    input: {
                        categoryName: "$sales.salesByCategory.categoryName",
                        totalSales: "$sales.salesByCategory.totalSales"
                    }
                }
            }
        }
    },
    {
        $match: {
            categoryCount: {
                $gte: 2
            }
        }
    }
])
```

The first two results returned by this query are:

```json
[
    {
        "_id": "14343900-2a5c-44bf-a52b-9efe63579866",
        "storeName": "Northwind Traders | Home Improvement Closet - West Evanside",
        "categoryCount": 2,
        "firstTwoCategories": [
            {
                "categoryName": "Doors",
                "totalSales": 21108
            },
            {
                "categoryName": "Hardware",
                "totalSales": 14263
            }
        ]
    },
    {
        "_id": "19ea47b8-4fbd-468c-88f6-133ffa517fad",
        "storeName": "Proseware, Inc. | Grocery Bazaar - North Earnest",
        "categoryCount": 2,
        "firstTwoCategories": [
            {
                "categoryName": "Frozen Foods",
                "totalSales": 36967
            },
            {
                "categoryName": "Meat",
                "totalSales": 2724
            }
        ]
    }
]
```

### Example 3: Get first two promotion events per store

To retrieve the two earliest promotion events within each store, run a query to sort promotion events in ascending order of date within the scope of the store and return the first two events from the sorted result set.

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $sort: {
            "_id": 1,
            "promotionEvents.promotionalDates.startDate.Year": 1,
            "promotionEvents.promotionalDates.startDate.Month": 1,
            "promotionEvents.promotionalDates.startDate.Day": 1
        }
    },
    {
        $group: {
            _id: "$_id",
            storeName: {
                $first: "$name"
            },
            eventCount: {
                $sum: 1
            },
            firstTwoEvents: {
                $firstN: {
                    n: 2,
                    input: {
                        eventName: "$promotionEvents.eventName",
                        startYear: "$promotionEvents.promotionalDates.startDate.Year",
                        startMonth: "$promotionEvents.promotionalDates.startDate.Month"
                    }
                }
            }
        }
    },
    {
        $match: {
            eventCount: {
                $gte: 2
            }
        }
    }
])
```

The first two results returned by this query are:

```json
[
    {
        "_id": "34e650dc-df46-49b4-aacb-7365e4fd7103",
        "storeName": "Tailwind Traders | Flooring Bargains - Dexterport",
        "eventCount": 2,
        "firstTwoEvents": [
            {
                "eventName": "Spectacular Savings Showcase",
                "startYear": 2024,
                "startMonth": 6
            },
            {
                "eventName": "Super Saver Celebration",
                "startYear": 2024,
                "startMonth": 9
            }
        ]
    },
    {
        "_id": "22e6367e-8341-415f-9795-118d2b522abf",
        "storeName": "Adatum Corporation | Outdoor Furniture Mart - Port Simone",
        "eventCount": 5,
        "firstTwoEvents": [
            {
                "eventName": "Super Saver Soiree",
                "startYear": 2023,
                "startMonth": 9
            },
            {
                "eventName": "Massive Deal Mania",
                "startYear": 2023,
                "startMonth": 12
            }
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
