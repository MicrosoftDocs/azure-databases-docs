---
title: $push (array update operator)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $push operator is used to add new elements to an existing array field within a document without affecting the other elements in the array.
author: sandeepsnairms
ms.author: sandnair
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/09/2024
---

# `$push` (array update operator)

The `$push` operator is used to append a specified value to an array within a document. This operator is useful when you need to add new elements to an existing array field without affecting the other elements in the array. It can be used in various scenarios such as adding new sales categories, promotional events, or staff members to a store's document.

## Syntax

```javascript
db.collection.update(
   { <query> },
   { $push: { <field>: <value> } },
   { <options> }
)
```

## Parameters

| | Description |
| --- | --- |
| **`<query>`** | The selection criteria for the documents to update. |
| **`<field>`** | The array field to which the value is appended. |
| **`<value>`** | The value to append to the array field. |
| **`<options>`** | *(Optional)*. Extra options for the update operation. |

## Related content

- [Migration path](migrations-options.md)
- [Compatibility](compatibility.md)
