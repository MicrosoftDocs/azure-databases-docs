---
title: $slice (projection)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $slice operator is used to return a subset of an array limited by a specified number or range of items.
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/09/2024
---

# `$slice` (projection)

The `$slice` operator is used to return a subset of an array. It can be used to limit the number of elements in an array to a specified number or to return elements from a specified position in the array. This is particularly useful when dealing with large arrays where only a portion of the data is needed for processing or display.

The `$slice` operator in MongoDB is used within a projection to return a subset of an array field. It allows you to limit the number of elements returned from an array, either by specifying the number of elements to include or by specifying a range.

## Syntax

```javascript
db.collection.find({},
  {
    <field>: { $slice: <count> }
  }
)
```

```javascript
db.collection.find({},
  {
    <field>: { $slice: [ <skip>, <limit> ] }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`** | The array field from which you want to slice a subset. |
| **`<count>`** | The number of elements to return from the beginning of the array. |

| | Description |
| --- | --- |
| **`<skip>`** | The number of elements to skip. |
| **`<limit>`** | The number of elements to return after skipping. |

## Related content

- [Migration path](migrations-options.md)
- [Compatibility](compatibility.md)
