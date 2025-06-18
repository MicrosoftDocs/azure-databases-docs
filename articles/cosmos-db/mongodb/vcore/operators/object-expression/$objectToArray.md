---
  title: $objectToArray object expression in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The objectToArray command is used to transform a document (object) into an array of key-value pairs.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 11/01/2024
---

# $objectToArray as object expression operator

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$objectToArray` operator is used to transform a document (object) into an array of key-value pairs. Each key-value pair in the resulting array is represented as a document with `k` and `v` fields. This operator is useful when you need to manipulate or analyze the structure of documents within your collections.

## Syntax

```json
{ $objectToArray: <object> }
```

- `<object>`: The document (object) to be transformed into an array of key-value pairs.

## Examples

Given a sample JSON document representing a store, we can use the `$objectToArray` operator to transform various parts of this document.

### Example 1: Transforming the `location` object

The following aggregation pipeline transforms the `location` object into an array of key-value pairs.

```json
db.stores.aggregate([
  {
    $project: {
      locationArray: { $objectToArray: "$store.location" }
    }
  }
])
```

### Example 2: Transforming the `staff.totalStaff` object

This example demonstrates how to transform the `staff.totalStaff` object into an array of key-value pairs.

```json
db.stores.aggregate([
  {
    $project: {
      totalStaffArray: { $objectToArray: "$store.staff.totalStaff" }
    }
  }
])
```

### Example 3: Transforming the `salesByCategory` array

If you want to transform the `salesByCategory` array, you would first need to unwind the array and then apply the `$objectToArray` operator.

```json
db.stores.aggregate([
  { $unwind: "$store.sales.salesByCategory" },
  {
    $project: {
      salesByCategoryArray: { $objectToArray: "$store.sales.salesByCategory" }
    }
  }
])
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]