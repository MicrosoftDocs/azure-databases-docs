---
  title: $topN
  titleSuffix: Overview of the $topN operator in Azure Cosmos DB for MongoDB vCore
  description: The $topN accumulator operator returns the top N elements from a group based on a specified sort order.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $topN

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$topN` accumulator operator returns the top N elements from a group based on a specified sort order. It extends the functionality of `$top` by allowing you to retrieve multiple top elements instead of just the single highest-ranked item.

## Syntax

The syntax for the `$topN` accumulator operator is as follows:

```javascript
{
  $group: {
    _id: <expression>,
    <field>: { 
      $topN: {
        n: <number>,
        sortBy: { <field1>: <sort order>, <field2>: <sort order>, ... },
        output: <expression>
      }
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`n`** | The number of elements to return. Must be a positive integer. |
| **`sortBy`** | Specifies the sort order using a document with field names and sort directions (1 for ascending, -1 for descending). |
| **`output`** | The expression that specifies the field or value to return from the top N documents. |

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
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        },
        {
          "categoryName": "Media Players",
          "discountPercentage": 21
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 22
        }
      ]
    }
  ]
}
```

### Example 1: Get top three selling categories per store

Find the top three highest-selling categories for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      top3Categories: {
        $topN: {
          n: 3,
          sortBy: { "sales.salesByCategory.totalSales": -1 },
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

This produces output showing the top three selling categories for each store:

```json
[
  {
    _id: '8c8f23c9-1893-4ddd-97ad-dd57088058a5',
    storeName: 'Proseware, Inc. | Camera Haven - North Jerroldville',
    top3Categories: [
      { categoryName: 'Waterproof Camcorders', totalSales: 25237 },
      { categoryName: 'Camera Lenses', totalSales: 21189 },
      { categoryName: 'Action Camcorders', totalSales: 19467 }
    ]
  },
  {
    _id: '7f0b0454-e22b-4646-8eb4-32ad5eb48042',
    storeName: 'First Up Consultants | Tool Boutique - Paoloberg',
    top3Categories: [
      { categoryName: 'Drills', totalSales: 40686 },
      { categoryName: 'Screwdrivers', totalSales: 30155 },
      { categoryName: 'Chisels', totalSales: 15762 }
    ]
  },
.
.
.
]
```

### Example 2: Get top two recent promotion events

Find the two most recent promotion events for each store based on start date.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      top2RecentPromotions: {
        $topN: {
          n: 2,
          sortBy: { 
            "promotionEvents.promotionalDates.startDate.Year": -1,
            "promotionEvents.promotionalDates.startDate.Month": -1,
            "promotionEvents.promotionalDates.startDate.Day": -1
          },
          output: {
            eventName: "$promotionEvents.eventName",
            startDate: "$promotionEvents.promotionalDates.startDate"
          }
        }
      }
    }
  }
])
```

This returns the two most recent promotion events for each store:

```json
[
  {
    _id: '4a99546f-a1d2-4e61-ae9f-b8c7c1faf73c',
    storeName: 'Lakeshore Retail | Stationery Nook - West Van',
    top2RecentPromotions: [
      {
        eventName: 'Crazy Markdown Madness',
        startDate: { Year: 2024, Month: 9, Day: 21 }
      },
      {
        eventName: 'Flash Sale Fiesta',
        startDate: { Year: 2024, Month: 6, Day: 23 }
      }
    ]
  },
  {
    _id: 'e0c47a06-4fe0-46b7-a309-8971bbb3978f',
    storeName: 'VanArsdel, Ltd. | Baby Products Bargains - Elainamouth',
    top2RecentPromotions: [
      {
        eventName: 'Crazy Deal Days',
        startDate: { Year: 2024, Month: 9, Day: 21 }
      }
    ]
  },
.
.
.
]
```

### Example 3: Get top five highest discounts by category

Find the top five categories with the highest discount percentages across all promotion events for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      top5Discounts: {
        $topN: {
          n: 5,
          sortBy: { "promotionEvents.discounts.discountPercentage": -1 },
          output: {
            categoryName: "$promotionEvents.discounts.categoryName",
            discountPercentage: "$promotionEvents.discounts.discountPercentage",
            eventName: "$promotionEvents.eventName"
          }
        }
      }
    }
  }
])
```

This shows the top five categories with highest discount percentages for each store:

```json
[
  {
    _id: '4a99546f-a1d2-4e61-ae9f-b8c7c1faf73c',
    storeName: 'Lakeshore Retail | Stationery Nook - West Van',
    top5Discounts: [
      {
        categoryName: 'Rulers',
        discountPercentage: 24,
        eventName: 'Markdown Madness'
      },
      {
        categoryName: 'Notebooks',
        discountPercentage: 21,
        eventName: 'Markdown Madness'
      },
      {
        categoryName: 'Paper Clips',
        discountPercentage: 17,
        eventName: 'Flash Sale Fiesta'
      },
      {
        categoryName: 'Pencils',
        discountPercentage: 15,
        eventName: 'Bargain Blitz Bash'
      },
      {
        categoryName: 'Erasers',
        discountPercentage: 14,
        eventName: 'Crazy Markdown Madness'
      }
    ]
  },
.
.
.
]
```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
