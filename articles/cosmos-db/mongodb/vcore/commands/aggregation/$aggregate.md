---
  title: Aggregate command usage in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The aggregate command is used to process data records and return computed results.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# Aggregate

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `aggregate` command is used to process data records and return computed results. It performs operations on the data, such as filtering, grouping, and sorting, and can transform the data in various ways. The `aggregate` command is highly versatile and is commonly used for data analysis and reporting.

## Syntax

```shell
db.collection.aggregate(pipeline, options)
```

- **pipeline**: An array of aggregation stages that process and transform the data.
- **options**: Optional. Specifies additional options for the aggregation, such as `explain`, `allowDiskUse`, and `cursor`.

## Examples

### Example 1: Calculate total sales by category

This example demonstrates how to calculate the total sales for each category in the `stores` collection.

```javascript
db.stores.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  },
  {
    $group: {
      _id: "$sales.salesByCategory.categoryName",
      totalSales: { $sum: "$sales.salesByCategory.totalSales" }
    }
  }
])
```

### Example 2: Find stores with full-time staff greater than 10

This example shows how to filter stores where the number of full-time staff is greater than 10.

```javascript
db.stores.aggregate([
  {
    $match: {
      "staff.totalStaff.fullTime": { $gt: 10 }
    }
  }
])
```

### Example 3: List all promotion events with discounts greater than 15%

This example lists all promotion events where any discount is greater than 15%.

```javascript
db.stores.aggregate([
  {
    $unwind: "$promotionEvents"
  },
  {
    $unwind: "$promotionEvents.discounts"
  },
  {
    $match: {
      "promotionEvents.discounts.discountPercentage": { $gt: 15 }
    }
  },
  {
    $group: {
      _id: "$promotionEvents.eventName",
      discounts: { $push: "$promotionEvents.discounts" }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
