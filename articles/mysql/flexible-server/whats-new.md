---
title: "What's New in Azure Database for MySQL"
description: Learn about recent updates to Azure Database for MySQL.
author: deepthiprasad
ms.author: deprasa
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - build-2025
---

# What's new in Azure Database for MySQL?

[Azure Database for MySQL](overview.md) is an Azure Database service that provides more granular control and flexibility over database management functions and configuration settings. The service currently supports the community versions of MySQL 5.7 and 8.0.

This article summarizes new releases and features in the Azure Database for MySQL service.

For previously released features, visit [Azure Database for MySQL: Previous released features](whats-new-archive.md).

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## December 2025

### Azure MySQL Import CLI adds support for MySQL 8.4

Azure Database for MySQL - Import CLI now supports importing MySQL 8.4 workloads from on-premises environments or virtual machines directly into Azure Database for MySQL.

This update ensures that customers running the latest MySQL versions can seamlessly migrate their data to Azure with minimal effort, leveraging the simplicity and automation provided by the Import CLI tool. Whether you're modernizing your infrastructure or scaling to the cloud, this feature helps accelerate your migration journey while maintaining compatibility and performance. For more information, see [Migrate MySQL on-premises or Virtual Machine (VM) workload to Azure Database for MySQL with Azure Database for MySQL Import CLI](../migrate/migrate-external-mysql-import-cli.md).

## November 2025

### Reader Endpoint (Private Preview)

The Reader Endpoint feature for Azure Database for MySQL is now ready for private preview.

