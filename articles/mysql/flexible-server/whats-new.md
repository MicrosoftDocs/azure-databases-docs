---
title: "What's New in Azure Database for MySQL - Flexible Server"
description: Learn about recent updates to Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: vamehta, maghan
ms.date: 04/22/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
---

# What's new in Azure Database for MySQL

[What is Azure Database for MySQL](overview.md) Is a n Azure Database service that provides more granular control and flexibility over database management functions and configuration settings.

This article summarizes new releases and features in the Azure Database for MySQL service.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we remove it from this article.

## March 2025

## New Built-in Stored Procedures for Plugin Management and Undo Log Cleanup

We have introduced two new built-in stored procedures in Azure Database for MySQL – Flexible Server, allowing customers to manage plugin settings and clean up undo logs without requiring support intervention:

- **Validate Password Plugin Management**:
  - Enable: `CALL az_install_validate_password_plugin();`
  - Disable: `CALL az_uninstall_validate_password_plugin();`
  - Once enabled, the plugin's configuration parameters are available in the **Server Parameters** page on the Azure portal.

- **Undo Log Cleanup**:
  - A new stored procedure is available to manually clean up the **Undo Log**, preventing unnecessary storage consumption.

Refer to [this](./concepts-built-in-store-procedure.md) document to learn more about Azure Database for MySQL flexible server built-in store procedure

## Caching SHA-2 Password Plugin Now Exposed by Default

The `caching_sha2_password` plugin is now exposed to customers by default. Customers can enable and configure it by setting the relevant **server parameters** in the Azure portal.

## February 2025

**Known Issues**

- Azure Advisor recommendations might continue to recommend enabling accelerated logs even after the feature is enabled on your **Azure Database for MySQL – Flexible Server**. We're actively working on a fix, and this issue will be resolved at the earliest. If [accelerated logs](./concepts-accelerated-logs.md) is already enabled on your server, you can safely ignore this recommendation.

- For [CMK enabled](./concepts-customer-managed-key.md) servers, enabling [accelerated logs](./concepts-accelerated-logs.md) might not work due to a current limitation. As a workaround, you can temporarily disable CMK, enable accelerated logs, and then re-enable CMK. We're actively working to resolve this issue at the earliest. For more information, see the [accelerated logs documentation](./concepts-accelerated-logs.md).

## January 2025

**Default zone-resiliency for Business-Critical service tier**

You'll now benefit from the highest level of availability against infrastructure failures within an availability zone, at no additional cost for mission-critical workloads running on the Business-Critical service tier. Regardless of whether your flexible servers are enabled with High Availability (HA), your server data and log files will be hosted in zone-redundant storage by default. While zone-redundant HA-enabled servers continue to benefit from a 99.99% uptime SLA from the built-in zonal redundancy and hot standby, non-HA servers will also be able to recover quickly from zonal outages using zone-redundant backups. This enhancement is applicable to all new server provisioned in Business-Critical service tier.

**Accelerated Logs Enabled for All New Business Critical Servers**

Accelerated Logs, a feature that significantly enhances the performance of Azure Database for MySQL Flexible Server instances, is now enabled by default for all new Business-Critical servers. Accelerated Logs offers a dynamic solution designed for high throughput needs, reducing latency with no additional cost. Existing Business Critical servers can also enable Accelerated Logs through the Azure portal. [Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md).

**Server parameter lower_case_table_names is now supported for MySQL 8.0+ - Private Preview**

Azure Database for MySQL - Flexible Server now supports the lower_case_table_names server parameter in private preview for MySQL 8.0+. Customers can configure this parameter with a value of 1 or 2 during server creation. To participate in the private preview, please open a [support ticket](https://azure.microsoft.com/support/create-ticket) for assistance.

## November 2024

**MySQL 8.4 LTS version support - Public Preview**

Azure MySQL Flexible Server now supports MySQL 8.4 LTS version, bringing the latest MySQL capabilities to Azure. MySQL 8.4 LTS version offers enhanced replication features, expanded monitoring, and long-term support, making it ideal for production environments requiring stability and advanced management. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

**MySQL 9.1 innovation version support - Public Preview**

Azure Database for MySQL now supports MySQL 9.1 Innovation version, introduces experimental features, including JavaScript support for stored procedures and the new vector data type, designed for modern applications in machine learning and analytics. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

## Feedback and support

If you have questions about or suggestions for working with Azure Database for MySQL Flexible Server, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.

## Related content

- [Azure Database for MySQL pricing](https://azure.microsoft.com/pricing/details/mysql/server/)
- [public documentation](index.yml)
- [troubleshooting common migration errors](../howto-troubleshoot-common-errors.md)
