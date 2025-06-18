---
  title: $slice (array update) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $slice is used to limit the number of elements in an array that are returned in a query.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 10/14/2024
---

# $slice (array update)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$slice` operator is used to limit the number of elements in an array that are returned in a query. It can be useful when dealing with large arrays where only a subset of the elements is needed. This operator can be applied to arrays to either return the first N elements, the last N elements, or a specific range of elements.

## Syntax

The general syntax for the `$slice` operator is as follows:

```json
{
  "$push": {
    "<field>": {
      "$each": [ "<value1>", "<value2>" ],
      "$slice": <num>
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`field`**| The array field to which the `$slice` operator is applied.|
| **`<value1>, <value2>`**| The values to be inserted into the array. We can keep an empty array for slicing through existing values in array field.|
| **`<num>`**| A value of zero clears the array, a negative value retains that many elements from the end of the array, and a positive value retains that many elements from the beginning of the array.|

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
      "eventName": "Discount Delight Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 5, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 5, "Day": 18 }
      }
    },
    {
      "eventName": "New Promotion Event",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 7, "Day": 1 },
        "endDate": { "Year": 2024, "Month": 7, "Day": 7 }
        },
        "discounts": [
          { "categoryName": "DJ Lights", "discountPercentage": 20 }
        ]
    },
    {
        "eventName": "Cyber Monday Event",
        "promotionalDates": {
          "startDate": { "Year": 2024, "Month": 8, "Day": 1 },
          "endDate": { "Year": 2024, "Month": 8, "Day": 7 }
        },
        "discounts": [ { "categoryName": "DJ Speakers", "discountPercentage": 25 } ]
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

### Example 1: Slice for the first N or last N elements from an array field

The example uses `$push` with `$each` to add new elements to the `promotionEvents` array and `$slice` to retain only the first N (positive slice) or last N (negative slice) elements. This way ensures the array keeps the most recent entries after the update.

```javascript
db.stores.updateOne(
  { _id: '7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5' },
  {
    $push: {
      promotionEvents: {
        $each: [
          {
            eventName: "Black Friday Event",
            promotionalDates: {
              startDate: { Year: 2024, Month: 8, Day: 1 },
              endDate: { Year: 2024, Month: 8, Day: 7 }
            },
            discounts: [
              { categoryName: 'DJ Speakers', discountPercentage: 25 }
            ]
          },
          {
            eventName: "Mega Discount Days",
            promotionalDates: {
              startDate: { Year: 2024, Month: 5, Day: 11 },
              endDate: { Year: 2024, Month: 5, Day: 18 }
            },
            discounts: [
              { categoryName: "DJ Lights", discountPercentage: 20 }
            ]
          }
        ],
        $slice: -3
      }
    }
  }
)
```

The query adds `Black Friday Event` and `Mega Discount Days` event to the `promotionEvents` array and slices for the last 3 elements within the array.

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
      "discounts": [
        { "categoryName": "DJ Speakers", "discountPercentage": 25 }
      ]
    },
    {
      "eventName": "Black Friday Event",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 8, "Day": 1 },
        "endDate": { "Year": 2024, "Month": 8, "Day": 7 }
      },
      "discounts": [
        { "categoryName": "DJ Speakers", "discountPercentage": 25 }
      ]
    },
    {
      "eventName": "Mega Discount Days",
      "promotionalDates": {
        "startDate": { "Year": 2024, "Month": 5, "Day": 11 },
        "endDate": { "Year": 2024, "Month": 5, "Day": 18 }
      },
      "discounts": [
        { "categoryName": "DJ Lights", "discountPercentage": 20 }
      ]
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

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
