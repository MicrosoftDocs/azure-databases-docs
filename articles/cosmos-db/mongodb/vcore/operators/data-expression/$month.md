---
  title: $month (date expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $month operator extracts the month portion from a date value.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/16/2025
---

# $month (date expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$month` operator extracts the month portion from a date value, returning a number between 1 and 12, where 1 represents January and 12 represents December. This operator is essential for seasonal analysis and monthly reporting.

## Syntax

The syntax for the `$month` operator is as follows:

```javascript
{
  $month: <dateExpression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, a Timestamp, or an ObjectId. If the expression resolves to `null` or is missing, `$month` returns `null`. |

## Example

Let's understand the usage with sample JSON from the `stores` dataset.

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

### Example 1: Extract month from store opening date

This example extracts the month portion from the store opening date to analyze seasonal opening patterns.

```javascript
db.stores.aggregate([
  { $match: {"_id": "905d1939-e03a-413e-a9c4-221f74055aac"} },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      openingMonth: {
        $month: "$storeOpeningDate"
      },
      openingMonthName: {
        $switch: {
          branches: [
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 1] }, then: "January" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 2] }, then: "February" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 3] }, then: "March" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 4] }, then: "April" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 5] }, then: "May" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 6] }, then: "June" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 7] }, then: "July" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 8] }, then: "August" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 9] }, then: "September" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 10] }, then: "October" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 11] }, then: "November" },
            { case: { $eq: [{ $month: "$storeOpeningDate" }, 12] }, then: "December" }
          ]
        }
      }
    }
  }
])
```

The query returns the month portion (9) from the store opening timestamp, representing September.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "storeOpeningDate": ISODate("2024-09-26T22:55:25.779Z"),
  "openingMonth": 9,
  "openingMonthName": "September"
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
