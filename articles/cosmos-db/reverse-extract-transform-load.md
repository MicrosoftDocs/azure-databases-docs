---
title: Reverse extract, transform, & load (ETL)
description: Review how reverse extract, transform, and load (ETL) moves data from a data lake layer back into operational system (database) layer for real-time analytics. 
author: rakhithejraj
ms.author: rakhithejraj
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: concept-article
ms.date: 04/21/2025
appliesto:
  - ✅ NoSQL
---

# Reverse extract, transform, & load (ETL) with Azure Cosmos DB for NoSQL

Cloud data warehouses and data lakes enrich data, centralize information, and enable powerful analytics. But the real value of data lies in turning insights into real-world decisions and customer experiences. To achieve this goal, clean, reliable data must move out of the warehouse / data lakes into operational systems. Reverse ETL moves data from your data warehouse layer, like Delta Lake in Azure Databricks or Microsoft Fabric, back into operational systems. This migration step allows downstream apps to use the most recent, enriched data for real-time operational analytics. Reverse ETL plays a crucial role in unlocking the full potential of your data assets by bridging the gap between analytics and operations, enabling better decision-making.

Azure Cosmos DB for NoSQL is designed for ultra-low latency, global distribution, and NoSQL scalability, making it ideal for real-time applications. With Reverse ETL, you can sync Delta-enriched data into Azure Cosmos DB, enabling real-time operational analytics. You can use this pattern to push data like product catalogs, personalized customer info, pricing updates, inventory data, and feature recommendations. You can push this data into your operational data store, empowering downstream apps to make data-driven decisions instantly.

## Solution architecture

A streamlined architecture to implement reverse ETL is composed of Apache Spark and Azure Databricks. This architecture extracts cleansed and enriched data from sources like Delta Tables and writes the data back to the operational store in Azure Cosmos DB for NoSQL.

:::image type="complex" source="media/reverse-extract-transform-load/solution.png" lightbox="media/reverse-extract-transform-load/solution-expanded.png" alt-text="Diagram of a reverse ETL architecture comprised of multiple components migrating data.":::
    Diagram of a reverse ETL architecture comprised of multiple components migrating data. The components include data sources that could include product, CRM, order, or ad data. The data from the data sources is then ingested into a data warehouse or data lake using an ETL workflow. Finally, the data is sent out of the intermediate storage using a reverse ETL workflow. The data is sent into an operational data store like Azure Cosmos DB for NoSQL.
:::image-end:::

This diagram includes the following components:

- **Data sources** that include data such as; product data, CRM data, order information, and ad information.

- **ETL workflow** moving data from the original data sources to a data warehouse or data lake to store and enrich the data using solutions like Azure Databricks or Microsoft Fabric.

- **Reverse ETL workflow** to migrate the enriched data to an operational data store using Apache Spark and Delta tables

- **Operation data store** like Azure Cosmos DB for NoSQL to use the enriched data in real-time applications.

The reverse ETL process enables scenarios such as:

- **Real-Time Decisions:** Apps get access to the freshest data without relying on analysts or SQL.

- **Data Activation:** Insights are pushed where they’re needed—not just in dashboards.

- **Unified Source of Truth:** Delta Lake acts as the canonical layer, ensuring consistency across systems.  

## Data ingestion stages

For scenarios like feature store, recommendation engines, fraud detection, or real-time product catalogs, it's important to separate the data flow into two stages. These stages assume you have a reverse ETL pipeline from Delta Lake to Azure Cosmos DB for NoSQL.

:::image type="complex" source="media/reverse-extract-transform-load/stages.png" lightbox="media/reverse-extract-transform-load/stages-expanded.png" alt-text="Diagram of the two reverse ETL stages from Delta Lake to Azure Cosmos DB for NoSQL.":::
    Diagram of the two reverse ETL stages from Delta Lake to Azure Cosmos DB for NoSQL. The first stage loads data using a one-time batch process. The second stage uses change data capture to sync the data. Both stages output data into Azure Cosmos DB for NoSQL as the operational data store.
:::image-end:::

The stages in this diagram consist of:

1. **Initial load**: The initial load is a one-time batch process step to ingest all historical data from Delta Tables into Azure Cosmos DB for NoSQL. It sets the foundation for your reverse ETL pipeline by ensuring the operational data store has complete historic data. This load is a fundamental step before starting incremental sync of data.

1. **Change data capture (CDC) sync**: This step implements an incremental, continuous sync of changes from Delta Tables to Azure Cosmos DB for NoSQL. Changes in the delta table can be captured after enabling Delta Change Data Feed (CDF). You can implement either batch-based or streaming-based change data capture (CDC) sync.

There are two options for CDC sync into Azure Cosmos DB for NoSQL:

- **Batch CDC sync**: This option runs on a schedule (ex. daily or hourly) and loads an incremental snapshot of the data based on changes captured since the last version or timestamp.

    > [!TIP]
    > Switch to a newer Azure Cosmos DB snapshot to avoid data inconsistencies when large incremental volumes are being loaded from a delta table to Azure Cosmos DB for NoSQL. For example, when writing to a new container or using a version flag, flip a pointer to a newer screenshot once the new data is fully loaded.

- **Stream CDC sync**: This option continuously syncs incremental changes in near real-time, keeping the target system up to date with minimal lag. This option uses Apache Spark structured streaming to continuously capture and write changes. The delta table acts as a streaming source with `readChangeData = true`, and the Azure Cosmos DB for NoSQL connector acts as a streaming sink. 

    > [!TIP]
    > Specify a checkpoint location to ensure progress is tracked and duplicate writes are avoided.

## Best practices

- Use Apache Spark batch jobs with the Azure Cosmos DB for NoSQL connector to perform the initial load step.

- Optimize ingestion throughput by switching to standard provisioned throughput if the initial load is expected to consume a large amount of RU/s relative to your allocated throughput. Specifically, use standard provisioned throughput if the maximum request units per second (RU/s) is utilized consistently for most the duration of the initial load process. Don't use autoscale throughput for the initial load step in this scenario.

    > [!TIP]
    > If the [normalized RU consumption metric](monitor-normalized-request-units.md) is consistently 100%, then the metric indicates that the initial load consistently consumes the maximum autoscale request units (RUs). This threshold is a clear indicator that this scenario applies to your workload and you should use standard provisioned throughput.

- Choose an effective partition key that maximizes parallelism. For more information, see [partitioning and partition key recommendations](partitioning-overview.md).

- Plan for the total number of partitions and total RU/s across all partitions for large data ingestions. For more information and guidance, see [recommendations for partitioning and throughput](scaling-provisioned-throughput-best-practices.md#how-to-optimize-rus-for-large-data-ingestion).

- Use [Apache Spark throughput control](throughput-control-spark.md) to limit the request unit (RU) consumption of jobs. Throughput control helps prevent overloading the target operational container.

- Use autoscale throughput when possible in Azure Cosmos DB for NoSQL for CDC sync as autoscale scales up/down RU/s dynamically based on usage. Autoscale throughput is ideal for periodic and spiky workloads like scheduled CDC sync jobs. For more information, see [throughput recommendations](how-to-choose-offer.md#overview-of-provisioned-throughput-types).

- Estimate the initial ingestion duration for your initial data load step. For more information and a sample, see [throughput estimation](scaling-provisioned-throughput-best-practices.md#example-1).

## Next step

> [!div class="nextstepaction"]
> [Implement reverse ETL with Azure Databricks](tutorial-reverse-extract-transform-load.md)
