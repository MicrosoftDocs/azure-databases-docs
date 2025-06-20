---
title: $max
titleSuffix: Overview of the $max operator in Azure Cosmos DB for MongoDB vCore
description: The $max accumulator operator returns the maximum value from a set of input values.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $max

The `$max` operator is an accumulator that returns the maximum value from a set of input values. It is commonly used in conjunction with aggregation stages such as `$group`, `$bucket`, `$bucketAuto`, or `$setWindowFields`. This operator is particularly useful for identifying the highest value in a dataset, such as maximum sales, maximum discounts, or other numerical comparisons.

## Syntax
```javascript
$max: <expression>
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`<expression>`** | Any valid expression that resolves to a value. The `$max` operator evaluates this expression to determine the maximum value. |

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

### Example 1: Calculate the maximum sales by category

This example calculates the maximum `totalSales` for each `categoryName` in the `salesByCategory` array.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { 
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      maxSales: { $max: "$sales.salesByCategory.totalSales" }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 'Christmas Trees', maxSales: 49697 },
  { _id: 'Nuts', maxSales: 48020 },
  { _id: 'Camping Tables', maxSales: 48568 },
  { _id: 'Music Theory Books', maxSales: 46133 },
  { _id: 'Fortified Wine', maxSales: 49912 },
  { _id: "Children's Mystery", maxSales: 48984 },
  { _id: 'Short Throw Projectors', maxSales: 49840 },
  { _id: 'Pliers', maxSales: 49270 },
  { _id: 'Bluetooth Headphones', maxSales: 49618 },
  { _id: 'Video Storage', maxSales: 49793 },
  { _id: 'Cleansers', maxSales: 49960 },
  { _id: 'Camera Straps', maxSales: 48156 },
  { _id: 'Carry-On Bags', maxSales: 49939 },
  { _id: 'Disinfectant Wipes', maxSales: 49906 },
  { _id: 'Insignia Smart TVs', maxSales: 49029 },
  { _id: 'Toner Refill Kits', maxSales: 46303 },
  { _id: 'iPads', maxSales: 49597 },
  { _id: 'Memory Foam Mattresses', maxSales: 49534 },
  { _id: 'Storage Baskets', maxSales: 48456 },
  { _id: 'Body Spray', maxSales: 49471 }
]
```

### Example 2: Using `$max` in `$bucket`

This example creates buckets based on sales values and calculates the avg sales value for each bucket.

```javascript
db.stores.aggregate([
  {
    $bucket: {
      groupBy: "$sales.totalSales",
      boundaries: [0, 1000, 5000, 10000],
      default: "Other",
      output: {
        maxSales: { $max: "$sales.totalSales" }
      }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 1000, maxSales: 4996 },
  { _id: 'Other', maxSales: 404106 },
  { _id: 0, maxSales: 995 },
  { _id: 5000, maxSales: 9999 }
]
```
### Example 3: Using `$max` in `$setWindowFields`

To get the maximum discount for the category "Laptops" by company, in the year 2023:

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },

  // Filter only Laptops category and events in 2023
  {
    $match: {
      "promotionEvents.promotionalDates.startDate.Year": 2023,
      "promotionEvents.discounts.categoryName": "Laptops"
    }
  },

  // Use $setWindowFields to calculate average discount by city
  {
    $setWindowFields: {
      partitionBy: "$company",
      output: {
        maxDiscount: {
          $max: "$promotionEvents.discounts.discountPercentage",
          window: { documents: ["unbounded", "unbounded"] }
        }
      }
    }
  },

  // Group by city to return one result per city
  {
    $group: {
      _id: "$company",
      maxDiscount: { $first: "$maxDiscount" }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 'Boulder Innovations', maxDiscount: 24 },
  { _id: 'VanArsdel, Ltd.', maxDiscount: 24 },
  { _id: 'Proseware, Inc.', maxDiscount: 24 },
  { _id: 'Fabrikam, Inc.', maxDiscount: 23 },
  { _id: 'Contoso, Ltd.', maxDiscount: 24 },
  { _id: 'Fourth Coffee', maxDiscount: 18 },
  { _id: 'Trey Research', maxDiscount: 24 },
  { _id: 'Adatum Corporation', maxDiscount: 17 },
  { _id: 'Relecloud', maxDiscount: 22 },
  { _id: 'Lakeshore Retail', maxDiscount: 25 },
  { _id: 'Northwind Traders', maxDiscount: 18 },
  { _id: 'First Up Consultants', maxDiscount: 15 },
  { _id: 'Wide World Importers', maxDiscount: 25 },
  { _id: 'Tailwind Traders', maxDiscount: 25 }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]