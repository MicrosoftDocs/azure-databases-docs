---
  title: $bitsAnyClear
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Overview of the $bitsAnyClear operator in Azure Cosmos DB for MongoDB (vCore)
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $bitsAnyClear

This operator is used to match documents where any of the bit positions specified in a bitmask are clear (that is, 0). It's useful for querying documents with binary data or flags stored as integers. This operator enables efficient querying based on specific bit patterns.

## Syntax

```javascript
{
  <field>: { $bitsAnyClear: <bitmask> }
}
```
## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document to be queried.|
| **`<bitmask>`** |A bitmask where each bit position represents a position to check if it's clear (0).|

## Example

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

```javascript
db.stores.find({
  "store.staff.totalStaff.fullTime": { $bitsAnyClear: 0b00000111 }
})
```

In this example, `0b00000111` is the bitmask representing the first 3 bits. The query would return documents where any of the first 3 bits of the `totalStaff.fullTime` field are clear.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
