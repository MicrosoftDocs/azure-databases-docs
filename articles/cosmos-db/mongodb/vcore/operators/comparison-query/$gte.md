---
title: $gte
titleSuffix: Overview of the $gte query operator in Azure Cosmos DB for MongoDB vCore
description: The $gte query operator in Azure Cosmos DB for MongoDB vCore returns documents where the value of a field is greater than or equal to a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# $gte (Comparison query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$gte` operator is used to filter documents where the value of a field is greater than or equal to a specified value. The `$gte` operator is used to retrieve documents that meet a minimum threshold for the value of a field or to find records within a range of values for the field.

## Syntax

The syntax for using the `$gte` operator is:

```mongodb
{ "field": { "$gte": value } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to compare|
| **`value`** | The value that the field should be greater than|

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

### Example 1: Retrieve all stores where the total sales is greater than or equal to $35,000

```javascript
db.stores.find({ "sales.totalSales": { "$gte": 35000 } },{"name": 1, "sales.totalSales": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "sales": { "totalSales": 37701 }
}
```

### Example 2: Find stores with 12 or more full-time staff

```javascript
db.stores.find({ "staff.totalStaff.fullTime": { "$gte": 12 } },{"name": 1, "staff.totalStaff.fullTime": 1}, {"limit": 1})
```

This returns the following results:
```json
{
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "staff": { "totalStaff": { "fullTime": 18 } }
}
```

### Example 3: Find promotion events with a discount percentage greater than or equal to 15% for Mirrors

```javascript
db.stores.find({ "promotionEvents.discounts": { "$elemMatch": { "categoryName": "Laptops", "discountPercentage": { "$gte": 15 } } } }, {"name": 1}, {"limit": 2})
```

This returns the following results:
```json
[
  {
    "_id": "60e43617-8d99-4817-b1d6-614b4a55c71e",
    "name": "Wide World Importers | Electronics Emporium - North Ayanashire"
  },
  {
    "_id": "3c441d5a-c9ad-47f4-9abc-ac269ded44ff",
    "name": "Contoso, Ltd. | Electronics Corner - New Kiera"
  }
]
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$gt for greater than comparisons]($gt.md)
- [$lt for less than comparisons]($lt.md)
