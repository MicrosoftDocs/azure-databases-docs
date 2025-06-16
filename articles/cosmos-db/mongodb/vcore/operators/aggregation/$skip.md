---
title: $skip (Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $skip stage in the aggregation pipeline is used to skip a specified number of documents from the input and pass the remaining documents to the next stage in the pipeline.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $skip (Aggregation Pipeline Stage)
The $skip stage in the aggregation pipeline is used to skip a specified number of documents from the input and pass the remaining documents to the next stage in the pipeline. The stage is useful for implementing pagination in queries and for controlling the subset of documents that subsequent stages in the pipeline operate on.

## Syntax
The syntax for the $skip stage is straightforward. It accepts a single parameter, which is the number of documents to skip.

```json
{
  $skip: <number>
}
```

### Parameters

| | Description |
| --- | --- |
| **`number`** | The number of documents to skip before passing the remaining documents to the next stage. |

## Examples
### Example 1: Skipping Documents in a Collection
Suppose we have a collection named stores with documents representing various store details. To skip the first 2 documents and return the rest, you can use the following aggregation pipeline:

```json
db.stores.aggregate([
  { $skip: 2 }
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
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c6",
    "store": {
      "name": "Uptown Store",
      "promotionEvents": ["Back to School", "Winter Sale"]
    }
  }
]
```

### Example 2: Skipping Documents and Then Limiting the Result
To skip the first 2 documents and then limit the result to the next 3 documents, you can combine $skip with $limit:

```json
db.stores.aggregate([
  { $skip: 2 },
  { $limit: 3 }
])
```

### Example 3: Skipping Documents in a More Complex Pipeline
Consider a scenario where you want to skip the first promotion event and then project the remaining events for a specific store:

```json 
db.stores.aggregate([
  { $match: { "store.storeId": "12345" } },
  { $unwind: "$store.promotionEvents" },
  { $skip: 1 },
  { $project: { "store.promotionEvents": 1, _id: 0 } }
])
``` 

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).