---
  title: $maxN (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $maxN operator returns the n largest values from an array.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $maxN (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$maxN` operator returns the n largest values from an array. It is useful when you want to find the top performing items based on numerical values, such as the highest sales figures or largest discount percentages.

## Syntax

The syntax for the `$maxN` operator is as follows:

```javascript
{
  $maxN: {
    input: <array>,
    n: <number>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`** | The array from which to return the n largest values. The array should contain numerical values. |
| **`n`** | The number of largest values to return. Must be a positive integer. |

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
  },
  "promotionEvents": [
    {
      "eventName": "Major Bargain Bash",
      "discounts": [
        {
          "categoryName": "Sound Bars",
          "discountPercentage": 9
        },
        {
          "categoryName": "VR Games",
          "discountPercentage": 7
        },
        {
          "categoryName": "Xbox Games",
          "discountPercentage": 25
        },
        {
          "categoryName": "Projector Accessories",
          "discountPercentage": 18
        },
        {
          "categoryName": "Mobile Games",
          "discountPercentage": 8
        },
        {
          "categoryName": "Projector Cases",
          "discountPercentage": 22
        }
      ]
    }
  ]
}
```

### Example 1: Get top three sales values

Suppose you want to find the top 3 sales values from all sales categories.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      topThreeSales: {
        $maxN: {
          input: "$sales.salesByCategory.totalSales",
          n: 3
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
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    topThreeSales: [ 45004, 43522, 32272 ]
  }
]
```

### Example 2: Get highest discount percentages

You can also use `$maxN` to find the highest discount percentages from a promotion event.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  { $unwind: "$promotionEvents" },
  { $match: {"promotionEvents.eventName": "Major Bargain Bash"} },
  {
    $project: {
      name: 1,
      eventName: "$promotionEvents.eventName",
      topTwoDiscounts: {
        $maxN: {
          input: "$promotionEvents.discounts.discountPercentage",
          n: 2
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
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    eventName: 'Major Bargain Bash',
    topTwoDiscounts: [ 25, 22 ]
  }
]
```

### Example 3: Compare top sales across multiple stores

You can use `$maxN` to compare the top sales values across different stores.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      topTwoSales: {
        $maxN: {
          input: "$sales.salesByCategory.totalSales",
          n: 2
        }
      }
    }
  },
  { $limit: 3 }
])
```

This query returns the top two sales values for the first three stores in the collection, making it easy to compare performance across different locations.

```json
[
  {
    _id: 'af9015d8-3f6b-455f-8967-a83cc22ff018',
    name: 'VanArsdel, Ltd. | Party Goods Nook - Kunzeshire',
    topTwoSales: [ 3526 ]
  },
  {
    _id: 'ed319c06-731d-45fc-8a47-b05af8637cdf',
    name: 'Relecloud | Computer Outlet - Langoshfort',
    topTwoSales: [ 46356, 41111 ]
  },
  {
    _id: '62438f5f-0c56-4a21-8c6c-6bfa479494ad',
    name: 'First Up Consultants | Plumbing Supply Shoppe - New Ubaldofort',
    topTwoSales: [ 36202, 32306 ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]