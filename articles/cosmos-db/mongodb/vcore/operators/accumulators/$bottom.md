---
  title: $bottom
  titleSuffix: Overview of the $bottom operator in Azure Cosmos DB for MongoDB vCore
  description: The $bottom operator returns the bottom elements in a group according to a specified sort order.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $bottom

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$bottom` operator returns the bottom elements in a group according to a specified sort order. It is useful when you want to find the lowest-ranked documents based on certain criteria within each group.

## Syntax

The syntax for the `$bottom` operator is as follows:

```javascript
{
  $bottom: {
    sortBy: { <field1>: <sort order>, <field2>: <sort order>, ... },
    output: <expression>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`sortBy`** | Specifies the field(s) to sort by and the sort order. Use 1 for ascending order and -1 for descending order. |
| **`output`** | An expression that specifies the output for elements in the bottom of the sort order. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
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

### Example 1: Find store with lowest total sales

Find the store with the lowest total sales among all stores.

```javascript
db.stores.aggregate([
  {
    $group: {
      _id: null,
      bottomStore: {
        $bottom: {
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

This will produce the following output:

```json
[
  {
    _id: null,
    bottomStore: {
      storeId: '27d12c50-ef9b-4a1e-981f-2eb46bf68c70',
      storeName: 'Boulder Innovations | Electronics Closet - West Freddy',
      totalSales: 404106
    }
  }
]
```

### Example 2: Find lowest performing category per store

Find the category with the lowest sales in each store that has multiple categories.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { $match: { "sales.salesByCategory.totalSales": { $exists: true } } },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      lowestCategory: {
        $bottom: {
          sortBy: { "sales.salesByCategory.totalSales": 1 },
          output: {
            categoryName: "$sales.salesByCategory.categoryName",
            totalSales: "$sales.salesByCategory.totalSales"
          }
        }
      }
    }
  }
])
```

This will produce output showing the lowest performing category for each store:

```json
[
  {
    _id: 'b1d86d1f-8705-4157-b64c-a9eda0df4921',
    storeName: 'VanArsdel, Ltd. | Baby Products Haven - West Kingfort',
    lowestCategory: { categoryName: 'Baby Monitors', totalSales: 49585 }
  },
  {
    _id: '22e6367e-8341-415f-9795-118d2b522abf',
    storeName: 'Adatum Corporation | Outdoor Furniture Mart - Port Simone',
    lowestCategory: { categoryName: 'Outdoor Benches', totalSales: 4976 }
  },
.
.
.
.
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
