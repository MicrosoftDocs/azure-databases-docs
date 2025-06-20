---
  title: $filter (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $filter operator filters for elements from an array based on a specified condition.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 10/14/2024
---

# $filter (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$filter` operator is used to filter elements from an array based on a specified condition. This operator is useful when you need to manipulate or retrieve specific array elements within documents.

## Syntax

The basic syntax of the `$filter` operator is as follows:

```json
{
  "$filter": {
    "input": "<array>",
    "as": "<string>",
    "cond": "<expression>"
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`input`**| An expression that resolves to an array.|
| **`as`**| A string that specifies the variable name for each element in the input array.|
| **`cond`**| An expression that determines whether to include the element in the output array.|

## Example

Let's understand the usage with sample json from `stores` dataset.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": { "lat": 60.1441, "lon": -141.5012 },
  "staff": { "totalStaff": { "fullTime": 2, "partTime": 0 } },
  "sales": {
    "salesByCategory": [
      { "categoryName": "DJ Headphones", "totalSales": 35921 },
      { "categoryName": "DJ Cables", "totalSales": 1000 }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 3, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 2, "Day": 18 }
      },
      "discounts": [
        { "categoryName": "DJ Turntables", "discountPercentage": 18 },
        { "categoryName": "DJ Mixers", "discountPercentage": 15 }
      ]
    },
    {
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 5, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 5, "Day": 18 }
      }
    }
  ],
  "tag": [
    "#ShopLocal",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

### Example 1: Retrieve an element filtered on condition

The following example demonstrates how to filter sales category based on `totalSales`.

```javascript
db.yourCollection.aggregate([
  { $match: { _id: '7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5' } },
  { $project: { filteredSalesByCategory: { $filter: { input: "$sales.salesByCategory", as: "item", cond: { $gt: ["$$item.totalSales", 10000] } } } } }
])
```

The resulting document has an extra field, `filteredSalesByCategory`, which include the items from `salesByCategory` that have `totalSales` greater than 10000.

```json
{
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "filteredSalesByCategory": [ { "categoryName": "DJ Headphones", "totalSales": 35921 } ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
