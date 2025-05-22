---
title: $derivative
titleSuffix: Overview of the $derivative operator in Azure Cosmos DB for MongoDB vCore
description: The $derivative operator in Azure Cosmos DB for MongoDB vCore calculates the average rate of change of the value of a field within a specified window. 
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $derivative

The `$derivative` operator sorts documents on one more fields within a partition and calculates the average rate of change of a field between the first and last documents within the window.

## Syntax

```mongodb
{
  "$derivative": {
    "input": <expression>,
    "unit": <timeWindow>
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The expression or the field to calculate the rate of range|
| **`unit`** | The time window for the rate of change|

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

### Example 1 - Calculate the derivative for the total sales of each store under the Boulder Innovations whose documents are last updated within a specified time range 

```mongodb
db.stores.aggregate([
  {"$match": {
        "company": {
            "$in": [
                "Boulder Innovations"
            ]
        },
        "$and": [
            {
                "lastUpdated": {
                    "$gt": ISODate("2024-12-01T03:06:24.180Z")
                }
            },
            {
                "lastUpdated": {
                    "$lt": ISODate("2024-12-01T03:55:17.557Z")
                }
            }
        ]
    }},
    {"$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "lastUpdated": 1
        },
        "output": {
            "storeAverageSales": {
                "$derivative": {
                    "input": "$sales.totalSales",
                    "unit": "week"
                },
                "window": {
                    "range": [
                        -1,
                        0
                    ],
                    "unit": "week"
                }
            }
        }
    }},
    {"$project": {
        "lastUpdated": 1,
        "storeAverageSales": 1
    }}
])
```

This query returns the following result:

```json
{
    "_id": "6f20a67f-885c-46ed-8b74-7229e8372387",
    "lastUpdated": "ISODate('2024-12-01T03:15:05.615Z')",
    "storeAverageSales": null
},
{
    "_id": "c22cc140-a27a-4363-a3dd-49ced8af0b2b",
    "lastUpdated": "ISODate('2024-12-01T03:30:08.755Z')",
    "storeAverageSales": 33204600.83707952
},
{
    "_id": "2f70ad3a-c0bd-448a-81ba-8cc011b34ee6",
    "lastUpdated": "ISODate('2024-12-01T03:38:30.206Z')",
    "storeAverageSales": 23269835.56067211
},
{
    "_id": "6cbbdc6d-56a4-472d-9121-20a7b002b4d5",
    "lastUpdated": "ISODate('2024-12-01T03:45:17.557Z')",
    "storeAverageSales": 13936212.969289305
},
{
    "_id": "073ad628-fdc7-4115-ab12-f49bd02a2fb8",
    "lastUpdated": "ISODate('2024-12-01T03:55:06.549Z')",
    "storeAverageSales": 21554495.708753344
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
