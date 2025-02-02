---
title: $unset (as Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $unset stage in the aggregation pipeline is used to remove specified fields from documents.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# $unset (as Aggregation Pipeline Stage)
The $unset stage the aggregation pipeline is used to remove specified fields from documents. This can be particularly useful when you need to exclude certain fields from the results of an aggregation query for reasons such as privacy, reducing payload size, or simply cleaning up the output.

## Syntax
The syntax for the $unset stage is straightforward. It accepts a single argument which can be a field name or an array of field names to be removed from the documents.

```json
{
  $unset: "<field1>" | ["<field1>", "<field2>", ...]
}
```

Parameters
field1, field2, ... : The names of the fields to remove from the documents.

## Example(s)
Here are a few examples demonstrating how to use the $unset stage in an aggregation pipeline.

### Example 1: Remove a Single Field
Suppose you want to remove the location field from the documents.

```json
db.stores.aggregate([
  {
    $unset: "store.location"
  }
])
```

### Example 2: Remove Multiple Fields
Suppose you want to remove the location and sales.totalSales fields from the documents.

```json
db.stores.aggregate([
  {
    $unset: ["store.location", "store.sales.totalSales"]
  }
])
```

### Example 3: Remove Nested Fields
Suppose you want to remove the staff.totalStaff.fullTime and promotionEvents.discounts fields from the documents.

```json
db.stores.aggregate([
  {
    $unset: ["store.staff.totalStaff.fullTime", "store.promotionEvents.discounts"]
  }
])
```

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).