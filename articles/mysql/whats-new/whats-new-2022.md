---
title: What's new - 2022 archive
description: 2022 feature announcements for Azure Database for MySQL flexible server, listed newest first.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom: references_regions
ai-usage: ai-assisted
---

# What's new in Azure Database for MySQL flexible server in 2022?

This article summarizes the 2022 feature announcements for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## December 2022

In December 2022, Azure Database for MySQL flexible server added replication metrics and data-out replication. The following updates improve replication visibility and enable synchronizing data to external MySQL replicas.

- **New Replication Metrics**

  You can now have a better visibility into replication performance and health through newly exposed replication status metrics based on different replication types offered by Azure Database for MySQL- flexible server. [Learn More](../flexible-server/concepts-monitoring.md#replication-metrics)

- **Support for Data-out Replication**

  Azure Database for MySQL: flexible server now supports Data-out replication. This capability allows customers to synchronize data out of Azure Database for MySQL flexible server (source) to another MySQL (replica) which could be on-premises, in virtual machines, or a database service hosted outside of Azure. Learn more about [How to configure Azure Database for MySQL flexible server data-out replication](../flexible-server/how-to-data-out-replication.md).

## November 2022

In November 2022, Azure Database for MySQL flexible server brought Microsoft Entra ID authentication and customer-managed keys to general availability. The following updates also expand availability in Azure US Government regions.

- **Microsoft Entra IDauthentication for Azure Database for MySQL flexible server (General Availability)**

  Using identities, you can now authenticate to Azure Database for MySQL using Microsoft Entra ID. With authentication, you can manage database user identities and other Microsoft services in a central location, simplifying permission management. [Microsoft Entra authentication for Azure Database for MySQL flexible server](../flexible-server/security-entra-authentication.md)

- **Customer managed keys data encryption - Azure Database for MySQL flexible server (General Availability)**

  With data encryption with customer-managed keys (CMKs) for Azure Database for MySQL flexible server Preview, you can bring your key (BYOK) for data protection at rest and implement separation of duties managing keys and data. Data encryption with CMKs is set at the server level. For a given server, a CMK, called the key encryption key (KEK), is used to encrypt the data encryption key (DEK) used by the service. With customer managed keys (CMKs), the customer is responsible for the full control of the key lifecycle management (key creation, upload, rotation, deletion), key usage permissions, and auditing operations on keys. [Data encryption with customer managed keys for Azure Database for MySQL](../flexible-server/security-customer-managed-key.md)

- **General availability in Azure US Government regions**
  Azure Database for MySQL flexible server is now available in the following Azure regions:
  - USGov Virginia
  - USGov Arizona
  - USGov Texas

- **Known issues**

  In specific scenario wherein if the source server if configured as Zone redundant HA and also enabled for Geo-redundancy, the geo-restore workflow fails if the target region doesn't have availability zone support.

## October 2022

In October 2022, Azure Database for MySQL flexible server added new compute options, upgrade previews, and monitoring enhancements. The following updates cover AMD SKUs, autoscale IOPS, major version upgrades, and more metrics.

- **AMD compute SKUs for General Purpose and Memory-Optimized tiers in Azure Database for MySQL flexible server**

  You can now choose between Intel and AMD hardware for Azure Database for MySQL flexible server instances based on the General Purpose (Dadsv5-series) and Memory-Optimized (Eadsv5-series) tiers. AMD SKU offers competitive price-performance options to all Azure Database for MySQL flexible server users. To ensure transparency in the portal, you can select the compute hardware vendor for both primary and secondary server. After determining the best compute processor for your workload, deploy flexible servers in more available regions and zones. [Azure Database for MySQL flexible server service tiers](../flexible-server/concepts-service-tiers-storage.md).

- **Autoscale IOPS in Azure Database for MySQL flexible server (Preview)**

  You can now scale IOPS on demand without having to pre-provision a certain amount of IOPS. With this feature, you can now enjoy worry free IO management in Azure Database for MySQL flexible server because the server scales IOPs up or down automatically depending on workload needs. With this feature, you pay only for the IO you use and no longer need to provision and pay for resources they aren't fully using, saving time and money. In addition, mission-critical Tier-1 applications can achieve consistent performance by making extra IO available to the workload anytime. Auto scale IO eliminates the administration required to provide the best performance for Azure Database for MySQL customers at the least cost. [Azure Database for MySQL flexible server service tiers](../flexible-server/concepts-service-tiers-storage.md)

- **Perform Major version upgrade with minimal efforts for Azure Database for MySQL flexible server (Preview)**

  The major version upgrade feature allows you to perform in-place upgrades of existing instances of Azure Database for MySQL flexible server from MySQL 5.7 to MySQL 8.0 with the select of a button, without any data movement or the need to make any application connection string changes. Take advantage of this functionality to efficiently perform major version upgrades on your instances of Azure Database for MySQL flexible server and use the latest MySQL 8.0 offers. [Major version upgrade in Azure Database for MySQL](../flexible-server/how-to-upgrade.md).

- **Enhanced metrics for better monitoring**

  You can now monitor more metrics under monitoring for your Azure Database for MySQL flexible server instance. Enhanced metrics allow you to have more visibility and monitor performance with [Innodb metrics](../flexible-server/concepts-monitoring.md#innodb-metrics) and troubleshoot database management operations with metrics like [DML statistics](../flexible-server/concepts-monitoring.md#dml-statistics) and [DDL statistics](../flexible-server/concepts-monitoring.md#ddl-statistics). [Learn more](../flexible-server/concepts-monitoring.md#enhanced-metrics)

- **Server parameters that are now configurable**

  List of server parameters that are now configurable.
  - [slave_transaction_retries](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-replica.html#sysvar_slave_transaction_retries)
  - [slave_checkpoint_period](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-replica.html#sysvar_slave_checkpoint_period)
  - [slave_checkpoint_group](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-replica.html#sysvar_slave_checkpoint_group)

- **Known issues**

  - Change of compute size isn't currently permitted after the [Major version upgrade in Azure Database for MySQL](../flexible-server/how-to-upgrade.md) of your Azure Database for MySQL flexible server instance. Changing the compute size of your Azure Database for MySQL flexible server instance is recommended before the major version upgrade from version 5.7 to version 8.0.

## September 2022

In September 2022, Azure Database for MySQL flexible server expanded replication, authentication, and encryption capabilities. The following updates cover HA read replicas, Microsoft Entra ID authentication, customer-managed keys, and time zone configuration.

- **Read replica for HA enabled Azure Database for MySQL flexible server (General Availability)**

  The read replica feature allows you to replicate data from an Azure Database for MySQL flexible server instance to a read-only server. You can replicate the source server to up to 10 replicas. This functionality is now extended to support HA enabled servers within same region. [Read replicas in Azure Database for MySQL](../flexible-server/concepts-read-replicas.md).

- **Microsoft Entra IDauthentication for Azure Database for MySQL flexible server (Public Preview)**

  You can now authenticate to Azure Database for MySQL flexible server using Microsoft Entra ID using identities. With authentication, you can manage database user identities and other Microsoft services in a central location, simplifying permission management. [Microsoft Entra authentication for Azure Database for MySQL flexible server](../flexible-server/security-entra-authentication.md).

- **Known issues**

  - The server parameter aad_auth_only stays set to ON only when the authentication type is changed to Microsoft Entra IDauthentication. We recommend disabling it manually when you opt for MySQL authentication only in the future.

  - The newly restored server will also have the server parameter aad_auth_only set to ON if it was ON on the source server during failover. You must manually disable this server parameter to use MySQL authentication on the restored server. Otherwise, an Admin must be configured.

- **Customer managed keys data encryption - Azure Database for MySQL flexible server (Preview)**

  With data encryption with customer-managed keys (CMKs) for Azure Database for MySQL flexible server Preview, you can bring your key (BYOK) for data protection at rest and implement separation of duties for managing keys and data. Data encryption with CMKs is set at the server level. For a given server, a CMK, called the key encryption key (KEK), is used to encrypt the data encryption key (DEK) used by the service. With customer managed keys (CMKs), the customer is responsible for the full control of the key lifecycle management (key creation, upload, rotation, deletion), key usage permissions, and auditing operations on keys. [Data encryption with customer managed keys for Azure Database for MySQL](../flexible-server/security-customer-managed-key.md).

- **Change Timezone of your Azure Database for MySQL flexible server instance in a single step**

  Previously to change time_zone of your Azure Database for MySQL flexible server instance required two steps to take effect. Now you no longer need to call the procedure mysql.az_load_timezone() to populate the mysql.time_zone_name table. Azure Database for MySQL flexible server timezone can be changed directly by just changing the server parameter time_zone from [portal](../flexible-server/how-to-configure-server-parameters-portal.md#working-with-the-time-zone-parameter) or [CLI](../flexible-server/how-to-configure-server-parameters-cli.md#working-with-the-time-zone-parameter).

- **Known issues**

  - The server parameter aad_auth_only stays set to ON only when the authentication type is changed to Microsoft Entra IDauthentication. We recommend disabling it manually when you opt for MySQL authentication only in the future.

  - The newly restored server will also have the server parameter aad_auth_only set to ON if it was ON on the source server during failover. To use MySQL authentication on the restored server, you must manually disable this server parameter. Otherwise, an Admin must be configured.

## August 2022

In August 2022, Azure Database for MySQL flexible server added server logs, on-demand backup, and new compute options. The following updates also make more server parameters configurable.

- **Server logs for Azure Database for MySQL flexible server**

  Server Logs help customers to emit the server logs to server storage space in file format, which you can later download. Slow query logs are supported with server logs, which can help customers in performance troubleshooting and query tuning. Customers can store logs for up to a week or up to 7 GB. You can configure or download them from [Enable and download server logs for Azure Database for MySQL flexible server](../flexible-server/how-to-server-logs-portal.md) or [List and download Azure Database for MySQL flexible server logs by using the Azure CLI](../flexible-server/how-to-server-logs-cli.md).[Learn more](../flexible-server/concepts-monitoring.md#server-logs).

- **On-Demand Backup for Azure Database for MySQL flexible server**

  The On-Demand backup feature allows customers to trigger On-Demand backups of their production workload, in addition to the automated backups taken by Azure Database for MySQL flexible server, and store them in alignment with the server's backup retention policy. These backups can be used as the fastest restore point to perform a point-in-time restore for faster and more predictable restore times. [Learn more](../flexible-server/how-to-trigger-on-demand-backup.md#trigger-on-demand-backup).

- **Memory-Optimized tier now supports Ev5 compute series**

  Memory Optimized tier for Azure Database for MySQL flexible server now supports the Ev5 compute series in more regions.
Learn more about [Boost Azure MySQL Memory Optimized flexible server performance by 30% with the Ev5 compute series!](https://techcommunity.microsoft.com/blog/adformysql/boost-azure-mysql-business-critical-flexible-server-performance-by-30-with-the-e/3603698)

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

    Server parameter aad_auth_only was exposed in this month's deployment. Enabling server parameter aad_auth_only will block all non Microsoft Entra IDMySQL connections to your Azure Database for MySQL flexible server instance. We're currently working on extra configurations required for Microsoft Entra IDauthentication to be fully functional, and the feature will be available in the upcoming deployments. Wait to enable the aad_auth_only parameter until then.

## June 2022

In June 2022, Azure Database for MySQL flexible server documented a diagnostic logs known issue. The following update describes the affected logging behavior and how to verify it.

- **Known Issues**

  You might no longer see logs uploaded to data sinks configured under diagnostics settings on a few servers where audit or slow logs are enabled. Verify whether your logs have the latest updated timestamp for the events based on the [data sink](../flexible-server/tutorial-query-performance-insights.md#set-up-diagnostics) you've configured. If your server is affected by this issue, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) so that we can apply a quick fix on the server to resolve the issue.

## May 2022

In May 2022, Azure Database for MySQL flexible server introduced business-critical and burstable compute options. The following updates make the Memory Optimized tier generally available and add new Burstable instances.

- **Announcing Azure Database for MySQL flexible server for business-critical workloads**
  Azure Database for MySQL Memory Optimized service tier is generally available. The Memory Optimized service tier is ideal for Tier 1 production workloads that require low latency, high concurrency, fast failover, and high scalability, such as gaming, e-commerce, and Internet-scale applications, to learn more about [Memory Optimized service Tier](https://techcommunity.microsoft.com/blog/adformysql/announcing-azure-database-for-mysql---flexible-server-for-business-critical-work/3361718).

- **Announcing the addition of new Burstable compute instances for Azure Database for MySQL flexible server**
  We're announcing the addition of new Burstable compute instances to support customers' autoscaling compute requirements from 1 vCore up to 20 vCores. learn more about [Compute Option for Azure Database for MySQL flexible server](../flexible-server/concepts-compute-storage.md).

- **Known issues**
  - The Reserved instances (RI) feature in Azure Database for MySQL flexible server isn't working properly for the Memory-Optimized service tier after restructuring from the Memory Optimized service tier. Specifically, instance reservation has stopped working, and we're working to fix the issue.
  - Private DNS integration details aren't displayed on a few Azure Database for MySQL Database flexible server instances that have enabled HA. This issue doesn't impact the server's availability or name resolution. We're working on a permanent fix to resolve the issue, and it will be available in the next deployment. Meanwhile, suppose you want to view the Private DNS Zone details. In that case, you can either search under [Quickstart: Create an Azure private DNS zone using the Azure portal](/azure/dns/private-dns-getstarted-portal) in the Azure portal or you can perform a [manual failover](../flexible-server/concepts-high-availability.md#planned-forced-failover) of the HA enabled Azure Database for MySQL flexible server instance and refresh the Azure portal.

## April 2022

In April 2022, Azure Database for MySQL flexible server delivered minor version upgrades and TLS protocol changes. The following updates cover new minor versions and the deprecation of older TLS protocols.

- **Minor version upgrade for Azure Database for MySQL flexible server to 8.0.28**
  Azure Database for MySQL flexible server 8.0 now is running on minor version 8.0.28. To learn more about changes coming in this minor version, see [Changes in MySQL 8.0.28 (General Availability)](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-28.html).

- **Minor version upgrade for Azure Database for MySQL flexible server to 5.7.37**
  Azure Database for MySQL flexible server 5.7 is now running on minor version 5.7.37. To learn more about changes coming in this minor version, see [Changes in MySQL 5.7.37 (General Availability](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-37.html).

  > [!NOTE]  
  > Some regions are still running older minor versions of Azure Database for MySQL flexible server and will be patched by end of April 2022.

- **Deprecation of TLSv1 or TLSv1.1 protocols with Azure Database for MySQL flexible server (8.0.28)**

  Starting version 8.0.28, the MySQL community edition supports TLS protocol TLSv1.2 or TLSv1.3 only. Azure Database for MySQL flexible server will also stop supporting TLSv1 and TLSv1.1 protocols to align with modern security standards. You can no longer configure TLSv1 or TLSv1.1 from the server parameter pane for newly created and previously created resources. The default is TLSv1.2. Resources created before the upgrade still support communication through TLS protocol TLSv1 or TLS v1.1 through May 1, 2022.

## March 2022

In March 2022, Azure Database for MySQL flexible server added geo-redundant backup and disaster recovery capabilities. The following updates enable backup storage migration and disaster recovery drills.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Migrate from locally redundant backup storage to geo-redundant backup storage for existing flexible server**
  Azure Database for MySQL flexible server provides the added flexibility to migrate to geo-redundant backup storage from locally redundant backup storage post server-create to provide higher data resiliency. Enabling geo-redundancy via the server's Compute + Storage page empowers customers to recover their existing Azure Database for MySQL flexible server instances from a geographic disaster or regional failure when they can't access the server in the primary region. With this feature enabled for their existing servers, customers can perform geo-restore and deploy a new server to the geo-paired Azure region using the original server's latest geo-redundant backup. [Backup and restore in Azure Database for MySQL](../flexible-server/concepts-backup-restore.md).

- **Simulate disaster recovery drills for your stopped servers**
  Azure Database for MySQL flexible server now provides the ability to perform geo-restore on stopped servers helping users simulate disaster recovery drills for their workloads to estimate impact and recovery time. This helps users plan better to meet their disaster recovery and business continuity objectives by using geo-redundancy feature offered by Azure Database for MySQL flexible server. [Point-in-time restore in Azure Database for MySQL flexible server with Azure CLI](../flexible-server/how-to-restore-server-cli.md).

## January 2022

In January 2022, Azure Database for MySQL flexible server introduced server management changes and expanded regional availability. The following updates cover stopped-server operations, new regions, and HA IOPS reservations.

This release of Azure Database for MySQL flexible server includes the following updates.

- **All Operations are disabled on Stopped Azure Database for MySQL flexible server instances**
  Operations on servers in a [Stop](../flexible-server/concept-servers.md#stop-and-start-a-server) state are disabled and show as inactive in the Azure portal. Operations that aren't supported on stopped servers include changing the pricing tier, number of vCores, storage size or IOPS, backup retention day, server tag, the server password, server parameters, storage autogrow, GEO backup, HA, and user identity.

- **Availability in three additional Azure regions**

  The public preview of Azure Database for MySQL flexible server is now available in the following Azure regions:
  - China East 2
  - China North 2

- **Reserving 36 IOPs for Azure Database for MySQL flexible server instances that have HA enabled**

  We're adding 36 IOPs and reserving them to support standby failover operation on servers that have enabled High Availability. This IOPs is in addition to the configured IOPs on your servers, so more monthly charges would apply based on your Azure region. The extra IOPS help us ensure our commitment to providing smooth failover experience from primary to standby replica. The added charge can be estimated by navigating to the [Azure Database for MySQL flexible server pricing page](https://azure.microsoft.com/pricing/details/mysql/flexible-server), choosing the Azure region for your server, and multiplying IOPs/month cost by 36 IOPs. For example, if your server is hosted in East US, the extra IO costs you can expect are $0.05*36 = USD 1.8 per month.

- **Bug fixes**

  Restart workflow struck issue with servers with HA, and Geo-redundant backup option enabled is fixed.

- **Known issues**

  - When you're using ARM templates for provisioning or configuration changes for HA enabled servers, if a single deployment is made to enable/disable HA and other server properties like backup redundancy, storage etc., then deployment would fail. You can mitigate it by submitting the deployment request separately to enable\disable and configuration changes. You don't have an issue with Portal or Azure CLI, as these requests are already separated.

  - When you're viewing automated backups for a HA enabled server on the Backup and Restore page, if at some point in time a forced or automatic failover is performed, you might lose viewing rights to the server's backups on the Backup and Restore page. Despite the invisibility of information regarding backups on the portal, the flexible server is successfully taking daily automated backups for the server in the backend. The server can be restored to any point within the retention period.

## Related content

- [What's new in Azure Database for MySQL flexible server in 2023](whats-new-2023.md)
- [What's new in Azure Database for MySQL flexible server in 2024](whats-new-2024.md)
- [What's new in Azure Database for MySQL flexible server in 2025](whats-new-2025.md)
- [What's new in Azure Database for MySQL flexible server in 2026](whats-new-2026.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)