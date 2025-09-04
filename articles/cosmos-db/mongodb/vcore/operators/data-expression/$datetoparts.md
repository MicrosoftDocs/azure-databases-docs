---
title: $dateToParts
titleSuffix: Overview of the $dateToParts operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dateToParts operator in Azure Cosmos DB for MongoDB vCore decomposes a date into its individual parts such as year, month, day, and more.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/04/2025
---

# $dateToParts

The `$dateToParts` operator is used to extract individual components (Year, Month, Day, Hour, Minute, Second, Millisecond, etc.) from a date object. The operator is useful for scenarios where manipulation or analysis of specific date parts is required, such as sorting, filtering, or aggregating data based on individual date components.

## Syntax

```javascript
$dateToParts: {
  date: <dateExpression>,
  timezone: <string>, // optional
  iso8601: <boolean> // optional
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`date`** | The date expression to extract parts from. |
| **`timezone`** | Optional. Specifies the timezone for the date. Defaults to UTC if not provided. |
| **`iso8601`** | Optional. If true, the operator uses ISO 8601 week date calendar system. Defaults to false. |

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

### Example 1: Extracting date parts from a field

This query uses `$dateToParts` to break down the `lastUpdated` date into components like year, month, day, and time. It helps in analyzing or transforming individual parts of a date for further processing.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dateParts: {
        $dateToParts: { 
          date: "$lastUpdated" 
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
    "dateParts": {
      "year": 2024,
      "month": 12,
      "day": 4,
      "hour": 11,
      "minute": 50,
      "second": 6,
      "millisecond": 0
    }
  }
]
```

### Example 2: Using timezone

This query extracts the `lastUpdated` timestamp of a specific document and breaks it into date parts like year, month, day, and hour using $dateToParts. Including the "America/New_York" timezone permits the breakdown, reflects the local time instead of UTC.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      datePartsWithTimezone: {
        $dateToParts: { 
          date: "$lastUpdated", 
          timezone: "America/New_York" 
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
    "datePartsWithTimezone": {
      "year": 2024,
      "month": 12,
      "day": 4,
      "hour": 6,
      "minute": 50,
      "second": 6,
      "millisecond": 0
    }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
