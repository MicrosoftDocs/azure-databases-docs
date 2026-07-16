---
title: Release notes - 2026
description: 2026 release notes for Azure Database for MySQL flexible server.
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 07/15/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
ai-usage: ai-assisted
---

# Azure Database for MySQL flexible server 2026 release notes

[Azure Database for MySQL flexible server](../flexible-server/overview.md) is a fully managed database service that gives you granular control and flexibility over database management functions and configuration settings. The service supports the community versions of MySQL 5.7, 8.0, and 8.4. Each monthly version delivers new capabilities, engine updates, improvements, and fixes that roll out to new servers first and to existing servers during their next scheduled maintenance.

This article consolidates the 2026 monthly version release notes for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## July 2026

The July 2026 update delivers minor engine version upgrades, reliability improvements, and known issue fixes. Review the following details before your servers upgrade during their next scheduled maintenance.

### Version release notes

The July 2026 version of Azure Database for MySQL flexible server is available. Starting July 14, 2026, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

#### Maintenance scheduling considerations

You can extend the maintenance reschedule window up to August 15, 2026. Some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with your original CMW preference.

#### Engine version changes

This version includes the following minor version changes:

- 8.0.44 -> 8.0.45
- 8.4.7 -> 8.4.8

#### Features

This version doesn't introduce any new features.

#### Improvements

- Added resiliency against transient network issues.
- During this scheduled maintenance window, a few HA-enabled servers migrate from the current architecture to a dedicated Standard Load Balancer (SLB) - based architecture. The candidate servers are communicated through the usual maintenance notifications. This enhancement adds a dedicated SLB to HA configurations for servers created with public access or private endpoints. By managing the MySQL data traffic path, the SLB eliminates the need for DNS changes during failovers, significantly reducing failover time. There's a brief extra downtime (of around 30 seconds) while this migration is performed. This feature isn't supported by servers using private access with a virtual network integration.

#### Known issues fixes

- Fixes a timeout issue with major version upgrade availability and now recovers quickly in case of an exception.
- Fixes logic to allow MultiZone HA by checking for remaining supported zones.

## May 2026

The May 2026 update introduces new customer-managed key and resiliency capabilities, along with TLS and networking improvements and known issue fixes. Review the following details before your servers upgrade during their next scheduled maintenance.

### Version release notes

The May 2026 version of Azure Database for MySQL flexible server is available. Beginning May 19, 2026, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

#### Maintenance scheduling considerations

The maintenance reschedule window can be extended up to June 21, 2026. Some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with your original CMW preference.

#### Engine version changes

This version doesn't include any engine version changes.

#### Features

- You can now use HSM-backed key vaults at the ProtectedSubscription level when configuring customer-managed keys (CMK), giving you stronger key isolation for regulated and compliance-sensitive workloads.
- You can now add availability zones to an existing server without recreating it, making it easier to improve resiliency as your workload evolves.
- List APIs for databases and servers now support pagination, providing faster and more reliable responses when you manage a large number of resources.

#### Improvements

- TLS certificates are now automatically renewed earlier in their lifecycle (at 84% of validity) and all certificates follow the same renewal schedule, reducing the chance of connection issues caused by certificate expiry.
- During this scheduled maintenance window, a few HA-enabled servers migrate from the current architecture to a dedicated Standard Load Balancer (SLB) - based architecture. The candidate servers are communicated through the usual maintenance notifications. This enhancement adds a dedicated SLB to HA configurations for servers created with public access or private endpoints. By managing the MySQL data traffic path, the SLB eliminates the need for DNS changes during failovers, significantly reducing failover time. There's a brief extra downtime (of around 30 seconds) while this migration is performed. This feature isn't supported by servers using private access with a virtual network integration.

#### Known issues fixes

- Resolved an intermittent connectivity issue that could affect servers configured with private access (virtual network integration), by reverting a recent change to the underlying networking stack.
- Resolved an issue where binlog copy operations could fail when an expected binlog file was missing. The service now handles this case gracefully without interrupting the operation.

## March 2026

The March 2026 update includes minor engine version upgrades, troubleshooting and integration improvements, and a known issue fix. Review the following details before your servers upgrade during their next scheduled maintenance.

### Version release notes

The March 2026 version of Azure Database for MySQL flexible server is now available. Starting March 31, 2026, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

#### Maintenance scheduling considerations

You can extend the maintenance reschedule window up to the end of April. Some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with your original CMW preference.

#### Engine version changes

This version includes the following minor version changes:

- 8.0.42 -> 8.0.44
- 8.4.5 -> 8.4.7
- 9.3.0 -> 9.5.0

#### Features

This version doesn't introduce any new features.

#### Improvements

- Returns clear, actionable customer-facing errors for invalid key scenarios, improving troubleshooting and support experience.
- Enables self-service configuration of binlog_row_metadata, unblocking CDC/Data Out integrations and reducing support dependency.
- As part of the March 2026 update, the daily automated backup time for your server is expected to change once. After this update, backups continue to run once, every day as usual. The daily automatic backup continues unchanged and only the scheduled time of the daily backup shifts once. No user action is required.

#### Known issues fixes

- Adds check to see if target AZ is available as a supported zone for the specific SKU.

## January 2026

The January 2026 update focuses on error message and TLS improvements along with known issue fixes. Before you reschedule maintenance, review the certificate-related maintenance scheduling considerations.

### Version release notes

The January 2026 version of Azure Database for MySQL flexible server is now available. Starting January 22, 2026, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

#### Maintenance scheduling considerations

For Azure Database for MySQL instances in the Azure public cloud, an internal certificate expires by the end of February 2026. As a result, the maintenance reschedules window for this cycle is limited to dates before the end of February. Postponing maintenance beyond February might cause the server to become unreachable after the certificate expires. Therefore, rescheduling past the end of February isn't supported for this maintenance event.

For some Azure Database for MySQL instances in Azure National Clouds, the certificate that the current Certificate Authority (CA) issued expires before February 6, 2026. After the certificate expires, client connections to the server fail, resulting in service unavailability.

To assess whether your server is affected, verify the certificate expiration date from a client environment by using the following command: `openssl s_client -starttls mysql -connect <server_dns>:3306`. For affected servers, the maintenance reschedule window is limited and can't be freely postponed, as further delay increases the risk of certificate expiration and client connection failures. In some cases, if the server was restarted recently, the certificate is automatically refreshed. If you believe this condition applies to your server, open an Azure Support case. After validation, the maintenance reschedule window can be extended up to the end of February.

During this maintenance cycle, there are major global events between **February 5-10, 2026** and **February 16-23, 2026** that might limit our ability to fully honor all customers' Custom Maintenance Window (CMW) preferences during initial scheduling. As a result, some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with these event periods or your original CMW preference.

#### Engine version changes

This version doesn't include any engine version changes.

#### Features

This version doesn't introduce any new features.

#### Improvements

- Improved the error message that's shown when you attempt to enable HA on a VNET-based instance that still has Accelerated Logs enabled.
- Added TLS 1.3 support for Azure MySQL 5.7 version.

#### Known issues fixes

- Fixed an issue where enabling geo backup caused subsequent GTID reset operations to fail.
- Fixed an issue where certain HA servers behind a dedicated SLB couldn't enable a private endpoint.

## Related content

- [What's new in Azure Database for MySQL flexible server in 2026](../whats-new/whats-new-2026.md)
- [Azure Database for MySQL flexible server 2025 release notes](release-notes-2025.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)
