---
  title: $mergeObjects
  titleSuffix: Overview of the $mergeObjects expression in Azure Cosmos DB for MongoDB vCore
  description: The $mergeObjects operator merges multiple documents into a single document
  author: abinav2307
  ms.author: abramees
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: conceptual
  ms.date: 05/12/2025
---

# $mergeObjects as object expression operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$mergeObjects` operator combines multiple documents into a single document. The mergeObjects operation is used in aggregation pipelines to merge fields from different documents or add one or more fields to an existing document. The operator overwrites fields in the target document with fields from the source document when conflicts occur.

## Syntax

```mongodb
{ "$mergeObjects": [ <document1>, <document2>, ... ] }
```

## Parameters
| Parameter | Description |
| --- | --- |
| **`document1, document2`** | The documents to be merged. The documents can be specified as field paths, subdocuments, or constants. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
