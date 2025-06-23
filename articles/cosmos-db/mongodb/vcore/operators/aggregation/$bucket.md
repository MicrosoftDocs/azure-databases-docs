---
title: $bucket (as Aggregation Pipeline Stages) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Groups input documents into buckets based on specified boundaries.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 09/27/2024
---

# $bucket (as Aggregation Pipeline Stages) usage on Azure Cosmos DB for MongoDB vCore

The `$bucket` stage in an aggregation pipeline groups input documents into buckets based on specified boundaries. This is especially useful for creating histograms or categorizing data into ranges. It allows you to define custom bucket boundaries and provides a way to summarize data within these ranges.

## Syntax

```json
{
  $bucket: {
    groupBy: <expression>,
    boundaries: [ <lowerBoundary>, <upperBoundary>, ... ],
    default: <defaultBucket>,
    output: {
      <outputField1>: { <accumulator1> },
      ...
    }
  }
}
```

## Parameters

| Parameter           | Description |
| ------------------- | ----------- |
| **`groupBy`**       | The expression to group documents by. |
| **`boundaries`**    | An array of boundary values to define the buckets. The array must be sorted in ascending order and include at least two values. |
| **`default`**       | The name of the bucket for documents that do not fall within the specified boundaries. |
| **`output`**        | An optional field to specify computed fields for each bucket. |

## Example(s)

### Example 1: Categorizing `fullSales` into ranges

The following example categorizes the `fullSales` field into three buckets: `[0, 1000)`, `[1000, 5000)`, and `[5000, 10000)`. Documents that do not fall into these ranges are grouped into a default bucket.

```json
db.sales.aggregate([
  {
    $bucket: {
      groupBy: "$sales.fullSales",
      boundaries: [0, 1000, 5000, 10000],
      default: "Other",
      output: {
        count: { $sum: 1 },
        totalSales: { $sum: "$sales.fullSales" }
      }
    }
  }
])
```

### Example 2: Categorizing promotional event discounts

The following example groups the discount percentages in the `promotionEvents.discounts` array into buckets: `[0, 10)`, `[10, 20)`, and `[20, 30)`.

```json
db.promotionEvents.aggregate([
  {
    $unwind: "$discounts"
  },
  {
    $bucket: {
      groupBy: "$discounts.discountPercentage",
      boundaries: [0, 10, 20, 30],
      default: "Other",
      output: {
        count: { $sum: 1 },
        averageDiscount: { $avg: "$discounts.discountPercentage" }
      }
    }
  }
])
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]