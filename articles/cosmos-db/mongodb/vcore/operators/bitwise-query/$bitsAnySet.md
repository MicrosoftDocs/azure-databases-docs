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
  _id: 'a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6',
  name: 'Lakeshore Retail | Holiday Supply Hub - Marvinfort',
  location: {
    lat: -74.0427,
    lon: 160.8154
  },
  staff: {
    employeeCount: {
      fullTime: 9,
      partTime: 18
    }
  }, 
  company: 'Lakeshore Retail',
  city: 'Marvinfort',
  storeOpeningDate: 2024-10-01T18:24:02.586Z,
  lastUpdated: Timestamp({ t: 1730485442, i: 1 }),
  storeFeatures: 38
}
```

The `storeFeatures` field is a bitmask integer representing various store capabilities. Each bit corresponds to a feature:

| Bit | Value | Feature                 |
|-----|-------|--------------------------|
| 0   | 1     | In-Store Pickup          |
| 1   | 2     | Parking                  |
| 2   | 4     | Wheelchair Access        |
| 3   | 8     | Open 24 Hours            |
| 4   | 16    | Pet-Friendly             |
| 5   | 32    | Free Wi-Fi               |
| 6   | 64    | Restrooms                |
| 7   | 128   | Home Delivery            |

Find stores that offer either home delivery OR free Wi-Fi (bits 5 and 7)


```javascript
db.stores.find({
  storeFeatures: { $bitsAnySet: [5, 7] }},
  { _id: 1, name: 1, storeFeatures: 1 }).limit(5)
```

Equivalent:

```javascript
db.stores.find({
  storeFeatures: { $bitsAnySet: 160  }},  // 32 + 128
  { _id: 1, name: 1, storeFeatures: 1 }).limit(5)
```

Sample output:

```JSON
[
  {
    _id: 'a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6',
    name: 'Lakeshore Retail | Holiday Supply Hub - Marvinfort',
    storeFeatures: 38
  },
  {
    _id: '44fdb9b9-df83-4492-8f71-b6ef648aa312',
    name: 'Fourth Coffee | Storage Solution Gallery - Port Camilla',
    storeFeatures: 222
  },
  {
    _id: '94792a4c-4b03-466b-91f6-821c4a8b2aa4',
    name: 'Fourth Coffee | Eyewear Shop - Lessiemouth',
    storeFeatures: 225
  },
  {
    _id: '728c068a-638c-40af-9172-8ccfa7dddb49',
    name: 'Contoso, Ltd. | Book Store - Lake Myron',
    storeFeatures: 239
  },
  {
    _id: 'e6410bb3-843d-4fa6-8c70-7472925f6d0a',
    name: 'Relecloud | Toy Collection - North Jaylan',
    storeFeatures: 108
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
