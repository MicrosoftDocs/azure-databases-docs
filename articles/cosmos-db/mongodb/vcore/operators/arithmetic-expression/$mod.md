---
title: $mod
titleSuffix: Overview of the $mod operator in Azure Cosmos DB for MongoDB (vCore)
description: The $mod operator filters documents based on a modulus operation.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $mod

The `$mod` query operator is used to filter documents based on the remainder of a division operation. This operator allows for queries that involve mathematical conditions, such as finding values divisible by a number or having a specific remainder. It's supported in Azure Cosmos DB for MongoDB (vCore).

## Syntax

```javascript
{ 
  <field>: { $mod: [ <divisor>, <remainder> ] } 
}
```

## Parameters
| Parameter | Description |
| --- | --- |
|**`<field>`**| The field on which to perform the modulus operation|
|**`<divisor>`**| The number by which to divide the field's value|
|**`<remainder>`**| The expected remainder after the division|

## Examples

Consider this sample document from the stores collection.

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

### Example 1: Find stores where the total sales volume is divisible by 3

To find stores within the "First Up Consultants" company whose sales volumes are divisible by 3, first run a query to filter on the company name. Then, use the $mod operator on the totalSales field to retrieve the desired stores.

```javascript
db.stores.aggregate([{
    "$match": {
        "company": {
            "$in": [
                "First Up Consultants"
            ]
        },
        "$and": [{
            "sales.totalSales": {
                "$mod": [5, 2]
            }
        }]
    }
}, {
    "$project": {
        "company": 1,
        "sales.revenue": 1
    }
}])
```

The first three results returned by this query are:

```json
[
    {
        "_id": "1596d31a-84d4-47bb-973f-884cc1a1aa03",
        "sales": {
            "revenue": 74467
        },
        "company": "First Up Consultants"
    },
    {
        "_id": "269181ff-e9db-4019-9f36-7b7935ef6ab2",
        "sales": {
            "revenue": 48832
        },
        "company": "First Up Consultants"
    },
    {
        "_id": "cb93912d-4392-4393-a1f9-b3d1f0681254",
        "sales": {
            "revenue": 11227
        },
        "company": "First Up Consultants"
    }
]
```

## Considerations

- If fewer than two values are specified in the array for the $mod operator, an error is thrown by the server indicating not enough arguments were passed. 
- If more than two values are specified in the array for the $mod operator, an error is thrown by the server indicating too many arguments were passed.

## Limitations

- The `$mod` operator is applied to numerical fields only. Using it on non-numerical fields result in an error.
- Ensure that the divisor isn't zero, as it leads to an invalid operation.

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
