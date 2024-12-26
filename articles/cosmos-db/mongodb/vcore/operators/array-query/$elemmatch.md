---
  title: $elemmatch (array query) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $elemmatch operator returns complete array, qualifying criteria with at least one matching array element.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# $elemMatch (array query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$elemMatch` operator is used to match documents that contain an array field with at least one element that matches all the specified query criteria. This operator is particularly useful when you need to find array documents with specified element.

## Syntax

The basic syntax for the `$elemMatch` operator is as follows:

```javascript
db.collection.find({ <field>: { $elemMatch: { <query1>, <query2>, ... } } })
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field in the document that contains the array to be queried. |
| **`query`** | The conditions that at least one element in the array must satisfy. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
[
  {
    "_id": "91de5201-8194-44bf-848f-674e8df8bf5e",
    "name": "Adatum Corporation",
    "promotionEvents": [
      {
        "discounts": [
          { "categoryName": "DJ Cases", "discountPercentage": 6 },
          { "categoryName": "DJ Mixers", "discountPercentage": 14 }
        ]
      },
      {
        "discounts": [
          { "categoryName": "DJ Headphones", "discountPercentage": 19 },
          { "categoryName": "DJ Speakers", "discountPercentage": 13 }
        ]
      },
      {
        "discounts": [
          { "categoryName": "DJ Lighting", "discountPercentage": 12 },
          { "categoryName": "DJ Accessories", "discountPercentage": 6 }
        ]
      }
    ]
  }
]
```

### Example 1: Find in an array for specific element among the list of elements

This example finds the first two documents in the `stores` collection that have at least one discount with the category name "DJ Lighting" in their `promotionEvents` array. The query only returns the `_id` and `promotionEvents.discounts` fields for those documents.

```javascript
db.stores.find(  {"promotionEvents.discounts":{$elemMatch:{"categoryName":"DJ Lighting"}}}
                ,{ _id: 1, "promotionEvents.discounts": 1 }).limit(2)
```

We receive the following documents returned.

```json
{
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "promotionEvents": [
      {
        "discounts": [
          {
            "categoryName": "DJ Turntables",
            "discountPercentage": 18
          },
          {
            "categoryName": "DJ Mixers",
            "discountPercentage": 15
          }
        ]
      },
      {
        "discounts": [
          {
            "categoryName": "DJ Lighting",
            "discountPercentage": 14
          },
          {
            "categoryName": "DJ Cases",
            "discountPercentage": 20
          }
        ]
      }
    ]
  },
  {
    "_id": "91de5201-8194-44bf-848f-674e8df8bf5e",
    "promotionEvents": [
      {
        "discounts": [
          {
            "categoryName": "DJ Cases",
            "discountPercentage": 6
          },
          {
            "categoryName": "DJ Mixers",
            "discountPercentage": 14
          }
        ]
      },
      {
        "discounts": [
          {
            "categoryName": "DJ Headphones",
            "discountPercentage": 19
          },
          {
            "categoryName": "DJ Speakers",
            "discountPercentage": 13
          }
        ]
      },
      {
        "discounts": [
          {
            "categoryName": "DJ Lighting",
            "discountPercentage": 12
          },
          {
            "categoryName": "DJ Accessories",
            "discountPercentage": 6
          }
        ]
      }
    ]
}

```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
