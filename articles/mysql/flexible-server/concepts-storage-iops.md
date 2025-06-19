---
title: Storage IOPS in Azure Database for MySQL - Flexible Server
description: This article describes the storage IOPS in Azure Database for MySQL - Flexible Server.
author: code-sidd
ms.author: sisawant
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: article
ms.custom:
  - build-2024
---

# Storage IOPS in Azure Database for MySQL - Flexible Server

The number of read and write operations that the storage system can perform is measured in input/output operations per second (IOPS). Higher IOPS values indicate better storage performance, which allows your database to handle more simultaneous read and write operations. The result is faster data retrieval and improved overall efficiency.

If the IOPS setting is too low, the database server might experience delays in processing requests, resulting in slow performance and reduced throughput. If the IOPS setting is too high, it might lead to unnecessary resource allocation and potentially increased costs without significant performance improvements.

## Choose an IOPS management setting

Azure Database for MySQL - Flexible Server currently offers two settings for IOPS management: pre-provisioned IOPS and autoscale IOPS.

### Pre-provisioned IOPS

You can use pre-provisioned IOPS to allocate a specific number of IOPS to your Azure Database for MySQL - Flexible Server instance. Defining a specific IOPS limit for your storage volume guarantees the ability to handle a certain number of requests per second. This setting helps ensure consistent and predictable performance for your workloads.

Pre-provisioned IOPS also provide the flexibility of increasing provisioned IOPS for the storage volume associated with the server. You can customize performance by adding extra IOPS beyond the default provisioned level at any time, to better align with your workload requirements.

### Autoscale IOPS

