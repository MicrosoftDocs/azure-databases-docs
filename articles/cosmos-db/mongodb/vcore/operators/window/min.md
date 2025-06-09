---
title: $min
titleSuffix: Overview of the $min operator in Azure Cosmos DB for MongoDB vCore
description: The $min operator in Azure Cosmos DB for MongoDB vCore returns the minimum value of the specified expression 
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $min

The `$min` operator evaluates and returns the minimum value of the specified query expression.

## Syntax

```mongodb
{
  "$min": <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | The expression to evaluate and return the minimum value|

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

### Example 1 - Calculate the minimum sales across all stores under the Boulder Innovations company 

```mongodb
db.stores.aggregate([
  {
      "$match": {
          "company": {
              "$in": [
                  "Boulder Innovations"
              ]
          }
      }
  },
  {
      "$group": {
          "_id": "$company",
          "minTotalSales": {
              "$min": "$sales.TotalSales"
          }
      }
  }
])
```

This query returns the following results:

```json
{
    "_id": "Boulder Innovations",
    "minTotalSales": 119
}
```

### Example 2 - Use the set window operator to retrieve the min sales partition by store across all stores under the Boulded Innovations company 

```mongodb
db.stores.aggregate([
{
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
        "partitionBy": "$name",
        "sortBy": {
            "sales.totalSales": 1
        },
        "output": {
            "minimumSalesForStore": {
                "$min": "$sales.totalSales",
                "window": {
                    "documents": [
                        "current",
                        "unbounded"
                    ]
                }
            }
        }
    }
},
{
    "$project": {
        "_id": 1,
        "sales.totalSales": 1
      }
}])
```

The first 2 documents returned by this query are:

```json
{
    "_id": "12f4027e-9eec-453b-bc3c-a392d60aa16b",
    "sales": { "totalSales": 10539 }
},
{
    "_id": "5b0ae35e-f590-49b8-b3c3-9c90f0b361bd",
    "sales": { "totalSales": 62885 }
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
