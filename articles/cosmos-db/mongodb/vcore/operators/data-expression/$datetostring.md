---
title: $dateToString
titleSuffix: Overview of the $dateToString operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dateToString operator converts a date object into a formatted string.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dateToString

The `$dateToString` operator is used to convert a date object to a string in a specified format. It's commonly used in aggregation pipelines to format date fields for reporting, querying, or display purposes. This operator is highly versatile and allows you to define custom date formats.

## Syntax

```javascript
{
  $dateToString: {
    format: "<format_string>",
    date: <date_expression>,
    timezone: "<timezone>",
    onNull: "<replacement_value>"
  }
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`format`** | A string that specifies the format of the output date. |
| **`date`** | The date expression to format. |
| **`timezone`** | (Optional) A string that specifies the timezone. Defaults to UTC if not provided. |
| **`onNull`** | (Optional) A value to return if the `date` field is `null` or missing. |

## Format Specifiers

| Symbol | Meaning                  |
| ------ | ------------------------ |
| `%Y`   | Year (four digits)          |
| `%m`   | Month (two digits)         |
| `%d`   | Day of month (two digits)  |
| `%H`   | Hour (24-hour, two digits) |
| `%M`   | Minute (two digits)        |
| `%S`   | Second (two digits)        |
| `%L`   | Millisecond (three digits)   |

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

### Example 1: Formatting a date field to an ISO-like string

This query uses `$dateToString` operator to format the `lastUpdated` timestamp into a `YYYY-MM-DD` string. It helps present dates in a readable format suitable for logs, reports, or UI.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      formattedDate: {
        $dateToString: {
          format: "%Y-%m-%d",
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
    "formattedDate": "2024-12-04"
  }
]
```

### Example 2: Handling Null Values

This query formats the nonexistent field `lastUpdated_new` timestamp as a `YYYY-MM-DD` string using `$dateToString`. Considering the date is missing or null, it substitutes a fallback string "No date available" via the onNull option.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      formattedDateOrDefault: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$lastUpdated_new", // field doesn't exist
          onNull: "No date available"
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
    "formattedDateOrDefault": "No date available"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]


