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



Find stores that **have parking AND restrooms** (bits 1 and 6)

```javascript
db.stores.find({
  storeFeatures: { $bitsAllSet: [1, 6] }},
  { _id: 1, name: 1, storeFeatures: 1 }).limit(5)
```

Equivalent:
```javascript
db.stores.find({
  storeFeatures: { $bitsAllSet: 66 }},
  { _id: 1, name: 1, storeFeatures: 1 }).limit(5)
```

Sample output:

```json
[
  {
    _id: '7e53ca0f-6e24-4177-966c-fe62a11e9af5',
    name: 'Contoso, Ltd. | Office Supply Deals - South Shana',
    storeFeatures: 86
  },
  {
    _id: '44fdb9b9-df83-4492-8f71-b6ef648aa312',
    name: 'Fourth Coffee | Storage Solution Gallery - Port Camilla',
    storeFeatures: 222
  },
  {
    _id: '728c068a-638c-40af-9172-8ccfa7dddb49',
    name: 'Contoso, Ltd. | Book Store - Lake Myron',
    storeFeatures: 239
  },
  {
    _id: 'a2b54e5c-36cd-4a73-b547-84e21d91164e',
    name: 'Contoso, Ltd. | Baby Products Corner - Port Jerrold',
    storeFeatures: 126
  },
  {
    _id: 'dda2a7d2-6984-40cc-bbea-4cbfbc06d8a3',
    name: 'Contoso, Ltd. | Home Improvement Closet - Jaskolskiview',
    storeFeatures: 107
  }
]

```


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
