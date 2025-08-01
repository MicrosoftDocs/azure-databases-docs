---
  title: $sort (array update) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $sort is used to sort an array in ascending or descending order within a document during an update operation.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 10/14/2024
---

# $sort (array update)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$sort` operator is used to sort an array in ascending or descending order within a document during an update operation. This operator is useful for maintaining ordered arrays based on specific fields.

## Syntax

```json
{
  "$sort": {
    "<field1>": <sortOrder>,
    "<field2>": <sortOrder>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`**| The field in the array to sort by.|
| **`sortOrder`**| The sort order (1 for ascending, -1 for descending).|

## Example

Let's review the usage with a sample json document from `stores` collection.

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
      "eventName": "Cyber Monday Event",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 8, "Day": 1 },
        "endDate": { "Year": 2024, "Month": 8, "Day": 7 }
      },
      "discounts": [ { "categoryName": "DJ Speakers", "discountPercentage": 25 } ]
    },
    {
      "eventName": "Black friday Event",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 8, "Day": 1 },
        "endDate": { "Year": 2024, "Month": 8, "Day": 7 }
      },
      "discounts": [ { "categoryName": "DJ Speakers", "discountPercentage": 25 } ]
    },
    {
      "eventName": "Mega Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 5, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 5, "Day": 18 }
      },
      "discounts": [ { "categoryName": "DJ Lights", "discountPercentage": 20 } ]
    }
  ],
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

### Example 1: Sorting an array of objects

The example sorts the `salesByCategory` array in place based on the `totalSales` field in ascending order.

```javascript
db.stores.update( { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" }
                , { $push: { "sales.salesByCategory": { $each: [], $sort: { "totalSales": 1 } } } }
)
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
