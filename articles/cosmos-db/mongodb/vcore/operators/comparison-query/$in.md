---
title: $in
titleSuffix: Overview of the $in operator in Azure Cosmos DB for MongoDB (vCore)
description: The $in operator matches value of a field against an array of specified values
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/04/2025
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

## Examples

Let's understand the usage with sample json from `stores` dataset.

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

### Example 1 - Use $in operator as comparison-query to find a store with specific categories of promotions

The query finds stores that offer discounts in either "Smoked Salmon" or "Anklets" categories via promotion events.

```javascript
db.stores.find(
  {
    "promotionEvents.discounts.categoryName": {
      "$in": ["Smoked Salmon", "Anklets"]
    }
  },
  {
    "name": 1,
    "promotionEvents.discounts.categoryName": 1
  }
).limit(1)
```

This returns the following result:

```json
{
  "_id": "48fcdab8-b961-480e-87a9-19ad880e9a0a",
  "name": "Lakeshore Retail | Jewelry Collection - South Nicholas",
  "promotionEvents": [
    {
      "discounts": [
        {"categoryName": "Anklets"},
        {"categoryName": "Cufflinks"}
      ]
    },
    {
      "discounts": [
        {"categoryName": "Anklets"},
        {"categoryName": "Brooches"}
      ]
    },
    {
      "discounts": [
        {"categoryName": "Rings"},
        {"categoryName": "Bracelets"}
      ]
    },
    {
      "discounts": [
        {"categoryName": "Charms"},
        {"categoryName": "Bracelets"}
      ]
    },
    {
      "discounts": [
        {"categoryName": "Watches"},
        {"categoryName": "Pendants"}
      ]
    }
  ]
}
```

### Example 2 - Use $in operator as array-expression in an array for a specified value or set of values

The query searches for the specified store and filters documents where at least one `discountPercentage` within any `promotionEvents.discounts` is either 15 or 20. It uses a dot notation path and the $in operator to match nested discount values across the array hierarchy.

```javascript
db.stores.find(
  {
    "_id": "48fcdab8-b961-480e-87a9-19ad880e9a0a",
    "promotionEvents.discounts.discountPercentage": { $in: [15, 20] }
  },
  {
    "_id": 1,
    "name": 1,
    "promotionEvents.discounts": 1
  }
)
```

The query returns document where the `discounts` array contains any element with a `discountPercentage` of either `15` or `20`, and only shows the `complete discounts array` for those documents.

```json
{
  "_id": "48fcdab8-b961-480e-87a9-19ad880e9a0a",
  "name": "Lakeshore Retail | Jewelry Collection - South Nicholas",
  "promotionEvents": [
    {
      "discounts": [
        { "categoryName": "Anklets", "discountPercentage": 12 },
        { "categoryName": "Cufflinks", "discountPercentage": 9 }
      ]
    },
    {
      "discounts": [
        { "categoryName": "Anklets", "discountPercentage": 23 },
        { "categoryName": "Brooches", "discountPercentage": 12 }
      ]
    },
    {
      "discounts": [
        { "categoryName": "Rings", "discountPercentage": 10 },
        { "categoryName": "Bracelets", "discountPercentage": 21 }
      ]
    },
    {
      "discounts": [
        { "categoryName": "Charms", "discountPercentage": 9 },
        { "categoryName": "Bracelets", "discountPercentage": 13 }
      ]
    },
    {
      "discounts": [
        { "categoryName": "Watches", "discountPercentage": 20 },
        { "categoryName": "Pendants", "discountPercentage": 7 }
      ]
    }
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
