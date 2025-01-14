---
title: $lte
titleSuffix: Overview of the $lte query operator in Azure Cosmos DB for MongoDB vCore
description: Overview of the $lte query operator in Azure Cosmos DB for MongoDB vCore
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 01/06/2025
---

# $lte

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$lte` operator is used to match documents where the value of a field is less than or equal to a specified value. The `$lte` operator filters documents based on numerical, date, or other comparable fields.

## Syntax

The syntax for using the `$lte` operator is:

```mongodb
{
  "field": { "$lte": value }
}
```

## Parameters
- `field`: The field to be compared.
- `value`: The value to compare against.

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

### Example 1: Retrieve all stores where the total sales is less than or equal to $35,000

```javascript
db.stores.find({ "sales.totalSales": { "$lte": 35000 } })
```

### Example 2: Find stores with 12 or fewer full-time staff

```javascript
db.stores.find({ "staff.totalStaff.fullTime": { "$lte": 12 } })
```

### Example 3: Find promotion events with a discount percentage less than or equal to 15% for laptops

```javascript
db.stores.find({ "promotionEvents.discounts": { "$elemMatch": { "categoryName": "Laptops", "discountPercentage": { "$lte": 15 } } } })
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/migration-options)
- [$lt for less than comparisons]($lt.md)
- [$gt for greater than comparisons]($gt.md)
