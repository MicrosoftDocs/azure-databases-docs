---
  title: $lookup (aggregation pipeline stage) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $lookup stage in the Aggregation Framework is used to perform left outer joins with other collections.
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/11/2024
---

# $lookup (as Aggregation Pipeline Stage)
[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$lookup` stage in the Aggregation Framework is used to perform left outer joins with other collections. It allows you to combine documents from different collections based on a specified condition. This operator is useful for enriching documents with related data from other collections without having to perform multiple queries.

## Syntax

The syntax for the `$lookup` stage is as follows:

```javascript
{
  $lookup: {
    from: <collection to join>,
    localField: <field from input documents>,
    foreignField: <field from the documents of the "from" collection>,
    as: <output array field>
  }
}
```

## Parameters

| | Description |
| --- | --- |
| **`from`** | The name of the collection to join with.|
| **`localField`** | The field from the input documents that are matched with the `foreignField`.|
| **`foreignField`** | The field from the documents in the `from` collection that are matched with the `localField`.|
| **`as`** | The name of the new array field to add to the input documents. This array contains the matched documents from the `from` collection.|

## Example

Let's say we have a `ratings` collection with two documents.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "rating": 5
}
{
  "_id": "36375751-060e-46ad-974a-c834d1aeb6e1",
  "rating": 3
}
```

Let's understand the usage with the following sample json in stores collection.
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

We want to join the `ratings` collection with the `stores` collection to list promotion events related to each store having a 5 rating.


```javascript
db.ratings.aggregate([
  // filter based on rating in ratings collection
  {
    $match: {
      "rating": 5
    }
  },
  // find related documents in stores collection
  {
    $lookup: {
      from: "stores",
      localField: "_id",
      foreignField: "_id",
      as: "storeEvents"
    }
  },
  // deconstruct array to output a document for each element of the array
  {
    $unwind: "$storeEvents"
  },
   // Include only _id and name fields in the output 
  { $project: { _id: 1, "storeEvents.name": 1 } }  

])
```

This query would return the following document.

```json

{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "storeEvents": {
    "name": "Lenore's New DJ Equipment Store"
  }
}


```


## Limitations

- let isn't supported as part of pipeline

## Related Content
[!INCLUDE[Related content](../includes/related-content.md)]