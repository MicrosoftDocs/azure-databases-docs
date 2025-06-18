---
  title: $range (array expression) usage on Azure Cosmos DB for MongoDB vCore
  titleSuffix: Azure Cosmos DB for MongoDB vCore
  description: The $range operator allows generating an array of sequential integers.
  author: avijitgupta
  ms.author: avijitgupta
  ms.service: azure-cosmos-db
  ms.subservice: mongodb-vcore
  ms.topic: language-reference
  ms.date: 09/16/2024
---

# $range (array expression)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

The `$range` operator is used to generate an array of sequential integers. This operator is particularly useful for creating arrays of numbers within a specific range, which can then be used for various purposes such as pagination, indexing, or generating test data.

## Syntax

The syntax for the `$range` operator is:

```javascript
$range: [ <start>, <end>, <step> ]
```

## Parameters

| | Description |
| --- | --- |
| **`start`** | The starting value of the range (inclusive). |
| **`end`** | The ending value of the range (exclusive). |
| **`step`** | The increment value between each number in the range (optional, defaults to 1). |

## Examples

Here are some examples demonstrating the use of the `$range` operator.

### Example 1: Generate a range of numbers

To generate an array of integers from 0 to 9:

```javascript
db.stores.aggregate([
  { $match: { "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"} }
, {
    $project: {
      rangeArray: { $range: [0, 5] }
    }
  }
])
```

The query results in generating an array of sequential numbers.

```json
{
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "rangeArray": [ 0, 1, 2, 3, 4 ]
}
```

### Example 2: Generate a range of numbers with a step value

To generate an array of even numbers from 0 to 18:

```javascript
db.stores.aggregate([
  { $match: { "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60"} }
, {
    $project: {
      evenNumbers: { $range: [0, 8, 2] }
    }
  }
])
```

The query results in generating an array of even numbers, stepping by 2.

```json
{
    "_id": "988d2dd1-2faa-4072-b420-b91b95cbfd60",
    "rangeArray": [ 0, 2, 4, 6 ]
}
```

## Related content

[!INCLUDE[Related content](../includes/related-content.md)].
