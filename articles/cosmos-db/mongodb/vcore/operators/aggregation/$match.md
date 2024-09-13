---
  title: $match (aggregation pipeline stage) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $match stage in the aggregation pipeline is used to filter documents that match a specified condition.
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/11/2024
---

# $match (as Aggregation Pipeline Stage)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$match` stage in the aggregation pipeline is used to filter documents that match a specified condition. It's similar to the `find` operation but is used within the aggregation pipeline to narrow down the documents that pass through to the next stage. This stage is highly useful for optimizing performance by reducing the number of documents that need to be processed in subsequent stages.

## Syntax

The basic syntax for the `$match` stage is as follows:

```javascript
{
  $match: {
    <query>
  }
}
```

| | Description |
| --- | --- |
| **`<query>`**| A standard MongoDB query document that specifies the conditions that the documents must meet.|

## Examples

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

### Example 1: Match documents using string comparison

To filter documents where the `_id` is "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5":

```javascript
db.stores.aggregate([
    {
      $match: {
        "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"
      }
    }
])
```
This query would return the sample document.


### Example 2: Match documents  using numeric comparison

To filter documents where the total sales are greater than $35,000:

```javascript
db.stores.aggregate([
    {
      $match: {
        "sales.totalSales": { $gt: 35000 }
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
{
   "_id":"3db06cf7-a6a0-4cc0-bb6b-a7e44896a6b3",
   "name":"Monserrat's Books"
}{
   "_id":"36375751-060e-46ad-974a-c834d1aeb6e1",
   "name":"Marlen's Kitchen Appliances"
}{
   "_id":"55925ade-5b78-46a1-99ba-e20ff154dac4",
   "name":"Una's Party Goods"
}

```

### Example 3: Match documents within sub documents

To filter documents where there's a discount of 15% on DJ Mixers:

```javascript
db.stores.aggregate([
    {
      $match: {
        "promotionEvents.discounts": {
          $elemMatch: {
            "categoryName": "DJ Mixers",
            "discountPercentage": 15
          }
        }
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
  "_id": "4748bb29-99ba-4232-85c8-e3ac2084fa60",
  "name": "Adaline's DJ Equipment Boutique"
},
{
  "_id": "fd1c4f7f-e3af-41fb-9c78-9c7472e1b885",
  "name": "Clemmie's DJ Equipment Hub"
}
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]