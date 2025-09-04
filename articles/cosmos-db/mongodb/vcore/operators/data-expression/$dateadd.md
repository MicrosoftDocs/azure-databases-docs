---
title: $dateAdd
titleSuffix: Overview of the $dateAdd operator in Azure Cosmos DB for MongoDB (vCore)
description: Adds a specified number of time units (day, hour, month etc) to a date.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/04/2025
---

# $dateAdd

The `$dateAdd` operator adds a specified number of time units to a date. It's useful in scenarios where you need to calculate future dates based on a given date and a time interval.

## Syntax

```javascript
$dateAdd: {
   startDate: <expression>,
   unit: <string>,
   amount: <number>,
   timezone: <string>  // Optional
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`startDate`** | The starting date for the addition operation. |
| **`unit`** | The unit of time to add. Valid units include: `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`, `millisecond`. |
| **`amount`** | The number of units to add. |
| **`timezone`** | Optional. The timezone to use for the operation. |

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

### Example 1: Adding days to a date

The query projects `eventName` and computes a `newEndDate` by adding 7 days to a date constructed from nested year, month, and day fields. The result is a simplified document showing the event name and its extended end date.

```javascript
db.stores.aggregate([
  { $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.promotionalDates" },
  {
    $project: {
      eventName: 1,
      newEndDate: {
        $dateAdd: {
          startDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.endDate.Year",
              month: "$promotionEvents.promotionalDates.endDate.Month",
              day: "$promotionEvents.promotionalDates.endDate.Day"
            }
          },
          unit: "day",
          amount: 7
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
     "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
     "newEndDate": "2024-10-06T00:00:00.000Z"
   }
]
```

### Example 2: Adding months to a date

The aggregation query projects the `eventName` and calculates a newStartDate by adding 1 month to a reconstructed start date from nested promotion fields. It helps determine an adjusted event start date based on the original schedule. The query returns each document’s eventName and a newStartDate that is 1 month after the original startDate from nested promotion event data.

```javascript
db.stores.aggregate([
  { $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
  { $unwind: "$promotionEvents" },
  { $unwind: "$promotionEvents.promotionalDates" },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      newStartDate: {
        $dateAdd: {
          startDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.startDate.Year",
              month: "$promotionEvents.promotionalDates.startDate.Month",
              day: "$promotionEvents.promotionalDates.startDate.Day"
            }
          },
          unit: "month",
          amount: 1
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
     "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
     "eventName": "Massive Markdown Mania",
     "newStartDate": "2024-10-21T00:00:00.000Z"
   }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
