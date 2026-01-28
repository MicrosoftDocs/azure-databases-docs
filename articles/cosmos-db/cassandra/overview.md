---
title: Introduction/Overview
titleSuffix: Azure Cosmos DB for Apache Cassandra
description: Learn how to use Azure Cosmos DB for Apache Cassandra to power existing and new applications with Cassandra drivers and CQL.
author: seesharprun
ms.author: sidandrews
ms.reviewer: thvankra
ms.service: azure-cosmos-db
ms.subservice: apache-cassandra
ms.topic: overview
ms.date: 07/22/2025
ai-usage: ai-generated
appliesto:
  - ✅ Apache Cassanda
---

# What is Azure Cosmos DB for Apache Cassandra?

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

Azure Cosmos DB is a fully managed and serverless NoSQL database for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it's ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL data.

Azure Cosmos DB for Apache Cassandra is a fully managed NoSQL database service that enables you to run Cassandra workloads in the cloud with minimal changes to your application code. This API supports the Cassandra Query Language (CQL) and is compatible with existing Cassandra drivers and tools, making it easy to migrate or extend your applications without rearchitecting.

## Data

The API for Cassandra is designed for applications that require scalable, distributed storage of wide-column data. It supports tables with flexible schemas, allowing you to store and query large volumes of structured and semi-structured data. Each table consists of rows and columns, with support for partition and clustering keys to optimize data distribution and query performance. This model is ideal for time series, sensor data, user profiles, and other scenarios where high write throughput and fast lookups are important.

## Features

Every Azure Cosmos DB compatibility API offers a robust set of features to help you build modern, scalable applications. Key features of the API for Cassandra include:

- **Wire protocol compatibility**: Use your existing Cassandra drivers, software development kits (SDKs), and tools with minimal changes—often just updating the connection string.

- **Fully managed service**: Azure Cosmos DB handles infrastructure, patching, scaling, and backups, so you can focus on your application.

- **Elastic scalability**: Instantly scale throughput and storage across regions to meet the needs of your workload, with predictable performance.

- **Global distribution**: Distribute your data across any Azure region for low-latency access and high availability.

- **Automatic indexing**: All data is indexed by default, enabling fast queries without manual index management.

- **Change feed support**: Access a persistent change log for event sourcing and real-time analytics scenarios.

- **Tunable consistency levels**: Choose from five consistency levels to balance performance and data consistency for your application.

- **Enterprise-grade security**: Benefit from encryption at rest and in transit, IP firewall, audit logs, and compliance certifications.

## Common scenarios

The API for Cassandra is well-suited for applications that require high write throughput, flexible data models, and global scale. Common use cases include:

- **IoT and time series data**: Store and analyze large volumes of sensor or event data with high write rates and efficient queries.

- **User profile and personalization**: Manage user data, preferences, and activity logs for web and mobile applications.

- **Catalogs and inventory**: Track product catalogs, inventory levels, and order histories in retail and supply chain solutions.

- **Real-time analytics**: Power dashboards and analytics applications that require fast ingestion and querying of operational data.

## Azure Managed Instance for Apache Cassandra

For some workloads, adapting to Azure Cosmos DB for Cassandra can be a challenge due to differences in behavior or configuration from the native platform. This constraint is especially applicable for lift-and-shift migrations. Azure Managed Instance for Apache Cassandra is a first-party Azure service for hosting and maintaining pure open-source Apache Cassandra clusters with full native platform compatibility.

For more information, see [Azure Managed Instance for Apache Cassandra](../../managed-instance-apache-cassandra/introduction.md)

## Next step

- [Start using Azure Cosmos DB for Apache Cassandra](quickstart-python.md)
