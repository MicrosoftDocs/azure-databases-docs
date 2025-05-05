---
title: $[] (positional-all update) usage in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $[] operator is used to update all elements in an array that match the query condition.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 10/14/2024
---

# $[] (as Array Update Operator)
The $[] operator in Azure Cosmos DB for MongoDB vCore is used to update all elements in an array that match a specified condition. This operator allows you to perform updates on multiple elements in an array without specifying their positions. It is particularly useful when you need to apply the same update to all items in an array.

## Syntax
The syntax for using the $[] array update operator is as follows:

```javascript
db.collection.update(
   <query>,
   {
     $set: {
       "<arrayField>.$[]": <value>
     }
   }
)
```

## Parameters

| Parameter      | Description                                                  |
|----------------|--------------------------------------------------------------|
| `<query>`      | The selection criteria for the documents to update.          |
| `<arrayField>` | The field containing the array to update.                    |
| `<value>`      | The value to set for each matching element in the array.     |


## Example(s)
### Example 1: Updating Discount Percentages
Suppose you want to update the discount percentage for all categories in the "Summer Sale" promotion event. You can use the $[] operator to achieve this:

```javascript
db.stores.update(
  { "store.storeId": "12345", "store.promotionEvents.eventName": "Summer Sale" },
  {
    $set: {
      "store.promotionEvents.$[event].discounts.$[].discountPercentage": 5
    }
  },
  {
    arrayFilters: [{ "event.eventName": "Summer Sale" }]
  }
)
```

### Example 2: Updating Sales by Category
If you want to increase the total sales for all categories by 10%, you can use the $[] operator as follows:

```javascript
db.stores.update(
  { "store.storeId": "12345" },
  {
    $mul: {
      "store.sales.salesByCategory.$[].totalSales": 1.10
    }
  }
)
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
