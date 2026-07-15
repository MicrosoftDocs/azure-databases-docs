---
title: What's new - 2024 archive
description: 2024 feature announcements for Azure Database for MySQL flexible server, listed newest first.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, randolphwest
ms.date: 06/18/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ai-usage: ai-assisted
---

# What's new in Azure Database for MySQL flexible server in 2024?

This article summarizes the 2024 feature announcements for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## November 2024

In November 2024, Azure Database for MySQL flexible server added public preview support for new MySQL versions. The following updates introduce the MySQL 8.4 LTS and MySQL 9.1 Innovation versions.

### MySQL 8.4 LTS version support - Public Preview

Azure Database for MySQL now supports the MySQL 8.4 LTS version, bringing the latest MySQL capabilities to Azure. MySQL 8.4 LTS version offers enhanced replication features, expanded monitoring, and long-term support, making it ideal for production environments requiring stability and advanced management. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

### MySQL 9.1 innovation version support - Public Preview

Azure Database for MySQL now supports the MySQL 9.1 Innovation version and introduces experimental features, including JavaScript support for stored procedures and the new vector data type designed for modern applications in machine learning and analytics. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

## October 2024

In October 2024, Azure Database for MySQL flexible server changed SKU availability. The following update limits new B1 servers and recommends alternative SKUs.

**New B1 servers aren't available**

Starting November 1, 2024, new B1 servers are limited to ensure performance and reliability in light of ongoing security improvements. Explore alternative SKUs that support your needs while maintaining high service reliability. Thank you for your understanding as the product team works to improve your experience.

**What does this change mean for you?**

- Limited access: New B1 instances aren't available after October 28, 2024.

- Existing deployments: Current B1 instances aren't affected.
- Alternative options: Use other SKUs, such as B1ms and B2s, which provide enhanced compute power and memory while supporting greater performance.

**Next steps**:

- Review recommended alternative SKUs.
- Access documentation for changing your SKU:
  - [Azure portal](/azure/mysql/flexible-server/how-to-manage-server-portal)
  - [Azure CLI](/azure/mysql/flexible-server/how-to-manage-server-cli)
- Review the Usage Dashboard to monitor your current usage.

## September 2024

In September 2024, Azure Database for MySQL flexible server made Flexible Maintenance generally available. The following update lets you reschedule maintenance through the Azure CLI.

