---
title: $pop
titleSuffix: Overview of the $pop operation in Azure Cosmos DB for MongoDB (vCore)
description: Removes the first or last element of an array.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 10/15/2024
---

# $pop

The `$pop` operator is used to remove the first or last element of an array. This operator is useful when you need to manage arrays by removing elements from either end. The `$pop` operator can be used in update operations.

## Syntax

```javascript
{ $pop: { <field>: <value> } }
```

- `<field>`: The field that contains the array from which you want to remove an element.
- `<value>`: Use `1` to remove the last element, and `-1` to remove the first element.

## Parameters

| Parameter | Description |
| --- | --- |
| **`<field>`** | The field that contains the array from which you want to remove an element. |
| **`<value>`** | Use `1` to remove the last element, and `-1` to remove the first element. |

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

### Example 1: Removing the last tag from the `tag` array

```shell
db.stores.update(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $pop: { "tag": 1 } }
)
```

This query would return the following document. The last element from the array is removed.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "1",
  "upsertedCount": 0
}

```

### Example 2: Removing the last discount from the `promotionEvents` array

```shell
db.stores.update(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $pop: { "promotionEvents": -1 } }
)
```

This query would return the following document. The first element from the array is removed.

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