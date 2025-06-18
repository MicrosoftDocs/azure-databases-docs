---
  title: $millisecond (date expression)
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $millisecond operator extracts the milliseconds portion from a date value.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/16/2025
---

# $millisecond (date expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$millisecond` operator extracts the milliseconds portion from a date value, returning a number between 0 and 999. This operator is useful for precise timestamp analysis and filtering operations that require millisecond-level granularity.

## Syntax

The syntax for the `$millisecond` operator is as follows:

```javascript
{
  $millisecond: <dateExpression>
}
```

## Parameters

| | Description |
| --- | --- |
| **`dateExpression`** | An expression that resolves to a Date, a Timestamp, or an ObjectId. If the expression resolves to `null` or is missing, `$millisecond` returns `null`. |

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

### Example 1: Extract milliseconds from store opening date

This example extracts the milliseconds portion from the store opening date.

```javascript
db.stores.aggregate([
  { $match: {"_id": "905d1939-e03a-413e-a9c4-221f74055aac"} },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      openingMilliseconds: {
        $millisecond: "$storeOpeningDate"
      }
    }
  }
])
```

The query returns the milliseconds portion (779) from the store opening timestamp.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "storeOpeningDate": ISODate("2024-09-26T22:55:25.779Z"),
  "openingMilliseconds": 779
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]