--- 
  title: $binarySize
  titleSuffix: Overview of the $binarySize operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $binarySize operator is used to return the size of a binary data field. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $binarySize

The `$binarySize` operator is used to return the size of a binary data field. This can be useful when dealing with binary data stored, such as images, files, or any other binary content. The argument for `$binarySize` should be a string, or a binary value.

## Syntax

```javascript
{
  $binarySize: "<field>"
}
```

### Parameters

| Parameter | Description |
| --- | --- |
| **`<field>`**| The field for which you want to get the binary size.|

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

### Example 1: Calculate the size of a string or binary data in bytes using $binarySize

The aggregation pipeline calculates the binary size of the name field for each document in the stores collection.

```javascript
db.stores.aggregate([
  {
    $project: {
      name: 1,          
      dataSize: {
        $binarySize: "$name" // Calculate the binary size of the string data
      }
    }
  },
  // Limit the result to the first 3 documents
  { $limit: 3 }  
])
```

The query results help us with understanding storage impact or when optimizing field sizes.

```json
  {
    "_id": "7e53ca0f-6e24-4177-966c-fe62a11e9af5",
    "name": "Contoso, Ltd. | Office Supply Deals - South Shana",
    "dataSize": 49
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "name": "Lakeshore Retail | Home Decor Hub - Franciscoton",
    "dataSize": 48
  },
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "name": "Lakeshore Retail | Holiday Supply Hub - Marvinfort",
    "dataSize": 50
  }
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
