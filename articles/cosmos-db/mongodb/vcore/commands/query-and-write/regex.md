---
title: $regex
titleSuffix: Overview of the $regex operator in Azure Cosmos DB for MongoDB vCore
description: The $regex operator in Azure Cosmos DB for MongoDB vCore performs a pattern match with a regular expression
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# regex

The `$regex` operator is used to perform pattern matching with regular expressions and is particularly useful for querying string fields for matches that fit specific patterns. Common use cases include searching for documents where a field contains a substring, starts with a certain prefix, or matches a complex pattern.

## Syntax

```mongodb
{ "field": { $regex: /pattern/, $options: '<options>' }  }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to query|
| **`/pattern/`** | The regular expression pattern you want to match|
| **`options`** | Optional flags to modify the behavior of the regex. Common options include i for case-insensitive matching, m for multiline matching, etc.|

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
db.stores.find({"promotionEvents.eventName": {"$regex": /Days/}}, {"name": 1}, {"limit": 3})
```

This returns the following results:
```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury"
  },
  {
    "_id": "f2a8c190-28e4-4e14-9d8b-0256e53dca66",
    "name": "Fabrikam, Inc. | Car Accessory Outlet - West Adele"
  },
  {
    "_id": "65300639-9bf0-460c-ae1f-891b2ff479b1",
    "name": "Wide World Importers | Fitness Equipment Emporium - Reillyborough"
  }
]
```

### Example 2 - Perform a case insensitive regex pattern match

Find all stores with a promotion event where the name contains the case insensitive substring 'days'

```mongodb
db.stores.find({"promotionEvents.eventName": {"$regex": /bash/i}})
```

This returns the following results:
```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury"
  },
  {
    "_id": "438db151-04b8-4422-aa97-acf94bc69cfc",
    "name": "Fourth Coffee | Turntable Boutique - Tromptown"
  },
  {
    "_id": "c5041337-bd61-4efa-bc7a-02799a2ce82c",
    "name": "Wide World Importers | Headphone Corner - McGlynnview"
  }
]
```
## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [find with vCore based Azure Cosmos DB for MongoDB](find.md)
- [findAndModify with vCore based Azure Cosmos DB for MongoDB](findandmodify.md)
