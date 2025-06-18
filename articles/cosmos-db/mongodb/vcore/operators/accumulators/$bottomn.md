---
  title: $bottomN (accumulator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $bottomN operator returns the bottom N elements in a group according to a specified sort order.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $bottomN (accumulator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bottomN` operator returns the bottom N elements in a group according to a specified sort order. It's useful when you want to find the lowest-ranked N documents based on certain criteria within each group.

## Syntax

The syntax for the `$bottomN` operator is as follows:

```javascript
{
  $bottomN: {
    n: <expression>,
    sortBy: { <field1>: <sort order>, <field2>: <sort order>, ... },
    output: <expression>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`n`** | An expression that specifies the number of bottom elements to return. Must be a positive integer. |
| **`sortBy`** | Specifies the fields to sort by and the sort order. Use 1 for ascending order and -1 for descending order. |
| **`output`** | An expression that specifies the output for elements in the bottom of the sort order. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      },
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272
      }
    ]
  }
}
```

### Example 1: Find bottom three stores by total sales

Find the three stores with the lowest total sales.

```javascript
db.stores.aggregate([
  {
    $group: {
      _id: null,
      bottomThreeStores: {
        $bottomN: {
          n: 3,
          sortBy: { "sales.totalSales": 1 },
          output: {
            storeId: "$_id",
            storeName: "$name",
            totalSales: "$sales.totalSales"
          }
        }
      }
    }
  }
])
```

This produces the following output:

```json
[
  {
    _id: null,
    bottomThreeStores: [
      {
        storeId: '27d12c50-ef9b-4a1e-981f-2eb46bf68c70',
        storeName: 'Boulder Innovations | Electronics Closet - West Freddy',
        totalSales: 404106
      },
      {
        storeId: 'ffe155dd-caa2-4ac1-8ec9-0342241a84a3',
        storeName: 'Lakeshore Retail | Electronics Stop - Vicentastad',
        totalSales: 399426
      },
      {
        storeId: 'cba62761-10f8-4379-9eea-a9006c667927',
        storeName: 'Fabrikam, Inc. | Electronics Nook - East Verlashire',
        totalSales: 374845
      }
    ]
  }
]
```

### Example 2: Find bottom two categories per store

Find the two categories with the lowest sales in each store that has multiple categories.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { $match: { "sales.salesByCategory.totalSales": { $exists: true } } },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      categoryCount: { $sum: 1 },
      bottomTwoCategories: {
        $bottomN: {
          n: 2,
          sortBy: { "sales.salesByCategory.totalSales": 1 },
          output: {
            categoryName: "$sales.salesByCategory.categoryName",
            totalSales: "$sales.salesByCategory.totalSales"
          }
        }
      }
    }
  },
  { $match: { categoryCount: { $gte: 2 } } }
])
```

This produces output showing the bottom two categories for each store with multiple categories:

```json
[
  {
    _id: '4a99546f-a1d2-4e61-ae9f-b8c7c1faf73c',
    storeName: 'Lakeshore Retail | Stationery Nook - West Van',
    categoryCount: 2,
    bottomTwoCategories: [
      { categoryName: 'Pencils', totalSales: 33447 },
      { categoryName: 'Rulers', totalSales: 2234 }
    ]
  },
  {
    _id: '7b09ecb8-ba2a-4595-b313-67cfd732379f',
    storeName: 'VanArsdel, Ltd. | DJ Equipment Bazaar - Kiehnside',
    categoryCount: 2,
    bottomTwoCategories: [
      { categoryName: 'DJ Headphones', totalSales: 46705 },
      { categoryName: 'DJ Software', totalSales: 19949 }
    ]
  }
.
.
.
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
