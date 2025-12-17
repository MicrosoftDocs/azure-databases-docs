---
title: Migrate From Kafka Connector V1 to V2
description: Learn how to migrate your application from using Azure Cosmos DB Kafka Connector V1 to V2
author: TheovanKraay
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 04/16/2025
ms.author: thvankra
ms.devlang: java
---

# Migration Guide: Azure Cosmos DB Kafka Connector V1 → V2

This guide helps users upgrade from the V1 to V2 Azure Cosmos DB Kafka Connectors (source and sink). V2 introduces significant **breaking changes**, architectural improvements, and configuration updates.

## 🔄 Key Architectural Differences

It is important to understand the difference between Kafka V1 and Kafka V2 connector. While the sink connector has almost no difference in terms of performance and implementation details, V2 source connector uses [Change Feed Pull Model framework](change-feed-pull-model.md). This allows the V2 source connector to handle multiple containers under a database compared to V1 Source Connector which was only able to handle a single container per connector instance. This difference makes the V2 source connector more efficient compared to the V1 source connector in terms of memory and throughput. V2 connector has planet scale optimization over V1 connector.

| Feature                          | V1 Connector (Legacy)                     | V2 Connector (Modern)                           |
|----------------------------------|-------------------------------------------|-------------------------------------------------|
| Change Feed Mode                 | **Change Feed Processor** (Lease container) | **Change Feed Pull Model** (Kafka offset topic) |
| Offset Storage                   | Cosmos DB lease container                 | Kafka internal offset topics                    |
| Delivery Semantics (Source)     | At-least-once                             | Exactly-once                                    |
| Delivery Semantics (Sink)       | At-least-once                             | Exactly-once                                    |
| Parallelism                     | Cosmos SDK partitions                     | Kafka Connect task/thread model                 |
| SDK Version                     | Legacy SDK                                | Azure Cosmos Java SDK V4                        |
| State/Checkpoint Compatibility  | Cosmos-managed (in container)             | Kafka-managed (in topic)                        |
| Configuration Style             | Cosmos-specific, lease-based              | Kafka-native, declarative                       |
| Authentication Mechanism        | Only Key based authentication support     | Key Based + Entra ID authentication Support     |
| Throughput Control Support      | Not supported                             | Throughput Control Group is supported           |

---

## ⚙️ Configuration Comparison (V1 vs. V2)

### 🔹 Connection Configuration

| V1 Config                       | V2 Config                       | Notes                   |
|--------------------------------|----------------------------------|-------------------------|
| `connect.cosmos.master.key`    | `azure.cosmos.account.key`      | Renamed for clarity     |
| `connect.cosmos.host`          | `azure.cosmos.account.endpoint` | Renamed for consistency |

### Newly added Connection Configurations in the V2 connector

| Configuration Name                      | Notes                                          |
|-----------------------------------------|------------------------------------------------|
| `azure.cosmos.account.tenantId`         | Required for service principal authentication  |
| `azure.cosmos.auth.aad.clientSecret`    | Required for service principal authentication  |
| `azure.cosmos.auth.aad.clientId`        | ClientId/ApplicationId of the service principal|
| `azure.cosmos.auth.aad.clientSecret`    | Client secret/password of the service principal|

---

### 🔹 Source Connector Configuration

| V1 Config                                 | V2 Config                          | Notes                                  |
|-------------------------------------------|------------------------------------|----------------------------------------|
| `connect.cosmos.source.container`         | `azure.cosmos.container.name`      | Unified naming                         |
| `connect.cosmos.database.name`            | `azure.cosmos.database.name`       | Unchanged                              |
| `connect.cosmos.source.database`          | *removed*                          | Use `cosmos.database.name`             |
| `connect.cosmos.source.lease.container`   | *removed*                          | Leases not used in V2                  |
| `connect.cosmos.source.lease.prefix`      | *removed*                          | Lease management removed               |
| `connect.cosmos.source.start.from.latest` | `azure.cosmos.source.start.from`   | Use `Beginning` or `Now`               |
| `connect.cosmos.source.task.count`        | `tasks.max`                        | Standard Kafka Connect config          |

