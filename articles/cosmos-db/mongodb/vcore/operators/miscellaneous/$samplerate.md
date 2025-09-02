---
  title: $sampleRate
  titleSuffix: Overview of the $sampleRate operation in Azure Cosmos DB for MongoDB (vCore)
  description: The $sampleRate operator randomly samples documents from a collection based on a specified probability rate, useful for statistical analysis and testing.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 02/12/2025
---

# $sampleRate

The `$sampleRate` operator randomly samples documents from a collection based on a specified probability rate. This operator is useful for statistical analysis, testing with subset data, and performance optimization when working with large datasets where you need a representative sample.

## Syntax

The syntax for the `$sampleRate` operator is as follows:

```javascript
{ $match: { $sampleRate: <number> } }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`number`** | A floating-point number between 0 and 1 representing the probability that a document will be included in the sample. For example, 0.33 means approximately 33% of documents are sampled.

## Examples

Consider this sample document from the stores collection.

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

### Example 1: Basic random sampling

To randomly sample approximately 33% of all stores:

```javascript
db.stores.aggregate([
  { $match: { $sampleRate: 0.33 } }
])
```

This query returns one-third of all documents in the stores collection, selected randomly.

### Example 2: Sampling with more filters

To sample 50% of stores that have total sales greater than 50,000:

```javascript
db.stores.aggregate([
  { $match: { 
    "sales.totalSales": { $gt: 50000 },
    $sampleRate: 0.5 
  }}
])
```

This query first filters stores with sales above 50,000, then randomly samples 50% of those matching documents.

### Example 3: Sampling for statistical analysis

To get a 25% sample of stores and calculate average sales:

```javascript
db.stores.aggregate([
  { $match: { $sampleRate: 0.25 } },
  { $group: {
    _id: null,
    averageSales: { $avg: "$sales.totalSales" },
    totalStores: { $sum: 1 },
    maxSales: { $max: "$sales.totalSales" },
    minSales: { $min: "$sales.totalSales" }
  }}
])
```

This query samples 25% of stores and calculates statistical measures on the sampled data.

The $sampleRate operator is valuable for statistical analysis and data exploration when working with large datasets where processing all documents would be computationally expensive. It efficiently creates representative samples for performance testing, quality assurance validation, and machine learning dataset generation. The operator is ideal for approximate reporting scenarios where statistical accuracy is acceptable and processing speed is prioritized over exact precision.


## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
