---
title: Compare Provisioned Throughput and Serverless
description: Learn about how to choose between provisioned throughput and serverless for your workload.
author: markjbrown
ms.author: mjbrown
ms.service: azure-cosmos-db
ms.topic: concept-article
ms.date: 07/25/2025
ms.custom:
  - cosmos-db-video
  - build-2025
appliesto:
  - ✅ NoSQL
  - ✅ MongoDB
  - ✅ Apache Cassandra
  - ✅ Apache Gremlin
  - ✅ Table
---

# How to choose between provisioned throughput and serverless

Azure Cosmos DB is available in two different capacity modes: [provisioned throughput](set-throughput.md) and [serverless](serverless.md). You can perform the exact same database operations in both modes, but the way you get billed for these operations is radically different.

The following video explains the core differences between these modes and how they fit different types of workloads:

>
> [!VIDEO https://www.youtube.com/embed/XRBOy1F7eZw]

## Detailed comparison

| Criteria | Provisioned throughput | Serverless |
| --- | --- | --- |
| Best suited for | Workloads with sustained traffic requiring predictable performance | Workloads with intermittent or unpredictable traffic and low average-to-peak traffic ratio |
| How it works | For each of your containers, you configure some amount of provisioned throughput expressed in Request Units per second (RU/s). Every second, this quantity of [Request Units](request-units.md) is available for your database operations. Provisioned throughput can be updated manually or adjusted automatically with [autoscale](provision-throughput-autoscale.md). | You run your database operations against your containers without having to configure any previously provisioned capacity. |
| Geo-distribution | Available (unlimited number of Azure regions) | Unavailable (serverless accounts can only run in a single Azure region) |
| Performance | Less than 10-ms latency for point-reads and writes covered by SLA | Less than 10-ms latency for point-reads and less than 30 ms for writes covered by SLO |
| Billing model | Billing is done on a per-hour basis for the RU/s provisioned, regardless of how many RUs were consumed. | Billing is done on a per-hour basis for the number of RUs consumed by your database operations. |

Maximum RU/s availability is dependent on data stored in the container. To learn more, see [Azure Cosmos DB serverless account performance](serverless-performance.md).

## Estimate your expected consumption

In some situations, it might be unclear whether provisioned throughput or serverless should be chosen for a given workload. To help with this decision, you can estimate your overall *expected consumption*, or the total number of RUs you might consume over a month. 

For more information, see [Estimate serverless costs](plan-manage-costs.md#estimating-serverless-costs).

**Example 1**: a workload is expected to burst to a maximum of 500 RU/s and consume a total of 20,000,000 RUs over a month.

- In provisioned throughput mode, you would configure a container with provisioned throughput at a quantity of 500 RU/s for a monthly cost of: `$0.008 * 5 * 730 = $29.20`
- In serverless mode, you would pay for the consumed RUs: `$0.25 * 20 = $5.00`

**Example 2**: a workload is expected to burst to a maximum of 500 RU/s and consume a total of 250,000,000 RUs over a month.

- In provisioned throughput mode, you would configure a container with provisioned throughput at a quantity of 500 RU/s for a monthly cost of: `$0.008 * 5 * 730 = $29.20`
- In serverless mode, you would pay for the consumed RUs: `$0.25 * 250 = $62.50`

These examples don't account for the storage cost, which is the same between the two modes.

> [!NOTE]
> The costs shown in the previous example are for demonstration purposes only. For the latest pricing information, see the [pricing page](https://azure.microsoft.com/pricing/details/cosmos-db/).

## Next steps

- [Introduction to provisioned throughput in Azure Cosmos DB](set-throughput.md)
- [Azure Cosmos DB serverless account type](serverless.md)
- [Request Units in Azure Cosmos DB](request-units.md)
