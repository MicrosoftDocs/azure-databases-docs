---
title: aggregation - $sort (Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $sort stage in the aggregation pipeline is used to order the documents in the pipeline by a specified field or fields.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $sort (as Aggregation Pipeline stage)
The $sort stage in the aggregation pipeline is used to order the documents in the pipeline by a specified field or fields. This is particularly useful when you need to present data in a specific order, such as sorting sales data by total sales or ordering events by their start dates.

## Syntax
The syntax for the $sort stage is as follows:

```json
{
  $sort: { <field1>: <sort order>, <field2>: <sort order>, ... }
}
```

field: The field by which to sort the documents.
sort order: The order in which to sort the field. 1 for ascending order and -1 for descending order.

## Example(s)
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

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).