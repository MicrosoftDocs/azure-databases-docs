---
title: $[identifier] usage in Azure Cosmos DB for MongoDB vCore
titleSuffix: Overview of the $[identifier] positional operator in Azure Cosmos DB for MongoDB (vCore)
description: The $[] operator is used to update all elements using a specific identifer in an array that match the query condition.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 10/14/2024
---

# $[identifier]
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

| Parameter | Description |
| --- | --- |
| **`<update operator>`** | The update operator to be applied (e.g., `$set`, `$inc`, etc.). |
| **`<array field>`** | The field containing the array to be updated. |
| **`<identifier>`** | A placeholder used in `arrayFilters` to match specific elements in the array. |
| **`<value>`** | The value to be set or updated. |
| **`arrayFilters`** | An array of filter conditions to identify which elements to update. |
| **`<field>`** | The specific field within array elements to be checked. |
| **`<condition>`** | The condition that array elements must meet to be updated. |


## Examples

Consider this sample document from the stores collection.

```json
{
  "_id": "905d1939-e03a-413e-a9c4-221f74055aac",
  "name": "Trey Research | Home Office Depot - Lake Freeda",
  "location": { "lat": -48.9752, "lon": -141.6816 },
  "staff": { "employeeCount": { "fullTime": 12, "partTime": 19 } },
  "sales": {
    "salesByCategory": [ { "categoryName": "Desk Lamps", "totalSales": 37978 } ],
    "revenue": 37978
  },
  "promotionEvents": [
    {
      "eventName": "Crazy Deal Days",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 9, "Day": 27 },
        "endDate": { "Year": 2023, "Month": 10, "Day": 4 }
      },
      "discounts": [
        { "categoryName": "Desks", "discountPercentage": 22 },
        { "categoryName": "Filing Cabinets", "discountPercentage": 23 }
      ]
    },
    {
      "eventName": "Incredible Markdown Mania",
      "promotionalDates": {
        "startDate": { "Year": 2023, "Month": 12, "Day": 26 },
        "endDate": { "Year": 2024, "Month": 1, "Day": 2 }
      },
      "discounts": [
        { "categoryName": "Monitor Stands", "discountPercentage": 20 },
        { "categoryName": "Desks", "discountPercentage": 24 }
      ]
    }
  ]
}
```

### Example 1: Updating Discount Percentage for a Specific Category
To update the discount percentage for the "Laptops" category in the "Holiday Specials" promotion event.

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
To increase the total sales for the "Smartphones" category by $10,000.

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
