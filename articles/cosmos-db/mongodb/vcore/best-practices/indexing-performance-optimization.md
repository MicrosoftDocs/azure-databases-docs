---
title: |
  Tutorial: Indexing and Performance Optimization for Azure Cosmos DB MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: This tutorial provides a detailed guide on indexing and performance optimization for Azure Cosmos DB for MongoDB vCore. It covers the various types of indexes, such as single-field, compound, and wildcard indexes, and their practical use cases. The document explains how to configure custom indexing policies, monitor index usage, and implement indexing strategies for optimized performance. It also highlights best practices to reduce Request Unit (RU) consumption, avoid over-indexing, and enhance query efficiency. This documentation is intended for developers and IT professionals looking to maximize the performance of their Cosmos DB for MongoDB vCore workloads.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 01/20/2025
# CustomerIntent: As a developer or IT professional, I need to understand the types of indexes supported in Azure Cosmos DB for MongoDB vCore, how to configure and monitor indexing policies, and strategies to optimize query performance while minimizing RU consumption. This knowledge will help me build efficient and cost-effective applications.
---

# Indexing and Performance Optimization for Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]


## Types of Indexes Supported
1. Default Indexes
    - By default, every collection has an index on the _id field, which ensures uniqueness and fast lookups.
      ```javascript
      db.collection.find({ _id: ObjectId("60d5f97c3c1a4b2a4c123456") })
      ``` 
    - The above query uses the default `_id` index for efficient retrieval.  

1. Single-field Indexes
    - Indexes a single field to optimize queries that filter on that field.
    - Example
      Create an index on the `username` field:
      ```javascript
      db.collection.createIndex({ username: 1 })
      ```
      Query using the index:
      ```javascript
      db.collection.find({ username: "john_doe" })
      ```
1. Compound Indexes
    - Combine multiple fields into a single index to optimize queries that involve multiple conditions.
    - Example:
      Create an index on `first_name` and `last_name`:
      ```javascript
      db.collection.createIndex({ first_name: 1, last_name: 1 })
      ```
      Query using the index:
      ```javascript
      db.collection.find({ first_name: "John", last_name: "Doe" })
      ```
    - Note: The index can also be used for queries filtering on `first_name` alone but not for `last_name` alone.

1. Wildcard Indexes
    - Automatically index all fields or a subset of fields dynamically.      
    - Example:
      Create a wildcard index for all subfields under `user_profile`:
      ```javascript
      db.collection.createIndex({ "user_profile.$**": 1 })
      ```
      Query using the index:
      ```javascript
      db.collection.find({ "user_profile.address.city": "Seattle" })
      ```
1. Text Indexes
    - Enable full-text search on string fields.
    - Example:
      Create a text index on `title` and `description`:
      ```javascript
      db.collection.createIndex({ title: "text", description: "text" })
      ```
      Query using the index:
      ```javascript
      db.collection.find({ $text: { $search: "MongoDB indexing" } })
      ``` 
1. TTL Indexes (Time-to-Live)
    - Automatically delete documents after a specified time. Useful for session data or temporary logs.
    - Example:
      Create a TTL index on the `createdAt` field with a 1-hour expiration:
      ```javascript
      db.collection.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })
      ```
      Insert a document with a createdAt field:
      ```javascript
      db.collection.insertOne({ name: "temp_data", createdAt: new Date() })
      ```
    - The document will be automatically deleted after one hour.

## Automatic Indexing in Azure Cosmos DB
**Automatic indexing** is a key feature of Azure Cosmos DB for MongoDB vCore. It ensures that all fields in your documents are automatically indexed by default, making it easier to perform queries without manually managing index creation.   
- Pros: Query performance without manual configurations.
- Cons: Potential overhead for write operations. 

## Configuring Custom Indexing Policies
Custom indexing policies allow developers to tailor indexing behavior in Azure Cosmos DB for MongoDB vCore to fit specific application needs. By configuring indexing policies, you can control which fields are indexed, how they are indexed, and reduce indexing overhead to optimize performance and minimize storage costs.
- Use cases:
    1. Reducing write latency.
    1. Optimizing storage by excluding fields that don’t require indexing.
- Examples 
    - Excluding specific fields from being indexed
        ```json
        {
            "excludedPaths": [
                {
                "path": "/largeDataField/?"
                }
            ]
        }

        ``` 
    - Including only specific fields for indexing
        ```json
        {
            "includedPaths": [
                {
                "path": "/specificField/?"
                }
            ]
        }

        ```    

##  Indexing Strategies for Performance Optimization
- **Equality Queries** Use single-field or compound indexes for equality filters. 
    ```javascript
    db.collection.createIndex({ field: 1 })
    ```
- **Range Queries** Create indexes for range operations (e.g., `$lt`, `$gt`, `$gte`, `$lte`).
    ```javascript
    db.collection.createIndex({ price: 1 })
    ```
- **Sort Operations** Use indexes to optimize sort queries.     
    ```javascript
    db.collection.createIndex({ name: 1, age: -1 })
    ```
- **Multikey Indexes** Explain indexing for array fields and how MongoDB vCore expands arrays for indexing.    

## Monitoring Index Usage
- **Index Statistics**: Use the `explain()` method to analyze query plans.
    ```javascript
    db.collection.find({ field: value }).explain("executionStats")
    ```
- `Index Hits and Misses`: Identify underutilized or unused indexes.   

## Performance Considerations
- **Index Overhead**: Increased storage and write operation costs for too many indexes.
- **Avoid Over-Indexing**: Index only fields frequently queried.
- **Batch Writes**: Use batch operations to minimize write latencies.
- **Query Optimization**: Use projections to return only required fields.

## Real-World Examples
- **Case Study 1**: Optimizing an e-commerce app with compound indexes for product searches.
- **Case Study 2**: Reducing write latencies in a high-throughput IoT application by excluding large payloads from indexing.

##  Tools for Performance Monitoring
- **Azure Metrics**: Monitor RU consumption and identify queries with high RU costs.
- **Azure Monitor**: Set up alerts for high indexing costs or write latencies.