---
title: $collStats
titleSuffix: Overview of the $collStats operator in Azure Cosmos DB for MongoDB (vCore)
description: The $collStats stage in the aggregation pipeline is used to return statistics about a collection.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/27/2024
---

# $collStats

The $collStats stage in the aggregation pipeline is used to return statistics about a collection. This stage can be particularly useful for understanding the performance characteristics of a collection, such as the number of documents, the size of the collection, and storage statistics. It provides detailed information that can help with database optimization and monitoring.

## Syntax

```javascript
{
  $collStats: {
    latencyStats: { histograms: <boolean> },
    storageStats: { scale: <number> },
    count: {}
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`latencyStats`** | Optional. Specifies whether to include latency statistics. The `histograms` field is a boolean that indicates whether to include histograms of latency data. |
| **`storageStats`** | Optional. Specifies whether to include storage statistics. The `scale` field is a number that indicates the scale factor for the storage statistics. |
| **`count`** | Optional. Includes the count of documents in the collection. |


### Example: Basic Collection Statistics

To count documents in the store collection:
```javascript
db.store.aggregate([
  {
    $collStats: {
      count: {}
    }
  }
])
```
Sample output
```json
[
  {
    "count": 1523
  }
]
```

This example returns the count of documents in the store collection.


## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).