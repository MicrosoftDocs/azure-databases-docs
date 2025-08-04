---
  title: $toDate
  titleSuffix: Overview of the $toDate operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $toDate operator converts a value to a date.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/04/2025
---

# $toDate

The `$toDate` operator converts a value to a date. The operator accepts various input formats including strings, numbers (representing milliseconds since Unix epoch), ObjectId, and Timestamp values. This operator is essential for data transformation and type conversion operations.

## Syntax

```javascript
{
  $toDate: <expression>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`expression`** | An expression that can be converted to a date. Supported formats include: ISO date strings, milliseconds since Unix epoch (number), ObjectId, and Timestamp. If the expression can't be converted to a date, the operation returns an error. |

## Example

Let's understand the usage with sample json from the `stores` dataset.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "location": { "lat": -48.9752, "lon": -141.6816 },
  "staff": { "employeeCount": { "fullTime": 12, "partTime": 19 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Desk Lamps", "totalSales": 37978 } ],
    "revenue": 37978
  },
  "promotionEvents": [
    {
      "eventName": "Crazy Deal Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      }
    }
  ],
  "company": "Trey Research",
  "city": "Lake Freeda",
  "storeOpeningDate": ISODate("2024-09-26T22:55:25.779Z"),
  "lastUpdated": Timestamp({ "t": 1729983325, "i": 1 })
}
```

### Example 1: Convert timestamp to date

The example converts a Unix timestamp to a proper date format for better readability and date operations.

```javascript
db.stores.aggregate([
  { $match: { "_id": "905d1939-e03a-413e-a9c4-221f74055aac" } },
  {
    $project: {
      name: 1,
      lastUpdated: 1,
      lastUpdatedAsDate: { $toDate: "$lastUpdated" }
    }
  }
])
```

The query converts the timestamp field to a readable date format.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "lastUpdated": { "t": 1729983325, "i": 1 },
  "lastUpdatedAsDate": ISODate("2024-10-26T22:55:25.000Z")
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
