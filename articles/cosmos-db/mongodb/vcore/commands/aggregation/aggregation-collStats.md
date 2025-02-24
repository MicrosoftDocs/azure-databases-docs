---
title: $collStats (as Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $collStats stage in the aggregation pipeline is used to return statistics about a collection.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $collStats (as Aggregation Pipeline Stage)
This section will have an introduction to the command, its use cases, and behavior.

The $collStats stage in the aggregation pipeline is used to return statistics about a collection. This stage can be particularly useful for understanding the performance characteristics of a collection, such as the number of documents, the size of the collection, and storage statistics. It provides detailed information that can help with database optimization and monitoring.

## Syntax
This section will have the syntax of the command and its parameter definitions.

```json
{
  $collStats: {
    latencyStats: { histograms: <boolean> },
    storageStats: { scale: <number> },
    count: {}
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`latencyStats`** | Optional. Specifies whether to include latency statistics. The `histograms` field is a boolean that indicates whether to include histograms of latency data. |
| **`storageStats`** | Optional. Specifies whether to include storage statistics. The `scale` field is a number that indicates the scale factor for the storage statistics. |
| **`count`** | Optional. Includes the count of documents in the collection. |

## Example(s)
This section will have one or more examples that will help explain the command usage.

### Example 1: Basic Collection Statistics
```json
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