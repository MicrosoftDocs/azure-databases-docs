---
title: $count (as Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $count stage in the aggregation pipeline is used to count the number of documents that pass through the pipeline.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $count (as Aggregation Pipeline Stage)
The $count stage in the aggregation pipeline is used to count the number of documents that pass through the pipeline. This stage outputs a document with a single field containing the count of the documents. It is particularly useful when you need to determine the number of documents that match certain criteria or have passed through various stages of transformation in the pipeline.

## Syntax
The syntax for the $count stage is straightforward. It takes a single argument, which is the name of the field that will hold the count of documents.

```json
{
  $count: <field>
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The name of the field in the output document where the count will be stored. |

## Example(s)
### Example 1: Counting Total Documents
To count the total number of documents in a collection:

```json
db.store.aggregate([
  {
    $count: "totalDocuments"
  }
])
```

### Example 2: Counting Documents After Filtering
To count the number of promotional events that offer a discount on laptops:

```json
db.store.aggregate([
  {
    $unwind: "$promotionEvents"
  },
  {
    $unwind: "$promotionEvents.discounts"
  },
  {
    $match: {
      "promotionEvents.discounts.categoryName": "Laptops"
    }
  },
  {
    $count: "laptopDiscountEvents"
  }
])
```

### Example 3: Counting Documents in Nested Arrays
To count the total number of sales categories:

```json
db.store.aggregate([
  {
    $unwind: "$sales.salesByCategory"
  },
  {
    $count: "totalSalesCategories"
  }
])
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).