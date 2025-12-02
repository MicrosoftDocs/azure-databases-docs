---
title: Introduction/Overview
titleSuffix: Azure Cosmos DB for MongoDB
description: Learn how to use Azure Cosmos DB for MongoDB to store and query massive amounts of data using popular open-source drivers.
author: seesharprun
ms.author: sidandrews
ms.reviewer: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: overview
ms.date: 07/22/2025
ai-usage: ai-generated
appliesto:
  - ✅ MongoDB
---

# What is Azure Cosmos DB for MongoDB?

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

Azure Cosmos DB is a fully managed and serverless NoSQL database for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it's ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL data.

Azure Cosmos DB for MongoDB is a fully managed NoSQL database service that enables you to run MongoDB workloads in the cloud with minimal changes to your application code. This API supports the MongoDB wire protocol, so you can use your existing MongoDB drivers, software development kits (SDKs), and tools. You can connect to the API for MongoDB to interact with your data just as you would with a native MongoDB database.

## Data

The API for MongoDB is designed for document data models, allowing you to store and query JSON-like documents with flexible schemas. Collections can contain documents of varying structures, making it easy to evolve your application over time. This model is ideal for content management, catalogs, user profiles, and any scenario where you need to store and retrieve rich, hierarchical data.

## Features

Every Azure Cosmos DB compatibility API offers a robust set of features to help you build modern, scalable applications. Key features of the API for MongoDB include:

- **Wire protocol compatibility**: Use your existing MongoDB drivers, SDKs, and tools with minimal changes—often just updating the connection string.

- **Fully managed service**: Azure Cosmos DB handles infrastructure, patching, scaling, and backups, so you can focus on your application.

- **Elastic scalability**: Instantly scale throughput and storage to handle collections with millions of documents and high transaction rates.

- **Global distribution**: Distribute your data across any Azure region for low-latency access and high availability.

- **Automatic and transparent sharding**: Data is automatically partitioned and distributed for optimal performance and scale, with no manual sharding required.

- **Real-time analytics**: Run analytics workloads on your operational data without impacting transactional performance, using integrated features like Azure Synapse Link.

- **Tunable consistency levels**: Choose from five consistency levels to balance performance and data consistency for your application.

- **Enterprise-grade security**: Benefit from encryption at rest and in transit, role-based access control, audit logs, and compliance certifications.

## Common scenarios

The API for MongoDB is well-suited for applications that require flexible document storage, high availability, and global scale. Common use cases include:

- **Content management and catalogs**: Store and manage product catalogs, articles, or digital assets with flexible document structures.

- **User profiles and personalization**: Manage user data, preferences, and activity logs for web and mobile applications.

- **IoT and telemetry**: Ingest and analyze large volumes of device or sensor data in real time.

- **Real-time analytics and dashboards**: Power analytics applications that require fast ingestion and querying of operational data.

> [!IMPORTANT]
> This introduction reviews various features of Azure Cosmos DB for MongoDB that provides wire protocol compatibility with MongoDB databases. Microsoft doesn't run MongoDB databases to provide this service. Azure Cosmos DB isn't affiliated with MongoDB, Inc.

## Next step

- [Start using Azure Cosmos DB for MongoDB](quickstart-nodejs.md)
