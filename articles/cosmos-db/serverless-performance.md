---
title: Performance for the serverless account type
description: Learn more about performance for the Azure Cosmos DB serverless account type.
author: richagaur
ms.author: richagaur
ms.service: azure-cosmos-db
ms.custom: build-2023
ms.topic: best-practice
ms.date: 12/01/2022
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# Azure Cosmos DB serverless account performance

Azure Cosmos DB serverless resources have performance characteristics that are different than the characteristics of provisioned throughput resources. Serverless containers don't offer any guarantees of predictable throughput or latency. The maximum capacity of a serverless container is determined by the data that stored within it. The capacity varies with data size.

## Request unit changes

An Azure Cosmos DB serverless account provides a maximum throughput of 5,000 request units per second (RU/s) for a single container. If the data within the container exceeds the capacity of a single physical partition, the container's throughput scales linearly with the number of partitions. The throughput can be calculated using the following formula:

```
Throughput (RU/s) = Number of partitions * 5,000
```

> [!NOTE]
> The numbers that are described in this article represent the maximum RU/s capacity that's available to a serverless container. However, it's important to note that if you choose a serverless account type, you have no assurances of predictable throughput or latency. If your container requires these types of guarantees, we recommend that you choose to create a provisioned throughput account type instead of a serverless account.

## Next steps

- Learn more about the Azure Cosmos DB [serverless](serverless.md) option.
- Learn more about [request units](request-units.md).
- Review how to [choose between provisioned throughput and serverless](throughput-serverless.md).