Reader Endpoint provides a dedicated read-only endpoint for read replicas, enabling automatic connection-based load balancing of read-only traffic across multiple replicas. This feature simplifies application architecture by offering a single endpoint for read operations, improving scalability and fault tolerance. Azure Database for MySQL supports up to 10 read replicas per primary server. By routing read-only traffic through the reader endpoint, application teams can efficiently manage connections and optimize performance without handling individual replica endpoints. Reader endpoints continuously monitor the health of replicas and automatically exclude any replica that exceeds the configured replication lag threshold or becomes unavailable. To enroll in the preview, submit your details using this [form](https://aka.ms/mysqlearlyaccessenroll).

### Rename Server (Private Preview)

Azure Database for MySQL - Flexible Server now supports server renaming. With this new capability, you no longer need to restore or migrate to a new server instance just to change the server name. The feature is currently in preview, and you should avoid production workloads while trying it out. To enroll in the preview, submit your details through this [form](https://aka.ms/mysqlearlyaccessenroll).

## October 2025

### General Availability of Dedicated SLB for HA enabled servers

Dedicated SLB in Azure Database for MySQL - Flexible Server for HA-enabled servers is now generally available (GA). This feature adds a dedicated Standard Load Balancer (SLB) to High Availability (HA) configurations for servers created with public access or private link. By managing the MySQL data traffic path, SLB removes the need for DNS changes during failover, significantly reducing failover time. This feature isn't supported for servers using private access with VNet integration. [Learn more](concepts-high-availability.md#failover-process)

### General Availability of Custom Port Support

Custom port support for Azure Database for MySQL - Flexible Server is now generally available (GA). This long-requested feature gives you greater flexibility to align MySQL server deployments with your network and security requirements. By default, MySQL uses TCP port 3306; with this GA release, you can configure a custom port (between 25001 and 26000) when creating a new Azure Database for MySQL flexible server. [Learn more](concepts-networking.md#custom-port-support)

### Enhanced portal experience for high availability

The portal experience for High Availability (HA) options is now more intuitive and aligned with Azure standards. To help customers run mission-critical workloads with zone-aware HA, the portal now prioritizes Zone-Redundant HA wherever available and displays SLA details alongside the selection for better clarity. If Zone-Redundant HA isn't available, customers can enable Local Redundant HA. Additionally, "Same Zone" is rebranded to Local Redundant to ensure consistency with Azure naming conventions. [Manage zone redundant high availability in Azure Database for MySQL with the Azure portal](how-to-configure-high-availability.md)

### General Availability of Server Parameters support for `lower_case_table_names` in Azure Database for MySQL- Flexible Server

For [MySQL version 8.0+](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html), you can configure `lower_case_table_names` only when you're initializing the server. For restore operations or replica server creation, the parameter is automatically copied from the source server and can't be changed. [Learn More](concepts-server-parameters.md#lower_case_table_names)

## September 2025

### Azure MySQL 8.4 General Available

Azure Database for MySQL - Flexible Server now supports MySQL 8.4 in General Availability (GA). This support means you can create new MySQL 8.4 servers on Azure fully supported for production workloads. MySQL 8.4 is a long-term supported release from the MySQL community, bringing the latest features and improvements while emphasizing stability. With Azure's managed service, you get these new capabilities backed by Azure's enterprise-grade reliability and support. In short, MySQL 8.4 GA opens the door for you to upgrade your databases and future-proof your MySQL environment on Azure. [Learn more](../concepts-version-policy.md#supported-mysql-versions)

## Aug 2025

### Cross subscription and cross resource-group placement in restore and replica provisioning workflow

You can now restore a server or create a read replica in a different subscription and resource group in Azure Database for MySQL - Flexible Server. This enhancement offers greater flexibility for cross-environment restores, resource organization, and subscription-level separation, helping you meet governance and operational requirements. For more information, see [Point-in-time restore in Azure Database for MySQL with the Azure portal](how-to-restore-server-portal.md).

### Ability to delete on-demand backup

You can now delete on-demand backups in Azure Database for MySQL - Flexible Server, giving you greater control over backup management and storage costs. This feature allows you to remove on-demand backups that you no longer need, helping you maintain a cleaner backup inventory and optimize resource usage. For more information, see [Backup and restore](how-to-trigger-on-demand-backup.md#trigger-on-demand-backup).

## July 2025

### General Availability in new Azure regions

Azure Database for MySQL Flexible Server is now available in the following Azure regions:

- Chile Central
- Indonesia Central
- Malaysia West

### Self-Heal in Azure Database for MySQL (Public Preview)

The Self-Heal feature in Azure Database for MySQL empowers customers to resolve common server issues independently, without needing to open a support case. It provides a one-click repair experience that helps restore service health quickly and safely. For more information, see [Self-Heal in Azure Database for MySQL (Public Preview)](how-to-self-heal.md).

### Accelerated logs feature is now available in General Purpose service tier

Accelerated logs are now supported in the General Purpose service tier of Azure Database for MySQL - Flexible Server. Previously available only in the Business Critical tier, this feature enhances performance and reduces transaction latency. The accelerated logs feature in the General Purpose tier is available at an extra cost. For more information, see [Accelerated logs in Azure Database for MySQL](concepts-accelerated-logs.md).

### Automate scheduling of on-demand backups

Azure Database for MySQL now supports the ability to schedule on-demand backups by using automation tasks. This feature gives you greater control and flexibility in managing on-demand backups for your Azure Database for MySQL Flexible Server instances. For more information, see [How to schedule an automation task](create-automation-tasks.md#on-demand-backup-server-task).

### Configure backup interval for the automated backups

Azure Database for MySQL now supports the ability to configure the backup interval for the automatic backups that the system takes to improve restore speed. This new feature optimizes the process by introducing more frequent snapshots, thereby reducing the number of binlogs that need to be replayed for point-in-time restore and minimizing overall restore time. For more information, see [Backup frequency](concepts-backup-restore.md#backup-frequency).

## June 2025

### Auto Initialization of Time Zones

Time zones are automatically loaded during server creation, removing the need for customers to manually execute the `mysql.az_load_timezone` stored procedure afterwards to load the time zone. For more information, refer to the server parameter details for [time_zone](concepts-server-parameters.md#time_zone).

## May 2025

### Configure backup interval for the automated backups (Preview)

Azure Database for MySQL now supports the ability to configure the backup interval for the automatic backups that the system takes to improve restore speed. The feature is currently available in limited regions, namely West Central US and East Asia. For more information, see [Backup frequency](concepts-backup-restore.md#backup-frequency).

### Enable Auto-Scale of IOPS for Faster Restore and Replica Provisions

Azure Database for MySQL now supports the ability to enable [autoscaling of IOPS](https://techcommunity.microsoft.com/blog/adformysql/autoscale-iops-for-azure-database-for-mysql---flexible-server---general-availabi/3884602) for both the source and target servers during restore operations and replica provisioning workflows. This enhancement helps accelerate the restore and replica provisioning process by temporarily boosting IOPS to meet the performance demands of these operations. After provisioning completes, you can disable the autoscale IOPS setting.

For more information, see [Point-in-time restore in Azure Database for MySQL with the Azure portal](how-to-restore-server-portal.md).

### High Availability with Dedicated Azure Standard Load Balancer (SLB) (preview)

A dedicated standard load balancer (SLB) in Azure Database for MySQL for High Availability (HA) enabled servers is now available for public preview. This feature adds a dedicated standard load balancer to the HA configuration, enabling low-latency, high-throughput distribution of front-end traffic across backend servers. This enhancement improves failover performance and ensures more efficient handling of MySQL data traffic. If you want to enable an SLB for your HA server, [file a support ticket with Azure Support](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).

## March 2025

### New built-in stored procedures for plugin management and undo log cleanup

Azure Database for MySQL now includes two built-in stored procedures that you can use to manage plugin settings and clean up undo logs without needing support intervention:

- Validate Password Plugin Management:
  - Enable: `CALL az_install_validate_password_plugin();`
  - Disable: `CALL az_uninstall_validate_password_plugin();`
  - After you enable the plugin, you can access its configuration parameters on the Azure portal's **Server Parameters** page.

- **Undo Log Cleanup**:
  - Use the new stored procedure to manually clean up the **Undo Log** and prevent unnecessary storage consumption.

For more information, see [Built-in stored procedures in Azure Database for MySQL](concepts-built-in-store-procedure.md).

### Caching SHA-2 password plugin now exposed by default

The `caching_sha2_password` plugin is now exposed to customers by default. Customers can enable and configure it by setting the relevant **Server Parameters** in the Azure portal.

### Default zone-resiliency for Business-Critical service tier (Rollback)

In response to customer feedback requesting flexibility in choosing their deployment type, we have reversed the change that made zone-resiliency the default for the Business-Critical service tier.

## February 2025

### Known Issues

- Azure Advisor recommendations recommend enabling accelerated logs even after the feature is enabled on your Azure Database for MySQL server.

- For servers with [customer-managed keys (CMK)](security-customer-managed-key.md), enabling [accelerated logs](concepts-accelerated-logs.md) might not work due to a current limitation. You can temporarily disable CMK, enable accelerated logs, and re-enable CMK as a workaround.

  To learn more, visit [Accelerated logs in Azure Database for MySQL](concepts-accelerated-logs.md).

## January 2025

### Default zone-resiliency for Business-Critical service tier

You now benefit from the highest level of availability against infrastructure failures within an availability zone at no extra cost for mission-critical workloads running on the Business-Critical service tier. Regardless of whether your flexible servers are enabled with High Availability (HA), your server data and log files are hosted in zone-redundant storage by default. While zone-redundant HA-enabled servers continue to benefit from a 99.99% uptime SLA from the built-in zonal redundancy and hot standby, non-HA servers can recover quickly from zonal outages using zone-redundant backups. This enhancement applies to all new servers provisioned in the Business-Critical service tier.

> [!NOTE]  
> Based on customer feedback requesting the ability to choose their preferred deployment type, we've decided to roll back Default zone-resiliency for Business-Critical service tier. Now, for both Business Critical and General-Purpose servers, customers must select the High Availability (HA) mode either same-zone or zone-redundant at the time of server creation. This selection is final and can't be modified later.

### Accelerated Logs enabled for all new Memory-Optimized servers

Accelerated Logs, a feature that significantly enhances the performance of Azure Database for MySQL flexible server instances, is now enabled by default for all new Business-Critical servers. Accelerated Logs offers a dynamic solution designed for high throughput needs, reducing latency with no extra cost. Existing Business Critical servers can also enable Accelerated Logs through the Azure portal. [Accelerated logs in Azure Database for MySQL](concepts-accelerated-logs.md).

## November 2024

### MySQL 8.4 LTS version support - Public Preview

Azure Database for MySQL now supports the MySQL 8.4 LTS version, bringing the latest MySQL capabilities to Azure. MySQL 8.4 LTS version offers enhanced replication features, expanded monitoring, and long-term support, making it ideal for production environments requiring stability and advanced management. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

### MySQL 9.1 innovation version support - Public Preview

Azure Database for MySQL now supports the MySQL 9.1 Innovation version and introduces experimental features, including JavaScript support for stored procedures and the new vector data type designed for modern applications in machine learning and analytics. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

## October 2024

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

- **Azure Database for MySQL Flexible Maintenance is now generally available**

  Azure Database for MySQL officially released the Flexible Maintenance feature to general availability (GA). This feature enables you to reschedule maintenance activities through the Azure CLI, giving you more control and flexibility. The rescheduled window now includes all available maintenance dates within the same region and the same round of maintenance, instead of being limited to the 14-day window around the instance scheduled date.

  To learn more, visit [Scheduled maintenance](concepts-maintenance.md#maintenance-reschedule).

## August 2024

- **Azure Database for MySQL now supports up to 8 TB in a single data file**

  Azure Database for MySQL now supports single InnoDB data files up to **8 TB** in size. By using this feature, you can store larger datasets within a single file. This enhancement reduces the need for data partitioning and streamlines database management, making it easier to handle substantial volumes of data by using the InnoDB storage engine. [Learn more](concepts-server-parameters.md#innodb_file_per_table).

- **Major version upgrade support for Burstable compute tier**

  Azure Database for MySQL now offers major version upgrades for Burstable SKU compute tiers. This support automatically upgrades the compute tier to General Purpose SKU before performing the upgrade, ensuring sufficient resources. You can choose to revert to Burstable SKU after the upgrade. Additional costs might apply.

  For more information, see [Upgrade MySQL version](how-to-upgrade.md#perform-a-planned-major-version-upgrade-using-the-azure-portal-for-burstable-sku-servers).

- **Deprecated metrics announcement**

  The following metrics in Azure Database for MySQL are deprecated:

  - Storage Throttle Count
  - Available Memory Bytes
  - MySQL Lock Row Lock Waits

These metrics aren't supported and are removed from monitoring by the end of August 2024. Update your monitoring and alerting configurations to exclude these metrics and use alternative metrics that provide similar insights.

## July 2024

- **Move from private access (virtual network integrated) network to public access or private link**

  You can transition Azure Database for MySQL Flexible Server from private access (virtual network integrated) to public access, with the option to use Private Link. By using this functionality, you can switch your server from virtual network integrated to Private Link or public infrastructure seamlessly, without altering the server name or migrating data.

  For more information, see [Move from private access (virtual network integrated) network to public access or private link](concepts-networking-vnet.md#move-from-private-access-virtual-network-integrated-network-to-public-access-or-private-link).

- **Managed HSM support for Azure Database for MySQL Flexible Server (Generally Available)**

  Azure Key Vault Managed HSM support for Customer Managed Keys (CMK) in Azure Database for MySQL Flexible Server is now generally available (GA). By using Managed HSM, you can import your HSM-backed encryption keys by using the CMK bring your key (BYOK) feature to protect data at rest in your Azure Database for MySQL Flexible Server instances while maintaining data residency and full control of your HSM keys.

For more information, see [Data encryption with customer managed keys for Azure Database for MySQL](security-customer-managed-key.md).

## May 2024

- **Accelerated Logs in Azure Database for MySQL Flexible Server is now Generally Available**

  The Accelerated Logs feature for Azure Database for MySQL Flexible Server is now generally available (GA). This feature is available within the Business-Critical service tier and significantly enhances the performance of Azure Database for MySQL Flexible Server instances. It offers a dynamic solution designed for high throughput needs, reducing latency with no extra cost. For more information, see [Accelerated logs in Azure Database for MySQL](concepts-accelerated-logs.md).

- **Support for storage up to 32 TB in Azure Database for MySQL Flexible Server is now Generally Available**

  Storage support up to 32 TB in Azure Database for MySQL Flexible Server is now generally available (GA). This feature is available only in the Business Critical service tier.

  For more information, see [Azure Database for MySQL - Flexible Server service tiers](concepts-service-tiers-storage.md).

## April 2024

- **Enhanced Memory Allocation in Azure Database for MySQL Flexible Server**

  In the April deployments, we introduced optimized memory allocation for Azure Database for MySQL Flexible Server. This refinement ensures a more accurate and efficient memory calculation for the MySQL Server component, allowing it to utilize available resources effectively for query processing and data management. [Azure Database for MySQL - Flexible Server service tiers](concepts-service-tiers-storage.md).

- **Enhanced Monitoring for Azure Database for MySQL Flexible Server: Introducing New Metrics**

  The newly added metrics include MySQL Uptime, MySQL History list length, MySQL Deadlocks, Active Transactions, and MySQL Lock Timeouts. These metrics provide a more detailed view of your server's performance, enabling you to monitor and optimize your database operations more effectively. In addition to these new metrics, the Memory percent metric now offers more precise calculations of memory usage for the MySQL server (mysqld) process. [Monitor Azure Database for MySQL - Flexible Server](concepts-monitoring.md)

- **Microsoft Defender for Cloud supports Azure Database for MySQL Flexible Server (General Availability)**

  Microsoft Defender for Cloud feature for Azure Database for MySQL Flexible Server is now generally available (GA) in all service tiers. The Microsoft Defender Advanced Threat Protection feature simplifies the security management of Azure Database for MySQL Flexible Server instances. It monitors the server for anomalous or suspicious database activities to detect potential threats and provides security alerts for you to investigate and take appropriate action, allowing you to actively improve the security posture of your database without being a security expert. [What is Microsoft Defender for open-source relational databases](/azure/defender-for-cloud/defender-for-databases-introduction)

- **On-demand Backup and Export (Preview)**

  Azure Database for MySQL allows triggering an on-demand server backup and exporting it to an Azure storage account (Azure blob storage). The feature is currently in public preview and available only in public cloud regions.

To learn more, visit [Backup and restore in Azure Database for MySQL](concepts-backup-restore.md).

- **Known Issues**

  While attempting to enable the Microsoft Defender for Cloud feature for an Azure Database for MySQL Flexible Server, you might encounter the following error: 'The server <server_name> is incompatible with Advanced Threat Protection. Contact Microsoft support to update the server to a supported version.' This error can occur on MySQL Flexible Servers that are waiting for an internal update. The error resolves automatically in the next internal update of your server. Alternatively, you can open a support ticket to expedite an immediate update.

## March 2024

- **Accelerated Logs now supports major version upgrades.**

  Accelerated Logs now supports [major version upgrade](how-to-upgrade.md), so you can upgrade from MySQL version 5.7 to 8.0 with the accelerated logs feature enabled. [Accelerated logs in Azure Database for MySQL](concepts-accelerated-logs.md)

- **Support for long-term retention of backups in Azure Database for MySQL Flexible Server (Preview)**

  This feature allows you to retain backups for up to 35 days and up to 10 years. [Backup and restore in Azure Database for MySQL](concepts-backup-restore.md)

## February 2024

- **Accelerated Logs is now available for existing servers and three new regions.**

  Accelerated Logs, previously limited to servers created after November 14, is now accessible for all existing Business Critical tier's **standalone** servers in the preview phase. Accelerated logs also support [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](security-entra-authentication.md). Additionally, this feature is available in three new regions: Japan East, Korea Central, and Poland Central. [Accelerated logs in Azure Database for MySQL](concepts-accelerated-logs.md)

- **Known Issues**

  Due to a technical issue in this month's deployment, primary servers with read-replica are temporarily restricted from enabling the [accelerated logs](concepts-accelerated-logs.md) feature. Turn off the accelerated logs feature before creating a replica server. If you need help with accelerated logs and replica creation, open a [support ticket](https://azure.microsoft.com/support/create-ticket) for assistance.

To learn more, visit [Limitations](concepts-accelerated-logs.md#limitations).

- **Audit logs now support wild card entries**

  The server parameters now support wildcards in `audit_log_include_users` and `audit_log_exclude_users`, enhancing flexibility for specifying user inclusions and exclusions in audit logs.

- **Enhanced Audit Logging with CONNECTION_V2 for Comprehensive MySQL User Audits**

Server parameter [audit_log_events](./concepts-audit-logs.md#configure-audit-logging) now supports event CONNECTION_V2 for detailed connection logs, providing insights into user audits, connection status, and [error codes in MySQL](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html) interactions.

To learn more, visit [Audit logging](./concepts-audit-logs.md#configure-audit-logging).

## Feedback and support

If you have questions or suggestions for working with Azure Database for MySQL, consider the following points of contact:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.

## Related content

- [Azure Database for MySQL pricing](https://azure.microsoft.com/pricing/details/mysql/server/)
- [Azure Database for MySQL documentation](../index.yml)
- [Troubleshoot errors commonly encountered during or post migration to Azure Database for MySQL - Flexible Server](how-to-troubleshoot-common-errors.md)
- [Azure Database for MySQL: Previous released features](whats-new-archive.md)
