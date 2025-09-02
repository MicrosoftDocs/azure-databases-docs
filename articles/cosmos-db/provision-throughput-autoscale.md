---
title: Create Azure Cosmos DB containers and databases in autoscale or dynamic scaling mode.
description: Learn about the benefits, use cases, and how to provision Azure Cosmos DB databases and containers in autoscale as well as dynamic scaling mode.
author: kirillg
ms.author: kirillg
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 09/03/2025
ai-usage: ai-assisted
---

# Create Azure Cosmos DB containers and databases with autoscale throughput
[!INCLUDE[NoSQL, MongoDB, Cassandra, Gremlin, Table](includes/appliesto-nosql-mongodb-cassandra-gremlin-table.md)]

In Azure Cosmos DB, you can configure either standard (manual) or autoscale provisioned throughput on your databases and containers. Autoscale provisioned throughput in Azure Cosmos DB allows you to **scale the throughput (RU/s) of your database or container automatically and instantly**. 

Autoscale provisioned throughput is well suited for mission-critical workloads that have variable or unpredictable traffic patterns, and require SLAs on high performance and scale. Autoscale by default scales workloads based on the most active region and partition. For nonuniform workloads that have different workload patterns across regions and partitions, this scaling can cause unnecessary scale-ups. **Dynamic scaling or dynamic autoscale** is an enhancement to autoscale provisioned throughout that helps scaling of such nonuniform workloads independently based on usage, at per region and per partition level. Dynamic scaling allows you to save cost if you often experience hot partitions and/or have multiple regions. 

## Benefits of autoscale

Azure Cosmos DB databases and containers that are configured with autoscale provisioned throughput have the following benefits:

* **Simple:** Autoscale removes the complexity of managing RU/s with custom scripting or manually scaling capacity. 

* **Scalable:** Databases and containers automatically scale the provisioned throughput as needed. There's no disruption to client connections, applications, or to Azure Cosmos DB SLAs.

* **Cost-effective:** Autoscale helps optimize your RU/s usage and cost usage by scaling down when not in use. You only pay for the resources that your workloads need on a per-hour basis. Of all hours in a month, if you set autoscale max RU/s(Tmax) and use the full amount Tmax for 66% of the hours or less, you can save with autoscale. In addition with dynamic scaling, adding a secondary region for high availability is more cost-efficient as each region and partition scales independently based on actual usage. To learn more, see the [how to choose between standard (manual) and autoscale provisioned throughput](how-to-choose-offer.md) article.

* **Highly available:** Databases and containers using autoscale use the same globally distributed, fault-tolerant, highly available Azure Cosmos DB backend to ensure data durability and high availability.

## Use cases of autoscale

The use cases of autoscale include:

* **Variable or unpredictable workloads:** When your workloads have variable or unpredictable spikes in usage, autoscale helps by automatically scaling up and down based on usage. Examples include retail websites that have different traffic patterns depending on seasonality; IOT workloads that have spikes at various times during the day; line of business applications that see peak usage a few times a month or year, and more. With autoscale, you no longer need to manually provision for peak or average capacity. 

* **New applications:** If you're developing a new application and not sure about the throughput (RU/s) you need, autoscale makes it easy to get started. You can start with the autoscale entry point of 100 - 1000 RU/s, monitor your usage, and determine the right RU/s over time.

* **Infrequently used applications:** If you have an application, which is only used for a few hours several times a day, week, or month—such as a low-volume application/web/blog site. Autoscale adjusts the capacity to handle peak usage and scales down when it's over. 

* **Development and test workloads:** If you or your team use Azure Cosmos DB databases and containers during work hours, but don't need them on nights or weekends, autoscale helps save cost by scaling down to a minimum when not in use. 

* **Scheduled production workloads/queries:** If you have a series of scheduled requests, operations, or queries that you want to run during idle periods, you can do that easily with autoscale. When you need to run the workload, the throughput automatically scales to needed value and scales down afterward. 

Building a custom solution to these problems not only requires an enormous amount of time, but also introduces complexity in your application's configuration or code. Autoscale enables the above scenarios out of the box and removes the need for custom or manual scaling of capacity. 

## Use cases of dynamic scaling

The use cases of dynamic scaling include:

- Database workloads that have a highly trafficked primary region and a secondary passive region for disaster recovery.
  - With dynamic scaling, achieving high availability with multiple regions is more cost effective. The secondary region independently and automatically scales down while idle. The secondary region also automatically scales up as it becomes active and while handling write replication traffic from the primary region.
- Multi-region database workloads.
  - These workloads often observe uneven distribution of requests across regions due to natural traffic growth and dips throughout the day. For example, a database might be active during business hours across globally distributed time zones.

## How autoscale provisioned throughput works

