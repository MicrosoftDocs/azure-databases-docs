---
  title: $week
  titleSuffix: Overview of the $week operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $week operator returns the week number for a date as a value between 0 and 53.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 08/04/2025
---

# $week

The `$week` operator returns the week number for a date as a value between 0 and 53. Week 0 begins on January 1, and subsequent weeks begin on Sundays. If the date is null or missing, `$week` returns null.

## Syntax

The syntax for the `$week` operator is as follows:

```javascript
{
  $week: <dateExpression>
}
```

Or with timezone specification

```javascript
{
  $week: {
    date: <dateExpression>,
    timezone: <timezoneExpression>
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`dateExpression`** | Any expression that resolves to a Date, Timestamp, or ObjectId. |
| **`timezone`** | Optional. The timezone to use for the calculation. Can be an Olson Timezone Identifier (for example, "America/New_York") or a UTC offset (for example, "+0530"). |

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
      },
      "discounts": [
        { "categoryName": "Desks", "discountPercentage": 22 },
        { "categoryName": "Filing Cabinets", "discountPercentage": 23 }
      ]
    }
  ],
  "company": "Trey Research",
  "city": "Lake Freeda",
  "storeOpeningDate": ISODate("2024-12-30T22:55:25.779Z"),
  "lastUpdated": { "t": 1729983325, "i": 1 }
}
```

### Example 1: Get week number for store opening date

The example extracts the week number from the store opening date.

```javascript
db.stores.aggregate([
  { $match: { "_id": "905d1939-e03a-413e-a9c4-221f74055aac" } },
  {
    $project: {
      name: 1,
      storeOpeningDate: 1,
      openingWeek: { $week: { $toDate: "$storeOpeningDate" } }
    }
  }
])
```

The query returns the week number for the corresponding date value in ``storeOpeningDate` field.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "storeOpeningDate": ISODate("2024-12-30T22:55:25.779Z"),
  "openingWeek": 52
}
```

### Example 2: Group stores by opening week

The example groups stores by the week they were opened for analysis.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,
      openingWeek: { $week: { $toDate: "$storeOpeningDate" } },
      openingYear: { $year: { $toDate: "$storeOpeningDate" } }
    }
  },
  {
    $group: {
      _id: { week: "$openingWeek", year: "$openingYear" },
      storeCount: { $sum: 1 },
      stores: { $push: "$name" }
    }
  },
  { $sort: { "_id.year": 1, "_id.week": -1 } },
  { $limit : 3 } ])
```

The query groups stores by their opening week and year.

```json
  {
    "_id": { "week": 40, "year": 2021 },
    "storeCount": 1,
    "stores": [ "First Up Consultants | Bed and Bath Center - South Amir" ]
  },
  {
    "_id": { "week": 52, "year": 2024 },
    "storeCount": 1,
    "stores": [ "Trey Research | Home Office Depot - Lake Freeda" ]
  },
  {
    "_id": { "week": 50, "year": 2024 },
    "storeCount": 2,
    "stores": [
      "Fourth Coffee | Paper Product Bazaar - Jordanechester",
      "Adatum Corporation | Pet Supply Center - West Cassie"
    ]
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
