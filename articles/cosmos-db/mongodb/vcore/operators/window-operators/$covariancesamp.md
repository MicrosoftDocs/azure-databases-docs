---
title: $covarianceSamp
titleSuffix: Overview of the $covarianceSamp operator in Azure Cosmos DB for MongoDB (vCore)
description: The $covarianceSamp operator returns the covariance of a sample of two numerical expressions
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $covarianceSamp

The `$covarianceSamp` operator sorts documents on one more fields within a partition and calculates the covariance of a sample two numerical fields within a specified document window.

## Syntax

```javascript
{
    $covarianceSamp: [ < numericalExpression1 > , < numericalExpression2 > ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`numericalExpression1`** | The first numerical expression to use to calculate the covariance sample within the specified document window|
| **`numericalExpression2`** | The first numerical expression to use to calculate the covariance sample within the specified document window|

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

### Example 1 - Calculate the covariance sample between an unbounded starting document and the current document for stores in the Boulder Innovations company 

To calculate the covariance sample for stores in the Boulder Innovations company, first run a query to filter on the company, then sort the resulting stores in ascending order of their opening dates, and calculate the covariance of the sales of the sorted result set.

```javascript
db.stores.aggregage(
[{
      "$match": {
          "company": {
              "$in": [
                  "Boulder Innovations"
              ]
          },
        "$and": [
            {
                "storeOpeningDate": {
                    "$gt": ISODate("2024-09-01T03:06:24.180Z")
                }
            },
            {
                "storeOpeningDate": {
                    "$lt": ISODate("2024-09-30T03:55:17.557Z")
                }
            }
        ]
      }
  },
  {
    "$setWindowFields": {
        "partitionBy": "$company",
        "sortBy": {
            "storeOpeningDate": 1
        },
        "output": {
            "covarianceSampForSales": {
                "$covarianceSamp": [
                    {
                        "$hour": "$storeOpeningDate"
                    },
                    "$sales.revenue"
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
        "sales.revenue": 1,
        "storeOpeningDate": 1,
        "covarianceSampForSales": 1
    }
  }]
)
```

The first 2 documents in the response are:

```json
[{
    "_id": "5c7932cb-b720-44a9-8b73-7e3cd95efc99",
    "name": "Boulder Innovations | Home Decor Bazaar - Rutherfordchester",
    "sales": {
        "totalSales": 20383
    },
    "company": "Boulder Innovations",
    "lastUpdated": "ISODate('2024-12-01T01:15:36.736Z')",
    "covarianceSampForSales": 0
},
{
    "_id": "be1e76e0-3ccf-43d3-b6eb-9e352860575a",
    "name": "Boulder Innovations | Book Shoppe - Wolffside",
    "sales": { "totalSales": 48540 },
    "company": "Boulder Innovations",
    "storeOpeningDate": ISODate('2024-09-02T02:05:26.540Z'),
    "covarianceSampForSales": 2120.3
}]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
