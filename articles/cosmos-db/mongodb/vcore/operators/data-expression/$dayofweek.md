---
title: $dayOfWeek
titleSuffix: Overview of the $dayOfWeek operator in Azure Cosmos DB for MongoDB vCore
description: The $dayOfWeek operator in Azure Cosmos DB for MongoDB vCore extracts the day of the week from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dayOfWeek

The `$dayOfWeek` operator extracts the day of the week from a date value, where 1 represents Sunday and 7 represents Saturday. It is useful for grouping or filtering documents based on the day of the week.

## Syntax

```javascript
{ $dayOfWeek: <dateExpression> }
```

## Parameters

| Parameter              | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| **`<dateExpression>`** | The date expression from which to extract the day of the week. |

## Examples

We'll use this document from the `stores` collection to demonstrate how `$dayOfWeek` works:

```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```

### Example 1: Extract day of the week

This example extracts the day of the week from the `lastUpdated` field.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      dayOfWeek: { $dayOfWeek: "$metadata.lastUpdated" }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]