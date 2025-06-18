---
  title: $arrayToObject (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $arrayToObject allows converting an array into a single document.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 10/14/2024
---

# $arrayToObject (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$arrayToObject` operator is used to convert an array into a single document. This operator is useful when you need to transform arrays of key-value pairs into a more structured document format.

## Syntax

The syntax for the `$arrayToObject` operator is as follows:

```json
{ $arrayToObject: <array> }
```

## Parameters

| | Description |
| --- | --- |
| **`<array>`**| The array to be converted into a document. Each element in the array must be either: a) A two-element array where the first element is the field name and the second element is the field value. b) A document with exactly two fields, "k" and "v", where "k" is the field name and "v" is the field value.|

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

### Example 1: Convert the array to a key: value document

The example aggregation query converts the `salesByCategory` array into an object where each `categoryName` is a key and `totalSales` is the corresponding value. This transformation simplifies access to sales data by category directly from an object structure.

```javascript
db.stores.aggregate([
  { $match: { _id: '7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5' } },
  { $project: { "sales.salesByCategory": { $arrayToObject: { $map: { input: "$sales.salesByCategory", as: "item", in: { k: "$$item.categoryName", v: "$$item.totalSales" } } } } } }
])
```

The query returns the converted `salesByCategory` array as a document.

```json
{
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "sales": { "salesByCategory": { "DJ Headphones": 35921, "DJ Cables": 1000 } }
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
