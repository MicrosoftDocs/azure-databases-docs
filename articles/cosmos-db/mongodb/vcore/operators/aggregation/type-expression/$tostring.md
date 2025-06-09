---
title: $toString
titleSuffix: Overview of the $toString operator in Azure Cosmos DB for MongoDB vCore
description: The $toString operator in Azure Cosmos DB for MongoDB vCore converts an expression into a String
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# $toString

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$toString` operator simply returns the value of the expression as a String.

## Syntax

The syntax for the `$toString` operator is:

```mongodb
{ "$toString": <expression> }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | The specified value to convert into a String value|

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

### Example 1: Convert a Double value into a String value

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
        "latitudeAsString": {
            "$toString": "$location.lat"
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "originalLatitude": 72.8377,
    "latitudeAsString": "72.8377"
}
```

### Example 2: Convert an Int value into a String value

```javascript
db.stores.aggregate([
{
    "$match": {
        "_id": "b0107631-9370-4acd-aafa-8ac3511e623d"
    }
},
{
    "$project": {
        "originalTotalSales": "$sales.totalSales",
        "totalSalesAsString": {
            "$toString": "$sales.totalSales"
        }
    }
}])
```

This query returns the following result:

```json
{
    "_id": "b0107631-9370-4acd-aafa-8ac3511e623d",
    "originalTotalSales": 9366,
    "totalSalesAsString": "9366"
}
```

This table delineates the expected behavior of the $toString operator based on the data type of the input value.

| **Value Type**                                                         | **Behavior/Output**                  |
|------------------------------------------------------------------------|--------------------------------------|
| Boolean value true                                                     | Output -> "true"                     |
| Boolean value false                                                    | Output -> "false"                    |
| Any Double, Int, Long or Decimal value. For example, 72                | Output -> "72"                       |
| Any ObjectId value. For example, ObjectId("b010763193704acdaafa8ac3")  | Output -> "b010763193704acdaafa8ac3" |


## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [$type to determine the BSON type of a value]($type.md)
- [$toInt to convert a value to an ObjectId]($toobjectid.md)
