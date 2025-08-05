---
title: $bucket
titleSuffix: Overview of the $addFields operator in Azure Cosmos DB for MongoDB (vCore)
description: Groups input documents into buckets based on specified boundaries.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 06/23/2025
---

# $bucket

The `$bucket` stage in an aggregation pipeline groups input documents into buckets based on specified boundaries. This is especially useful for creating histograms or categorizing data into ranges. It allows you to define custom bucket boundaries and provides a way to summarize data within these ranges.

## Syntax

```javascript
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

| Parameter | Description |
| --- | --- |
| **`groupBy`** | The expression to group documents by. |
| **`boundaries`** | An array of boundary values to define the buckets. The array must be sorted in ascending order and include at least two values. |
| **`default`** | The name of the bucket for documents that do not fall within the specified boundaries. |
| **`output`** | An optional field to specify computed fields for each bucket. |

## Examples

Consider this sample document from the stores collection.
```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### Example 1: Categorizing `fullSales` into ranges

The following example categorizes the `fullSales` field into three buckets: `[0, 1000)`, `[1000, 5000)`, and `[5000, 10000)`. Documents that do not fall into these ranges are grouped into a default bucket.

```javascript
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

```javascript
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
