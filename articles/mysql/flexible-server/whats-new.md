---
title: "What's New in Azure Database for MySQL"
description: Learn about recent updates to Azure Database for MySQL.
author: deepthiprasad
ms.author: deprasa
ms.reviewer: maghan
ms.date: 05/19/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - build-2025
---

# What's new in Azure Database for MySQL?

[Azure Database for MySQL](overview.md) Is an Azure Database service that provides more granular control and flexibility over database management functions and configuration settings. The service currently supports the community versions of MySQL 5.7 and 8.0.

This article summarizes new releases and features in the Azure Database for MySQL service.

For previously released features, visit [Azure Database for MySQL: Previous released features](whats-new-archive.md).

> [!NOTE]
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.
## November 2025

### Reader Endpoint (Private Preview) 
We’re excited to announce that the Reader Endpoint feature for Azure Database for MySQL is now ready for private preview.   
Reader Endpoint provides a dedicated read-only endpoint for read replicas, enabling automatic connection-based load balancing of read-only traffic across multiple replicas. This simplifies application architecture by offering a single endpoint for read operations, improving scalability and fault tolerance. Azure Database for MySQL supports up to 10 read replicas per primary server. By routing read-only traffic through the reader endpoint, application teams can efficiently manage connections and optimize performance without handling individual replica endpoints. Reader endpoints continuously monitor the health of replicas and automatically exclude any replica that exceeds the configured replication lag threshold or becomes unavailable. To enroll in the preview, please submit your details using this [form](https://aka.ms/mysqlearlyaccessenroll).  

### Rename Server (Private Preview)
We are excited to share that Azure Database for MySQL – Flexible Server now supports server renaming. With this new capability, you no longer need to restore or migrate to a new server instance just to change the server name. The feature is currently available in preview, and we recommend avoiding production workloads while trying it out.To enroll in the preview, please submit your details using this [form](https://aka.ms/mysqlearlyaccessenroll).  

## October 2025

###  General Availability of Dedicated SLB for HA enabled servers
We’re excited to announce the General Availability of Dedicated SLB in Azure Database for MySQL – Flexible Server for HA-enabled servers. This feature adds a dedicated Standard Load Balancer (SLB) to High Availability (HA) configurations for servers created with public access or private link. By managing the MySQL data traffic path, SLB removes the need for DNS changes during failover, significantly reducing failover time. Please note, this feature is not supported for servers using private access with VNet integration.[Learn More](concepts-high-availability.md#failover-process)

###  General Availability of Custom Port Support
We are excited to announce that custom port support for Azure Database for MySQL – Flexible Server is now generally available (GA). This long-requested feature gives you greater flexibility to align MySQL server deployments with your network and security requirements. By default, MySQL uses TCP port 3306; with this GA release, you can configure a custom port (between 25001 and 26000) when creating a new Azure Database for MySQL flexible server. [Learn more](concepts-networking.md#custom-port-support)

### Enhanced portal experience for high availability
We’ve updated the portal experience for High Availability (HA) options to make it more intuitive and aligned with Azure standards. To help customers run mission-critical workloads with zone-aware HA, the portal now prioritizes Zone-Redundant HA wherever available and displays SLA details alongside the selection for better clarity. If Zone-Redundant HA is not available, customers can enable Local Redundant HA. Additionally, we are rebranding “Same Zone” to Local Redundant to ensure consistency with Azure naming conventions.[Learn More](how-to-configure-high-availability.md)

### General Availability of Server Parameters support for `lower_case_table_names` in  Azure Database for MySQL- Flexible Server
For [MySQL version 8.0+](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html) you can configure `lower_case_table_names` only when you're initializing the server. For restore operations or replica server creation, the parameter will automatically be copied from the source server and cannot be changed. [Learn More](concepts-server-parameters.md#lower_case_table_names)


## September 2025

### Azure MySQL 8.4 General Available

We’re excited to announce that Azure Database for MySQL – Flexible Server now supports MySQL 8.4 in General Availability (GA). This means you can create new MySQL 8.4 servers on Azure fully supported for production workloads. MySQL 8.4 is a long-term supported release from the MySQL community, bringing the latest features and improvements while emphasizing stability. With Azure’s managed service, you get these new capabilities backed by Azure’s enterprise-grade reliability and support. In short, MySQL 8.4 GA opens the door for you to upgrade your databases and future-proof your MySQL environment on Azure. [Learn more](../concepts-version-policy.md#supported-mysql-versions)

## Aug 2025

### Cross subscription and cross resource-group placement in restore/replica provisioning workflow

You can now restore a server or create a read replica in a different subscription and resource group in Azure Database for MySQL – Flexible Server. This enhancement offers greater flexibility for cross-environment restores, resource organization, and subscription-level separation, helping meet governance and operational requirements. To learn more, visit [Point-in-time restore](how-to-restore-server-portal.md).

### Ability to delete on-demand backup

You can now delete on-demand backups in Azure Database for MySQL – Flexible Server, giving you greater control over backup management and storage costs. This feature allows you to remove on-demand backups that are no longer needed, helping maintain a cleaner backup inventory and optimize resource usage. To learn more, visit [Backup and restore](how-to-trigger-on-demand-backup.md#trigger-on-demand-backup)

## July 2025

### General Availability in new Azure regions

Azure Database for MySQL Flexible Server is now available in the following Azure regions:

- Chile Central

- Indonesia Central

- Malaysia West

### Self-Heal in Azure Database for MySQL (Public Preview)
The Self-Heal feature in Azure Database for MySQL empowers customers to resolve common server issues independently, without needing to open a support case. It provides a one-click repair experience that helps restore service health quickly and safely. [Learn more](./how-to-self-heal.md).

### Accelerated logs feature is now available in General Purpose service tier
Accelerated logs are now supported in the General Purpose service tier of Azure Database for MySQL – Flexible Server. Previously available only in the Memory-Optimized tier, this feature enhances performance and reduces transaction latency. Accelerated logs feature in General Purpose tier is available at an additional cost. [Learn more](./concepts-accelerated-logs.md).


### Automate scheduling of on-demand backups

Azure Database for MySQL now supports the ability to schedule on-demand backups using automation tasks. This feature gives you greater control and flexibility in managing on-demand backups for your Azure Database for MySQL Flexible Server instances. Learn more about the how to schedule an automation task [here](./create-automation-tasks.md#on-demand-backup-server-task).


### Configure backup interval for the automated backups

Azure Database for MySQL now supports ability to configure backup interval for the automatic backup’s taken by the system to improve restore speed. This new feature optimizes the process by introducing more frequent snapshots, thereby reducing the number of binlogs that need to be replayed for point-in-time restore and minimizing overall restore time. Learn more about the feature [here](./concepts-backup-restore.md#backup-frequency).

## June 2025

### Auto Initialization of Time Zones

Time zones are automatically loaded during server creation, removing the need for customers to manually execute the mysql.az_load_timezone stored procedure afterwards to load the time zone. For more information, refer to the server parameter details for [time_zone](concepts-server-parameters.md#time_zone)

## May 2025

### Configure backup interval for the automated backups (Preview)

Azure Database for MySQL now supports ability to configure backup interval for the automatic backup’s taken by the system to improve restore speed. The feature is currently available in limited regions, namely – West Central US and East Asia. Learn more about the feature [here](./concepts-backup-restore.md#backup-frequency).

### Enable Auto-Scale of IOPS for Faster Restore and Replica Provisions

Azure Database for MySQL now supports the ability to enable [autoscaling of IOPS](https://techcommunity.microsoft.com/blog/adformysql/autoscale-iops-for-azure-database-for-mysql---flexible-server---general-availabi/3884602) for both the source and target servers during restore operations and replica provisioning workflows. This enhancement helps accelerate the restore and replica provisioning process by temporarily boosting IOPS to meet the performance demands of these operations. Once provisioning is complete, you can disable the autoscale IOPS setting.

To learn more, visit [Point-in-time restore](how-to-restore-server-portal.md).

### High Availability with Dedicated Azure Standard Load Balancer (SLB) (preview)

A dedicated standard load balancer (SLB) in Azure Database for MySQL for High Availability (HA) enabled servers is now available for public preview. This feature adds a dedicated standard load balancer to the HA configuration, enabling low-latency, high-throughput distribution of front-end traffic across backend servers. This enhancement improves failover performance and ensures more efficient handling of MySQL data traffic. If you want to enable an SLB for your HA server, [file a support ticket with Azure Support.](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).

## March 2025

### New Built-in Stored Procedures for Plugin Management and Undo Log Cleanup

There are two new built-in stored procedures in Azure Database for MySQL, allowing customers to manage plugin settings and clean up undo logs without requiring support intervention:

- Validate Password Plugin Management:
  - Enable: `CALL az_install_validate_password_plugin();`
  - Disable: `CALL az_uninstall_validate_password_plugin();`
  - Once enabled, the plugin's configuration parameters are available on the Azure portal's **Server Parameters** page.

- Undo Log Cleanup:
  - A new stored procedure is available to clean up the **Undo Log** manually, preventing unnecessary storage consumption.

Refer to the [Built-in stored procedures in Azure Database for MySQL](./concepts-built-in-store-procedure.md) article to learn more about Azure Database for MySQL built-in store procedure

### Caching SHA-2 Password Plugin Now Exposed by Default

The `caching_sha2_password` plugin is now exposed to customers by default. Customers can enable and configure it by setting the relevant **Server Parameters** in the Azure portal.

### Default zone-resiliency for Business-Critical service tier (Rollback)
In response to customer feedback requesting flexibility in choosing their deployment type, we’ve decided to reverse the change that made zone-resiliency the default for the Business-Critical service tier.

## February 2025

### Known Issues

- Azure Advisor recommendations recommend enabling accelerated logs even after the feature is enabled on your Azure Database for MySQL server.

- For servers with [customer-managed keys (CMK)](concepts-customer-managed-key.md), enabling [accelerated logs](./concepts-accelerated-logs.md) might not work due to a current limitation. You can temporarily disable CMK, enable accelerated logs, and re-enable CMK as a workaround. 

  To learn more, visit [Accelerated logs](./concepts-accelerated-logs.md).

## January 2025

### Default zone-resiliency for Business-Critical service tier

You now benefit from the highest level of availability against infrastructure failures within an availability zone at no extra cost for mission-critical workloads running on the Business-Critical service tier. Regardless of whether your flexible servers are enabled with High Availability (HA), your server data and log files are hosted in zone-redundant storage by default. While zone-redundant HA-enabled servers continue to benefit from a 99.99% uptime SLA from the built-in zonal redundancy and hot standby, non-HA servers can recover quickly from zonal outages using zone-redundant backups. This enhancement applies to all new servers provisioned in the Business-Critical service tier.

> [!NOTE]
> Based on customer feedback requesting the ability to choose their preferred deployment type, we’ve decided to roll back Default zone-resiliency for Business-Critical service tier. Now, for both Memory-Optimized and General-Purpose servers, customers must select the High Availability (HA) mode either same-zone or zone-redundant at the time of server creation. This selection is final and cannot be modified later.

### Accelerated Logs enabled for all new Memory-Optimized servers

Accelerated Logs, a feature that significantly enhances the performance of Azure Database for MySQL flexible server instances, is now enabled by default for all new Business-Critical servers. Accelerated Logs offers a dynamic solution designed for high throughput needs, reducing latency with no extra cost. Existing Memory-Optimized servers can also enable Accelerated Logs through the Azure portal. [Accelerated logs feature in Azure Database for MySQL ](concepts-accelerated-logs.md).

## November 2024

### MySQL 8.4 LTS version support - Public Preview

Azure Database for MySQL now supports the MySQL 8.4 LTS version, bringing the latest MySQL capabilities to Azure. MySQL 8.4 LTS version offers enhanced replication features, expanded monitoring, and long-term support, making it ideal for production environments requiring stability and advanced management. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

### MySQL 9.1 innovation version support - Public Preview

Azure Database for MySQL now supports the MySQL 9.1 Innovation version and introduces experimental features, including JavaScript support for stored procedures and the new vector data type designed for modern applications in machine learning and analytics. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

## October 2024

**New B1 Servers are unavailable**

Starting November 1, 2024, new B1 servers are limited to ensure performance and reliability in light of ongoing security improvements. We recommend exploring alternative SKUs designed to support your needs while maintaining high service reliability. Thank you for your understanding as we work to improve your experience.

**What does this mean for you?**

- Limited Access: New B1s instances will be unavailable after 10/28/24.

- Existing deployments: Any current B1 instances are unaffected.
- Alternative options: Explore and consider using other SKUs, such as B1ms and B2s, which provide enhanced compute power and memory while supporting greater performance.

**Next Steps:**

- Review recommended alternative SKUs
- Access documentation for changing your SKU here:
  - [Azure portal](/azure/mysql/flexible-server/how-to-manage-server-portal)
  - [Azure CLI](/azure/mysql/flexible-server/how-to-manage-server-cli)
- Review the Usage Dashboard to monitor your current usage

## September 2024

- **Azure Database for MySQL Flexible Maintenance is now Generally Available**

  Azure Database for MySQL has officially released the Flexible Maintenance feature to General Availability (GA). This feature allows users to reschedule maintenance activities via the Azure CLI, providing enhanced control and flexibility. The rescheduled window has also been expanded to cover all available maintenance dates within the same region and the same round of maintenance instead of being limited to the 14-day window around the instance scheduled date.

  To learn more, visit [Scheduled maintenance](./concepts-maintenance.md#maintenance-reschedule).

## August 2024

- **Azure Database for MySQL now supports up to 8 TB in a single data file!**

  Azure Database for MySQL now supports single InnoDB data files up to **8 TB** in size, enabling users to store larger datasets within a single file. This enhancement reduces the need for data partitioning and streamlines database management, making it easier to handle substantial volumes of data using the InnoDB storage engine. [Learn more.](./concepts-server-parameters.md#innodb_file_per_table)

- **Major version upgrade support for Burstable compute tier**

  Azure Database for MySQL now offers major version upgrades for Burstable SKU compute tiers. This support automatically upgrades the compute tier to General Purpose SKU before performing the upgrade, ensuring sufficient resources. Customers can choose to revert to Burstable SKU after the upgrade. Additional costs might apply.

  To learn more, visit [Upgrade MySQL version](./how-to-upgrade.md#perform-a-planned-major-version-upgrade-using-the-azure-portal-for-burstable-sku-servers).

- **Deprecated Metrics Announcement**

  We want to inform you about the deprecation of the following metrics in Azure Database for MySQL.
  
  - Storage Throttle Count (deprecated)
  - Available Memory Bytes (deprecated)
  - MySQL Lock Row Lock Waits (deprecated)

These metrics are no longer supported and are removed from the monitoring by the end of August 2024. We recommend updating your monitoring and alerting configurations to exclude these metrics and use alternative metrics that provide similar insights.

## July 2024

- **Move from private access (virtual network integrated) network to public access or private link**

  Azure Database for MySQL Flexible Server can be transitioned from private access (virtual network Integrated) to public access, with the option to use Private Link. This functionality enables servers to switch from virtual network integrated to Private Link/Public infrastructure seamlessly, without altering the server name or migrating data, simplifying the process for customers. 

  To learn more, visit [Move from private access (virtual network integrated) network to public access or private link](concepts-networking-vnet.md#move-from-private-access-virtual-network-integrated-network-to-public-access-or-private-link).

- **Managed HSM support for Azure Database for MySQL Flexible Server (Generally Available)**

  We're excited to announce the General Availability (GA) of Azure Key Vault Managed HSM support for Customer Managed Keys (CMK) in Azure Database for MySQL Flexible Server. With Managed HSM, you can import your HSM-backed encryption keys using the CMK bring your key (BYOK) feature to protect data at rest in your Azure Database for MySQL Flexible Server instances while maintaining data residency and full control of your HSM keys.

To learn more, visit [Data encryption with customer managed keys](concepts-customer-managed-key.md).

## May 2024

- **Accelerated Logs in Azure Database for MySQL Flexible Server is now Generally Available**

  We're thrilled to announce the General Availability (GA) of the Accelerated Logs feature for Azure Database for MySQL Flexible Server. This feature is available within the Business-Critical service tier and significantly enhances the performance of Azure Database for MySQL Flexible Server instances. It offers a dynamic solution designed for high throughput needs, reducing latency with no additional cost. [Accelerated logs feature in Azure Database for MySQL—Flexible Server](concepts-accelerated-logs.md).

- **Support for storage up to 32 TB in Azure Database for MySQL Flexible Server is now Generally Available**

  We're excited to announce the general availability (GA) of storage support up to 32 TB in Azure Database for MySQL Flexible Server. The feature is available only in the Memory-Optimized service tier.

  To learn more, visit [Service tiers](concepts-service-tiers-storage.md).

## April 2024

- **Enhanced Memory Allocation in Azure Database for MySQL Flexible Server**

  In the April deployments, we introduced optimized memory allocation for Azure Database for MySQL Flexible Server. This refinement ensures a more accurate and efficient memory calculation for the MySQL Server component, allowing it to utilize available resources effectively for query processing and data management. [Azure Database for MySQL - Flexible Server service tiers](concepts-service-tiers-storage.md).

- **Enhanced Monitoring for Azure Database for MySQL Flexible Server: Introducing New Metrics**

  The newly added metrics include MySQL Uptime, MySQL History list length, MySQL Deadlocks, Active Transactions, and MySQL Lock Timeouts. These metrics provide a more detailed view of your server's performance, enabling you to monitor and optimize your database operations more effectively. In addition to these new metrics, we've also improved the Memory percent metric. It now offers more precise calculations of memory usage for the MySQL server (mysqld) process. [Monitor Azure Database for MySQL - Flexible Server](concepts-monitoring.md)

- **Microsoft Defender for Cloud supports Azure Database for MySQL Flexible Server (General Availability)**

  We're excited to announce the general availability of the Microsoft Defender for Cloud feature for Azure Database for MySQL Flexible Server in all service tiers. The Microsoft Defender Advanced Threat Protection feature simplifies the security management of Azure Database for MySQL Flexible Server instances. It monitors the server for anomalous or suspicious database activities to detect potential threats and provides security alerts for you to investigate and take appropriate action, allowing you to actively improve the security posture of your database without being a security expert. [What is Microsoft Defender for open-source relational databases](/azure/defender-for-cloud/defender-for-databases-introduction)

- **On-demand Backup and Export (Preview)**

  Azure Database for MySQL allows triggering an on-demand server backup and exporting it to an Azure storage account (Azure blob storage). The feature is currently in public preview and available only in public cloud regions.

To learn more, visit [Backup and restore](concepts-backup-restore.md).

- **Known Issues**

  While attempting to enable the Microsoft Defender for Cloud feature for an Azure Database for MySQL Flexible Server, you might encounter the following error: 'The server <server_name> is incompatible with Advanced Threat Protection. Contact Microsoft support to update the server to a supported version.' This issue can occur on MySQL Flexible Servers still awaiting an internal update. It's automatically resolved in the following internal update of your server. Alternatively, you can open a support ticket to expedite an immediate update."

## March 2024

- **Accelerated Logs now supports major version upgrades.**

  Accelerated Logs has now introduced support for [major version upgrade](how-to-upgrade.md), allowing an upgrade from MySQL version 5.7 to 8.0 with accelerated logs feature enabled.[Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md)

- **Support for Long-term retention of backups in Azure Database for MySQL Flexible Server (Preview)**

  This feature allows backups to be retained for up to 35 days and up to 10 years. [Backup and restore in Azure Database for MySQL - Flexible Server](concepts-backup-restore.md)

## February 2024

- **Accelerated Logs is now available for existing servers and three new regions.**

  Accelerated Logs, previously limited to servers created after November 14, is now accessible for all existing Memory-Optimized tier's **standalone** servers in the preview phase. Accelerated logs also support [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](concepts-azure-ad-authentication.md). Additionally, this feature has been extended to include three new regions: Japan East, Korea Central, and Poland Central. [Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md)

- **Known Issues**

  Due to a technical issue in this month's deployment, primary servers with read-replica are temporarily restricted from enabling the [accelerated logs](concepts-accelerated-logs.md) feature. Users should turn off the accelerated logs feature before creating a replica server. If you require assistance with accelerated logs and replica creation, open a [support ticket](https://azure.microsoft.com/support/create-ticket) for assistance.

To learn more, visit [Limitations](concepts-accelerated-logs.md#limitations).

- **Audit logs now support wild card entries**

  The server parameters now support wildcards in `audit_log_include_users` and `audit_log_exclude_users`, enhancing flexibility for specifying user inclusions and exclusions in audit logs.

- **Enhanced Audit Logging with CONNECTION_V2 for Comprehensive MySQL User Audits**

Server parameter [audit_log_events](./concepts-audit-logs.md#configure-audit-logging) now supports event CONNECTION_V2 for detailed connection logs, providing insights into user audits, connection status, and [error codes in MySQL](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html) interactions.

To Learn more, visit [Audit logging](./concepts-audit-logs.md#configure-audit-logging).

## Feedback and support

If you have questions about or suggestions for working with Azure Database for MySQL, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.

## Related content

- [Azure Database for MySQL pricing](https://azure.microsoft.com/pricing/details/mysql/server/)
- [Azure Database for MySQL documentation](../index.yml)
- [Troubleshoot errors](how-to-troubleshoot-common-errors.md)
- [Azure Database for MySQL: Previous released features](whats-new-archive.md)
