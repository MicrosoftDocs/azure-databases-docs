---
title: Introduction/overview
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn about Azure Cosmos DB for NoSQL, what it is, and how it can be used to build solutions for unstructured data.
author: seesharprun
ms.author: sidandrews
ms.reviewer: markjbrown
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: overview
ms.date: 11/03/2025
ai-usage: ai-generated
---

# What is Azure Cosmos DB for NoSQL?

Azure Cosmos DB for NoSQL is a fully managed and serverless NoSQL and vector database for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it's ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL and vector data.

This service is tailored for NoSQL workloads for scale-out scenarios. It supports querying JSON data using a SQL-like query language, making it approachable for developers familiar with the SQL syntax while using the flexibility of a NoSQL unstructured data store.

## Global Distribution and Scalability

Azure Cosmos DB for NoSQL is designed to scale horizontally across multiple regions, ensuring low-latency access to data for users worldwide. With its turnkey global distribution, you can replicate your data across Azure regions with just a few actions. The service automatically handles partitioning and scaling to meet your application's performance and storage needs.

## Flexible Schema and JSON Data Model

The API for NoSQL uses a JSON-based data model, allowing you to store and query unstructured or semi-structured data without the constraints of a fixed schema. This flexibility makes it ideal for applications where data structures evolve over time, such as IoT, e-commerce, and social media platforms.

## Low Latency and High Availability

Azure Cosmos DB for NoSQL guarantees single-digit millisecond read and write latencies at the 99th percentile. It also offers 99.999% availability for multi-region configurations, ensuring your application remains responsive and reliable even during peak usage or regional outages.

## SQL-like Query Language

The API for NoSQL provides a SQL-like query language for querying JSON data, making it easy for developers to retrieve and manipulate data without learning a new syntax. This feature bridges the gap between traditional relational database users and NoSQL systems.

## Requirements and Dependencies

To use Azure Cosmos DB for NoSQL, you need an Azure subscription. The service integrates seamlessly with other Azure services, such as Azure Functions, Azure Logic Apps, and Azure Synapse Analytics, enabling you to build end-to-end solutions. Software Development Kits (SDKs) are available for popular programming languages, including .NET, Python, TypeScript, Rust, Go, JavaScript, and Java.

## Limitations and Considerations

While Azure Cosmos DB for NoSQL is highly versatile, it's optimized for JSON-based NoSQL workloads for scale-out scenarios.

If your application requires support for other database models, such as MongoDB, Cassandra, PostgreSQL, or Gremlin, consider one of the following services:

- [Azure DocumentDB](../../documentdb/overview.md)
- [Azure Managed Instance for Apache Cassandra](../../managed-instance-apache-cassandra/introduction.md)
- [Graph in Microsoft Fabric](/fabric/graph/overview)
- [Azure Database for PostgreSQL](../../postgresql/index.yml)
 
Additionally, the service's cost model is based on provisioned throughput (RU/s), so careful planning is required to optimize costs for your workload.

[!INCLUDE[Section - Compare to Azure DocumentDB](../includes/section-compare-to-documentdb.md)]

## Related content

- [Get started developing solutions](quickstart-python.md)
- [Learn about global distribution](../distribute-data-globally.md?context=/azure/cosmos-db/nosql/context/context)
- [Explore the JSON resource model](../resource-model.md?context=/azure/cosmos-db/nosql/context/context)
- [Design for high availability](/azure/reliability/reliability-cosmos-db-nosql?context=/azure/cosmos-db/nosql/context/context)
- [Review the NoSQL query language](/cosmos-db/query)
