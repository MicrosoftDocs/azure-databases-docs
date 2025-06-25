---
title: $type
titleSuffix: Overview of the $type operator in Azure Cosmos DB for MongoDB vCore
description: The $type operator in Azure Cosmos DB for MongoDB vCore returns the type of the specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $type

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$type` operator returns the type of the value specified in the expression.

## Syntax

The syntax for the `$type` operator is:

```mongodb
{ "$type": <expression> }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | The specified value whose type to retrieve|

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

### Example 1: Get the type of a Double value
```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "longitude": "$location.lon",
        "longitudeType": {
            "$type": "$location.lon"
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "longitude": 72.8377,
    "longitudeType": "double"
}
```

### Example 2: Get the type of a String value

```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "name": "$name",
        "nameType": {
            "$type": "$name"
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "name": "Wide World Importers | Furniture Bargains - Roobport",
    "nameType": "string"
}
```

### Example 3: Get the type of an Int value

```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "fullTimeStaff": "$staff.totalStaff.fullTime",
        "fullTimeStaffType": {
            "$type": "$staff.totalStaff.fullTime"
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "fullTimeStaff": 3,
    "fullTimeStaffType": "int"
}
```

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$convert to convert a value from one type to another]($convert.md)

