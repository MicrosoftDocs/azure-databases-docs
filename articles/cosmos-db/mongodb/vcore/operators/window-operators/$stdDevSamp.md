---
  title: $stdDevSamp (as Window operators) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Calculates the sample standard deviation of numeric values in a window.
  author: gahl-levy
  ms.author: gahllevy
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 06/23/2025
---

# $stdDevSamp (as Window operators) usage on Azure Cosmos DB for MongoDB vCore

The `$stdDevSamp` operator calculates the sample standard deviation of numeric values for documents in a defined window. This is useful for statistical analysis, enabling you to understand the variability of data within a specific subset of documents.

## Syntax

```javascript
{
  $stdDevSamp: <expression>
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`<expression>`** | An expression that resolves to numeric values. Non-numeric values are ignored. |

## Example(s)

### Example 1: Calculate the sample standard deviation of sales across documents

The following aggregation pipeline calculates the sample standard deviation of the `totalSales` field for sales categories using a window function:

```javascript
db.sales.aggregate([
  {
    $setWindowFields: {
      partitionBy: "$categoryName",
      sortBy: { totalSales: 1 },
      output: {
        salesStdDev: {
          $stdDevSamp: "$totalSales",
          window: {
            documents: ["unbounded", "current"]
          }
        }
      }
    }
  }
])
```

### Example 2: Calculate the sample standard deviation of discount percentages

This example calculates the sample standard deviation of `discountPercentage` across promotional events:

```javascript
db.promotionEvents.aggregate([
  {
    $unwind: "$discounts"
  },
  {
    $setWindowFields: {
      partitionBy: "$eventName",
      sortBy: { "discounts.discountPercentage": 1 },
      output: {
        discountStdDev: {
          $stdDevSamp: "$discounts.discountPercentage",
          window: {
            documents: ["unbounded", "current"]
          }
        }
      }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]