---
title: Best Practices for Optimal Performance in Azure Managed Instance for Apache Cassandra
description: Learn about best practices to ensure optimal performance from Azure Managed Instance for Apache Cassandra.
author: IriaOsara
ms.author: iriaosara
ms.reviewer: sidandrews
ms.date: 06/05/2025
ms.service: azure-managed-instance-apache-cassandra
ms.topic: how-to
keywords: azure performance cassandra
#customer intent: As a database administrator, I want to optimize performance for my Azure Managed Instance for Apache Cassandra.
---

# Best practices for optimal performance in Azure Managed Instance for Apache Cassandra

Azure Managed Instance for Apache Cassandra is a fully managed service for pure open-source Apache Cassandra clusters. The service also allows configurations to be overridden, depending on the specific needs of each workload. This feature allows maximum flexibility and control where needed. This article provides tips on how to optimize performance.

## Optimal setup and configuration

### Replication factor, number of disks, number of nodes, and SKUs

Azure supports *three* availability zones in most regions. Azure Managed Instance for Apache Cassandra maps availability zones to racks. We recommend that you choose a partition key with high cardinality to avoid hot partitions. For the best level of reliability and fault tolerance, we highly recommend configuring a replication factor of 3. We also recommend specifying a multiple of the replication factor as the number of nodes, for example 3, 6, 9, etc.

Azure uses a RAID 0 over the number of disks you provision. To get the optimal IOPS, check for the maximum IOPS on the SKU you chose together with the IOPS of a P30 disk. For example, the `Standard_DS14_v2` SKU supports 51,200 uncached IOPS, whereas a single P30 disk has a base performance of 5,000 IOPS. Four disks would lead to 20,000 IOPS, which is well below the limits of the machine.

We strongly recommend extensive benchmarking of your workload against the SKU and number of disks. Benchmarking is especially important for SKUs with only eight cores. Our research shows that eight core CPUs only work for the least demanding workloads. Most workloads need a minimum of 16 cores to be performant.

## Analytical vs. Transactional workloads

Transactional workloads typically need a data center optimized for low latency, while analytical workloads often use more complex queries, which take longer to run. In most cases, you would want separate data centers:

- One optimized for low latency
- One optimized for analytical workloads

### Optimizing for analytical workloads

