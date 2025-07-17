---
title: $count
titleSuffix: Overview of the $count operator in Azure Cosmos DB for MongoDB vCore
description: The `$count` accumulator is used to count the number of documents or groupings in a pipeline stage.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 01/05/2025
---

# $count

The `$count` operator is an accumulator used in aggregation pipelines to count the number of documents or groupings. It is commonly used in stages such as `$group`, `$bucket`, `$bucketAuto`, or `$setWindowFields`. This operator is useful for summarizing data or generating counts for specific groupings.

## Syntax

```javascript
{
  $count: "<fieldName>"
}
```

- `<fieldName>`: Specifies the name of the output field that will store the count.

## Parameters

| Parameter      | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **`<fieldName>`** | The name of the field in the output document where the count will be stored.|

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

### Example 1: Count the Total Number of Documents
The following pipeline counts the total number of documents in a collection.

```javascript
db.stores.aggregate([
  {
    $count: "totalDocuments"
  }
])
```

This query would return the following document.

```json
[
 { totalDocuments: 41501 }
]
```

---

### Example 2: Count Documents Grouped by a Field
The following pipeline uses `$group` to count the number of documents for each `categoryName` in the `salesByCategory`.

```javascript
db.stores.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  },
  {
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      totalCount: { $count: {} }
    }
  }
])
```

This query would return the following document.

```json
[
  { _id: 'Christmas Trees', totalCount: 93 },
  { _id: 'Nuts', totalCount: 83 },
  { _id: 'Camping Tables', totalCount: 130 },
  { _id: 'Music Theory Books', totalCount: 52 },
  { _id: 'Fortified Wine', totalCount: 55 },
  { _id: "Children's Mystery", totalCount: 45 },
  { _id: 'Short Throw Projectors', totalCount: 72 },
  { _id: 'Pliers', totalCount: 56 },
  { _id: 'Bluetooth Headphones', totalCount: 104 },
  { _id: 'Video Storage', totalCount: 80 },
  { _id: 'Cleansers', totalCount: 68 },
  { _id: 'Camera Straps', totalCount: 64 },
  { _id: 'Carry-On Bags', totalCount: 57 },
  { _id: 'Disinfectant Wipes', totalCount: 85 },
  { _id: 'Insignia Smart TVs', totalCount: 81 },
  { _id: 'Toner Refill Kits', totalCount: 38 },
  { _id: 'iPads', totalCount: 51 },
  { _id: 'Memory Foam Mattresses', totalCount: 58 },
  { _id: 'Storage Baskets', totalCount: 68 },
  { _id: 'Body Spray', totalCount: 96 }
]
```

---

### Example 3: Count Promotion Events
The following pipeline counts the number of `promotionEvents`.

```javascript
db.stores.aggregate([
  {
    $unwind: "$promotionEvents"
  },
  {
    $count: "totalPromotionEvents"
  }
])
```

This query would return the following document.

```json
[ 
{ totalPromotionEvents: 145673 } 
]
```

### Example 4: Using `$count` in `$setWindowFields`

Count of sales for the category "Laptops" by company in the year 2023

```javascript
db.stores.aggregate([
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.discounts" },

  // Filter only for Laptop discounts in 2023
  {
    $match: {
      "promotionEvents.promotionalDates.startDate.Year": 2023,
      "promotionEvents.discounts.categoryName": "Laptops"
    }
  },

  // Add sales count by city using window function
  {
    $setWindowFields: {
      partitionBy: "$company",
      output: {
        salesCount: {
          $count: {},
          window: { documents: ["unbounded", "unbounded"] }
        }
      }
    }
  },

  // Group to return a single result per city
  {
    $group: {
      _id: "$company",
      salesCount: { $first: "$salesCount" }
    }
  }
])

```

This query would return the following document.

```json
[
  { _id: 'Boulder Innovations', salesCount: 10 },
  { _id: 'VanArsdel, Ltd.', salesCount: 13 },
  { _id: 'Proseware, Inc.', salesCount: 12 },
  { _id: 'Fabrikam, Inc.', salesCount: 11 },
  { _id: 'Contoso, Ltd.', salesCount: 13 },
  { _id: 'Fourth Coffee', salesCount: 8 },
  { _id: 'Trey Research', salesCount: 14 },
  { _id: 'Adatum Corporation', salesCount: 12 },
  { _id: 'Relecloud', salesCount: 16 },
  { _id: 'Lakeshore Retail', salesCount: 13 },
  { _id: 'Northwind Traders', salesCount: 5 },
  { _id: 'First Up Consultants', salesCount: 4 },
  { _id: 'Wide World Importers', salesCount: 7 },
  { _id: 'Tailwind Traders', salesCount: 12 }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]