When configuring containers and databases with autoscale, you specify the maximum throughput `Tmax` required. Azure Cosmos DB scales the throughput `T` such `0.1*Tmax <= T <= Tmax`. For example, if you set the maximum throughput to 20,000 RU/s, the throughput scales between 2000 to 20,000 RU/s. Because scaling is automatic and instantaneous, at any point in time, you can consume up to the provisioned `Tmax` with no delay. 

Each hour, you're billed for the highest throughput `T` the system scaled to within the hour. When dynamic scaling is enabled, scaling is based on the RU/s usage at each physical partition and region. As each partition and region scale independently, this can lead to cost savings for nonuniform workloads, as unnecessary scale-ups are avoided.

The entry point for autoscale maximum throughput `Tmax` starts at 1000 RU/s, which scales between 100 - 1000 RU/s. You can set `Tmax` in increments of 1000 RU/s and change the value at any time.  

For example, if we have a collection with **1000** RU/s and **2** partitions, each partition can go up to **500** RU/s. For one hour of activity, the utilization would look like this:

| Region | Partition | Throughput | Utilization | Notes |
| --- | --- | --- | --- | --- |
| Write | P1 | <= 500 RU/s | 100% | 500 RU/s consisting of 50 RU/s used for write operations and 450 RU/s for read operations. |
| Write | P2 | <= 200 RU/s | 40% | 200 RU/s consisting of all read operations. |
| Read | P1 | <= 150 RU/s | 30% | 150 RU/s consisting of 50 RU/s used for writes replicated from the write region. 100 RU/s are used for read operations in this region. |
| Read | P2 | <= 50 RU/s | 10% | |

Without dynamic scaling, all partitions are scaled uniformly based on the hottest partition. In this example, because the hottest partition had 100% utilization, all partitions in both the write and read regions are scaled to 1000 RU/s, making the total RU/s scaled to **2000 RU/s**.

With dynamic scaling, because each partition and region's throughput is scaled independently, the total RU/s scaled to would be **900 RU/s**, which better reflects the actual traffic pattern and lowers costs.

## Enabling autoscale on existing resources

