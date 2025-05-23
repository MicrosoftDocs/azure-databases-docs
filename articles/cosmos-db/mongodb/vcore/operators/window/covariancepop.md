---
title: $covariancePop
titleSuffix: Overview of the $covariancePop operator in Azure Cosmos DB for MongoDB vCore
description: The $covariancePop operator in Azure Cosmos DB for MongoDB vCore returns the covariance of two numerical expressions
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $covariancePop

The `$covariancePop` operator sorts documents on one more fields within a partition and calculates a covariance of two numerical fields within a specified document window.

## Syntax

```mongodb
{
  "$covariancePop": [<numericalExpression1>, <numericalExpression2>]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`numericalExpression1`** | The first numerical expression to use to calculate the covariance within the specified document window|
| **`numericalExpression2`** | The first numerical expression to use to calculate the covariance within the specified document window|

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

### Example 1 - Calculate the covariance between an unbounded starting document and the current document for stores in the Boulder Innovations company 

```mongodb
db.stores.aggregage(
[{
      "$match": {
          "company": {
              "$in": [
                  "Boulder Innovations"
              ]
          }
      }
  },
  {
    "$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "lastUpdated": 1
        },
        "output": {
            "covariancePopForSales": {
                "$covariancePop": [
                    {
                        "$hour": "$lastUpdated"
                    },
                    "$sales.totalSales"
                ],
                "window": {
                    "documents": [
                        "unbounded",
                        "current"
                    ]
                }
            }
        }
    }
  },
  {
    "$project": {
        "company": 1,
        "name": 1,
        "sales.totalSales": 1,
        "lastUpdated": 1,
        "covariancePopForSales": 1
    }
  }]
)
```

The first 2 documents in the response are:

```json
{
    "_id": "a639bcc2-a553-4365-8298-ad21b71fe225",
    "name": "Boulder Innovations | Computer Variety - Lake Noemie",
    "sales": {
        "totalSales": 18216
    },
    "company": "Boulder Innovations",
    "lastUpdated": "ISODate('2024-12-01T01:05:22.107Z')",
    "covariancePopForSales": 0
},
{
    "_id": "5c7932cb-b720-44a9-8b73-7e3cd95efc99",
    "name": "Boulder Innovations | Home Decor Bazaar - Rutherfordchester",
    "sales": {
        "totalSales": 20383
    },
    "company": "Boulder Innovations",
    "lastUpdated": "ISODate('2024-12-01T01:15:36.736Z')",
    "covariancePopForSales": 0
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
