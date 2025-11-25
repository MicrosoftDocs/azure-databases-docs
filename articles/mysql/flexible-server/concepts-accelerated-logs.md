---
title: Accelerated Logs Feature in Azure Database for MySQL - Flexible Server
description: This article describes the accelerated logs feature in Azure Database for MySQL - Flexible Server and its benefits for high-performance workloads.
author: VandhanaMehta  
ms.author: vamehta  
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ms.custom:
  - references_regions
  - ignite-2023
  - build-2024
  - build-2025
# customer intent: As a reader, I want to understand the concept of accelerated logs in Azure Database for MySQL - Flexible Server.
---

# Accelerated logs in Azure Database for MySQL

The accelerated logs feature is a performance optimization feature designed to improve throughput and reduce transaction latency in [Azure Database for MySQL – Flexible Server](./concepts-service-tiers-storage.md).
The feature boosts server performance by optimizing operations related to transactional logs. When you enable this feature, the server can automatically store transactional logs on faster storage to enhance server throughput.

The following compute tiers support accelerated logs:

| Service Tier       | Availability | Cost               |
|:-------------------|:-------------|:-------------------|
| Memory-Optimized  | Available    | No additional cost |
| General Purpose    | Available    | Additional cost applies. [See pricing details](https://azure.microsoft.com/pricing/details/mysql/)    |

> [!NOTE]
> Accelerated Logs now support the **General Purpose** service tier, so a broader range of workloads can benefit from enhanced performance capabilities.

This article describes the benefits and limitations of accelerated logs. It also outlines the steps to enable and disable the feature.

## Key benefits

Database servers with mission-critical workloads demand robust performance, high throughput, and substantial input/output operations per second (IOPS). These servers can also be sensitive to latency fluctuations in commit times for database transactions.

The accelerated logs feature is designed to address these challenges by optimizing the placement of transactional logs on high-performance storage. Separating transaction log operations from database queries and data updates significantly improves commit latency in database transactions.

Benefits of accelerated logs include:

- **Enhanced throughput**: Query throughput can increase up to twofold in high-concurrency scenarios, resulting in faster query execution. This improvement also reduces latency by up to 50%.
- **Cost efficiency**: Accelerated logs offer a cost-effective solution for mission-critical workloads by providing enhanced performance at no extra expense.
- **Enhanced scalability**: Accelerated logs can accommodate growing workloads for applications that need to scale easily while maintaining high performance. Applications and services on the Memory-Optimized service tier benefit from more responsive interactions and reduced query wait times.

> [!NOTE]
>  - If you enable [zone-redundant high availability](concepts-high-availability.md) for your server, expect additional latency due to the cross-zonal copy of data. We recommend that you conduct your own benchmark tests for an accurate performance assessment.
> 
>  - You can't enable accelerated logs without an availability zone allocated to the server. To enable accelerated logs for such servers, please raise a support case. 

## Limitations

- When you enable the accelerated logs feature, **the [`binlog_expire_logs_seconds`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_expire_logs_seconds) server parameter is disregarded entirely, and any configured value no longer has any effect**. However, if you disable the accelerated logs feature, the server once again adheres to the configured value of `binlog_expire_logs_seconds` for binary log retention. This change also applies to replica servers. 

- [Storage autogrow](./concepts-service-tiers-storage.md#storage-autogrow) is enabled by default for a server with accelerated logs and can't be disabled.

## Availability of accelerated logs by region

The accelerated logs feature is currently available only in the following regions:

- Australia East
  - Brazil South
  - Canada Central
  - Central India
  - Central US
  - China North 3
  - East Asia
  - East US
  - East US 2
  - France Central
  - Germany West Central
  - Israel central
  - Italy North
  - Japan East
  - Korea Central
  - Mexico Central
  - New Zealand North
  - North Europe
  - Norway East
  - Poland Central
  - South Africa North
  - South Central US
  - Southeast Asia
  - Spain Central
  - Sweden Central
  - Switzerland North
  - UAE North
  - UK South
  - US Gov Virginia
  - West Europe
  - West US 2
  - West US 3

## Enable accelerated logs

You can enable the feature during creation of a flexible server or on an existing flexible server.

### Enable accelerated logs during server creation

1. In the [Azure portal](https://portal.azure.com/), select **Flexible Server**, and then select **Create**.

1. Enter values for **Subscription**, **Resource group**, **Server name**, **Region**, and other fields. For details, see the [quickstart for server creation](quickstart-create-server-portal.md).

1. Select the **Configure server** option to change the default compute and storage settings.

1. In the **Storage** section, select the **Accelerated logs** checkbox to enable the feature. The checkbox is available for **Memory-Optimized** and **General Purpose** compute tier.

    :::image type="content" source="media/concepts-accelerated-logs/accelerated-logs-mysql-portal-create.png" alt-text="Screenshot that shows the checkbox for enabling accelerated logs during server creation." lightbox="media/concepts-accelerated-logs/accelerated-logs-mysql-portal-create.png":::

1. Select the **Compute size** value from the dropdown list. Then select **Save** and proceed to deploy your Azure Database for MySQL - Flexible Server instance by following instructions in the [quickstart for server creation](quickstart-create-server-portal.md).

### Enable accelerated logs on your existing server

> [!NOTE]  
> Your server restarts during the deployment process, so ensure that you either pause your workload or schedule it for a time that aligns with your application maintenance or that's off-hours.

1. Go to the [Azure portal](https://portal.azure.com/).

1. Go to **Settings** > **Compute + storage**. In the **Storage** section, select the **Accelerated Logs** checkbox.

    :::image type="content" source="media/concepts-accelerated-logs/accelerated-logs-mysql-portal-enable.png" alt-text="Screenshot that shows selections for enabling accelerated logs on an existing server." lightbox="media/concepts-accelerated-logs/accelerated-logs-mysql-portal-enable.png":::

1. Select **Save** and wait for the deployment process to finish. After you receive a successful deployment message, the feature is ready for use.

## Disable accelerated logs

> [!NOTE]  
> Your server restarts during the deployment process, so make sure that you either pause your workload or schedule it for a time that aligns with your application maintenance or that's during off-hours.

1. Go to the [Azure portal](https://portal.azure.com/).

1. Go to **Settings** > **Compute + storage**. In the **Storage** section, clear the **Accelerated Logs** checkbox.

    :::image type="content" source="media/concepts-accelerated-logs/accelerated-logs-mysql-portal-disable.png" alt-text="Screenshot that shows selections for disabling accelerated logs on an existing server." lightbox="media/concepts-accelerated-logs/accelerated-logs-mysql-portal-disable.png":::

1. Select **Save** and wait for the deployment process to finish. After you receive a successful deployment message, the feature is disabled.

## Related content

- [Quickstart: Create an instance of Azure Database for MySQL with the Azure portal](quickstart-create-server-portal.md)
- [Limitations in Azure Database for MySQL - Flexible Server](concepts-limitations.md)
