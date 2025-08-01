---
title: $sortByCount
titleSuffix: Overview of the $sort operator in Azure Cosmos DB for MongoDB vCore
description: The $sortByCount stage in the aggregation pipeline is used to group documents by a specified expression and then sort the count of documents in each group in descending order.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/27/2024
---

# $sortByCount
The $sortByCount stage in the aggregation pipeline is used to group documents by a specified expression and then sort the count of documents in each group in descending order. The `$sortByCount` stage is useful for quickly identifying the most common values within a dataset.

## Syntax
The syntax for the $sortByCount stage is:

```javascript
{
  $sortByCount: <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | This is the field or computed expression on which to group and count the documents. |

## Example
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
To group by the eventName field and count the number of occurrences of each event name, sorting the results in descending order of the count

```javascript
db.stores.aggregate([
  { $unwind: "$store.promotionEvents" },
  { $sortByCount: "$store.promotionEvents.eventName" }
])
```
Sample output
```json
[
  { "_id": "Summer Sale", "count": 152 },
  { "_id": "Black Friday", "count": 120 },
  { "_id": "Holiday Deals", "count": 98 }
]
```

This pipeline will: 
1. Use $unwind to deconstruct the promotionEvents array field from the input documents.
1. Use $sortByCount to group by the eventName field and count the number of occurrences of each event name, sorting the results in descending order of the count.


## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).