Further configuration properties can be found on [Kafka Connector V2 source connector documentation](kafka-connector-source-v2.md#source-configuration-properties)

---

### 🔹 Sink Connector Configuration

| V1 Config                            | V2 Config                            | Notes       |
|-------------------------------------|--------------------------------------|-------------|
| `connect.cosmos.sink.database.name` | `azure.cosmos.database.name`         | Unified     |
| `connect.cosmos.sink.container.name`| `azure.cosmos.container.name`        | Unified     |
| `connect.cosmos.sink.upsert.enabled`| `azure.cosmos.sink.upsert.enabled`   | Preserved   |
| `connect.cosmos.sink.id.strategy`   | `azure.cosmos.sink.id.strategy`      | Preserved   |

Further configuration properties can be found on [Kafka Connector V2 sink connector documentation](kafka-connector-sink-v2.md#sink-configuration-properties)

---

### 🧪 Observability & Debugging

| V1 Config                   | V2 Config                   | Notes                        |
|----------------------------|-----------------------------|------------------------------|
| Custom logging in code     | Standard SLF4J logging      | Use Kafka Connect logs       |
| Lease container inspection | Kafka offset topic inspection| Compatible with Kafka tooling|

---

## ⚠️ Breaking Changes

- **Lease Container Removed**: Metadata is no longer stored in a Cosmos container.
- **Start Position**: V2 must restart from either the beginning or current time using `cosmos.source.start.from`.
- **Offset Management**: Now handled by Kafka internally — not transferable from lease containers.
- **Thread Model**: V2 uses Kafka’s task threading model. Adjust `tasks.max` instead of Cosmos-specific settings.

---

## ✅ Migration Steps

1. **Stop the V1 Connector**

   - Use Kafka Connect's REST API to gracefully stop your running V1 connector.
   - Back up any data needed from the lease container (if required).

2. **Deploy the V2 Connector**

   - Place V2 connector JARs into the Kafka Connect plugin path.
   - Remove old V1 connector JARs to avoid conflicts.

3. **Create New Configurations**

   - Example Source Config (V2):

     ```json
     {
       "name": "cosmos-source",
       "connector.class": "com.azure.cosmos.kafka.connect.source.CosmosSourceConnector",
       "tasks.max": "1",
       "cosmos.account.endpoint": "<endpoint>",
       "cosmos.account.key": "<key>",
       "cosmos.database.name": "<database>",
       "cosmos.container.name": "<container>",
       "topic": "<kafka-topic>",
       "cosmos.source.start.from": "Beginning"
     }
     ```

   - Example Sink Config (V2):

     ```json
     {
       "name": "cosmos-sink",
       "connector.class": "com.azure.cosmos.kafka.connect.sink.CosmosSinkConnector",
       "tasks.max": "1",
       "cosmos.account.endpoint": "<endpoint>",
       "cosmos.account.key": "<key>",
       "cosmos.database.name": "<database>",
       "cosmos.container.name": "<container>",
       "topics": "<kafka-topic>",
       "cosmos.sink.upsert.enabled": true
     }
     ```

4. **Start the V2 Connector**

   - Submit the new config using Kafka Connect REST API.
   - Monitor logs and topic data flow.

5. **Validate Output**

   - Confirm document ingestion or read progress via metrics and Cosmos DB Insights.
   - Validate offset commits in internal Kafka topics.

---

## 📌 Additional Tips

- **Test in staging** before running V2 in production.
- If exact delivery guarantees are critical, start with a new Kafka topic to avoid duplicates.
- Clean up old lease containers once confident with V2.

---

## 📚 References

- [V2 Connector GitHub](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/cosmos/azure-cosmos-kafka-connect)
- [Kafka Connect Docs](https://kafka.apache.org/documentation/#connect)
