---
title: $out usage on Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The `$out` stage in an aggregation pipeline writes the resulting documents to a specified collection.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 06/23/2025
---

# $out usage on Azure Cosmos DB for MongoDB vCore

The `$out` stage in an aggregation pipeline allows you to write the resulting documents of the pipeline into a specified collection. It is commonly used to save the output of complex aggregation operations for further use or analysis. When used, the specified collection is either created or replaced with the new documents.

## Syntax

```javascript
{
  $out: "<outputCollection>"
}
```

## Parameters  

| Parameter | Description |
| --- | --- |
| **`<outputCollection>`** | The name of the collection where the aggregation result will be stored. |

## Example(s)

### Example 1: Writing Aggregation Results to a New Collection

The following aggregation pipeline writes the documents with total sales greater than 30,000 into a new collection called `highSales`.

```javascript
db.sales.aggregate([
  {
    $match: {
      "sales.salesByCategory.totalSales": { $gt: 30000 }
    }
  },
  {
    $out: "highSales"
  }
]);
```

### Example 2: Writing Processed Data to Another Collection

The below example extracts promotion events and writes them into a collection named `promotionEventsSummary`.

```javascript
db.promotionEvents.aggregate([
  {
    $project: {
      eventName: 1,
      promotionalDates: 1,
      "discounts.categoryName": 1,
      "discounts.discountPercentage": 1
    }
  },
  {
    $out: "promotionEventsSummary"
  }
]);
```


## Related content
[!INCLUDE[Related content](../includes/related-content.md)]