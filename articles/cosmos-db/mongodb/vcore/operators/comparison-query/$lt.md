---
title: $lt
titleSuffix: Overview of the $lt operator
description: The $lt operator retrieves documents where the value of field is less than a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $lt

The `$lt` operator retrieves documents where the value of a field is strictly less than a specified value. The `$lt` operator filters documents based on numeric, date, or string values.

## Syntax

```javascript
{
    field: {
        $lt: value
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document you want to evaluate|
| **`value`** | The value to compare against the field's value. The operator will match documents where the field's value is less than this specified value|

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

### Example 1: Find a store with sales below $36,000

To find a store with less than $36,000 in sales, first run a query using $lt on the sales.totalSales field. Then project only the name and total sales of the resulting stores and limit the number of results to a single document.

```javascript
db.stores.find({
    "sales.totalSales": {
        "$lt": 36000
    }
}, {
    "name": 1,
    "sales.totalSales": 1
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
        "sales": { "totalSales": 17676 }
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
