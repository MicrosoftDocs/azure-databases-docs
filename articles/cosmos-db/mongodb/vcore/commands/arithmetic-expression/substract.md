--- 
title: $subtract (as arithmetic expression operator) usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: Subtracts two numbers and returns the result.
author: khelanmodi
ms.author: khelanmodi
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 09/27/2024
---

# $subtract (as arithmetic expression operator)

The `$subtract` operator in MongoDB is used to subtract two numbers and return the result. This operator is useful in various scenarios such as calculating differences between dates, times, or numerical values in a document.

## Syntax

```json
{ $subtract: [ <expression1>, <expression2> ] }
```

## Parameters

| | Description |
| --- | --- |
| **`<expression1>`** | The minuend (the number from which another number is to be subtracted). |
| **`<expression2>`** | The subtrahend (the number to be subtracted). |

## Example(s)

### Example 1: Subtracting Total Sales from Full Sales

The following example demonstrates how to subtract the `fullSales` value from the `totalSales` value in the `salesByCategory` array.

```json
db.collection.aggregate([
  {
    $project: {
      category: "$sales.salesByCategory.categoryName",
      salesDifference: { $subtract: ["$sales.salesByCategory.totalSales", "$sales.fullSales"] }
    }
  }
])
```

### Example 2: Calculating the Duration of a Promotional Event

The following example calculates the duration of a promotional event in days by subtracting the `startDate` from the `endDate`.

```json
db.collection.aggregate([
  {
    $project: {
      eventName: "$promotionEvents.eventName",
      eventDuration: {
        $subtract: [
          { $dateFromParts: { year: "$promotionEvents.promotionalDates.endDate.Year", month: "$promotionEvents.promotionalDates.endDate.Month", day: "$promotionEvents.promotionalDates.endDate.Day" } },
          { $dateFromParts: { year: "$promotionEvents.promotionalDates.startDate.Year", month: "$promotionEvents.promotionalDates.startDate.Month", day: "$promotionEvents.promotionalDates.startDate.Day" } }
        ]
      }
    }
  }
])
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](migration-options.md).
- Get started by [creating an account](../quickstart-portal.md).