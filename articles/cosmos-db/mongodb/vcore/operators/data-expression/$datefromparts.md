---
title: $dateFromParts
titleSuffix: Overview of the $dateDiff operator in Azure Cosmos DB for MongoDB (vCore)
description: Constructs a date from individual components.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/04/2025
---

# $dateFromParts

The `$dateFromParts` operator constructs a date from individual components such as year, month, day, hour, minute, second, and millisecond. This operator can be useful when dealing with data that stores date components separately.

## Syntax

```javascript
{
    $dateFromParts: {
        year: < year > ,
        month: < month > ,
        day: < day > ,
        hour: < hour > ,
        minute: < minute > ,
        second: < second > ,
        millisecond: < millisecond > ,
        timezone: < timezone >
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`year`** | The year component of the date. |
| **`month`** | The month component of the date. |
| **`day`** | The day component of the date. |
| **`hour`** | The hour component of the date. |
| **`minute`** | The minute component of the date. |
| **`second`** | The second component of the date. |
| **`millisecond`** | The millisecond component of the date. |
| **`timezone`** | Optional. A timezone specification. |

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

### Example 1: Constructing a start date

This aggregation query constructs precise startDate and endDate values from nested fields using `$dateFromParts`, then calculates the event duration in days. It helps standardize and analyze event timelines stored in fragmented date formats.

```javascript
db.stores.aggregate([
  { 
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } 
  },
  { 
    $unwind: "$promotionEvents" 
  },
  {
    $project: {
      _id: 1,
      startDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.startDate.Year",
          month: "$promotionEvents.promotionalDates.startDate.Month",
          day: "$promotionEvents.promotionalDates.startDate.Day"
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
    "startDate": "2024-09-21T00:00:00.000Z"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
