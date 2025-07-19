---
title: $expMovingAvg
titleSuffix: Overview of the $expMovingAvg operator
description: The $expMovingAvg operator calculates the moving average of a field based on the specified number of documents to hold the highest weight
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

```javascript
{
    $expMovingAvg: {
        input: < field to use for calculation >,
        N: < number of recent documents with the highest weight
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The field whose values are used to calculate the exponential moving average|
| **`N`** | The number of previous documents with the highest weight in calculating the exponential moving average|


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

### Example 1 - Calculate the exponential moving average of total sales

To retrieve the exponential moving average of the total sales across all stores within the Boulder Innovations company, first run a query to filter on the company. Then, sort the resulting documents in ascending order of their opening date. Finally, assigned the highest weight to the two most recent documents to calculate the exponential moving average of total sales.

```javascript
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
[
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
]
```

### Example 2 - Calculate the exponential moving average of the total sales using the alpha parameter

To retrieve the exponential moving average of the total sales across all stores within the Boulder Innovations company, first run a query to filter on the company. Then, sort the resulting documents in ascending order of their opening date. Finally, specify a decay rate (alpha) to calculate the exponential moving average of total sales. A higher alpha value gives previous documents a lower weight in the calculation.

```javascript
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
    }
])
```

The first three documents returned by this query are:

```json
[
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
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
