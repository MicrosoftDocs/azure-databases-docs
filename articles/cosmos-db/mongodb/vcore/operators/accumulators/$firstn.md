---
  title: $firstN (accumulator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $firstN operator returns the first N values in a group according to the group's sorting order.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $firstN (accumulator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$firstN` operator returns the first N values in a group according to the group's sorting order. If no sorting order is specified, the order is undefined. It is useful when you want to retrieve the first N documents or values from each group.

## Syntax

The syntax for the `$firstN` operator is as follows:

```javascript
{
  $firstN: {
    n: <expression>,
    input: <expression>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`n`** | An expression that specifies the number of first elements to return. Must be a positive integer. |
| **`input`** | An expression that specifies the values from which to return the first N elements. |

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
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        }
      }
    },
    {
      "eventName": "Fantastic Deal Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 9,
          "Day": 27
        }
      }
    }
  ]
}
```

### Example 1: Get first three stores by total sales

Get the first three stores when sorted by total sales in descending order.

```javascript
db.stores.aggregate([
  { $sort: { "sales.totalSales": -1 } },
  {
    $group: {
      _id: null,
      topThreeStores: {
        $firstN: {
          n: 3,
          input: {
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
    topThreeStores: [
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

### Example 2: Get first two categories per store

Get the first two categories (by sales amount) for each store that has multiple categories.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { $match: { "sales.salesByCategory.totalSales": { $exists: true } } },
  { $sort: { "_id": 1, "sales.salesByCategory.totalSales": -1 } },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      categoryCount: { $sum: 1 },
      firstTwoCategories: {
        $firstN: {
          n: 2,
          input: {
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

This produces output showing the top two categories by sales for each store with multiple categories:

```json
[
  {
    _id: '14343900-2a5c-44bf-a52b-9efe63579866',
    storeName: 'Northwind Traders | Home Improvement Closet - West Evanside',
    categoryCount: 2,
    firstTwoCategories: [
      { categoryName: 'Doors', totalSales: 21108 },
      { categoryName: 'Hardware', totalSales: 14263 }
    ]
  },
  {
    _id: '19ea47b8-4fbd-468c-88f6-133ffa517fad',
    storeName: 'Proseware, Inc. | Grocery Bazaar - North Earnest',
    categoryCount: 2,
    firstTwoCategories: [
      { categoryName: 'Frozen Foods', totalSales: 36967 },
      { categoryName: 'Meat', totalSales: 2724 }
    ]
  },
.
.
.
]
```

### Example 3: Get first two promotion events per store

Get the first two promotion events for each store based on chronological order.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { 
    $sort: { 
      "_id": 1,
      "promotionEvents.promotionalDates.startDate.Year": 1,
      "promotionEvents.promotionalDates.startDate.Month": 1,
      "promotionEvents.promotionalDates.startDate.Day": 1
    }
  },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      eventCount: { $sum: 1 },
      firstTwoEvents: {
        $firstN: {
          n: 2,
          input: {
            eventName: "$promotionEvents.eventName",
            startYear: "$promotionEvents.promotionalDates.startDate.Year",
            startMonth: "$promotionEvents.promotionalDates.startDate.Month"
          }
        }
      }
    }
  },
  { $match: { eventCount: { $gte: 2 } } }
])
```

This returns the first two promotion events chronologically for each store that has multiple events.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
