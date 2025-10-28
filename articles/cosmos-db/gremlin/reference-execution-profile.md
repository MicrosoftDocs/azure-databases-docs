---
title: Execution Profile Reference
description: Review the possible properties and values returned by an execution profile invocation in Azure Cosmos DB for Apache Gremlin.
ms.topic: reference
ms.date: 07/23/2025
ai-usage: ai-assisted
---

# Azure Cosmos DB for Apache Gremlin execution profile reference

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

This article provides a reference for the execution profile feature in Azure Cosmos DB for Apache Gremlin. It explains the structure and properties of the response returned by the `executionProfile()` function.

## Response

The response of an `executionProfile()` function invocation yields a hierarchy of JSON objects with the following structure.

### Gremlin operation

This object represents the entire Gremlin operation that was executed. This object is named `gremlin`. This object contains the following properties:

| | Description |
| --- | --- |
| **`gremlin`** | The explicit Gremlin statement that was executed. |
| **`totalTime`** | The time, in milliseconds, that the execution of the step incurred in. |
| **`metrics`** | An array that contains each of the Cosmos DB runtime operators that were executed to fulfill the query. This list is sorted in order of execution. |

### Azure Cosmos DB for Apache Gremlin runtime operators

This list represents each of the components of the entire Gremlin operation. The list is named `metrcis`. This list is sorted in order of execution. Each object contains the following properties:

| | Description |
| --- | --- |
| **`name`** | Name of the operator. This property is the type of step that was evaluated and executed. |
| **`time`** | Amount of time, in milliseconds, that a given operator took. |
| **`annotations`** | Contains additional information, specific to the operator that was executed. |
| **`annotations.percentTime`** | Percentage of the total time that it took to execute the specific operator. |
| **`counts`** | Number of objects that were returned from the storage layer by this operator. This count is contained in the `counts.resultCount` scalar value within. |
| **`storeOps`** | Represents a storage operation that can span one or multiple partitions. |
| **`storeOps.fanoutFactor`** | Represents the number of partitions that this specific storage operation accessed. |
| **`storeOps.count`** | Represents the number of results that this storage operation returned. |
| **`storeOps.size`** | Represents the size in bytes of the result of a given storage operation. |

### Example response

Here's an example response in JSON format:

```json
[
  {
    "gremlin": "g.V().hasLabel('tweet').out().executionProfile()",
    "totalTime": 42,
    "metrics": [
      {
        "name": "GetVertices",
        "time": 31,
        "annotations": { "percentTime": 73.81 },
        "counts": { "resultCount": 30 },
        "storeOps": [ { "fanoutFactor": 1, "count": 13, "size": 6819, "time": 1.02 } ]
      },
      {
        "name": "GetEdges",
        "time": 6,
        "annotations": { "percentTime": 14.29 },
        "counts": { "resultCount": 18 },
        "storeOps": [ { "fanoutFactor": 1, "count": 20, "size": 7950, "time": 1.98 } ]
      },
      {
        "name": "GetNeighborVertices",
        "time": 5,
        "annotations": { "percentTime": 11.9 },
        "counts": { "resultCount": 20 },
        "storeOps": [ { "fanoutFactor": 1, "count": 4, "size": 1070, "time": 1.19 } ]
      },
      {
        "name": "ProjectOperator",
        "time": 0,
        "annotations": { "percentTime": 0 },
        "counts": { "resultCount": 20 }
      }
    ]
  }
]
```

### Response schema

The response also matches this JSON schema:

```json
[
  {
    "type": "object",
    "properties": {
      "gremlin": { "type": "string" },
      "totalTime": { "type": "number" },
      "metrics": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "time": { "type": "number" },
            "annotations": {
              "type": "object",
              "properties": {
                "percentTime": { "type": "number" }
              },
              "additionalProperties": true
            },
            "counts": {
              "type": "object",
              "properties": {
                "resultCount": { "type": "number" }
              },
              "additionalProperties": true
            },
            "storeOps": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "fanoutFactor": { "type": "number" },
                  "count": { "type": "number" },
                  "size": { "type": "number" },
                  "time": { "type": "number" }
                },
                "additionalProperties": true
              }
            }
          },
          "additionalProperties": true
        }
      }
    },
    "required": ["gremlin", "totalTime", "metrics"],
    "additionalProperties": true
  }
]
```

## Operators

| | Description |
| --- | --- |
| **`GetVertices`** | This step obtains a predicated set of objects from the persistence layer. |
| **`GetEdges`** | This step obtains the edges that are near a set of vertices. This step can result in one or many storage operations. |
| **`GetNeighborVertices`** | This step obtains the vertices that are connected to a set of edges. The edges contain the partition keys and unique identifiers of both their source and target vertices. |
| **`Coalesce`** | This step accounts for the evaluation of two operations whenever the `coalesce()` Gremlin step is executed. |
| **`CartesianProductOperator`** | This step computes a cartesian product between two datasets. Executed whenever the predicates `to()` or `from()` are used. |
| **`ConstantSourceOperator`** | This step computes an expression to produce a constant value as a result. |
| **`ProjectOperator`** | This step prepares and serializes a response using the result of preceding operations. |
| **`ProjectAggregation`** | This step prepares and serializes a response for an aggregate operation. |
