---
title: Query Graph Data
description: Perform common graph data queries and supplement those queries with the execution step using Azure Cosmos DB for Apache Gremlin.
ms.topic: how-to
ms.date: 07/22/2025
---

# Query Graph Data in Azure Cosmos DB for Apache Gremlin

The Azure Cosmos DB [API for Gremlin](overview.md) supports [Gremlin](https://tinkerpop.apache.org/gremlin.html) queries. This article provides sample documents and queries to get you started. A detailed Gremlin reference is provided in the [Gremlin support](support.md) article.

This article covers the following tasks: 

> [!div class="checklist"]
> * Querying data with Gremlin

## Prerequisites

For these queries to work, you must have an Azure Cosmos DB account and have graph data in the container. Don't have any of those? Complete the [5-minute quickstart](quickstart-dotnet.md) to create an account and populate your database. You can run the following queries using the [Gremlin console](https://tinkerpop.apache.org/docs/current/reference/#gremlin-console), or your favorite Gremlin driver.

## Count vertices in the graph

The following snippet shows how to count the number of vertices in the graph:

```
g.V().count()
```

## Filters

You can perform filters using Gremlin's `has` and `hasLabel` steps, and combine them using `and`, `or`, and `not` to build more complex filters. Azure Cosmos DB provides schema-agnostic indexing of all properties within your vertices and degrees for fast queries:

```
g.V().hasLabel('person').has('age', gt(40))
```

## Projection

You can project certain properties in the query results using the `values` step:

```
g.V().hasLabel('person').values('name')
```

## Find related edges and vertices

So far, we've only seen query operators that work in any database. Graphs are fast and efficient for traversal operations when you need to navigate to related edges and vertices. Let's find all friends of Thomas. We do this by using Gremlin's `outE` step to find all the out-edges from Thomas, then traversing to the in-vertices from those edges using Gremlin's `inV` step:

```cs
g.V('thomas').outE('knows').inV().hasLabel('person')
```

The next query performs two hops to find all of Thomas' "friends of friends", by calling `outE` and `inV` two times. 

```cs
g.V('thomas').outE('knows').inV().hasLabel('person').outE('knows').inV().hasLabel('person')
```

You can build more complex queries and implement powerful graph traversal logic using Gremlin, including mixing filter expressions, performing looping using the `loop` step, and implementing conditional navigation using the `choose` step. Learn more about what you can do with [Gremlin support](support.md)!

## Use execution profile

This article provides an overview of how to use the execution profile step for Azure Cosmos DB for Gremlin graph databases. This step provides relevant information for troubleshooting and query optimizations, and it's compatible with any Gremlin query that can be executed against a Cosmos DB Gremlin API account.

To use this step, simply append the `executionProfile()` function call at the end of your Gremlin query. **Your Gremlin query will be executed** and the result of the operation will return a JSON response object with the query execution profile.

For example:

```java
    // Basic traversal
    g.V('mary').out()

    // Basic traversal with execution profile call
    g.V('mary').out().executionProfile()
```

After calling the `executionProfile()` step, the response will be a JSON object that includes the executed Gremlin step, the total time it took, and an array of the Cosmos DB runtime operators that the statement resulted in.

> [!NOTE]
> This implementation for Execution Profile is not defined in the Apache Tinkerpop specification. It is specific to Azure Cosmos DB for Gremlin's implementation.


### Response Example

The following is an annotated example of the output that will be returned:

> [!NOTE]
> This example is annotated with comments that explain the general structure of the response. An actual executionProfile response won't contain any comments.

```json
[
  {
    // The Gremlin statement that was executed.
    "gremlin": "g.V('mary').out().executionProfile()",

    // Amount of time in milliseconds that the entire operation took.
    "totalTime": 28,

    // An array containing metrics for each of the steps that were executed. 
    // Each Gremlin step will translate to one or more of these steps.
    // This list is sorted in order of execution.
    "metrics": [
      {
        // This operation obtains a set of Vertex objects.
        // The metrics include: time, percentTime of total execution time, resultCount, 
        // fanoutFactor, count, size (in bytes) and time.
        "name": "GetVertices",
        "time": 24,
        "annotations": {
          "percentTime": 85.71
        },
        "counts": {
          "resultCount": 2
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 2,
            "size": 696,
            "time": 0.4
          }
        ]
      },
      {
        // This operation obtains a set of Edge objects. 
        // Depending on the query, these might be directly adjacent to a set of vertices, 
        // or separate, in the case of an E() query.
        //
        // The metrics include: time, percentTime of total execution time, resultCount, 
        // fanoutFactor, count, size (in bytes) and time.
        "name": "GetEdges",
        "time": 4,
        "annotations": {
          "percentTime": 14.29
        },
        "counts": {
          "resultCount": 1
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 1,
            "size": 419,
            "time": 0.67
          }
        ]
      },
      {
        // This operation obtains the vertices that a set of edges point at.
        // The metrics include: time, percentTime of total execution time and resultCount.
        "name": "GetNeighborVertices",
        "time": 0,
        "annotations": {
          "percentTime": 0
        },
        "counts": {
          "resultCount": 1
        }
      },
      {
        // This operation represents the serialization and preparation for a result from 
        // the preceding graph operations. The metrics include: time, percentTime of total 
        // execution time and resultCount.
        "name": "ProjectOperator",
        "time": 0,
        "annotations": {
          "percentTime": 0
        },
        "counts": {
          "resultCount": 1
        }
      }
    ]
  }
]
```

> [!NOTE]
> The executionProfile step executes the Gremlin query. This includes the `addV` or `addE`steps, which will result in the creation and will commit the changes specified in the query. As a result, the Request Units generated by the Gremlin query will also be charged.

### Execution profile response objects

The response of an executionProfile() function will yield a hierarchy of JSON objects with the following structure:
  - **Gremlin operation object**: Represents the entire Gremlin operation that was executed. Contains the following properties.
    - `gremlin`: The explicit Gremlin statement that was executed.
    - `totalTime`: The time, in milliseconds, that the execution of the step incurred in. 
    - `metrics`: An array that contains each of the Cosmos DB runtime operators that were executed to fulfill the query. This list is sorted in order of execution.
    
  - **Cosmos DB runtime operators**: Represents each of the components of the entire Gremlin operation. This list is sorted in order of execution. Each object contains the following properties:
    - `name`: Name of the operator. This is the type of step that was evaluated and executed. Read more in the table below.
    - `time`: Amount of time, in milliseconds, that a given operator took.
    - `annotations`: Contains additional information, specific to the operator that was executed.
    - `annotations.percentTime`: Percentage of the total time that it took to execute the specific operator.
    - `counts`: Number of objects that were returned from the storage layer by this operator. This is contained in the `counts.resultCount` scalar value within.
    - `storeOps`: Represents a storage operation that can span one or multiple partitions.
    - `storeOps.fanoutFactor`: Represents the number of partitions that this specific storage operation accessed.
    - `storeOps.count`: Represents the number of results that this storage operation returned.
    - `storeOps.size`: Represents the size in bytes of the result of a given storage operation.

Cosmos DB Gremlin Runtime Operator|Description
---|---
`GetVertices`| This step obtains a predicated set of objects from the persistence layer. 
`GetEdges`| This step obtains the edges that are near a set of vertices. This step can result in one or many storage operations.
`GetNeighborVertices`| This step obtains the vertices that are connected to a set of edges. The edges contain the partition keys and IDs of both their source and target vertices.
`Coalesce`| This step accounts for the evaluation of two operations whenever the `coalesce()` Gremlin step is executed.
`CartesianProductOperator`| This step computes a cartesian product between two datasets. Executed whenever the predicates `to()` or `from()` are used.
`ConstantSourceOperator`| This step computes an expression to produce a constant value as a result.
`ProjectOperator`| This step prepares and serializes a response using the result of preceding operations.
`ProjectAggregation`| This step prepares and serializes a response for an aggregate operation.

> [!NOTE]
> This list continues to be updated as new operators are added.

### Examples on how to analyze an execution profile response

The following are examples of common optimizations that can be spotted using the Execution Profile response:
  - Blind fan-out query.
  - Unfiltered query.

#### Blind fan-out query patterns

Assume the following execution profile response from a **partitioned graph**:

```json
[
  {
    "gremlin": "g.V('tt0093640').executionProfile()",
    "totalTime": 46,
    "metrics": [
      {
        "name": "GetVertices",
        "time": 46,
        "annotations": {
          "percentTime": 100
        },
        "counts": {
          "resultCount": 1
        },
        "storeOps": [
          {
            "fanoutFactor": 5,
            "count": 1,
            "size": 589,
            "time": 75.61
          }
        ]
      },
      {
        "name": "ProjectOperator",
        "time": 0,
        "annotations": {
          "percentTime": 0
        },
        "counts": {
          "resultCount": 1
        }
      }
    ]
  }
]
```

The following conclusions can be made from it:
- The query is a single ID lookup, since the Gremlin statement follows the pattern `g.V('id')`.
- Judging from the `time` metric, the latency of this query seems to be high since it's more than 10ms for a single point-read operation.
- If we look into the `storeOps` object, we can see that the `fanoutFactor` is `5`, which means that [5 partitions](../partitioning-overview.md) were accessed by this operation.

As a conclusion of this analysis, we can determine that the first query is accessing more partitions than necessary. This can be addressed by specifying the partitioning key in the query as a predicate. This leads to less latency and less cost per query. Learn more about [graph partitioning](partitioning.md). A more optimal query would be `g.V('tt0093640').has('partitionKey', 't1001')`.

#### Unfiltered query patterns

Compare the following two execution profile responses. For simplicity, these examples use a single partitioned graph.

This first query retrieves all vertices with the label `tweet` and then obtains their neighboring vertices:

```json
[
  {
    "gremlin": "g.V().hasLabel('tweet').out().executionProfile()",
    "totalTime": 42,
    "metrics": [
      {
        "name": "GetVertices",
        "time": 31,
        "annotations": {
          "percentTime": 73.81
        },
        "counts": {
          "resultCount": 30
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 13,
            "size": 6819,
            "time": 1.02
          }
        ]
      },
      {
        "name": "GetEdges",
        "time": 6,
        "annotations": {
          "percentTime": 14.29
        },
        "counts": {
          "resultCount": 18
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 20,
            "size": 7950,
            "time": 1.98
          }
        ]
      },
      {
        "name": "GetNeighborVertices",
        "time": 5,
        "annotations": {
          "percentTime": 11.9
        },
        "counts": {
          "resultCount": 20
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 4,
            "size": 1070,
            "time": 1.19
          }
        ]
      },
      {
        "name": "ProjectOperator",
        "time": 0,
        "annotations": {
          "percentTime": 0
        },
        "counts": {
          "resultCount": 20
        }
      }
    ]
  }
]
```

Notice the profile of the same query, but now with an extra filter, `has('lang', 'en')`, before exploring the adjacent vertices:

```json
[
  {
    "gremlin": "g.V().hasLabel('tweet').has('lang', 'en').out().executionProfile()",
    "totalTime": 14,
    "metrics": [
      {
        "name": "GetVertices",
        "time": 14,
        "annotations": {
          "percentTime": 58.33
        },
        "counts": {
          "resultCount": 11
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 11,
            "size": 4807,
            "time": 1.27
          }
        ]
      },
      {
        "name": "GetEdges",
        "time": 5,
        "annotations": {
          "percentTime": 20.83
        },
        "counts": {
          "resultCount": 18
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 18,
            "size": 7159,
            "time": 1.7
          }
        ]
      },
      {
        "name": "GetNeighborVertices",
        "time": 5,
        "annotations": {
          "percentTime": 20.83
        },
        "counts": {
          "resultCount": 18
        },
        "storeOps": [
          {
            "fanoutFactor": 1,
            "count": 4,
            "size": 1070,
            "time": 1.01
          }
        ]
      },
      {
        "name": "ProjectOperator",
        "time": 0,
        "annotations": {
          "percentTime": 0
        },
        "counts": {
          "resultCount": 18
        }
      }
    ]
  }
]
```

These two queries reached the same result, however, the first one requires more Request Units since it needed to iterate a larger initial dataset before querying the adjacent items. We can see indicators of this behavior when comparing the following parameters from both responses:
- The `metrics[0].time` value is higher in the first response, which indicates that this single step took longer to resolve.
- The `metrics[0].counts.resultsCount` value is higher as well in the first response, which indicates that the initial working dataset was larger.
