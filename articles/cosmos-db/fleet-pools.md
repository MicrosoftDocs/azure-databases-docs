---
title: Fleets Pools (Preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Pools manage throughput in Azure Cosmos DB fleets aimed at optimizing resource allocation for multitenant applications.
author: deborahc
ms.author: dech
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 05/07/2025
ai-usage: ai-assisted
show_latex: true
appliesto:
  - ✅ NoSQL
ms.custom:
  - build-2025
---

# Pools for Azure Cosmos DB fleets 

When using Azure Cosmos DB fleets, you can simplify your throughput management with **pools**. Pools allow you to create a shared pool of throughput request units per second (RU/s) at the fleetspace level that multiple resources can use RU/s from as needed. Because pools are a fleet feature, resources across different subscriptions and resource groups within the same fleetspace can share RU/s from a common pool. 

Pools are designed for **customers building multi-tenant applications** where isolation requirements often dictate that each tenant's data is stored in a separate database account, database, or container. Instead of overprovisioning throughput to accommodate peak throughput needs, pools let you create each tenant based on their typical workload. When tenants require more capacity due to spikes, they can draw from the shared pool. This approach helps you right-size individual tenant resources while maintaining performance and cost efficiency across your fleet. 

> [!IMPORTANT]
> Pooling is intended for multitenant applications and scenarios where there are a high number of tenants with different traffic patterns. In a pooling scenario, not all tenants are active at the same time. If you're running workload with a smaller number of tenants, or one where most tenants are 100% idle or 100% active, pooling might not provide more benefits.

## Concepts

- **Dedicated RU/s**: This throughput is the RU/s provisioned at the database or container level that are dedicated to that resource. These request units are guaranteed and ensure that each resource has a minimum level of guaranteed performance.  

    - There are always dedicated RU/s for resources within your database accounts set at the shared database or container level. These dedicated throughput allocations represent the RU/s already configured on your shared database or container level.

    - The entry point for dedicated RU/s is 100 – 1,000 autoscale RU/s. 

    - For autoscale, the dedicated RU/s refers to the autoscale max throughput, which is always guaranteed and available. 

- **Pool RU/s**: You can set pooled RU/s. Pooled RU/s are the total RU/s available within a fleetspace that any resource in its database accounts can use when dedicated RU/s are exceeded. 

Resources that surpass their **dedicated RU/s** allocation get throttled without the pooling feature. With pooling, they can scale beyond their dedicated limits by consuming more RU/s from the shared pool—ensuring better cost efficiency and performance for multitenant workloads.  

Dedicated RU/s are consumed first before drawing from the pool.

## Example scenario

Suppose you’re an independent software vendor (ISV) with 1,000 tenants, each with:

- One database account per tenant for security isolation across resources 

- One container per account 

- Autoscale provisioned between 100-1000 RU/s per container 

However, tenant activity is unpredictable:

- Most tenants use low RU/s most of the time 

- Peak demand per active tenant can reach 5000 RU/s 

### Without pooling 

- You must overprovision every container with 5000 RU/s to handle peak loads

- This solution results in wasted RU/s and unnecessary costs when tenants are idle

### With pooling 

- Containers primarily use dedicated RU/s (for example, 100-1,000 RU/s)

- The fleet has a separate throughput pool (for example, 100,000 – 500,000 RU/s) at the fleetspace level.

- Tenants can temporarily draw from the pool instead of getting throttled when it exceeds its dedicated RU/s

- Overprovisioning is prevented while ensuring tenants get the throughput they need when demand spikes

## How pooled throughput works

Pool RU/s are configured for autoscale by default. When you configure a pool within a fleetspace, you define a minimum throughput and a maximum throughput the pool can scale between. The maximum can be at most 10 times the minimum. For example, if you set the minimum throughput to 100,000 RU/s, you can set the maximum to any value up to 1,000,000 RU/s. 

Each hour, you're billed for the highest RU/s the pool scaled to within the hour for each region the pool is available in. If the pool is idle, you're billed for the minimum RU/s for each region.

## Configuration rules

Throughput pooling requires all database accounts in a **fleetspace** to have the **same regional configuration**. This means that accounts with different regions or different settings of single or multi-region write (general purpose vs business critical service tier) **cannot** share the same throughput pool. Pool RU/s are also not shared across regions.

Here are examples of allowed and unallowed configurations:

- Varying regional configurations
    - **Allowed**: Two accounts, both configured as single-region write in two distinct Azure regions.
    - **Allowed**: Two accounts, both configured as multi-region write in two distinct Azure regions.
    - **Not allowed**: One account, with single-region write but distributed to two distinct Azure regions. Another account, with single-region write, in a different single Azure region.
    - **Not allowed**: Two accounts, with global distribution configured for two different sets of regions.
- Varying service tiers
    - **Allowed**: Two accounts, both with multi-region write (business critical) configured in two separate Azure regions.
    - **Not allowed**: Two accounts, one with multi-region write and the other with single-region write.

> [!NOTE]
> Accounts must have the same underlying configuration of multi-region writes (business critical) or single-region writes (general purpose) to participate in the same pool.

## Monitoring consumption

In the preview, you can monitor the RU/s the pool scaled to via the `FleetspaceAutoscaledThroughput` metric available at the fleet level.

You can also monitor pooled RU/s consumption at the account level in Azure portal via Azure Monitor following these steps:

1. Navigate to your Azure Cosmos DB account's **Metrics** page in the Azure portal.

1. Filter to the database and container of interest.

1. Select the **Total Requests** metric. Then, split by **Capacity Type** to see whether requests were consuming from the pool or just from the resources' dedicated throughput. You can also determine how many request units were consumed from the throughput pool versus the dedicated RU/s provisioned for each resource using the **Total Request Units** metric.

:::image source="media/fleet-pools/azure-monitor-visualization.png" alt-text="Screenshot of the request unit visualization in Azure Monitor using the Azure portal.":::

## Default limitations

With the pooling feature, the total RU/s available for consumption to each physical partition is still subject to standard [physical partition limits](partitioning-overview.md#physical-partitions). Each **physical partition** has limits on how much extra RU/s it can draw from the pool. 

In the preview:

- A physical partition uses up to 5,000 extra RU/s from the pool in addition to its dedicated throughput.

- A physical partition’s total consumption of dedicated + pool RU/s can't exceed 10,000 RU/s total, even if more RU/s are available to use from the pool. 

- The maximum total RU/s a physical partition can consume while using pooling = $\min(5000+currentThroughput, 10000)$.

> [!TIP]
> You can use the metric `PhysicalPartitionThroughput` in Azure Monitor to determine how many dedicated RU/s are allocated to each physical partition.

## Related content

- [Fleets overview](fleet.md)
- [Fleet analytics](fleet-analytics.md)
