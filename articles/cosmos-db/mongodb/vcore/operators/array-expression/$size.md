---
  title: $size (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $size operator is used to count number of elements in an array.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: how-to
  ms.date: 09/16/2024
---

# $size (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$size` operator is used to count the number of elements in an array. It is particularly useful when you need to determine the size of an array field within a document. This operator can be used in aggregation pipelines and in query projections.

## Syntax

The syntax for using the `$size` operator is as follows:

```javascript
{ $size: <array> }
```

## Parameters

| | Description |
| --- | --- |
| **`array`** | The array whose number of elements you want to count. |

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

### Example 1: Find number of elements in an array

The example query calculates and returns the count of elements in the `salesByCategory` array for the provided JSON sample.

```javascript
db.stores.aggregate([
  {
    $match: { "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"}
  },
  {
    $project: {
      "storeId": 1,
      "name": 1,
      "numberOfSalesCategories": { $size: "$sales.salesByCategory" }
    }
  }
])
```

The query returns the number of sales categories available for the "Lakeshore Retail" store.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "numberOfSalesCategories": 7
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
