---
  title: $bitsAllSet
  titleSuffix: Overview of the $bitsAllSet operator in Azure Cosmos DB for MongoDB (vCore)
  description: The bitsAllSet command is used to match documents where all the specified bit positions are set.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/02/2024
---

# $bitsAllSet


The `$bitsAllSet` operator is used to match documents where all the specified bit positions are set (that is, are 1). This operator is useful for performing bitwise operations on fields that store integer values. It can be used in scenarios where you need to filter documents based on specific bits being set within an integer field.

## Syntax

```javascript
{
  <field>: { $bitsAllSet: <bitmask> }
}
```
## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field in the document on which the bitwise operation is to be performed.|
| **`<bitmask>`** | A bitmask indicating which bits must be set in the field's value.|

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


### Example 1: Find stores with specific bits set in `storeId`

```javascript
db.stores.find({
  "store.storeId": { $bitsAllSet: 0b00000011 }
})
```

This query would return documents where the `storeId` field has both the first and second bits set.

### Example 2: Find stores with specific bits set in `totalStaff.fullTime`

```javascript
db.stores.find({
  "store.staff.totalStaff.fullTime": { $bitsAllSet: 0b00001111 }
})
```

This query would return documents where the `fullTime` field in `totalStaff` has the first 4 bits set.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
