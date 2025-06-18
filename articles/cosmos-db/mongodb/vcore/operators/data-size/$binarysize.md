--- 
  title: $binarySize (data size operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $binarySize operator is used to return the size of a binary data field. 
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/27/2024
---

# $binarySize (data size operator)

The `$binarySize` operator is used to return the size of a binary data field. This can be useful when dealing with binary data stored, such as images, files, or any other binary content. The argument for `$binarySize` should be a string, or a binary value.

## Syntax

The syntax for using the `$binarySize` operator is as follows:

```json
{
  $binarySize: "<field>"
}
```

### Parameters

| | Description |
| --- | --- |
| **`<field>`**| The field for which you want to get the binary size.|

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

To project the size of a binary field


```JavaScript
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

This query would return the following document.

```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "name": "Lakeshore Retail | DJ Equipment Stop - Port Cecile",
    "dataSize": 50
  },
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "name": "VanArsdel, Ltd. | Musical Instrument Outlet - East Cassie",
    "dataSize": 57
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "name": "Northwind Traders | Bed and Bath Place - West Oraland",
    "dataSize": 53
  }
]
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]