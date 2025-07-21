---
title: $in
titleSuffix: Overview of the $in operator in Azure Cosmos DB for MongoDB (vCore)
description: The $in operator matches value of a field against an array of specified values
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $in

The `$in` operator matches values of a field against an array of possible values. The `$in` operator filters documents where the value of a field equals any of the specified values.

## Syntax

```javascript
{
    field: {
        $in: [ listOfValues ]
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to match|
| **`[listOfValues]`** | An array of values to match against the specified field|

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

### Example 1 - Find a store with promotion events offering a discount percentage of either 10%, 15% or 20%

To find a store with promotion events across any sales category with discounts of either 10%, 15%, or 20%, first run a query using $in on the nested discountPercentage field. Then project only the name and discount offered by the store and limit the result to a single document from the result set. 

```javascript
db.stores.find({
    "promotionEvents.discounts.discountPercentage": {
        "$in": [10, 15, 20]
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
        "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
        "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
        "promotionEvents": [
          {
            "discounts": [
              { "discountPercentage": 14 },
              { "discountPercentage": 6 },
              { "discountPercentage": 21 },
              { "discountPercentage": 21 },
              { "discountPercentage": 5 },
              { "discountPercentage": 22 }
            ]
          }
        ]
    }
]
```

### Example 2 - Find a store with specific categories of promotions

To find a store with discounts specifically for Smoked Salmon and Anklets, first run a query using $in on the nested categoryName array. Then project only the name and discount category offered by the store. Lastly, limit the results to a single document from the result set.

```javascript
db.stores.find({
    "promotionEvents.discounts.categoryName": {
        "$in": ["Smoked Salmon", "Anklets"]
    }
}, {
    "name": 1,
    "promotionEvents.discounts.categoryName": 1
}, {
    "limit": 1
})
```

This returns the following result:

```json
[
    {
        "_id": "3f140a3f-6809-4b40-85b1-75657f5605b8",
        "name": "Boulder Innovations | Jewelry Store - Littleborough",
        "promotionEvents": [
          {
            "discounts": [ { "categoryName": "Watches" }, { "categoryName": "Rings" } ]
          },
          {
            "discounts": [ { "categoryName": "Anklets" }, { "categoryName": "Earrings" } ]
          },
          {
            "discounts": [ { "categoryName": "Rings" }, { "categoryName": "Anklets" } ]
          },
          {
            "discounts": [ { "categoryName": "Earrings" }, { "categoryName": "Necklaces" } ]
          },
          {
            "discounts": [ { "categoryName": "Charms" }, { "categoryName": "Bracelets" } ]
          },
          {
            "discounts": [ { "categoryName": "Watches" }, { "categoryName": "Brooches" } ]
          }
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
