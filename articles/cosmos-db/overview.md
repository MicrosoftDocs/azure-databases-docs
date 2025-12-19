---
title: Introduction/overview
description: Learn about Azure Cosmos DB for NoSQL, what it is, and how it can be used to build solutions for unstructured data.
author: seesharprun
ms.author: sidandrews
ms.reviewer: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: overview
ms.date: 12/15/2025
ai-usage: ai-generated
appliesto:
  - ✅ NoSQL
---

# What is Azure Cosmos DB for NoSQL?

Azure Cosmos DB for NoSQL is a fully managed and serverless NoSQL and vector database for modern app development, including AI applications and agents. With SLA-backed speed, availability, and instant dynamic scalability, it's ideal for real-time workloads that demand high performance and distributed processing over massive volumes of JSON and vector data.

This service is part of the Azure Cosmos DB portfolio but is tailored for NoSQL workloads. It supports querying JSON data with a SQL-like query language, which makes it approachable for developers who know SQL while still benefiting from the flexibility of a schema-agnostic data store.

## Global Distribution and Scalability

Azure Cosmos DB for NoSQL is designed to scale horizontally across multiple regions, ensuring low-latency access to data for users worldwide. With turnkey global distribution, you can replicate data across Azure regions with only a few actions while the service automatically handles partitioning and scaling to meet performance and storage needs.

## Flexible Schema and JSON Data Model

The API for NoSQL uses a JSON-based data model, allowing you to store and query unstructured or semi-structured data without rigid schema constraints. This flexibility makes it a fit for applications where data structures evolve frequently, such as IoT, e-commerce, and social media platforms.

## Low Latency and High Availability

Azure Cosmos DB for NoSQL guarantees single-digit millisecond read and write latencies at the 99th percentile. It also offers 99.999% availability for multi-region configurations so your application remains responsive and reliable during peak usage or regional outages.

## SQL-like Query Language

The API for NoSQL provides a SQL-like query language for querying JSON data, helping developers retrieve and manipulate data without learning an unfamiliar syntax. This feature bridges the gap between traditional relational database users and distributed NoSQL systems.

## Requirements and Dependencies

To use Azure Cosmos DB for NoSQL, you need an Azure subscription. The service integrates with Azure Functions, Azure Logic Apps, Azure Synapse Analytics, and other Azure services to build end-to-end solutions. Software Development Kits (SDKs) are available for popular programming languages, including .NET, Python, TypeScript, JavaScript, Java, Go, and Rust.

## Limitations and Considerations

Azure Cosmos DB for NoSQL is optimized for JSON-based, scale-out workloads. When your scenario aligns with a different data model, consider this guidance to land on the right service:

- [Azure DocumentDB](../documentdb/overview.md) when you need MongoDB aggregation pipelines, multi-document transactions, or multicloud portability without refactoring drivers.
- [Azure Managed Instance for Apache Cassandra](../managed-instance-apache-cassandra/introduction.md) when you require unchanged Cassandra Query Language (CQL) workloads with full Cassandra node-level control.
- [Cosmos AIGraph (OmniRAG)](https://github.com/AzureCosmosDB/CosmosAIGraph) when your graph workload centers on Retrieval Augmented Generation (RAG) or AI-driven traversals that combine knowledge graphs with vector/hybrid search.
- [Graph in Microsoft Fabric](/fabric/graph/overview) when you need analytical graph processing, BI integrations, or GQL-compliant workloads operating inside OneLake.
- [Azure Database for PostgreSQL](../postgresql/index.yml) when you require a relational engine with SQL joins, stored procedures, or scale-up transactional semantics.

Because the API for NoSQL uses a request unit (RU/s) cost model, estimate and monitor throughput to optimize spending for your workload.

## Azure Cosmos DB vs. Azure DocumentDB

Azure Cosmos DB and Azure DocumentDB are both NoSQL database services built to store JSON data with high reliability. Azure Cosmos DB is optimized for scale-out scenarios that demand global distribution, massive scale, and instantaneous scaling with automatic failover across regions.

Azure DocumentDB (vCore) is optimized for scale-up scenarios that prioritize rich query capabilities and familiar development experiences. It runs on the open-source DocumentDB engine built on PostgreSQL with full MongoDB wire protocol compatibility. This compatibility makes it ideal for complex aggregation pipelines, analytics, and advanced document database features.

| Characteristic | Azure Cosmos DB (RU/serverless) | Azure DocumentDB (vCore) |
| --- | --- | --- |
| Availability service level agreement (SLA) | 99.999% (multi-region) | 99.995% |
| Scaling model | Horizontal (RU-based + serverless) | Vertical (vCore-based) |
| Query focus | Optimized for point reads and distributed queries | Advanced aggregation pipelines and complex joins |
| Global distribution | Turnkey multi-region with automatic failover | Regional deployment with optional geo-replicas |
| Cost model | Variable RU-based or serverless | Predictable compute + storage |

For more detailed information, see [Azure DocumentDB vs. Azure Cosmos DB decision guide](../documentdb/compare-cosmos-db.md?context=/azure/cosmos-db/context/context).

## Related content

- [Get started developing solutions](quickstart-python.md)
- [Learn about global distribution](distribute-data-globally.md)
- [Explore the JSON resource model](resource-model.md)
- [Design for high availability](/azure/reliability/reliability-cosmos-db-nosql?context=/azure/cosmos-db/context/context)
- [Review the NoSQL query language](/cosmos-db/query?context=/azure/cosmos-db/context/context)
