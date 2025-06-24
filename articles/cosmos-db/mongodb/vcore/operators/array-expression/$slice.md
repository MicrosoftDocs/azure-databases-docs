---
  title: $slice (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $slice operator returns a subset of an array from any element onwards in the array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/11/2024
---

# $slice (Array Expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$slice` operator is used to return a subset of an array. It can be used to limit the number of elements in an array to a specified number or to return elements from a specified position in the array. This is particularly useful when dealing with large arrays where only a portion of the data is needed for processing or display.

## Syntax

The syntax for the `$slice` operator is as following.

- Returns elements from either the start or end of the array

```javascript
{ $slice: [ <array>, <n> ] }
```

- Returns elements from the specified position in the array

```javascript
{ $slice: [ <array>, <position>, <n> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`array`** | Any valid array expression. |
| **`position`** | Any valid integer expression. |
| **`n`** | Any valid integer expression. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "sales": {
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
    ]},
"tag": [
    '#ShopLocal',
    '#FashionStore',
    '#SeasonalSale',
    '#FreeShipping',
    '#MembershipDeals'
  ]
}
```

### Example 1: Return the set of elements from the array

The example queries for the first three elements of the `sales.salesByCategory` array for `_id: 988d2dd1-2faa-4072-b420-b91b95cbfd60` within `stores` collection.

```javascript
db.stores.aggregate([
     { $match: { "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"} }
   , { $project: { "salesByCategory": { $slice: [ "$sales.salesByCategory", 3 ] } } }
])
```

The query response reverts with first three array elements for the sample json.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
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
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
