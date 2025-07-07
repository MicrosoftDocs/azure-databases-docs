---
title: $merge usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $merge stage in an aggregation pipeline writes the results of the aggregation to a specified collection.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 06/23/2025
---

# $merge
The `$merge` stage in an aggregation pipeline is used to write the results of the aggregation query into a specified collection. This stage is particularly useful for tasks like updating or inserting documents into a target collection based on the output of an aggregation operation. It helps streamline workflows by combining data transformation and data persistence in a single operation.

## Syntax
```javascript
{
  $merge: {
    into: <collection>,
    on: <field or fields>,
    whenMatched: <action>,
    whenNotMatched: <action>
  }
}
```

## Parameters  
| Parameter | Description |
| --- | --- |
| **`into`** | Specifies the target collection where the aggregation results will be written. |
| **`on`** | Specifies the field(s) to identify matching documents in the target collection. |
| **`whenMatched`** | Specifies the action to take when a matching document is found. Options include `merge`, `replace`, `keepExisting`, `fail`, or a custom pipeline. |
| **`whenNotMatched`** | Specifies the action to take when no matching document is found. Options include `insert` or `discard`. |

## Example(s)
### Example 1: Merge data into a collection
This example aggregates documents and writes the results to a collection named `salesSummary`, updating existing documents where the `_id` matches and inserting new documents otherwise.

```javascript
db.sales.aggregate([
  {
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      totalSales: { $sum: "$sales.salesByCategory.totalSales" }
    }
  },
  {
    $merge: {
      into: "salesSummary",
      on: "_id",
      whenMatched: "merge",
      whenNotMatched: "insert"
    }
  }
])
```

### Example 2: Replace documents in the target collection
This example replaces documents in the `promotionEventsSummary` collection based on the `_id` field.

```javascript
db.promotionEvents.aggregate([
  {
    $project: {
      _id: "$eventName",
      startDate: "$promotionalDates.startDate",
      endDate: "$promotionalDates.endDate",
      totalDiscounts: { $size: "$discounts" }
    }
  },
  {
    $merge: {
      into: "promotionEventsSummary",
      on: "_id",
      whenMatched: "replace",
      whenNotMatched: "insert"
    }
  }
])
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]