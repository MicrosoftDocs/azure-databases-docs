---
title: $in
titleSuffix: Overview of the $in query operator in Azure Cosmos DB for MongoDB vCore
description: The $in query operator in Azure Cosmos DB for MongoDB vCore matches value of a field against an array of specified values
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $in

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$in` operator is used to match values of a field against an array of possible values. The `$in` operator filters documents where the value of a field equals any of the specified values.

## Syntax

```mongodb
{ field: { $in: [<value1>, <value2>, ... <valueN>] } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to match|
| **`[<value1>, <value2>, ... <valueN>]`** | An array of values to match against the specified field|

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

### Example 1 - Find documents with promotion events offering a discount percentage of either 10%, 15% or 20%

```javascript
db.stores.find({ "promotionEvents.discounts.discountPercentage": { "$in": [10, 15, 20] }}, {"name": 1, "promotionEvents.discounts.discountPercentage": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "promotionEvents": [
      {
        "discounts": [
          { "discountPercentage": 14 },
          { "discountPercentage": 6 },
          { "discountPercentage": 21 },
          { "discountPercentage": 21 },
          { "discountPercentage": 5 },
          { "discountPercentage": 22 }
        ]
      }
    ]
}
```

### Example 2 - Find documents with discount offers on specific categories of promotions

```javascript
db.stores.find({ "promotionEvents.discounts.categoryName": { "$in": ["Smoked Salmon", "Anklets"] }}, {"name": 1, "promotionEvents.discounts.categoryName": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "3f140a3f-6809-4b40-85b1-75657f5605b8",
    "name": "Boulder Innovations | Jewelry Store - Littleborough",
    "promotionEvents": [
      {
        "discounts": [ { "categoryName": "Watches" }, { "categoryName": "Rings" } ]
      },
      {
        "discounts": [ { "categoryName": "Anklets" }, { "categoryName": "Earrings" } ]
      },
      {
        "discounts": [ { "categoryName": "Rings" }, { "categoryName": "Anklets" } ]
      },
      {
        "discounts": [ { "categoryName": "Earrings" }, { "categoryName": "Necklaces" } ]
      },
      {
        "discounts": [ { "categoryName": "Charms" }, { "categoryName": "Bracelets" } ]
      },
      {
        "discounts": [ { "categoryName": "Watches" }, { "categoryName": "Brooches" } ]
      }
    ]
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$nin for not-in comparisons]($nin.md)
