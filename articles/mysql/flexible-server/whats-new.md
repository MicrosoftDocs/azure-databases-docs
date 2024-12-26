---
title: "What's New"
description: Learn about recent updates to Azure Database for MySQL.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: vamehta, maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom:
  - mvc
  - references_regions
  - ignite-2024
---

# What's new in Azure Database for MySQL

[What is Azure Database for MySQL - Flexible Server?](overview.md) is a deployment mode designed to provide more granular control and flexibility over database management functions and configuration settings than the Azure Database for MySQL single server deployment mode. The service currently supports the community versions of MySQL 5.7 and 8.0.

This article summarizes new releases and features in the Azure Database for MySQL Flexible Server, which will begin in January 2021. Listings appear in reverse chronological order, with the most recent updates first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## November 2024

**MySQL 8.4 LTS version support - Public Preview**

Azure MySQL Flexible Server now supports MySQL 8.4 LTS version, bringing the latest MySQL capabilities to Azure. MySQL 8.4 LTS version offers enhanced replication features, expanded monitoring, and long-term support, making it ideal for production environments requiring stability and advanced management. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

**MySQL 9.1 innovation version support - Public Prevew**

Azure MySQL Flexible Server now supports MySQL 9.1 Innovation version, introduces experimental features, including JavaScript support for stored procedures and the new vector data type, designed for modern applications in machine learning and analytics. [Azure Database for MySQL version support policy](../concepts-version-policy.md)

> [!NOTE]  
> Due to Azure deployment restrictions during the holiday season, some users may not see the options for Azure MySQL versions 8.4 and 9.1 when creating a new server. For affected customers, you can send the subscription ID you wish to enroll in the Azure MySQL 8.4 and 9.1 public preview to this email address: AskAzureDBforMySQL@service.microsoft.com. Once we receive your email, we will unblock your subscription to enable selection of Azure MySQL 8.4 and 9.1.

## October 2024

**New B1s Servers are unavailable**

To ensure performance and reliability in light of ongoing security improvements, the creation of new B1s servers will be limited starting 11/1/2024. We recommend exploring alternative SKUs designed to better support your needs while maintaining high service reliability. Thank you for your understanding as we work to improve your experience.

**What does this mean for you?**

- Limited Access: New B1s instances will be unavailable after 10/28/24.

- Existing Deployments: Any current B1s instances will remain unaffected.
- Alternative Options: Explore and consider using other SKUs, such as B1ms and B2s, which provide enhanced compute power and memory while supporting greater performance.

**Next Steps:**
- Review recommended alternative SKUs
- Access documentation for changing your SKU here:
  - [Azure portal](/azure/mysql/flexible-server/how-to-manage-server-portal)
  - [Azure CLI](/azure/mysql/flexible-server/how-to-manage-server-cli)
- Review the Usage Dashboard to monitor your current usage

## September 2024

- **Azure Database for MySQL Flexible Server Flexible Maintenance is now Generally Available**

  Azure Database for MySQL Flexible Server has officially released the Flexible Maintenance feature to General Availability (GA). With this feature, users can now reschedule maintenance activities via the Azure CLI, providing enhanced control and flexibility. The reschedule window has also been expanded to cover all available maintenance dates within the same region and same round of maintenance, instead of being limited to the 14-day window around the instance's originally scheduled date.[Learn more](./concepts-maintenance.md#maintenance-reschedule)

## August 2024

