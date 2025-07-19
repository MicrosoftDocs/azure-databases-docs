---
title: $integral
titleSuffix: Overview of the $integral operator
description: The $integral operator calculates the area under a curve with the specified range of documents forming the adjacent documents for the calculation.
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/19/2025
---

# $integral

The `$integral` operator calculates the area under a curve based on the specified range of documents sorted based on a specific field.

## Syntax

```javascript
{
    $integral: {
        input: < expression > ,
        unit: < time window >
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The field in the documents for the integral|
| **`unit`** | The specified time unit for the integral|

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

### Example 1 - Calculate the integral of total sales

To calculate the integral of total sales across all stores under the Boulder Innovations company, first run a query to filter on the company name. Then, sort the resulting stores in ascending order of their opening dates. Lastly, calculate the integral of total sales from the first to the current document in the sorted result set.

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
            "salesIntegral": {
                "$integral": {
                        "input": "$sales.revenue",
						            "unit": "hour"
                },
                "window": {
                    "range": [
                        "unbounded",
                        "current"
                    ],
					        "unit": "hour"
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
        "salesIntegral": 1
    }
  }])
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
  "salesIntegral": 0
},
{
  "_id": "5c7932cb-b720-44a9-8b73-7e3cd95efc99",
  "name": "Boulder Innovations | Home Decor Bazaar - Rutherfordchester",
  "sales": { "totalSales": 20383 },
  "company": "Boulder Innovations",
  "storeOpeningDate": ISODate('2024-09-02T01:15:36.736Z'),
  "salesIntegral": 3295.0089959722222
},
{
  "_id": "f54dfadb-bc62-42ff-912b-a281950019d6",
  "name": "Boulder Innovations | Smart TV Depot - Lake Lonnyborough",
  "sales": { "totalSales": 43648 },
  "company": "Boulder Innovations",
  "storeOpeningDate": ISODate('2024-09-02T01:28:42.683Z'),
  "salesIntegral": 10284.58849
}
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
