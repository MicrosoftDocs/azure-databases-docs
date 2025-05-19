---
title: $stddevpop
titleSuffix: Overview of the $stddevpop operator in Azure Cosmos DB for MongoDB vCore
description: The $stddevpop operator in Azure Cosmos DB for MongoDB vCore calculates the standard deviation of the specified values
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 05/19/2025
---

# $stddevpop

The `$stddevpop` operator calculates the standard deviation of the specified values. The operator can only calculate the standard deviation on numeric values.

## Syntax

```mongodb
{
  "$stddevpop": {"fieldName"}
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`fieldName`** | The field whose values are used to calculate the standard deviation|

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

### Example 1 - Calculate the standard deviation of the total sales across all stores under the Fourth Coffee company

```mongodb
db.stores.aggregate([{"$match": {"company": "Fourth Coffee"} }, {"$group": {"_id": "$company", "stdDev": {"$stdDevPop": "$sales.totalSales"} } }])
```

This query returns the following results:

```json
{
    "_id": "Fourth Coffee",
    "stdDev": 39133.27057120701
}
```

### Example 2 - Calculate the standard deviation for a field with a single value

```mongodb
db.stores.aggregate([{"$match": {"company": "Fourth Coffee"} }, {"$group": {"_id": "$name", "stdDev": {"$stdDevPop": "$sales.totalSales"} } }])
```

This query groups the documents corresponding to 'Fourth Company' by store. Each store contains just a single document and only one distinct value for total sales. The query returns the following result, with a standard deviation of 0 as expected.

```json
[{
    "_id": "Fourth Coffee | Outdoor Equipment Collection - Kochview",
    "stdDev": 0
},
{
    "_id": "Fourth Coffee | Grocery Hub - Brakusborough",
    "stdDev": 0
},
{
    "_id": "Fourth Coffee | Pet Supply Nook - Lake Armanimouth",
    "stdDev": 0
},
{
    "_id": "Fourth Coffee | Beauty Product Nook - Emmytown",
    "stdDev": 0
},
{
    "_id": "Fourth Coffee | Bed and Bath Closet - Legroston",
    "stdDev": 0
},
{
    "_id": "Fourth Coffee | Automotive Part Collection - Cassinport",
    "stdDev": 0
}]
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
