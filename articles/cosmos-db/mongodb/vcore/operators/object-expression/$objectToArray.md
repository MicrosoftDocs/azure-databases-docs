---
  title: $objectToArray
  titleSuffix: Overview of the $objectToArray expression in Azure Cosmos DB for MongoDB (vCore)
  description: The objectToArray command is used to transform a document (object) into an array of key-value pairs.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 08/03/2025
---

# $objectToArray

The `$objectToArray` operator is used to transform a document (object) into an array of key-value pairs. Each key-value pair in the resulting array is represented as a document with `k` and `v` fields. This operator is useful when you need to manipulate or analyze the structure of documents within your collections.

## Syntax

```javascript
{ $objectToArray: <object> }
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`<object>`** | The document (object) to be transformed into an array of key-value pairs. |

## Examples

Given a sample JSON document representing a store, we can use the `$objectToArray` operator to transform various parts of this document.

### Example 1: Transforming the `location` object

The example aggregation pipeline transforms the `location` object into an array of key-value pairs.

```javascript
db.stores.aggregate([
  {
    $project: {
      locationArray: { $objectToArray: "$location" }
    }
  },
  {
    $limit: 2  // Limit output to first 5 documents
  }
])
```

The output represents the result of using the `$objectToArray` aggregation operator on the `location` field for each document.

```json
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "locationArray": [
      {
        "k": "lat",
        "v": -74.0427
      },
      {
        "k": "lon",
        "v": 160.8154
      }
    ]
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "locationArray": [
      {
        "k": "lat",
        "v": 61.3945
      },
      {
        "k": "lon",
        "v": -3.6196
      }
    ]
  }
```

### Example 2: Transforming the `salesByCategory` array

If you want to transform the `salesByCategory` array, you would first need to unwind the array and then apply the `$objectToArray` operator.

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $project: {
      salesByCategoryArray: { $objectToArray: "$sales.salesByCategory" }
    }
  },
  { 
    $limit: 2
  }
])
```

Converting subdocuments to key-value pairs is often used when you want to dynamically process field names, especially when:
    - Building generic pipelines.
    - Mapping field names into key-value structures for flexible transformations or further processing.

```json
[
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "salesByCategoryArray": [
      {
        "k": "categoryName",
        "v": "Stockings"
      },
      {
        "k": "totalSales",
        "v": 25731
      }
    ]
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "salesByCategoryArray": [
      {
        "k": "categoryName",
        "v": "Lamps"
      },
      {
        "k": "totalSales",
        "v": 19880
      }
    ]
  }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)]
