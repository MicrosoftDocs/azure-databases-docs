---
title: $gt
titleSuffix: Overview of the $gt query operator in Azure Cosmos DB for MongoDB vCore
description: Overview of the $gt query operator in Azure Cosmos DB for MongoDB vCore
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 01/06/2025
---

# $gt (Comparison Query)

The `$gt` operator is used to select documents where the value of a field is greater than a specified value. The `$gt` operator queries numerical and date values to filter records that exceed a specified threshold.

## Syntax

```mongodb
{ "field": { "$gt": value } }
```

## Parameters

- `field`: The field in the document you want to compare.
- `value`: The value that the field should be greater than.

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

### Example 1: Retrieve all stores where the total sales exceed $35,000

```javascript
db.stores.find({ "sales.totalSales": { "$gt": 35000 } })
```

### Example 2: Find stores with more than 12 full-time staff

```javascript
db.stores.find({ "staff.totalStaff.fullTime": { "$gt": 12 } })
```

### Example 3: Find promotion events with a discount percentage greater than 10% for Art & Craft Kits

```javascript
db.stores.find({ "promotionEvents.discounts": { "$elemMatch": { "categoryName": "Art & Craft Kits", "discountPercentage": { "$gt": 10 } } } })  
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$gte for greater than or equal to comparisons]($gte.md)
- [$lte for less than or equal to comparisons]($lte.md)
