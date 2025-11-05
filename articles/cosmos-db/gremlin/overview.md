---
title: Introduction/Overview
titleSuffix: Azure Cosmos DB for Apache Gremlin
description: Learn how to use Azure Cosmos DB for Apache Gremlin to store, query, and traverse massive graphs with the Gremlin graph query language of Apache TinkerPop.
author: seesharprun
ms.author: sidandrews
ms.reviewer: mansha
ms.service: azure-cosmos-db
ms.subservice: apache-gremlin
ms.topic: overview
ms.date: 07/22/2025
ai-usage: ai-generated
---

# What is Azure Cosmos DB for Apache Gremlin?

[!INCLUDE[Note - Recommended services](includes/note-recommended-services.md)]

Azure Cosmos DB is a fully managed and serverless NoSQL database for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it's ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL data.

Azure Cosmos DB for Apache Gremlin is a fully managed graph database service that enables you to store, query, and traverse large-scale graph data using the Gremlin query language. This API is built on the open-source Apache TinkerPop framework and is designed for applications that need to model and analyze complex relationships between data points. This API is designed for solutions such as social networks, recommendation engines, and connected devices.

## Data

The API for Gremlin is purpose-built for storing and managing property graph data. Property graphs consist of vertices (nodes) and edges (relationships), each of which can have an arbitrary number of key-value properties. This flexible structure allows you to represent highly connected data, such as people and their relationships, devices and their connections, or any network of entities and interactions. The API supports dynamic schemas, so you can evolve your graph structure as your application grows.

## Features

Every Azure Cosmos DB compatibility API offers a robust set of features to help you build modern, scalable applications. Key features of the API for Gremlin include:

- **Fully managed service**: No need to manage infrastructure, updates, or backups. Azure Cosmos DB handles all operational aspects, so you can focus on your application logic.

- **Elastic scalability**: Seamlessly scale storage and throughput to handle graphs with billions of vertices and edges. Data is automatically partitioned and distributed for high performance.

- **Global distribution**: Provides low-latency access and high availability for users worldwide by replicating your graph data across any Azure region.

- **Automatic indexing**: All properties on vertices and edges are indexed by default, enabling fast and flexible queries without manual index management.

- **Open-source compatibility**: The API is built on Apache TinkerPop, supports the Gremlin query language, and integrates with a wide ecosystem of tools and libraries.

- **Tunable consistency levels**: Choose from five well-defined consistency levels to balance performance, availability, and data consistency for your application needs.

- **Integrated security**: Benefit from enterprise-grade security features, including encryption at rest and in transit, role-based access control, and compliance certifications.

## Common scenarios

The API for Gremlin is ideal for scenarios where relationships between data points are as important as the data itself. Common use cases include:

- **Social networks and customer 360**: Model and analyze connections between people, their interests, and interactions to deliver personalized experiences and insights.

- **Recommendation engines**: Deliver real-time, personalized recommendations by combining information about users, products, and behaviors.

- **Geospatial and logistics**: Find optimal routes, analyze proximity, and manage networks of locations or assets for applications in transportation, logistics, and travel.

- **Internet of Things (IoT)**: Gain insights into system health and dependencies by representing and monitoring networks of devices, sensors, and their interactions.

> [!IMPORTANT]
> This introduction reviews various features of Azure Cosmos DB for Apache Gremlin that provides wire protocol compatibility with the Apache TinkerPop specification. Some features might differ from Apache TinkerPop. For more information, see [compatibility with Apache TinkerPop](support.md).
