---
title: $sortByCount (Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $sortByCount stage in the aggregation pipeline is used to group documents by a specified expression and then sort the count of documents in each group in descending order.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $sortByCount (Aggregation Pipeline Stage)
The $sortByCount stage in the aggregation pipeline is used to group documents by a specified expression and then sort the count of documents in each group in descending order. This stage is particularly useful for quickly identifying the most common values within a dataset.

## Syntax
The syntax for the $sortByCount stage is:

```json
{
  $sortByCount: <expression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`expression`** | This is the field or computed expression on which to group and count the documents. |

## Example(s)
Consider a collection named stores with documents structured as described earlier. To find out the most common promotional events based on their names, you can use the $sortByCount stage as follows:

### Example 1: Count and Sort Promotional Events by Event Name
```json
db.stores.aggregate([
  { $unwind: "$store.promotionEvents" },
  { $sortByCount: "$store.promotionEvents.eventName" }
])
```
Sample output
```json
[
  { "_id": "Summer Sale", "count": 152 },
  { "_id": "Black Friday", "count": 120 },
  { "_id": "Holiday Deals", "count": 98 }
]
```

This pipeline will: 1. Use $unwind to deconstruct the promotionEvents array field from the input documents. 2. Use $sortByCount to group by the eventName field and count the number of occurrences of each event name, sorting the results in descending order of the count.

### Example 2: Count and Sort Sales by Category Name
```json
db.stores.aggregate([
  { $unwind: "$store.sales.salesByCategory" },
  { $sortByCount: "$store.sales.salesByCategory.categoryName" }
])
```
Sample output
```json
[
  { "_id": "Electronics", "count": 152 },
  { "_id": "Clothing", "count": 120 },
  { "_id": "Home Goods", "count": 98 }
]
```

This pipeline will: 1. Use $unwind to deconstruct the salesByCategory array field from the input documents. 2. Use $sortByCount to group by the categoryName field and count the number of occurrences of each category name, sorting the results in descending order of the count.

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).