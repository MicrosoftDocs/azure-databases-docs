---
title: $nin
titleSuffix: Overview of the $nin operator
description: The $nin operator retrieves documents where the value of a field doesn't match a list of values
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $nin

The `$nin` operator retrieves documents where the value of a specified field doesn't match a list of values.

## Syntax

```javascript
{
    field: {
        $nin: [ < listOfValues > ]
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to compare|
| **`[<listOfValues>]`** | An array of values that shouldn't match the value of the field being compared|

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

### Example 1 - Find a store with a discount that isn't 10%, 15%, or 20%

To find a store with promotions offering discounts that are not 10%, 15%, or 20%, first run a query using $nin on the nested discountPercentage field. Then project only the name and discount offered by the result store and limit the result to a single document from the result set.

```javascript
db.stores.find({
    "promotionEvents.discounts.discountPercentage": {
        "$nin": [10, 15, 20]
    }
}, {
    "name": 1,
    "promotionEvents.discounts.discountPercentage": 1
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
        "promotionEvents": [
          {
            "discounts": [
              { "discountPercentage": 18 },
              { "discountPercentage": 17 },
              { "discountPercentage": 9 },
              { "discountPercentage": 5 },
              { "discountPercentage": 5 },
              { "discountPercentage": 6 },
              { "discountPercentage": 9 },
              { "discountPercentage": 5 },
              { "discountPercentage": 19 },
              { "discountPercentage": 21 }
            ]
          }
        ]
    }
]
```

### Example 2 - Find a store with no discounts on a specific categories of promotions

To find a store without promotions on Smoked Salmon and Anklets, first run a query using $nin on the nested categoryName field. Then project the name and promotions offered by the store and limit the results to one document from the result set.

```javascript
db.stores.find({
    "promotionEvents.discounts.categoryName": {
        "$nin": ["Smoked Salmon", "Anklets"]
    }
}, {
    "name": 1,
    "promotionEvents.discounts.categoryName": 1
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
            "discounts": [
              { "categoryName": "Bath Accessories" },
              { "categoryName": "Pillow Top Mattresses" },
              { "categoryName": "Bathroom Scales" },
              { "categoryName": "Towels" },
              { "categoryName": "Bathrobes" },
              { "categoryName": "Mattress Toppers" },
              { "categoryName": "Hand Towels" },
              { "categoryName": "Shower Heads" },
              { "categoryName": "Bedspreads" },
              { "categoryName": "Bath Mats" }
            ]
          }
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
