---
  title: $pullAll
  titleSuffix: Overview of the $pullAll operation in Azure Cosmos DB for MongoDB (vCore)
  description: The $pullAll operator is used to remove all instances of the specified values from an array.  
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/11/2024
---

# $pullAll


The `$pullAll` operator is used to remove all instances of the specified values from an array. This operator is useful when you need to clean up arrays by removing multiple specific elements in a single operation.

Both `$pull` and `$pullAll` are used to remove elements from an array, but they differ in how they identify the elements to be removed. `$pull` removes all elements from an array that match a specific condition, which can be a simple value or a more complex query (like matching sub-document fields). On the other hand, `$pullAll` removes specific values provided as an array of exact matches, but it doesn't support conditions or queries. Essentially, `$pull` is more flexible as it allows conditional removal based on various criteria, while `$pullAll` is simpler, working only with a fixed set of values.

## Syntax

The syntax for the `$pullAll` operator is as follows:

```javascript
{
  $pullAll: { <field1>: [ <value1>, <value2>, ... ], ... }
}
```
## Parameters

| Parameter | Description |
| --- | --- |
| **`<field1>`**| The field where the specified values will be removed.|
| **`[ <value1>, <value2>, ... ]`**| An array of values to be removed from the specified field.|

## Examples

Consider this sample document from the stores collection.

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
### Example 1: Remove multiple elements from an array

To remove the discounts for "#MembershipDeals" and "#SeasonalSale" from the 'tag' array.

```javascript
db.stores.updateMany(
    //filter
    { "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5"},
    {
      $pullAll: {
        "tag": ["#MembershipDeals","#SeasonalSale" ]
      }
    }
)
```
This query would return the following document.

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": 1,
  "modifiedCount": 1,
  "upsertedCount": 0
}

```
## Related content
[!INCLUDE[Related content](../includes/related-content.md)]