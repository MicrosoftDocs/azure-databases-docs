---
title: $dateTrunc
titleSuffix: Overview of the $dateTrunc operator in Azure Cosmos DB for MongoDB vCore
description: The $dateTrunc operator in Azure Cosmos DB for MongoDB vCore truncates a date to a specified unit.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dateTrunc

The `$dateTrunc` expression operator truncates a date to the nearest specified unit (e.g., hour, day, month). It is particularly useful when working with time-series data or when grouping data by specific time intervals. This operator can be used to simplify and standardize date calculations.

## Syntax

```javascript
  $dateTrunc: {
    date: <dateExpression>,
    unit: "<unit>",
    binSize: <number>,       // optional
    timezone: "<timezone>",  // optional
    startOfWeek: "<day>"     // optional (used when unit is "week")
  }
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`date`** | The date to truncate. |
| **`unit`** | The unit to truncate the date to. Supported values include `year`, `month`, `week`, `day`, `hour`, `minute`, `second`, and `millisecond`. |
| **`binSize`** | (Optional) The size of each bin for truncation. For example, if `binSize` is 2 and `unit` is `hour`, the date will be truncated to every 2 hours. |
| **`timezone`** | (Optional) The timezone to use for truncation. Defaults to UTC if not specified. |

## Example(s)
We'll use this document from the `stores` collection to demonstrate how `$dateTrunc` works:
```json
{
  "_id": "store-01",
  "name": "Time Travel Mart",
  "metadata": {
    "lastUpdated": ISODate("2024-07-21T14:38:00Z")
  }
}
```
### Example 1: Truncate to the day
```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      truncatedToDay: {
        $dateTrunc: {
          date: "$metadata.lastUpdated",
          unit: "day"
        }
      }
    }
  }
])
```
This example normalizes all date and time values to the beginning of their respective day.

### Example 2: Truncate to the hour in a specific timezone
```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      truncatedToHour: {
        $dateTrunc: {
          date: "$metadata.lastUpdated",
          unit: "hour",
          timezone: "America/New_York"
        }
      }
    }
  }
])
```
This example adjusts dates to a specified timezone before truncating them to the hour.

### Example 3: Truncate to the start of the week
```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 0,
      truncatedToWeek: {
        $dateTrunc: {
          date: "$metadata.lastUpdated",
          unit: "week",
          startOfWeek: "Monday"
        }
      }
    }
  }
])
```
This example aligns dates to the beginning of a week, with a configurable start day.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]