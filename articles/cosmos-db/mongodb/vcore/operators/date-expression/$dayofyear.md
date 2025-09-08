---
title: $dayOfYear
titleSuffix: Overview of the $dayOfYear operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dayOfYear operator extracts the day of the year from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/08/2025
---

# $dayOfYear

The `$dayOfYear` operator extracts the day of the year from a date value, where 1 represents January 1. It's useful for grouping or filtering documents based on the day of the year.

## Syntax

```javascript
{
  $dayOfYear: <dateExpression>
}
```

## Parameters

| Parameter              | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| **`<dateExpression>`** | The date expression from which to extract the day of the year. |

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

### Example 1: Extract day of the year

This query uses the `$dayOfYear` operator to extract the ordinal day of the year (1–366) from the `lastUpdated` timestamp.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dayOfYear: { $dayOfYear: "$lastUpdated" }
    }
  }
])
```

The result shows the calendar day number on which `lastUpdated` occurred. In current example, 339 for December 4 in a nonleap year.

```json
{ "dayOfYear": 339 }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
