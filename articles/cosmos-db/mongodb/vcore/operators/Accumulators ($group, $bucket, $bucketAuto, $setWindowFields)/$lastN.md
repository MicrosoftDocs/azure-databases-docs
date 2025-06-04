---
  title: $lastN (accumulator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $lastN accumulator operator returns the last N values in a group of documents.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $lastN (accumulator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$lastN` accumulator operator returns the last N values in a group of documents for a specified expression. It is useful when you need to retrieve multiple final values from a sorted collection rather than just the single last value.

## Syntax

The syntax for the `$lastN` accumulator operator is as follows:

```javascript
{
  $group: {
    _id: <expression>,
    <field>: { 
      $lastN: {
        input: <expression>,
        n: <number>
      }
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`** | The expression that specifies the field or value to return the last N occurrences of. |
| **`n`** | The number of values to return. Must be a positive integer. |

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
    },
    {
      "eventName": "Major Bargain Bash",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        }
      }
    }
  ]
}
```

### Example 1: Get Last 2 Promotion Events by Date

Retrieve the two most recent promotion events for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $sort: { 
      "promotionEvents.promotionalDates.startDate.Year": 1,
      "promotionEvents.promotionalDates.startDate.Month": 1,
      "promotionEvents.promotionalDates.startDate.Day": 1
    }
  },
  {
    $group: {
      _id: "$_id",
      storeName: { $last: "$name" },
      lastTwoPromotions: { 
        $lastN: {
          input: "$promotionEvents.eventName",
          n: 2
        }
      },
      lastTwoPromotionDates: {
        $lastN: {
          input: "$promotionEvents.promotionalDates.startDate",
          n: 2
        }
      }
    }
  }
])
```

This will produce output showing the two most recent promotion events for each store:

```json
[
  {
    _id: 'e28fff9b-a8fb-4ac9-bb37-dea60d2a7d32',
    storeName: 'Lakeshore Retail | Outdoor Furniture Collection - Erdmanside',
    lastTwoPromotions: [ 'Big Bargain Bash', 'Spectacular Savings Showcase' ],
    lastTwoPromotionDates: [
      { Year: 2024, Month: 9, Day: 21 },
      { Year: 2024, Month: 6, Day: 23 }
    ]
  },
  {
    _id: '1bec7539-dc75-4f7e-b4e8-afdf8ff2f234',
    storeName: 'Adatum Corporation | Health Food Market - East Karina',
    lastTwoPromotions: [ 'Price Slash Spectacular', 'Spectacular Savings Showcase' ],
    lastTwoPromotionDates: [
      { Year: 2024, Month: 9, Day: 21 },
      { Year: 2024, Month: 6, Day: 23 }
    ]
  },
.
.
.
]
```

### Example 2: Get Top 3 Selling Categories

Find the top 3 highest-selling categories for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { $sort: { "sales.salesByCategory.totalSales": 1 } },
  {
    $group: {
      _id: "$_id",
      storeName: { $last: "$name" },
      top3Categories: { 
        $lastN: {
          input: "$sales.salesByCategory.categoryName",
          n: 3
        }
      },
      top3SalesAmounts: {
        $lastN: {
          input: "$sales.salesByCategory.totalSales",
          n: 3
        }
      }
    }
  }
])
```

This will return the top 3 categories with highest sales for each store:

```json
[
  {
    _id: '22e6367e-8341-415f-9795-118d2b522abf',
    storeName: 'Adatum Corporation | Outdoor Furniture Mart - Port Simone',
    top3Categories: [ 'Outdoor Benches' ],
    top3SalesAmounts: [ 4976 ]
  },
  {
    _id: 'a00a3ccd-49a2-4e43-b0d9-e56b96113ed0',
    storeName: 'Wide World Importers | Smart Home Deals - Marcuschester',
    top3Categories: [ 'Smart Thermostats', 'Smart Plugs' ],
    top3SalesAmounts: [ 38696, 633 ]
  },
.
.
.
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]