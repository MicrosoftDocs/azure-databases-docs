---
title: $toInt
titleSuffix: Overview of the $eq query operator in Azure Cosmos DB for MongoDB vCore
description: Overview of the $eq query operator in Azure Cosmos DB for MongoDB vCore
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 01/06/2025
---

# $toInt 

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The toInt operator converts a specified value into an integer value.

## Syntax

The syntax for the `$eq` operator is:

```mongodb
{ "$toInt": <expression> }
```

## Parameters

- `expression`: The specified value to convert into an integer value

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

### Example 1: Convert a Double value into an Integer value
A Double value is truncated and returned as an Integer value

```javascript
db.SampleCollection.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "originalLatitude": "$location.lat",
        "latitudeAsInt": {
            "$toInt": "$location.lat"
        }
    }
}])
```

### Example 2: Convert a String value into an Integer value

A String can be converted into an Integer value if it was already the string representation of an integer.

In this query, the string "72" can be converted to an integer value.

```javascript
db.SampleCollection.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "originalLatitude": "$location.lat",
        "latitudeAsInt": {
            "$toInt": {
                "$toString": "72"
            }
        }
    }
}
])
```
However, this query returns an error since the string "72.0" isn;t the string representation of an integer value.

```javascript
db.SampleCollection.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "originalLatitude": "$location.lat",
        "latitudeAsInt": {
            "$toInt": {
                "$toString": "72.0"
            }
        }
    }
}
])
```

Tabulated here is the expected behavior of the $toInt operator based on the data type of the input value.

| **Value Type**                                               | **Behavior/Output** |
|--------------------------------------------------------------|---------------------|
| Boolean value true                                           | Output -> 1         |
| Boolean value false                                          | Output -> 0         |
| Double value. E.g., 72.0                                     | Output -> 72        |
| String representation of an integer value. For example, "72" | Output -> 72        |
| String representation of a double value. For example, "72.0" | Output -> Error     |
| Null value                                                   | Output -> null      |
