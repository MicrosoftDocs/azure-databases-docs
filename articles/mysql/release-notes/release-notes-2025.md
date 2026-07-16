---
title: Release notes - 2025
description: 2025 release notes for Azure Database for MySQL flexible server.
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 07/15/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
ai-usage: ai-assisted
---

# Azure Database for MySQL flexible server 2025 release notes

This article consolidates the 2025 monthly version release notes for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## October 2025

The October 2025 maintenance delivered improvements and known issue fixes.

### Version release notes

We're excited to announce the October 2025 version of Azure Database for MySQL flexible server. Starting October 1, 2025, all new servers are automatically onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in the Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

#### Engine version changes

- No changes to existing 8.0 server.
- No changes to existing 8.4 server.
- No changes to existing 5.7 server.
- No changes to innovation release version server.

#### Improvements

- Resource movement now supports moving resources that have private endpoints.

#### Known issues fixes

- Fixed the issue where replicas of source servers with geo-backup enabled could experience worsening replication lag under certain conditions. Once lag began, replicas failed to catch up and the delay continued to grow, independent of workload. This fix ensures replication lag now stabilizes and recovery mechanisms behave as expected.

## September 2025

The September 2025 maintenance included engine version updates, new features, improvements, and known issue fixes.

### Version release notes

The September 2025 version of Azure Database for MySQL flexible server is now available. Starting September 1, 2025, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

> [!IMPORTANT]  
> - During maintenance for this version, Azure Database for MySQL forces an upgrade of the TLS 1.0/1.1 setting to TLS 1.2. If you still use TLS 1.0 or 1.1 to connect to your MySQL servers, update your clients to support TLS 1.2. Otherwise, you might experience connectivity problems after the new version is applied.
> - To maintain strong security and compliance standards, Azure Database for MySQL rotates certificate authorities (CAs) during maintenance for this version. For more information about the process and actions you can take to preserve connectivity across the maintenance, see [Certificate rotation for Azure Database for MySQL flexible server](/azure/mysql/flexible-server/security-tls-root-certificate-rotation).

#### Engine version changes

- All existing 8.0 servers upgrade to version 8.0.42.
- No changes to existing 8.4 servers.
- No changes to existing 5.7 servers.
- No changes to innovation release version servers.

#### Features

- Preview of dedicated SLB based HA. [Manage zone redundant high availability in Azure Database for MySQL with the Azure portal](../flexible-server/how-to-configure-high-availability.md).
- Support for in place major version upgrade from 8.0 to 8.4. [Major version upgrade in Azure Database for MySQL](../flexible-server/how-to-upgrade.md).

#### Improvements

