---
title: What's new - 2021 archive
description: 2021 feature announcements for Azure Database for MySQL flexible server, listed newest first.
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

# What's new in Azure Database for MySQL flexible server in 2021?

This article summarizes the 2021 feature announcements for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## November 2021

In November 2021, Azure Database for MySQL flexible server became generally available with new backup and restore capabilities. The following updates cover backup visibility, fastest restore points, and deleted server recovery.

- **General Availability of Azure Database for MySQL flexible server**

  Azure Database for MySQL flexible server is now **General Availability** in more than [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md) worldwide.

- **View available full backups in Azure portal**

  A dedicated Backup and Restore option is now available in the Azure portal. This page lists the backups available within the server's retention period, effectively providing a single pane view for managing a server's backups and consequent restores. You can use this option to:
  - View the completion timestamps for all available full backups within the server's retention period
  - Perform restore operations using these full backups

- **Fastest restore points**

  With the fastest restore point option, you can restore an Azure Database for MySQL flexible server instance in the fastest time possible on a given day within the server's retention period. This restore operation restores the full snapshot backup without requiring restore or recovery of logs. With fastest restore point, customers see three options while performing point in time restores from Azure portal latest restore point, custom restore point, and fastest restore point. [Learn more](../flexible-server/concepts-backup-restore.md#point-in-time-restore).

- **FAQ in the Azure portal**

  The Backup and Restore page includes a section dedicated to listing your most frequently asked questions and answers. This should provide answers to most questions about backup directly within the Azure portal. In addition, selecting the question mark icon for FAQs on the top menu provides access to even more related detail.

- **Restore a deleted Azure Database for MySQL flexible server instance**

  The service now allows you to recover a deleted Azure Database for MySQL flexible server resource within five days from the time of server deletion. For a detailed guide on restoring a deleted server, [refer to the documented steps](../flexible-server/how-to-restore-dropped-server.md). To protect server resources post deployment from accidental deletion or unexpected changes, we recommend administrators to use [management locks](/azure/azure-resource-manager/management/lock-resources).

- **Known issues**

  On servers with HA and Geo-redundant backup option enabled, we found a rare issue encountered by a race condition, which blocks the restart of the standby server to finish. As a result of this issue, when you fail over the HA enabled Azure Database for MySQL flexible server instance might get stuck in restarting state for a long time. The fix will be deployed to the production in the next deployment cycle.

## October 2021

In October 2021, Azure Database for MySQL flexible server added performance, resiliency, and management capabilities. The following updates cover thread pools, geo-redundant restore, monitoring, reserved instances, and more.

