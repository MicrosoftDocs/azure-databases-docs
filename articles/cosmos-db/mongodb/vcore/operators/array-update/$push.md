---
  title: $push
  titleSuffix: Overview of the $push operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $push operator adds a specified value to an array within a document. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/11/2024
---

# $push

The `$push` operator is used to add a specified value to an array within a document. The $push operator adds new elements to an existing array without affecting other elements in the array. It

## Syntax

```javascript
db.collection.update({
    < query >
}, {
    $push: {
        < field >: < value >
    }
}, {
    < options >
})
```

## Parameters
| Parameter | Description |
| --- | --- |
| **`<query>`**| The selection criteria for the documents to update.|
| **`<field>`**| The array field to which the value will be appended.|
| **`<value>`**| The value to append to the array field.|
| **`<options>`**| Optional. Additional options for the update operation.|

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

### Example 1 - Add a new sales category

To add a new sales category to the salesByCategory array, run a query using the $push operator on the field with a new Sales object with the name of the category and its sales volume.

```javascript
db.stores.update(
   { _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
   { $push: { "sales.salesByCategory": { "categoryName": "DJ Cables", "totalSales": 1000.00 } } }
)
```

This query returns the following result:

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
