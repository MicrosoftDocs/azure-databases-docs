---
title: $lte
titleSuffix: Overview of the $lte operator in Azure Cosmos DB for MongoDB (vCore)
description: The $lte operator retrieves documents where the value of a field is less than or equal to a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $lte

The `$lte` operator retrieves documents where the value of a field is less than or equal to a specified value. The `$lte` operator filters documents based on numerical, date, or other comparable fields.

## Syntax

```javascript
{
    field: {
        $lte: <value>
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to be compared|
| **`value`** | The value to compare against|

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

### Example 1: Find a store with sales <= $35,000

To find a store with sales <= $35,000, run a query using $lte on the sales.totalSales field and limit the resulting documents to a single store.

```javascript
db.stores.find({
    "sales.totalSales": {
        "$lte": 35000
    }
}, {
    "_id": 1
}, {
    "limit": 1
})
```

This query returns the following result:

```json
[
  {
    "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6"
  }
]
```

### Example 2: Find a store with 12 or fewer full-time staff

To find a store with <= 12 full-time staff, run a query using $lte on the nested fullTime field. Then project only the name and full time staff count and limit the results to one store from the result set.

```javascript
db.stores.find({
    "staff.totalStaff.fullTime": {
        "$lte": 12
    }
}, {
    "name": 1,
    "staff.totalStaff.fullTime": 1
}, {
    "limit": 1
})
```

This query returns the following result:

```json
[
  {
      "_id": "e6895a31-a5cd-4103-8889-3b95a864e5a6",
      "name": "VanArsdel, Ltd. | Picture Frame Store - Port Clevelandton",
      "staff": { "totalStaff": { "fullTime": 6 } }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