- **Thread pools are now available for Azure Database for MySQL flexible server**

  Thread pools enhance the scalability of Azure Database for MySQL flexible server. Using a thread pool, users can optimize performance, achieve better throughput, and lower latency for high concurrent workloads. [Learn more](https://techcommunity.microsoft.com/category/azuredatabases/blog/adformysql).

- **Geo-redundant backup restore to geo-paired region for DR scenarios**

  The service now provides the flexibility to choose geo-redundant backup storage for higher data resiliency. Enabling geo-redundancy empowers customers to recover from a geographic disaster or regional failure when they can't access the server in the primary region. With this feature enabled, customers can perform geo-restore and deploy a new server to the geo-paired geographic region using the original server's latest geo-redundant backup. [Backup and restore in Azure Database for MySQL](../flexible-server/concepts-backup-restore.md).

- **Availability Zones Selection when creating Read replicas**

  When creating Read replica, you can select the Availability Zones location of your choice. An Availability Zone is a high availability offering that protects your applications and data from datacenter failures. Availability Zones are unique physical locations within an Azure region. [Read replicas in Azure Database for MySQL](../flexible-server/concepts-read-replicas.md).

- **Read replicas in Azure Database for MySQL flexible server will no longer be available on Burstable SKUs**

  If you have an existing Azure Database for MySQL flexible server instance with read replica enabled, you have to scale up your server to either General Purpose or Memory Optimized pricing tiers or delete the read replica within 60 days. After the 60 days, while you can continue to use the primary server for your read-write operations, replication to read replica servers will be stopped. For newly created servers, read replica option is available only for the General Purpose and Memory Optimized pricing tiers.

- **Monitoring Azure Database for MySQL flexible server with Azure Monitor Workbooks**

  Azure Database for MySQL flexible server is now integrated with Azure Monitor Workbooks. Workbooks provide a flexible canvas for data analysis and creating rich visual reports within the Azure portal. With this integration, the server has link to workbooks and few sample templates, which help to monitor the service at scale. These templates can be edited, customized to customer requirements and pinned to dashboard to create a focused and organized view of Azure resources. [Tutorial: Query Performance Insight for Azure Database for MySQL](../flexible-server/tutorial-query-performance-insights.md), [Tutorial: Configure audit logs by using Azure Database for MySQL flexible server](../flexible-server/tutorial-configure-audit.md), and Instance Overview templates are currently available. [Monitor Azure Database for MySQL flexible server by using Azure Monitor workbooks](../flexible-server/concepts-workbooks.md).

- **Prepay for Azure Database for MySQL flexible server compute resources with reserved instances**

  Azure Database for MySQL flexible server now helps you save money by prepaying for compute resources compared to pay-as-you-go prices. With Azure Database for MySQL flexible server reserved instances, you make an upfront commitment on Azure Database for MySQL flexible server for one or three years to get a significant discount on the compute costs. You can exchange a reservation from Azure Database for MySQL single server with Azure Database for MySQL flexible server. [Learn more](../concept-reserved-pricing.md).

- **Stopping the server for up to 30 days while the server is not in use**

  Azure Database for MySQL flexible server now allows you to Stop the server for up to 30 days when not in use and Start the server when you're ready to resume your development. This enables you to develop at your own pace and save development costs on the database servers by paying for the resources only when used. This is important for dev-test workloads and when you only use the server for part of the day. When you stop the server, all active connections are dropped. When the server is in the Stopped state, the server's compute isn't billed. However, storage continues to be billed as the server's storage remains to ensure that data files are available when the server is started again. [Learn more](../flexible-server/concept-servers.md#stop-and-start-a-server).

- **Terraform Support for Azure Database for MySQL flexible server**

  Terraform support for Azure Database for MySQL flexible server is now released with the [latest v2.81.0 release of azurerm](https://github.com/hashicorp/terraform-provider-azurerm/blob/v2.81.0/CHANGELOG.md). The detailed reference document for provisioning and managing an Azure Database for MySQL flexible server instance using Terraform can be found [here](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mysql_flexible_server). Any bugs or known issues can be found or reported [here](https://github.com/hashicorp/terraform-provider-azurerm/issues).

- **Static Parameter innodb_log_file_size is now Configurable**

  - [innodb_log_file_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size) can now be configured to any of these values: 256 MB, 512 MB, 1 GB, or 2 GB. Because it's a static parameter, it requires a server restart. If you've changed the parameter innodb_log_file_size from default, check if the "show global status like 'innodb_buffer_pool_pages_dirty'" stays at 0 for 30 seconds to avoid restart delay. See [Server parameters in Azure Database for MySQL flexible server](../flexible-server/concepts-server-parameters.md) to learn more.

- **Availability in two additional Azure regions**

  Azure Database for MySQL flexible server is now available in the following Azure regions:

  - US West 3
  - North Central US

[Learn more](../flexible-server/overview.md#azure-regions).

- **Known Issues**
  - When a primary Azure region is down, you can't create geo-redundant servers in its geo-paired region as storage can't be provisioned in the primary Azure region. You must wait for the primary region to be up to provision geo-redundant servers in the geo-paired region.

## September 2021

In September 2021, Azure Database for MySQL flexible server expanded regional availability. The following updates add new regions and fix same-zone HA creation.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Availability in three additional Azure regions**

  The public preview of Azure Database for MySQL flexible server is now available in the following Azure regions:

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

In August 2021, Azure Database for MySQL flexible server added high availability, networking, and security capabilities. The following updates cover same-zone HA, private DNS integration, point-in-time restore options, and plugin previews.

This release of Azure Database for MySQL flexible server includes the following updates.

- **High availability within a single zone using Same-Zone High Availability**

  The service now allows customers to choose the preferred availability zone for their standby server when they enable high availability. With this feature, customers can place a standby server in the same zone as the primary server, which reduces the replication lag between primary and standby. This also provides lower latencies between the application server and database server if placed within the same Azure zone. [High-availability in Azure Database for MySQL](../flexible-server/concepts-high-availability.md).

- **Standby zone selection using Zone-Redundant High Availability**

  The service now allows customers to choose the standby server zone location. Using this feature, customers can place their standby server in the zone of their choice. Colocating the standby database servers and applications in the same zone reduces latencies and allows customers to better prepare for disaster recovery situations and "zone down" scenarios. [High-availability in Azure Database for MySQL](../flexible-server/concepts-high-availability.md).

- **Private DNS zone integration**

  [What is an Azure Private DNS zone?](/azure/dns/private-dns-privatednszone) provides a reliable and secure DNS service (responsible for translating a service name to IP address) for your virtual network. Azure Private DNS manages and resolves domain names in the virtual network without configuring a custom DNS solution. This enables you to connect your application running on a virtual network to your Azure Database for MySQL flexible server instance running on a locally or globally peered virtual network. Azure Database for MySQL flexible server now integrates with an Azure private DNS zone to allow seamless resolution of private DNS within the current virtual network, or any peered virtual network to which the private DNS zone is linked. With this integration, if the IP address of the backend Azure Database for MySQL flexible server instance changes during failover or any other event, your integrated private DNS zone is updated automatically to ensure your application connectivity resumes automatically once the server is online. [Private Network Access using virtual network integration for Azure Database for MySQL flexible server](../flexible-server/concepts-networking-vnet.md).

- **Point-In-Time Restore for a server in a specified virtual network**

  The Point-In-Time Restore experience for the service now enables customers to configure networking settings, allowing users to switch between private and public networking options when performing a restore operation. This feature allows customers to inject a server being restored into a specified virtual network securing their connection endpoints. [Point-in-time restore in Azure Database for MySQL with the Azure portal](../flexible-server/how-to-restore-server-portal.md).

- **Point-In-Time Restore for a server in an availability zone**

  The Point-In-Time Restore experience for the service now enables customers to configure availability zone. Colocating the database servers and standby applications in the same zone reduces latencies and allows customers to better prepare for disaster recovery situations and "zone down" scenarios. [High-availability in Azure Database for MySQL](../flexible-server/concepts-high-availability.md).

- **validate_password and caching_sha2_password plugin available in private preview**

  Azure Database for MySQL flexible server now supports enabling validate_password and caching_sha2_password plugins in preview. The validate_password plugin provides password policy enforcement and password strength validation. The caching_sha2_password plugin provides a more secure authentication method than the default mysql_native_password plugin. To learn more, visit [server parameters](../flexible-server/concepts-server-parameters.md).

- **Availability in four additional Azure regions**

  The public preview of Azure Database for MySQL flexible server is now available in the following Azure regions:

  - Australia Southeast
  - South Africa North
  - East Asia (Hong Kong Special Administrative Region)
  - Central India

  [Learn more](../flexible-server/overview.md#azure-regions).

- **Known issues**

  - Right after Zone-Redundant high availability server failover, clients fail to connect to the server if using SSL with ssl_mode VERIFY_IDENTITY. This issue can be mitigated by using ssl_mode as VERIFY_CA.
  - Unable to create Same-Zone High availability server in the following regions: Central India, East Asia, Korea Central, South Africa North, Switzerland North.
  - In a rare scenario and after HA failover, the primary server is in read_only mode. Resolve the issue by updating "read_only" value from the server parameters page to OFF.
  - After successfully scaling Compute on the Compute + Storage page, IOPS are reset to the SKU default. Customers can work around the issue by rescaling IOPs on the Compute + Storage page to desired value (previously set) post the compute deployment and consequent IOPS reset.

## July 2021

In July 2021, Azure Database for MySQL flexible server added migration and regional availability updates. The following updates enable online migration from single server and expand supported regions.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Online migration from Azure Database for MySQL single server to Azure Database for MySQL flexible server**

  Customers can now migrate an instance of Azure Database for MySQL single server to Azure Database for MySQL flexible server with minimum downtime to their applications using Data-in Replication. For detailed, step-by-step instructions, see [Migrate Azure Database for MySQL single server instances to Azure Database for MySQL flexible server with minimal downtime](../howto-migrate-single-flexible-minimum-downtime.md).

- **Availability in West US and Germany West Central**

  The public preview of Azure Database for MySQL flexible server is now available in the West US and Germany West Central Azure regions.

## June 2021

In June 2021, Azure Database for MySQL flexible server improved storage, replication, and developer experiences. The following updates cover storage changes, the free offer, data-in replication, and GitHub Actions support.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Improved performance on smaller storage servers**

  Beginning June 21, 2021, the minimum allowed provisioned storage size for all newly created server increases from 5 GB to 20 GB. In addition, the available free IOPS increases from 100 to 300. These changes are summarized in the following table:

  | **Current** | **As of June 21, 2021** |
  | --- | --- |
  | Minimum allowed storage size: 5 GB | Minimum allowed storage size: 20 GB |
  | IOPS available: Max(100, 3 * [Storage provisioned in GB]) | IOPS available: (300 + 3 * [Storage provisioned in GB]) |

- **Free 12-month offer**

  As of June 15, 2021, the [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) provides customers up to 12 months of free access to Azure Database for MySQL flexible server with 750 hours of usage and 32 GB of storage per month. Customers can use this offer to develop and deploy applications that use Azure Database for MySQL flexible server. [Use an Azure free account to try Azure Database for MySQL flexible server for free](../flexible-server/how-to-deploy-on-azure-free-account.md).

- **Storage auto-grow**

  Storage auto grow prevents a server from running out of storage and becoming read-only. If storage auto grow is enabled, the storage automatically grows without affecting the workload. Beginning June 21, 2021, all newly created servers have storage auto grow enabled by default.
- **Data-in Replication**

  Azure Database for MySQL flexible server now supports [Replicate data into Azure Database for MySQL flexible server](../flexible-server/concepts-data-in-replication.md). Use this feature to synchronize and migrate data from a MySQL server running on-premises, in virtual machines, on Azure Database for MySQL single server, or database services outside Azure to Azure Database for MySQL flexible server. Learn more about [How to configure Azure Database for MySQL flexible server data-in replication](../flexible-server/how-to-data-in-replication.md).

- **GitHub Actions support with Azure CLI**

  Azure Database for MySQL flexible server CLI now allows customers to automate workflows to deploy updates with GitHub Actions. This feature helps set up and deploy database updates with MySQL GitHub Actions workflow. These CLI commands assist with setting up a repository to enable continuous deployment for ease of development. [Learn more](/cli/azure/mysql/flexible-server/deploy).

- **Zone redundant HA forced failover fixes**

  This release includes fixes for known issues related to forced failover to ensure that server parameters and more IOPS changes are persisted across failovers.

- **Known issues**

  - Trying to perform up a compute scale or scale down operation on an existing server with less than 20 GB of storage provisioned doesn't complete successfully. Resolve the issue by scaling the provisioned storage to 20 GB and retrying the compute scaling operation.

## May 2021

In May 2021, Azure Database for MySQL flexible server expanded regional availability and connection flexibility. The following updates cover new regions, TLS enforcement options, and zone-redundant HA.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Extended regional availability (France Central, Brazil South, and Switzerland North)**

  The public preview of Azure Database for MySQL flexible server is now available in the France Central, Brazil South, and Switzerland North regions. [Learn more](../flexible-server/overview.md#azure-regions).

- **SSL/TLS 1.2 enforcement can be disabled**

  This release provides the enhanced flexibility to customize SSL and minimum TLS version enforcement. To learn more, see [Connect to Azure Database for MySQL flexible server with encrypted connections](../flexible-server/security-tls-how-to-connect.md).

- **Zone redundant HA available in UK South and Japan East region**

  Azure Database for MySQL flexible server now offers zone-redundant high availability in two more regions: UK South and Japan East. [Learn more](../flexible-server/overview.md#azure-regions).

- **Known issues**

  - Additional IOPs changes don't take effect in zone redundant HA enabled servers. Customers can work around the issue by disabling HA, scaling IOPs, and the re-enabling zone redundant HA.
  - After force failover, the standby availability zone is inaccurately reflected in the portal. (No workaround)
  - Server parameter changes don't take effect in zone redundant HA enabled server after forced failover. (No workaround)

## April 2021

In April 2021, Azure Database for MySQL flexible server added management tooling and developer experiences. The following updates cover forced failover, a PowerShell module, and Azure CLI query support.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Ability to force failover to standby server with zone redundant high availability released**

  Customers can now manually force a failover to test functionality with their application scenarios, which can help them to prepare for any outages. [Learn more](https://techcommunity.microsoft.com/blog/adformysql/forced-failover-for-azure-database-for-mysql-%E2%80%93-flexible-server/2280671).

- **PowerShell module for Azure Database for MySQL flexible server released**

  Developers can now use PowerShell to provision, manage, operate, and support Azure Database for MySQL flexible server instances and dependent resources. [Learn more](https://techcommunity.microsoft.com/blog/adformysql/introducing-the-mysql-flexible-server-powershell-module/2203383).

- **Connect, test, and execute queries using Azure CLI**

  Azure Database for MySQL flexible server now provides an improved developer experience allowing customers to connect and execute queries to their servers using the Azure CLI with the "az mysql flexible-server connect" and "az mysql flexible-server execute" commands. [Learn more](../flexible-server/connect-azure-cli.md#view-all-the-arguments).

- **Fixes for provisioning failures for server creates in virtual network with private access**

  All the provisioning failures caused when creating a server in virtual network are fixed. With this release, users can create Azure Database for MySQL flexible server instances with private access every time.

## March 2021

In March 2021, Azure Database for MySQL flexible server added version and placement capabilities. The following updates cover MySQL 8.0.21, availability zone placement, and performance improvements.

This release of Azure Database for MySQL flexible server includes the following updates.

- **MySQL 8.0.21 released**

  MySQL 8.0.21 is now available in Azure Database for MySQL flexible server in all major [Azure regions](../flexible-server/overview.md#azure-regions). Customers can use the Azure portal, the Azure CLI, or Azure Resource Manager templates to provision the MySQL 8.0.21 release. [Learn more](../flexible-server/quickstart-create-server-portal.md#create-an-azure-database-for-mysql-flexible-server).

- **Support for Availability zone placement during server creation released**

  Customers can now specify their preferred Availability zone during server creation. This functionality allows customers to collocate their applications hosted on Azure VM, Virtual Machine Scale Set, or AKS and database in the same Availability zones to minimize database latency and improve performance. [Learn more](../flexible-server/quickstart-create-server-portal.md#create-an-azure-database-for-mysql-flexible-server).

- **Performance fixes for issues when running Azure Database for MySQL flexible server in virtual network with private access**

  Before this release, the performance of Azure Database for MySQL flexible server degraded significantly when running in virtual network configuration. This release includes the fixes for the issue, allowing users to see improved performance on Azure Database for MySQL flexible server in virtual network.

- **Known issues**

  - SSL\TLS 1.2 is enforced and can't be disabled. (No workarounds)
  - There are intermittent provisioning failures for servers provisioned in a virtual network. The workaround is to retry the server provisioning until it succeeds.

## February 2021

In February 2021, Azure Database for MySQL flexible server added independent IOPS provisioning. The following update lets you scale IOPS separately from storage.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Additional IOPS feature released**

  Azure Database for MySQL flexible server supports provisioning more [IOPS](../flexible-server/concepts-compute-storage.md#iops) independent of the storage provisioned. Customers can use this feature to increase or decrease the number of IOPS anytime based on their workload requirements.

- **Known issues**

  The performance of Azure Database for MySQL flexible server degrades with private access-virtual network isolation (No workaround).

## January 2021

In January 2021, Azure Database for MySQL flexible server added read replica support. The following update enables asynchronous replication to up to 10 replicas in the same region.

This release of Azure Database for MySQL flexible server includes the following updates.

- **Up to 10 read replicas for Azure Database for MySQL flexible server**

  Azure Database for MySQL flexible server now supports asynchronous data replication from one Azure Database for MySQL flexible server instance (the 'source') to up to 10 Azure Database for MySQL flexible server instances (the 'replicas') in the same region. This functionality enables read-heavy workloads to scale out and be balanced across replica servers according to a user's preferences. [Read replicas in Azure Database for MySQL](../flexible-server/concepts-read-replicas.md).

## Related content

- [What's new in Azure Database for MySQL flexible server in 2022](whats-new-2022.md)
- [What's new in Azure Database for MySQL flexible server in 2023](whats-new-2023.md)
- [What's new in Azure Database for MySQL flexible server in 2024](whats-new-2024.md)
- [What's new in Azure Database for MySQL flexible server in 2025](whats-new-2025.md)
- [What's new in Azure Database for MySQL flexible server in 2026](whats-new-2026.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)