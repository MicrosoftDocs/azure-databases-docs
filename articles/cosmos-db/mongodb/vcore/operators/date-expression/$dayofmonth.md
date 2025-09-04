---
title: $dayOfMonth
titleSuffix: Overview of the $dayOfMonth operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dayOfMonth operator extracts the day of the month from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/04/2025
---

# $dayOfMonth

The `$dayOfMonth` operator extracts the day of the month (1–31) from a date value. It's useful for grouping or filtering documents based on the day of the month.

## Syntax

```javascript
{
  $dayOfMonth: <dateExpression>
}
```

## Parameters

| Parameter              | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| **`<dateExpression>`** | The date expression from which to extract the day of the month. |

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

### Example 1: Extract day of the month

This query uses the `$dayOfMonth` operator to extract the day of the month (1–31) from the `lastUpdated` timestamp and isolates the date component of the field for reporting or grouping.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dayOfMonth: { $dayOfMonth: "$lastUpdated" }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "dayOfMonth": "4"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
