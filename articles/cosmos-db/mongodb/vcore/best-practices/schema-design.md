---
title: |
  Tutorial: Schema Design in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: This tutorial provides a comprehensive guide to schema design in Azure Cosmos DB for MongoDB vCore. It explores best practices, design patterns, and considerations for optimizing data models in a flexible, document-oriented database. Developers and IT professionals will learn to balance denormalization and normalization, handle data relationships, and leverage schema design patterns such as embedding, referencing, and bucket patterns for scalable and efficient applications.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer, I need to understand schema design principles for Azure Cosmos DB for MongoDB vCore, including best practices, data modeling patterns, and optimization techniques, to build scalable, efficient, and flexible applications.
---


# Schema Design in Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Schema design is a critical aspect of building scalable, efficient, and high-performing applications on Cosmos DB for MongoDB vCore. Unlike relational databases, MongoDB leverages a flexible, schema-less design, allowing for dynamic and hierarchical data structures. However, crafting an effective schema requires careful consideration of access patterns, storage efficiency, and scalability requirements.

This guide provides best practices, examples, and considerations for designing schemas optimized for Cosmos DB for MongoDB vCore.

## Core Principles of Schema Design

### Document-Oriented Model
MongoDB uses a document-oriented data model, where data is stored as BSON (Binary JSON) documents. Each document is a self-contained unit of data, supporting hierarchical and nested structures.

### Denormalization vs. Normalization

- **Denormalization**: Embed related data within the same document to reduce joins and improve read performance.
- **Normalization**: Use references to link related data across multiple documents, reducing duplication and improving write performance.

### Schema Flexibility
MongoDB supports schema-less design, allowing documents within the same collection to have varying structures. While this flexibility is powerful, consistency should be maintained wherever possible to simplify queries and application logic.

## Key Considerations for Schema Design

1. **Access Patterns**
    - Analyze how your application reads and writes data.
    - Optimize schemas for the most common queries to reduce the need for transformations.
1. **Data Relationships**
    - One-to-One: Embed the related document directly.
    - One-to-Many: Embed or reference based on query and update frequency.
    - Many-to-Many: Use referencing to maintain scalability.
1. **Document Size**
    - Limit document size to 16 MB (MongoDB's BSON size limit).
    - For large data, consider splitting into smaller, related documents.
1. **Indexing**
    - Use indexes to optimize query performance.
    - Choose appropriate shard keys to ensure even distribution and avoid hotspots.
1. **Partitioning**
    - Design schemas with sharding in mind, ensuring data is evenly distributed across partitions using an effective shard key.
1. **Write and Read Optimization**
    - Embed data for high read throughput.
    - Normalize data for high write throughput.

## Schema Design Patterns  

1. **Single Document Pattern**
    - Store all related data in a single document for atomic operations.
    - **Use Case**: User profiles, configuration settings.

    ```json
    {
        "_id": "user123",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "preferences": {
            "theme": "dark",
            "notifications": true
        }
    }
    ```    

1. **Embedded Document Pattern**
    - Embed related entities for quick access and reduced join operations.
    - **Use Case**: Orders with line items.    
    ``` json
    {
        "_id": "order123",
        "userId": "user123",
        "items": [
            { "productId": "prod1", "quantity": 2 },
            { "productId": "prod2", "quantity": 1 }
        ],
        "total": 100.50
    }
    ```

1. **Referencing Pattern**
    - Use references for loosely coupled entities, reducing redundancy.
    - **Use Case**: Social networks or systems with large, related datasets.    
    ```json
    // Users Collection
    {
        "_id": "user123",
        "name": "John Doe",
        "friendIds": ["user124", "user125"]
    }

    ```
    ```json
    // Friends Collection
    {
        "_id": "user124",
        "name": "Jane Smith"
    }
    ```

1. **Bucket Pattern**
    - Group related data into buckets to minimize document count and reduce query overhead.
    - **Use Case**: Time-series data or logs.
    ```json
    {
        "_id": "sensor123",
        "type": "temperature",
        "readings": [
            { "timestamp": "2025-01-01T10:00:00Z", "value": 22.5 },
            { "timestamp": "2025-01-01T11:00:00Z", "value": 23.0 }
        ]
    }
    ```
1. Polymorphic Pattern
    - Use a flexible schema to store different types of entities in the same collection.
    - **Use Case**: Multi-tenant or dynamic data models.
    ```json
    {
        "_id": "1",
        "type": "user",
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    ```   
    ``` json
    {
        "_id": "2",
        "type": "product",
        "name": "Laptop",
        "price": 1200
    }
    ```

## Schema Evolution
MongoDB’s flexible schema design allows for incremental changes without downtime. To manage schema evolution:
- Use a versioning field in documents (e.g., `schemaVersion`).
- Migrate documents progressively as new application versions roll out.  

## Best Practices
1. **Embed for Read Efficiency**: Embed data when queries frequently access related information together.
1. **Reference for Write Efficiency**: Use references when related data is large or frequently updated.
1. **Optimize Shard Keys**: Choose shard keys that align with query patterns and avoid high-cardinality fields.
1. **Leverage Indexes**: Design indexes based on query patterns to improve performance.
1. **Test and Monitor**: Continuously test schema design with real-world workloads to identify bottlenecks.

Designing an effective schema in Cosmos DB for MongoDB vCore requires balancing flexibility and structure. By understanding data access patterns, relationships, and scalability needs, developers can create schemas that ensure optimal performance and maintainability.