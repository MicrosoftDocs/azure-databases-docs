---
title: $eq
titleSuffix: Overview of the $eq operator
description: The $eq query operator compares the value of a field to a specified value
author: abinav2307
ms.author: abramees
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 02/24/2025
---

# $eq

The `$eq` operator is used to match documents where the value of a field is equal to a specified value. The $eq operator filters documents based on exact matches on query predicates to retrieve documents with specific values, objects and arrays.

## Syntax

```javascript
{
    field: {
        $eq: <value>
    }
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`field`** | The field to be compared|
| **`value`** | The value to compare against|

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
  ],
  "company": "Lakeshore Retail",
  "city": "Port Cecile",
  "lastUpdated": {
    "$date": "2024-12-11T10:21:58.274Z"
  }
}
```

### Example 1: Use $eq filter on a root level field

To find a store with the name "Boulder Innovations | Home Security Place - Ankundingburgh", run a query with the $eq predicate to match on the name field and project only the ID and name fields in the result.

```javascript
db.stores.find({
    "name": {
        "$eq": "Boulder Innovations | Home Security Place - Ankundingburgh"
    }
}, {
    "name": 1
})
```

This query returns the following result:

```json
{
    "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
    "name": "Boulder Innovations | Home Security Place - Ankundingburgh"
}
```

### Example 2: Use $eq filter on a nested field

To find a store with a total sales of exactly $37,015, run a query using the $eq operator using the dot notation on the nested field sales.totalSales field.

```javascript
db.stores.find({
    "sales.totalSales": {
        "$eq": 37015
    }
}, {
    "name": 1,
    "sales.totalSales": 1
})
```

This returns the following results:
```json
{
    "_id": "bda56164-954d-4f47-a230-ecf64b317b43",
    "name": "Boulder Innovations | Home Security Place - Ankundingburgh",
    "sales": { "totalSales": 37015 }
}
```

### Example 3: Use $eq for individual items in an array

The following query retrieves documents using equality predicates on individual items within the nested promotionEvents.discounts array. 

This query searches for an equality match on any one of the objects within the nested discounts array

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        "$eq": {
            "categoryName": "Alarm Systems",
            "discountPercentage": 5
        }
    }
}, {
    "name": 1
}, {
    "limit": 2
})
```

This query returns the following results:
```json
[
  {
    "_id": "ece5bf6c-3255-477e-bf2c-d577c82d6995",
    "name": "Proseware, Inc. | Home Security Boutique - Schambergertown"
  },
  {
    "_id": "7baa8fd8-113a-4b10-a7b9-2c116e976491",
    "name": "Tailwind Traders | Home Security Pantry - Port Casper"
  }
]
```

### Example 4: Use $eq to match the entire array

This query searches for documents based on exact match on ALL the values within the promotionEvents.discounts array.

```javascript
db.stores.find({
    "promotionEvents.discounts": {
        "$eq": [{
            "categoryName": "Alarm Systems",
            "discountPercentage": 5
        }, {
            "categoryName": "Door Locks",
            "discountPercentage": 12
        }]
    }
}, {
    "name": 1
})
```

This returns the following results:

```json
[
{
    "_id": "aa9ad64c-29da-42f8-a1f0-30e03bf04a2d",
    "name": "Boulder Innovations | Home Security Market - East Sheridanborough"
}
]
```

> [!NOTE]
> For an equality match on an entire array, the order of the specified values in the equality predicates must also be an exact match.

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
