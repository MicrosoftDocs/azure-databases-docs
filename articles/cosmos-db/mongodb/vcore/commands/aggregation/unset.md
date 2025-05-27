---
title: $unset (as Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $unset stage in the aggregation pipeline is used to remove specified fields from documents.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $unset (as Aggregation Pipeline Stage)
The $unset stage the aggregation pipeline is used to remove specified fields from documents. This can be particularly useful when you need to exclude certain fields from the results of an aggregation query for reasons such as privacy, reducing payload size, or simply cleaning up the output.

## Syntax
The syntax for the $unset stage is straightforward. It accepts a single argument which can be a field name or an array of field names to be removed from the documents.

```json
{
  $unset: "<field1>" | ["<field1>", "<field2>", ...]
}
```

## Parameters

| | Description |
| --- | --- |
| **`field1, field2, ...`** | The names of the fields to remove from the documents. |

## Example(s)
Here are a few examples demonstrating how to use the $unset stage in an aggregation pipeline.

### Example 1: Remove a Single Field
Suppose you want to remove the location field from the documents.

```json
db.stores.aggregate([
  {
    $unset: "store.location"
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
      "sales": {
        "totalSales": 15000,
        "salesByCategory": [
          {
            "category": "Electronics",
            "totalSales": 5000
          },
          {
            "category": "Clothing",
            "totalSales": 10000
          }
        ]
      }
    }
  }
]
```

### Example 2: Remove Multiple Fields
Suppose you want to remove the location and sales.totalSales fields from the documents.

```json
db.stores.aggregate([
  {
    $unset: ["store.location", "store.sales.totalSales"]
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
      "sales": {
        "salesByCategory": [
          {
            "category": "Electronics",
            "totalSales": 5000
          },
          {
            "category": "Clothing",
            "totalSales": 10000
          }
        ]
      }
    }
  }
]
```

### Example 3: Remove Nested Fields
Suppose you want to remove the staff.totalStaff.fullTime and promotionEvents.discounts fields from the documents.

```json
db.stores.aggregate([
  {
    $unset: ["store.staff.totalStaff.fullTime", "store.promotionEvents.discounts"]
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
          "partTime": 8
        }
      },
      "promotionEvents": ["Summer Sale", "Black Friday", "Holiday Deals"]
    }
  }
]
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).