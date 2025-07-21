---
title: $maxN
titleSuffix: Overview of the $maxN operator
description: Retrieves the top N values based on a specified filtering criteria
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $maxN

The `$maxN` operator is used to retrieve the top N values for a field based on a specified filtering critieria. 

## Syntax

```javascript
$maxN: {
    input: < field or expression > ,
    n: < number of values to retrieve >
}
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`input`** | Specifies the field or expression to evaluate for maximum values. |
| **`n`** | Specifies the number of maximum values to retrieve. Must be a positive integer. |

## Examples

Consider this sample document from the stores collection.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```


### Example 1: Retrieve top 2 sales categories

The following query retrieves the top 2 sales categories with the highest sales volume:

```javascript
db.stores.aggregate([{
        $project: {
            topSalesCategories: {
                $maxN: {
                    input: "$sales.salesByCategory",
                    n: 2
                }
            }
        }
    },
    {
        $limit: 4
    }
])
```

This query returns the following results:

```json
[
    {
        "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
        "topSalesCategories": [
            {
                "categoryName": "Photo Albums",
                "totalSales": 17676
            }
        ]
    },
    {
        "_id": "b5c9f932-4efa-49fd-86ba-b35624d80d95",
        "topSalesCategories": [
            {
                "categoryName": "Rulers",
                "totalSales": 35346
            }
        ]
    },
    {
        "_id": "5c882644-f86f-433f-b45e-88e2015825df",
        "topSalesCategories": [
            {
                "categoryName": "iPads",
                "totalSales": 39014
            },
            {
                "categoryName": "Unlocked Phones",
                "totalSales": 49969
            }
        ]
    },
    {
        "_id": "cba62761-10f8-4379-9eea-a9006c667927",
        "topSalesCategories": [
            {
                "categoryName": "Ultrabooks",
                "totalSales": 41654
            },
            {
                "categoryName": "Toner Refill Kits",
                "totalSales": 10726
            }
        ]
    }
]
```

### Example 2: Using `$maxN` in `$setWindowFields`

To retrieve the top N discounts for "Laptops" in 2023 per city:

```javascript
db.stores.aggregate([{
        $unwind: "$promotionEvents"
    },
    {
        $unwind: "$promotionEvents.discounts"
    },
    // Match only "Laptops" discounts from year 2023
    {
        $match: {
            "promotionEvents.discounts.categoryName": "Laptops",
            "promotionEvents.promotionalDates.startDate.Year": 2023
        }
    },
    // Group by city and collect top N max discounts
    {
        $group: {
            _id: "$city",
            topDiscounts: {
                $maxN: {
                    input: "$promotionEvents.discounts.discountPercentage",
                    n: 3 // Change this to however many top discounts you want
                }
            }
        }
    }
])
```

The first three results returned by this query are:

```json
[
    {
        "_id": "Lake Margareteland",
        "topDiscounts": [
            18
        ]
    },
    {
        "_id": "Horacetown",
        "topDiscounts": [
            13
        ]
    },
    {
        "_id": "D'Amoreside",
        "topDiscounts": [
            9
        ]
    }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
