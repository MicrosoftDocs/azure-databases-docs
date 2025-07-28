---
  title: $in
  titleSuffix: Overview of the $in operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $in operator allows finding a value existence within an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $in

The `$in` operator filters documents where a field's value matches any value in a specified array, making it ideal for matching multiple criteria. It's especially useful for querying nested arrays and handling complex data structures efficiently.

## Syntax

```javascript
{
  field: { $in: [<value1>, <value2>, ...] }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to query. |
| **`<value1>, <value2>, ...`** | An array of values to match against the specified field. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail",
  "location": {
    "lat": -9.9399,
    "lon": -0.334
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 7
    }
  },
  "sales": {
    "totalSales": 35911,
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35911
      }
    ]
  },
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
          "categoryName": "DJ Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 10
        }
      ]
    }
  ]
}
```

### Example 1: Find in an array for a specified value or set of values

The example queries for document with specified `_id` that have `DJ Mixers` with a discount percentage of either `15` or `20` within the `promotionEvents.discounts` array.

```javascript
db.stores.find({ "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
                ,"promotionEvents.discounts.discountPercentage": { $in: [15, 20] }
                },
               { "_id":1, "name":1, "promotionEvents.discounts":1}
)
```

The query returns document where the `discounts` array contains any element with a `discountPercentage` of either `15` or `20`, and only shows the complete discounts array for those documents

```json
{
  "id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail",
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
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
