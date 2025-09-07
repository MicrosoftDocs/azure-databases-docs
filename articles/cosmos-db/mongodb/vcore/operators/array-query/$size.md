---
title: $size
titleSuffix: Overview of the $size operator in Azure Cosmos DB for MongoDB (vCore)
description: The $size operator is used to query documents where an array field has a specified number of elements.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/28/2024
---

# $size

The `$size` operator is used to query documents where an array field has a specified number of elements. This operator is useful when you need to find documents based on the size of an array field, such as finding documents with some items in a list.

## Syntax

```javascript
db.collection.find({ <field>: { $size: <number> } })
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field that contains the array. |
| **`number`** | The number of elements the array should have. |

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

### Example 1: Finding documents with a specific number of elements in an array

The example retrieves documents from the `stores` collection where the `sales.salesByCategory` array contains exactly seven items.

```javascript
db.stores.find(  { "sales.salesByCategory": { $size: 7 }}
                ,{"_id":1,"name":1,"sales.salesByCategory":1}
                ).limit(2)
```

This query returns the two documents from the `stores` collection as restricted by `limit` clause.

```json
{
  "_id": "7ed4b356-1290-433e-bd96-bf95f817eaaa",
  "name": "Wide World Importers",
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "Ultrabooks",
        "totalSales": 31304
      },
      {
        "categoryName": "Laptop Accessories",
        "totalSales": 10044
      },
      {
        "categoryName": "Laptops",
        "totalSales": 48851
      },
      {
        "categoryName": "Refill Kits",
        "totalSales": 9604
      },
      {
        "categoryName": "Prepaid Phones",
        "totalSales": 28600
      },
      {
        "categoryName": "Android Phones",
        "totalSales": 4580
      },
      {
        "categoryName": "Photo Printers",
        "totalSales": 35234
      }
    ]
  }
}
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
    ]
  }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
