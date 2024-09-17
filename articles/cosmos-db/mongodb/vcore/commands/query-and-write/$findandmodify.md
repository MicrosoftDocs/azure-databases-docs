---
  title: findAndModify command usage in Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The findAndModify command is used to atomically modify and return a single document.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/12/2024
---

# findAndModify

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `findAndModify` command is used to atomically modify and return a single document. This command is particularly useful for operations that require reading and updating a document in a single step, ensuring data consistency. Common use cases include implementing counters, queues, and other atomic operations.

## Syntax

The syntax for the `findAndModify` command is as follows:

```javascript
db.collection.findAndModify({
   query: <document>,
   sort: <document>,
   remove: <boolean>,
   update: <document>,
   new: <boolean>,
   fields: <document>,
   upsert: <boolean>
})
```

### Parameters

- **query**: The selection criteria for the document to modify.
- **sort**: Determines which document to modify if the query selects multiple documents.
- **remove**: If `true`, removes the selected document.
- **update**: The modifications to apply.
- **new**: If `true`, returns the modified document rather than the original.
- **fields**: Limits the fields to return for the matching document.
- **upsert**: If `true`, creates a new document if no document matches the query.

## Examples

### Example 1: Update total sales

Suppose we want to update the total sales for the store with `storeId` "e5767a9f-cd95-439c-9ec4-7ddc13d22926" to `550000.00` and return the updated document.

```javascript
db.stores.findAndModify({
   query: { "_id": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" },
   update: { $set: { "sales.totalSales": 550000.00 } },
   new: true
})
```

#### Sample output

```javascript
```

### Example 2: Add a New Promotional Event

Let's add a new promotional event called "Back to School" to the store with `storeId` "e5767a9f-cd95-439c-9ec4-7ddc13d22926" and return the updated document.

```javascript
db.stores.findAndModify({
   query: { "store.storeId": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" },
   update: { $push: { "promotionEvents": {
       "eventName": "Electronics For All Days",
       "promotionalDates": {
         "startDate": "2024-09-01",
         "endDate": "2024-09-31"
       },
       "discounts": [
         {
           "categoryName": "Laptops",
           "discountPercentage": 10
         },
         {
           "categoryName": "Smartphones",
           "discountPercentage": 5
         }
       ]
   }}},
   new: true
})
```

#### Sample output

```javascript
```

### Example 3: Remove a promotional event

Suppose we want to remove the "Summer Sale" promotional event from the store with `storeId` "12345" and return the original document.

```javascript
db.stores.findAndModify({
   query: { "store.storeId": "e5767a9f-cd95-439c-9ec4-7ddc13d22926" },
   update: { $pull: { "promotionEvents": { "eventName": "Electronics For All Days" } } },
   new: false
})
```

#### Sample output

```javascript
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
