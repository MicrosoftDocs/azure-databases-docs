---
title: $toDecimal
titleSuffix: Overview of the $toDecimal operator in Azure Cosmos DB for MongoDB vCore
description: The $toDecimal operator in Azure Cosmos DB for MongoDB vCore converts an expression into a Decimal type
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $toDecimal

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$toDecimal` operator converts an expression into a Decimal value. Long, Double or Int values are simply converted to a Decimal data type, while Decimal values are returned as is. A boolean value of true is returned as 1, while false is returned as 0. Lastly, ISODates are returned as a Decimal value corresponding to the number of milliseconds since January 1st, 1970 represented by the ISODate value.

## Syntax

The syntax for the `$toDecimal` operator is:

```mongodb
{ "$toDecimal": <expression> }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | The specified value to convert into a Decimal value|

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

### Example 1: Convert a Double value into a Decimal value

```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "originalLatitude": "$location.lat",
        "latitudeAsDecimal": {
            "$toDecimal": "$location.lat"
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "originalLatitude": 72.8377,
    "latitudeAsDecimal": "Decimal128('72.8377000000000')"
}
```

### Example 2: Convert an ISODate value into a Decimal value

```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "dateAsDecimal": {
            "$toDecimal": ISODate("2025-01-06T00:00:00.000Z")
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "dateAsDecimal": "Decimal128('1736121600000')"
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$type to determine the BSON type of a value]($type.md)
- [$toInt to convert a value to an Integer type]($toint.md)
- [$toLong to convert a value to a Long type]($tolong.md)
- [$toDouble to convert a value to a Double type]($todouble.md)
