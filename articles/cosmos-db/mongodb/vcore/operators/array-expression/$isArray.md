---
  title: $isArray (Array Expression Operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: Learn the syntax and see examples of how to use $isArray (Array Expression) operator.
  author: sandeep-nair
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: how-to
  ms.date: 09/02/2024
---

# $isArray (Array Expression Operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$isArray` operator is used to determine if a specified value is an array. It returns `true` if the value is an array and `false` otherwise. This operator is often used in aggregation pipelines to filter or transform documents based on whether a field contains an array.

## Syntax

The syntax for the `$isArray` operator is as follows:

```javascript
{ $isArray: <expression> }
```

## Parameters

| | Description |
| --- | --- |
| **`<expression>`**| Any valid expression that resolves to a value you want to check.|


Let's understand the usage with the following sample json.
```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lenore's New DJ Equipment Store",
  "location": {
    "lat": -9.9399
  },
  "staff": {
    "totalStaff": {
      "fullTime": 14,
      "partTime": 18,
      "temporary": 3,
      "parTime": 0
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
    "#FashionStore",
    "#SeasonalSale",
    "#FreeShipping",
    "#MembershipDeals"
  ]
}
```

Here are some examples demonstrating the usage of the `$isArray` operator.

### Example 1: Checking if a field is an array.

To check if the `salesByCategory` field in the `sales` subdocument is an array across all documents.

```javascript
db.stores.aggregate([
  {
    $project: {
      _id: 1,
      isSalesByCategoryArray: { $isArray: "$sales.salesByCategory" }
    }
  },
 // Limit the result to the first 3 documents
  { $limit: 3 } 
])
```
This query would return the following document.

```json
[
{
  "_id": "66d7cc1674d12223cc1b5a41",
  "isSalesByCategoryArray": false
},
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "isSalesByCategoryArray": true
},
{
  "_id": "66d7cc1674d12223cc1b5a41",
  "isSalesByCategoryArray": false
}
]
```



### Example 2: Filtering documents based on array fields.

We can also use `$isArray` to filter documents where the `promotionEvents` field is an array.

```javascript
db.stores.aggregate([
  {
    $match: {
      $expr: { $isArray: "$promotionEvents" }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 },
   // Include only _id and name fields in the output 
  { $project: { _id: 1, name: 1 } }    
])
```

This query would return the following document.

```json
[
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "name": "Lenore's New DJ Equipment Store"
},
{
  "_id": "fe239ccd-15e2-4d53-9d5b-ffc95a36fbe1",
  "name": "Serena's Musical Instruments"
},
{
  "_id": "3db06cf7-a6a0-4cc0-bb6b-a7e44896a6b3",
  "name": "Monserrat's Books"
}
]

```
## Related Content
[!INCLUDE[Related content](../includes/related-content.md)]