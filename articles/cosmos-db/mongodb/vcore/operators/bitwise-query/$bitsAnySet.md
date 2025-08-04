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
```
### Example 1: Querying for Documents with Specific Bit Positions Set

This uses the bitwise operator $bitsAnySet, which matches documents where any of the bit positions specified in the array are set to **1** in the `staff.totalStaff.fullTime` field.The positions 1,correspond to the second bit (bit 1) and the fourth bit (bit 3), counting bits from right to left starting at 0.The query matches documents where either bit 1 or bit 3 (or both) are set to 1 in the fullTime field.

```javascript
db.stores.find({
  "staff.totalStaff.fullTime": { $bitsAnySet: [1, 3] }},
  { _id: 1, name: 1, staff: 1 }
).limit(2)
```
Sample output:

```JSON
[
  {
    _id: 'gaming-store-mall-001',
    name: 'Gaming Paradise - Mall Location',
    staff: {
      totalStaff: { fullTime: 8, partTime: 12 },
      manager: 'Alex Johnson',
      departments: [ 'gaming', 'accessories', 'repairs' ]
    }
  },
  {
    _id: '26afb024-53c7-4e94-988c-5eede72277d5',
    name: 'First Up Consultants | Microphone Bazaar - South Lexusland',
    staff: {
      minStaffRequired: 15,
      employeeCount: { fullTime: 10, partTime: 8 },
      totalStaff: { fullTime: 14, partTime: 8 }
    }
  }
]
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
Sample output:

```JSON
[
  {
    _id: 'e2a23707-b166-4df4-ad76-ea3e300d27ad',
    name: 'Contoso, Ltd. | Electronics Corner - Lake Maryse',
    staff: { employeeCount: { fullTime: 8, partTime: 1 } }
  },
  {
    _id: '7bc85b2e-d6c2-4341-a841-9020dffad454',
    name: 'Contoso, Ltd. | Electronics Pantry - North Monserrate',
    staff: { employeeCount: { fullTime: 18, partTime: 10 } }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
