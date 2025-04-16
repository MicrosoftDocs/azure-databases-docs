---
title: Migrate from Azure Cosmos DB Kafka Connector V1 to V2
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

> This guide helps users upgrade from the V1 to V2 Azure Cosmos DB Kafka Connectors (source and sink). V2 introduces significant **breaking changes**, architectural improvements, and configuration updates.

---

## 🔄 Key Architectural Differences

| Feature                            | V1 Connector (Legacy)                       | V2 Connector (Modern)                             |
|------------------------------------|---------------------------------------------|---------------------------------------------------|
| Change Feed Mode                   | **Change Feed Processor** (Lease container) | **Change Feed Pull Model** (Kafka offset topic)   |
| Offset Storage                     | Cosmos DB lease container                   | Kafka internal offset topics                      |
| Delivery Semantics (Source)       | At-least-once                               | Exactly-once                                      |
| Delivery Semantics (Sink)         | At-least-once                               | Exactly-once                                      |
| Parallelism                        | Cosmos SDK partitions                       | Kafka Connect task/thread model                   |
| SDK Version                        | Legacy SDK                                  | Azure Cosmos Java SDK v4                          |
| State/Checkpoint Compatibility     | Cosmos-managed (in container)               | Kafka-managed (in topic)                          |
| Configuration Style                | Cosmos-specific, lease-based                | Kafka-native, declarative                         |

---

## ⚙️ Configuration Comparison (V1 vs. V2)

### 🔹 Connection Configuration

| V1 Config                          | V2 Config                          | Notes                                |
|-----------------------------------|------------------------------------|--------------------------------------|
| `cosmos.master.key`               | `cosmos.account.key`               | Renamed for clarity                  |
| `cosmos.host`                     | `cosmos.account.endpoint`          | Renamed for consistency              |

---

### 🔹 Source Connector Configuration

| V1 Config                          | V2 Config                          | Notes                                          |
|-----------------------------------|------------------------------------|------------------------------------------------|
| `cosmos.source.container`         | `cosmos.container.name`            | Unified naming                               |
| `cosmos.database.name`            | `cosmos.database.name`             | Unchanged                                     |
| `cosmos.source.database`          | *removed*                          | Use `cosmos.database.name`                   |
| `cosmos.source.lease.container`   | *removed*                          | Leases not used in V2                         |
| `cosmos.source.lease.prefix`      | *removed*                          | Lease management removed                      |
| `cosmos.source.start.from.latest` | `cosmos.source.start.from`         | Use `Beginning` or `Now`                      |
| `cosmos.source.task.count`        | `tasks.max`                        | Standard Kafka Connect config                 |

---

### 🔹 Sink Connector Configuration

| V1 Config                          | V2 Config                          | Notes                                      |
|-----------------------------------|------------------------------------|--------------------------------------------|
| `cosmos.sink.database.name`       | `cosmos.database.name`             | Unified                                    |
| `cosmos.sink.container.name`      | `cosmos.container.name`            | Unified                                    |
| `cosmos.sink.upsert.enabled`      | `cosmos.sink.upsert.enabled`       | Preserved                                  |
| `cosmos.sink.id.strategy`         | `cosmos.sink.id.strategy`          | Preserved                                  |

---

### 🧪 Observability & Debugging

| V1 Config                          | V2 Config                          | Notes                                     |
|-----------------------------------|------------------------------------|-------------------------------------------|
| Custom logging in code            | Standard SLF4J logging             | Use Kafka Connect logs                    |
| Lease container inspection        | Kafka offset topic inspection      | Compatible with Kafka tooling             |

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

