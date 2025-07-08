---
title: $addFields (aggregation)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $addFields stage in the aggregation pipeline is used to add new fields to documents.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/27/2024
---

# $addFields (aggregation)
The $addFields stage in the aggregation pipeline is used to add new fields to documents. It can also be used to reset the values of existing fields. This stage is particularly useful when you need to create new fields based on existing data or modify existing fields within your documents.

## Syntax
The basic syntax for the $addFields stage is as follows:

```json
{
  $addFields: {
    <newField1>: <expression1>,
    <newField2>: <expression2>,
    ...
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`newField1`** | The name of the new field to add or the existing field to modify. |
| **`expression1`** | The expression to compute the value of newField1. |

## Example(s)
### Example 1: Adding a New Field
Suppose we have a collection named stores with documents similar to the provided JSON structure. To add a new field totalDiscountEvents that counts the number of promotion events, we can use the following aggregation pipeline:

```json
db.stores.aggregate([
  {
    $addFields: {
      totalDiscountEvents: { $size: "$store.promotionEvents" }
    }
  }
])
```
Sample output
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": ["Summer Sale", "Black Friday", "Holiday Deals"]
    },
    "totalDiscountEvents": 3
  }
]
```

### Example 2: Modifying an Existing Field
If we want to add a field totalStaffCount that sums up the full-time and part-time staff, we can use:

```json
db.stores.aggregate([
  {
    $addFields: {
      totalStaffCount: {
        $add: ["$store.staff.totalStaff.fullTime", "$store.staff.totalStaff.partTime"]
      }
    }
  }
])
```
Sample output
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "staff": {
        "totalStaff": {
          "fullTime": 12,
          "partTime": 8
        }
      }
    },
    "totalStaffCount": 20
  }
]
```


### Example 3: Adding Nested Fields
To add a nested field location.coordinates that combines latitude and longitude into an array, use:

```json
db.stores.aggregate([
  {
    $addFields: {
      "store.location.coordinates": ["$store.location.lat", "$store.location.lon"]
    }
  }
])
```
Sample output
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "location": {
        "lat": 47.6097,
        "lon": -122.3331,
        "coordinates": [47.6097, -122.3331]
      }
    }
  }
]
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).