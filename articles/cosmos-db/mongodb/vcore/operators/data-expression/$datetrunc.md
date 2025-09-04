---
title: $dateTrunc
titleSuffix: Overview of the $dateTrunc operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dateTrunc operator in Azure Cosmos DB for MongoDB vCore truncates a date to a specified unit.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/04/2025
---

# $dateTrunc

The `$dateTrunc` expression operator truncates a date to the nearest specified unit (for example, hour, day, month). It's useful when working with time-series data or when grouping data by specific time intervals. This operator can be used to simplify and standardize date calculations.

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
| **`binSize`** | (Optional) The size of each bin for truncation. For example, if `binSize` is 2 and `unit` is `hour`, the date is truncated to every 2 hours. |
| **`timezone`** | (Optional) The timezone to use for truncation. Defaults to UTC if not specified. |

## Examples

Consider this sample document from the stores collection.

```json
{
  "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
  "name": "Relecloud | Toy Collection - North Jaylan",
  "location": {
    "lat": 2.0797,
    "lon": -94.4134
  },
  "staff": {
    "employeeCount": {
      "fullTime": 7,
      "partTime": 4
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "Educational Toys",
        "totalSales": 3299
      }
    ],
    "revenue": 3299
  },
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 29
        }
      },
      "discounts": [
        {
          "categoryName": "Remote Control Toys",
          "discountPercentage": 6
        },
        {
          "categoryName": "Building Sets",
          "discountPercentage": 21
        }
      ]
    }
  ],
  "company": "Relecloud",
  "city": "North Jaylan",
  "lastUpdated": {
    "$timestamp": {
      "t": 1733313006,
      "i": 1
    }
  },
  "storeOpeningDate": "2024-09-05T11:50:06.549Z"
}
```

### Example 1: Truncate to the day

This query uses `$dateTrunc` to truncate the `lastUpdated` timestamp to the start of the day (00:00:00) in UTC. The operator is useful for grouping or comparing data by calendar day regardless of time.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      truncatedToDay: {
        $dateTrunc: {
          date: "$lastUpdated",
          unit: "day"
        }
      }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "truncatedToDay": "2024-11-29T00:00:00.000Z"
  }
]
```

### Example 2: Truncate to the start of the week

This query uses `$dateTrunc` to round the `lastUpdated` timestamp down to the start of its week. It specifies Monday as the start of the week to ensure consistent calendar alignment.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      truncatedToWeek: {
        $dateTrunc: {
          date: "$lastUpdated",
          unit: "week",
          startOfWeek: "Monday"
        }
      }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "truncatedToWeek": "2024-11-25T00:00:00.000Z"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]

