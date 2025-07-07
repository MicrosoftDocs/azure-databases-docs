---
  title: $sampleRate (miscellaneous expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $sampleRate operator allows randomly sampling documents from a collection at a specified rate.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $sampleRate (miscellaneous expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$sampleRate` operator is used to randomly sample documents from a collection at a specified rate. This operator is particularly useful for creating representative subsets of large datasets for analysis, testing, or performance optimization purposes.

## Syntax

The syntax for the `$sampleRate` operator is as follows:

```javascript
{
  $sampleRate: <number>
}
```

## Parameters

| | Description |
| --- | --- |
| **`rate`** | A number between 0 and 1 representing the sampling rate. For example, 0.3 means approximately 30% of documents will be included in the sample. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  },
  "sales": {
    "totalSales": 151864,
    "salesByCategory": [
      {
        "categoryName": "Sound Bars",
        "totalSales": 2120
      },
      {
        "categoryName": "Home Theater Projectors",
        "totalSales": 45004
      }
    ]
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
        }
      ]
    }
  ]
}
```

### Example 1: Basic sampling

Sample approximately 30% of stores for analysis:

```javascript
db.stores.aggregate([
  { $sampleRate: 0.3 },
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      fullTimeStaff: "$staff.totalStaff.fullTime"
    }
  }
])
```

This will produce an output with approximately 30% of the documents from the stores collection. The exact number may vary due to the random nature of sampling:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "totalSales": 151864,
  "fullTimeStaff": 19
}
// Additional sampled documents...
```

### Example 2: Sampling with Filtering

Sample 50% of stores that have total sales greater than 50,000:

```javascript
db.stores.aggregate([
  { $match: { "sales.totalSales": { $gt: 50000 } } },
  { $sampleRate: 0.5 },
  {
    $project: {
      name: 1,
      totalSales: "$sales.totalSales",
      location: 1
    }
  }
])
```

This will first filter stores with sales greater than 50,000, then sample approximately 50% of those matching documents:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "totalSales": 151864,
  "location": {
    "lat": 70.1272,
    "lon": 69.7296
  }
}
// Additional sampled documents...
```

### Example 3: Small Sample for Testing

Create a small 10% sample for testing purposes:

```javascript
db.stores.aggregate([
  { $sampleRate: 0.1 },
  {
    $project: {
      name: 1,
      totalStaff: {
        $add: ["$staff.totalStaff.fullTime", "$staff.totalStaff.partTime"]
      },
      promotionCount: { $size: "$promotionEvents" }
    }
  },
  { $sort: { totalStaff: -1 } }
])
```

This will produce a 10% sample of stores with calculated total staff and promotion event counts, sorted by total staff in descending order:

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "totalStaff": 39,
  "promotionCount": 6
}
// Additional sampled documents...
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]