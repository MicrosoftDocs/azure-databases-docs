---
title: $count (aggregation pipeline stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $count stage in the aggregation pipeline is used to count the number of documents that pass through the pipeline.
author: gahl.levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/09/2024
---

# `$count` (as aggregation pipeline stage)

The `$count` stage in the aggregation pipeline is used to count the number of documents that pass through the pipeline. This stage outputs a document with a single field containing the count of the documents. It is particularly useful when you need to determine the number of documents that match certain criteria or have passed through various stages of transformation in the pipeline.

## Syntax

```javascript
{
  $count: <field>
}
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`** | The name of the field in the output document where the count will be stored. |

## Related content

- [Migration path](migrations-options.md)
- [Compatibility](compatibility.md)
