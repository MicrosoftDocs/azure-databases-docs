---
title: $sum accumulator operator 
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Aggregation operator to calculate the sum of numeric values.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $sum

The `$sum` operator is an aggregation operator used in MongoDB to calculate the sum of numeric values. It is commonly employed within aggregation pipelines, such as `$group`, `$bucket`, `$bucketAuto`, and `$setWindowFields`. It is a versatile operator that helps summarize data effectively in various use cases, such as calculating totals, averages, or other derived metrics.

## Syntax

```javascript
{
  $sum: <expression>
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`<expression>`** | The expression to evaluate and sum. This can be a field path, a numeric value, or another expression. |

## Examples

Let's understand the usage with documents structured according to this schema.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}

```

### Example 1: Using `$sum` in `$group`

To compute total discount percentage per category across all promotion events in 2023.

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $match: {
      "promotionEvents.promotionalDates.startDate.Year": 2023
    }
  },
  {
    $group: {
      _id: "$promotionEvents.discounts.categoryName",
      totalDiscountIn2023: {
        $sum: "$promotionEvents.discounts.discountPercentage"
      }
    }
  },
  {
    $project: {
      _id: 0,
      categoryName: "$_id",
      totalDiscountIn2023: 1
    }
  }
])

```

This query would return the following document.

```json
{
  "categoryName": "Glass Frames",
  "totalDiscountIn2023": 25
}
{
  "categoryName": "Picture Hanging Supplies",
  "totalDiscountIn2023": 14
}

```

### Example 2:  Using `$min` in `$bucket`

Grouping by Sales Ranges and Summing totalSales:

```javascript
db.stores.aggregate([
  {
    $bucket: {
      groupBy: "$sales.totalSales",  // Field to group by
      boundaries: [0, 10000, 20000, 50000, 100000],  // Sales ranges
      default: "Other",  // Default bucket for values outside the defined ranges
      output: {
        totalSalesSum: { $sum: "$sales.totalSales" },  // Sum the sales for each bucket
        count: { $sum: 1 }  // Count the number of documents in each bucket
      }
    }
  }
])

```

This query would return the following document.

```json
[
  { _id: 'Other', totalSalesSum: 454981695, count: 3001 },
  { _id: 0, totalSalesSum: 20033725, count: 3903 },
  { _id: 10000, totalSalesSum: 71303703, count: 4712 },
  { _id: 50000, totalSalesSum: 756168541, count: 11025 },
  { _id: 20000, totalSalesSum: 678976078, count: 18861 }
]
```

### Example 3: Using `$sum` in `$setWindowFields`

To calculate total discount per categoryName for promotions in 2023

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },
  {
    $match: {
      "promotionEvents.promotionalDates.startDate.Year": 2023
    }
  },
  {
    $setWindowFields: {
      partitionBy: "$promotionEvents.discounts.categoryName",  // Group by categoryName
      output: {
        totalDiscountIn2023: {
          $sum: "$promotionEvents.discounts.discountPercentage",  // Sum discount percentage
          window: {
            documents: ["unbounded", "unbounded"]  // Aggregate over all documents in the partition
          }
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      categoryName: "$promotionEvents.discounts.categoryName",
      discountPercentage: "$promotionEvents.discounts.discountPercentage",
      totalDiscountIn2023: 1
    }
  },
  { $limit: 5 }
])

```

This query would return the following document.

```json
[
  {
    totalDiscountIn2023: 1106,
    categoryName: '2-in-1 Laptops',
    discountPercentage: 25
  },
  {
    totalDiscountIn2023: 1106,
    categoryName: '2-in-1 Laptops',
    discountPercentage: 22
  },
  {
    totalDiscountIn2023: 1106,
    categoryName: '2-in-1 Laptops',
    discountPercentage: 19
  },
  {
    totalDiscountIn2023: 1106,
    categoryName: '2-in-1 Laptops',
    discountPercentage: 17
  },
  {
    totalDiscountIn2023: 1106,
    categoryName: '2-in-1 Laptops',
    discountPercentage: 10
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]