---
title: $avg
titleSuffix: Overview of the $avg operator in Azure Cosmos DB for MongoDB vCore
description: Computes the average of numeric values for documents in a group, bucket, or window.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $avg

The `$avg` accumulator computes the average of numeric values. It is commonly used in aggregation pipelines, such as `$group`, `$bucket`, `$bucketAuto`, or `$setWindowFields`. This operation is helpful for calculating average values across groups of documents or within defined windows.

## Syntax

```javascript
$avg: <expression>
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<expression>`** | Specifies the field or expression to calculate the average. Non-numeric values are ignored. |

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

### Example 1: Calculate the average sales by category

This example calculates the average `totalSales` for each `categoryName` in the `salesByCategory` array.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  { 
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      avgSales: { $avg: "$sales.salesByCategory.totalSales" }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 'Christmas Trees', avgSales: 25987.956989247312 },
  { _id: 'Nuts', avgSales: 25115.98795180723 },
  { _id: 'Camping Tables', avgSales: 25012.546153846153 },
  { _id: 'Music Theory Books', avgSales: 26138.80769230769 },
  { _id: 'Fortified Wine', avgSales: 24748.672727272726 },
  { _id: "Children's Mystery", avgSales: 23764.044444444444 },
  { _id: 'Short Throw Projectors', avgSales: 27157.472222222223 },
  { _id: 'Pliers', avgSales: 26712.875 },
  { _id: 'Bluetooth Headphones', avgSales: 26311.58653846154 },
  { _id: 'Video Storage', avgSales: 26121.475 },
  { _id: 'Cleansers', avgSales: 25836.397058823528 },
  { _id: 'Camera Straps', avgSales: 22487.609375 },
  { _id: 'Carry-On Bags', avgSales: 24294.263157894737 },
  { _id: 'Disinfectant Wipes', avgSales: 27066.929411764704 },
  { _id: 'Insignia Smart TVs', avgSales: 27096.83950617284 },
  { _id: 'Toner Refill Kits', avgSales: 24963.71052631579 },
  { _id: 'iPads', avgSales: 22583.882352941175 },
  { _id: 'Memory Foam Mattresses', avgSales: 28073.05172413793 },
  { _id: 'Storage Baskets', avgSales: 24092.514705882353 },
  { _id: 'Body Spray', avgSales: 26080.84375 }
]
```

### Example 2: Using `$avg` in `$bucket`

This example creates buckets based on sales values and calculates the avg sales value for each bucket.

```javascript
db.stores.aggregate([
  {
    $bucket: {
      groupBy: "$sales.totalSales",
      boundaries: [0, 1000, 5000, 10000],
      default: "Other",
      output: {
        avgSales: { $avg: "$sales.totalSales" }
      }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 1000, avgSales: 3029.053674121406 },
  { _id: 'Other', avgSales: 52169.85442987472 },
  { _id: 0, avgSales: 576.3164179104477 },
  { _id: 5000, avgSales: 7538.786819770345 }
]
```
### Example 3: Using `$avg` in `$setWindowFields`

To get the average discount for the category "Laptops" by company, in the year 2023:

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
        avgDiscount: {
          $avg: "$promotionEvents.discounts.discountPercentage",
          window: { documents: ["unbounded", "unbounded"] }
        }
      }
    }
  },

  // Group by city to return one result per city
  {
    $group: {
      _id: "$company",
      avgDiscount: { $first: "$avgDiscount" }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 'Boulder Innovations', avgDiscount: 14.5 },
  { _id: 'VanArsdel, Ltd.', avgDiscount: 14.461538461538462 },
  { _id: 'Proseware, Inc.', avgDiscount: 16.25 },
  { _id: 'Fabrikam, Inc.', avgDiscount: 14.454545454545455 },
  { _id: 'Contoso, Ltd.', avgDiscount: 14.384615384615385 },
  { _id: 'Fourth Coffee', avgDiscount: 13.625 },
  { _id: 'Trey Research', avgDiscount: 17.785714285714285 },
  { _id: 'Adatum Corporation', avgDiscount: 11.666666666666666 },
  { _id: 'Relecloud', avgDiscount: 14.375 },
  { _id: 'Lakeshore Retail', avgDiscount: 15.846153846153847 },
  { _id: 'Northwind Traders', avgDiscount: 14.2 },
  { _id: 'First Up Consultants', avgDiscount: 11.25 },
  { _id: 'Wide World Importers', avgDiscount: 15.571428571428571 },
  { _id: 'Tailwind Traders', avgDiscount: 16.166666666666668 }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]