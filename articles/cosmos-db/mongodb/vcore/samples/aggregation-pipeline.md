---
title: |
  Tutorial: Aggregation Pipelines for Azure Cosmos DB MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: In this tutorial, we explore how to use aggregation pipelines in Azure Cosmos DB for MongoDB vCore. The guide covers the key stages of the aggregation pipeline, such as $match, $group, $sort, and $project, and demonstrates how to implement complex data transformations and queries. You will also learn how to optimize aggregation performance, reduce Request Unit (RU) consumption, and manage large result sets effectively. This documentation is tailored for developers and IT professionals seeking to leverage the full potential of Cosmos DB's MongoDB API for data processing and querying.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 12/18/2024
# CustomerIntent: As a developer, I need to understand how to use aggregation pipelines effectively within Azure Cosmos DB for MongoDB vCore. I want to optimize query performance, reduce RU consumption, and efficiently process large datasets using MongoDB aggregation stages in my applications.
---

# Aggregation Pipelines for Azure Cosmos DB MongoDB API (vCore)

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

## Introduction to Aggregation in MongoDB

Aggregation is a powerful mechanism used to process data records and return computed results. In Azure Cosmos DB's MongoDB API, aggregation is implemented using the aggregation pipeline which allows you to perform data transformations and computations.

## Overview of Aggregation Pipelines

An **aggregation** pipeline is a series of stages that process documents in the order they are defined. Each stage performs an operation on the data, such as filtering, grouping, sorting, or transforming data, and passes the results to the next stage.
In Cosmos DB's MongoDB API, the aggregation pipeline follows the same syntax and structure as in MongoDB. However, there are some performance considerations unique to Cosmos DB that should be kept in mind.

## Aggregation Pipeline Stages

Below are the common stages used in an aggregation pipeline. Each stage processes data and passes it to the next one.

1. `$match`
    - **purpose:** Filters the data by a specified condition, similar to a `WHERE` clause in SQL.
    - **Example:**
        ```json
        {
            "$match": { "status": "active" }
        }
        ```
1.  `$group`
    - **Purpose:** Groups documents by a specified identifier and performs aggregation operations such as sum, average, and count on grouped data.
    - **Example:**
        ```json
        {
            "$group": {
                "_id": "$category",
                "total_sales": { "$sum": "$sales" }
            }
        }
        ```
1.  `$sort`
    - **Purpose:** Sorts the documents based on one or more fields.
    - **Example:**
        ```json
        {
            "$sort": { "total_sales": -1 }
        }
        ```    
 1. `$project`
    - **Purpose:** Reshapes each document, typically to include, exclude, or compute new fields.
    - **Example:**
        ```json
        {
            "$project": {
                "_id": 0,
                "product_name": 1,
                "total_sales": 1
            }
        }
        ```

1.  `$limit`
    - **Purpose:** Limits the number of documents passed to the next stage.
    - **Example:**
        ```json
        {
            "$limit": 5
        }
        ```  

1.  `$skip`
    - **Purpose:** Skips the first N documents, commonly used for pagination.
    - **Example:**
        ```json
        {
            "$skip": 10
        }
        ```

1.  `$unwind`
    - **Purpose:** Deconstructs an array field into individual documents.
    - **Example:**
        ```json
        {
            "$unwind": "$items"
        }
        ```

## Aggregation Pipeline Example
Here is an example of an aggregation pipeline that retrieves the top 5 categories by total sales.
```json
[
  { 
    "$match": { "status": "active" }
  },
  {
    "$group": {
      "_id": "$category",
      "total_sales": { "$sum": "$sales" }
    }
  },
  {
    "$sort": { "total_sales": -1 }
  },
  {
    "$limit": 5
  },
  {
    "$project": {
      "_id": 0,
      "category": "$_id",
      "total_sales": 1
    }
  }
]
```
## Optimizing Aggregation Pipelines in Azure Cosmos DB
While Cosmos DB MongoDB API supports aggregation pipelines, it is important to follow best practices to ensure the best performance. Here are some optimization tips:

1. Use Indexed Fields in `$match`
When filtering data with `$match`, try to use indexed fields. This reduces the time Cosmos DB takes to scan the entire collection.

1. Minimize Unnecessary Stages
Remove any stages that are not necessary for the results you want. For example, only use `$project` if you need to reshape the output.

1. Avoid Complex `$group` Operations on Large Data Sets
The `$group` stage can be expensive, especially when operating on large datasets. Use `$match` before `$group` to reduce the number of documents being processed.

1. Use `$limit` to Reduce Data Load
If you only need a small subset of results, use `$limit` early in the pipeline to reduce the number of documents that need to be processed.

1. Monitor RU Consumption
Aggregation operations consume Request Units (RUs) in Cosmos DB, so monitor your RU consumption for high-cost operations.

## Handling Large Aggregation Results
When dealing with large result sets, consider using the following techniques:

### Pagination with `$skip` and `$limit`
You can implement pagination by using a combination of $skip and $limit. For example:

```json
[
{ "$skip": 20 },
{ "$limit": 10 }
]
```
### Result Size Limitation
If the aggregation result is too large, you can limit the result set using the maxItemCount option in Cosmos DB SDK.

## Common Errors and Troubleshooting
### Exceeding RU Limits
If you encounter errors related to exceeding the RU limits, consider the following:

- Break your aggregation into smaller steps.
- Use `$match` early in the pipeline to reduce the number of documents.
- Monitor and adjust the RU consumption based on the aggregation pipeline's complexity.

### Incorrect Data Types in `$group`
Ensure that the fields used in `$group` operations are of the correct data type (e.g., numbers for summing, strings for grouping). Incorrect data types may cause unexpected results.

### Indexing
Ensure that your collections have appropriate indexes for faster query performance, especially for fields used in `$match` or `$sort` stages.

## Azure Cosmos DB Specific Considerations
-   **Request Units (RU/s):** Aggregations in Cosmos DB consume RUs. Complex pipelines, especially those involving `$group`, `$sort`, and `$unwind`, may result in higher RU consumption. Plan your RU provisioning accordingly.

-   **Partitioning:** Cosmos DB uses partitioning to scale collections. If your collection is partitioned, ensure that your aggregation query can benefit from partitioning by targeting specific partitions.

-   **Consistency**: Cosmos DB's default consistency model is eventual consistency. Aggregation operations may return different results depending on consistency settings. If strong consistency is required, be aware of potential performance impacts.

## Best Practices for Aggregation in Cosmos DB MongoDB API
- Use `$match` as the first stage to filter unnecessary documents early in the pipeline.
- Optimize indexing for fields used in $match, `$sort`, and `$group`.
- Break down large aggregations into multiple smaller queries when working with large datasets.
- Test and monitor RU consumption for each aggregation query to avoid hitting limits.