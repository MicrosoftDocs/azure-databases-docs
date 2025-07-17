---
  title: $firstN (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $firstN operator returns the first n elements from an array.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $firstN (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$firstN` operator returns the first n elements from an array. It is useful when you want to limit the number of elements returned from the beginning of an array, such as getting the top few items from a list.

## Syntax

The syntax for the `$firstN` operator is as follows:

```javascript
{
  $firstN: {
    input: <array>,
    n: <number>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`** | The array from which to return the first n elements. |
| **`n`** | The number of elements to return from the beginning of the array. Must be a positive integer. |

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

### Example 1: Get first three sales categories

Suppose you want to get the first three sales categories for analysis.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      firstThreeCategories: {
        $firstN: {
          input: "$sales.salesByCategory",
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
    totalSales: 151864,
    firstThreeCategories: [
      { categoryName: 'Sound Bars', totalSales: 2120 },
      { categoryName: 'Home Theater Projectors', totalSales: 45004 },
      { categoryName: 'Game Controllers', totalSales: 43522 }
    ]
  }
]
```

### Example 2: Get first two promotion events

You can also use `$firstN` to get the first few promotion events from a store.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      firstTwoPromotions: {
        $firstN: {
          input: "$promotionEvents",
          n: 2
        }
      }
    }
  }
])
```

This returns the first two promotion events with their complete details including event names, promotional dates, and discount information.

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    firstTwoPromotions: [
      {
        eventName: 'Massive Markdown Mania',
        promotionalDates: {
          startDate: { Year: 2023, Month: 6, Day: 29 },
          endDate: { Year: 2023, Month: 7, Day: 9 }
        },
        discounts: [
          { categoryName: 'DVD Players', discountPercentage: 14 },
          { categoryName: 'Projector Lamps', discountPercentage: 6 },
          { categoryName: 'Media Players', discountPercentage: 21 },
          { categoryName: 'Blu-ray Players', discountPercentage: 21 },
          {
            categoryName: 'Home Theater Systems',
            discountPercentage: 5
          },
          { categoryName: 'Televisions', discountPercentage: 22 }
        ]
      },
      {
        eventName: 'Fantastic Deal Days',
        promotionalDates: {
          startDate: { Year: 2023, Month: 9, Day: 27 },
          endDate: { Year: 2023, Month: 10, Day: 7 }
        },
        discounts: [
          { categoryName: 'TV Mounts', discountPercentage: 15 },
          { categoryName: 'Game Accessories', discountPercentage: 25 },
          {
            categoryName: 'Portable Projectors',
            discountPercentage: 25
          },
          { categoryName: 'Projector Screens', discountPercentage: 21 },
          { categoryName: 'Blu-ray Players', discountPercentage: 20 },
          { categoryName: 'DVD Players', discountPercentage: 21 }
        ]
      }
    ]
  }
]
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]