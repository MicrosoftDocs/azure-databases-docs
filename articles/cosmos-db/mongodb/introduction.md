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

Azure Cosmos DB is a fully managed and serverless NoSQL database for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it is ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL data.

<!-- COPILOT: Don't edit above this line -->

It offers single-digit millisecond response times, automatic and instant scalability, and guaranteed speed at any scale. It's the database that ChatGPT relies on to [dynamically scale](../introduction.md) with high reliability and low maintenance.

Azure Cosmos DB for MongoDB makes it easy to use Azure Cosmos DB as if it were a MongoDB database. You can use your existing MongoDB skills and continue to use your favorite MongoDB drivers, SDKs, and tools by pointing your application to the connection string for your account using the API for MongoDB. 

Azure Cosmos DB for MongoDB provides a service-level agreement (SLA) that covers the full stack: the database and the underlying infrastructure, unlike third-party MongoDB services such as MongoDB Atlas, which only cover the database and exclude services, hardware, or software provided by the cloud platform.

> [!VIDEO https://learn-video.azurefd.net/vod/player?id=234381e8-24dd-4692-bb70-596c97959216]

## Cosmos DB for MongoDB benefits

Cosmos DB for MongoDB has numerous benefits compared to other MongoDB service offerings such as MongoDB Atlas. 

[A fully managed MongoDB-compatible service](./ru/introduction.md) with flexible scaling using [Request Units (RUs)](../request-units.md). Designed for cloud-native applications.

- **Instantaneous scalability**: With the [autoscale](../provision-throughput-autoscale.md) feature, your database scales instantaneously with zero warmup period. Other MongoDB offerings such as MongoDB Atlas can take hours to scale up and up to days to scale down.

- **Automatic and transparent sharding**: The API for MongoDB manages all of the infrastructure for you. This management includes sharding and optimizing the number of shards. Other MongoDB offerings, such as MongoDB Atlas, require you to specify and manage sharding to horizontally scale. This automation gives you more time to focus on developing applications for your users.

- **Five 9's of availability**: [99.999% availability](../high-availability.md) is easily configurable to ensure your data is always there for you.

- **Active-active database**: Unlike MongoDB Atlas, Cosmos DB for MongoDB supports active-active across multiple regions. Databases can span multiple regions, with no single point of failure for *writes and reads for the same data*. MongoDB Atlas global clusters only support active-passive deployments for writes for the same data.  

- **Cost-efficient, granular, unlimited scalability**: Sharded collections can scale to any size, unlike other MongoDB service offerings. The Azure Cosmos DB platform can scale in increments as small as 1/100th of a VM due to its architecture. This scalability means that you can scale your database to the exact size you need, without paying for unused resources.

- **Real-time analytics (HTAP) at any scale**: Run analytics workloads against your transactional MongoDB data in real time with no effect on your database. This analysis is fast and inexpensive, due to the cloud native analytical columnar store being utilized, with no ETL pipelines. Easily create Power BI dashboards, integrate with Azure Machine Learning and Azure AI services, and bring all of your data from your MongoDB workloads into a single data warehousing solution. Learn more about the [Azure Synapse Link](../synapse-link.md).

- **Serverless deployments**: Cosmos DB for MongoDB offers a [serverless capacity mode](../serverless.md). With [serverless](../serverless.md), you're only charged per operation, and don't pay for the database when you don't use it.

> [!TIP]
> For an in-depth comparison of each architecture to help choose which one is right for you, see [Choose your model](./choose-model.md).

Azure Cosmos DB for MongoDB in Request Unit architecture makes it easy to use Azure Cosmos DB as if it were a MongoDB database. You can use your existing MongoDB skills and continue to use your favorite MongoDB drivers, SDKs, and tools. Azure Cosmos DB for MongoDB (RU) is built on top of the Cosmos DB platform. This service takes advantage of Azure Cosmos DB's global distribution, elastic scale, and enterprise-grade security.

> [!VIDEO https://learn-video.azurefd.net/vod/player?id=234381e8-24dd-4692-bb70-596c97959216]

> [!TIP]
> Want to try the Azure Cosmos DB for MongoDB with no commitment? Create an Azure Cosmos DB account using [Try Azure Cosmos DB](../../try-free.md) for free.

## Azure Cosmos DB for MongoDB (RU) benefits

Cosmos DB for MongoDB (RU) has numerous benefits compared to other MongoDB service offerings such as MongoDB Atlas:

- **Instantaneous scalability**: With the [Autoscale](../../provision-throughput-autoscale.md) feature, your database scales instantaneously with zero warmup period. Other MongoDB offerings such as MongoDB Atlas can take hours to scale up and up to days to scale down.

- **Automatic and transparent sharding**: The API for MongoDB manages all of the infrastructure for you. This management includes sharding and optimizing the number of shards. Other MongoDB offerings such as MongoDB Atlas, require you to specify and manage sharding to horizontally scale. This automation gives you more time to focus on developing applications for your users.

- **Five 9's of availability**: [99.999% availability](../../high-availability.md) is easily configurable to ensure your data is always there for you.

- **Active-active database**: Unlike MongoDB Atlas, Azure Cosmos DB for MongoDB (RU) supports active-active across multiple regions. Databases can span multiple regions, with no single point of failure for **writes and reads for the same data**. MongoDB Atlas global clusters only support active-passive deployments for writes for the same data.  
- **Cost efficient, granular, unlimited scalability**: Sharded collections can scale to any size, unlike other MongoDB service offerings. The Azure Cosmos DB platform can scale in increments as small as 1/100th of a VM due to its architecture. This support means that you can scale your database to the exact size you need, without paying for unused resources.

- **Real time analytics (HTAP) at any scale**: Run analytics workloads against your transactional MongoDB data in real time with no effect on your database. This analysis is fast and inexpensive, due to the cloud native analytical columnar store being utilized, with no ETL pipelines. Easily create Power BI dashboards, integrate with Azure Machine Learning and Azure AI services, and bring all of your data from your MongoDB workloads into a single data warehousing solution. Learn more about the [Azure Synapse Link](../../synapse-link.md).

- **Serverless deployments**: Azure Cosmos DB for MongoDB (RU) offers a [serverless capacity mode](../../serverless.md). With [Serverless](../../serverless.md), you're only charged per operation, and don't pay for the database when you don't use it.

- **Free Tier**: With Azure Cosmos DB free tier, you get the first 1000 RU/s and 25 GB of storage in your account for free forever, applied at the account level. Free tier accounts are automatically [sandboxed](../../limit-total-account-throughput.md) so you never pay for usage.

- **Free 7 day Continuous Backups**: Azure Cosmos DB for MongoDB (RU) offers free seven day continuous backups for any amount of data. This retention means that you can restore your database to any point in time within the last seven days.

- **Upgrades take seconds**: All API versions are contained within one codebase, making version changes as simple as [flipping a switch](../upgrade-version.md), with zero downtime.

- **Role Based Access Control**: With Azure Cosmos DB for MongoDB (RU), you can assign granular roles and permissions to users to control access to your data and audit user actions- all using native Azure tooling.

- **In-depth monitoring capabilities**: Azure Cosmos DB for MongoDB (RU) integrates natively with [Azure Monitor](/azure/azure-monitor/overview) to provide in-depth monitoring capabilities.

## How Cosmos DB for MongoDB works

Azure Cosmos DB for MongoDB (RU) implements the wire protocol for MongoDB. This implementation allows transparent compatibility with MongoDB client SDKs, drivers, and tools. Azure Cosmos DB doesn't host the MongoDB database engine. Any MongoDB client driver compatible with the API version you're using can connect with no special configuration.

> [!IMPORTANT]
> This article describes a feature of Azure Cosmos DB that provides wire protocol compatibility with MongoDB databases. Microsoft does not run MongoDB databases to provide this service. Azure Cosmos DB is not affiliated with MongoDB, Inc.

### Choosing a server version

All versions run on the same codebase, making upgrades a simple task that can be completed in seconds with zero downtime. Azure Cosmos DB simply flips a few feature flags to go from one version to another.  The feature flags also enable continued support for old API versions such as 4.0 and 3.6. You can choose the server version that works best for you.

Not sure if your workload is ready? Use the automatic [premigration assessment](../pre-migration-steps.md) to determine if you're ready to migrate to Cosmos DB for MongoDB in RU or vCore architecture.

## What you need to know to get started

With the RU model, you aren't billed for virtual machines in a cluster. [Pricing](../../how-pricing-works.md) is based on throughput in request units (RUs) configured on a per database or per collection basis. The first 1000 RUs per second are free with [Free Tier](../../free-tier.md).

There are three ways to deploy the Cosmos DB for MongoDB:

- [Provisioned throughput](../../set-throughput.md): Set a RU/sec number and change it manually. This model best fits consistent workloads.

- [Autoscale](../../provision-throughput-autoscale.md): Set an upper bound on the throughput you need. Throughput instantly scales to match your needs. This model best fits workloads that change frequently and optimizes their costs.

- [Serverless](../../serverless.md): Only pay for the throughput you use, period. This model best fits dev/test workloads.

Sharded cluster performance is dependent on the shard key you choose when creating a collection. Choose a shard key carefully to ensure that your data is evenly distributed across shards.

## How Azure Cosmos DB for MongoDB works

Cosmos DB for MongoDB implements the wire protocol for MongoDB. This implementation allows transparent compatibility with MongoDB client SDKs, drivers, and tools. Azure Cosmos DB doesn't host the MongoDB database engine. Any MongoDB client driver compatible with the API version you're using should be able to connect, with no special configuration.

<!-- COPILOT: Don't edit below this line -->

> [!IMPORTANT]
> This article various features of Azure Cosmos DB for MongoDB that provides wire protocol compatibility with MongoDB databases. Microsoft doesn't run MongoDB databases to provide this service. Azure Cosmos DB isn't affiliated with MongoDB, Inc.

## Azure Cosmos DB for MongoDB vCore

For some workloads, adapting to Azure Cosmos DB for MongoDB can be a challenge due to differences in behavior or configuration from the native platform. This is especially true for lift-and-shift migrations. Azure Cosmos DB for MongoDB vCore is a first-party Azure service with dedicated instances for new and existing MongoDB apps. This architecture offers a familiar vCore architecture for MongoDB users, instantaneous scaling, and seamless native integration with various Azure services.

For more information, see [Azure Cosmos DB for MongoDB vCore](vcore/introduction.md)

## Next step

- [Start using Azure Cosmos DB for MongoDB](quickstart-nodejs.md)
