---
title: Dynamic Scaling (Per-region and per-partition autoscale)
titleSuffix: Azure Cosmos DB
description: Configure autoscale in Azure Cosmos DB for uneven workload patterns by customizing autoscale for specific regions or partitions.
author: rakhithejraj
ms.author: rakhithejraj
ms.reviewer: sidandrews
ms.service: cosmos-db
ms.custom:
  - Fabriccon Sep2024
ms.topic: conceptual
ms.date: 09/25/2024
# CustomerIntent: As a database adminstrator, I want to fine tune autoscaler for specific regions or partitions so that I can balance an uneven workload.
---

# Dynamic Scaling (Per-region and per-partition autoscale)

[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

Azure Cosmos DB autoscale by default scales workloads based on the most active region and partition. For nonuniform workloads that have different workload patterns across regions and partitions, this scaling can cause unnecessary scale-ups. With this improvement to autoscale, also known as "dynamic scaling," the per region and per partition autoscale feature now allows your workloads’ regions and partitions to scale independently based on usage.

Dynamic scaling is recommended for autoscale workloads that are nonuniform across regions and partitions. This feature allows you to save costs if you often experience hot partitions and/or have multiple regions. When enabled, dynamic scaling applies to all autoscale resources in the account.

## Use cases

- Database workloads that have a highly trafficked primary region and a secondary passive region for disaster recovery.
  - With dynamic scaling, you can now save on costs as the secondary region independently and automatically scales down while idle. The secondary regions also automatically scales-up as it becomes active and while handling write replication from the primary region.
- Multi-region database workloads.
  - These workloads often observe uneven distribution of requests across regions due to natural traffic growth and dips throughout the day. For example, a database might be active during business hours across globally distributed time zones.

## Example

For example, if we have a collection with **1000** RU/s and **2** partitions, each partition can go up to **500** RU/s. For one hour of activity, the utilization would look like this:

| Region | Partition | Throughput | Utilization | Notes |
| --- | --- | --- | --- | --- |
| Write | P1 | <= 500 RU/s | 100% | 500 RU/s consisting of 50 RU/s used for write operations and 450 RU/s for read operations. |
| Write | P2 | <= 200 RU/s | 40% | 200 RU/s consisting of all read operations. |
| Read | P1 | <= 150 RU/s | 30% | 150 RU/s consisting of 50 RU/s used for writes replicated from the write region. 100 RU/s are used for read operations in this region. |
| Read | P2 | <= 50 RU/s | 10% | |

Because all partitions are scaled uniformly based on the hottest partition, both the write and read regions are scaled to 1000 RU/s, making the total RU/s as much as **2000 RU/s**.

With dynamic scaling, you can optimize your throughput. The total consumption would be **900 RU/s** as each partition or region's throughput is scaled independently and measured per hour using the same scenario.

## Get started

Dynamic scaling is enabled by default for all Azure Cosmos DB accounts created after **September 25, 2024**. For customers who wish to enable this feature for their older accounts can do so [programmatically](https://review.learn.microsoft.com/en-us/azure/cosmos-db/autoscale-faq?branch=pr-en-us-165&tabs=azure-powerShell#how-can-i-enable-dynamic-autoscale-on-an-account-programatically-) through Azure PowerShell/CLI/Rest API or from the features pane of Azure portal as shown below:

1. Navigate to your Azure Cosmos DB account in the [Azure portal](https://portal.azure.com).
1. Navigate to the **Features** page.
1. Locate and enable the **Dynamic Scaling (Per Region and Per Partition Autoscale)** feature.

    :::image type="content" source="media/autoscale-per-partition-region/enable-feature.png" lightbox="media/autoscale-per-partition-region/enable-feature.png" alt-text="Screenshot of the 'Dynamic Scaling (Per Region and Per Partition Autoscale)' feature in the Azure portal.":::

    > [!IMPORTANT]
    > The feature is enabled at the account level, so all autoscale containers and shared throughput databases within the account will automatically have this capability applied. Enabling this feature does not affect resources in the account that are using manual throughput. Manual resources will need to be changed to autoscale to take advantage of dynamic scaling. Enabling this feature has zero downtime or performance impact. This feature is not applicable for serverless accounts

1. Below 3 metrics are used to understand the dynamic scaling behaviour better:

    |Metric Name|Definition|Use Case|
    |-------------|------|-------|
    |Autoscaled RU|Shows the dynamically scaled provisioned throughput at each partiion and region level only for dynamic autosacle enabled accounts.|Use this metric to verify if the paritions and regions independently scale based on their actual usage.|
    |Provisioned Throughput|Shows the static or dynamically scaled provisioned throughput.|Use this metric to verify that the provisioned throughput matches the workload's needs.|
    |Normalized RU Consumption|This metric represents the ratio of consumed RU/s to provisioned RU/s at each partition and region level.|Use this metric to provide insights into whether the provisioned throughput is under or over-utilized.|

    Use [Azure Monitor metrics](monitor-reference.md#supported-metrics-for-microsoftdocumentdbdatabaseaccounts) - `Autoscaled RU` to analyze how the new autoscaling is applied across partitions and regions. Filter to your desired database account and container, then filter or split by the `Physical PartitionID` metric. This metric shows all partitions across their various regions.

    Then, use `Normalized RU Consumption` to see how partitions and regions scale independently. With dynamic scaling, Normalized RU Consumption metric reflects RU/s consumed in secondary regions due to write replication in addition to the read/write RU/s and customers have to provision the RU/s accordingly. You can use the `Provisioned Throughput` metric to see what throughput value is emitted. With dynamic scaling, the Provisioned Throughput metric reflects the sum of each partition’s highest RU/s scaled to within the hour. Because of the hour boundary, the value resets at the start of each hour. 





