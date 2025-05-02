---
title: "What's New in Azure Database for MySQL"
description: Learn about recent updates to Azure Database for MySQL.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: vamehta, maghan
ms.date: 04/22/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
---

# What's new in Azure Database for MySQL?

[What is Azure Database for MySQL](overview.md) Is an Azure Database service that provides more granular control and flexibility over database management functions and configuration settings. The service currently supports the community versions of MySQL 5.7 and 8.0.

This article summarizes new releases and features in the Azure Database for MySQL service.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we remove it from this article.

## May 2025

### Enable Auto-Scale of IOPS for faster restore and replica provisions

Azure Database for MySQL now supports the ability to enable [auto-scaling of IOPS](https://techcommunity.microsoft.com/blog/adformysql/autoscale-iops-for-azure-database-for-mysql---flexible-server---general-availabi/3884602) for both the source and target servers during restore operations and replica provisioning workflows. This enhancement helps accelerate the restore and replica provisioning process by temporarily boosting IOPS to meet the performance demands of these operations. Once provisioning is complete, you can disable the auto-scale IOPS setting.

To learn more, visit [How to restore a server](./how-to-restore-server-portal.md).

## March 2025

### New Built-in Stored Procedures for Plugin Management and Undo Log Cleanup

There are two new built-in stored procedures in Azure Database for MySQL, allowing customers to manage plugin settings and clean up undo logs without requiring support intervention:

- Validate Password Plugin Management:
  - Enable: `CALL az_install_validate_password_plugin();`
  - Disable: `CALL az_uninstall_validate_password_plugin();`
  - Once enabled, the plugin's configuration parameters are available in the **Server Parameters**  page on the Azure portal.

- Undo Log Cleanup:
  - A new stored procedure is available to manually clean up the **Undo Log**, preventing unnecessary storage consumption.

Refer to the [Built-in stored procedures in Azure Database for MySQL](./concepts-built-in-store-procedure.md) article to learn more about Azure Database for MySQL built-in store procedure

### Caching SHA-2 Password Plugin Now Exposed by Default

The `caching_sha2_password` plugin is now exposed to customers by default. Customers can enable and configure it by setting the relevant **Server Parameters** in the Azure portal.

## February 2025

### Known Issues

- Azure Advisor recommendations might continue to recommend enabling accelerated logs even after the feature is enabled on your Azure Database for MySQL server.

- For servers with [customer managed keys (CMK)](./concepts-customer-managed-key.md), enabling [accelerated logs](./concepts-accelerated-logs.md) might not work due to a current limitation. As a workaround, you can temporarily disable CMK, enable accelerated logs, and then re-enable CMK. We're actively working to resolve this issue at the earliest. For more information, see the [accelerated logs documentation](./concepts-accelerated-logs.md).

## January 2025

### Default zone-resiliency for Business-Critical service tier

You now benefit from the highest level of availability against infrastructure failures within an availability zone, at no extra cost for mission-critical workloads running on the Business-Critical service tier. Regardless of whether your flexible servers are enabled with High Availability (HA), your server data and log files are hosted in zone-redundant storage by default. While zone-redundant HA-enabled servers continue to benefit from a 99.99% uptime SLA from the built-in zonal redundancy and hot standby, non-HA servers are able to recover quickly from zonal outages using zone-redundant backups. This enhancement is applicable to all new server provisioned in Business-Critical service tier.

### Accelerated Logs enabled for all new business critical servers

Accelerated Logs, a feature that significantly enhances the performance of Azure Database for MySQL Flexible Server instances, is now enabled by default for all new Business-Critical servers. Accelerated Logs offers a dynamic solution designed for high throughput needs, reducing latency with no extra cost. Existing Business Critical servers can also enable Accelerated Logs through the Azure portal. [Accelerated logs feature in Azure Database for MySQL ](concepts-accelerated-logs.md).

## November 2024

### MySQL 8.4 LTS version support - Public Preview

Azure Database for MySQL now supports MySQL 8.4 LTS version, bringing the latest MySQL capabilities to Azure. MySQL 8.4 LTS version offers enhanced replication features, expanded monitoring, and long-term support, making it ideal for production environments requiring stability and advanced management. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

### MySQL 9.1 innovation version support - Public Preview

Azure Database for MySQL now supports MySQL 9.1 Innovation version, introduces experimental features, including JavaScript support for stored procedures and the new vector data type, designed for modern applications in machine learning and analytics. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

## Feedback and support

If you have questions about or suggestions for working with Azure Database for MySQL, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.

## Related content

- [Azure Database for MySQL pricing](https://azure.microsoft.com/pricing/details/mysql/server/)
- [public documentation](index.yml)
- [troubleshooting common migration errors](../howto-troubleshoot-common-errors.md)