Use the [Azure portal](how-to-provision-autoscale-throughput.md#enable-autoscale-on-existing-database-or-container), [CLI](how-to-provision-autoscale-throughput.md#azure-cli) or [PowerShell](how-to-provision-autoscale-throughput.md#azure-powershell) to enable autoscale on an existing database or container. You can switch between autoscale and standard (manual) provisioned throughput at any time. For more information, refer this [documentation](autoscale-faq.yml#how-does-the-migration-between-autoscale-and-standard--manual--provisioned-throughput-work-) for more information.

## <a id="autoscale-limits"></a> Throughput and storage limits for autoscale

For any value of `Tmax`, the database or container can store a total of `0.1 * Tmax GB`. After this amount of storage is reached, the maximum RU/s will be automatically increased based on the new storage value, without impacting your application. 

For example, if you start with a maximum RU/s of 50,000 RU/s (scales between 5000 - 50,000 RU/s), you can store up to 5000 GB of data. If you exceed 5000 GB - for example, storage is now 6000 GB, the new maximum RU/s becomes 60,000 RU/s (scales between 6000 - 60,000 RU/s).

When you use database level throughput with autoscale, you can have the first 25 containers share an autoscale maximum RU/s of 1000 (scales between 100 - 1000 RU/s), as long as you don't exceed 100 GB of storage. For more information, refer this [documentation](autoscale-faq.yml#can-i-change-the-maximum-ru-s-on-a-database-or-container--).

## Enabling dynamic scaling

Dynamic scaling is enabled by default for all Azure Cosmos DB accounts created after **September 25, 2024**. Customers who wish to enable this feature for their older accounts can do so [programmatically](autoscale-faq.yml#how-can-i-enable-dynamic-autoscale-on-an-account-programatically-)
 through Azure PowerShell/CLI/Rest API or from the features pane of Azure portal as shown:

1. Navigate to your Azure Cosmos DB account in the [Azure portal](https://portal.azure.com).
1. Navigate to the **Features** page.
1. Locate and enable the **Dynamic Scaling (Per Region and Per Partition Autoscale)** feature.

    :::image type="content" source="media/autoscale-per-partition-region/enable-feature.png" lightbox="media/autoscale-per-partition-region/enable-feature.png" alt-text="Screenshot of the 'Dynamic Scaling (Per Region and Per Partition Autoscale)' feature in the Azure portal.":::

    > [!IMPORTANT]
    > The feature is enabled at the account level, so all autoscale containers and autoscale shared throughput databases within the account will automatically have this capability applied. Enabling this feature does not affect resources in the account that are using manual throughput. Manual resources will need to be changed to autoscale to take advantage of dynamic scaling. Enabling this feature has zero downtime or performance impact. This feature is not applicable for serverless accounts. This feature is supported on all clouds.

## Monitoring Metrics

You can use the following metrics to monitor autoscale and dynamic scaling:

| Metric Name | Definition | Metric Usage |
| --- | ----- | --- |
| Provisioned Throughput | Shows the aggregated highest RU/s scaled to across the hour, and represents the total RU/s scaled to for the hour. | You can use the `Provisioned Throughput` metric to see the RU/s you're billed for in each hour. With autoscale, you're billed based on the most active partition for each hour and the same is applied to all partitions and regions. With dynamic autoscale, you're billed for the aggregated highest RU/s scaled to in each hour at each partition and region level.|
| Normalized RU Consumption | This metric represents the ratio of consumed RU/s to provisioned RU/s at each partition and region level. |Use this metric to determine if the autoscale maximum throughput is under or over-provisioned. <br/><br/> If the metric value is consistently 100% and your application is seeing rate-limiting (429 error code), then you might need more RU/s. In contrast, if this metric value is low and there's no rate-limiting, then there might be room to optimize and scale-down the RU/s. Learn how to [interpret and debug code 429 rate limiting errors](sql/troubleshoot-request-rate-too-large.md). <br/><br/> The `Normalized RU Consumption` metric reflects the RU/s consumed in secondary region due to write replication traffic from the primary, in addition to any read traffic on the secondary. |
| Autoscaled RU | Shows the dynamically scaled provisioned throughput at each partition and region level only for dynamic autoscale enabled accounts. | Use this metric to see how partitions in each region scale independently based on their usage. <br/><br/> Use [Azure Monitor metrics](monitor-reference.md#supported-metrics-for-microsoftdocumentdbdatabaseaccounts) - `Autoscaled RU` to analyze how the new autoscaling is applied across partitions and regions. Filter to your desired database account and container, then filter or split by the Physical PartitionID metric. This metric shows all partitions across their various regions. |

> [!IMPORTANT]
>It is recommended to use Azure Cosmos DB's native dynamic scaling capability to manage your capacity. However, if needed, the [Normalized RU Consumption metric](monitor-normalized-request-units.md) in Azure Monitor can be used to make programmatic scaling decisions. Other approaches, like using the ReadThroughputAsync() call in the Azure Cosmos DB SDKs to get the ProvisionedThroughput, or using ProvisionedThroughput in Azure Monitor are not recommended and will lead to inaccurate results. These metrics represent billed throughput with a delay and shouldn't be used for scaling decisions.

## Comparison – containers configured with manual vs autoscale throughput
For more detail, see this [documentation](how-to-choose-offer.md) on how to choose between standard (manual) and autoscale throughput.  

|| Containers with standard (manual) throughput  | Containers with autoscale throughput |
|---------|---------|---------|
| **Provisioned throughput (RU/s)** | Manually provisioned. | Automatically and instantaneously scaled based on the workload usage patterns. |
| **Rate-limiting of requests/operations (429)**  | May happen, if consumption exceeds provisioned capacity. | Doesn't happen if you consume RU/s within the autoscale throughput range that is configured.    |
| **Capacity planning** |  You have to do capacity planning and set the exact throughput you need. |    The system automatically takes care of capacity planning and capacity management. |
| **Pricing** | You pay for the manually provisioned RU/s per hour, using the [standard (manual) RU/s per hour rate](https://azure.microsoft.com/pricing/details/cosmos-db/). | You pay per hour for the highest RU/s the system scaled up to within the hour. <br/><br/> For single write region accounts, you pay for the RU/s used on an hourly basis, using the [autoscale RU/s per hour rate](https://azure.microsoft.com/pricing/details/cosmos-db/). <br/><br/>For accounts with multiple write regions, there's no extra charge for autoscale. You pay for the throughput used on hourly basis using the same [multi-region write RU/s per hour rate](https://azure.microsoft.com/pricing/details/cosmos-db/). <br/><br/>|
| **Best suited for workload types** |  Predictable and stable workloads|   Unpredictable and variable workloads  |

## Migrate standard provisioned throughput to autoscale

Users that want to migrate a large number of resources from standard provisioned throughput to autoscale can use an Azure CLI script to migrate every throughput resource in an Azure subscription to autoscale.

## Next steps

* Review the [autoscale FAQ](autoscale-faq.yml).
* Learn how to [choose between manual and autoscale throughput](how-to-choose-offer.md).
* Learn how to [provision autoscale throughput on an Azure Cosmos DB database or container](how-to-provision-autoscale-throughput.md).
* Learn more about [partitioning](partitioning-overview.md) in Azure Cosmos DB.
* Trying to do capacity planning for a migration to Azure Cosmos DB? You can use information about your existing database cluster for capacity planning.
    * If all you know is the number of vCores and servers in your existing database cluster, read about [estimating request units using vCores or vCPUs](convert-vcore-to-request-unit.md) 
    * If you know typical request rates for your current database workload, read about [estimating request units using Azure Cosmos DB capacity planner](estimate-ru-with-capacity-planner.md)
