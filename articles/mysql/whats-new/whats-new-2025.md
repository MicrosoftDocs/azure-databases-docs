---
title: What's new - 2025
description: 2025 feature announcements for Azure Database for MySQL flexible server, listed newest first.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan, randolphwest
ms.date: 06/18/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ms.custom: references_regions
ai-usage: ai-assisted
---

# What's new in Azure Database for MySQL flexible server in 2025?

This article summarizes the 2025 feature announcements for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## December 2025

In December 2025, Azure Database for MySQL flexible server extended its import tooling. The following update adds Azure MySQL Import CLI support for MySQL 8.4 workloads.

### Azure MySQL Import CLI adds support for MySQL 8.4

Azure Database for MySQL - Import CLI now supports importing MySQL 8.4 workloads from on-premises environments or virtual machines directly into Azure Database for MySQL. With this update, you can migrate your MySQL 8.4 data to Azure by using the automation that the Import CLI provides.

For more information, see [Migrate MySQL on-premises or Virtual Machine (VM) workload to Azure Database for MySQL with Azure Database for MySQL Import CLI](../migrate/migrate-external-mysql-import-cli.md).

## November 2025

In November 2025, Azure Database for MySQL flexible server introduced new preview capabilities for read scaling and server management. The following updates add a dedicated reader endpoint and server renaming.

### Reader Endpoint (Preview)

The Reader Endpoint feature for Azure Database for MySQL is now ready for preview.

