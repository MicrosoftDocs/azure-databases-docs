---
  title: $all
  titleSuffix: Overview of the $all operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $all operator helps finding array documents matching all the elements.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/25/2024
---

# $all

The `$all` operator is used to select documents where the value of a field is an array that contains all the specified elements. This operator is useful when you need to ensure that an array field contains multiple specified elements, regardless of their order in the array.

## Syntax

```javascript
db.collection.find({ <field>: { $all: [ <value1> , <value2> ... ] } })
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to be queried. |
| **`<value1> , <value2>`** | The values that must all be present in the array field. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "a57511bb-1ea3-4b26-bf0d-8bf928f2bfa8",
  "name": "Wide World Importers",
  "location": {
    "lat": 68.6378,
    "lon": -145.2852
  },
  "staff": {
    "totalStaff": {
      "fullTime": 1,
      "partTime": 5
    }
  },
  "sales": {
    "totalSales": 23399,
    "salesByCategory": [
      {
        "categoryName": "Smartphones",
        "totalSales": 5231
      },
      {
        "categoryName": "Laptops",
        "totalSales": 18168
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Unbeatable Bargain Bash",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 5,
          "Day": 17
        },
        "endDate": {
          "Year": 2023,
          "Month": 5,
          "Day": 25
        }
      },
      "discounts": [
        {
          "categoryName": "Video Games",
          "discountPercentage": 20
        },
        {
          "categoryName": "Tablets",
          "discountPercentage": 18
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

### Example 1: Find documents containing all the specified elements in an array

The example allows querying the `stores` collection to find documents containing both elements `Laptops` and `Smartphones` within `salesByCategory.categoryName` array.

```javascript
db.stores.find(
    { "sales.salesByCategory.categoryName": { $all: ["Laptops", "Smartphones"]} },
    { _id: 1, "sales.salesByCategory.categoryName": 1 }
).limit(2)
```

The query returns the two documents containing both `Laptops` and `Smartphones` within `salesCategory` array.

```json
  {
    "_id": "a57511bb-1ea3-4b26-bf0d-8bf928f2bfa8",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Smartphones"
        },
        {
          "categoryName": "Laptops"
        }
      ]
    }
  },
  {
    "_id": "ca56d696-5208-40c3-aa04-d4e245df44dd",
    "sales": {
      "salesByCategory": [
        {
          "categoryName": "Laptops"
        },
        {
          "categoryName": "Smartphones"
        }
      ]
    }
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
