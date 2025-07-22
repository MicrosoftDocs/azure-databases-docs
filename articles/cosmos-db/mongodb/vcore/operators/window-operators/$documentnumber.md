---
title: $documentNumber
titleSuffix: Overview of the $documentNumber operator in Azure Cosmos DB for MongoDB (vCore)
description: The $documentNumber operator assigns and returns a position for each document within a partition based on a specified sort order 
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $documentNumber

The `$documentNumber` operator sorts documents on one or more fields within a partition and assigns a document number for each document in the result set.

## Syntax

```javascript
{
    $documentNumber: {}
}
```

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

### Example 1 - Retrieve a document number by total sales

To retrieve a document number (positional ranking) for each store under the Boulder Innovations company, first run a query to filter on the company name, then sort the results in ascending order of total sales, and assign a document number to each of the documents in the sorted result set.

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": ["Boulder Innovations"]
        }
    }
}, {
    "$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "sales.totalSales": -1
        },
        "output": {
            "documentNumber": {
                "$documentNumber": {}
            }
        }
    }
}, {
    "$project": {
        "company": 1,
        "documentNumber": 1
    }
}])
```

The first 5 documents in the response are:

```json
[
{
    "_id": "27d12c50-ef9b-4a1e-981f-2eb46bf68c70",
    "company": "Boulder Innovations",
    "documentNumber": 1
},
{
    "_id": "4276b045-2488-4fea-86d4-c055097ccd62",
    "company": "Boulder Innovations",
    "documentNumber": 2
},
{
    "_id": "8c72f697-314f-4cda-a0d2-873164e5e590",
    "company": "Boulder Innovations",
    "documentNumber": 3
},
{
    "_id": "98e5d149-1823-48c5-aa9b-52513cb2ef00",
    "company": "Boulder Innovations",
    "documentNumber": 4
},
{
    "_id": "1259ee1c-be37-4a7d-82d1-20532cbecbdf",
    "company": "Boulder Innovations",
    "documentNumber": 5
}
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
