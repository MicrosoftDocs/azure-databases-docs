---
title: $regex
titleSuffix: Overview of the $regex operator in Azure Cosmos DB for MongoDB vCore
description: Overview of the $regex operator in Azure Cosmos DB for MongoDB vCore
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 01/03/2025
---

# regex

The `$regex` operator is used to perform pattern matching with regular expressions and is particularly useful for querying string fields for matches that fit specific patterns. Common use cases include searching for documents where a field contains a substring, starts with a certain prefix, or matches a complex pattern.

## Syntax

```mongodb
{ "field": { $regex: /pattern/, $options: '<options>' }  }
```

## Parameters
- `field`: The field in the document you want to query.
- `/pattern/`: The regular expression pattern you want to match.
- `options`: Optional flags to modify the behavior of the regex. Common options include i for case-insensitive matching, m for multiline matching, etc.

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

### Example 1 - Find all stores with a promotion event where the name contains the substring 'Days'

```mongodb
db.stores.find({"promotionEvents.eventName": {"$regex": /Days/}})
```

### Example 2 - Perform a case insensitive regex pattern match

Find all stores with a promotion event where the name contains the case insensitive substring 'days'

```mongodb
db.stores.find({"promotionEvents.eventName": {"$regex": /bash/i}})
```
## Related Content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/migration-options)
- [find with vCore based Azure Cosmos DB for MongoDB](find.md)
- [findAndModify with vCore based Azure Cosmos DB for MongoDB](findandmodify.md)
