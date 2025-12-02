---
title: Compute and Storage Configurations
description: Supported compute and storage configurations for Azure DocumentDB clusters
author: niklarin
ms.author: nlarin
ms.topic: limits-and-quotas
ms.date: 11/07/2025
---

# Compute and storage configurations for Azure DocumentDB

Azure DocumentDB compute resources are provided as vCores, which represent the logical CPU of the underlying hardware. The storage size for provisioning refers to the capacity available to the shards in your cluster.

The storage is used for database files, temporary files, transaction logs, and the
database server logs. You can select the compute and storage settings independently. The selected compute and storage values apply to each shard in the cluster.

## Compute in Azure DocumentDB

The total amount of RAM in a single shard is based on the
selected number of vCores.

| Cluster tier | vCores        | One shard, GiB RAM |
|--------------|-------------- |--------------------|
| M10          | 1 (burstable) | 2                  |
| M20          | 2 (burstable) | 4                  |
| M25          | 2 (burstable) | 8                  |
| M30          | 2             | 8                  |
| M40          | 4             | 16                 |
| M50          | 8             | 32                 |
| M60          | 16            | 64                 |
| M80          | 32            | 128                |
| M200         | 64            | 256                |

## Storage in Azure DocumentDB

The total amount of storage you assign also defines the I/O capacity
available to each shard in the cluster.

| Storage size, GiB | Maximum IOPS |
|-------------------|--------------|
| 32                | 3,500†       |
| 64                | 3,500†       |
| 128               | 3,500†       |
| 256               | 3,500†       |
| 512               | 3,500†       |
| 1,024             | 5,000        |
| 2,048             | 7,500        |
| 4,095             | 7,500        |
| 8,192             | 16,000       |
| 16,384            | 18,000       |
| 32,767            | 20,000       |

† Max IOPS (Input/Output Operations Per Second) with free disk bursting. Storage up to 512 GiB inclusive come with free disk bursting enabled.

## Maximize IOPS for your compute and storage configuration

Each *compute* configuration has an IOPS limit that depends on the number of vCores. Make sure you select compute configuration for your cluster to fully utilize IOPS in the selected storage.

| Storage size      | Storage IOPS, up to | Min compute tier | Min vCores |
|-------------------|---------------------|------------------|------------|
| Up to 0.5 TiB     | 3,500†              | M30              | 2 vCores   |
| 1 TiB             | 5,000               | M40              | 4 vCores   |
| 2 TiB             | 7,500               | M50              | 8 vCores   |
| 4 TiB             | 7,500               | M50              | 8 vCores   |
| 8 TiB             | 16,000              | M60              | 16 vCores  |
| 16 TiB            | 18,000              | M60              | 16 vCores  |
| 32 TiB            | 20,000              | M60              | 16 vCores  |

† Max IOPS with free disk bursting. Storage up to 512 GiB inclusive come with free disk bursting enabled.

For instance, if you need 8 TiB of storage per shard or more, make sure you select 16 vCores or more for the node's compute configuration. That selection would allow you to maximize IOPS usage provided by the selected storage.

## Considerations for compute and storage

When configuring your Azure DocumentDB cluster, it's important to understand how compute and storage choices affect performance, cost, and scalability for your specific workload.

### Working set and memory considerations

In Azure DocumentDB, *the working set* refers to the portion of your data that is frequently accessed and used by your applications. It includes both the data and the indexes that are regularly read or written to during the application's typical operations. The concept of a working set is important for performance optimization because MongoDB, like many databases, performs best when the working set fits in RAM.

To define and understand your MongoDB database working set, consider the following components:

1. **Frequently accessed data**: This data include documents that your application reads or updates regularly.
1. **Indexes**: Indexes that are used in query operations also form part of the working set because they need to be loaded into memory to ensure fast access.
1. **Application usage patterns**: Analyzing the usage patterns of your application can help identify which parts of your data are accessed most frequently.

By keeping the working set in RAM, you can minimize slower disk I/O operations, thus improving the performance of your MongoDB database. If your working set exceeds the available RAM, consider optimizing your data model, adding more RAM to your cluster, or using sharding to distribute data across multiple nodes.

### Choose optimal configuration for a workload

Determining the right compute and storage configuration for your Azure DocumentDB workload involves evaluating several factors related to your application's requirements and usage patterns. The key steps and considerations to determine the optimal configuration include:

1. **Understand your workload**
    - **Data volume**: Estimate the total size of your data, including indexes.
    - **Read/write ratio**: Determine the ratio of read operations with write operations.
    - **Query patterns**: Analyze the types of queries your application performs. For instance, simple reads, complex aggregations.
    - **Concurrency**: Assess the number of concurrent operations your database needs to handle.

1. **Monitor current performance**
    - **Resource utilization**: Use monitoring tools to track CPU, memory, disk I/O, and network usage before migrating your workload to Azure. After deploying your MongoDB workload on an Azure DocumentDB cluster, continue monitoring using [Azure monitoring metrics](./how-to-monitor-diagnostics-logs.md).
    - **Performance metrics**: Monitor key performance metrics such as latency, throughput, and cache hit ratios.
    - **Bottlenecks**: Identify any existing performance bottlenecks, such as high CPU usage, memory pressure, or slow disk I/O.

