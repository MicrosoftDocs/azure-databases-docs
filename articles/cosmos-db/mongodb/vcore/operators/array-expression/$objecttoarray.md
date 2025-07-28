---
  title: $objectToArray
  titleSuffix: Overview of the $objectToArray operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $objectToArray operator is used to convert a document into an array of key-value pairs.
  author: sandeepsnairms
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $objectToArray

The `$objectToArray` operator is used to convert a document (that is, an object) into an array of key-value pairs. This operator can be useful when you need to manipulate or analyze the structure of a document in a more flexible array format.

## Syntax

```javascript
{
  $objectToArray: <object>
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<object>`**| The document (or object) that you want to convert into an array of key-value pairs.|

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

### Example 1: Converting a geospatial field to an array

The aggregation pipeline converts the `location` field of the `store` document into an array of key-value pairs.

```javascript
db.stores.aggregate([ 
    {
        $project: {
          locationArray: { $objectToArray: "$location" }
        }
    },
    // Limit the result to the first 3 documents
    { $limit: 3 }
])
```

The query returns three documents with location field converted to array.

```json
[
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "locationArray": [ { "k": "lat", "v": -85.0867 }, { "k": "lon", "v": -165.3524 } ]
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "locationArray": [ { "k": "lat", "v": -22.5751 }, { "k": "lon", "v": -12.4458 } ]
  },
  {
    "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
    "locationArray": [ { "k": "lat", "v": -41.287 }, { "k": "lon", "v": -76.0176 } ]
  }
]

```

### Example 2: Converting a sub document to an array

The example demonstrates the operator usage to convert `totalStaff` field of the `staff` document into an array of key-value pairs.

```javascript
db.stores.aggregate([
    {
      $project: {
        staffArray: { $objectToArray: "$staff.totalStaff" }
      }
    },
    // Limit the result to the first 3 documents
    { $limit: 3 }
])
```

The query returns three documents with staff attribute converted to array.

```json
[
  {
    "_id": "649626c9-eda1-46c0-a27f-dcee19d97f41",
    "staffArray": [ { "k": "fullTime", "v": 15 }, { "k": "partTime", "v": 9 } ]
  },
  {
    "_id": "8345de34-73ec-4a99-9cb6-a81f7b145c34",
    "staffArray": [ { "k": "fullTime", "v": 12 }, { "k": "partTime", "v": 14 } ]
  },
  {
    "_id": "57cc4095-77d9-4345-af20-f8ead9ef0197",
    "staffArray": [ { "k": "fullTime", "v": 4 }, { "k": "partTime", "v": 8 } ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
