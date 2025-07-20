---
title: $ne
titleSuffix: Overview of the $ne operator
description: The $ne operator retrieves documents where the value of a field doesn't equal a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $ne

The `$ne` operator retrieves documents where the value of a field doesn't equal a specified value.

## Syntax

```javascript
{
    field: {
        $ne: value
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to be compared|
| **`value`** | The value that the field shouldn't be equal to|

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

### Example 1 - Find a store whose name isn't "Fourth Coffee"

To find a store with a name that isn't "Fourth Coffee", first run a query using $ne on the name field. Then project only the name of the resulting documents and limit the results to one store from the result set.

```javascript
db.stores.find({
    "name": {
        "$ne": "Fourth Coffee"
    }
}, {
    "_id": 1,
    "name": 1
}, {
    "limit": 1
})
```

This query returns the following result:

```json
[
    {
        "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
        "name": "First Up Consultants | Bed and Bath Center - South Amir"
    }
]
```

### Example 2 - Find a store with promotion events that aren't in 2024

To find a store with promotions events that don't start in 2024, first run a query using $ne on the nested startDate field. Then project the name and promotions offered by the stores and limit the results to one document from the result set.

```javascript
db.stores.find({
    "promotionEvents.promotionalDates.startDate": {
        "$ne": "2024"
    }
}, {
    "name": 1,
    "promotionEvents.promotionalDates.startDate": 1
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
        "promotionEvents": [
          {
            "promotionalDates": { "startDate": { "Year": 2024, "Month": 9, "Day": 21 } }
          }
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
