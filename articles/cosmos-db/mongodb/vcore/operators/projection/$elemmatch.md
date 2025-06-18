---
  title: $elemMatch (projection) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $elemMatch operator returns only the first element from an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/12/2024
---

# $elemMatch (projection)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$elemMatch` projection operator is used to project the first element in an array that matches the specified query condition. This operator is useful when you want to retrieve only the matching elements from an array within a document, rather than the entire array.

## Syntax

The syntax for using the `$elemMatch` projection operator is as follows:

```json
db.collection.find({},
    {
      "field": { "$elemMatch": { <query> } }
    }
)
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field containing the array from which you want to project the matching element. |
| **`query`** | The condition that the elements in the array need to match. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "34f462fe-5085-4a77-a3de-53f4117466bd",
  "name": "Wide World Importers",
  "location": {
    "lat": -63.5435,
    "lon": 77.7226
  },
  "staff": {
    "totalStaff": {
      "fullTime": 16,
      "partTime": 16
    }
  },
  "sales": {
    "totalSales": 41481,
    "salesByCategory": [
      {
        "categoryName": "Holiday Tableware",
        "totalSales": 41481
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Crazy Deal Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 11,
          "Day": 13
        },
        "endDate": {
          "Year": 2023,
          "Month": 11,
          "Day": 22
        }
      },
      "discounts": [
        {
          "categoryName": "Gift Boxes",
          "discountPercentage": 9
        },
        {
          "categoryName": "Holiday Tableware",
          "discountPercentage": 24
        }
      ]
    },
    {
      "eventName": "Incredible Savings Showcase",
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
  ],
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}

```

### Example 1: Projects the first element from an array, matching for $elemMatch condition

This example retrieves the `_id`, `name`, and the first matching `promotionEvents` array element from the `stores` collection for a specific document.

```javascript
db.stores.find(
  {"_id": '34f462fe-5085-4a77-a3de-53f4117466bd'},
  { "_id":1,"name":1,"promotionEvents": { $elemMatch: { "eventName": "Incredible Savings Showcase" } } }
);
```

The query returned the requested `_id` document with only "Incredible Savings Showcase" event specific details from `promotionEvents` array.

```json
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
```

## Limitation

- `$elemMatch` doesn't support text query expression.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
