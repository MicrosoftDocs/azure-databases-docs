---
title: $dayOfYear
titleSuffix: Overview of the $dayOfYear operator in Azure Cosmos DB for MongoDB vCore
description: The $dayOfYear operator in Azure Cosmos DB for MongoDB vCore extracts the day of the year from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---
# $dayOfYear

The `$dayOfYear` operator extracts the day of the year from a date value, where 1 represents January 1. It's useful for grouping or filtering documents based on the day of the year.

## Syntax

```javascript
{ $dayOfYear: <dateExpression> }
```

## Parameters

| Parameter              | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| **`<dateExpression>`** | The date expression from which to extract the day of the year. |

## Examples

We'll use this document from the `stores` collection to demonstrate how `$dayOfYear` works:

```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```

### Example 1: Extract day of the year

This example extracts the day of the year from the `lastUpdated` field.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      dayOfYear: { $dayOfYear: "$metadata.lastUpdated" }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]