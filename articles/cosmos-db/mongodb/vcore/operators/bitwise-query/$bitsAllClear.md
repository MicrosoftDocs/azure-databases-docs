---
title: $bitsallclear
titleSuffix: Overview of the $bitsallclear operator in Azure Cosmos DB for MongoDB (vCore)
description: The $bitsallclear operator is used to match documents where all the bit positions specified in a bitmask are clear.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 11/01/2024
---

# $bitsAllClear

The `$bitsAllClear` operator is used to match documents where all the bit positions specified in a bitmask are clear (that is, 0). This operator is useful in scenarios where you need to filter documents based on specific bits being unset in a binary representation of a field.

## Syntax

```javascript
{
  <field>: {
    $bitsAllClear: <bitmask>
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document to be evaluated. |
| **`<bitmask>`** | A bitmask where each bit position specifies the corresponding bit position in the field's value that must be clear (0). |


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


### Example 1: xxx

```javascript
db.stores.find({
  "store.storeId": { $bitsAllClear: 0b00000011 }
})
```

This query would return documents where all the specified bit positions in the `storeId` field are clear.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
