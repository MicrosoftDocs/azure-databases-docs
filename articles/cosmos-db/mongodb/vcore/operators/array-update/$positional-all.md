---
title: $[] usage in Azure Cosmos DB for MongoDB vCore
titleSuffix: Overview of the $[] positional operator in Azure Cosmos DB for MongoDB (vCore)
description: The $[] operator is used to update all elements in an array that match the query condition.
author: avijitgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 10/14/2024
---

# $[]
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

| Parameter | Description |
| --- | --- |
| **`<query>`** | The selection criteria for the documents to update. |
| **`<arrayField>`** | The field containing the array to update. |
| **`<value>`** | The value to set for each matching element in the array. |


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


### Example 1: Updating Discount Percentages

To update to all elements in the discounts array inside each promotion event:

```javascript
db.stores.updateOne(
  { _id: "905d1939-e03a-413e-a9c4-221f74055aac" },
  {
    $inc: {
      "promotionEvents.$[].discounts.$[].discountPercentage": 5
    }
  }
)

```

### Example 2: Updating Sales by Category

To increase the total sales for all categories by 10%, use the $[] operator as follows:

```javascript
db.stores.update(
  { _id: "905d1939-e03a-413e-a9c4-221f74055aac" },
  {
    $mul: {
      "sales.salesByCategory.$[].totalSales": 1.10
    }
  }
)
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
