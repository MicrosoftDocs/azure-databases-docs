---
title: $bottomN
titleSuffix: Overview of the $bottomN operator in Azure Cosmos DB for MongoDB vCore
description: The $bottomN operator in Azure Cosmos DB for MongoDB vCore returns the last N documents from the result sorted by one or more fields 
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $bottomN

The `$bottomN` operator sorts documents on one more fields specified by the query and returns the last N documents matching the filtering criteria.

## Syntax

```mongodb
{
  "$bottomN": {"output": [listOfFields], "sortBy": {"<fieldName>": <sortOrder>}, "n": <numDocumentsToReturn>}
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`listOfFields`** | The list of fields to be returned for the last document in the result set|
| **`fieldName`** | The field to use for sorting the result set|
| **`sortOrder`** | 1 or -1. 1 implies sorting in ascending order of the value of the field while -1 implies sorting in descending order of the values of the field|
| **`n`** | The number of documents to return from the bottom of the sorted result set |

## Examples

Consider this sample document from the stores collection in the StoreData database.

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

### Example 1 - Retrieve the last 2 documents in the result set after sorting stores under the Boulder Innovations company in ascending order of total sales 

```mongodb
db.stores.aggregate([{"$match": {"company": { "$in": ["Boulder Innovations"] } } }, {"$group": {"_id": "$company", "bottomSales": {"$bottomN": {"output": ["$company", "$sales"], "sortBy": {"sales.totalSales": 1}, "n": 2} } } }])
```

This query returns the following results:

```json
{
    "_id": "Boulder Innovations",
    "bottomSales": [
        [
            "Boulder Innovations",
            {
                "totalSales": 404106,
                "salesByCategory": [
                    {
                        "categoryName": "iPads",
                        "totalSales": 46592
                    },
                    {
                        "categoryName": "External Hard Drives",
                        "totalSales": 11364
                    },
                    {
                        "categoryName": "Student Laptops",
                        "totalSales": 30481
                    },
                    {
                        "categoryName": "Android Tablets",
                        "totalSales": 48149
                    },
                    {
                        "categoryName": "Desktops",
                        "totalSales": 42726
                    },
                    {
                        "categoryName": "Inkjet Cartridges",
                        "totalSales": 36581
                    },
                    {
                        "categoryName": "2-in-1 Laptops",
                        "totalSales": 26355
                    },
                    {
                        "categoryName": "Phone Mounts",
                        "totalSales": 19886
                    },
                    {
                        "categoryName": "Android Phones",
                        "totalSales": 4532
                    },
                    {
                        "categoryName": "Power Banks",
                        "totalSales": 48347
                    },
                    {
                        "categoryName": "All-in-One Printers",
                        "totalSales": 44346
                    },
                    {
                        "categoryName": "Photo Printers",
                        "totalSales": 44747
                    }
                ]
            }
        ],
        [
            "Boulder Innovations",
            {
                "totalSales": 327029,
                "salesByCategory": [
                    {
                        "categoryName": "Label Printers",
                        "totalSales": 34821
                    },
                    {
                        "categoryName": "Tablet Stands",
                        "totalSales": 22118
                    },
                    {
                        "categoryName": "Windows Tablets",
                        "totalSales": 31942
                    },
                    {
                        "categoryName": "Toner Refill Kits",
                        "totalSales": 37574
                    },
                    {
                        "categoryName": "Prepaid Phones",
                        "totalSales": 34461
                    },
                    {
                        "categoryName": "Android Phones",
                        "totalSales": 39716
                    },
                    {
                        "categoryName": "Screen Protectors",
                        "totalSales": 4487
                    },
                    {
                        "categoryName": "Laser Printers",
                        "totalSales": 30532
                    },
                    {
                        "categoryName": "iPads",
                        "totalSales": 7261
                    },
                    {
                        "categoryName": "Keyboard Cases",
                        "totalSales": 37198
                    },
                    {
                        "categoryName": "Phone Stands",
                        "totalSales": 46919
                    }
                ]
            }
        ]
    ]
}
```

### Example 2 - Retrieve the last 2 documents in the result set after sorting stores under the Boulder Innovations company in descending order of total sales 

```mongodb
db.stores.aggregate([{"$match": {"company": { "$in": ["Boulder Innovations"] } } }, {"$group": {"_id": "$company", "bottomSales": {"$bottomN": {"output": ["$company", "$sales"], "sortBy": {"sales.totalSales": -1}, "n": 2} } } }])
```

This query returns the following result:

```json
{
    "_id": "Boulder Innovations",
    "bottomSales": [
        [
            "Boulder Innovations",
            {
                "totalSales": 119,
                "salesByCategory": [
                    {
                        "categoryName": "Yoga Mats",
                        "totalSales": 119
                    }
                ]
            }
        ],
        [
            "Boulder Innovations",
            {
                "totalSales": 162,
                "salesByCategory": [
                    {
                        "categoryName": "Portable Turntables",
                        "totalSales": 162
                    }
                ]
            }
        ]
    ]
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