1. **Estimate resource requirements**
    - **Memory**: Ensure that your [working set](#working-set-and-memory-considerations) (frequently accessed data and indexes) fits into RAM. If your working set size exceeds available memory, consider adding more RAM or optimizing your data model.
    - **CPU**: Choose a CPU configuration that can handle your query load and concurrency requirements. CPU-intensive workloads could require more cores. Use 'CPU percent' metric with 'Max' aggregation on your Azure DocumentDB cluster to see historical compute usage patterns.
    - **Storage IOPS**: Select storage with sufficient IOPS to handle your read and write operations. Use 'IOPS' metric with 'Max' aggregation on your cluster to see historical storage IOPS usage.
    - **Network**: Ensure adequate network bandwidth to handle data transfer between your application and the database, especially for distributed setups. Make sure you configured host for your MongoDB application to support [accelerated networking](/azure/virtual-network/accelerated-networking-overview) technologies such as SR-IOV.

1. **Scale appropriately**
    - **Vertical scaling**: Scales compute / RAM up and down and scale storage up. 
        - Compute: Increase the vCore / RAM on a cluster if your workload requires temporary increase or is often crossing over 70% of CPU utilization for prolonged periods. 
        - Make sure you have appropriate data retention in your Azure DocumentDB database. Retention allows you to avoid unnecessary storage use. Monitor storage usage by [setting alerts](./how-to-manage-alerts.md) on the 'Storage percent' and/or 'Storage used' metrics with 'Max' aggregation. Consider increase storage as your workload size crosses 70% usage.
    - **Horizontal scaling**: Consider using multiple shards for your cluster  to distribute your data across multiple Azure DocumentDB nodes for performance gains and better capacity management as your workload grows. This scaling is especially useful for large datasets (over 2-4 TiB) and high-throughput applications.

1. **Test and iterate**
    - **Benchmarking**: Perform measurement for the most frequently used queries with different configurations to determine the effect on performance. Use CPU/RAM and IOPS metrics and application-level benchmarking.
    - **Load testing**: Conduct load testing to simulate production workloads and validate the performance of your chosen configuration.
    - **Continuous monitoring**: Continuously monitor your Azure DocumentDB deployment and adjust resources as needed based on changing workloads and usage patterns.

By systematically evaluating these factors and continuously monitoring and adjusting your configuration, you can ensure that your MongoDB deployment is well-optimized for your specific workload.

### Considerations for storage

Deciding on the appropriate storage size for your workload involves several considerations to ensure optimal performance and scalability. Here are considerations for the storage size in Azure DocumentDB:

1. **Estimate data size:**
   - Calculate the expected size of your Azure DocumentDB data. Consider:
     - **Current data size:** If migrating from an existing database.
     - **Growth rate:** Estimate how much data will be added over time.
     - **Document size and structure:** Understand your data schema and document sizes, as they affect storage efficiency.

1. **Factor in indexes:**
   - Azure DocumentDB uses **[indexes](./indexing.md)** for efficient querying. Indexes consume extra disk space.
   - Estimate the size of indexes based on:
     - **Number of indexes**.
     - **Size of indexed fields**.

1. **Performance considerations:**
   - Disk performance impacts database operations, especially for workloads that can't fit their [working set](#working-set-and-memory-considerations) into RAM. Consider:
     - **I/O throughput:** IOPS, or Input/Output Operations Per Second, is the number of requests that are sent to storage disks in one second. The larger storage size comes with more IOPS. Ensure adequate throughput for read/write operations. Use 'IOPS' metric with 'Max' aggregation to monitor used IOPS on your cluster.
     - **Latency:** Latency is the time it takes an application to receive a single request, send it to storage disks, and send the response to the client. Latency is a critical measure of an application's performance in addition to IOPS and throughput. The type of storage used and storage configuration largely defines latency. In a managed service like Azure DocumentDB, the fast storage such as Premium SSD disks is used with settings optimized to reduce latency. 

1. **Future growth and scalability:**
   - Plan for future data growth and scalability needs.
   - Allocate more disk space beyond current needs to accommodate growth without frequent storage expansions.

1. **Example calculation**:
   - Suppose your initial data size is 500 GiB.
   - With indexes, it might grow to 700 GiB.
   - If you anticipate doubling the data in two years, plan for 1.4 TiB (700 GiB * 2).
   - Add a buffer for overhead, growth, and operational needs.
   - You might want to start with 1-TiB storage today and upscale it to 2 TiB once its size grows over 800 GiB.

Deciding on storage size involves a combination of estimating current and future data needs, considering indexing and compression, and ensuring adequate performance and scalability. Regular monitoring and adjustment based on actual usage and growth trends are also crucial to maintaining optimal MongoDB performance.

## What is burstable compute?

Burstable tier offers an intelligent solution tailored for small database workloads. By providing minimal CPU performance during idle periods, these clusters optimize resource utilization. However, the real brilliance lies in their ability to seamlessly scale up to full CPU power in response to increased traffic or workload demands. This adaptability provides peak performance precisely when needed, while delivering substantial cost savings.

By reducing the initial price point of the service, Azure DocumentDB's Burstable Cluster Tier aims to facilitate user onboarding and exploration of Azure DocumentDB at reduced prices. This democratization of access empowers businesses of all sizes to harness the power of Azure DocumentDB without breaking the bank. Whether you're a startup, a small business, or an enterprise, this tier opens up new possibilities for cost-effective scalability.

Provisioning a burstable tier is as straightforward as provisioning regular tiers; you only need to choose ["M10," "M20," or "M25"](#compute-in-azure-documentdb) in the cluster tier option. Here's a quick start guide that offers step-by-step instructions on how to set up an [Azure DocumentDB](quickstart-portal.md) cluster.

## Related content

- [Learn how to scale Azure DocumentDB cluster](./how-to-scale-cluster.md)
- [Check out indexing best practices](./how-to-create-indexes.md)
