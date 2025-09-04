---
  title: $hour
  titleSuffix: Overview of the $hour operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $hour operator returns the hour portion of a date as a number between 0 and 23.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/04/2025
---

# $hour

The `$hour` operator returns the hour portion of a date as a number between 0 and 23. The operator accepts a date expression that resolves to a Date, Timestamp, or ObjectId.

## Syntax

```javascript
{
  $hour: <dateExpression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, Timestamp, or ObjectId. If the expression resolves to null or is missing, `$hour` returns null. |

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

### Example 1: Extract hour from current date

This query extracts the `hour` from the current date and time.

```javascript
db.stores.aggregate([
  { $match: { "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a" } },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      currentHour: { $hour: new Date() },
      documentHour: { $hour: "$storeOpeningDate" }
    }
  }
])
```

This query returns the following result.

```json
[
  {
    "_id": "e6410bb3-843d-4fa6-8c70-7472925f6d0a",
    "name": "Relecloud | Toy Collection - North Jaylan",
    "storeOpeningDate": "2024-09-05T11:50:06.549Z",
    "currentHour": 12,
    "documentHour": 11
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
