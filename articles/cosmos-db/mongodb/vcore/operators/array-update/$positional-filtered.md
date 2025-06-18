---
title: $[identifier] usage in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $[] operator is used to update all elements using a specific identifer in an array that match the query condition.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 10/14/2024
---

# $[identifier] (as Array Update Operator)
The $[identifier] array update operator in Azure Cosmos DB for MongoDB vCore is used to update specific elements in an array that match a given condition. This operator is particularly useful when you need to update multiple elements within an array based on certain criteria. It allows for more granular updates within documents, making it a powerful tool for managing complex data structures.

## javascript
```json
{
  "<update operator>": {
    "<array field>.$[<identifier>]": <value>
  }
},
{
  "arrayFilters": [
    { "<identifier>.<field>": <condition> }
  ]
}
```

## Parameters

| Parameter           | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `<update operator>` | The update operator to be applied (e.g., `$set`, `$inc`, etc.).             |
| `<array field>`     | The field containing the array to be updated.                               |
| `<identifier>`      | A placeholder used in `arrayFilters` to match specific elements in the array.|
| `<value>`           | The value to be set or updated.                                             |
| `arrayFilters`      | An array of filter conditions to identify which elements to update.         |
| `<field>`           | The specific field within array elements to be checked.                     |
| `<condition>`       | The condition that array elements must meet to be updated.                  |


## Example(s)

### Example 1: Updating Discount Percentage for a Specific Category
Suppose you want to update the discount percentage for the "Laptops" category in the "Holiday Specials" promotion event.

```javascript
db.collection.update(
  { "store.storeId": "12345", "store.promotionEvents.eventName": "Holiday Specials" },
  {
    $set: {
      "store.promotionEvents.$[event].discounts.$[discount].discountPercentage": 18
    }
  },
  {
    arrayFilters: [
      { "event.eventName": "Holiday Specials" },
      { "discount.categoryName": "Laptops" }
    ]
  }
)
```

### Example 2: Increasing Total Sales by Category
Suppose you want to increase the total sales for the "Smartphones" category by $10,000.

```javascript
db.collection.update(
  { "store.storeId": "12345" },
  {
    $inc: {
      "store.sales.salesByCategory.$[category].totalSales": 10000
    }
  },
  {
    arrayFilters: [
      { "category.categoryName": "Smartphones" }
    ]
  }
)
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
