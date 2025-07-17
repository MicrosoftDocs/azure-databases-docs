---
title: $count (aggregation)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $count stage in the aggregation pipeline is used to count the number of documents that pass through the pipeline.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/11/2024
---

# `$count` (aggregation)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$count` stage in the aggregation pipeline is used to count the number of documents that pass through the pipeline. This stage outputs a document with a single field containing the count of the documents. It's useful when you need to determine the number of documents that match certain criteria or passed through various stages of transformation in the pipeline.

## Syntax

```javascript
{
  $count: <field>
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The name of the field in the output document where the count is stored. |

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
