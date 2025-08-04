---
  title: $zip
  titleSuffix: Overview of the $zip operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $zip operator allows merging two or more arrays element-wise into a single array or arrays.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $zip (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$zip` operator is used to merge two or more arrays element-wise into a single array of arrays. It's useful when you want to combine related elements from multiple arrays into a single array structure.

## Syntax

The syntax for the `$zip` operator is as follows:

```javascript
{
  $zip: {
    inputs: [ <array1>, <array2>, ... ],
    useLongestLength: <boolean>, // Optional
    defaults: <array> // Optional
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`inputs`** | An array of arrays to be merged element-wise. |
| **`useLongestLength`** | A boolean value that, if set to true, uses the longest length of the input arrays. If false or not specified, it uses the shortest length. |
| **`defaults`** | An array of default values to use if `useLongestLength` is true and any input array is shorter than the longest array. |

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
        "categoryName": "Napkins"
      },
      {
        "categoryName": "Pillow Cases",
        "totalSales": 38833
      }
    ]
  }
}
```

### Example 1: Basic Usage

Suppose you want to merge the `categoryName` and `totalSales` fields from the `salesByCategory` array.

```javascript
db.stores.aggregate([
  { $match: {"_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"} },
  {
    $project: {
      name:1,
      categoryNames: "$sales.salesByCategory.categoryName",
      totalSales: "$sales.salesByCategory.totalSales",
      categoryWithSales: {
        $zip: {
          inputs: ["$sales.salesByCategory.categoryName", "$sales.salesByCategory.totalSales"],
          useLongestLength: false
        }
      }
    }
  }
])
```

The query returns individual array of arrays under `categoryWithSales` field. `useLongestLength` set to `true` would return the following output, while a value of `false` removes the `Napkins` array from the output.

```json
{
  "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
  "name": "Lakeshore Retail",
  "categoryNames": [
    "Towel Racks",
    "Washcloths",
    "Face Towels",
    "Toothbrush Holders",
    "Hybrid Mattresses",
    "Napkins",
    "Pillow Cases"
  ],
  "totalSales": [
    13237, 44315,
    42095, 47912,
    48660, 38833
  ],
  "categoryWithSales": [
    ["Towel Racks", 13237],
    ["Washcloths", 44315],
    ["Face Towels", 42095],
    ["Toothbrush Holders", 47912],
    ["Hybrid Mattresses", 48660],
    ["Napkins", null],
    ["Pillow Cases", 38833]
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
