---
  title: $position (array update) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $position is used to specify the position in the array where a new element should be inserted.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 10/14/2024
---

# $position (array update)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$position` operator is used to specify the position in the array where a new element should be inserted. This operator is useful when you need to insert an element at a specific index in an array rather than appending it to the end.

## Syntax

The basic syntax for using the `$position` operator in an update command is as follows:

```json
{
  "$push": {
    "<arrayField>": {
      "$each": ["<value1>", "<value2>"],
      "$position": <index>
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<arrayField>`**| The field in the document that contains the array to be updated.|
| **`<value1>, <value2>, ...`**| The values to be inserted into the array.|
| **`<index>`**| The position at which the values should be inserted.|

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

### Example 1: Insert an element at specific index location in an array field

The example inserts the tag `#NewArrival` at the second position (index 1) in the `tag` array of a specific document.

```javascript
db.stores.update(
  { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
  { $push: { "tag": { $each: ["#NewArrival"], $position: 1 } } }
)
```

The example document updated `tag` field has following values.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "tag": [
    "#ShopLocal",
    "#NewArrival",
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
