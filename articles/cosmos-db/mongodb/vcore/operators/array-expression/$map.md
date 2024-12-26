---
  title: $map (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $map operator allows applying an expression to each element in an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/16/2024
---

# $map (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$map` operator in MongoDB is used to apply an expression to each element in an array and return an array with the applied results. This operator is useful for transforming arrays within documents, such as modifying each element or extracting specific fields.

## Syntax

```javascript
{
  $map: {
    input: <array>,
    as: <variable>,
    in: <expression>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`** | The array to which the expression will be applied. |
| **`as`** | The variable name for each element in the array. |
| **`in`** | The expression to apply to each element. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "location": {
    "lat": -51.3041,
    "lon": -166.0838
  },
  "staff": {
    "totalStaff": {
      "fullTime": 5,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 266491,
    "salesByCategory": [
      {
        "categoryName": "Towel Racks",
        "totalSales": 13237
      },
      {
        "categoryName": "Washcloths",
        "totalSales": 44315
      },
      {
        "categoryName": "Face Towels",
        "totalSales": 42095
      },
      {
        "categoryName": "Toothbrush Holders",
        "totalSales": 47912
      },
      {
        "categoryName": "Hybrid Mattresses",
        "totalSales": 48660
      },
      {
        "categoryName": "Napkins",
        "totalSales": 31439
      },
      {
        "categoryName": "Pillow Cases",
        "totalSales": 38833
      }
    ]
  },
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### Example 1: Extracting category names

The aggregation pipeline filters the `stores` collection for `_id`, then projects a new field `categoryNames` where each element in the salesByCategory array has its totalSales increased by 500 using the $map operator.

```javascript
db.stores.aggregate([
  {$match: { "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"}
   },
  {
    $project: {
      categoryNames: {
        $map: {
          input: "$sales.salesByCategory.totalSales",
          as: "category",
          in: {$add: ["$$category",500]}
        }
      }
    }
  }
])
```

The query returns the updated data for `totalSales` with `500` added to individual element from the sample json.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "categoryNames": [
    13737,
    44815,
    42595,
    48412,
    49160,
    31939,
    39333
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
