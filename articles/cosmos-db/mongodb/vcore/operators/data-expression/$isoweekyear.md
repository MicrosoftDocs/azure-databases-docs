---
  title: $isoWeekYear
  titleSuffix: Overview of the $isoWeekYear operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $isoWeekYear operator returns the year number in ISO 8601 format, which can differ from the calendar year for dates at the beginning or end of the year.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/04/2025
---

# $isoWeekYear

The `$isoWeekYear` operator returns the year number in ISO 8601 format. The ISO week-numbering year can differ from the calendar year for dates at the beginning or end of the year. The ISO week year is the year that contains the Thursday of the week in question.

## Syntax

```javascript
{
  $isoWeekYear: <dateExpression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, Timestamp, or ObjectId. If the expression resolves to null or is missing, `$isoWeekYear` returns null. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "promotionEvents": [
    {
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 12,
          "Day": 26
        },
        "endDate": {
          "Year": 2024,
          "Month": 1,
          "Day": 5
        }
      }
    }
  ]
}
```

### Example 1: Compare calendar year vs ISO week year

This example demonstrates the difference between calendar year and ISO week year, especially for dates near year boundaries.

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
      },
      endDate: {
        $dateFromParts: {
          year: "$promotionEvents.promotionalDates.endDate.Year",
          month: "$promotionEvents.promotionalDates.endDate.Month",
          day: "$promotionEvents.promotionalDates.endDate.Day"
        }
      }
    }
  },
  {
    $project: {
      eventName: 1,
      startDate: 1,
      endDate: 1,
      startCalendarYear: { $year: "$startDate" },
      startISOWeekYear: { $isoWeekYear: "$startDate" },
      endCalendarYear: { $year: "$endDate" },
      endISOWeekYear: { $isoWeekYear: "$endDate" },
      yearDifference: {
        $ne: [{ $year: "$startDate" }, { $isoWeekYear: "$startDate" }]
      }
    }
  },
  { $match: {"eventName": "Discount Delight Days" } }
])
```

The query compares calendar year and ISO week year for promotion dates.

```json
[
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "eventName": "Discount Delight Days",
    "startDate": "2023-12-26T00:00:00.000Z",
    "endDate": "2024-01-05T00:00:00.000Z",
    "startCalendarYear": 2023,
    "startISOWeekYear": Long("2023"),
    "endCalendarYear": 2024,
    "endISOWeekYear": Long("2024"),
    "yearDifference": true
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
