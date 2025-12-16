---
title: Introduction/Overview
titleSuffix: Azure Cosmos DB for Table
description: Learn how to use Azure Cosmos DB for Table to store, manage, and query massive volumes of key-value typed NoSQL data.
author: seesharprun
ms.author: sidandrews
ms.reviewer: sasinnat
ms.service: azure-cosmos-db
ms.subservice: table
ms.topic: overview
ms.date: 07/22/2025
ai-usage: ai-generated
---

# What is Azure Cosmos DB for Table?

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

Azure Cosmos DB is a fully managed and serverless NoSQL database for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it's ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL data.

Azure Cosmos DB for Table is a fully managed NoSQL database service that enables you to store, manage, and query large volumes of key-value data using the familiar Azure Table storage APIs. This API is designed for applications that need scalable, high-performance storage for structured/nonrelational data. This API is also compatible with existing Azure Table Storage software development kits (SDKs) and tools.

## Data

The API for Table is optimized for storing and retrieving key-value and tabular data. Each table consists of entities (rows) identified by a unique combination of partition key and row key, with flexible properties for each entity. This model is ideal for scenarios such as device registries, user profiles, configuration data, and other applications that require fast lookups and simple queries over large datasets.

## Features

Every Azure Cosmos DB compatibility API offers a robust set of features to help you build modern, scalable applications. Key features of the API for Table include:

- **Wire protocol compatibility**: Use your existing Azure Table Storage SDKs and tools with minimal or no code changes.

- **Fully managed service**: Azure Cosmos DB handles infrastructure, patching, scaling, and backups, so you can focus on your application.

- **Elastic scalability**: Instantly scale throughput and storage to handle millions of operations per second and massive datasets.

- **Global distribution**: Distribute your tables across any Azure region for low-latency access and high availability.

- **Automatic indexing**: All properties are indexed by default, enabling fast queries without manual index management.

- **Tunable consistency levels**: Choose from five consistency levels to balance performance and data consistency for your application.

- **Enterprise-grade security**: Benefit from encryption at rest and in transit, role-based access control, audit logs, and compliance certifications.

## Common scenarios

The API for Table is well-suited for applications that require scalable, high-performance key-value storage. Common use cases include:

- **Device registries and IoT**: Store and manage metadata for millions of devices or sensors with fast lookups and updates.

- **User profiles and session data**: Manage user information, preferences, and session state for web and mobile applications.

- **Configuration and reference data**: Store application settings, lookup tables, and other reference data for fast access.

- **Audit logs and event tracking**: Capture and query large volumes of log or event data for monitoring and analytics.

## Next step

- [Start using Azure Cosmos DB for Table](quickstart-dotnet.md)
