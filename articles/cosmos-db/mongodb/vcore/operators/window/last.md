---
title: $last
titleSuffix: Overview of the $last operator in Azure Cosmos DB for MongoDB vCore
description: The $last operator in Azure Cosmos DB for MongoDB vCore returns the last document from the result sorted by one or more fields 
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/20/2025
---

# $last

The `$last` operator sorts documents on one more fields specified by the query and returns the last document matching the filtering criteria.

## Syntax

```mongodb
{
  "$last": <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | The expression to evaluate and return the last document from the result set|

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

### Example 1 - Retrieve the last document in the result set after sorting stores under the Boulder Innovations company in ascending order of their last updated date 

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
      "$sort": {
          "lastUpdated": 1
      }
  },
  {
      "$group": {
          "_id": "$company",
          "lastUpdated": {
              "$last": "$lastUpdated"
          }
      }
  }
])
```

This query returns the following results:

```json
{
    "_id": "Boulder Innovations",
    "lastUpdated": "ISODate('2024-12-31T23:20:24.097Z')"
  }
```

### Example 2 - Use the set window operator to retrieve the last document in the result set after sorting stores under the Boulder Innovations company in ascending order of last updated date 

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
        "partitionBy": "$company",
        "sortBy": {
            "lastUpdated": 1
        },
        "output": {
            "lastUpdatedDateForStore": {
                "$last": "$lastUpdated",
                "window": {
                    "documents": [
                        "current",
                        "unbounded"
                    ]
                }
            }
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "Boulder Innovations",
    "lastUpdated": "ISODate('2024-12-31T23:20:24.097Z')"
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
