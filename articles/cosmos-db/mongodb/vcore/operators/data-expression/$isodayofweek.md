---
  title: $isoDayOfWeek (date expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $isoDayOfWeek operator returns the weekday number in ISO 8601 format, ranging from 1 (Monday) to 7 (Sunday).
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $isoDayOfWeek (date expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$isoDayOfWeek` operator returns the weekday number in ISO 8601 format, ranging from 1 (Monday) to 7 (Sunday). The operator accepts a date expression that resolves to a Date, Timestamp, or ObjectId.

## Syntax

The syntax for the `$isoDayOfWeek` operator is as follows:

```javascript
{
  $isoDayOfWeek: <dateExpression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, Timestamp, or ObjectId. If the expression resolves to null or is missing, `$isoDayOfWeek` returns null. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296,
    "address": "123 Entertainment Blvd",
    "city": "East Linwoodbury"
  },
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
      },
      "discounts": [
        {
          "categoryName": "DVD Players",
          "discountPercentage": 14
        },
        {
          "categoryName": "Projector Lamps",
          "discountPercentage": 6
        }
      ]
    },
    {
      "eventName": "Fantastic Deal Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2023,
          "Month": 9,
          "Day": 27
        },
        "endDate": {
          "Year": 2023,
          "Month": 10,
          "Day": 7
        }
      },
      "discounts": [
        {
          "categoryName": "TV Mounts",
          "discountPercentage": 15
        }
      ]
    },
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
      },
      "discounts": [
        {
          "categoryName": "Game Controllers",
          "discountPercentage": 22
        },
        {
          "categoryName": "Home Theater Projectors",
          "discountPercentage": 23
        },
        {
          "categoryName": "Sound Bars",
          "discountPercentage": 10
        }
      ]
    },
    {
      "eventName": "Super Sale Spectacular",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 25
        },
        "endDate": {
          "Year": 2024,
          "Month": 4,
          "Day": 2
        }
      },
      "discounts": [
        {
          "categoryName": "PlayStation Games",
          "discountPercentage": 22
        },
        {
          "categoryName": "TV Mounts",
          "discountPercentage": 9
        },
        {
          "categoryName": "Mobile Games",
          "discountPercentage": 20
        }
      ]
    },
    {
      "eventName": "Grand Deal Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 6,
          "Day": 23
        },
        "endDate": {
          "Year": 2024,
          "Month": 6,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Remote Controls",
          "discountPercentage": 7
        },
        {
          "categoryName": "Televisions",
          "discountPercentage": 11
        },
        {
          "categoryName": "Business Projectors",
          "discountPercentage": 13
        }
      ]
    },
    {
      "eventName": "Major Bargain Bash",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 21
        },
        "endDate": {
          "Year": 2024,
          "Month": 9,
          "Day": 30
        }
      },
      "discounts": [
        {
          "categoryName": "Sound Bars",
          "discountPercentage": 9
        },
        {
          "categoryName": "VR Games",
          "discountPercentage": 7
        }
      ]
    }
  ],
  "company": "Proseware, Inc.",
  "city": "East Linwoodbury",
  "storeOpeningDate": "2024-09-23T13:45:01.480Z",
  "lastUpdated": "2025-06-11T11:06:57.922Z",
  "status": "active",
  "category": "high-volume",
  "priority": 1,
  "reviewDate": "2025-06-11T11:10:50.276Z"
}
```

### Example 1: Analyze promotion events by day of week

The example reviews promotion events to see which days of the week they typically started on.

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
    $group: {
      _id: { $isoDayOfWeek: "$startDate" },
      eventCount: { $sum: 1 },
      events: { $push: "$eventName" }
    }
  },
  {
    $project: {
      _id: 1,
      dayName: {
        $switch: {
          branches: [
            { case: { $eq: ["$_id", 1] }, then: "Monday" },
            { case: { $eq: ["$_id", 2] }, then: "Tuesday" },
            { case: { $eq: ["$_id", 3] }, then: "Wednesday" },
            { case: { $eq: ["$_id", 4] }, then: "Thursday" },
            { case: { $eq: ["$_id", 5] }, then: "Friday" },
            { case: { $eq: ["$_id", 6] }, then: "Saturday" },
            { case: { $eq: ["$_id", 7] }, then: "Sunday" }
          ]
        }
      },
      eventCount: 1,
      events: 1
    }
  },
  { $sort: { "_id": 1 } }
])
```

The query returns promotion events grouped by the ISO day of week they start on.

```json
  {
    "_id": 1,
    "eventCount": 1,
    "events": ["Super Sale Spectacular"],
    "dayName": "Monday"
  },
  {
    "_id": 2,
    "eventCount": 1,
    "events": ["Discount Delight Days"],
    "dayName": "Tuesday"
  },
  {
    "_id": 3,
    "eventCount": 1,
    "events": ["Fantastic Deal Days"],
    "dayName": "Wednesday"
  },
  {
    "_id": 4,
    "eventCount": 1,
    "events": ["Massive Markdown Mania"],
    "dayName": "Thursday"
  },
  {
    "_id": 6,
    "eventCount": 1,
    "events": ["Major Bargain Bash"],
    "dayName": "Saturday"
  },
  {
    "_id": 7,
    "eventCount": 1,
    "events": ["Grand Deal Days"],
    "dayName": "Sunday"
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]