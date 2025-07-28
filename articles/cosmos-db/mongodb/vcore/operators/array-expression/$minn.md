---
  title: $minN
  titleSuffix: Overview of the $minN operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $minN operator returns the n smallest values from an array.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $minN

The `$minN` operator returns the n smallest values from an array. It's useful when you want to find the lowest performing items based on numerical values, such as the smallest sales figures or lowest discount percentages.

## Syntax

```javascript
{
  $minN: {
    input: <array>,
    n: <number>
  }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`input`** | The array used to get the n smallest values. The array should contain numerical values. |
| **`n`** | The number of smallest values to return. Must be a positive integer. |

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
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
      },
      {
        "categoryName": "Game Controllers",
        "totalSales": 43522
      },
      {
        "categoryName": "Remote Controls",
        "totalSales": 28946
      },
      {
        "categoryName": "VR Games",
        "totalSales": 32272
      }
    ]
  },
  "staff": {
    "totalStaff": {
      "fullTime": 19,
      "partTime": 20
    }
  }
}
```

### Example 1: Get lowest two sales values

The aggregation query extracts the two lowest sales values for a specific store document.

```javascript
db.stores.aggregate([
  { $match: {"_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74"} },
  {
    $project: {
      name: 1,
      lowestTwoSales: {
        $minN: {
          input: "$sales.salesByCategory.totalSales",
          n: 2
        }
      }
    }
  }
])
```

The query was directed towards a sample document for a store to review and help identify lowest sale values.

```json
{
  "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
  "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
  "lowestTwoSales": [2120, 28946]
}
```

### Example 2: Identify underperforming categories across all stores

The query finds the stores with the lowest two sales values across all stores, to identify consistently underperforming product categories.

```javascript
db.stores.aggregate([
  { $match: { "sales.salesByCategory": { $exists: true, $ne: [] } } },
  {
    $project: {
      name: 1,
      location: 1,
      bottomTwoSales: {
        $minN: {
          input: "$sales.salesByCategory.totalSales",
          n: 2
        }
      }
    }
  },
  { $sort: { "bottomTwoSales.0": 1 } },
  { $limit: 3 }
])
```

The query returns the three stores with the overall lowest minimum sales values, helping identify locations that require support or, different product strategies.

```json
{
    "_id": "c601ced7-d472-47e8-91c1-f213e3f60250",
    "name": "Tailwind Traders | Bed and Bath Bazaar - West Imaniside",
    "location": { "lat": -41.113, "lon": -108.3752 },
    "bottomTwoSales": [101, 12774]
  },
  {
    "_id": "09782c05-a134-43a1-a65b-6a332bc89d7c",
    "name": "Tailwind Traders | Microphone Deals - Sonnytown",
    "location": { "lat": -61.9575, "lon": 55.2523 },
    "bottomTwoSales": [102, 18531]
  },
  {
    "_id": "57303916-24f1-43a9-a50c-b96fb76ae40c",
    "name": "Fabrikam, Inc. | Art Supply Boutique - Port Geovanni",
    "location": { "lat": 63.9018, "lon": -125.7517 },
    "bottomTwoSales": [102, 6352]
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
