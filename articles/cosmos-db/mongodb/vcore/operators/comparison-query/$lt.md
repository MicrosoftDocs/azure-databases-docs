---
title: $lt
titleSuffix: Overview of the $lt query operator in Azure Cosmos DB for MongoDB vCore
description: The $lt query operator in Azure Cosmos DB for MongoDB vCore matches documents where the value of field is less than a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# $lt

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$lt` operator is used to match documents where the value of a field is strictly less than a specified value. The `$lt` operator filters documents based on numeric, date, or string values.

## Syntax

The syntax for using the `$lt` operator in a MongoDB query is:

```mongodb
{ "field": { "$lt": value } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to evaluate|
| **`value`** | The value to compare against the field's value. The operator will match documents where the field's value is less than this specified value|

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

### Example 1: Find stores with total sales less than $36000

```javascript
db.stores.find({"sales.totalSales": { "$lt": 36000 }}, {"name": 1, "sales.totalSales": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
    "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
    "sales": { "totalSales": 17676 }
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$gt for greater than comparisons]($gt.md)
- [$lte for less than or equal to comparisons]($lte.md)
