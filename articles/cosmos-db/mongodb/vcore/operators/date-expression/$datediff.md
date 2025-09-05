--- 
title: $dateDiff
titleSuffix: Overview of the $dateDiff operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dateDiff operator calculates the difference between two dates in various units such as years, months, days, etc.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/04/2025
---

# $dateDiff

The `$dateDiff` operator calculates the difference between two dates in various units such as years, months, days, etc. It's useful for determining the duration between two timestamps in your dataset.

## Syntax

```javascript
$dateDiff: {
   startDate: <expression>,
   endDate: <expression>,
   unit: <string>,
   timezone: <string>, // Optional
   startOfWeek: <string> // Optional
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`startDate`**| The beginning date for the calculation.|
| **`endDate`**| The ending date for the calculation.|
| **`unit`**| The unit of time to measure the difference. Valid values include: `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`, `millisecond`.|
| **`timezone`**| Optional. The timezone to use for the calculation.|
| **`startOfWeek`**| Optional. The starting day of the week. Valid values are: `Sunday`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`.|

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

## Example 1: Calculate duration in days between two dates

This query uses `$dateDiff` to compute the number of units (e.g., days, months) between two date fields. It helps measure durations like event length or time since a given date. This query returns the durationInDays along with other fields for the specified `stores` document.

```javascript
db.stores.aggregate([
  { $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
  { $unwind: "$promotionEvents" },
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      startDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.startDate.Year",
          month: "$promotionEvents.promotionalDates.startDate.Month",
          day: "$promotionEvents.promotionalDates.startDate.Day"
        }
      },
      endDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.endDate.Year",
          month: "$promotionEvents.promotionalDates.endDate.Month",
          day: "$promotionEvents.promotionalDates.endDate.Day"
        }
      },
      durationInDays: {
        $dateDiff: {
          startDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.startDate.Year",
              month: "$promotionEvents.promotionalDates.startDate.Month",
              day: "$promotionEvents.promotionalDates.startDate.Day"
            }
          },
          endDate: {
            $dateFromParts: {
              year: "$promotionEvents.promotionalDates.endDate.Year",
              month: "$promotionEvents.promotionalDates.endDate.Month",
              day: "$promotionEvents.promotionalDates.endDate.Day"
            }
          },
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
     "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
     "eventName": "Massive Markdown Mania",
     "startDate": "2024-09-21T00:00:00.000Z",
     "endDate": "2024-09-29T00:00:00.000Z",
     "durationInDays": 8
   }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
