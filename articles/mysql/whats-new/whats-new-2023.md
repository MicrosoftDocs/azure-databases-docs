---
title: What's new - 2023 archive
description: 2023 feature announcements for Azure Database for MySQL flexible server, listed newest first.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ai-usage: ai-assisted
---

# What's new in Azure Database for MySQL flexible server in 2023?

This article summarizes the 2023 feature announcements for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## December 2023

In December 2023, Azure Database for MySQL flexible server introduced maintenance and troubleshooting previews. The following updates add near-zero-downtime maintenance and direct access to server error logs.

- **Near Zero Downtime Maintenance for Azure Database for MySQL flexible server (Preview)**

  This feature significantly reduces maintenance-related downtime, typically maintaining operations under 60 seconds in most cases. Using planned failover in HA enabled servers, it updates the standby server first, followed by a failover to make it the primary, and concludes with updating the former primary server, ensuring minimal service disruption. [Learn more](../flexible-server/concepts-maintenance.md#near-zero-downtime-maintenance-public-preview)

- **Error logs under server logs for Azure Database for MySQL flexible server (Preview)**

  This new feature enables direct access to [MySQL Server error logs](https://dev.mysql.com/doc/refman/8.0/en/error-log.html), significantly improving the ability to troubleshoot issues and enhancing transparency and independence with Azure Database for MySQL flexible server.[Error logs in Azure Database for MySQL flexible server (Preview)](../flexible-server/concepts-error-logs.md)

## November 2023

In November 2023, Azure Database for MySQL flexible server expanded replica, configuration, and disaster recovery capabilities. The following updates cover replica provisioning, server parameters, accelerated logs, and universal geo restore.

- **Enhanced replica provisioning experience**

  The replica provisioning experience will now provide extra flexibility to modify the replica compute and storage settings during the provisioning workflow. You can modify the computing settings of the replica server at the time of provisioning instead of making the changes after provisioning the replica server. The feature will also enable the modification of the backup retention days of the replica server and the configuration of it to have a different value than that of the source server.

- **Modify multiple server parameters using Azure CLI**

  You can now conveniently update multiple server parameters for your Azure Database for MySQL flexible server instance using Azure CLI. [Learn more](../flexible-server/how-to-configure-server-parameters-cli.md#modify-a-server-parameter-value).

- **Accelerated logs in Azure Database for MySQL flexible server (Preview)**

  We're excited to announce a preview of the accelerated logs feature for Azure Database for MySQL's flexible server. This feature is available within the Memory Optimized service tier. Accelerated logs significantly enhance the performance of Azure Database for MySQL flexible server instances, offering a dynamic solution that is designed for high throughput needs that also reduces latency and optimizes cost efficiency. [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md).

- **Universal Geo Restore in Azure Database for MySQL flexible server (General Availability)**

  The Universal Geo Restore feature allows you to restore a source server instance to an alternate region from the Azure supported regions where the Azure Database for MySQL flexible server is [available](../flexible-server/overview.md#azure-regions). If a large-scale incident in a region results in the unavailability of a database application, then you can use this feature as a disaster recovery option to restore the server to an Azure-supported target region that's different from the source server region. [Learn more](../flexible-server/concepts-backup-restore.md#restore).

## October 2023

In October 2023, Azure Database for MySQL flexible server added new compute options for the Memory Optimized tier. The following updates introduce more vCore choices and document known issues.

- **Addition of New vCore Options in Azure Database for MySQL flexible server**

  We're excited to inform you that we have introduced 20 new vCores options under the Memory Optimized Service tier for Azure Database for MySQL flexible server. Find more information under [Compute Option for Azure Database for MySQL flexible server](../flexible-server/concepts-service-tiers-storage.md#service-tiers-size-and-server-types).

- **Known Issues**

  - When attempting to modify the User assigned managed identity and Key identifier in a single request while changing the CMK settings, the operation gets struck. We're working on the upcoming deployment for the permanent solution to address this issue. In the meantime, ensure that you perform the two operations of updating the User Assigned Managed Identity and Key identifier in separate requests. The sequence of these operations isn't critical, as long as the user-assigned identities have the necessary access to both key vaults.
  - We identified a known issue where customers are unable to initialize a new Custom Maintenance Window (CMW) configuration while creating or updating their Azure Database for MySQL flexible server instance using ARM/CLI/RestAPI. Currently, the CMW configuration can only be initially set up through the Azure portal. Subsequent modifications to the CMW can then be made during server updates. We're actively working to resolve this limitation. As a workaround, customers can manually set up a CMW for their MySQL server via the Azure portal before making any further changes through ARM/CLI/RestAPI.

## September 2023

In September 2023, Azure Database for MySQL flexible server brought maintenance, replication, networking, and migration enhancements. The following updates cover flexible maintenance, read replicas, private link, and single server migration.

- **Flexible Maintenance for Azure Database for MySQL flexible server (Public Preview)**

  Flexible Maintenance for Azure Database for MySQL flexible server enables a tailored maintenance schedule to suit your operational rhythm. This feature allows you to reschedule maintenance tasks within a maximum 14-day window and initiate on-demand maintenance, granting you unprecedented control over server upkeep timing. Stay tuned for more customizable experiences in the future. [Scheduled maintenance in Azure Database for MySQL](../flexible-server/concepts-maintenance.md).

- **Universal Cross Region Read Replica on Azure Database for MySQL flexible server (General Availability)**

  Azure Database for MySQL flexible server now supports Universal Read Replicas in Public regions. This feature allows you to replicate your data from an instance of Azure Database for MySQL flexible server to a read-only server in the Universal region, which could be any region from the list of Azure supported regions where Azure Database for MySQL flexible server is available. [Read replicas in Azure Database for MySQL](../flexible-server/concepts-read-replicas.md).

- **Private Link for Azure Database for MySQL flexible server (General Availability)**

  You can now enable private endpoints to provide a secure means to access the Azure Database for MySQL flexible server via a Private Link, allowing both public and private access simultaneously. If necessary, you have the choice to restrict public access, ensuring that connections are exclusively routed through private endpoints for heightened network security. It's also possible to configure or update Private Link settings either during or after the creation of the server. [Private Link for Azure Database for MySQL flexible server](../flexible-server/concepts-networking-private-link.md).

- **Azure MySQL Import Smart Defaults for Azure Database for MySQL single server to Azure Database for MySQL flexible server migration (Public Preview)**

  You can now migrate an Azure Database for MySQL single server instance to an Azure Database for MySQL flexible server instance by running a single CLI command with minimal inputs. The command leverages smart defaults for target Azure Database for MySQL flexible server provisioning based on the source server SKU and properties!

- **Nominate an eligible Azure Database for MySQL single server instance for in-place automigration to Azure Database for MySQL flexible server**

  If you own an Azure Database for MySQL single server workload with Basic or GP SKU, data storage used < 10 GiB, and no complex features (CMK, Microsoft Entra ID, Read Replica, Private Link) enabled, you can now nominate yourself (if not already scheduled by the service) for in-place automigration to Azure Database for MySQL flexible server by submitting your server details through this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4lhLelkCklCuumNujnaQ-ZUQzRKSVBBV0VXTFRMSDFKSUtLUDlaNTA5Wi4u).

## August 2023

In August 2023, Azure Database for MySQL flexible server added disaster recovery and MySQL 8.0 compatibility features. The following updates preview universal geo restore and add generated invisible primary keys.

- **Universal Geo Restore in Azure Database for MySQL flexible server (Public Preview)**

  The Universal Geo Restore feature allows you to restore a source server instance to an alternate region from the Azure supported regions where the Azure Database for MySQL flexible server is [available](../flexible-server/overview.md#azure-regions). If a large-scale incident in a region results in the unavailability of database applications, you can use this feature as a disaster recovery option to restore the server to an Azure-supported target region that's different from the source server region. [Learn more](../flexible-server/concepts-backup-restore.md#restore).

- **Generated Invisible Primary Key in Azure Database for MySQL flexible server**

  Azure Database for MySQL flexible server now supports [generated invisible primary key (GIPK)](https://dev.mysql.com/doc/refman/8.0/en/create-table-gipks.html) for MySQL version 8.0. With this change, by default, the value of the server system variable "[sql_generate_invisible_primary_key](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_generate_invisible_primary_key)" is ON for all Azure Database for MySQL flexible server instances on MySQL 8.0. With GIPK mode ON, MySQL generates an invisible primary key to any InnoDB table, which is newly created without an explicit primary key. Learn more about the GIPK mode: [Generated Invisible Primary Keys](../flexible-server/concepts-limitations.md#generated-invisible-primary-keys) and [Invisible Column Metadata](https://dev.mysql.com/doc/refman/8.0/en/invisible-columns.html#invisible-column-metadata).

## July 2023

In July 2023, Azure Database for MySQL flexible server made autoscale IOPS generally available. The following update lets the server scale IOPS automatically based on workload needs.

- **Autoscale IOPS in Azure Database for MySQL flexible server (General Availability)**

  You can now scale IOPS on demand without having to pre-provision a certain amount of IOPS. With this feature, you can now enjoy worry-free IO management in Azure Database for MySQL flexible server because the server scales IOPs up or down automatically depending on workload needs. With this feature, you pay only for the IO you use and no longer need to provision and pay for resources you aren't fully using, saving time and money. The autoscale IOPS feature eliminates the administration required to provide the best performance for Azure Database for MySQL flexible server customers at the lowest cost. [Learn more](../flexible-server/concepts-storage-iops.md#autoscale-iops).

## June 2023

In June 2023, Azure Database for MySQL flexible server added networking, encryption, and performance capabilities. The following updates cover private link, customer-managed key encryption, server parameters, and higher IOPS.

- **Private Link for Azure Database for MySQL flexible server (Preview)**

  You can now enable private access to the Azure Database for MySQL flexible server using Private Link. Azure Private Link essentially brings Azure services inside your private Virtual Network (virtual network). Using the private IP address, the Azure Database for MySQL flexible server instance is accessible just like any other resource within the virtual network. [Private Link for Azure Database for MySQL flexible server](../flexible-server/concepts-networking-private-link.md).

- **Enhanced Data Encryption with Customer Managed Keys for Azure Database for MySQL flexible server**

  Azure Database for MySQL flexible server now supports allowing access to Azure Key Vault from selected Vnets to enable data encryption using Customer-Managed Keys. [Data encryption with customer managed keys for Azure Database for MySQL](../flexible-server/security-customer-managed-key.md).

- **Server Parameters support for Azure Database for MySQL- flexible server**

  Contact our [support team](https://azure.microsoft.com/support/create-ticket) if you need assistance with the following server parameters.

  [lower_case_table_names](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lower_case_table_names): MySQL version 5.7 supports a value change to 2. Changing the value from two back to 1 isn't allowed. Contact our support team for assistance.

  [innodb_flush_log_at_trx_commit](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit): This parameter determines the level of strictness for commit operations to ensure ACID compliance. Changing the value from its default setting might result in data loss.

- **Max IOPS support for Azure Database for MySQL- flexible server**

  Memory Optimized SKU now supports 80 K IOPS, enabling enhanced performance with increased IO operations per second. [Learn more](../flexible-server/concepts-service-tiers-storage.md#service-tiers-size-and-server-types).

## May 2023

In May 2023, Azure Database for MySQL flexible server expanded replication and major version upgrade capabilities. The following updates cover geo-paired read replicas, GTID-based replication, and in-place major version upgrades.

- **Read-Replica in Geo-Paired Region on Azure Database for MySQL- flexible server (General Availability)**

  Azure Database for MySQL now supports cross-region read-replica in a geo-paired region. The feature allows you to replicate your data from an instance of Azure Database for MySQL flexible server to a read-only server in a geo-paired region. [Read replicas in Azure Database for MySQL](../flexible-server/concepts-read-replicas.md)

- **Support for data-in replication using GTID**

  flexible server now also supports [Replicate data into Azure Database for MySQL flexible server](../flexible-server/concepts-data-in-replication.md) using GTID based replication. You can also use this feature to configure data-in replication for HA-enabled servers. To learn more - see [how to configure data-in replication using GTID](../flexible-server/how-to-data-in-replication.md)

- **Major version upgrades from 5.7 to 8.0 for Azure Database for MySQL flexible server (General Availability)**

  The major version upgrade feature allows you to perform in-place upgrades of existing instances of Azure Database for MySQL flexible server from MySQL 5.7 to MySQL 8.0 with the select of a button, without any data movement or the need to make any application connection string changes. With the ability to upgrade your Azure Database for MySQL flexible server major version from 5.7 to 8.0, you'll gain access to performance enhancements, security improvements, and new features, such as Data Dictionary, JSON enhancements, and Windows functions. [Major version upgrade in Azure Database for MySQL](../flexible-server/how-to-upgrade.md)

## April 2023

In April 2023, Azure Database for MySQL flexible server documented a storage autogrow known issue. The following update describes the current behavior and its effect.

- **Known issues**

  When the [storage autogrow feature](../flexible-server/concepts-service-tiers-storage.md#storage-autogrow) is enabled and pre-provisioned [IOPS](../flexible-server/concepts-service-tiers-storage.md#iops) is increased, it might result in unexpected increase in the storage size of the instance. We're actively working to resolve this issue and will provide updates as soon as they're available.

## March 2023

In March 2023, Azure Database for MySQL flexible server added resource health monitoring and a more flexible restore experience. The following updates cover HA server health and restore configuration options.

- **Azure Resource Health**

  Use Azure Resource Health to monitor the health and availability of the HA-enabled server if there's a planned or unplanned failover. [High-availability in Azure Database for MySQL](../flexible-server/concepts-high-availability.md)

- **Enhanced restore experience**

  Restore experience provides extra flexibility to modify the compute and storage settings while provisioning the restored server. The restored server can currently be configured to have a higher compute tier, compute size, and storage than the source server at the time of provisioning. Options like "Storage autogrow", "Backup retention days," and "Geo-redundancy" can also be edited to have a different value than that of the source server.

## February 2023

In February 2023, Azure Database for MySQL flexible server introduced monitoring and engine configuration enhancements. The following updates cover metrics workbooks, major version upgrades, redo log management, and minor version changes.

- **Enhanced metrics workbook is now available**

  Monitor system's performance with our recently added [Enhanced Metrics](../flexible-server/concepts-monitoring.md#enhanced-metrics) workbook. With all enhanced metrics consolidated in one place, you can easily monitor and track your system's health and make informed decisions to improve its overall performance.

- **Major version upgrade is now back and available for use**

  The Major Version upgrade feature was temporarily disabled in the portal due to technical issues, but it's now back in use.
  If you encounter any issues with the upgrade feature, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we assist you.

- **Redo logs management in MySQL version 8.0**

  Starting from [MySQL version 8.0.30 and above](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-30.html), there's been a change in the way the redo log is configured. Instead of using the [innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size) variable, the redo log can now be easily adjusted from the available values using the [innodb_redo_log_capacity](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_redo_log_capacity) variable. [Learn more](https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html).

- **Unsupported Server Parameters**

  The ability to modify the [thread_handling](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html) parameter in the Azure Database for MySQL flexible server is discontinued considering the underlying architecture and performance.

- **Minor version upgrade for Azure Database for MySQL to 8.0.31**

  After this month's deployment, Azure Database for MySQL flexible server 8.0 will be running on minor version 8.0.31*, to learn more about changes coming in this minor version [visit Changes in MySQL 8.0.31 (General Availability)](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-31.html)

- **Known issues**

  Upgrade Option Unavailable in Portal: Following technical issues after this month's deployment, the Major Version Upgrade feature has been temporarily disabled. We apologize for any inconvenience. Our team is working on a solution, and the issue will be resolved in the next deployment cycle. If you require immediate assistance with the Major Version Upgrade, open a [support ticket](https://azure.microsoft.com/support/create-ticket/), and we assist you.

## Related content

- [What's new in Azure Database for MySQL flexible server in 2024](whats-new-2024.md)
- [What's new in Azure Database for MySQL flexible server in 2025](whats-new-2025.md)
- [What's new in Azure Database for MySQL flexible server in 2026](whats-new-2026.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)