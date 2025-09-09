---
title: $dateSubtract
titleSuffix: Overview of the $dateSubtract operator in Azure Cosmos DB for MongoDB (vCore)
description: The $dateSubtract operator subtracts a specified amount of time from a date.
author: patty-chow
ms.author: pattychow
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 06/24/2025
---

# $dateSubtract

The `$dateSubtract` operator subtracts a specified time unit from a date. It's useful for calculating past dates or intervals in aggregation pipelines.

## Syntax

```javascript
{
  $dateSubtract: {
    startDate: <dateExpression>,
    unit: "<unit>",
    amount: <number>,
    timezone: "<timezone>" // optional
  }
}
```

## Parameters

| Parameter       | Description                                      |
| --------------- | ------------------------------------------------ |
| **`startDate`** | The date expression to subtract from.            |
| **`unit`**      | The time unit to subtract (for example, "day", "hour"). |
| **`amount`**    | The amount of the time unit to subtract.         |
| **`timezone`**  | *(Optional)* Timezone for date calculation.      |

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

### Example 1: Subtract seven days

This example calculates the date one week before the `lastUpdated` field. This query uses `$dateSubtract` to calculate the date exactly seven days before the `storeOpeningDate` timestamp.

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      dateOneWeekAgo: {
        $dateSubtract: {
          startDate: "$storeOpeningDate",
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
    "dateOneWeekAgo": "2024-08-29T11:50:06.549Z"
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]


