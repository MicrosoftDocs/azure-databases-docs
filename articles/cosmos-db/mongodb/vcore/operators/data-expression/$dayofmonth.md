---
title: $dayOfMonth
titleSuffix: Overview of the $dayOfMonth operator in Azure Cosmos DB for MongoDB vCore
description: The $dayOfMonth operator in Azure Cosmos DB for MongoDB vCore extracts the day of the month from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dayOfMonth

The `$dayOfMonth` operator extracts the day of the month (1–31) from a date value. It is useful for grouping or filtering documents based on the day of the month.

## Syntax

```javascript
{ $dayOfMonth: <dateExpression> }
```

## Parameters

| Parameter              | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| **`<dateExpression>`** | The date expression from which to extract the day of the month. |

## Examples

We'll use this document from the `stores` collection to demonstrate how `$dayOfMonth` works:

```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```

### Example 1: Extract day of the month

This example extracts the day of the month from the `lastUpdated` field.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      dayOfMonth: { $dayOfMonth: "$metadata.lastUpdated" }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]