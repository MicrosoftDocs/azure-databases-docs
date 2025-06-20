---
  title: $push (array update) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $push operator is used to append a specified value to an array within a document. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/11/2024
---

# $push (array update)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$push` operator is used to append a specified value to an array within a document. This operator is useful when you need to add new elements to an existing array field without affecting the other elements in the array. It can be used in various scenarios such as adding new sales categories, promotional events, or staff members to a store's document.

## Syntax

The basic syntax of the `$push` operator is as follows:

```javascript
db.collection.update(
   { <query> },
   { $push: { <field>: <value> } },
   { <options> }
)
```

## Parameters
| | Description |
| --- | --- |
| **`<query>`**| The selection criteria for the documents to update.|
| **`<field>`**| The array field to which the value will be appended.|
| **`<value>`**| The value to append to the array field.|
| **`<options>`**| Optional. Additional options for the update operation.|

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

To add a new sales category "DJ Cables" with total sales of 1000.00 to the `salesByCategory` array.

```javascript
db.stores.update(
   { _id: "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5" },
   { $push: { "sales.salesByCategory": { "categoryName": "DJ Cables", "totalSales": 1000.00 } } }
)
```
This query would return the following document.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": "1",
  "modifiedCount": "1",
  "upsertedCount": 0
}
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]
