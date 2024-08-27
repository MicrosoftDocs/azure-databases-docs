---
title: Operator - $elemMatch (projection)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: TODO
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# Operator: `$elemMatch` (projection)

The `$elemMatch` projection operator in Azure CosmosDB for MongoDB vCore is used to project the first element in an array that matches the specified query condition. This operator is particularly useful when you want to retrieve only the matching elements from an array within a document, rather than the entire array.

## Syntax

```json
db.collection.find({},
    {
      "field": { "$elemMatch": { <query> } }
    }
)
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field containing the array from which you want to project the matching element. |
| **`query`** | The condition that the elements in the array need to match. |