- Data migration service can now detect data corruption during external data migration, with both REST API and MySQL import CLI support.
- Capacity-related server creation error messages are more descriptive and include the link to the customer-facing troubleshooting guide.
- Error message related to private endpoint operations is more descriptive.
- Introduced a new built-in store procedure `mysql.az_drop_broken_table` to fix table corruption issue. [Learn more](../flexible-server/concepts-built-in-store-procedure.md#drop-problematic-table).

#### Known issues fixes

- Fixed the issue that in certain scenarios, virtual network server enabling fails.
- Fixed the issue that in certain scenarios, virtual network server creation or point in time recovery gets stuck until a timeout or customer cancel it.
- Fixed the issue that the resource ID isn't properly returned when executing an ARG query on the `servicehealthresources` table.

## July 2025

The July 2025 maintenance included engine version updates, a new feature, improvements, and known issue fixes.

### Version release notes

We're excited to announce the July 2025 version of Azure Database for MySQL flexible server. Starting July 1, 2025, all new servers are automatically onboarded to this latest version. The next scheduled maintenance upgrades existing servers. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

#### Engine version changes

- All existing 8.4 servers upgrade to 8.4.5 version.
- Innovation release version defaults to 9.3 version.
- No changes to existing 8.0 server.
- No changes to existing 5.7 server.

#### Features

- Azure Database for MySQL now supports binding Azure MySQL to a custom port. [Learn more](https://techcommunity.microsoft.com/blog/adformysql/now-in-public-preview-custom-port-support-in-azure-database-for-mysql-%E2%80%93-flexible/4432164)

#### Improvements

- The `binlog_storage_used` metric is visible to you.
- Support for larger text up to 8,192 bytes for the Azure MySQL flexible server slow query logs.

#### Known issues fixes

- Fixed the issue that maintenance window property is missing in the LIST server REST API.
- Fixed the shutdown crash issue of Azure MySQL 5.7 due to community bug.

## May 2025

The May 2025 maintenance included engine version updates and maintenance experience improvements.

### Version release notes

We're excited to announce the May 2025 version of Azure Database for MySQL flexible server. Starting May 1, 2025, the service automatically onboards all new servers to this latest version. The next scheduled maintenance upgrades existing servers. If you prefer to upgrade your servers earlier, you can enroll in the Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

#### Engine version changes

- All existing 8.0 servers upgrade to 8.0.41 version.
- All existing 8.4 servers upgrade to 8.4.4 version.
- Innovation release version defaults to 9.2 version.
- No changes to existing 5.7 server.

#### Features

- A set of maintenance experience improvements. Customers see these features only after global deployment is complete. [Manage scheduled maintenance settings for Azure Database for MySQL flexible server](../flexible-server/how-to-maintenance-portal.md)

> [!NOTE]  
> An issue exists where using **Reschedule to now** in the Azure portal might not take effect due to a defect. The product team is actively working to resolve this issue. Customers needing immediate rescheduling should use the Azure CLI command ([az mysql flexible-server maintenance reschedule](/cli/azure/mysql/flexible-server/maintenance#az-mysql-flexible-server-maintenance-reschedule)).

#### Improvements

- No improvements in this release.

#### Known issues fixes

- No known issue fixes in this release.

## March 2025

The March 2025 maintenance included a new preview feature and a known issue fix.

### Version release notes

The March 2025 version of Azure Database for MySQL is now available. All new servers are automatically onboarded to the latest version. Existing servers are upgraded during their next scheduled maintenance. To upgrade your servers earlier, enroll in the Virtual Canary Program by visiting [Scheduled maintenance in Azure Database for MySQL](https://aka.ms/mysql/virtual-canary).

#### Engine version changes

No major or minor version upgrade for all existing servers.

#### Features

- Public Preview for HA with dedicated SLB. This feature adds a dedicated [Load Balancer](/azure/load-balancer/load-balancer-overview) to a High availability (HA) configuration. It helps the HA servers use the benefits offered by a load balancer, such as low latency and high throughput network traffic distribution of front-end requests to back-end servers. SLB managing the MySQL data traffic path eliminates the need for changing the DNS during failover, which improves the failover time by about 20 seconds.

#### Improvements

- No major improvement in this release.

#### Known issues fixes

- Fix the issue due to an internal error, the correct charges of your consumption for geo-redundant servers weren't previously reflected in your billing. This issue is now resolved, and moving forward your billing aligns with the actual usage.

## February 2025

The February 2025 maintenance included engine version updates, new features, improvements, and known issue fixes.

### Version release notes

We're excited to announce the February 2025 version of Azure Database for MySQL flexible server. Starting February 10, 2025, all new servers are automatically onboarded to this latest version. The next scheduled maintenance upgrades existing servers. If you prefer to upgrade your servers earlier, you can enroll in the Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

#### Engine version changes

No major or minor version upgrade for existing 5.7 servers.

All existing 8.0 major version servers are upgraded to 8.0.40 minor version. To learn more about MySQL 8.0.40 version, see [MySQL 8.0.40 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-40.html).

#### Features

- Support customer managed plugin enablement for MySQL flexible server: `validate_password` is supported.
- Support checking the full version information through Azure CLI.
- Support enrollment of Virtual Canary Program through Azure CLI.

#### Improvements

- Enhancements to online schema changes now prevent data loss and duplicate key issues, ensuring better data integrity. These improvements apply to all new and existing servers. DDL operations on tables are now more reliable, reducing the risk of inconsistencies. For more details on the bug, [check the blog](https://techcommunity.microsoft.com/blog/adformysql/best-practices-for-safely-performing-schema-changes-in-azure-database-for-mysql/4356830).
- Export backup destination folder name is changed from timestamp to `backupName`.

#### Known issues fixes

- Fixed the issue where changing the customer maintenance window failed in certain scenarios.
- Fixed the issue where migrating a server from single server to flexible server and creating a new partial table after migration caused the major version upgrade to fail.
- Fixed the issue where the MySQL parameter `event_scheduler` was incorrectly turned off during an HA server failover.
- Fixed the issue where the major version upgrade failed when the audit log was enabled with ConnectionV2.
- Fixed the issue where a major version upgrade could lead to incomplete rollbacks, causing MySQL to repeatedly crash after rolling back to version 5.7.
- Fixed the issue where the `audit_log_exclude_users` parameter was unavailable with the `table_access` event.

## Related content

- [What's new in Azure Database for MySQL flexible server in 2025](../whats-new/whats-new-2025.md)
- [Azure Database for MySQL flexible server 2024 release notes](release-notes-2024.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)