Reader Endpoint provides a dedicated read-only endpoint for read replicas, enabling automatic connection-based load balancing of read-only traffic across multiple replicas. This feature simplifies application architecture by offering a single endpoint for read operations, improving scalability and fault tolerance. Azure Database for MySQL supports up to 10 read replicas per primary server. By routing read-only traffic through the reader endpoint, you can efficiently manage connections and optimize performance without handling individual replica endpoints. Reader endpoints continuously monitor the health of replicas and automatically exclude any replica that exceeds the configured replication lag threshold or becomes unavailable. To enroll in the preview, submit your details using this [form](https://aka.ms/mysqlearlyaccessenroll).

### Rename Server (Preview)

Azure Database for MySQL flexible server now supports server renaming. With this new capability, you no longer need to restore or migrate to a new server instance just to change the server name. The feature is currently in preview, and you should avoid production workloads while trying it out. To enroll in the preview, submit your details through this [form](https://aka.ms/mysqlearlyaccessenroll).

## October 2025

In October 2025, Azure Database for MySQL flexible server reached several general availability milestones for high availability and networking. The following updates cover dedicated SLB, custom port support, portal improvements, and server parameter changes.

### General Availability of Dedicated SLB for HA enabled servers

Dedicated SLB in Azure Database for MySQL flexible server for HA-enabled servers is now generally available (GA). This feature adds a dedicated Standard Load Balancer (SLB) to High Availability (HA) configurations for servers created with public access or private link. By managing the MySQL data traffic path, SLB removes the need for DNS changes during failover, significantly reducing failover time. This feature isn't supported for servers using private access with VNet integration. [Learn more](../flexible-server/concepts-high-availability.md#failover-process)

### General Availability of Custom Port Support

Custom port support for Azure Database for MySQL flexible server is now generally available (GA). This long-requested feature gives you greater flexibility to align MySQL server deployments with your network and security requirements. By default, MySQL uses TCP port 3306; with this GA release, you can configure a custom port (between 25001 and 26000) when creating a new Azure Database for MySQL flexible server. [Learn more](../flexible-server/concepts-networking.md#custom-port-support)

### Enhanced portal experience for high availability

The portal experience for High Availability (HA) options is now more intuitive and aligned with Azure standards. To help you run mission-critical workloads with zone-aware HA, the portal now prioritizes Zone-Redundant HA wherever available and displays SLA details alongside the selection for better clarity. If Zone-Redundant HA isn't available, you can enable Local Redundant HA. Additionally, "Same Zone" is rebranded to Local Redundant to ensure consistency with Azure naming conventions. [Manage zone redundant high availability in Azure Database for MySQL with the Azure portal](../flexible-server/how-to-configure-high-availability.md)

### General Availability of Server Parameters support for `lower_case_table_names` in Azure Database for MySQL- flexible server

For [MySQL version 8.0+](https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html), you can configure `lower_case_table_names` only when you're initializing the server. For restore operations or replica server creation, the parameter is automatically copied from the source server and can't be changed. [Learn More](../flexible-server/concepts-server-parameters.md#lower_case_table_names)

## September 2025

In September 2025, Azure Database for MySQL flexible server made MySQL 8.4 generally available. The following update lets you create production-ready MySQL 8.4 servers on Azure.

### Azure MySQL 8.4 General Available

Azure Database for MySQL flexible server now supports MySQL 8.4 in General Availability (GA). This support means you can create new MySQL 8.4 servers on Azure fully supported for production workloads. MySQL 8.4 is a long-term supported release from the MySQL community, bringing the latest features and improvements while emphasizing stability. With Azure's managed service, you get these new capabilities backed by Azure's enterprise-grade reliability and support. In short, MySQL 8.4 GA opens the door for you to upgrade your databases and future-proof your MySQL environment on Azure. [Learn more](../concepts-version-policy.md#supported-mysql-versions)

## August 2025

In August 2025, Azure Database for MySQL flexible server added flexibility to restore, replica, and backup workflows. The following updates enable cross-subscription and cross resource-group placement and on-demand backup deletion.

### Cross subscription and cross resource-group placement in restore and replica provisioning workflow

You can now restore a server or create a read replica in a different subscription and resource group in Azure Database for MySQL flexible server. This enhancement offers greater flexibility for cross-environment restores, resource organization, and subscription-level separation, helping you meet governance and operational requirements. For more information, see [Point-in-time restore in Azure Database for MySQL with the Azure portal](../flexible-server/how-to-restore-server-portal.md).

### Ability to delete on-demand backup

You can now delete on-demand backups in Azure Database for MySQL flexible server, giving you greater control over backup management and storage costs. This feature allows you to remove on-demand backups that you no longer need, helping you maintain a cleaner backup inventory and optimize resource usage. For more information, see [Backup and restore](../flexible-server/how-to-trigger-on-demand-backup.md#trigger-on-demand-backup).

## July 2025

In July 2025, Azure Database for MySQL flexible server expanded regional availability and self-service management. The following updates add new regions, self-heal, accelerated logs in the General Purpose tier, and more backup options.

### General Availability in new Azure regions

Azure Database for MySQL flexible server is now available in the following Azure regions:

- Chile Central
- Indonesia Central
- Malaysia West

### Self-Heal in Azure Database for MySQL (Public Preview)

The Self-Heal feature in Azure Database for MySQL lets you resolve common server issues independently, without needing to open a support case. It provides a one-click repair experience that helps restore service health quickly and safely. For more information, see [Self-Heal in Azure Database for MySQL (Public Preview)](../flexible-server/how-to-self-heal.md).

### Accelerated logs feature is now available in General Purpose service tier

Accelerated logs are now supported in the General Purpose service tier of Azure Database for MySQL flexible server. Previously available only in the Memory Optimized tier, this feature enhances performance and reduces transaction latency. The accelerated logs feature in the General Purpose tier is available at an extra cost. For more information, see [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md).

### Automate scheduling of on-demand backups

Azure Database for MySQL now supports the ability to schedule on-demand backups by using automation tasks. This feature gives you greater control and flexibility in managing on-demand backups for your Azure Database for MySQL flexible server instances. For more information, see [How to schedule an automation task](../flexible-server/create-automation-tasks.md#on-demand-backup-server-task).

### Configure backup interval for the automated backups

Azure Database for MySQL now supports the ability to configure the backup interval for the automatic backups that the system takes to improve restore speed. This new feature optimizes the process by introducing more frequent snapshots, thereby reducing the number of binlogs that need to be replayed for point-in-time restore and minimizing overall restore time. For more information, see [Backup frequency](../flexible-server/concepts-backup-restore.md#backup-frequency).

## June 2025

In June 2025, Azure Database for MySQL flexible server simplified time zone configuration. The following update loads time zones automatically during server creation.

### Auto Initialization of Time Zones

Time zones are automatically loaded during server creation, removing the need for you to manually run the `mysql.az_load_timezone` stored procedure afterward to load the time zone. For more information, refer to the server parameter details for [time_zone](../flexible-server/concepts-server-parameters.md#time_zone).

## May 2025

In May 2025, Azure Database for MySQL flexible server previewed new backup and resiliency capabilities. The following updates cover backup interval configuration, IOPS autoscaling, and a dedicated load balancer for high availability.

### Configure backup interval for the automated backups (Preview)

Azure Database for MySQL now supports the ability to configure the backup interval for the automatic backups that the system takes to improve restore speed. The feature is currently available in limited regions, namely West Central US and East Asia. For more information, see [Backup frequency](../flexible-server/concepts-backup-restore.md#backup-frequency).

### Enable Auto-Scale of IOPS for Faster Restore and Replica Provisions

Azure Database for MySQL now supports the ability to enable [autoscaling of IOPS](https://techcommunity.microsoft.com/blog/adformysql/autoscale-iops-for-azure-database-for-mysql---flexible-server---general-availabi/3884602) for both the source and target servers during restore operations and replica provisioning workflows. This enhancement helps accelerate the restore and replica provisioning process by temporarily boosting IOPS to meet the performance demands of these operations. After provisioning completes, you can disable the autoscale IOPS setting.

For more information, see [Point-in-time restore in Azure Database for MySQL with the Azure portal](../flexible-server/how-to-restore-server-portal.md).

### High Availability with Dedicated Azure Standard Load Balancer (SLB) (preview)

A dedicated standard load balancer (SLB) in Azure Database for MySQL for High Availability (HA) enabled servers is now available for public preview. This feature adds a dedicated standard load balancer to the HA configuration, enabling low-latency, high-throughput distribution of front-end traffic across backend servers. This enhancement improves failover performance and ensures more efficient handling of MySQL data traffic. If you want to enable an SLB for your HA server, [file a support ticket with Azure Support](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).

## March 2025

In March 2025, Azure Database for MySQL flexible server added new server management capabilities. The following updates introduce built-in stored procedures, a plugin change, and a service tier update.

### New built-in stored procedures for plugin management and undo log cleanup

Azure Database for MySQL now includes two built-in stored procedures that you can use to manage plugin settings and clean up undo logs without needing support intervention:

- Validate Password Plugin Management:
  - Enable: `CALL az_install_validate_password_plugin();`
  - Disable: `CALL az_uninstall_validate_password_plugin();`
  - After you enable the plugin, you can access its configuration parameters on the Azure portal's **Server Parameters** page.

- **Undo Log Cleanup**:
  - Use the new stored procedure to manually clean up the **Undo Log** and prevent unnecessary storage consumption.

For more information, see [Built-in stored procedures in Azure Database for MySQL](../flexible-server/concepts-built-in-store-procedure.md).

### Caching SHA-2 password plugin now exposed by default

The `caching_sha2_password` plugin is now exposed by default. You can enable and configure it by setting the relevant **Server Parameters** in the Azure portal.

### Default zone-resiliency for Business-Critical service tier (Rollback)

In response to customer feedback requesting flexibility in choosing their deployment type, we have reversed the change that made zone-resiliency the default for the Business-Critical service tier.

## February 2025

In February 2025, Azure Database for MySQL flexible server documented known issues for accelerated logs. The following update describes current limitations and workarounds.

### Known Issues

- Azure Advisor recommendations recommend enabling accelerated logs even after the feature is enabled on your Azure Database for MySQL server.

- For servers with [customer-managed keys (CMK)](../flexible-server/security-customer-managed-key.md), enabling [accelerated logs](../flexible-server/concepts-accelerated-logs.md) might not work due to a current limitation. You can temporarily disable CMK, enable accelerated logs, and re-enable CMK as a workaround.

  To learn more, visit [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md).

## January 2025

In January 2025, Azure Database for MySQL flexible server improved availability and performance defaults. The following updates cover zone resiliency for the Business-Critical tier and accelerated logs for Memory Optimized servers.

### Default zone-resiliency for Business-Critical service tier

You now benefit from the highest level of availability against infrastructure failures within an availability zone at no extra cost for mission-critical workloads running on the Business-Critical service tier. Regardless of whether your flexible servers are enabled with High Availability (HA), your server data and log files are hosted in zone-redundant storage by default. While zone-redundant HA-enabled servers continue to benefit from a 99.99% uptime SLA from the built-in zone redundancy and hot standby, non-HA servers can recover quickly from zone outages using zone-redundant backups. This enhancement applies to all new servers provisioned in the Business-Critical service tier.

> [!NOTE]  
> Based on customer feedback requesting the ability to choose their preferred deployment type, we've decided to roll back Default zone-resiliency for Business-Critical service tier. Now, for both Memory Optimized and General-Purpose servers, you must select the High Availability (HA) mode either same-zone or zone-redundant at the time of server creation. This selection is final and can't be modified later.

### Accelerated Logs enabled for all new Memory-Optimized servers

Accelerated Logs, a feature that significantly enhances the performance of Azure Database for MySQL flexible server instances, is now enabled by default for all new Business-Critical servers. Accelerated Logs offers a dynamic solution designed for high throughput needs, reducing latency with no extra cost. Existing Memory Optimized servers can also enable Accelerated Logs through the Azure portal. [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md).

## Related content

- [Azure Database for MySQL flexible server release notes 2025](../release-notes/release-notes-2025.md)
- [Azure Database for MySQL flexible server 2025 release notes](../release-notes/release-notes-2025.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)
