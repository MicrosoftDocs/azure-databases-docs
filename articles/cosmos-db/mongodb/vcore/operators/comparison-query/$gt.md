---
title: $gt
titleSuffix: Overview of the $gt operator
description: The $gt query operator retrieves documents where the value of a field is greater than a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $gt

The `$gt` operator retrieves documents where the value of a field is greater than a specified value. The `$gt` operator queries numerical and date values to filter records that exceed a specified threshold.

## Syntax

```javascript
{
    field: {
        $gt: value
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to compare|
| **`value`** | The value that the field should be greater than|

## Examples

Consider this sample document from the stores collection.

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

### Example 1: Retrieve stores with sales exceeding $35,000

To retrieve a store with over $35,000 in sales, first run a query with $gt operator on the sales.totalSales field. Then limit the query results to one store.

```javascript
db.stores.find({
    "sales.totalSales": {
        "$gt": 35000
    }
}, {
    "name": 1,
    "sales.totalSales": 1
}, {
    "limit": 1
})
```

This returns the following result:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "sales": { "totalSales": 37701 }
    }
]
```

### Example 2: Find a store with more than 12 full-time staff

To find a store with more than 12 full time staff, first run a query with the $gt operator on the staff.totalStaff.fullTime field. Then project just the name and totalStaff fields and limit the result set to a single store from the list of matching results.

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        "$gt": 12
    }
}, {
    "name": 1,
    "staff.totalStaff": 1
}, {
    "limit": 1
})
```

This query returns the following result:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir",
        "staff": { "totalStaff": { "fullTime": 18, "partTime": 17 } }
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
