---
  title: $elemMatch
  titleSuffix: Overview of the $elemMatch operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $elemMatch operator returns only the first element from an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/04/2025
---

# $elemMatch

The `$elemMatch` projection operator is used to project the first element in an array that matches the specified query condition. This operator is useful when you want to retrieve only the matching elements from an array within a document, rather than the entire array.

## Syntax

```json
db.collection.find({}, {
    "field": {
        "$elemMatch": {
            < query >
        }
    }
})
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field containing the array from which you want to project the matching element. |
| **`query`** | The condition that the elements in the array need to match. |

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

### Example 1: Projects the first element from an array, matching for $elemMatch condition

This query retrieves the `_id`, `name`, and the first matching `promotionEvents` array element from the `stores` collection for a specific document.

```javascript
db.stores.find({
    "_id": '34f462fe-5085-4a77-a3de-53f4117466bd'
}, {
    "_id": 1,
    "name": 1,
    "promotionEvents": {
        $elemMatch: {
            "eventName": "Incredible Savings Showcase"
        }
    }
})
```

This query returns the following result.

```json
[
  {
    "_id": "34f462fe-5085-4a77-a3de-53f4117466bd",
    "name": "Wide World Importers",
    "promotionEvents": [
      {
        "eventName": 'Incredible Savings Showcase',
        "promotionalDates": {
          "startDate": {
            "Year": 2024,
            "Month": 5,
            "Day": 11
          },
          "endDate": {
            "Year": 2024,
            "Month": 5,
            "Day": 20
          }
        },
        "discounts": [
          {
            "categoryName": "Ribbons",
            "discountPercentage": 15
          },
          {
            "categoryName": "Gift Bags",
            "discountPercentage": 25
          }
        ]
      }
    ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
