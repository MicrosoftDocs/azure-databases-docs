---
title: $dateSubtract
titleSuffix: Overview of the $dateSubtract operator in Azure Cosmos DB for MongoDB vCore
description: The $dateSubtract operator in Azure Cosmos DB for MongoDB vCore subtracts a specified amount of time from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dateSubtract

The `$dateSubtract` operator subtracts a specified time unit from a date. It's useful for calculating past dates or intervals in aggregation pipelines.

## Syntax

```javascript
{
  $dateSubtract: {
    startDate: <dateExpression>,
    unit: "<unit>",
    amount: <number>,
    timezone: "<timezone>" // optional
  }
}
```

## Parameters

| Parameter       | Description                                      |
| --------------- | ------------------------------------------------ |
| **`startDate`** | The date expression to subtract from.            |
| **`unit`**      | The time unit to subtract (e.g., "day", "hour"). |
| **`amount`**    | The amount of the time unit to subtract.         |
| **`timezone`**  | *(Optional)* Timezone for date calculation.      |

## Examples

We'll use this document from the `stores` collection to demonstrate how `$dateSubtract` works:

```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```

### Example 1: Subtract seven days

This example calculates the date one week before the `lastUpdated` field.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      dateOneWeekAgo: {
        $dateSubtract: {
          startDate: "$metadata.lastUpdated",
          unit: "day",
          amount: 7
        }
      }
    }
  }
])
```

### Example 2: Subtract two hours with timezone

This example subtracts two hours, considering the `America/New_York` timezone.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      dateTwoHoursAgo: {
        $dateSubtract: {
          startDate: "$metadata.lastUpdated",
          unit: "hour",
          amount: 2,
          timezone: "America/New_York"
        }
      }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]