---
  title: $range
  titleSuffix: Overview of the $range operator in Azure Cosmos DB for MongoDB (vCore)
  description: The $range operator allows generating an array of sequential integers.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 07/28/2025
---

# $range

The `$range` operator is used to generate an array of sequential integers. The operator helps create number arrays in a range, useful for pagination, indexing, or test data.

## Syntax

```javascript
{
    $range: [ <start>, <end>, <step> ]
}
```

## Parameters

| Parameter | Description |
| --- | --- |
| **`start`** | The starting value of the range (inclusive). |
| **`end`** | The ending value of the range (exclusive). |
| **`step`** | The increment value between each number in the range (optional, defaults to 1). |

## Examples

### Example 1: Generate a range of numbers

The example demonstrates usage of operator to generate an array of integers from 0 to 5, wherein it includes the left boundary while excludes the right.

```javascript
db.stores.aggregate([
  { $match: { "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"} }
, {
    $project: {
      rangeArray: { $range: [0, 5] }
    }
  }
])
```

This query returns the following result.

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "rangeArray": [
            0,
            1,
            2,
            3,
            4
        ]
    }
]
```

### Example 2: Generate a range of numbers with a step value

The example demonstrates usage of operator to generate an array of even numbers from 0 to 18.

```javascript
db.stores.aggregate([
  { $match: { "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6"} }
, {
    $project: {
      evenNumbers: { $range: [0, 8, 2] }
    }
  }
])
```

The query results the following result.

```json
[
    {
        "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
        "rangeArray": [
            0,
            2,
            4,
            6
        ]
    }
]
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)].
