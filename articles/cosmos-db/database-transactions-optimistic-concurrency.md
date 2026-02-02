---
title: Database Transactions and Optimistic Concurrency Control
description: Learn about database transactions and optimistic concurrency control in Azure Cosmos DB.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 07/07/2025
appliesto:
  - ✅ NoSQL
---

# Transactions and optimistic concurrency control

Database transactions provide a safe and predictable programming model to deal with concurrent changes to the data. Traditional relational databases, like SQL Server, allow you to write the business logic using stored procedures and triggers, and then send it to the server for execution directly within the database engine.

With traditional relational databases, you're required to deal with two different programming languages: a nontransactional application programming language, such as JavaScript, Python, C#, or Java; and a transactional programming language, such as T-SQL, that's natively executed by the database.

The database engine in Azure Cosmos DB supports full ACID (atomicity, consistency, isolation, durability) compliant transactions with snapshot isolation. All the database operations within the scope of a container's [logical partition](partitioning.md) are transactionally executed within the database engine that's hosted by the replica of the partition. These operations include both write (updating one or more items within the logical partition) and read operations.

The following table lists different operations and transaction types:

| **Operation**  | **Operation type** | **Single or multi-item transaction** |
|---------|---------|---------|
| Insert (without a pre/post trigger) | Write | Single item transaction |
| Insert (with a pre/post trigger) | Write and read | Multi-item transaction |
| Replace (without a pre/post trigger) | Write | Single item transaction |
| Replace (with a pre/post trigger) | Write and read | Multi-item transaction |
| Upsert (without a pre/post trigger) | Write | Single item transaction |
| Upsert (with a pre/post trigger) | Write and read | Multi-item transaction |
| Delete (without a pre/post trigger) | Write | Single item transaction |
| Delete (with a pre/post trigger) | Write and read | Multi-item transaction |
| Execute stored procedure | Write and read | Multi-item transaction |
| System initiated execution of a merge procedure | Write | Multi-item transaction |
| System initiated execution of deleting items based on expiration (TTL) of an item | Write | Multi-item transaction |
| Read | Read | Single-item transaction |
| Change feed | Read | Multi-item transaction |
| Paginated read | Read | Multi-item transaction |
| Paginated query | Read | Multi-item transaction |
| Execute UDF as part of the paginated query | Read | Multi-item transaction |

## Multi-item transactions

Azure Cosmos DB allows you to write [stored procedures, triggers, and user-defined-functions](stored-procedures-triggers-udfs.md) and merge procedures in JavaScript. Azure Cosmos DB natively supports JavaScript execution inside its database engine. You can register stored procedures, pre/post triggers, user-defined-functions (UDFs), and merge procedures on a container and later execute them transactionally within the Azure Cosmos DB database engine. Writing application logic in JavaScript allows natural expression of control flow, variable scoping, assignment, and integration of exception handling primitives within the database transactions directly in the JavaScript language.

The JavaScript-based stored procedures, triggers, UDFs, and merge procedures are wrapped within an ambient ACID transaction with snapshot isolation across all items within the logical partition. During its execution, if the JavaScript program throws an exception, the entire transaction is aborted and rolled-back. The resulting programming model is simple yet powerful. JavaScript developers get a durable programming model while still using their familiar language constructs and library primitives.

The ability to execute JavaScript directly within the database engine provides performance and transactional execution of database operations against the items of a container. Furthermore, since Azure Cosmos DB database engine natively supports JSON and JavaScript, there's no impedance mismatch between the type systems of an application and the database.

## Optimistic concurrency control

*Optimistic concurrency control (OCC)* allows you to prevent lost updates and deletes. Concurrent, conflicting operations are subjected to the regular pessimistic locking of the database engine hosted by the logical partition that owns the item. When two concurrent operations attempt to update the latest version of an item within a logical partition, one of them wins and the other fails. However, if one or two operations attempting to concurrently update the same item had previously read an older value of the item, the database doesn’t know if the previously read value by either or both of the conflicting operations was indeed the latest value of the item.

Fortunately, this situation can be detected with the OCC before letting the two operations enter the transaction boundary inside the database engine. The OCC protects your data from accidentally overwriting changes that were made by others. It also prevents others from accidentally overwriting your own changes.

### Implement optimistic concurrency control using ETag and HTTP headers

Every item stored in an Azure Cosmos DB container has a system defined `_etag` property. The value of the `_etag` is automatically generated and updated by the server every time the item is updated. `_etag` can be used with the client supplied `if-match` request header to allow the server to decide whether an item can be conditionally updated. If the value of the `if-match` header matches the value of the `_etag` at the server, the item is then updated. If the value of the `if-match` request header is no longer current, the server rejects the operation with an "HTTP 412 Precondition failure" response message. The client then can refetch the item to acquire the current version of the item on the server or override the version of item in the server with its own `_etag` value for the item. In addition, `_etag` can be used with the `if-none-match` header to determine whether a refetch of a resource is needed.

The item’s `_etag` value changes every time the item is updated. For replace item operations, `if-match` must be explicitly expressed as a part of the request options. For an example, see the [sample code in GitHub](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos.Samples/Usage/ItemManagement/Program.cs#L791-L887). The `_etag` values are implicitly checked for all written items touched by the stored procedure. If any conflict is detected, the stored procedure rolls back the transaction and throws an exception. With this method, either all or no writes within the stored procedure are applied atomically. This is a signal to the application to reapply updates and retry the original client request.

### Optimistic concurrency control and global distribution

The concurrent updates of an item are subjected to the OCC by Azure Cosmos DB’s communication protocol layer. For Azure Cosmos DB accounts configured for *single-region writes*, Azure Cosmos DB ensures that the client-side version of the item that you're updating (or deleting) is the same as the version of the item in the Azure Cosmos DB container. This ensures that your writes are protected from being overwritten accidentally by the writes of others and vice versa. In a multi-user environment, the optimistic concurrency control protects you from accidentally deleting or updating the wrong version of an item. As such, items are protected against the infamous "lost update" or "lost delete" problems.

In an Azure Cosmos DB account configured with *multi-region writes*, data can be committed independently into secondary regions if its `_etag` matches that of the data in the local region. Once new data is committed locally in a secondary region, it's then merged in the hub or primary region. If the conflict resolution policy merges the new data into the hub region, this data is then replicated globally with the new `_etag`. If the conflict resolution policy rejects the new data, the secondary region is rolled back to the original data and `_etag`.

## Next steps

Learn more about database transactions and optimistic concurrency control:

- [Databases, containers, and items in Azure Cosmos DB](resource-model.md)
- [Consistency levels in Azure Cosmos DB](consistency-levels.md)
- [Conflict types and resolution policies](conflict-resolution-policies.md)
- [Transactional batch operations in Azure Cosmos DB](transactional-batch.md)
- [Stored procedures, triggers, and user-defined functions](stored-procedures-triggers-udfs.md)
