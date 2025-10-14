---
title: Change Feed Design Patterns
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn common change feed design patterns in Azure Cosmos DB for NoSQL, including event sourcing, real-time processing, and data movement.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 09/03/2025
ms.custom: cosmos-db-video, build-2023
ai-usage: ai-assisted
applies-to:
  - ✅ NoSQL
---

# Change feed design patterns in Azure Cosmos DB for NoSQL

The Azure Cosmos DB change feed lets you efficiently process large datasets with high write volumes. It provides an alternative to querying entire datasets to identify changes. This article explains common change feed design patterns, their tradeoffs, and limitations to help you build scalable solutions.

> [!VIDEO 9fa5b80e-43be-4aaf-ac16-c928be26e1ab]

## Scenarios

Azure Cosmos DB is ideal for IoT, gaming, retail, and operational logging applications. A common design pattern in these applications is to use changes to the data to trigger other actions. These actions include:

- Triggering a notification or a call to an API when an item is inserted, updated, or deleted.
- Real-time stream processing for IoT or analytics on operational data.
- Data movement such as synchronizing with a cache, a search engine, a data warehouse, or cold storage.

The change feed in Azure Cosmos DB lets you build efficient, scalable solutions for these patterns, as shown in the following image:

:::image type="content" source="media/change-feed-design-patterns/overview.png" alt-text="Diagram showing how Azure Cosmos DB change feed powers real-time analytics and event-driven computing scenarios." border="false":::

## Event computing and notifications

The Azure Cosmos DB change feed simplifies scenarios that trigger a notification or call an API based on a specific event. Use the [change feed processor](change-feed-processor.md) to automatically poll your container for changes and call an external API for each write, update, or delete.

Selectively trigger a notification or call an API based on specific criteria. For example, if you're reading from the change feed using [Azure Functions](change-feed-functions.md), add logic to the function to send a notification only if a condition is met. Although the Azure Function code executes for each change, the notification is sent only if the condition is met.

## Real-time stream processing

The Azure Cosmos DB change feed lets you perform real-time stream processing for IoT or real-time analytics on operational data. For example, you receive and store event data from devices, sensors, infrastructure, and applications, and process these events in real time by using [Spark](/azure/hdinsight/spark/apache-spark-overview). The following image shows how to implement a lambda architecture by using the Azure Cosmos DB change feed:

:::image type="content" source="media/change-feed-design-patterns/lambda.png" alt-text="Diagram that shows an Azure Cosmos DB-based lambda pipeline for ingestion and query." border="false":::

In many cases, stream processing implementations first receive a high volume of incoming data into a temporary message queue such as Azure Event Hubs or Apache Kafka. The change feed is a great alternative due to Azure Cosmos DB's ability to support a sustained high rate of data ingestion with guaranteed low read and write latency.

### Data persistence