- **Azure Database for MySQL Flexible Maintenance is now generally available**

  Azure Database for MySQL officially released the Flexible Maintenance feature to general availability (GA). This feature enables you to reschedule maintenance activities through the Azure CLI, giving you more control and flexibility. The rescheduled window now includes all available maintenance dates within the same region and the same round of maintenance, instead of being limited to the 14-day window around the instance scheduled date.

  To learn more, visit [Scheduled maintenance](../flexible-server/concepts-maintenance.md#maintenance-reschedule).

## August 2024

In August 2024, Azure Database for MySQL flexible server expanded storage and upgrade capabilities. The following updates cover larger data files, Burstable tier major version upgrades, and metric deprecations.

- **Azure Database for MySQL now supports up to 8 TB in a single data file**

  Azure Database for MySQL now supports single InnoDB data files up to **8 TB** in size. By using this feature, you can store larger datasets within a single file. This enhancement reduces the need for data partitioning and streamlines database management, making it easier to handle substantial volumes of data by using the InnoDB storage engine. [Learn more](../flexible-server/concepts-server-parameters.md#innodb_file_per_table).

- **Major version upgrade support for Burstable compute tier**

  Azure Database for MySQL now offers major version upgrades for Burstable SKU compute tiers. This support automatically upgrades the compute tier to General Purpose SKU before performing the upgrade, ensuring sufficient resources. You can choose to revert to Burstable SKU after the upgrade. Additional costs might apply.

  For more information, see [Upgrade MySQL version](../flexible-server/how-to-upgrade.md#perform-a-planned-major-version-upgrade-using-the-azure-portal-for-burstable-sku-servers).

- **Deprecated metrics announcement**

  The following metrics in Azure Database for MySQL are deprecated:

  - Storage Throttle Count
  - Available Memory Bytes
  - MySQL Lock Row Lock Waits

These metrics aren't supported and are removed from monitoring by the end of August 2024. Update your monitoring and alerting configurations to exclude these metrics and use alternative metrics that provide similar insights.

## July 2024

In July 2024, Azure Database for MySQL flexible server added networking flexibility and security options. The following updates enable network mode transitions and Managed HSM support for customer-managed keys.

- **Move from private access (virtual network integrated) network to public access or private link**

  You can transition Azure Database for MySQL flexible server from private access (virtual network integrated) to public access, with the option to use Private Link. By using this functionality, you can switch your server from virtual network integrated to Private Link or public infrastructure seamlessly, without altering the server name or migrating data.

  For more information, see [Move from private access (virtual network integrated) network to public access or private link](../flexible-server/concepts-networking-vnet.md#move-from-private-access-virtual-network-integrated-network-to-public-access-or-private-link).

- **Managed HSM support for Azure Database for MySQL flexible server (Generally Available)**

  Azure Key Vault Managed HSM support for Customer Managed Keys (CMK) in Azure Database for MySQL flexible server is now generally available (GA). By using Managed HSM, you can import your HSM-backed encryption keys by using the CMK bring your key (BYOK) feature to protect data at rest in your Azure Database for MySQL flexible server instances while maintaining data residency and full control of your HSM keys.

For more information, see [Data encryption with customer managed keys for Azure Database for MySQL](../flexible-server/security-customer-managed-key.md).

## May 2024

In May 2024, Azure Database for MySQL flexible server brought accelerated logs and larger storage to general availability. The following updates are available in the applicable service tiers.

- **Accelerated Logs in Azure Database for MySQL flexible server is now Generally Available**

  The Accelerated Logs feature for Azure Database for MySQL flexible server is now generally available (GA). This feature is available within the Business-Critical service tier and significantly enhances the performance of Azure Database for MySQL flexible server instances. It offers a dynamic solution designed for high throughput needs, reducing latency with no extra cost. For more information, see [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md).

- **Support for storage up to 32 TB in Azure Database for MySQL flexible server is now Generally Available**

  Storage support up to 32 TB in Azure Database for MySQL flexible server is now generally available (GA). This feature is available only in the Memory Optimized service tier.

  For more information, see [Azure Database for MySQL flexible server service tiers](../flexible-server/concepts-service-tiers-storage.md).

## April 2024

In April 2024, Azure Database for MySQL flexible server added monitoring, security, and backup enhancements. The following updates cover memory allocation, new metrics, Microsoft Defender for Cloud, and on-demand backup and export.

- **Enhanced Memory Allocation in Azure Database for MySQL flexible server**

  In the April deployments, we introduced optimized memory allocation for Azure Database for MySQL flexible server. This refinement ensures a more accurate and efficient memory calculation for the MySQL Server component, allowing it to utilize available resources effectively for query processing and data management. [Azure Database for MySQL flexible server service tiers](../flexible-server/concepts-service-tiers-storage.md).

- **Enhanced Monitoring for Azure Database for MySQL flexible server: Introducing New Metrics**

  The newly added metrics include MySQL Uptime, MySQL History list length, MySQL Deadlocks, Active Transactions, and MySQL Lock Timeouts. These metrics provide a more detailed view of your server's performance, enabling you to monitor and optimize your database operations more effectively. In addition to these new metrics, the Memory percent metric now offers more precise calculations of memory usage for the MySQL server (mysqld) process. [Monitor Azure Database for MySQL flexible server](../flexible-server/concepts-monitoring.md)

- **Microsoft Defender for Cloud supports Azure Database for MySQL flexible server (General Availability)**

  Microsoft Defender for Cloud feature for Azure Database for MySQL flexible server is now generally available (GA) in all service tiers. The Microsoft Defender Advanced Threat Protection feature simplifies the security management of Azure Database for MySQL flexible server instances. It monitors the server for anomalous or suspicious database activities to detect potential threats and provides security alerts for you to investigate and take appropriate action, allowing you to actively improve the security posture of your database without being a security expert. [What is Microsoft Defender for open-source relational databases](/azure/defender-for-cloud/defender-for-databases-introduction)

- **On-demand Backup and Export (Preview)**

  Azure Database for MySQL allows triggering an on-demand server backup and exporting it to an Azure storage account (Azure blob storage). The feature is currently in public preview and available only in public cloud regions.

To learn more, visit [Backup and restore in Azure Database for MySQL](../flexible-server/concepts-backup-restore.md).

- **Known Issues**

  While attempting to enable the Microsoft Defender for Cloud feature for an Azure Database for MySQL flexible server, you might encounter the following error: 'The server <server_name> is incompatible with Advanced Threat Protection. Contact Microsoft support to update the server to a supported version.' This error can occur on MySQL flexible servers that are waiting for an internal update. The error resolves automatically in the next internal update of your server. Alternatively, you can open a support ticket to expedite an immediate update.

## March 2024

In March 2024, Azure Database for MySQL flexible server extended accelerated logs and backup retention. The following updates add major version upgrade support for accelerated logs and long-term backup retention.

- **Accelerated Logs now supports major version upgrades.**

  Accelerated Logs now supports [major version upgrade](../flexible-server/how-to-upgrade.md), so you can upgrade from MySQL version 5.7 to 8.0 with the accelerated logs feature enabled. [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md)

- **Support for long-term retention of backups in Azure Database for MySQL flexible server (Preview)**

  This feature allows you to retain backups for up to 35 days and up to 10 years. [Backup and restore in Azure Database for MySQL](../flexible-server/concepts-backup-restore.md)

## February 2024

In February 2024, Azure Database for MySQL flexible server expanded accelerated logs and audit logging. The following updates broaden accelerated logs availability and enhance audit log capabilities.

- **Accelerated Logs is now available for existing servers and three new regions.**

  Accelerated Logs, previously limited to servers created after November 14, is now accessible for all existing Memory Optimized tier's **standalone** servers in the preview phase. Accelerated logs also support [Microsoft Entra authentication for Azure Database for MySQL flexible server](../flexible-server/security-entra-authentication.md). Additionally, this feature is available in three new regions: Japan East, Korea Central, and Poland Central. [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md)

- **Known Issues**

  Due to a technical issue in this month's deployment, primary servers with read-replica are temporarily restricted from enabling the [accelerated logs](../flexible-server/concepts-accelerated-logs.md) feature. Turn off the accelerated logs feature before creating a replica server. If you need help with accelerated logs and replica creation, open a [support ticket](https://azure.microsoft.com/support/create-ticket) for assistance.

To learn more, visit [Limitations](../flexible-server/concepts-accelerated-logs.md#limitations).

- **Audit logs now support wild card entries**

  The server parameters now support wildcards in `audit_log_include_users` and `audit_log_exclude_users`, enhancing flexibility for specifying user inclusions and exclusions in audit logs.

- **Enhanced Audit Logging with CONNECTION_V2 for Comprehensive MySQL User Audits**

Server parameter [audit_log_events](../flexible-server/concepts-audit-logs.md#configure-audit-logging) now supports event CONNECTION_V2 for detailed connection logs, providing insights into user audits, connection status, and [error codes in MySQL](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html) interactions.

To learn more, visit [Audit logging](../flexible-server/concepts-audit-logs.md#configure-audit-logging).

## Related content

- [Azure Database for MySQL flexible server release notes 2024](../release-notes/release-notes-2024.md)
- [What's new in Azure Database for MySQL flexible server in 2025](whats-new-2025.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)


