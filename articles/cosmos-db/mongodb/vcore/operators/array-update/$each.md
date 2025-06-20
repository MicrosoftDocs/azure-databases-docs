---
  title: $each (array update) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $each operator is used within an `$addToSet` or `$push` operation to add multiple elements to an array field in a single update operation. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/11/2024
---
# $each (array update)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$each` operator is used within an `$addToSet` or `$push` operation to add multiple elements to an array field in a single update operation. This operator is useful when you need to insert multiple items into an array without having to perform multiple update operations. The `$each` operator ensures that each item in the specified array is added to the target array.

## Syntax

```javascript
{
  $push: {
    <field>: {
      $each: [ <value1>, <value2>, ... ],
      <modifier1>: <value1>,
      <modifier2>: <value2>,
      ...
    }
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`<field>`**| The field to be updated.|
| **`$each`**| An array of values to be added to the array field.|
| **`<modifier>`**| Optional modifiers like `$sort`, `$slice`, and `$position` to control the behavior of the `$push` operation.|

## Example

Let's understand the usage with the following sample json.
```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
   "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
  "location": {
    "lat": 60.1441,
    "lon": -141.5012
  },
  "staff": {
    "totalStaff": {
      "fullTime": 2,
      "partTime": 0
    }
  },
  "sales": {
    "salesByCategory": [
      {
        "categoryName": "DJ Headphones",
        "totalSales": 35921
      }
    ],
    "fullSales": 3700
  },
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 3,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 2,
          "Day": 18
        }
      },
      "discounts": [
        {
          "categoryName": "DJ Turntables",
          "discountPercentage": 18
        },
        {
          "categoryName": "DJ Mixers",
          "discountPercentage": 15
        }
      ]
    }
  ],
  "tag": [
    "#ShopLocal",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

To add multiple new promotion events to the `promotionEvents` array.

```javascript
db.stores.updateOne(
  { "name": "Lenore's New DJ Equipment Store" },
  {
    $push: {
      promotionEvents: {
        $each: [
          {
            eventName: "Grand Savings",
            promotionalDates: {
              startDate: "2024-08-01",
              endDate: "2024-08-31"
            },
            discounts: [             
              {
                categoryName: "DJ Headphones",
                discountPercentage: 5
              }
            ]
          },
          {
            eventName: "Big Bargain",
            promotionalDates: {
              startDate: "2024-11-25",
              endDate: "2024-11-30"
            },
            discounts: [
              {
                categoryName: "DJ Headphones",
                discountPercentage: 20
              }
            ]
          }
        ]
      }
    }
  }
)
```


This query would return the following document.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "0",
  "modifiedCount": "0",
  "upsertedCount": 0
}
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]