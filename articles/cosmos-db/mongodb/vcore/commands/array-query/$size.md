---
title: $size (array query operator)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $size operator is used to query documents where an array field has a specified number of elements.
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/09/2024
---

# `$size` (array query operator)

The `$size` operator in MongoDB is used to query documents where an array field has a specified number of elements. This operator is useful when you need to find documents based on the size of an array field, such as finding documents with some items in a list.

## Syntax

```javascript
db.collection.find({ <field>: { $size: <number> } })
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`** | The field that contains the array. |
| **`<number>`** | The number of elements the array should have. |

## Related content

- [Migration path](migrations-options.md)
- [Compatibility](compatibility.md)