Autoscale IOPS offer the flexibility to scale IOPS on demand. When you enable autoscale IOPS, your server automatically adjusts the IOPS limit of your database server based on the demand of your workload. This dynamic scaling helps optimize workload performance without manual intervention or configuration. For detailed information on the maximum supported IOPS for each service tier and compute size, see the [service tier documentation](./concepts-service-tiers-storage.md#service-tiers-size-and-server-types).

Other benefits of autoscale IOPS include:

- **Handling workload spikes**: Autoscale IOPS enable your database to seamlessly handle workload spikes or fluctuations without compromising the performance of your applications. This feature helps ensure consistent responsiveness, even during peak usage periods.

- **Cost savings**: Unlike pre-provisioned IOPS, where you specify and pay for a fixed IOPS limit regardless of usage, autoscale IOPS lets you pay for only the number of I/O operations that you consume. You avoid unnecessary provisioning and expenses for underutilized resources. The result is both cost savings and optimal performance, making autoscale a smart choice for managing your database workload efficiently.

## Monitor storage performance

You can monitor storage IOPS utilization by using [metrics available for Azure Database for MySQL - Flexible Server](./concepts-monitoring.md#list-of-metrics).

### Get an I/O utilization overview for a selected time period

1. In the Azure portal, go to your Azure Database for MySQL Flexible Server.
1. On the **Overview** pane, select the **Monitoring** tab.
1. In the **Show data for last** area, select a time period.

[:::image type="content" source="./media/concepts-storage-iops/1-overview.png" alt-text="Screenshot of the tab for monitoring a server to troubleshoot and optimize a workload.":::](./media/concepts-storage-iops/1-overview.png#lightbox)

### View a workbook for enhanced metrics

1. In the Azure portal, go to your Azure Database for MySQL Flexible Server.
1. Go to **Monitoring** > **Workbooks**.
1. Select the **Enhanced Metrics** workbook.
1. On the **Overview** tab of the workbook, check for **Storage IO Percentage** metrics.

[:::image type="content" source="./media/concepts-storage-iops/2-workbook.png" alt-text="Screenshot of a workbook for enhanced metrics.":::](./media/concepts-storage-iops/2-workbook.png#lightbox)

### Add metrics for storage I/O percentage and count

1. In the Azure portal, go to your Azure Database for MySQL Flexible Server.
1. Go to **Monitoring** > **Metrics**.
1. Select **Add metric**.
1. In the dropdown list of available metrics, select **Storage IO Percent** and **Storage IO Count**.

[:::image type="content" source="./media/concepts-storage-iops/3-metrics.png" alt-text="Screenshot of added monitoring metrics for storage input/output percentage and count.":::](./media/concepts-storage-iops/3-metrics.png#lightbox)

## Select the optimal IOPS setting

Now that you know how to monitor your IOPS usage effectively, you're equipped to explore the best settings for your server. When you're choosing the IOPS setting for your Azure Database for MySQL - Flexible Server instance, consider the following factors. Understanding these factors can help you make an informed decision for ensuring the best performance and cost-efficiency for your workload.

### Performance optimization

With autoscale IOPS, you can meet the requirements for consistency and predictability of your workload without facing the drawback of storage throttling and manual interaction to add more IOPS.

If your workload has consistent throughput or requires consistent IOPS, pre-provisioned IOPS might be preferable. It provides a predictable performance level, and the fixed allocation of IOPS correlates with workloads within the specified limits.

If you need throughput that's higher than the usual requirement, you can allot additional IOPS by using pre-provisioned IOPS. This option requires manual interaction and an understanding of throughput increase time.

### Throttling impact

Consider the impact of throttling on your workload. If potential performance degradation due to throttling is a concern, autoscale IOPS can dynamically handle workload spikes to minimize the risk of throttling and help maintain performance at an optimal level.

Ultimately, the decision between autoscale and pre-provisioned IOPS depends on your specific workload requirements and performance expectations. Analyze your workload patterns, evaluate the cost implications, and consider the potential impact of throttling to make a choice that aligns with your priorities.

| Workload considerations | Pre-provisioned IOPS | Autoscale IOPS |
| --- | --- | --- |
| Workloads with consistent and predictable I/O patterns | Recommended, because it uses only provisioned IOPS | Compatible, with no manual provisioning of IOPS required |
| Workloads with varying usage patterns | Not recommended, because it might not provide efficient performance during high usage periods. | Recommended, because it automatically adjusts to handle varying workloads |
| Workloads with dynamic growth or changing performance needs | Not recommended, because it requires constant adjustments for changing IOPS requirements | Recommended, because no extra settings are required for specific throughput requirements |

### Cost considerations

If you have a fluctuating workload with unpredictable peaks, opting for autoscale IOPS might be more cost-effective. It ensures that you pay for only the higher IOPS that you use during peak periods, offering flexibility and cost savings. Although pre-provisioned IOPS provides consistent and maximum IOPS, it might come at a higher cost, depending on the workload. Consider the trade-off between cost and performance required from your server.

<a id="testing-and-evaluation"></a>

### Test and evaluation

If you're unsure about the optimal IOPS setting, consider running performance tests by using both autoscale IOPS and pre-provisioned IOPS. Assess the results and determine which setting meets your workload requirements and performance expectations.

#### Example workload: E-commerce website

Suppose you own an e-commerce website that experiences fluctuations in traffic throughout the year. During normal periods, the workload is moderate. But during holiday seasons or special promotions, the traffic surges exponentially.

With autoscale IOPS, your database can dynamically adjust its IOPS to handle the increased workload during peak periods. When traffic spikes, such as during Black Friday sales, the autoscale feature allows your database to seamlessly scale up the IOPS to meet the demand. This ability helps ensure smooth and uninterrupted performance, and it helps prevent slowdowns or service disruptions. After the peak period, when the traffic subsides, the IOPS can scale back down. You then save costs, because you pay for only the resources utilized during the surge.

If you opt for pre-provisioned IOPS, you need to estimate the maximum workload capacity and allocate a fixed number of IOPS accordingly. However, during peak periods, the workload might exceed the predetermined IOPS limit. The storage I/O could then throttle, affecting performance and potentially causing delays or timeouts for your users.

#### Example workload: Platform for reporting and data analytics

Suppose you're using Azure Database for MySQL - Flexible Server for data analytics, where users submit complex queries and large-scale data processing tasks. The workload pattern is relatively consistent, with a steady flow of queries throughout the day.

With pre-provisioned IOPS, you can select a suitable number of IOPS based on the expected workload. As long as the chosen IOPS adequately handle the daily query volume, there's no risk of throttling or performance degradation. This approach provides cost predictability and enables you to optimize resources efficiently without the need for dynamic scaling.

The autoscale feature might not provide significant advantages in this case. Because the workload is consistent, you can provision the database with a fixed number of IOPS that comfortably meets the demand. Autoscaling might not be necessary, because there are no sudden bursts of activity that require additional IOPS.

By using pre-provisioned IOPS, you have predictable performance without the need for scaling. Cost is directly tied to the allocated storage.

## Frequently asked questions

### How do I move from pre-provisioned IOPS to autoscale IOPS?

1. In the Azure portal, find the relevant Azure Database for MySQL Flexible Server.
1. Go to the **Settings** pane, and then select **Compute + storage**.
1. In the **IOPS** section, select **Auto Scale IOPS** and save the settings to apply the modifications.

### How soon does autoscale IOPS take effect after I make the change?

After you enable autoscale IOPS for your Azure Database for MySQL Flexible Server and save the settings, the changes take effect immediately after the deployment to the resource finishes successfully. The autoscale IOPS feature is applied to your database without any delay.

### How does a point-in-time restore operation affect IOPS usage?

During a point-in-time restore (PITR) operation in Azure Database for MySQL - Flexible Server, a new server is created and data is copied from the source server's storage to the new server's storage. This process results in an increased IOPS usage on the source server.

The increase in IOPS usage is a normal occurrence and doesn't indicate any problems with the source server or the PITR operation. After the PITR operation is complete, the IOPS usage on the source server returns to its usual levels.

For more information on PITR, see [Backup and restore in Azure Database for MySQL - Flexible Server](concepts-backup-restore.md).

### How do I know that IOPS have scaled up and scaled down when the server is using the autoscale IOPS feature? Can I monitor IOPS usage for my server?

Refer to the [Monitor storage performance](#monitor-storage-performance) section earlier in this article. It helps you identify if your server has scaled up or scaled down during a specific time window.

### Can I switch between autoscale IOPS and pre-provisioned IOPS later?

Yes. You can move back to pre-provisioned IOPS by selecting it in the **Compute + storage** section of the **Settings** pane.

### How do I know how many IOPS I've used in Azure Database for MySQL - Flexible Server?

Go to **Monitoring** in the **Overview** section, or go to the [Storage IO Count metric](./concepts-monitoring.md#list-of-metrics) on the **Monitoring** pane. The Storage IO Count metric gives the sum of IOPS that the server used in the selected timeframe.

## Related content

- [service limitations](concepts-limitations.md)
- [pricing](./concepts-service-tiers-storage.md#price)
