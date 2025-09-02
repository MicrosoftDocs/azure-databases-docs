---
title: $pull
titleSuffix: Overview of the $pull operation in Azure Cosmos DB for MongoDB (vCore)
description: Removes all instances of a value from an array.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 10/15/2024
---

# $pull (array update)

The `$pull` operator is used to remove all instances of a specified value or values that match a condition from an array. This is useful when you need to clean up or modify array data within your documents.

## Syntax

```mongodb
{ $pull: { <field>: <value|condition> } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<field>`** | The field from which to remove one or more values. |
| **`<value|condition>`** | The value or condition to remove from the array. |

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
  ]
}

```

### Example 1: Remove a specific tag from the `tag` array

To remove the value "#SeasonalSale" from the tag array field.

```javascript
db.stores.update(
  { _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $pull: { tag: "#SeasonalSale" } }
)
```

This query would return the following document.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "1",
  "upsertedCount": 0
}
```

### Example 2: Remove all events from the `promotionEvents` array that end before a certain date

To remove all elements from the promotionEvents array where the endDate year is 2024 and the endDate month is earlier than March.

```javascript
db.stores.update(
  { _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $pull: { promotionEvents: { "promotionalDates.endDate.Year": 2024, "promotionalDates.endDate.Month": { $lt: 3 } } } }
)
```

This query would return the following document.

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
