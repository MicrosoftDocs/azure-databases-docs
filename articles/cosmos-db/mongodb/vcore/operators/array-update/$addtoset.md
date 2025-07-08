--- 
title: $addToSet
titleSuffix: Overview of the addToSet operation in Azure Cosmos DB for MongoDB vCore
description: The addToSet operator adds elements to an array if they don't already exist, while ensuring uniqueness of elements within the set.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 05/04/2025
---

# $addToSet (array update)

The `$addToSet` operator adds elements to an array if they don't already exist, while ensuring uniqueness of elements within the set.

## Syntax

```mongodb
{
  "$addToSet": { <field1>: <value1>, ... }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<field1>`** | The field to which you want to add elements. |
| **`<value1>`** | The value to be added to the array. |

## Example

Consider this sample document from the stores collection in the StoreData database.

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
  ]
}

```

### Example 1: Adding a new tag to the `tag` array


```mongodb
db.stores.update(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { "$addToSet": { "tag": "#ShopLocal" } }
)
```


This query would return the following document as `#ShopLocal` already existed.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "0",
  "upsertedCount": 0
}

```

### Example 2: Adding a new promotional event to the `promotionEvents` array

Add a new promotional event to the `promotionEvents` array, only if it doesn't already exist.

```json
db.stores.update(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { "$addToSet": { "promotionEvents": {
      "eventName": "Summer Sale",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 1 },
        "endDate": { "Year": 2024, "Month": 6, "Day": 15 }
      },
      "discounts": [
        { "categoryName": "DJ Speakers", "discountPercentage": 20 }
      ]
    }
  }}
)
```

This query would return the following document as it was a unique entry.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "1",
  "upsertedCount": 0
}

```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
