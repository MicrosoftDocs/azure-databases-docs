---
  title: $range
  titleSuffix: Overview of the $range operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $range operator allows generating an array of sequential integers.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/08/2025
---

# $range

The `$range` operator is used to generate an array of sequential integers. The operator helps create number arrays in a range, useful for pagination, indexing, or test data.

## Syntax

```javascript
{
    $range: [ <start>, <end>, <step> ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`start`** | The starting value of the range (inclusive). |
| **`end`** | The ending value of the range (exclusive). |
| **`step`** | The increment value between each number in the range (optional, defaults to 1). |

## Examples

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
  "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
  "location": { "lat": -74.0427, "lon": 160.8154 },
  "staff": { "employeeCount": { "fullTime": 9, "partTime": 18 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Stockings", "totalSales": 25731 } ],
    "revenue": 25731
  },
  "promotionEvents": [
    {
      "eventName": "Mega Savings Extravaganza",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 6, "Day": 29 },
        "endDate": { "Year": 2023, "Month": 7, "Day": 7 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 16 },
        { "categoryName": "Tree Ornaments", "discountPercentage": 8 }
      ]
    },
    {
      "eventName": "Incredible Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 11 },
        { "categoryName": "Holiday Cards", "discountPercentage": 9 }
      ]
    },
    {
      "eventName": "Massive Deal Mania",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 12, "Day": 26 },
        "endDate": { "Year": 2024, "Month": 1, "Day": 2 }
      },
      "discounts": [
        { "categoryName": "Gift Bags", "discountPercentage": 21 },
        { "categoryName": "Bows", "discountPercentage": 19 }
      ]
    },
    {
      "eventName": "Super Saver Soiree",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 3, "Day": 25 },
        "endDate": { "Year": 2024, "Month": 4, "Day": 1 }
      },
      "discounts": [
        { "categoryName": "Tree Ornaments", "discountPercentage": 15 },
        { "categoryName": "Stockings", "discountPercentage": 14 }
      ]
    },
    {
      "eventName": "Fantastic Savings Fiesta",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 6, "Day": 23 },
        "endDate": { "Year": 2024, "Month": 6, "Day": 30 }
      },
      "discounts": [
        { "categoryName": "Stockings", "discountPercentage": 24 },
        { "categoryName": "Gift Wrap", "discountPercentage": 16 }
      ]
    },
    {
      "eventName": "Price Plunge Party",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 9, "Day": 21 },
        "endDate": { "Year": 2024, "Month": 9, "Day": 28 }
      },
      "discounts": [
        { "categoryName": "Holiday Tableware", "discountPercentage": 13 },
        { "categoryName": "Holiday Cards", "discountPercentage": 11 }
      ]
    }
  ],
  "company": "Lakeshore Retail",
  "city": "Marvinfort",
  "storeOpeningDate": { "$date": "2024-10-01T18:24:02.586Z" },
  "lastUpdated": { "$timestamp": { "t": 1730485442, "i": 1 } },
  "storeFeatures": 38


### Example 1: Generate a range of numbers

The example demonstrates usage of operator to generate an array of integers from 0 to 5, wherein it includes the left boundary while excludes the right.

```javascript
db.stores.aggregate([
  { $match: { "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"} }
, {
    $project: {
      rangeArray: { $range: [0, 5] }
    }
  }
])
```

This query returns the following result.

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "rangeArray": [
            0,
            1,
            2,
            3,
            4
        ]
    }
]
```

### Example 2: Generate a range of numbers with a step value

The example demonstrates usage of operator to generate an array of even numbers from 0 to 18.

```javascript
db.stores.aggregate([
  { $match: { "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"} }
, {
    $project: {
      evenNumbers: { $range: [0, 8, 2] }
    }
  }
])
```

The query results the following result.

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "rangeArray": [
            0,
            2,
            4,
            6
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)].