Data written to Azure Cosmos DB appears in the change feed. In [latest version mode](change-feed-modes.md#latest-version-change-feed-mode), the data remains in the change feed until deletion. Message queues usually have a maximum retention period. For example, [Azure Event Hubs](https://azure.microsoft.com/services/event-hubs/) offers a maximum data retention of 90 days.

### Query ability

In addition to reading from an Azure Cosmos DB container's change feed, run SQL queries on the data stored in Azure Cosmos DB. The change feed isn't a duplication of data that's already in the container, but rather, it's just a different mechanism of reading the data. Therefore, if you read data from the change feed, the data is always consistent with queries of the same Azure Cosmos DB container.

### High availability

Azure Cosmos DB provides up to 99.999% read and write availability. Unlike many message queues, Azure Cosmos DB data can be globally distributed and configured with an [recovery time objective (RTO)](../consistency-levels.md#consistency-levels-and-data-durability) of zero.

After processing items in the change feed, build a materialized view and persist aggregated values back in Azure Cosmos DB. For example, use Azure Cosmos DB's change feed to implement real-time leaderboards based on scores from completed games.

## Data movement

Read from the change feed for real-time data movement.

For example, the change feed lets you perform the following tasks efficiently:

- Update a cache, search index, or data warehouse with data stored in Azure Cosmos DB.

- Perform zero-downtime migrations to another Azure Cosmos DB account or to another Azure Cosmos DB container that has a different logical partition key.

- Implement application-level data tiering and archival. For example, store "hot data" in Azure Cosmos DB and age out "cold data" to other storage systems like [Azure Blob Storage](/azure/storage/common/storage-introduction).

When you have to [denormalize data across partitions and containers](model-partition-example.md#v2-introduce-denormalization-to-optimize-read-queries), you can read from your container's change feed as a source for this data replication. Real-time data replication with the change feed guarantees only eventual consistency. You can [monitor how far the change feed processor lags behind](how-to-use-change-feed-estimator.md) in processing changes in your Azure Cosmos DB container.

## Event sourcing

The [event sourcing pattern](/azure/architecture/patterns/event-sourcing) uses an append-only store to record the full series of actions on data. The Azure Cosmos DB change feed is a great choice as a central data store in event sourcing architectures in which all data ingestion is modeled as writes (no updates or deletes). In this case, each write to Azure Cosmos DB is an "event," so there's a full record of past events in the change feed. Typical uses of the events published by the central event store are to maintain materialized views or to integrate with external systems. Because there isn't a time limit for retention in the [change feed latest version mode](change-feed-modes.md#latest-version-change-feed-mode), you can replay all past events by reading from the beginning of your Azure Cosmos DB container's change feed. You can even have [multiple change feed consumers subscribe to the same container's change feed](how-to-create-multiple-cosmos-db-triggers.md#optimizing-containers-for-multiple-triggers).

Azure Cosmos DB is an excellent central append-only persistent data store in the event sourcing pattern because of its strengths in horizontal scalability and high availability. Additionally, the change feed processor offers an ["at least once"](change-feed-processor.md#error-handling) guarantee, ensuring that you don't miss processing any events.

## Current limitations

The change feed has multiple modes, each with important limitations you should understand. There are several areas to consider when you design an application that uses the change feed in either [latest version mode](change-feed-modes.md#latest-version-change-feed-mode) or [all versions and deletes mode](change-feed-modes.md#all-versions-and-deletes-change-feed-mode-preview).

### Intermediate updates

#### [Latest version mode](#tab/latest-version)

In latest version mode, only the most recent change for a specific item is included in the change feed. When processing changes, you read the latest available item version. If there are multiple updates to the same item in a short period of time, it's possible to miss processing intermediate updates. To replay past individual updates to an item, model these updates as a series of writes or use all versions and deletes mode.

#### [All versions and deletes mode (preview)](#tab/all-versions-and-deletes)

All versions and deletes mode provides a full operation log of every item version from all operations. No intermediate updates are missed when they occur within the continuous backup retention period configured for the account.

---

### Deletes

#### [Latest version mode](#tab/latest-version)

The change feed latest version mode doesn't capture deletes. When you delete an item from your container, the item is removed from the change feed. The most common method to handle delete operations is to add a soft marker to the items being deleted. You can add a property called `deleted` and set it to `true` at the time of deletion. This document update shows up in the change feed. You can set a Time to Live (TTL) on this item so that it can be automatically deleted later.

#### [All versions and deletes mode (preview)](#tab/all-versions-and-deletes)

Deletes are captured in all versions and deletes mode without needing to set a soft delete marker. You also get metadata that indicates whether the delete was from a TTL expiration.

---

### Retention

#### [Latest version mode](#tab/latest-version)

The change feed in latest version mode has an unlimited retention. As long as an item exists in your container, it's available in the change feed.

#### [All versions and deletes mode (preview)](#tab/all-versions-and-deletes)

All versions and deletes mode lets you read changes that occur within the continuous backup retention period configured for the account. With a seven-day retention period, you can't read changes from eight days ago. If your application needs to track all updates from the beginning of the container, latest version mode might be a better fit.

---

### Guaranteed order

All change feed modes have a guaranteed order within a partition key value, but not across partition key values. You should select a partition key that gives you a guarantee of meaningful order.

Consider a retail application that uses the event sourcing design pattern. In this application, different user actions are each "events," which are modeled as writes to Azure Cosmos DB. Imagine if some example events occurred in the following sequence:

1. Customer adds Item A to their shopping cart.
1. Customer adds Item B to their shopping cart.
1. Customer removes Item A from their shopping cart.
1. Customer checks out and shopping cart contents are shipped.

A materialized view of current shopping cart contents is maintained for each customer. This application must ensure that these events are processed in the order in which they occur. For example, if the cart checkout were to be processed before Item A's removal, it's likely that Item A shipped to the customer instead of the Item B the customer wanted instead. To ensure these four events are processed in order, they should fall within the same partition key value. If you select `username` (each customer has a unique username) as the partition key, you can guarantee that these events show up in the change feed in the same order in which they're written to Azure Cosmos DB.

## Examples

Here are real-world change feed code examples for the latest version mode that go beyond the scope of the provided samples:

- Learn more in [Introduction to the change feed](https://azurecosmosdb.github.io/labs/dotnet/labs/08-change_feed_with_azure_functions.html).
- Learn more in [IoT use case centered around the change feed](https://github.com/AzureCosmosDB/scenario-based-labs).
- Learn more in [Retail use case centered around the change feed](https://github.com/AzureCosmosDB/scenario-based-labs).

## Related content

- [Change feed overview](../change-feed.md)
- [Change feed modes](change-feed-modes.md)
- [Options to read your change feed](read-change-feed.md)
