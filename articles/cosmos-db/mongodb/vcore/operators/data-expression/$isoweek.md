---
  title: $isoWeek (date expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $isoWeek operator returns the week number of the year in ISO 8601 format, ranging from 1 to 53.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/16/2025
---

# $isoWeek (date expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$isoWeek` operator returns the week number of the year in ISO 8601 format, ranging from 1 to 53. The operator accepts a date expression that resolves to a Date, Timestamp, or ObjectId. In ISO 8601, weeks start on Monday and the first week of the year is the week that contains the first Thursday of the year.

## Syntax

The syntax for the `$isoWeek` operator is as follows:

```javascript
{
  $isoWeek: <dateExpression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, Timestamp, or ObjectId. If the expression resolves to null or is missing, `$isoWeek` returns null. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "promotionEvents": [
    {
      "eventName": "Massive Markdown Mania",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 6,
          "Day": 29
        },
        "endDate": {
          "Year": 2023,
          "Month": 7,
          "Day": 9
        }
      }
    }
  ]
}
```

### Example 1: Get ISO week number for promotion events

The example demonstrates extracting the ISO week number for promotion event start dates.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
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
      }
    }
  },
  {
    $project: {
      eventName: 1,
      startDate: 1,
      isoWeekNumber: { $isoWeek: "$startDate" },
      year: { $year: "$startDate" }
    }
  }
])
```

The query returns the ISO week number for each promotion event start date.

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Massive Markdown Mania",
    "startDate": "2023-06-29T00:00:00.000Z",
    "isoWeekNumber": 26,
    "year": 2023
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Fantastic Deal Days",
    "startDate": "2023-09-27T00:00:00.000Z",
    "isoWeekNumber": 39,
    "year": 2023
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Discount Delight Days",
    "startDate": "2023-12-26T00:00:00.000Z",
    "isoWeekNumber": 52,
    "year": 2023
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Super Sale Spectacular",
    "startDate": "2024-03-25T00:00:00.000Z",
    "isoWeekNumber": 13,
    "year": 2024
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Grand Deal Days",
    "startDate": "2024-06-23T00:00:00.000Z",
    "isoWeekNumber": 25,
    "year": 2024
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Major Bargain Bash",
    "startDate": "2024-09-21T00:00:00.000Z",
    "isoWeekNumber": 38,
    "year": 2024
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
