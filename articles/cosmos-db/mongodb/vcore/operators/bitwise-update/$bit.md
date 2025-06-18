--- 
title: $bit(bitwise update) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The `$bit` operator is used to perform bitwise operations on integer values.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 10/15/2024
---


# $bit(bitwise update)
The `$bit` operator is used to perform bitwise operations on integer values. It can be used to update integer fields in documents by applying bitwise AND, OR, and XOR operations. Bitwise operators like $bit aren't designed for incrementing values, but for manipulating bits directly (like checking, setting, or clearing specific bits).

## Syntax
```
{ $bit: { <field>: { <operator>: <number> } } }
```

## Parameters  
| | Description |
| --- | --- |
| **`<field>`** | The field to perform the bitwise operation on. |
| **`<operator>`** | The bitwise operation to perform. Can be one of: `and`, `or`, `xor`. |
| **`<number>`** | The number to use for the bitwise operation. |

## Examples

Let's understand the usage with the following sample json.

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

### Example 1: Perform a bitwise AND operation on the `partTime` field in `totalStaff`.

```shell
db.stores.updateOne(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $bit: { "staff.totalStaff.partTime": { and: 1 } } }
)
```

This query would return the following document. The AND of 0 and 1 is 0 hence the new value of the field is 0.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "1",
  "upsertedCount": 0
}
```


### Example 2:  Perform a bitwise OR operation on the `partTime` field in `totalStaff`.

```shell
db.stores.updateOne(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $bit: { "staff.totalStaff.partTime": { "or" : 1 } } }
)
```

This query would return the following document. The OR of 0 and 1 is 1 hence the new value of the field is 1.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "1",
  "upsertedCount": 0
}
```

### Example 3: Perform a bitwise XOR operation on the `partTime` field in `totalStaff`.
```shell
db.stores.updateOne(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $bit: { "staff.totalStaff.partTime": { "xor" : 1 } } }
)
```
This query would return the following document. The XOR of 1 and 1 is 0 hence the new value of the field is 0.

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