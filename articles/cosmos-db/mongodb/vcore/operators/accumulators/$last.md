---
  title: $last (accumulator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $last accumulator operator returns the last value in a group of documents.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $last (accumulator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$last` accumulator operator returns the last value in a group of documents for a specified expression. It is commonly used in `$group` stages to get the final value from a sorted collection of documents.

## Syntax

The syntax for the `$last` accumulator operator is as follows:

```javascript
{
  $group: {
    _id: <expression>,
    <field>: { $last: <expression> }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<expression>`** | The expression that specifies the field or value to return the last occurrence of. |

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
  },
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        },
        "endDate": {
          "Year": 2023,
          "Month": 7,
          "Day": 9
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
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      }
    }
  ]
}
```

### Example 1: Get Last Promotion Event by Date

Get the most recent promotion event for each store by grouping stores and finding the last promotion event when sorted by date.

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
      lastPromotionEvent: { $last: "$promotionEvents.eventName" },
      lastPromotionStartDate: { $last: "$promotionEvents.promotionalDates.startDate" }
    }
  }
])
```

This will produce output showing the most recent promotion event for each store:

```json
[
  {
    _id: '64ec6589-068a-44a6-be5b-9d37bb0a90f1',
    storeName: 'First Up Consultants | Computer Gallery - West Cathrine',
    lastPromotionEvent: 'Blowout Bargain Bash',
    lastPromotionStartDate: { Year: 2024, Month: 9, Day: 21 }
  },
  {
    _id: 'a58d0356-493b-44e6-afab-260aa3296930',
    storeName: 'Fabrikam, Inc. | Outdoor Furniture Nook - West Lexie',
    lastPromotionEvent: 'Big Bargain Bash',
    lastPromotionStartDate: { Year: 2024, Month: 9, Day: 21 }
  },
.
.
.
]
```

### Example 2: Get Last Sales Category by Sales Amount

Find the highest-selling category (last when sorted by sales amount) for each store.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { $sort: { "sales.salesByCategory.totalSales": 1 } },
  {
    $group: {
      _id: "$_id",
      storeName: { $last: "$name" },
      topSellingCategory: { $last: "$sales.salesByCategory.categoryName" },
      topSalesAmount: { $last: "$sales.salesByCategory.totalSales" }
    }
  }
])
```

This will return the category with the highest sales for each store:

```json
[
  {
    _id: '2e07b49d-1730-491b-b847-44b6a34812c1',
    storeName: 'VanArsdel, Ltd. | Electronics Market - North Bransonborough',
    topSellingCategory: 'iPads',
    topSalesAmount: 37113
  },
  {
    _id: '4a99546f-a1d2-4e61-ae9f-b8c7c1faf73c',
    storeName: 'Lakeshore Retail | Stationery Nook - West Van',
    topSellingCategory: 'Pencils',
    topSalesAmount: 33447
  },
.
.
.
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]