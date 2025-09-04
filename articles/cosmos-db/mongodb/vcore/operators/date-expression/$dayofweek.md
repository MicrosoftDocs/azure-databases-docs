---
title: $dayOfWeek
titleSuffix: Overview of the $dayOfWeek operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dayOfWeek operator extracts the day of the week from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dayOfWeek

The `$dayOfWeek` operator extracts the day of the week from a date value, where 1 represents Sunday and 7 represents Saturday. It's useful for grouping or filtering documents based on the day of the week.

## Syntax

```javascript
{
  $dayOfWeek: <dateExpression>
}
```

## Parameters

| Parameter              | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| **`<dateExpression>`** | The date expression from which to extract the day of the week. |

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

### Example 1: Extract day of the week

This query uses the `$dayOfWeek` operator to extract the day of the week from the `lastUpdated` timestamp. The returned value ranges from 1 (Sunday) to 7 (Saturday), based on ISO-8601 ordering.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dayOfWeek: { $dayOfWeek: "$lastUpdated" }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "dayOfWeek": "4"
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
