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
This uses the bitwise operator $bitsAllSet, which matches documents where all bit positions specified in the bitmask are set to 1 in the `staff.totalStaff.fullTime` field. The bitmask 0b00000011 corresponds to the two least significant bits (bit 0 and bit 1). The query matches documents where both bits 0 and 1 are set to 1 in the fullTime field.

```javascript
db.stores.find(
  { "staff.totalStaff.fullTime": { $bitsAllSet: 0b00000011 } },
  { _id: 1, name: 1, staff: 1 }
).limit(2)

```
Sample output:

```json
[
  {
    _id: '40d6f4d7-50cd-4929-9a07-0a7a133c2e74',
    name: 'Proseware, Inc. | Home Entertainment Hub - East Linwoodbury',
    staff: { totalStaff: { fullTime: 19, partTime: 20 } }
  },
  {
    _id: 'f2a8c190-28e4-4e14-9d8b-0256e53dca66',
    name: 'Fabrikam, Inc. | Car Accessory Outlet - West Adele',
    staff: {
      maxStaffCapacity: 25,
      employeeCount: { fullTime: 10, partTime: 2 },
      totalStaff: { fullTime: 3, partTime: 2 }
    }
  }
]

```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
