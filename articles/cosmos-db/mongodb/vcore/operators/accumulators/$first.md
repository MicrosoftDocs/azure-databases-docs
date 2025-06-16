---
  title: $first (accumulator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $first operator returns the first value in a group according to the group's sorting order.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $first (accumulator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$first` operator returns the first value in a group according to the group's sorting order. If no sorting order is specified, the order is undefined. It is useful when you want to retrieve the first document or value from each group.

## Syntax

The syntax for the `$first` operator is as follows:

```javascript
{ $first: <expression> }
```

## Parameters

| | Description |
| --- | --- |
| **`<expression>`** | The expression that specifies the value to return from the first document in each group. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
  "name": "First Up Consultants | Bed and Bath Center - South Amir",
  "location": {
    "lat": 60.7954,
    "lon": -142.0012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 18,
      "partTime": 17
    }
  },
  "sales": {
    "totalSales": 37701,
    "salesByCategory": [
      {
        "categoryName": "Mattress Toppers",
        "totalSales": 37701
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Price Drop Palooza",
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

### Example 1: Get first store by store name alphabetically

Get the first store when sorted alphabetically by store name.

```javascript
db.stores.aggregate([
  { $sort: { "name": 1 } },
  {
    $group: {
      _id: null,
      firstStore: {
        $first: {
          storeId: "$_id",
          storeName: "$name",
          totalSales: "$sales.totalSales"
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
    firstStore: {
      storeId: 'c53d4c75-e551-43a6-8752-d85d2a094be4',
      storeName: 'Adatum Corporation | Appliance Bargains - Bufordside',
      totalSales: 82598
    }
  }
]
```

### Example 2: Get first category by sales amount per store

Get the first category (alphabetically) for each store along with store details.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { $sort: { "_id": 1, "sales.salesByCategory.categoryName": 1 } },
  {
    $group: {
      _id: "$_id",
      storeName: { $first: "$name" },
      totalSales: { $first: "$sales.totalSales" },
      firstCategory: {
        $first: {
          categoryName: "$sales.salesByCategory.categoryName",
          categoryTotalSales: "$sales.salesByCategory.totalSales"
        }
      }
    }
  }
])
```

This will produce output showing the first category alphabetically for each store:

```json
[
  {
    _id: '64ec6589-068a-44a6-be5b-9d37bb0a90f1',
    storeName: 'First Up Consultants | Computer Gallery - West Cathrine',
    totalSales: 186829,
    firstCategory: { categoryName: 'Cases', categoryTotalSales: 36386 }
  },
  {
    _id: '14343900-2a5c-44bf-a52b-9efe63579866',
    storeName: 'Northwind Traders | Home Improvement Closet - West Evanside',
    totalSales: 35371,
    firstCategory: { categoryName: 'Doors', categoryTotalSales: 21108 }
  },
.
.
.
]
```

### Example 3: Get first promotion event per store

Get the first promotion event for each store based on start date.

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
      firstPromotionEvent: {
        $first: {
          eventName: "$promotionEvents.eventName",
          startYear: "$promotionEvents.promotionalDates.startDate.Year",
          startMonth: "$promotionEvents.promotionalDates.startDate.Month"
        }
      }
    }
  }
])
```

This will return the earliest promotion event for each store based on the start date.

```javascript
[
  {
    _id: '64ec6589-068a-44a6-be5b-9d37bb0a90f1',
    storeName: 'First Up Consultants | Computer Gallery - West Cathrine',
    firstPromotionEvent: {
      eventName: 'Crazy Markdown Madness',
      startYear: 2024,
      startMonth: 6
    }
  },
  {
    _id: 'a58d0356-493b-44e6-afab-260aa3296930',
    storeName: 'Fabrikam, Inc. | Outdoor Furniture Nook - West Lexie',
    firstPromotionEvent: { eventName: 'Price Drop Palooza', startYear: 2023, startMonth: 9 }
  },
.
.
.
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
