---
title: Introduction/Overview
titleSuffix: Azure Cosmos DB for MongoDB (vCore)
description: Learn about vCore-based Azure Cosmos DB for MongoDB, a fully managed MongoDB-compatible database for building modern applications with a familiar architecture.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb-vcore
ms.custom:
  - ignite-2023
ms.topic: overview
ms.date: 06/11/2025
---

# What is Azure Cosmos DB for MongoDB (vCore architecture)?

Azure Cosmos DB for MongoDB in vCore architecture provides developers with a fully managed MongoDB-compatible database service for building modern applications with a familiar architecture. With Azure Cosmos DB for MongoDB (vCore), developers can enjoy the benefits of native Azure integrations, low total cost of ownership (TCO), and the familiar vCore architecture when migrating existing applications or building new ones.

## Build AI-Driven Applications with a Single Database Solution

Azure Cosmos DB for MongoDB (vCore) empowers generative AI applications with an integrated **vector database**. This enables efficient indexing and querying of data by characteristics for advanced use cases such as generative AI, without the complexity of external integrations. Unlike MongoDB Atlas and similar platforms, Azure Cosmos DB for MongoDB (vCore) keeps all original data and vector data within the database, ensuring simplicity and security. Even our free tier offers this capability, making sophisticated AI features accessible without additional cost.


## Effortless integration with the Azure platform

Azure Cosmos DB for MongoDB (vCore) provides a comprehensive and integrated solution for resource management, making it easy for developers to seamlessly manage their resources using familiar Azure tools. The service features deep integration into various Azure products, such as Azure Monitor and Azure CLI. This deep integration ensures that developers have everything they need to work efficiently and effectively.

Developers can rest easy knowing that they have access to one unified support team for all their services, eliminating the need to juggle multiple support teams for different services.

## Low total cost of ownership (TCO)

Azure Cosmos DB for MongoDB's scalable architecture is designed to deliver the best performance and cost efficiency for your workloads. Visit the [pricing page](https://azure.microsoft.com/pricing/details/cosmos-db/) to learn more about pricing for each cluster tier or price out a cluster in the Azure portal. With optional [in-region high availability (HA)](./high-availability.md), there's no need to pay for resources you don't need for workloads such as development and testing. With HA disabled, cost savings are passed on to you in the form of a reduced per-hour cost.

Here are the current tiers for the service:

| Cluster tier | vCPUs | RAM | Base storage |
| --- | --- | --- | --- |
| M10  | 1  | 2 GiB   | 32 GB  |  
| M20  | 2  | 4 GiB   | 32 GB  |  
| M25  | 2 burstable | 8 GB   | 32 GB  |  
| M30  | 2  | 8 GB   | 128 GB |  
| M40  | 4  | 16 GB  | 128 GB |  
| M50  | 8  | 32 GB  | 128 GB |  
| M60  | 16 | 64 GB  | 128 GB |  
| M80  | 32 | 128 GB | 128 GB |  
| M200 | 64 | 256 GB | 128 GB |  
| M200 Autoscale | Up to 64 | Up to 256 GB | 128 GB | 
| M300 | 48 | 324 GB | 128 GB |  
| M400 | 64 | 432 GB | 128 GB |  
| M600 | 80 | 640 GB | 128 GB |  

Azure Cosmos DB for MongoDB (vCore) is organized into easy to understand cluster tiers based on vCPUs, RAM, and attached storage. These tiers make it easy to lift and shift your existing workloads or build new applications.

## Flexibility for developers

Cosmos DB for MongoDB (vCore) is built with flexibility for developers in mind. The service offers high capacity vertical and horizontal scaling with no shard key required until the database surpasses TBs. The service also supports automatically sharding existing databases with no downtime. Developers can easily scale their clusters up or down, vertically and horizontally, all with no downtime, to meet their needs.

## Next steps

- Read more about [feature compatibility with MongoDB](compatibility.md).
- Review options for [migrating from MongoDB to Azure Cosmos DB for MongoDB (vCore)](migration-options.md)
- Get started by [creating an account](quickstart-portal.md).
