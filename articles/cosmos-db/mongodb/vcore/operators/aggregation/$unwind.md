---
title: $unwind (Aggregation Pipeline Stage)
titleSuffix: Azure Cosmos DB for MongoDB vCore
description: The $unwind stage in the aggregation framework is used to deconstruct an array field from the input documents to output a document for each element.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: language-reference
ms.date: 08/27/2024
---

# $unwind (Aggregation Pipeline Stage)
The $unwind stage in the aggregation framework is used to deconstruct an array field from the input documents to output a document for each element. Each output document is a copy of the original but with the value of the array field replaced by a single element. This is particularly useful for normalizing data stored in arrays and for performing operations on each element of an array separately.

## Syntax
```json
{
  $unwind: {
    path: <field path>,
    includeArrayIndex: <string>, // Optional
    preserveNullAndEmptyArrays: <boolean> // Optional
  }
}
```
## Parameters

| | Description |
| --- | --- |
| **`path`** | The field path to an array field. This is a required parameter. |
| **`includeArrayIndex`** | Optional. The name of a new field to hold the array index of the unwound element. |
| **`preserveNullAndEmptyArrays`** | Optional. If true, if the path is null, missing, or an empty array, `$unwind` outputs the document unchanged. |

## Example(s)
### Example 1: Unwind Sales by Category
To deconstruct the salesByCategory array in the store document:

```json
db.stores.aggregate([
  {
    $unwind: "$store.sales.salesByCategory"
  }
])
```
Sample output 
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "sales": {
        "totalSales": 15000,
        "salesByCategory": {
          "category": "Electronics",
          "totalSales": 5000
        }
      }
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "sales": {
        "totalSales": 15000,
        "salesByCategory": {
          "category": "Clothing",
          "totalSales": 10000
        }
      }
    }
  }
]
```

This will output documents where each document represents a single category's sales information.

### Example 2: Unwind Promotion Events with Array Index
To deconstruct the promotionEvents array and include the array index in the output:

```json
db.stores.aggregate([
  {
    $unwind: {
      path: "$store.promotionEvents",
      includeArrayIndex: "eventIndex"
    }
  }
])
```
Sample output
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Summer Sale",
        "eventDate": ISODate("2024-08-01T00:00:00Z")
      },
      "eventIndex": 0
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Black Friday",
        "eventDate": ISODate("2024-11-25T00:00:00Z")
      },
      "eventIndex": 1
    }
  }
]
```


This will output documents where each document represents a single promotion event, and the eventIndex field will contain the original index of the event in the array.

### Example 3: Unwind Discounts within Promotion Events
To deconstruct the discounts array within each promotion event and preserve documents with no discounts:
```json
db.stores.aggregate([
  {
    $unwind: {
      path: "$store.promotionEvents.discounts",
      preserveNullAndEmptyArrays: true
    }
  }
])
```
Sample output
```json
[
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Summer Sale",
        "discounts": {
          "discountType": "Percentage",
          "discountAmount": 20
        }
      }
    }
  },
  {
    "_id": "7954bd5c-9ac2-4c10-bb7a-2b79bd0963c5",
    "store": {
      "name": "Downtown Store",
      "promotionEvents": {
        "eventName": "Black Friday"
      }
    }
  }
]
```

This will output documents where each document represents a single discount within a promotion event, and documents with no discounts will be preserved.

## Related content

- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](../../migration-options.md)
- Get started by [creating an account](../../quickstart-portal.md).