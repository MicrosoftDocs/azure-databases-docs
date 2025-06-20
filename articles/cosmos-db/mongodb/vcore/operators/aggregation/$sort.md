---
title: $sort (aggregation pipeline stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $sort stage in the aggregation pipeline is used to order the documents in the pipeline by a specified field or fields.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/27/2024
---

# $sort (as aggregation pipeline stage)
The $sort stage in the aggregation pipeline is used to order the documents in the pipeline by a specified field or fields. This stage helps you sort data, like arranging sales by amount or events by date.

## Syntax
The syntax for the $sort stage is as follows:

```json
{
  $sort: { <field1>: <sort order>, <field2>: <sort order>, ... }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field to sort by |
| **`sort order`** | The order in which we should sort the field. 1 for ascending order and -1 for descending order. |

## Examples
### Example 1: Sorting by Total Sales in Descending Order
To sort the sales categories by their total sales in descending order:

```json
db.collection.aggregate([
  {
    $unwind: "$store.sales.salesByCategory"
  },
  {
    $sort: { "store.sales.salesByCategory.totalSales": -1 }
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
            "totalSales": 15000
          },
          {
            "category": "Clothing",
            "totalSales": 12000
          },
          {
            "category": "Home Goods",
            "totalSales": 10000
          }
        ]
      }
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
    "store": {
      "name": "Uptown Store",
      "sales": {
        "salesByCategory": [
          {
            "category": "Electronics",
            "totalSales": 20000
          },
          {
            "category": "Clothing",
            "totalSales": 18000
          },
          {
            "category": "Home Goods",
            "totalSales": 15000
          }
        ]
      }
    }
  }
]
```

### Example 2: Sorting by Event Start Date in Ascending Order
To sort the promotion events by their start dates in ascending order:

```json
db.collection.aggregate([
  {
    $unwind: "$store.promotionEvents"
  },
  {
    $sort: { "store.promotionEvents.promotionalDates.startDate": 1 }
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
      "promotionEvents": [
        {
          "eventName": "Summer Sale",
          "promotionalDates": {
            "startDate": ISODate("2024-06-01T00:00:00Z"),
            "endDate": ISODate("2024-06-30T23:59:59Z")
          }
        },
        {
          "eventName": "Black Friday",
          "promotionalDates": {
            "startDate": ISODate("2024-11-25T00:00:00Z"),
            "endDate": ISODate("2024-11-25T23:59:59Z")
          }
        },
        {
          "eventName": "Holiday Deals",
          "promotionalDates": {
            "startDate": ISODate("2024-12-01T00:00:00Z"),
            "endDate": ISODate("2024-12-31T23:59:59Z")
          }
        }
      ]
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
    "store": {
      "name": "Uptown Store",
      "promotionEvents": [
        {
          "eventName": "Back to School",
          "promotionalDates": {
            "startDate": ISODate("2024-08-01T00:00:00Z"),
            "endDate": ISODate("2024-08-31T23:59:59Z")
          }
        },
        {
          "eventName": "Winter Sale",
          "promotionalDates": {
            "startDate": ISODate("2024-12-01T00:00:00Z"),
            "endDate": ISODate("2024-12-31T23:59:59Z")
          }
        }
      ]
    }
  }
]
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).