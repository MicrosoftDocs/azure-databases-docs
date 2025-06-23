---
title: $expMovingAvg
titleSuffix: Overview of the $expMovingAvg operator in Azure Cosmos DB for MongoDB vCore
description: The $expMovingAvg operator in Azure Cosmos DB for MongoDB vCore calculates the moving average of the specified value based on the specified number of documents to hold the highest weight
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/19/2025
---

# $expMovingAvg

The `$expMovingAvg` operator calculates the exponential moving average of the values of a specified field.

## Syntax

```mongodb
{
  "$expMovingAvg": {
    "input": <field to use for calculation>,
    "N": <number of recent documents with the highest weight
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The field whose values are used to calculate the exponential moving average|
| **`N`** | The number of previous documents with the highest weight in calculating the exponential moving average|


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

### Example 1 - Calculate the exponential moving average of the total sales across all stores under the Fourth Coffee company using N

```mongodb
db.stores.aggregate(
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
            "storeOpeningDate": 1
        },
        "output": {
            "expMovingAvgForSales": {
                "$expMovingAvg": {
                    "input": "$sales.totalSales",
						        "N": 2
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
        "storeOpeningDate": 1,
        "expMovingAvgForSales": 1
    }
  }])
```

The firs three documents returned by this query are:

```json
{
    "_id": "a639bcc2-a553-4365-8298-ad21b71fe225",
    "name": "Boulder Innovations | Computer Variety - Lake Noemie",
    "sales": { "totalSales": 18216 },
    "company": 'Boulder Innovations',
    "storeOpeningDate": ISODate('2024-09-02T01:05:22.107Z'),
    "expMovingAvgForSales": 18216
  },
  {
    "_id": "5c7932cb-b720-44a9-8b73-7e3cd95efc99",
    "name": "Boulder Innovations | Home Decor Bazaar - Rutherfordchester",
    "sales": { "totalSales": 20383 },
    "company": "Boulder Innovations",
    "storeOpeningDate": ISODate('2024-09-02T01:15:36.736Z'),
    "expMovingAvgForSales": 19660.666666666668
  },
  {
    "_id": "f54dfadb-bc62-42ff-912b-a281950019d6",
    "name": "Boulder Innovations | Smart TV Depot - Lake Lonnyborough",
    "sales": { "totalSales": 43648 },
    "company": "Boulder Innovations",
    "storeOpeningDate": ISODate('2024-09-02T01:28:42.683Z'),
    "expMovingAvgForSales": 35652.22222222223
  }
```

### Example 2 - Calculate the exponential moving average of the total sales across all stores under the Fourth Coffee company using alpha

```mongodb
db.stores.aggregate(
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
            "storeOpeningDate": 1
        },
        "output": {
            "expMovingAvgForSales": {
                "$expMovingAvg": {
                    "input": "$sales.totalSales",
						        "alpha": 0.75
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
        "storeOpeningDate": 1,
        "expMovingAvgForSales": 1
    }
  }])
```

The first three documents returned by this query are:

```json
{
    "_id": "a639bcc2-a553-4365-8298-ad21b71fe225",
    "name": "Boulder Innovations | Computer Variety - Lake Noemie",
    "sales": { "totalSales": 18216 },
    "company": "Boulder Innovations",
    "storeOpeningDate": ISODate('2024-09-02T01:05:22.107Z'),
    "expMovingAvgForSales": 18216
  },
  {
    "_id": "5c7932cb-b720-44a9-8b73-7e3cd95efc99",
    "name": "Boulder Innovations | Home Decor Bazaar - Rutherfordchester",
    "sales": { "totalSales": 20383 },
    "company": "Boulder Innovations",
    "storeOpeningDate": ISODate('2024-09-02T01:15:36.736Z'),
    "expMovingAvgForSales": 19841.25
  },
  {
    "_id": "f54dfadb-bc62-42ff-912b-a281950019d6",
    "name": "Boulder Innovations | Smart TV Depot - Lake Lonnyborough",
    "sales": { "totalSales": 43648 },
    "company": "Boulder Innovations",
    "storeOpeningDate": ISODate('2024-09-02T01:28:42.683Z'),
    "expMovingAvgForSales": 37696.3125
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
