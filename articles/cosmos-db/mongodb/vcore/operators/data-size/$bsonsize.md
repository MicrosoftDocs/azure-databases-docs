--- 
  title: $bsonSize (data size operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $bsonSize operator is used to return the size of a document in bytes when encoded as BSON. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/27/2024
---

# $bsonSize (data size operator)

The `$bsonSize` operator is used to return the size of a document in bytes when encoded as BSON. This is useful for understanding the storage requirements of documents within your MongoDB collections. The operator can be used within aggregation pipelines to calculate the size of documents and is helpful for optimizing storage and understanding performance implications.

## Syntax

```mongodb
{ $bsonSize: <expression> }
```

### Parameters

| | Description |
| --- | --- |
| **`<expression>`**| Any valid expression that resolves to a document whose BSON size you want to calculate.|

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
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "documentSize": 957
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "documentSize": 1046
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "documentSize": 5656
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]