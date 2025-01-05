---
title: $text
titleSuffix: Overview of the $text operator in Azure Cosmos DB for MongoDB vCore
description: Overview of the $text operator in Azure Cosmos DB for MongoDB vCore
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 08/31/2024
---

The $text operator is used to perform text search queries on a collection. The $text operator enables searching for text within string fields that have been indexed as a text index.

## Syntax

The basic syntax for the $text operator is:

```mongodb
{
  $text: {
    $search: <string>,
    $language: <string>, // optional
    $caseSensitive: <boolean>, // optional
    $diacriticSensitive: <boolean> // optional
  }
}
```

## Parameters.
-   search - The search string to query in the text index
-   language - Optional field to specify the language to be used for the search. The default value is "english".
-   caseSensitive - Optional boolean field to specify whether the search should be a case sensitive search. The default value is false.
-   diacriticSensitive - Optional boolean field to specify whether the search should be diacritic-sensitive. The default value is false.

## Examples

Consider this sample document from the SampleCollection collection in the StoreData database.

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

> [!NOTE]
> Using the $text operator requires all fields that will be part of the query filter to be specified as a text index during index creation.

### Example 1 - Basic text search

```mongodb
db.SampleCollection.find({"$text": {"$search": "Ebba's Smart TVs"}})
```

> [!NOTE]
> By default, the text search functionality treats all word separators as tokenizers for the search query. In this example, the search query conducts a search on 3 separate tokens - "Ebba's", "Smart" and "TVs" and returns all documents that contain at least one of the three terms.

### Example 2 - Basic text search on the full string

```mongodb
db.SampleCollection.find({"$text": {"$search": "\"Ebba's Smart TVs\""}})
```

> [!NOTE]
> To avoid tokenizing the terms in the search string, the string should be enclosed by quotation marks. In this example, the query conducts a search on a single token - "Ebba's Smart TVs" without separating the three words into individual tokens.
