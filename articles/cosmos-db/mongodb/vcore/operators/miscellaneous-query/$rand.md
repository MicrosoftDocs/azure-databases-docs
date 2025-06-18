---
  title: $rand (Misc. Query) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $rand operator generates a random float value between 0 and 1.
  author: suvishodcitus
  ms.author: suvishod
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 02/12/2025
---

# $rand (misc. query)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$rand` operator generates a random float value between 0 and 1. This is useful for random sampling of documents or creating random values in aggregation pipelines. 

## Syntax

The syntax for the `$rand` operator is as follows:

```javascript
{ $rand: {} }
```

## Example

Let's understand the usage with sample data from the `stores` dataset.

```javascript
db.stores.aggregate([
   { 
     $project: {
       name: 1,
       randomValue: { $rand: {} },
       "sales.totalSales": 1
     }
   },
   { $limit: 2 }
])
```

This query adds a random value to each store document. When executed, it might return something like:

```json
[
  {
    "_id": "2cf3f885-9962-4b67-a172-aa9039e9ae2f",
    "name": "First Up Consultants | Bed and Bath Center - South Amir",
    "randomValue": 0.7645893472947384,
    "sales": {
      "totalSales": 37701
    }
  },
  {
    "_id": "40d6f4d7-50cd-4929-9a07-0a7a133c2e74",
    "name": "Proseware, Inc. | Home Entertainment Hub - East Linwoodbury",
    "randomValue": 0.23456789012345678,
    "sales": {
      "totalSales": 151864
    }
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
