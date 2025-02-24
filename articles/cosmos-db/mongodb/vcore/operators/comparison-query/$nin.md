---
title: $nin
titleSuffix: Overview of the $nin query operator in Azure Cosmos DB for MongoDB vCore
description: The $nin query operator in Azure Cosmos DB for MongoDB vCore returns documents where the value of a field doesn't match a list of values
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# $nin

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$nin` operator is used to retrieve documents where the value of a specified field doesn't match a list of values.

## Syntax

```mongodb
{ field: { $nin: [<value1>, <value2>, ... <valueN>] } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to compare|
| **`[<value1>, <value2>, ... <valueN>]`** | An array of values that shouldn't match the value of the field being compared|

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

### Example 1 - Find documents with promotion events offering a discount percentage that isn't either of 10%, 15%, or 20%

```javascript
db.stores.find({ "promotionEvents.discounts.discountPercentage": { "$nin": [10, 15, 20] }}, {"name": 1, "promotionEvents.discounts.discountPercentage": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "promotionEvents": [
      {
        "discounts": [
          { "discountPercentage": 18 },
          { "discountPercentage": 17 },
          { "discountPercentage": 9 },
          { "discountPercentage": 5 },
          { "discountPercentage": 5 },
          { "discountPercentage": 6 },
          { "discountPercentage": 9 },
          { "discountPercentage": 5 },
          { "discountPercentage": 19 },
          { "discountPercentage": 21 }
        ]
      }
    ]
}
```

### Example 2 - Find documents with discount offers that aren't on specific categories of promotions

```javascript
db.stores.find({ "promotionEvents.discounts.categoryName": { "$nin": ["Smoked Salmon", "Anklets"] }}, {"name": 1, "promotionEvents.discounts.categoryName": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "Bath Accessories" },
          { "categoryName": "Pillow Top Mattresses" },
          { "categoryName": "Bathroom Scales" },
          { "categoryName": "Towels" },
          { "categoryName": "Bathrobes" },
          { "categoryName": "Mattress Toppers" },
          { "categoryName": "Hand Towels" },
          { "categoryName": "Shower Heads" },
          { "categoryName": "Bedspreads" },
          { "categoryName": "Bath Mats" }
        ]
      }
    ]
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$in for in comparisons]($in.md)
