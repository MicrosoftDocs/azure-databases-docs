---
title: |
  Tutorial: Handling Data Types in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: This tutorial provides a detailed guide to handling data types in Azure Cosmos DB for MongoDB vCore. It covers supported BSON types, best practices for data type selection, and strategies for schema consistency. Learn how to manage types such as String, Integer, Boolean, Date, Array, Decimal128, and more to build robust, high-performing, and scalable applications. Practical examples and solutions to common challenges like type mismatches and precision loss are included for seamless implementation.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer or IT professional, I need to understand how to handle data types in Azure Cosmos DB for MongoDB vCore, including supported BSON types, best practices, and strategies to prevent issues like type mismatches or precision loss, ensuring efficient and reliable data operations.
---

# Handling Data Types in Azure Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

Data types are the foundation of effective schema design and data modeling. Azure Cosmos DB for MongoDB vCore adheres to the BSON (Binary JSON) format, which provides a rich set of data types optimized for storage and querying. Understanding these data types and their handling is critical for ensuring consistency, performance, and compatibility in your applications.

This guide provides an in-depth explanation of supported data types in Cosmos DB for MongoDB vCore, their usage, and considerations when designing schemas or interacting with the database programmatically.

## Supported BSON Data Types
The following BSON data types are supported in Cosmos DB for MongoDB vCore:

1. **String (`String`)**
    - **Description**: Stores textual data. UTF-8 encoding is used.
    - **Use Case**: Names, descriptions, or any readable text.
    - **Example:**
        ```json
        { "name": "John Doe" }
        ```

1. **Integer (`Int32` and `Int64`)**
    - **Description**: Stores numeric data. Int32 for 32-bit integers and Int64 for 64-bit integers.
    - **Use Case**: Counting items, user IDs, timestamps.
    - **Example:**
        ```json
        { "age": 30 }
        ```

1. **Double (`Double`)**
    - **Description**: Stores floating-point numbers.
    - **Use Case**: Monetary values, measurements with decimals.
    - **Example:**
        ```json
        { "price": 19.99 }
        ```
1. **Boolean (`Boolean`)**
    - **Description**: Represents true or false values.
    - **Use Case**: Flags, statuses, or binary decisions.
    - **Example:**
        ```json
        { "isActive": true }
        ```
1. **Date (`Date`)**
    - **Description**: Stores date and time values in milliseconds since the Unix epoch.
    - **Use Case**: Timestamps, event scheduling.
    - **Example:**
        ```json
        { "createdAt": ISODate("2025-01-27T10:00:00Z") }
        ```
1. **Null (`Null`)**
    - **Description**: Represents the absence of a value or a null field.
    - **Use Case**: Optional fields, default values.
    - **Example:**
        ```json
        { "middleName": null }
        ```
1. **Array (`Array`)**
    - **Description**: Stores lists of values of any type.
    - **Use Case**: Tags, collections, or ordered sets.
    - **Example:**
        ```json
        { "tags": ["mongodb", "cosmosdb", "vcore"] }
        ```
1. **Object (``Embedded Document``)**
    - **Description**: Stores nested documents.
    - **Use Case**: Hierarchical or related data.
    - **Example:**
        ```json
        { "address": { "city": "Seattle", "zip": "98101" } }
        ```
1. **ObjectId (`ObjectId`)**
    - **Description**: Unique identifier automatically generated for _id fields.
    - **Use Case**: Primary keys for documents. 
    - **Example:**
        ```json
        { "_id": ObjectId("60ad0fd3d34d12345abcde67") }
        ```
1. **Binary Data (`Binary`)**
    - **Description**: Stores binary-encoded data.
    - **Use Case**: Images, files, or encrypted data.
    - **Example:**
        ```json
        { "file": BinData(0, "base64encodeddata") }
        ```
1. **Decimal128 (`Decimal128`)**
    - **Description**: Stores high-precision decimal values.
    - **Use Case**: Financial data requiring exact precision.
    - **Example:**
        ```json
        { "amount": NumberDecimal("1234567890.12345") }
        ```
1. **Regular Expression (`Regex`)**
    - **Description**: Stores a regular expression pattern.
    - **Use Case**: Pattern matching in queries.
    - **Example:**
        ```json
        { "pattern": /abc/i }
        ```
1. **Timestamp (`Timestamp`)**
    - **Description**: A special BSON type for internal use.
    - **Use Case**: Oplog operations, change streams.
    - **Example:**
        ```json
        { "ts": Timestamp(1609459200, 1) }
        ```
1. **Min/Max Key (`MinKey`, `MaxKey`)**
    - **Description**: Special values used to compare keys at the lowest (MinKey) or highest (MaxKey) possible values.
    - **Use Case**: Internal queries, boundary testing.
    - **Example:**
        ```json
        { "min": MinKey(), "max": MaxKey() }
        ```
        
## Best Practices for Handling Data Types
1. **Match Application Needs**: 
Choose data types based on your application’s requirements. For example, use `Decimal128` for precise financial calculations and `Date` for timestamps.

1. **Avoid Overloading Types**:
Do not overload fields with inconsistent types. For example, avoid storing both `String` and `Number` in the same field.

1. **Index Appropriately**: 
Create indexes on frequently queried fields, ensuring data types align with query patterns.

1. **Use Schema Validation**: 
Employ schema validation rules to enforce consistent data types and structure within collections.

1. **Handle Null Values Gracefully**: 
Use `Null` for optional fields instead of omitting them to maintain schema clarity.

1. **Leverage Type Conversion**: 
When migrating or integrating data, convert types as needed to ensure compatibility.


## Common Challenges and Solutions
1. **Type Mismatch**
    - **Issue**: Query fails or returns incorrect results due to inconsistent field types.
    - **Solution**: Use schema validation and ensure all documents adhere to the expected types.
1. **Precision Loss**
    - **Issue**: Floating-point calculations may lose precision.
    - **Solution**: Use Decimal128 for applications requiring exact decimal precision.
1. **Date Handling**
    - **Issue**: Incorrect timezone handling or format mismatches.
    - **Solution**: Always store dates in UTC and use the ISODate format.

## Examples

### Example 1: Validating Data Types with Schema Validation
```json
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price"],
      properties: {
        name: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        price: {
          bsonType: "double",
          description: "must be a double and is required"
        }
      }
    }
  }
});
```

### Example 2: Using Decimal128 for Precision
```json
{ "price": NumberDecimal("123.45") }
```
### Example 3: Querying Based on Data Types
```json
db.collection.find({ "price": { $type: "double" } });
```

Effectively handling data types in Cosmos DB for MongoDB vCore ensures accurate queries, efficient storage, and reliable application behavior. By understanding supported BSON types and following best practices, developers can build robust schemas and avoid common pitfalls.