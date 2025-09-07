---
  title: $zip
  titleSuffix: Overview of the $zip operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $zip operator allows merging two or more arrays element-wise into a single array or arrays.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/08/2025
---

# $zip

The `$zip` operator is used to merge two or more arrays element-wise into a single array of arrays. It's useful when you want to combine related elements from multiple arrays into a single array structure.

## Syntax

```javascript
{
  $zip: {
    inputs: [ <array1>, <array2>, ... ],
    useLongestLength: <boolean>, // Optional
    defaults: <array> // Optional
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`inputs`** | An array of arrays to be merged element-wise. |
| **`useLongestLength`** | A boolean value that, if set to true, uses the longest length of the input arrays. If false or not specified, it uses the shortest length. |
| **`defaults`** | An array of default values to use if `useLongestLength` is true and any input array is shorter than the longest array. |

## Example

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
}
```

### Example 1: Basic Usage

Suppose you want to merge the `categoryName` and `totalSales` fields from the `salesByCategory` array.

```javascript
db.stores.aggregate([
  { $match: {"_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"} },
  {
    $project: {
      name:1,
      categoryNames: "$sales.salesByCategory.categoryName",
      totalSales: "$sales.salesByCategory.totalSales",
      categoryWithSales: {
        $zip: {
          inputs: ["$sales.salesByCategory.categoryName", "$sales.salesByCategory.totalSales"],
          useLongestLength: false
        }
      }
    }
  }
])
```

The query returns individual array of arrays under `categoryWithSales` field. `useLongestLength` set to `true` would return the following output, while a value of `false` removes the `Napkins` array from the output.

```json
{
  "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
  "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
  "categoryNames": ["Stockings"],
  "totalSales": [25731],
  "categoryWithSales": [["Stockings", 25731]]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
