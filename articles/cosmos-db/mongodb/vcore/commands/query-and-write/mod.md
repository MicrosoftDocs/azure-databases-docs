---
title: $mod
titleSuffix: Overview of the $mod query operator in Azure Cosmos DB for MongoDB vCore
description: The $mod query operator in Azure Cosmos DB for MongoDB vCore performs a modulo opeation on the value of a specified field
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: conceptual
ms.date: 02/24/2025
---

# mod

The `$mod` operator is used to perform a modulo operation on the value of a field and select documents with a specified result. The `$mod` operator is useful in grouping or filtering data based on cyclic patterns.

## Syntax
The syntax for the $mod operator is:

```mongodb
{ field: { $mod: [divisor, remainder] } }
```

### Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to which the modulo operation will be applied|
| **`divisor`** | The number by which the field's value will be divided|
| **`remainder`** | The remainder to compare against the result of the modulo operation|

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

### Example 1 - Find documents with an even number of staff members

```mongodb
db.stores.find({"staff.totalStaff.fullTime": {"$mod": [2, 0]}}, {"staff": true})
```

Two of the documents returned are:
```json
{
    "_id": "bd03a80f-f463-4997-b886-42547093965f",
    "staff": {
        "totalStaff": {
            "fullTime": 16,
            "partTime": 8
        }
    }
},
{
    "_id": "a2617acd-03a4-4d11-b892-95916738c858",
    "staff": {
        "totalStaff": {
            "fullTime": 10,
            "partTime": 16
        }
    }
}
```

### Example 2 - Find documents with an even number of staff members with a floating point divisor

The $mod operator rounds down floating points for the $mod operator.

The following queries all yield the same result.

```mongodb
db.stores.find({"staff.totalStaff.fullTime": {"$mod": [2.0, 0]}}, {"staff": true})
```

```mongodb
db.stores.find({"staff.totalStaff.fullTime": {"$mod": [2.25, 0]}}, {"staff": true})
```

```mongodb
db.stores.find({"staff.totalStaff.fullTime": {"$mod": [2.5, 0]}}, {"staff": true})
```

```mongodb
db.stores.find({"staff.totalStaff.fullTime": {"$mod": [2.9, 0]}}, {"staff": true})
```

All the queries yield the same result. Two of the documents returned are:
```json
{
    "_id": "ed319c06-731d-45fc-8a47-b05af8637cdf",
    "staff": {
        "totalStaff": {
            "fullTime": 10,
            "partTime": 3
        }
    }
},
{
    "_id": "28d7569c-1bae-40be-9958-c3110b6253fd",
    "staff": {
        "totalStaff": {
            "fullTime": 4,
            "partTime": 14
        }
    }
}
```

### Considerations
- If fewer than two values are specified in the array for the $mod operator, an error is thrown by the server indicating not enough arguments were passed. 
- If more than two values are specified in the array for the $mod operator, an error is thrown by the server indicating too many arguments were passed.

## Related content

- [Migrate to vCore based Azure Cosmos DB for MongoDB](https://aka.ms/migrate-to-azure-cosmosdb-for-mongodb-vcore)
- [find with vCore based Azure Cosmos DB for MongoDB](find.md)
