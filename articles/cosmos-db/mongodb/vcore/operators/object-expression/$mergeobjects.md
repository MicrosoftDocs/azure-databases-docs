---
  title: $mergeObjects object expression usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $mergeObjects operator is used to combine multiple documents into a single document.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $mergeObjects as object expression operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$mergeObjects` operator is used to combine multiple documents into a single document. This operator is useful in aggregation pipelines when you need to merge fields from different documents or add another field to an existing document. The behavior of `$mergeObjects` is to overwrite fields in the target document with fields from the source document when there are conflicts.

## Syntax

```javascript
{ $mergeObjects: [ <document1>, <document2>, ... ] }
```

## Parameters

| | Description |
| --- | --- |
| **`document1, document2`** | These documents are targeted for merge. The documents can be specified as field paths, subdocuments, or constants. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
