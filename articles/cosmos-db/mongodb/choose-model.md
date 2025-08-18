---
title: Choose between RU-based and vCore-based models
titleSuffix: Azure Cosmos DB for MongoDB
description: Learn how to choose between RU-based and vCore-based models in Azure Cosmos DB for MongoDB. Compare benefits and find the best fit for your workload. Start optimizing now.
author: gahl-levy
ms.author: gahllevy
ms.service: azure-cosmos-db
ms.subservice: mongodb
ms.topic: concept
ms.date: 08/21/2025
---

# RU-based and vCore-based models in Azure Cosmos DB for MongoDB

Azure Cosmos DB for MongoDB offers RU-based and vCore-based models for building scalable, cloud-native applications. This article compares these models and helps you select the best option for your workload and business needs.

## Choose between vCore-based and RU-based models

Here are a few key factors to help you decide which is the right option for you.

### When to choose vCore-based

- You're migrating (lift & shift) an existing MongoDB workload or building a new MongoDB application.
- Your workload has more long-running queries, complex aggregation pipelines, distributed transactions, joins, etc.
- You prefer high-capacity vertical and horizontal scaling with familiar vCore-based cluster tiers such as M30, M40, M50, and more.
- You're running applications requiring 99.995% availability.
- You need native support for storing and searching vector embeddings.

### When to choose RU-based

- You're building new cloud-native MongoDB apps or refactoring existing apps for cloud-native benefits.
- Your workload has more point reads (fetching a single item by its _id and shard key value) and few long-running queries and complex aggregation pipeline operations.
- You want limitless horizontal scalability, instantaneous scale up, and granular throughput control.
- You're running mission-critical applications requiring industry-leading 99.999% availability.

## Resource and billing differences

The vCore and RU services have different architectures with important billing differences.

### vCore-based resources and billing

- You'd like dedicated instances that utilize preset CPU, memory, and storage resources, which can dynamically scale to suit your needs.
- You prefer to pay a consistent flat fee based on compute (CPU, memory, and the number of nodes) and storage.

### RU-based resources and billing

- You'd like a multitenant service that instantly allocates resources to your workload, aligning with storage and throughput requirements. In this option, throughput is based on [request units (RUs)](../request-units.md).
- You prefer to pay fixed (standard provisioned throughput) or variable (autoscale) fees corresponding to Request Units (RUs) and consumed storage.

  > [!NOTE]
  > RU charges depend on the selected model: provisioned throughput (standard or autoscale) or serverless.

## Related content

- [Get started with Azure Cosmos DB for MongoDB vCore](./vcore/quickstart-portal.md)
- [Get started with Azure Cosmos DB for MongoDB RU](./quickstart-python.md)
