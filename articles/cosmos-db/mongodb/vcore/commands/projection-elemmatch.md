---
title: Operator - $elemMatch (projection)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $elemMatch operator is used to project the first element in an array that matches the specified query condition. 
author: avijitkgupta
ms.author: avijitgupta
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: reference
ms.date: 08/27/2024
---

# Operator: `$elemMatch` (projection)

The `$elemMatch` projection operator in Azure Cosmos DB for MongoDB vCore is used to project the first element in an array that matches the specified query condition. This operator is useful when you want to retrieve only the matching elements from an array within a document, rather than the entire array.

## Syntax

```json
db.collection.find({},
    {
      "field": { "$elemMatch": { <query> } }
    }
)
```

## Parameters

| | Description |
| --- | --- |
| **`field`** | The field containing the array from which you want to project the matching element. |
| **`query`** | The condition that the elements in the array need to match. |

## Examples

Here are a few examples of this operator in use.

These examples assume the following JSON data set.

```json
{
  "_id": "34f462fe-5085-4a77-a3de-53f4117466bd",
  "name": "Darius's Holiday Supplies",
  "location": {
    "lat": -63.5435,
    "lon": 77.7226
  },
  "staff": {
    "totalStaff": {
      "fullTime": 16,
      "partTime": 16
    }
  },
  "sales": {
    "totalSales": 41481,
    "salesByCategory": [
      {
        "categoryName": 'Holiday Tableware',
        "totalSales": 41481
      }
    ]
  },
  "promotionEvents":[
    {
      "eventName": "Incredible Savings Showcase",
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 5,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 5,
          "Day": 20
        }
      },
      "discounts": [
        {
          "categoryName": "Ribbons",
          "discountPercentage": 15
        },
        {
          "categoryName": "Gift Bags",
          "discountPercentage": 25
        }
      ]
    }
  ]
}
```

### Projecting a matching element from an array

Suppose you have a collection named `stores` with documents similar to the provided sample JSON. To project the `promotionEvents` array where the `eventName` is `"Incredible Savings Showcase"`, you can use the following query:

```javascript
db.stores.find(
  {"_id": '34f462fe-5085-4a77-a3de-53f4117466bd'},
  { "promotionEvents": { "$elemMatch": { "eventName": "Incredible Savings Showcase" } } }
);
```

This query returns the document with only the `promotionEvents` array element that matches the `eventName` `"Incredible Savings Showcase"`.

```json
{
  "_id": "34f462fe-5085-4a77-a3de-53f4117466bd",
  "promotionEvents": [
    {
      "eventName": 'Incredible Savings Showcase',
      "promotionalDates": {
        "startDate": {
          "Year": 2024,
          "Month": 5,
          "Day": 11
        },
        "endDate": {
          "Year": 2024,
          "Month": 5,
          "Day": 20
        }
      },
      "discounts": [
        {
          "categoryName": "Ribbons",
          "discountPercentage": 15
        },
        {
          "categoryName": "Gift Bags",
          "discountPercentage": 25
        }
      ]
    }
  ]
}
```

## Limitations

- `$elemMatch` doesn't support text query expression.

## Related content

- [`$elemMatch` (array query)](array-query-elemmatch.md)
