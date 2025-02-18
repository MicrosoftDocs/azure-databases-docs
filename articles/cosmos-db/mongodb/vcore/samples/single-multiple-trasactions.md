---
title: |
  Tutorial: Single vs. Multi-Document Transactions in Azure Cosmos DB for MongoDB vCore
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: This tutorial explores the concept of single vs. multi-document transactions in Azure Cosmos DB for MongoDB vCore, highlighting their key differences, use cases, and implementation. The guide provides a detailed comparison, performance considerations, and best practices to help developers and IT professionals make informed decisions when designing scalable, consistent, and optimized applications. Examples and step-by-step instructions are included for practical understanding and seamless integration.
author: v-smedapati
ms.author: v-smedapati
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.topic: tutorial
ms.date: 11/29/2024
# CustomerIntent: As a developer or IT professional, I need to understand the differences between single and multi-document transactions in Azure Cosmos DB for MongoDB vCore. This includes knowing their use cases, performance trade-offs, and implementation strategies to design efficient and reliable database interactions for my applications.
---

# Single vs. Multi-Document Transactions in Cosmos DB for MongoDB vCore

[!INCLUDE[MongoDB (vCore)](~/reusable-content/ce-skilling/azure/includes/cosmos-db/includes/appliesto-mongodb-vcore.md)]

## Single-Document Transactions
A **single-document transaction** involves operations confined to a single document in a collection. Since MongoDB ensures atomicity at the document level, any operation (or sequence of operations) on a single document is inherently transactional.

### Key Features
- **Atomicity**: Modifications within a single document (e.g., updates to multiple fields) are treated as an atomic operation.

- **Performance**: Single-document transactions are faster because they don't require additional overhead like locks or journaling across multiple documents.

- **Use Cases**:
    - Updating multiple fields in the same document.
    - Handling embedded documents or arrays within a single document.

### Example
Consider a scenario where we update a customer's address and phone number in the same document:

```javascript
db.customers.updateOne(
  { _id: "12345" },
  {
    $set: {
      "address.street": "123 Maple St",
      "phone": "555-1234"
    }
  }
);
```
This operation is atomic and ensures the document's integrity without requiring explicit transaction management. 

## Multi-Document Transactions
A **multi-document transaction** spans multiple documents within one or more collections. Cosmos DB for MongoDB vCore supports ACID transactions across documents, ensuring data consistency even in distributed environments.

### Key Features
- **Atomicity**: Guarantees all operations in the transaction are committed or rolled back together.
- **Consistency**: Ensures the database remains in a consistent state even during concurrent operations.
- **Scalability**: Supported across partitioned collections when using shard keys effectively.
- **Use Cases**:
    - Complex business workflows requiring consistency across multiple documents or collections.
    - Financial operations, such as transferring funds between accounts.

### Example
Consider transferring funds between two accounts. This requires modifying two documents atomically:

```javascript
const session = db.getMongo().startSession();

session.startTransaction();

try {
  const accountsCollection = session.getDatabase("bank").accounts;

  // Deduct amount from one account
  accountsCollection.updateOne(
    { _id: "account1" },
    { $inc: { balance: -500 } },
    { session }
  );

  // Add amount to another account
  accountsCollection.updateOne(
    { _id: "account2" },
    { $inc: { balance: 500 } },
    { session }
  );

  // Commit the transaction
  session.commitTransaction();
} catch (error) {
  // Rollback on error
  session.abortTransaction();
  console.error("Transaction aborted: ", error);
} finally {
  session.endSession();
}
```

## Differences Between Single and Multi-Document Transactions

| Aspect | Single-Document Transactions | Multi-Document Transactions |
| --- | --- | --- |
|**Scope** | Limited to a single document. | Spans multiple documents. |
| **Complexity** | Simple to implement. | Requires session and transaction management. |
| **Performance** | High due to lower overhead. | Slightly lower due to transactional overhead. |
| **Use Cases** | Small, self-contained updates. | Complex, interrelated operations. |
| **Atomicity Support** | Built-in at the document level. | Explicitly managed by the developer. |


## Performance Considerations
1. **Latency**: Multi-document transactions introduce additional latency due to the need for coordination and journaling.
1. **Resource Utilization**: Transactions consume additional memory and CPU resources, especially in write-intensive workloads.
1. **Partitioning**: When working with partitioned collections, ensure the shard key strategy minimizes cross-partition transactions.


## Best Practices
- Use single-document transactions wherever possible to minimize complexity and improve performance.
- Optimize shard key design for multi-document transactions to avoid cross-partition operations.
- Monitor and log transactions to identify bottlenecks and optimize queries.
- Test and validate rollback scenarios to ensure application resilience.