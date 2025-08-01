---
title: $slice (projection)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $slice operator is used to return a subset of an array limited by a specified number or range of items.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/12/2024
---

# $slice (projection)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$slice` operator is used to return a subset of an array. It can be used to limit the number of elements in an array to a specified number or to return elements from a specified position in the array. This operator is useful when dealing with large arrays where only a portion of the data is needed for processing or display.

## Syntax

```javascript
db.collection.find({},
  {
    <field>: { $slice: <count> }
  }
)
```

```javascript
db.collection.find({},
  {
    <field>: { $slice: [ <skip>, <limit> ] }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The array field from which you want to slice a subset. |
| **`count`** | The number of elements to return from the beginning of the array. |

| | Description |
| --- | --- |
| **`skip`** | The number of elements to skip. |
| **`limit`** | The number of elements to return after skipping. |

## Examples

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

### Example 1: Returns the first matching element from an array

The example queries `stores` data for "Lakeshore Retail", and finds the first document from "sales.salesByCategory" array.

```javascript
db.stores.find(
  { "name": "Lakeshore Retail"},
  { "_id":1,"name":1,"sales.salesByCategory": { $slice: 1 } } // restricts the fields to be returned
)
```

This query will return document from the `stores` collection, with first `categoryName` document within the array.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "Towel Racks",
        "totalSales": 13237
      }
    ]
  }
}
```

### Example 2: Return the last element from an array

The example queries `stores` data for "Lakeshore Retail", and finds the last document from "sales.salesByCategory" array.

```javascript
db.stores.find(
  { "name": "Lakeshore Retail"},
  { "_id":1,"name":1,"sales.salesByCategory": { $slice: -1 } } 
)
```

This query will return document from the `stores` collection, with last `categoryName` document within the array.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "Pillow Cases",
        "totalSales": 38833
      }
    ]
  }
}
```

### Example 3: Returns a range of elements from an array

The example queries `stores` data for "Lakeshore Retail", and finds a subset range from "sales.salesByCategory" array.

```javascript
db.stores.find(
  { "name": "Lakeshore Retail"},
  { "_id":1,"name":1,"sales.salesByCategory": { $slice: [3, 2] } }
)
```

This query returns document from the `stores` collection, with two elements starting from the fourth element of the `sales.salesByCategory` array.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "Toothbrush Holders",
        "totalSales": 47912
      },
      {
        "categoryName": "Hybrid Mattresses",
        "totalSales": 48660
      }
    ]
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
