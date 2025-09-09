---
title: $dateFromString
titleSuffix: Overview of the $dateDiff operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dateDiff operator converts a date/time string to a date object.
author: niklarin
ms.author: nlarin
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/04/2025
---

# $dateFromString

The `$dateFromString` operator is used to convert a date/time string to a date object. This operation can be useful when dealing with string representations of dates that need to be manipulated or queried as date objects.

## Syntax

```javascript
{
    $dateFromString: {
        dateString: < string > ,
        format: < string > ,
        timezone: < string > ,
        onError: < expression > ,
        onNull: < expression >
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`dateString`** | The date/time string to convert to a date object. |
| **`format`** | (Optional) The date format specification of the `dateString`. |
| **`timezone`** | (Optional) The timezone to use to format the date. |
| **`onError`** | (Optional) The value to return if an error occurs while parsing the `dateString`. |
| **`onNull`** | (Optional) The value to return if the `dateString` is `null` or missing. |

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

### Example 1: Convert promotional event dates to ISO dates

The example constructs full ISO date strings from individual year, month, and day fields using `$concat` and converts them to startDate and endDate using `$dateFromString`. It’s useful when date components are stored separately in documents.

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
      eventName: "$promotionEvents.eventName",
      startDate: {
        $dateFromString: {
          dateString: {
            $concat: [
              { $toString: "$promotionEvents.promotionalDates.startDate.Year" },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.startDate.Month", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.startDate.Month" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.startDate.Month" }
                }
              },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.startDate.Day", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.startDate.Day" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.startDate.Day" }
                }
              }
            ]
          }
        }
      },
      endDate: {
        $dateFromString: {
          dateString: {
            $concat: [
              { $toString: "$promotionEvents.promotionalDates.endDate.Year" },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.endDate.Month", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.endDate.Month" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.endDate.Month" }
                }
              },
              "-",
              {
                $cond: {
                  if: { $lt: ["$promotionEvents.promotionalDates.endDate.Day", 10] },
                  then: { $concat: ["0", { $toString: "$promotionEvents.promotionalDates.endDate.Day" }] },
                  else: { $toString: "$promotionEvents.promotionalDates.endDate.Day" }
                }
              }
            ]
          }
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
    "endDate": "2024-09-29T00:00:00.000Z"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