- **Azure Database for MySQL Flexible Server now supports up to 8 TB in a single data file!**

  Azure Database for MySQL now supports single InnoDB data files up to **8 TB** in size, enabling users to store larger datasets within a single file. This enhancement reduces the need for data partitioning and streamlines database management, making it easier to handle substantial volumes of data using the InnoDB storage engine. [Learn more.](./concepts-server-parameters.md#innodb_file_per_table)

- **Major version upgrade support for Burstable compute tier**

  Azure Database for MySQL now offers major version upgrades for Burstable SKU compute tiers. This support automatically upgrades the compute tier to General Purpose SKU before performing the upgrade, ensuring sufficient resources. Customers can choose to revert back to Burstable SKU after the upgrade. Additional costs might apply. [Learn more](how-to-upgrade.md#perform-a-planned-major-version-upgrade-from-mysql-57-to-mysql-80-using-the-azure-portal-for-burstable-sku-servers)

- **Deprecated Metrics Announcement**

  We would like to inform you about the deprecation of the following metrics in Azure Database for MySQL Flexible Server.
  - Storage Throttle Count (deprecated)
  - Available Memory Bytes (deprecated)
  - MySQL Lock Row Lock Waits (deprecated)

  These metrics will no longer be supported and will be removed from the monitoring by the end of August 2024. We recommend updating your monitoring and alerting configurations to exclude these metrics and use alternative metrics that provide similar insights. For more information and guidance on alternative metrics, please refer to [azure monitoring documentation](concepts-monitoring.md)

## July 2024

- **Move from private access (virtual network integrated) network to public access or private link**

  Azure Database for MySQL Flexible Server can be transitioned from private access (virtual network Integrated) to public access, with the option to use Private Link. This functionality enables servers to switch from virtual network integrated to Private Link/Public infrastructure seamlessly, without the need to alter the server name or migrate data, simplifying the process for customers. [Learn more](concepts-networking-vnet.md#move-from-private-access-virtual-network-integrated-network-to-public-access-or-private-link)

- **Managed HSM support for Azure Database for MySQL Flexible Server (Generally Available)**

  We're excited to announce the General Availability (GA) of Azure Key Vault Managed HSM support for Customer Managed Keys (CMK) in Azure Database for MySQL Flexible Server. With Managed HSM you can import your own HSM-backed encryption keys using the CMK bring your own key (BYOK) feature to protect data at rest in your Azure Database for MySQL Flexible Server instances while maintaining data residency and full control of your HSM keys. [Learn more](/azure/mysql/flexible-server/concepts-customer-managed-key)

## May 2024

- **Accelerated Logs in Azure Database for MySQL Flexible Server is now Generally Available**

  We're thrilled to announce the General Availability (GA) of the Accelerated Logs feature for Azure Database for MySQL Flexible Server. This feature is available within the Business-Critical service tier, which significantly enhances the performance of Azure Database for MySQL Flexible Server instances. It offers a dynamic solution designed for high throughput needs, reducing latency with no additional cost. [Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md).

- **Support for storage up to 32 TB in Azure Database for MySQL Flexible Server is now Generally Available**

  We're excited to announce the general availability (GA) of storage support up to 32 TB in Azure Database for MySQL Flexible Server. The feature is available only in the Business Critical service tier. To learn more, visit [service tiers](concepts-service-tiers-storage.md).

## April 2024

- **Enhanced Memory Allocation in Azure Database for MySQL Flexible Server**

  In the April deployments, we introduced optimized memory allocation for Azure Database for MySQL Flexible Server. This refinement ensures a more accurate and efficient memory calculation for the MySQL Server component, allowing it to utilize available resources effectively for query processing and data management. [Azure Database for MySQL - Flexible Server service tiers](concepts-service-tiers-storage.md).

- **Enhanced Monitoring for Azure Database for MySQL Flexible Server: Introducing New Metrics**

  The newly added metrics include MySQL Uptime, MySQL History list length, MySQL Deadlocks, Active Transactions, and MySQL Lock Timeouts. These metrics provide a more detailed view of your server's performance, enabling you to monitor and optimize your database operations more effectively. In addition to these new metrics, we've also improved the Memory percent metric. It now offers more precise calculations of memory usage for the MySQL server (mysqld) process. [Monitor Azure Database for MySQL - Flexible Server](concepts-monitoring.md)

- **Microsoft Defender for Cloud supports Azure Database for MySQL Flexible Server (General Availability)**

  We're excited to announce the general availability of the Microsoft Defender for Cloud feature for Azure Database for MySQL Flexible Server in all service tiers. The Microsoft Defender Advanced Threat Protection feature simplifies the security management of Azure Database for MySQL Flexible Server instances. It monitors the server for anomalous or suspicious database activities to detect potential threats and provides security alerts for you to investigate and take appropriate action, allowing you to actively improve the security posture of your database without being a security expert. [What is Microsoft Defender for open-source relational databases](/azure/defender-for-cloud/defender-for-databases-introduction)
- **On-demand backup and Export (Preview)**

  Azure Database for MySQL Flexible Server now allows triggering an on-demand server backup and exporting it to an Azure storage account (Azure blob storage). The feature is currently in public preview and available only in public cloud regions. [Learn more](./concepts-backup-restore.md#on-demand-backup-and-export-preview)
- **Known Issues**

  While attempting to enable the Microsoft Defender for Cloud feature for an Azure Database for MySQL Flexible Server, you might encounter the following error: 'The server <server_name> is incompatible with Advanced Threat Protection. Contact Microsoft support to update the server to a supported version.' This issue can occur on MySQL Flexible Servers still awaiting an internal update. It's automatically resolved in the following internal update of your server. Alternatively, you can open a support ticket to expedite an immediate update."

## March 2024

- **Accelerated Logs now supports major version upgrades.**

   Accelerated Logs has now introduced support for [major version upgrade](how-to-upgrade.md), allowing an upgrade from MySQL version 5.7 to MySQL version 8.0 with accelerated logs feature enabled.[Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md)

- **Support for Long-term retention of backups in Azure Database for MySQL Flexible Server (Preview)**

  This feature allows backups to be retained for up to 35 days and up to 10 years. [Backup and restore in Azure Database for MySQL - Flexible Server](concepts-backup-restore.md)

## February 2024

- **Accelerated Logs is now available for existing servers and three new regions.**

  Accelerated Logs, previously limited to servers created after November 14, is now accessible for all existing Business Critical tier's **standalone** servers in the preview phase. Accelerated logs also support [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](concepts-azure-ad-authentication.md). Additionally, this feature has been extended to include three new regions: Japan East, Korea Central, and Poland Central. [Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md)

- **Known Issues**

  Due to a technical issue in this month's deployment, primary servers with read-replica are temporarily restricted from enabling the [accelerated logs](concepts-accelerated-logs.md) feature. Users should turn off the accelerated logs feature before creating a replica server. If you require assistance with accelerated logs and replica creation, open a [support ticket](https://azure.microsoft.com/support/create-ticket) for assistance. [Learn more](./concepts-accelerated-logs.md#limitations).

- **Audit logs now support wild card entries**

  The server parameters now support wildcards in `audit_log_include_users` and `audit_log_exclude_users`, enhancing flexibility for specifying user inclusions and exclusions in audit logs. [Learn more](./concepts-audit-logs.md#configure-audit-logging)

- **Enhanced Audit Logging with CONNECTION_V2 for Comprehensive MySQL User Audits**

  Server parameter [audit_log_events](./concepts-audit-logs.md#configure-audit-logging) now supports event CONNECTION_V2 for detailed connection logs, providing insights into user audits, connection status, and [error codes in MySQL](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html) interactions.[Learn more](./concepts-audit-logs.md#analyze-logs-in-azure-monitor-logs)

## December 2023

- **Near Zero Downtime Maintenance for Azure Database for MySQL Flexible Server (Preview)**

  This feature significantly reduces maintenance-related downtime, typically maintaining operations under 60 seconds in most cases. Using planned failover in HA enabled servers, it updates the standby server first, followed by a failover to make it the primary, and concludes with updating the former primary server, ensuring minimal service disruption.[Learn more](./concepts-maintenance.md#near-zero-downtime-maintenance-public-preview)

- **Error logs under server logs for Azure Database for MySQL Flexible Server (Preview)**

  This new feature enables direct access to [MySQL Server error logs](https://dev.mysql.com/doc/refman/8.0/en/error-log.html), significantly improving the ability to troubleshoot issues and enhancing transparency and independence with Azure Database for MySQL Flexible Server.[Error logs in Azure Database for MySQL - Flexible Server (Preview)](concepts-error-logs.md)

## November 2023

- **Enhanced replica provisioning experience**

  The replica provisioning experience will now provide extra flexibility to modify the replica compute and storage settings during the provisioning workflow. You can modify the computing settings of the replica server at the time of provisioning instead of making the changes after provisioning the replica server. The feature will also enable the modification of the backup retention days of the replica server and the configuration of it to have a different value than that of the source server.

- **Modify multiple server parameters using Azure CLI**

  You can now conveniently update multiple server parameters for your Azure Database for MySQL Flexible Server instance using Azure CLI. [Learn more](./how-to-configure-server-parameters-cli.md#modify-a-server-parameter-value).

- **Accelerated logs in Azure Database for MySQL Flexible Server (Preview)**

  We're excited to announce a preview of the accelerated logs feature for Azure Database for MySQL's Flexible Server. This feature is available within the Business Critical service tier. Accelerated logs significantly enhance the performance of Azure Database for MySQL Flexible Server instances, offering a dynamic solution that is designed for high throughput needs that also reduces latency and optimizes cost efficiency.[Accelerated logs feature in Azure Database for MySQL - Flexible Server](concepts-accelerated-logs.md).

- **Universal Geo Restore in Azure Database for MySQL Flexible Server (General Availability)**

  The Universal Geo Restore feature allows you to restore a source server instance to an alternate region from the Azure supported regions where the Azure Database for MySQL Flexible Server is [available](./overview.md#azure-regions). If a large-scale incident in a region results in the unavailability of a database application, then you can use this feature as a disaster recovery option to restore the server to an Azure-supported target region that's different from the source server region. [Learn more](concepts-backup-restore.md#restore).

## October 2023

- **Addition of New vCore Options in Azure Database for MySQL Flexible Server**

  We're excited to inform you that we have introduced 20 new vCores options under the Business Critical Service tier for Azure Database for MySQL Flexible Server. Find more information under [Compute Option for Azure Database for MySQL Flexible Server](./concepts-service-tiers-storage.md#service-tiers-size-and-server-types).

- **Known Issues**

  - When attempting to modify the User assigned managed identity and Key identifier in a single request while changing the CMK settings, the operation gets struck. We're working on the upcoming deployment for the permanent solution to address this issue. In the meantime, ensure that you perform the two operations of updating the User Assigned Managed Identity and Key identifier in separate requests. The sequence of these operations isn't critical, as long as the user-assigned identities have the necessary access to both key vaults.
  - We identified a known issue where customers are unable to initialize a new Custom Maintenance Window (CMW) configuration while creating or updating their Azure Database for MySQL Flexible Server instance using ARM/CLI/RestAPI. Currently, the CMW configuration can only be initially set up through the Azure portal. Subsequent modifications to the CMW can then be made during server updates. We're actively working to resolve this limitation. As a workaround, customers can manually set up a CMW for their MySQL server via the Azure portal before making any further changes through ARM/CLI/RestAPI.

## September 2023

- **Flexible Maintenance for Azure Database for MySQL Flexible Server (Public Preview)**

  Flexible Maintenance for Azure Database for MySQL Flexible Server enables a tailored maintenance schedule to suit your operational rhythm. This feature allows you to reschedule maintenance tasks within a maximum 14-day window and initiate on-demand maintenance, granting you unprecedented control over server upkeep timing. Stay tuned for more customizable experiences in the future. [Scheduled maintenance in Azure Database for MySQL - Flexible Server](concepts-maintenance.md).

- **Universal Cross Region Read Replica on Azure Database for MySQL Flexible Server (General Availability)**

  Azure Database for MySQL Flexible Server now supports Universal Read Replicas in Public regions. This feature allows you to replicate your data from an instance of Azure Database for MySQL Flexible Server to a read-only server in the Universal region, which could be any region from the list of Azure supported regions where Azure Database for MySQL Flexible Server is available. [Read replicas in Azure Database for MySQL - Flexible Server](concepts-read-replicas.md).

- **Private Link for Azure Database for MySQL Flexible Server (General Availability)**

  You can now enable private endpoints to provide a secure means to access the Azure Database for MySQL Flexible Server via a Private Link, allowing both public and private access simultaneously. If necessary, you have the choice to restrict public access, ensuring that connections are exclusively routed through private endpoints for heightened network security. It's also possible to configure or update Private Link settings either during or after the creation of the server. [Private Link for Azure Database for MySQL - Flexible Server](concepts-networking-private-link.md).

- **Azure MySQL Import Smart Defaults for Azure Database for MySQL single server to Azure Database for MySQL Flexible Server migration (Public Preview)**

  You can now migrate an Azure Database for MySQL single server instance to an Azure Database for MySQL Flexible Server instance by running a single CLI command with minimal inputs. The command leverages smart defaults for target Azure Database for MySQL Flexible Server provisioning based on the source server SKU and properties!

- **Nominate an eligible Azure Database for MySQL single server instance for in-place automigration to Azure Database for MySQL Flexible Server**

  If you own an Azure Database for MySQL single server workload with Basic or GP SKU, data storage used < 10 GiB, and no complex features (CMK, Microsoft Entra ID, Read Replica, Private Link) enabled, you can now nominate yourself (if not already scheduled by the service) for in-place automigration to Azure Database for MySQL Flexible Server by submitting your server details through this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4lhLelkCklCuumNujnaQ-ZUQzRKSVBBV0VXTFRMSDFKSUtLUDlaNTA5Wi4u).

## August 2023

- **Universal Geo Restore in Azure Database for MySQL Flexible Server (Public Preview)**

  The Universal Geo Restore feature allows you to restore a source server instance to an alternate region from the Azure supported regions where the Azure Database for MySQL Flexible Server is [available](./overview.md#azure-regions). If a large-scale incident in a region results in the unavailability of database applications, you can use this feature as a disaster recovery option to restore the server to an Azure-supported target region that's different from the source server region. [Learn more](concepts-backup-restore.md#restore).

- **Generated Invisible Primary Key in Azure Database for MySQL Flexible Server**

  Azure Database for MySQL Flexible Server now supports [generated invisible primary key (GIPK)](https://dev.mysql.com/doc/refman/8.0/en/create-table-gipks.html) for MySQL version 8.0. With this change, by default, the value of the server system variable "[sql_generate_invisible_primary_key](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_generate_invisible_primary_key)" is ON for all Azure Database for MySQL Flexible Server instances on MySQL 8.0. With GIPK mode ON, MySQL generates an invisible primary key to any InnoDB table, which is newly created without an explicit primary key. Learn more about the GIPK mode: [Generated Invisible Primary Keys](./concepts-limitations.md#generated-invisible-primary-keys) and [Invisible Column Metadata](https://dev.mysql.com/doc/refman/8.0/en/invisible-columns.html#invisible-column-metadata).

## July 2023

- **Autoscale IOPS in Azure Database for MySQL Flexible Server (General Availability)**

  You can now scale IOPS on demand without having to pre-provision a certain amount of IOPS. With this feature, you can now enjoy worry-free IO management in Azure Database for MySQL Flexible Server because the server scales IOPs up or down automatically depending on workload needs. With this feature, you pay only for the IO you use and no longer need to provision and pay for resources you aren't fully using, saving time and money. The autoscale IOPS feature eliminates the administration required to provide the best performance for Azure Database for MySQL Flexible Server customers at the lowest cost. [Learn more](./concepts-storage-iops.md#autoscale-iops).

## June 2023

- **Private Link for Azure Database for MySQL Flexible Server (Preview)**

  You can now enable private access to the Azure Database for MySQL Flexible Server using Private Link. Azure Private Link essentially brings Azure services inside your private Virtual Network (virtual network). Using the private IP address, the Azure Database for MySQL Flexible Server instance is accessible just like any other resource within the virtual network. [Private Link for Azure Database for MySQL - Flexible Server](concepts-networking-private-link.md).

- **Enhanced Data Encryption with Customer Managed Keys for Azure Database for MySQL Flexible Server**

  Azure Database for MySQL Flexible Server now supports allowing access to Azure Key Vault from selected Vnets to enable data encryption using Customer-Managed Keys. [Data encryption with customer managed keys for Azure Database for MySQL - Flexible Server](concepts-customer-managed-key.md).

- **Server Parameters support for Azure Database for MySQL- Flexible Server**

   contact our [support team](https://azure.microsoft.com/support/create-ticket) if you need assistance with the server parameters below.

  [lower_case_table_names] (https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lower_case_table_names ): MySQL version 5.7 supports a value change to 2. Changing the value from two back to 1 isn't allowed. contact our support team for assistance.

  [innodb_flush_log_at_trx_commit](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit): This parameter determines the level of strictness for commit operations to ensure ACID compliance. Changing the value from its default setting might result in data loss.

- **Max IOPS support for Azure Database for MySQL- Flexible Server**

  Business Critical SKU now supports 80 K IOPS, enabling enhanced performance with increased IO operations per second. [Learn more](./concepts-service-tiers-storage.md#service-tiers-size-and-server-types).

## May 2023

- **Read-Replica in Geo-Paired Region on Azure Database for MySQL- Flexible Server (General Availability)**

  Azure Database for MySQL now supports cross-region read-replica in a geo-paired region. The feature allows you to replicate your data from an instance of Azure Database for MySQL Flexible Server to a read-only server in a geo-paired region. [Read replicas in Azure Database for MySQL - Flexible Server](concepts-read-replicas.md)

- **Support for data-in replication using GTID**

  Flexible Server now also supports [Replicate data into Azure Database for MySQL - Flexible Server](concepts-data-in-replication.md) using GTID based replication. You can also use this feature to configure data-in replication for HA-enabled servers. To learn more - see [how to configure data-in replication using GTID](how-to-data-in-replication.md)

- **Major version upgrades from 5.7 to 8.0 for Azure Database for MySQL Flexible Server (General Availability)**

  The major version upgrade feature allows you to perform in-place upgrades of existing instances of Azure Database for MySQL Flexible Server from MySQL 5.7 to MySQL 8.0 with the select of a button, without any data movement or the need to make any application connection string changes. With the ability to upgrade your Azure Database for MySQL Flexible Server major version from 5.7 to 8.0, you'll gain access to performance enhancements, security improvements, and new features, such as Data Dictionary, JSON enhancements, and Windows functions. [Major version upgrade in Azure Database for MySQL - Flexible Server](how-to-upgrade.md)

## April 2023

- **Known issues**

  When the [storage autogrow feature](./concepts-service-tiers-storage.md#storage-autogrow) is enabled and pre-provisioned [IOPS](./concepts-service-tiers-storage.md#iops) is increased, it might result in unexpected increase in the storage size of the instance. We're actively working to resolve this issue and will provide updates as soon as they're available.

## March 2023

- **Azure Resource Health**

  Use Azure Resource Health to monitor the health and availability of the HA-enabled server if there's a planned or unplanned failover. [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md)

- **Enhanced restore experience**

  Restore experience provides extra flexibility to modify the compute and storage settings while provisioning the restored server. The restored server can currently be configured to have a higher compute tier, compute size, and storage than the source server at the time of provisioning. Options like "Storage autogrow", "Backup retention days," and "Geo-redundancy" can also be edited to have a different value than that of the source server.

## February 2023

- **Enhanced metrics workbook is now available**

  Monitor system's performance with our recently added [Enhanced Metrics](./concepts-monitoring.md#enhanced-metrics) workbook. With all enhanced metrics consolidated in one place, you can easily monitor and track your system's health and make informed decisions to improve its overall performance.

- **Major version upgrade is now back and available for use**

  The Major Version upgrade feature was temporarily disabled in the portal due to technical issues, but it's now back in use.
  If you encounter any issues with the upgrade feature, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we assist you.

- **Redo logs management in MySQL version 8.0**

  Starting from [MySQL version 8.0.30 and above](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-30.html), there has been a change in the way the redo log is configured. Instead of using the [innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size) variable, the redo log can now be easily adjusted from the available values using the [innodb_redo_log_capacity](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_redo_log_capacity) variable. [Learn more](https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html).

- **Unsupported Server Parameters**

  The ability to modify the [thread_handling](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html) parameter in the Azure Database for MySQL Flexible Server is discontinued considering the underlying architecture and performance.

- **Minor version upgrade for Azure Database for MySQL to 8.0.31**

  After this month's deployment, Azure Database for MySQL Flexible Server 8.0 will be running on minor version 8.0.31*, to learn more about changes coming in this minor version [visit Changes in MySQL 8.0.31 (2022-10-11, General Availability)](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-31.html)

- **Known issues**

  Upgrade Option Unavailable in Portal: Following technical issues after this month's deployment, the Major Version Upgrade feature has been temporarily disabled. We apologize for any inconvenience. Our team is working on a solution, and the issue will be resolved in the next deployment cycle. If you require immediate assistance with the Major Version Upgrade, open a [support ticket](https://azure.microsoft.com/support/create-ticket/), and we assist you.

## December 2022

- **New Replication Metrics**

  You can now have a better visibility into replication performance and health through newly exposed replication status metrics based on different replication types offered by Azure Database for MySQL- Flexible Server. [Learn More](./concepts-monitoring.md#replication-metrics)

- **Support for Data-out Replication**

  Azure Database for MySQL: Flexible Server now supports Data-out replication. This capability allows customers to synchronize data out of Azure Database for MySQL Flexible Server (source) to another MySQL (replica) which could be on-premises, in virtual machines, or a database service hosted outside of Azure. Learn more about [How to configure Azure Database for MySQL - Flexible Server data-out replication](how-to-data-out-replication.md).

## November 2022

- **Microsoft Entra IDauthentication for Azure Database for MySQL – Flexible Server (General Availability)**

  Using identities, you can now authenticate to Azure Database for MySQL using Microsoft Entra ID. With authentication, you can manage database user identities and other Microsoft services in a central location, simplifying permission management. [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](concepts-azure-ad-authentication.md)

- **Customer managed keys data encryption – Azure Database for MySQL – Flexible Server (General Availability)**

    With data encryption with customer-managed keys (CMKs) for Azure Database for MySQL Flexible Server Preview, you can bring your key (BYOK) for data protection at rest and implement separation of duties managing keys and data. Data encryption with CMKs is set at the server level. For a given server, a CMK, called the key encryption key (KEK), is used to encrypt the data encryption key (DEK) used by the service. With customer managed keys (CMKs), the customer is responsible for the full control of the key lifecycle management (key creation, upload, rotation, deletion), key usage permissions, and auditing operations on keys. [Data encryption with customer managed keys for Azure Database for MySQL - Flexible Server](concepts-customer-managed-key.md)

- **General availability in Azure US Government regions**
    Azure Database for MySQL Flexible Server is now available in the following Azure regions:
    - USGov Virginia
    - USGov Arizona
    - USGov Texas

- **Known issues**

  In specific scenario wherein if the source server if configured as Zone redundant HA and also enabled for Geo-redundancy, the geo-restore workflow fails if the target region doesn't have availability zone support.

## October 2022

- **AMD compute SKUs for General Purpose and Business Critical tiers in Azure Database for MySQL Flexible Server**

  You can now choose between Intel and AMD hardware for Azure Database for MySQL Flexible Server instances based on the General Purpose (Dadsv5-series) and Business Critical (Eadsv5-series) tiers. AMD SKU offers competitive price-performance options to all Azure Database for MySQL Flexible Server users. To ensure transparency in the portal, you can select the compute hardware vendor for both primary and secondary server. After determining the best compute processor for your workload, deploy Flexible Servers in more available regions and zones. [Azure Database for MySQL - Flexible Server service tiers](concepts-service-tiers-storage.md).

- **Autoscale IOPS in Azure Database for MySQL Flexible Server (Preview)**

  You can now scale IOPS on demand without having to pre-provision a certain amount of IOPS. With this feature, you can now enjoy worry free IO management in Azure Database for MySQL Flexible Server because the server scales IOPs up or down automatically depending on workload needs. With this feature, you pay only for the IO you use and no longer need to provision and pay for resources they aren't fully using, saving time and money. In addition, mission-critical Tier-1 applications can achieve consistent performance by making extra IO available to the workload anytime. Auto scale IO eliminates the administration required to provide the best performance for Azure Database for MySQL customers at the least cost. [Azure Database for MySQL - Flexible Server service tiers](concepts-service-tiers-storage.md)

- **Perform Major version upgrade with minimal efforts for Azure Database for MySQL Flexible Server (Preview)**

  The major version upgrade feature allows you to perform in-place upgrades of existing instances of Azure Database for MySQL Flexible Server from MySQL 5.7 to MySQL 8.0 with the select of a button, without any data movement or the need to make any application connection string changes. Take advantage of this functionality to efficiently perform major version upgrades on your instances of Azure Database for MySQL Flexible Server and use the latest MySQL 8.0 offers. [Major version upgrade in Azure Database for MySQL - Flexible Server](how-to-upgrade.md).

- **MySQL extension for Azure Data Studio (Preview)**

  When working with multiple databases across data platforms and cloud deployment models, performing the most common tasks on all your databases using a single tool enhances productivity several fold. With the MySQL extension for Azure Data Studio, you can now connect to and modify MySQL databases along with your other databases, taking advantage of the modern editor experience and capabilities in Azure Data Studio, such as IntelliSense, code snippets, source control integration, native Jupyter Notebooks, an integrated terminal, and more. Use this new tooling with any MySQL server hosted on-premises, on virtual machines, on managed MySQL in other clouds, and on Azure Database for MySQL Flexible Server. [Quickstart: Use Azure Data Studio to connect and query MySQL](/azure-data-studio/quickstart-mysql).

- **Enhanced metrics for better monitoring**

  You can now monitor more metrics under monitoring for your Azure Database for MySQL Flexible Server instance. Enhanced metrics allow you to have more visibility and monitor performance with [Innodb metrics](./concepts-monitoring.md#innodb-metrics) and troubleshoot database management operations with metrics like [DML statistics](./concepts-monitoring.md#dml-statistics) and [DDL statistics](./concepts-monitoring.md#ddl-statistics). [Learn more](./concepts-monitoring.md#enhanced-metrics)

- **Server parameters that are now configurable**

  List of server parameters that are now configurable.
  - [slave_transaction_retries](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-replica.html#sysvar_slave_transaction_retries)
  - [slave_checkpoint_period](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-replica.html#sysvar_slave_checkpoint_period)
  - [slave_checkpoint_group](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-replica.html#sysvar_slave_checkpoint_group)

- **Known issues**

  - Change of compute size isn't currently permitted after the [Major version upgrade in Azure Database for MySQL - Flexible Server](how-to-upgrade.md) of your Azure Database for MySQL Flexible Server instance. Changing the compute size of your Azure Database for MySQL Flexible Server instance is recommended before the major version upgrade from version 5.7 to version 8.0.

## September 2022

- **Read replica for HA enabled Azure Database for MySQL Flexible Server (General Availability)**

  The read replica feature allows you to replicate data from an Azure Database for MySQL Flexible Server instance to a read-only server. You can replicate the source server to up to 10 replicas. This functionality is now extended to support HA enabled servers within same region. [Read replicas in Azure Database for MySQL - Flexible Server](concepts-read-replicas.md).

- **Microsoft Entra IDauthentication for Azure Database for MySQL Flexible Server (Public Preview)**

  You can now authenticate to Azure Database for MySQL Flexible Server using Microsoft Entra ID using identities. With authentication, you can manage database user identities and other Microsoft services in a central location, simplifying permission management. [Microsoft Entra authentication for Azure Database for MySQL - Flexible Server](concepts-azure-ad-authentication.md).

- **Known issues**

  - The server parameter aad_auth_only stays set to ON only when the authentication type is changed to Microsoft Entra IDauthentication. We recommend disabling it manually when you opt for MySQL authentication only in the future.

  - The newly restored server will also have the server parameter aad_auth_only set to ON if it was ON on the source server during failover. You must manually disable this server parameter to use MySQL authentication on the restored server. Otherwise, an Admin must be configured.

- **Customer managed keys data encryption – Azure Database for MySQL Flexible Server (Preview)**

    With data encryption with customer-managed keys (CMKs) for Azure Database for MySQL Flexible Server Preview, you can bring your key (BYOK) for data protection at rest and implement separation of duties for managing keys and data. Data encryption with CMKs is set at the server level. For a given server, a CMK, called the key encryption key (KEK), is used to encrypt the data encryption key (DEK) used by the service. With customer managed keys (CMKs), the customer is responsible for the full control of the key lifecycle management (key creation, upload, rotation, deletion), key usage permissions, and auditing operations on keys. [Data encryption with customer managed keys for Azure Database for MySQL - Flexible Server](concepts-customer-managed-key.md).

- **Change Timezone of your Azure Database for MySQL Flexible Server instance in a single step**

   Previously to change time_zone of your Azure Database for MySQL Flexible Server instance required two steps to take effect. Now you no longer need to call the procedure mysql.az_load_timezone() to populate the mysql.time_zone_name table. Azure Database for MySQL Flexible Server timezone can be changed directly by just changing the server parameter time_zone from [portal](./how-to-configure-server-parameters-portal.md#working-with-the-time-zone-parameter) or [CLI](./how-to-configure-server-parameters-cli.md#working-with-the-time-zone-parameter).

- **Known issues**

  - The server parameter aad_auth_only stays set to ON only when the authentication type is changed to Microsoft Entra IDauthentication. We recommend disabling it manually when you opt for MySQL authentication only in the future.

  - The newly restored server will also have the server parameter aad_auth_only set to ON if it was ON on the source server during failover. To use MySQL authentication on the restored server, you must manually disable this server parameter. Otherwise, an Admin must be configured.

## August 2022

- **Server logs for Azure Database for MySQL Flexible Server**

    Server Logs help customers to emit the server logs to server storage space in file format, which you can later download. Slow query logs are supported with server logs, which can help customers in performance troubleshooting and query tuning. Customers can store logs for up to a week or up to 7 GB. You can configure or download them from [Enable and download server logs for Azure Database for MySQL - Flexible Server](how-to-server-logs-portal.md) or [List and download Azure Database for MySQL - Flexible Server logs by using the Azure CLI](how-to-server-logs-cli.md).[Learn more](./concepts-monitoring.md#server-logs).

- **On-Demand Backup for Azure Database for MySQL Flexible Server**

    The On-Demand backup feature allows customers to trigger On-Demand backups of their production workload, in addition to the automated backups taken by Azure Database for MySQL Flexible Server, and store them in alignment with the server's backup retention policy. These backups can be used as the fastest restore point to perform a point-in-time restore for faster and more predictable restore times. [Learn more](how-to-trigger-on-demand-backup.md#trigger-on-demand-backup).

- **Business Critical tier now supports Ev5 compute series**

    Business Critical tier for Azure Database for MySQL Flexible Server now supports the Ev5 compute series in more regions.
Learn more about [Boost Azure MySQL Business Critical Flexible Server performance by 30% with the Ev5 compute series!](https://techcommunity.microsoft.com/blog/adformysql/boost-azure-mysql-business-critical-flexible-server-performance-by-30-with-the-e/3603698)

- **Server parameters that are now configurable**

    List of dynamic server parameters that are now configurable:
    - [lc_time_names](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lc_time_names)
    - [replicate_wild_ignore_table](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table)
    - [slave_pending_jobs_size_max](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#sysvar_slave_pending_jobs_size_max)
    - [slave_parallel_workers](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#sysvar_slave_parallel_workers)
    - [log_output](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_log_output)
    - [performance_schema_max_digest_length](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-system-variables.html#sysvar_performance_schema_max_digest_length)
    - [performance_schema_max_sql_text_length](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-system-variables.html#sysvar_performance_schema_max_sql_text_length)

- **Known Issues**

  - When you try to connect to the server, you receive error "ERROR 9107 (HY000): Only Microsoft Entra IDaccounts are allowed to connect to server".

    Server parameter aad_auth_only was exposed in this month's deployment. Enabling server parameter aad_auth_only will block all non Microsoft Entra IDMySQL connections to your Azure Database for MySQL Flexible Server instance. We're currently working on extra configurations required for Microsoft Entra IDauthentication to be fully functional, and the feature will be available in the upcoming deployments. Wait to enable the aad_auth_only parameter until then.

## June 2022

- **Known Issues**

  You might no longer see logs uploaded to data sinks configured under diagnostics settings on a few servers where audit or slow logs are enabled. Verify whether your logs have the latest updated timestamp for the events based on the [data sink](./tutorial-query-performance-insights.md#set-up-diagnostics) you've configured. If your server is affected by this issue, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) so that we can apply a quick fix on the server to resolve the issue.

## May 2022

- **Announcing Azure Database for MySQL Flexible Server for business-critical workloads**
    Azure Database for MySQL Flexible Server Business Critical service tier is generally available. The Business Critical service tier is ideal for Tier 1 production workloads that require low latency, high concurrency, fast failover, and high scalability, such as gaming, e-commerce, and Internet-scale applications, to learn more about [Business Critical service Tier](https://techcommunity.microsoft.com/blog/adformysql/announcing-azure-database-for-mysql---flexible-server-for-business-critical-work/3361718).

- **Announcing the addition of new Burstable compute instances for Azure Database for MySQL Flexible Server**
    We're announcing the addition of new Burstable compute instances to support customers' autoscaling compute requirements from 1 vCore up to 20 vCores. learn more about [Compute Option for Azure Database for MySQL Flexible Server](./concepts-compute-storage.md).

- **Known issues**
  - The Reserved instances (RI) feature in Azure Database for MySQL Flexible Server isn't working properly for the Business Critical service tier after rebranding from the Memory Optimized service tier. Specifically, instance reservation has stopped working, and we're working to fix the issue.
  - Private DNS integration details aren't displayed on a few Azure Database for MySQL Database Flexible Server instances that have enabled HA. This issue doesn't impact the server's availability or name resolution. We're working on a permanent fix to resolve the issue, and it will be available in the next deployment. Meanwhile, suppose you want to view the Private DNS Zone details. In that case, you can either search under [Quickstart: Create an Azure private DNS zone using the Azure portal](/azure/dns/private-dns-getstarted-portal) in the Azure portal or you can perform a [manual failover](concepts-high-availability.md#planned-forced-failover) of the HA enabled Azure Database for MySQL Flexible Server instance and refresh the Azure portal.

## April 2022

- **Minor version upgrade for Azure Database for MySQL Flexible Server to 8.0.28**
    Azure Database for MySQL Flexible Server 8.0 now is running on minor version 8.0.28. To learn more about changes coming in this minor version, see [Changes in MySQL 8.0.28 (2022-01-18, General Availability)](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-28.html).

- **Minor version upgrade for Azure Database for MySQL Flexible Server to 5.7.37**
    Azure Database for MySQL Flexible Server 5.7 is now running on minor version 5.7.37. To learn more about changes coming in this minor version, see [Changes in MySQL 5.7.37 (2022-01-18, General Availability](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-37.html).

    > [!NOTE]  
    > Some regions are still running older minor versions of Azure Database for MySQL Flexible Server and will be patched by end of April 2022.

- **Deprecation of TLSv1 or TLSv1.1 protocols with Azure Database for MySQL Flexible Server (8.0.28)**

    Starting version 8.0.28, the MySQL community edition supports TLS protocol TLSv1.2 or TLSv1.3 only. Azure Database for MySQL Flexible Server will also stop supporting TLSv1 and TLSv1.1 protocols to align with modern security standards. You can no longer configure TLSv1 or TLSv1.1 from the server parameter pane for newly created and previously created resources. The default is TLSv1.2. Resources created before the upgrade still support communication through TLS protocol TLSv1 or TLS v1.1 through May 1, 2022.

## March 2022

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Migrate from locally redundant backup storage to geo-redundant backup storage for existing Flexible Server**
    Azure Database for MySQL Flexible Server provides the added flexibility to migrate to geo-redundant backup storage from locally redundant backup storage post server-create to provide higher data resiliency. Enabling geo-redundancy via the server's Compute + Storage page empowers customers to recover their existing Azure Database for MySQL Flexible Server instances from a geographic disaster or regional failure when they can't access the server in the primary region. With this feature enabled for their existing servers, customers can perform geo-restore and deploy a new server to the geo-paired Azure region using the original server's latest geo-redundant backup. [Backup and restore in Azure Database for MySQL - Flexible Server](concepts-backup-restore.md).

- **Simulate disaster recovery drills for your stopped servers**
    Azure Database for MySQL Flexible Server now provides the ability to perform geo-restore on stopped servers helping users simulate disaster recovery drills for their workloads to estimate impact and recovery time. This helps users plan better to meet their disaster recovery and business continuity objectives by using geo-redundancy feature offered by Azure Database for MySQL Flexible Server. [Point-in-time restore in Azure Database for MySQL - Flexible Server with Azure CLI](how-to-restore-server-cli.md).

## January 2022

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **All Operations are disabled on Stopped Azure Database for MySQL Flexible Server instances**
    Operations on servers in a [Stop](concept-servers.md#stop-and-start-a-server) state are disabled and show as inactive in the Azure portal. Operations that aren't supported on stopped servers include changing the pricing tier, number of vCores, storage size or IOPS, backup retention day, server tag, the server password, server parameters, storage autogrow, GEO backup, HA, and user identity.

- **Availability in three additional Azure regions**

   The public preview of Azure Database for MySQL Flexible Server is now available in the following Azure regions:
  - China East 2
  - China North 2

- **Reserving 36 IOPs for Azure Database for MySQL Flexible Server instances that have HA enabled**

    We're adding 36 IOPs and reserving them to support standby failover operation on servers that have enabled High Availability. This IOPs is in addition to the configured IOPs on your servers, so more monthly charges would apply based on your Azure region. The extra IOPS help us ensure our commitment to providing smooth failover experience from primary to standby replica. The added charge can be estimated by navigating to the [Azure Database for MySQL Flexible Server pricing page](https://azure.microsoft.com/pricing/details/mysql/flexible-server), choosing the Azure region for your server, and multiplying IOPs/month cost by 36 IOPs. For example, if your server is hosted in East US, the extra IO costs you can expect are $0.05*36 = USD 1.8 per month.

- **Bug fixes**

    Restart workflow struck issue with servers with HA, and Geo-redundant backup option enabled is fixed.

- **Known issues**

  - When you're using ARM templates for provisioning or configuration changes for HA enabled servers, if a single deployment is made to enable/disable HA and other server properties like backup redundancy, storage etc., then deployment would fail. You can mitigate it by submitting the deployment request separately to enable\disable and configuration changes. You don't have an issue with Portal or Azure CLI, as these requests are already separated.

  - When you're viewing automated backups for a HA enabled server on the Backup and Restore page, if at some point in time a forced or automatic failover is performed, you might lose viewing rights to the server's backups on the Backup and Restore page. Despite the invisibility of information regarding backups on the portal, the Flexible Server is successfully taking daily automated backups for the server in the backend. The server can be restored to any point within the retention period.

## November 2021

- **General Availability of Azure Database for MySQL Flexible Server**

  Azure Database for MySQL Flexible Server is now **General Availability** in more than [What is Azure Database for MySQL - Flexible Server?](overview.md) worldwide.

- **View available full backups in Azure portal**

  A dedicated Backup and Restore option is now available in the Azure portal. This page lists the backups available within the server's retention period, effectively providing a single pane view for managing a server's backups and consequent restores. You can use this option to:
     1) View the completion timestamps for all available full backups within the server's retention period
     2) Perform restore operations using these full backups

- **Fastest restore points**

  With the fastest restore point option, you can restore an Azure Database for MySQL Flexible Server instance in the fastest time possible on a given day within the server's retention period. This restore operation restores the full snapshot backup without requiring restore or recovery of logs. With fastest restore point, customers will see three options while performing point in time restores from Azure portal viz latest restore point, custom restore point and fastest restore point. [Learn more](concepts-backup-restore.md#point-in-time-restore).

- **FAQ in the Azure portal**

  The Backup and Restore page includes a section dedicated to listing your most frequently asked questions and answers. This should provide answers to most questions about backup directly within the Azure portal. In addition, selecting the question mark icon for FAQs on the top menu provides access to even more related detail.

- **Restore a deleted Azure Database for MySQL Flexible Server instance**

  The service now allows you to recover a deleted Azure Database for MySQL Flexible Server resource within five days from the time of server deletion. For a detailed guide on restoring a deleted server, [refer to the documented steps](how-to-restore-dropped-server.md). To protect server resources post deployment from accidental deletion or unexpected changes, we recommend administrators to use [management locks](/azure/azure-resource-manager/management/lock-resources).

- **Known issues**

    On servers with HA and Geo-redundant backup option enabled, we found a rare issue encountered by a race condition, which blocks the restart of the standby server to finish. As a result of this issue, when you fail over the HA enabled Azure Database for MySQL Flexible Server instance might get stuck in restarting state for a long time. The fix will be deployed to the production in the next deployment cycle.

## October 2021

- **Thread pools are now available for Azure Database for MySQL Flexible Server**

    Thread pools enhance the scalability of Azure Database for MySQL Flexible Server. Using a thread pool, users can optimize performance, achieve better throughput, and lower latency for high concurrent workloads. [Learn more](https://techcommunity.microsoft.com/category/azuredatabases/blog/adformysql).

- **Geo-redundant backup restore to geo-paired region for DR scenarios**

    The service now provides the flexibility to choose geo-redundant backup storage for higher data resiliency. Enabling geo-redundancy empowers customers to recover from a geographic disaster or regional failure when they can't access the server in the primary region. With this feature enabled, customers can perform geo-restore and deploy a new server to the geo-paired geographic region using the original server's latest geo-redundant backup. [Backup and restore in Azure Database for MySQL - Flexible Server](concepts-backup-restore.md).

- **Availability Zones Selection when creating Read replicas**

    When creating Read replica, you can select the Availability Zones location of your choice. An Availability Zone is a high availability offering that protects your applications and data from datacenter failures. Availability Zones are unique physical locations within an Azure region. [Read replicas in Azure Database for MySQL - Flexible Server](concepts-read-replicas.md).

- **Read replicas in Azure Database for MySQL Flexible Server will no longer be available on Burstable SKUs**

    If you have an existing Azure Database for MySQL Flexible Server instance with read replica enabled, you have to scale up your server to either General Purpose or Business Critical pricing tiers or delete the read replica within 60 days. After the 60 days, while you can continue to use the primary server for your read-write operations, replication to read replica servers will be stopped. For newly created servers, read replica option is available only for the General Purpose and Business Critical pricing tiers.

- **Monitoring Azure Database for MySQL Flexible Server with Azure Monitor Workbooks**

     Azure Database for MySQL Flexible Server is now integrated with Azure Monitor Workbooks. Workbooks provide a flexible canvas for data analysis and creating rich visual reports within the Azure portal. With this integration, the server has link to workbooks and few sample templates, which help to monitor the service at scale. These templates can be edited, customized to customer requirements and pinned to dashboard to create a focused and organized view of Azure resources. [Tutorial: Query Performance Insight for Azure Database for MySQL - Flexible Server](tutorial-query-performance-insights.md), [Tutorial: Configure audit logs by using Azure Database for MySQL - Flexible Server](tutorial-configure-audit.md), and Instance Overview templates are currently available. [Monitor Azure Database for MySQL - Flexible Server by using Azure Monitor workbooks](concepts-workbooks.md).

- **Prepay for Azure Database for MySQL Flexible Server compute resources with reserved instances**

    Azure Database for MySQL Flexible Server now helps you save money by prepaying for compute resources compared to pay-as-you-go prices. With Azure Database for MySQL Flexible Server reserved instances, you make an upfront commitment on Azure Database for MySQL Flexible Server for one or three years to get a significant discount on the compute costs. You can exchange a reservation from Azure Database for MySQL single server with Azure Database for MySQL Flexible Server. [Learn more](../concept-reserved-pricing.md).

- **Stopping the server for up to 30 days while the server is not in use**

    Azure Database for MySQL Flexible Server now allows you to Stop the server for up to 30 days when not in use and Start the server when you're ready to resume your development. This enables you to develop at your own pace and save development costs on the database servers by paying for the resources only when used. This is important for dev-test workloads and when you only use the server for part of the day. When you stop the server, all active connections are dropped. When the server is in the Stopped state, the server's compute isn't billed. However, storage continues to be billed as the server's storage remains to ensure that data files are available when the server is started again. [Learn more](concept-servers.md#stop-and-start-a-server).

- **Terraform Support for Azure Database for MySQL Flexible Server**

    Terraform support for Azure Database for MySQL Flexible Server is now released with the [latest v2.81.0 release of azurerm](https://github.com/hashicorp/terraform-provider-azurerm/blob/v2.81.0/CHANGELOG.md). The detailed reference document for provisioning and managing an Azure Database for MySQL Flexible Server instance using Terraform can be found [here](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mysql_flexible_server). Any bugs or known issues can be found or reported [here](https://github.com/hashicorp/terraform-provider-azurerm/issues).

- **Static Parameter innodb_log_file_size is now Configurable**

  - [innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size) can now be configured to any of these values: 256 MB, 512 MB, 1 GB, or 2 GB. Because it's a static parameter, it requires a server restart. If you've changed the parameter innodb_log_file_size from default, check if the "show global status like 'innodb_buffer_pool_pages_dirty'" stays at 0 for 30 seconds to avoid restart delay. See [Server parameters in Azure Database for MySQL - Flexible Server](concepts-server-parameters.md) to learn more.

- **Availability in two additional Azure regions**

   Azure Database for MySQL Flexible Server is now available in the following Azure regions:

  - US West 3
  - North Central US

[Learn more](overview.md#azure-regions).

- **Known Issues**
  - When a primary Azure region is down, you can't create geo-redundant servers in its geo-paired region as storage can't be provisioned in the primary Azure region. You must wait for the primary region to be up to provision geo-redundant servers in the geo-paired region.

## September 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Availability in three additional Azure regions**

   The public preview of Azure Database for MySQL Flexible Server is now available in the following Azure regions:

  - UK West
  - Canada East
  - Japan West

- **Bug fixes**

  Same-zone HA creation is fixed in the following regions:

  - Central India
  - East Asia
  - Korea Central
  - South Africa North
  - Switzerland North

## August 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **High availability within a single zone using Same-Zone High Availability**

  The service now allows customers to choose the preferred availability zone for their standby server when they enable high availability. With this feature, customers can place a standby server in the same zone as the primary server, which reduces the replication lag between primary and standby. This also provides lower latencies between the application server and database server if placed within the same Azure zone. [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md).

- **Standby zone selection using Zone-Redundant High Availability**

  The service now allows customers to choose the standby server zone location. Using this feature, customers can place their standby server in the zone of their choice. Colocating the standby database servers and applications in the same zone reduces latencies and allows customers to better prepare for disaster recovery situations and "zone down" scenarios. [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md).

- **Private DNS zone integration**

  [What is an Azure Private DNS zone?](/azure/dns/private-dns-privatednszone) provides a reliable and secure DNS service (responsible for translating a service name to IP address) for your virtual network. Azure Private DNS manages and resolves domain names in the virtual network without configuring a custom DNS solution. This enables you to connect your application running on a virtual network to your Azure Database for MySQL Flexible Server instance running on a locally or globally peered virtual network. Azure Database for MySQL Flexible Server now integrates with an Azure private DNS zone to allow seamless resolution of private DNS within the current virtual network, or any peered virtual network to which the private DNS zone is linked. With this integration, if the IP address of the backend Azure Database for MySQL Flexible Server instance changes during failover or any other event, your integrated private DNS zone is updated automatically to ensure your application connectivity resumes automatically once the server is online. [Private Network Access using virtual network integration for Azure Database for MySQL - Flexible Server](concepts-networking-vnet.md).

- **Point-In-Time Restore for a server in a specified virtual network**

  The Point-In-Time Restore experience for the service now enables customers to configure networking settings, allowing users to switch between private and public networking options when performing a restore operation. This feature allows customers to inject a server being restored into a specified virtual network securing their connection endpoints. [Point-in-time restore in Azure Database for MySQL - Flexible Server with the Azure portal](how-to-restore-server-portal.md).

- **Point-In-Time Restore for a server in an availability zone**

  The Point-In-Time Restore experience for the service now enables customers to configure availability zone. Colocating the database servers and standby applications in the same zone reduces latencies and allows customers to better prepare for disaster recovery situations and "zone down" scenarios. [High availability concepts in Azure Database for MySQL - Flexible Server](concepts-high-availability.md).

- **validate_password and caching_sha2_password plugin available in private preview**

  Azure Database for MySQL Flexible Server now supports enabling validate_password and caching_sha2_password plugins in preview. The validate_password plugin provides password policy enforcement and password strength validation. The caching_sha2_password plugin provides a more secure authentication method than the default mysql_native_password plugin. To learn more, visit [server parameters](concepts-server-parameters.md).

- **Availability in four additional Azure regions**

  The public preview of Azure Database for MySQL Flexible Server is now available in the following Azure regions:

  - Australia Southeast
  - South Africa North
  - East Asia (Hong Kong Special Administrative Region)
  - Central India

   [Learn more](overview.md#azure-regions).

- **Known issues**

  - Right after Zone-Redundant high availability server failover, clients fail to connect to the server if using SSL with ssl_mode VERIFY_IDENTITY. This issue can be mitigated by using ssl_mode as VERIFY_CA.
  - Unable to create Same-Zone High availability server in the following regions: Central India, East Asia, Korea Central, South Africa North, Switzerland North.
  - In a rare scenario and after HA failover, the primary server is in read_only mode. Resolve the issue by updating "read_only" value from the server parameters page to OFF.
  - After successfully scaling Compute on the Compute + Storage page, IOPS are reset to the SKU default. Customers can work around the issue by rescaling IOPs on the Compute + Storage page to desired value (previously set) post the compute deployment and consequent IOPS reset.

## July 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Online migration from Azure Database for MySQL single server to Azure Database for MySQL Flexible Server**

  Customers can now migrate an instance of Azure Database for MySQL single server to Azure Database for MySQL Flexible Server with minimum downtime to their applications using Data-in Replication. For detailed, step-by-step instructions, see [Migrate Azure Database for MySQL single server instances to Azure Database for MySQL Flexible Server with minimal downtime](../howto-migrate-single-flexible-minimum-downtime.md).

- **Availability in West US and Germany West Central**

  The public preview of Azure Database for MySQL Flexible Server is now available in the West US and Germany West Central Azure regions.

## June 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Improved performance on smaller storage servers**

    Beginning June 21, 2021, the minimum allowed provisioned storage size for all newly created server increases from 5 GB to 20 GB. In addition, the available free IOPS increases from 100 to 300. These changes are summarized in the following table:

    | **Current** | **As of June 21, 2021** |
    | :--- | :--- |
    | Minimum allowed storage size: 5 GB | Minimum allowed storage size: 20 GB |
    | IOPS available: Max(100, 3 * [Storage provisioned in GB]) | IOPS available: (300 + 3 * [Storage provisioned in GB]) |

- **Free 12-month offer**

  As of June 15, 2021, the [Azure free account](https://azure.microsoft.com/free/) provides customers up to 12 months of free access to Azure Database for MySQL Flexible Server with 750 hours of usage and 32 GB of storage per month. Customers can use this offer to develop and deploy applications that use Azure Database for MySQL Flexible Server. [Use an Azure free account to try Azure Database for MySQL - Flexible Server for free](how-to-deploy-on-azure-free-account.md).

- **Storage auto-grow**

  Storage auto grow prevents a server from running out of storage and becoming read-only. If storage auto grow is enabled, the storage automatically grows without affecting the workload. Beginning June 21, 2021, all newly created servers have storage auto grow enabled by default.
- **Data-in Replication**

    Azure Database for MySQL Flexible Server now supports [Replicate data into Azure Database for MySQL - Flexible Server](concepts-data-in-replication.md). Use this feature to synchronize and migrate data from a MySQL server running on-premises, in virtual machines, on Azure Database for MySQL single server, or database services outside Azure to Azure Database for MySQL Flexible Server. Learn more about [How to configure Azure Database for MySQL - Flexible Server data-in replication](how-to-data-in-replication.md).

- **GitHub Actions support with Azure CLI**

  Azure Database for MySQL Flexible Server CLI now allows customers to automate workflows to deploy updates with GitHub Actions. This feature helps set up and deploy database updates with MySQL GitHub Actions workflow. These CLI commands assist with setting up a repository to enable continuous deployment for ease of development. [Learn more](/cli/azure/mysql/flexible-server/deploy).

- **Zone redundant HA forced failover fixes**

  This release includes fixes for known issues related to forced failover to ensure that server parameters and more IOPS changes are persisted across failovers.

- **Known issues**

  - Trying to perform up a compute scale or scale down operation on an existing server with less than 20 GB of storage provisioned doesn't complete successfully. Resolve the issue by scaling the provisioned storage to 20 GB and retrying the compute scaling operation.

## May 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Extended regional availability (France Central, Brazil South, and Switzerland North)**

    The public preview of Azure Database for MySQL Flexible Server is now available in the France Central, Brazil South, and Switzerland North regions. [Learn more](overview.md#azure-regions).

- **SSL/TLS 1.2 enforcement can be disabled**

   This release provides the enhanced flexibility to customize SSL and minimum TLS version enforcement. To learn more, see [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](how-to-connect-tls-ssl.md).

- **Zone redundant HA available in UK South and Japan East region**

   Azure Database for MySQL Flexible Server now offers zone-redundant high availability in two more regions: UK South and Japan East. [Learn more](overview.md#azure-regions).

- **Known issues**

  - Additional IOPs changes don't take effect in zone redundant HA enabled servers. Customers can work around the issue by disabling HA, scaling IOPs, and the re-enabling zone redundant HA.
  - After force failover, the standby availability zone is inaccurately reflected in the portal. (No workaround)
  - Server parameter changes don't take effect in zone redundant HA enabled server after forced failover. (No workaround)

## April 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Ability to force failover to standby server with zone redundant high availability released**

  Customers can now manually force a failover to test functionality with their application scenarios, which can help them to prepare for any outages. [Learn more](https://techcommunity.microsoft.com/blog/adformysql/forced-failover-for-azure-database-for-mysql-%E2%80%93-flexible-server/2280671).

- **PowerShell module for Azure Database for MySQL Flexible Server released**

  Developers can now use PowerShell to provision, manage, operate, and support Azure Database for MySQL Flexible Server instances and dependent resources. [Learn more](https://techcommunity.microsoft.com/blog/adformysql/introducing-the-mysql-flexible-server-powershell-module/2203383).

- **Connect, test, and execute queries using Azure CLI**

  Azure Database for MySQL Flexible Server now provides an improved developer experience allowing customers to connect and execute queries to their servers using the Azure CLI with the "az mysql flexible-server connect" and "az mysql flexible-server execute" commands. [Learn more](connect-azure-cli.md#view-all-the-arguments).

- **Fixes for provisioning failures for server creates in virtual network with private access**

  All the provisioning failures caused when creating a server in virtual network are fixed. With this release, users can create Azure Database for MySQL Flexible Server instances with private access every time.

## March 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **MySQL 8.0.21 released**

  MySQL 8.0.21 is now available in Azure Database for MySQL Flexible Server in all major [Azure regions](overview.md#azure-regions). Customers can use the Azure portal, the Azure CLI, or Azure Resource Manager templates to provision the MySQL 8.0.21 release. [Learn more](quickstart-create-server-portal.md#create-an-azure-database-for-mysql-flexible-server).

- **Support for Availability zone placement during server creation released**

  Customers can now specify their preferred Availability zone during server creation. This functionality allows customers to collocate their applications hosted on Azure VM, Virtual Machine Scale Set, or AKS and database in the same Availability zones to minimize database latency and improve performance. [Learn more](quickstart-create-server-portal.md#create-an-azure-database-for-mysql-flexible-server).

- **Performance fixes for issues when running Azure Database for MySQL Flexible Server in virtual network with private access**

  Before this release, the performance of Azure Database for MySQL Flexible Server degraded significantly when running in virtual network configuration. This release includes the fixes for the issue, allowing users to see improved performance on Azure Database for MySQL Flexible Server in virtual network.

- **Known issues**

  - SSL\TLS 1.2 is enforced and can't be disabled. (No workarounds)
  - There are intermittent provisioning failures for servers provisioned in a virtual network. The workaround is to retry the server provisioning until it succeeds.

## February 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Additional IOPS feature released**

  Azure Database for MySQL Flexible Server supports provisioning more [IOPS](concepts-compute-storage.md#iops) independent of the storage provisioned. Customers can use this feature to increase or decrease the number of IOPS anytime based on their workload requirements.

- **Known issues**

  The performance of Azure Database for MySQL Flexible Server degrades with private access-virtual network isolation (No workaround).

## January 2021

This release of Azure Database for MySQL Flexible Server includes the following updates.

- **Up to 10 read replicas for Azure Database for MySQL Flexible Server**

  Azure Database for MySQL Flexible Server now supports asynchronous data replication from one Azure Database for MySQL Flexible Server instance (the 'source') to up to 10 Azure Database for MySQL Flexible Server instances (the 'replicas') in the same region. This functionality enables read-heavy workloads to scale out and be balanced across replica servers according to a user's preferences. [Read replicas in Azure Database for MySQL - Flexible Server](concepts-read-replicas.md).

## Feedback and support

If you have questions about or suggestions for working with Azure Database for MySQL Flexible Server, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.

## Related content

- [Azure Database for MySQL Flexible Server pricing](https://azure.microsoft.com/pricing/details/mysql/server/)
- [public documentation](index.yml)
- [troubleshooting common migration errors](../howto-troubleshoot-common-errors.md)
