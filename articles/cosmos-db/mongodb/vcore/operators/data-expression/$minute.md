---
  title: $minute (date expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $minute operator extracts the minute portion from a date value.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 06/16/2025
---

# $minute (date expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$minute` operator extracts the minute portion from a date value, returning a number between 0 and 59. This operator is commonly used for time-based analysis and scheduling operations.

## Syntax

The syntax for the `$minute` operator is as follows:

```javascript
{
  $minute: <dateExpression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, a Timestamp, or an ObjectId. If the expression resolves to `null` or is missing, `$minute` returns `null`. |

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
  "company": "Trey Research",
  "city": "Lake Freeda",
  "storeOpeningDate": ISODate("2024-09-26T22:55:25.779Z"),
  "lastUpdated": Timestamp({ "t": 1729983325, "i": 1 })
}
```

### Example 1: Extract minutes from store opening date

This example extracts the minute portion from the store opening date to analyze opening time patterns.

```javascript
db.stores.aggregate([
  { $match: {"_id": "905d1939-e03a-413e-a9c4-221f74055aac"} },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      openingMinute: {
        $minute: "$storeOpeningDate"
      }
    }
  }
])
```

The query returns the minute portion (55) from the store opening timestamp.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "storeOpeningDate": ISODate("2024-09-26T22:55:25.779Z"),
  "openingMinute": 55
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
