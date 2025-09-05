---
title: $slice
titleSuffix: Overview of the $slice operator in Azure Cosmos DB for MongoDB (vCore)
description: The $slice operator is used to return a subset of an array limited by a specified number or range of items.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/04/2025
---

# $slice

The `$slice` operator is used to return a subset of an array. It can be used to limit the number of elements in an array to a specified number or to return elements from a specified position in the array. This operator is useful when dealing with large arrays where only a portion of the data is needed for processing or display.

## Syntax

```javascript
db.collection.find({},
  {
    <field>: { $slice: <count> }
  }
)
```

```javascript
db.collection.find({},
  {
    <field>: { $slice: [ <skip>, <limit> ] }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The array field from which you want to slice a subset. |
| **`count`** | The number of elements to return from the beginning of the array. |

| | Description |
| --- | --- |
| **`skip`** | The number of elements to skip. |
| **`limit`** | The number of elements to return after skipping. |

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

### Example 1: Returns the first matching element from an array

This query retrieves the first document from "sales.salesByCategory" array.

```javascript
db.stores.find({
        "name": "Lakeshore Retail"
    }, {
        "_id": 1,
        "name": 1,
        "sales.salesByCategory": {
            $slice: 1
        }
    } // restricts the fields to be returned
)
```

This query returns the following result.

```json
[
  {
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Towel Racks",
          "totalSales": 13237
        }
      ]
    }
  }
]
```

### Example 2: Return the last element from an array

This query retrieves the last document from "sales.salesByCategory" array.

```javascript
db.stores.find({
    "name": "Lakeshore Retail"
}, {
    "_id": 1,
    "name": 1,
    "sales.salesByCategory": {
        $slice: -1
    }
})
```

This query returns the following result.

```json
[
  {
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Pillow Cases",
          "totalSales": 38833
        }
      ]
    }
  }
]
```

### Example 3: Returns a range of elements from an array

This query retrieves a subset range from "sales.salesByCategory" array.

```javascript
db.stores.find({
    "name": "Lakeshore Retail"
}, {
    "_id": 1,
    "name": 1,
    "sales.salesByCategory": {
        $slice: [3, 2]
    }
})
```

This query returns the following result.

```json
[
  {
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "name": "Lakeshore Retail",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Toothbrush Holders",
          "totalSales": 47912
        },
        {
          "categoryName": "Hybrid Mattresses",
          "totalSales": 48660
        }
      ]
    }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
