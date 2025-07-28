---
  title: $reduce
  titleSuffix: Overview of the $reduce operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $reduce operator applies an expression to each element in an array & accumulate result as single value.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $reduce

The `$reduce` operator is used to apply an expression to each element in an array and accumulate the results into a single value. This operator is useful for performing operations that require iterating over array elements and aggregating their values.

## Syntax

```javascript
$reduce: {
   input: <array>,
   initialValue: <expression>,
   in: <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The array to iterate over. |
| **`initialValue`** | The initial cumulative value set before the array iteration begins. |
| **`in`** | A valid expression that evaluates to the accumulated value for each element in the array. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "d3c9df51-41bd-4b4e-a26b-b038d9cf8b45",
  "location": {
    "lat": -67.7571,
    "lon": 97.2505
  },
  "sales": {
    "totalSales": 149849,
    "salesByCategory": [
      {
        "categoryName": "DJ Speakers",
        "totalSales": 36972
      },
      {
        "categoryName": "DJ Headphones",
        "totalSales": 12877
      },
      {
        "categoryName": "Music Accessories",
        "totalSales": 40000
      },
      {
        "categoryName": "DJ Accessories",
        "totalSales": 60000
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

### Example 1: Aggregates the array values

The example demonstrates how to use `$reduce` to sum the total sales across different categories in the `salesByCategory` array.

```javascript
db.stores.aggregate([
  { $match: { "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"} }
, {
    $project: {
      totalSalesByCategory: {
        $reduce: {
          input: "$sales.salesByCategory.totalSales",
          initialValue: 0,
          in: { $add: ["$$value", "$$this"] }
        }
      }
    }
  }
])
```

The query returns `totalSales` across the categories.

```json
{
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "totalSalesByCategory": 149849
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
