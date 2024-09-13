---
  title: $objectToArray (array expression operator) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $objectToArray operator is used to convert a document into an array of key-value pairs.
  author: sandeep-nair
  ms.author: sandnair
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: reference
  ms.date: 09/02/2024
---

# $objectToArray (as Array Expression Operator)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$objectToArray` operator is used to convert a document (that is, an object) into an array of key-value pairs. This operator can be useful when you need to manipulate or analyze the structure of a document in a more flexible array format.

## Syntax

The syntax for the `$objectToArray` operator is as follows:

```javascript
{
  $objectToArray: <object>
}
```
## Parameters

| | Description |
| --- | --- |
| **`<object>`**| The document (or object) that you want to convert into an array of key-value pairs.|


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

Here are some examples of how to use the `$objectToArray` operator with the provided sample JSON.

### Example 1: Converting a geospatial field to an array.

The following aggregation pipeline converts the `location` field of the `store` document into an array of key-value pairs.

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

This query would return the following document.

```json
[
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "locationArray": [
    {
      "k": "lat",
      "v": -9.9399
    }
  ]
},
{
  "_id": "66d7cc1674d12223cc1b5a41",
  "locationArray": null
},
{
  "_id": "fe239ccd-15e2-4d53-9d5b-ffc95a36fbe1",
  "locationArray": [
    {
      "k": "lat",
      "v": -6.3542
    },
    {
      "k": "lon",
      "v": 21.6768
    }
  ]
}
]

```

### Example 2: Converting a sub document to an array.

This example converts the `totalStaff` field of the `staff` document into an array of key-value pairs.

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

This query would return the following document.

```json
[
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "staffArray": [
    {
      "k": "fullTime",
      "v": 14
    },
    {
      "k": "partTime",
      "v": 18
    },
    {
      "k": "temporary",
      "v": 3
    },
    {
      "k": "parTime",
      "v": 0
    }
  ]
},
{
  "_id": "66d7cc1674d12223cc1b5a41",
  "staffArray": null
},
{
  "_id": "fe239ccd-15e2-4d53-9d5b-ffc95a36fbe1",
  "staffArray": [
    {
      "k": "fullTime",
      "v": 8
    },
    {
      "k": "partTime",
      "v": 8
    }
  ]
}
]

```

### Example 3: Converting datetime field to an array.

This pipeline converts the `promotionalDates` field for each promotion event into an array of key-value pairs.

```javascript
db.stores.aggregate([
    {
      $project: {
        promotionEvents: {
          $map: {
            input: "$promotionEvents",
            as: "event",
            in: {
              eventName: "$$event.eventName",
              promotionalDatesArray: { $objectToArray: "$$event.promotionalDates" }
            }
          }
        }
      }
    },
    // Limit the result to the first document
    { $limit: 1 }
])
```

This query would return the following document.

```json
{
  "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
  "promotionEvents": [
    {
      "eventName": "Bargain Blitz Days",
      "promotionalDatesArray": [
        {
          "k": "startDate",
          "v": {
            "Year": 2024,
            "Month": 3,
            "Day": 11
          }
        },
        {
          "k": "endDate",
          "v": {
            "Year": 2024,
            "Month": 2,
            "Day": 18
          }
        }
      ]
    },
    {
      "eventName": "Discount Delight Days",
      "promotionalDatesArray": [
        {
          "k": "startDate",
          "v": {
            "Year": 2024,
            "Month": 5,
            "Day": 11
          }
        },
        {
          "k": "endDate",
          "v": {
            "Year": 2024,
            "Month": 5,
            "Day": 18
          }
        }
      ]
    },
    {
      "eventName": "Grand Savings",
      "promotionalDatesArray": [
        {
          "k": "startDate",
          "v": "2024-08-01"
        },
        {
          "k": "endDate",
          "v": "2024-08-31"
        }
      ]
    },
    {
      "eventName": "Big Bargain",
      "promotionalDatesArray": [
        {
          "k": "startDate",
          "v": "2024-11-25"
        },
        {
          "k": "endDate",
          "v": "2024-11-30"
        }
      ]
    }
  ]
}
```

## Related content
[!INCLUDE[Related content](../includes/related-content.md)]