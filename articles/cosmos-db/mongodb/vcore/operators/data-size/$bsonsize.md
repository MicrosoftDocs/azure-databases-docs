--- 
  title: $bsonSize
  titleSuffix: Overview of the $bsonSize operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $bsonSize operator is used to return the size of a document in bytes when encoded as BSON. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $bsonSize

The `$bsonSize` operator is used to return the size of a document in bytes when encoded as BSON. It's useful for understanding the storage requirements of documents within your collections. The operator can be used within aggregation pipelines to calculate the size of documents and is helpful for optimizing storage and understanding performance implications.

## Syntax

```javascript
{ $bsonSize: <expression> }
```

### Parameters

| Parameter | Description |
| --- | --- |
| **`<expression>`**| Any valid expression that resolves to a document whose BSON size you want to calculate.|

## Example

Let's understand the usage with sample json from `stores` dataset.

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

### Example 1: Calculate the total BSON-encoded size of a document in bytes using $bsonSize

To calculate the BSON size of the document, adding it as a new field called `bsonSize`,

```JavaScript
db.stores.aggregate([
  {
    $project: {
      _id: 1,              
      name: 1,         
      documentSize: { 
        $bsonSize: "$$ROOT"    //pass the whole document
      }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 }  
])
```

This query  would return the following document.

```json
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "documentSize": 2226
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "documentSize": 1365
  },
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "documentSize": 1882
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
