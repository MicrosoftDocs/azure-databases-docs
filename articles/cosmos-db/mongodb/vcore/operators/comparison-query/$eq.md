---
title: $eq
titleSuffix: Overview of the $eq query operator in Azure Cosmos DB for MongoDB vCore
description: The $eq query operator in Azure Cosmos DB for MongoDB vCore compares the value of a field to a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# $eq (Comparison Query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$eq` operator is used to match documents where the value of a field is equal to a specified value. This operator is used to filter documents based on exact matches and with query predicates to retrieve documents with specific values, objects and arrays.

## Syntax

The syntax for the `$eq` operator is:

```json
{ "field": { "$eq": "value" } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to be compared|
| **`value`** | The value to compare against|

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

### Example 1: Find documents based an equality match on the value of a root level field

To find a store with the name "Boulder Innovations | Home Security Place - Ankundingburgh":

```javascript
db.stores.find({ "name": { "$eq": "Boulder Innovations | Home Security Place - Ankundingburgh" } }, {"name": 1})
```

This returns the following results:
```json
{
    "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
    "name": "Boulder Innovations | Home Security Place - Ankundingburgh"
}
```
### Example 2: Find documents based on an equality match on the value of a nested field

To find stores where the total sales amount is exactly $37,015:

```javascript
db.stores.find({ "sales.totalSales": { "$eq": 37015 } }, {"name": 1, "sales.totalSales": 1})
```

This returns the following results:
```json
{
    "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
    "name": "Boulder Innovations | Home Security Place - Ankundingburgh",
    "sales": { "totalSales": 37015 }
}
```

### Example 3: Find documents based on an equality match on any individual item within an array

This query searches for an equality match on any one of the objects within the nested discounts array

```javascript
db.stores.find({"promotionEvents.discounts": { "$eq": {"categoryName": "Alarm Systems", "discountPercentage": 5}}}, {"name": 1}, {"limit": 2})
```

This returns the following results:
```json
[
  {
    "_id": "ece5bf6c-3255-477e-bf2c-d577c82d6995",
    "name": "Proseware, Inc. | Home Security Boutique - Schambergertown"
  },
  {
    "_id": "7baa8fd8-113a-4b10-a7b9-2c116e976491",
    "name": "Tailwind Traders | Home Security Pantry - Port Casper"
  }
]
```

### Example 4: Find documents based on an equality on the entire array

This query searches for documents based on exact match on ALL the values within an array.

```javascript
db.stores.find({"promotionEvents.discounts": { "$eq": [{"categoryName": "Alarm Systems", "discountPercentage": 5}, {"categoryName": "Door Locks", "discountPercentage": 12}]}}, {"name": 1})
```

This returns the following results:
```json
{
    "_id": "aa9ad64c-29da-42f8-a1f0-30e03bf04a2d",
    "name": "Boulder Innovations | Home Security Market - East Sheridanborough"
}
```

> [!NOTE]
> For an equality match on an entire array, the order of the specified values in the equality predicates must also be an exact match.

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$gte for greater than or equal to comparisons]($gte.md)
- [$lte for less than or equal to comparisons]($lte.md)
