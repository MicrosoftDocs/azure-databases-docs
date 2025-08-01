---
  title: $bitsAnySet
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Overview of the $bitsAnySet operator in Azure Cosmos DB for MongoDB (vCore)
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $bitsAnySet

This operator is used to select documents where any of the bit positions specified are set to `1`. It's useful for querying documents with fields that store bitmask values. This operator can be handy when working with fields that represent multiple boolean flags in a single integer.

## Syntax

```javascript
{
  <field>: { $bitsAnySet: [ <bit positions> ] }
}
```
## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to be queried.|
| **`<bit positions>`** | An array of bit positions to check if any are set to `1`.|

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

### Example 1: Querying for Documents with Specific Bit Positions Set

To find all stores where any of the bit positions 1 or 3 in the `storeId` field are set to `1`.

```javascript
db.stores.find({
  "store.storeId": { $bitsAnySet: [1, 3] }
})
```

### Example 2: Querying for Documents with Bit Positions in Nested Fields

To find all promotion events where any of the bit positions 0 or 2 in the `discountPercentage` for the "Laptops" category are set to `1`.

```javascript
db.stores.find({
  "store.promotionEvents.discounts": {
    $elemMatch: {
      "categoryName": "Laptops",
      "discountPercentage": { $bitsAnySet: [0, 2] }
    }
  }
})
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