We recommend that customers apply the following `cassandra.yaml` settings for analytical workloads. For more information about how to apply these settings, see [Update Cassandra configuration](create-cluster-portal.md#update-cassandra-configuration).

#### Timeouts

| Value | Cassandra MI Default | Recommendation for analytical workload |
| --- | --- | --- |
| read_request_timeout_in_ms | 5,000 | 10,000 |
| range_request_timeout_in_ms | 10,000 | 20,000 |
| counter_write_request_timeout_in_ms | 5,000 | 10,000 |
| cas_contention_timeout_in_ms | 1,000 | 2,000 |
| truncate_request_timeout_in_ms | 60,000 | 120,000 |
| slow_query_log_timeout_in_ms | 500 | 1,000 |
| roles_validity_in_ms | 2,000 | 120,000 |
| permissions_validity_in_ms | 2,000 | 120,000 |

#### Caches

| Value | Cassandra MI Default | Recommendation for analytical workload |
| --- | --- | --- |
| file_cache_size_in_mb | 2,048 | 6,144 |

#### More recommendations

| Value | Cassandra MI Default | Recommendation for analytical workload |
| --- | --- | --- |
| commitlog_total_space_in_mb | 8,192 | 16,384 |
| column_index_size_in_kb | 64 | 16 |
| compaction_throughput_mb_per_sec | 128 | 256 |

#### Client settings

We recommend boosting Cassandra client driver timeouts in accordance with the timeouts applied on the server.

### Optimizing for low latency

Our default settings are already suitable for low latency workloads. To ensure best performance for tail latencies, we highly recommend using a client driver that supports [speculative execution](https://docs.datastax.com/en/developer/java-driver/4.10/manual/core/speculative_execution/) and configuring your client accordingly. For Java V4 driver, you can find a demo illustrating how this works and how to enable the policy in [this sample](https://github.com/Azure-Samples/azure-cassandra-mi-java-v4-speculative-execution).

## Monitoring for performance bottle necks

### CPU performance

Like every database system, Cassandra works best if the CPU utilization is around 50% and never gets above 80%. You can view CPU metrics in the Metrics tab within Monitoring from the portal:

:::image type="content" source="media/best-practice-performance/metrics-cpu.png" border="true" alt-text="Screenshot of CPU metrics by idle usage." lightbox="media/best-practice-performance/metrics-cpu.png":::

> [!TIP]  
> For a realistic CPU view, add a filter and split the property by `Usage kind=usage_idle`. If this value is lower than 20%, you can apply splitting to obtain usage by all usage kinds.

:::image type="content" source="media/best-practice-performance/metrics-cpu-by-usage.png" border="true" alt-text="Screenshot of CPU metrics by usage kind." lightbox="media/best-practice-performance/metrics-cpu-by-usage.png":::

If the CPU is permanently above 80% for most nodes, the database becomes overloaded, which manifests in multiple client timeouts. In this scenario, we recommend that you take the following actions:

- Vertically scale up to a SKU with more CPU cores, especially if the cores are only 8 or less.
- Horizontally scale by adding more nodes. As mentioned earlier, the number of nodes should be multiple of the replication factor.

If the CPU is only high for a few nodes, but low for the others, it indicates a hot partition, which needs further investigation.

> [!NOTE]  
> Changing SKU is supported by using the Azure portal, Azure CLI, and ARM template deployment. You can deploy or edit an ARM template and replace SKU with one of the following values:
>  
> - Standard_E8s_v4
> - Standard_E16s_v4
> - Standard_E20s_v4
> - Standard_E32s_v4
> - Standard_DS13_v2
> - Standard_DS14_v2
> - Standard_D8s_v4
> - Standard_D16s_v4
> - Standard_D32s_v4
> - Standard_L8s_v3
> - Standard_L16s_v3
> - Standard_L32s_v3
> - Standard_L8as_v3
> - Standard_L16as_v3
> - Standard_L32as_v3
>  
> Currently, we don't support transitioning across SKU families. For instance, if you currently possess a `Standard_DS13_v2` and want to upgrade to a larger SKU such as `Standard_DS14_v2`, this option isn't available. However, you can open a support ticket to request an upgrade to the higher SKU.

### Disk performance

The service runs on Azure P30 managed disks, which allow for *burst IOPS*. Careful monitoring is required when it comes to disk related performance bottlenecks. In this case, it's important to review the IOPS metrics:

:::image type="content" source="media/best-practice-performance/metrics-disk.png" border="true" alt-text="Screenshot of disk I/O metrics." lightbox="media/best-practice-performance/metrics-disk.png":::

If metrics show one or all of the following characteristics, you might need to scale up.

- Consistently higher than or equal to the base IOPS. Remember to multiply 5,000 IOPS by the number of disks per node to get the number.
- Consistently higher than or equal to the maximum IOPS allowed for the SKU for writes.
- Your SKU supports cached storage (write-through-cache) and this number is smaller than the IOPS from the managed disks. This value is the upper limit for your read IOPS.

If you only see the IOPS elevated for a few nodes, you might have a hot partition and need to review your data for a potential skew.

If your IOPSs are lower than what you SKU supports, but higher or equal to the disk IOPS, you can take the following actions:

- Add more disks to increase performance. Increasing disks requires a support case to be raised.
- [Scale up the data centers](create-cluster-portal.md#scale-a-datacenter) by adding more nodes.

If your IOPS max out what your SKU supports, you can:

- Scale up to a different SKU supporting more IOPS.
- [Scale up the data centers](create-cluster-portal.md#scale-a-datacenter) by adding more nodes.

For more information, see [Virtual machine and disk performance](/azure/virtual-machines/disks-performance).

### Network performance

In most cases, network performance is sufficient. However, if you're frequently streaming data, such as frequent horizontal scale-up/scale down, or there are huge ingress/egress data movements, this performance can become a problem. You might need to evaluate the network performance of your SKU. For example, the `Standard_DS14_v2` SKU supports 12,000 Mb/s. Compare this value to the byte-in/out in the metrics:

:::image type="content" source="media/best-practice-performance/metrics-network.png" border="true" alt-text="Screenshot of network metrics." lightbox="media/best-practice-performance/metrics-network.png":::

If you only see the network elevated for a few nodes, you might have a hot partition and need to review your data distribution and access patterns for a potential skew.

- Vertically scale up to a different SKU supporting more network I/O.
- Horizontally scale up the cluster by adding more nodes.

### Too many connected clients

You should plan and provision deployments to support the maximum number of parallel requests required for the desired latency of an application. For a given deployment, introducing more load to the system above a minimum threshold increases overall latency. Monitor the number of connected clients to ensure this situation doesn't exceed tolerable limits.

:::image type="content" source="media/best-practice-performance/metrics-connections.png" border="true" alt-text="Screenshot of connected client metrics." lightbox="media/best-practice-performance/metrics-connections.png":::

### Disk space

In most cases, there's sufficient disk space. Default deployments are optimized for IOPS, which leads to low utilization of the disk. Nevertheless, we recommend occasionally reviewing disk space metrics. Cassandra accumulates numerous disks and then reduces it when compaction is triggered. It's important to review disk usage over longer periods to establish trends, like compaction unable to recoup space.

> [!NOTE]  
> In order to ensure available space for compaction, disk utilization should be kept to around 50%.

If you only see this behavior for a few nodes, you might have a hot partition and need to review your data distribution and access patterns for a potential skew.

- Add more disks but be mindful of IOPS limits imposed by your SKU
- Horizontally scale up the cluster

### JVM memory

Our default formula assigns half the virtual machine's memory to the Jave Virtual Machine (JVM) with an upper limit of 31 GB. In most cases, this approach is a good balance between performance and memory. Some workloads, especially ones that have frequent cross-partition reads or range scans might be memory challenged.

In most cases memory gets reclaimed effectively by the Java garbage collector, but especially if the CPU is often above 80% there aren't enough CPU cycles for the garbage collector left. So any CPU performance problems should be addresses before memory problems.

If the CPU hovers below 70%, and the garbage collection isn't able to reclaim memory, you might need more JVM memory. More JVM memory might be necessary if you're on a SKU with limited memory. In most cases, you need to review your queries and client settings and reduce `fetch_size` along with what is chosen in `limit` within your CQL query.

If you indeed need more memory, you can:

- File a ticket for us to increase the JVM memory settings for you
- Scale vertically to a SKU that has more memory available

### Tombstones

We run repairs every seven days with reaper, which removes rows whose TTL expired, called *tombstone*. Some workloads delete more frequently and show warnings like `Read 96 live rows and 5035 tombstone cells for query SELECT ...; token <token> (see tombstone_warn_threshold)` in the Cassandra logs, or even errors indicating that a query couldn't be fulfilled due to excessive tombstones.

A short term mitigation if queries don't get fulfilled is to increase the `tombstone_failure_threshold` in the [Cassandra configuration](create-cluster-portal.md#update-cassandra-configuration) from the default 100,000 to a higher value.

We also recommend that you review the TTL on the keyspace and potentially run repairs daily to clear out more tombstones. If the TTLs are short, for example less than two days, and data flows in and gets deleted quickly, we recommend that you review the [compaction strategy](https://cassandra.apache.org/doc/4.1/cassandra/operating/compaction/index.html#types-of-compaction) and favor `Leveled Compaction Strategy`. In some cases, such actions might indicate that a review of the data model is required.

### Batch warnings

You might encounter this warning in the [CassandraLogs](monitor-clusters.md#create-setting-portal) and potentially related failures:

`Batch for [<table>] is of size 6.740KiB, exceeding specified threshold of 5.000KiB by 1.740KiB.`

In this case, you should review your queries to stay below the recommended batch size. In rare cases and as a short term mitigation, you can increase `batch_size_fail_threshold_in_kb` in the [Cassandra configuration](create-cluster-portal.md#update-cassandra-configuration) from the default of 50 to a higher value.

## Large partition warning

You might encounter this warning in the [CassandraLogs](monitor-clusters.md#create-setting-portal):

`Writing large partition <table> (105.426MiB) to sstable <file>`

This message indicates a problem in the data model. For more information, see this [stack overflow article](https://stackoverflow.com/questions/74024443/how-do-i-analyse-and-solve-writing-large-partition-warnings-in-cassandra). This problem can cause severe performance issues and needs to be addressed.

## Specialized optimizations

### Compression

Cassandra allows the selection of an appropriate compression algorithm when a table is created. The default is LZ4, which is excellent for throughput and CPU but consumes more space on disk. Using Zstd (Cassandra 4.0 and up) saves about ~12% space with minimal CPU overhead.

### Optimizing memtable heap space

The default is to use 1/4 of the JVM heap for [memtable_heap_space](https://cassandra.apache.org/doc/stable/cassandra/managing/configuration/cass_yaml_file.html) in the cassandra.yaml. For write oriented application and/or on SKUs with small memory, this issue can lead to frequent flushing and fragmented `sstables`, which require more compaction. In such cases, increasing it to at least 4048 might be good. This approach requires careful benchmarking to make sure other operations, for example, reads, aren't affected.

## Next step

> [!div class="nextstepaction"]
> [Create a cluster using Azure Portal](create-cluster-portal.md)
