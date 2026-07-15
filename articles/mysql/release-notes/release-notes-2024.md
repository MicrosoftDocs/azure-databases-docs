---
title: Release notes - 2024
description: 2024 release notes for Azure Database for MySQL flexible server.
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 07/15/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
ai-usage: ai-assisted
---

# Azure Database for MySQL flexible server 2024 release notes

This article consolidates the 2024 monthly version release notes for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## October 2024

The October 2024 maintenance introduced improvements, known issue fixes, and security patches.

### Version release notes

This version release includes the October 2024 maintenance for Azure Database for MySQL flexible server. This maintenance incorporates several new features and improvements, along with known issue fixes and security patches.

#### Engine version changes

No engine version upgrade in this maintenance.

#### Features

This maintenance update doesn't introduce any new features.

#### Improvements

- Change the default value of the server parameter `tls_version` to `TLSv1.2, TLSv1.3` on MySQL 8.0, which means connections use TLSv1.3 by default.
- Expose the server parameters `innodb_ddl_buffer_size` and `innodb_ddl_threads`.
- Upgrade US region servers to a FIPS-compliant version by default. For more information, see [Azure FIPS compliance](/azure/compliance/offerings/offering-fips-140-2).

#### Known issues fixes

- Fix the issue where resetting the password doesn't work if the authentication plugin for the admin user changes.
- Fix the issue where servers configured with high `max_connections` might not work as expected.
- Fix the issue where you can't delete the server if it starts and stops more than 120 times.
- Fix the issue where the major version upgrade validation function might get stuck and block upcoming management operations such as server stop, start, update, and delete.
- Fix the issue where old geo replica promotion gets stuck.

## September 2024

The September 2024 maintenance upgraded servers that use TLS 1.0 or 1.1 to TLS 1.2.

### Version release notes

The September 2024 maintenance for Azure Database for MySQL flexible server upgrades servers that use TLS 1.0 or 1.1 to TLS 1.2.

#### Engine version changes

This maintenance doesn't upgrade the engine version.

#### Features

This maintenance update doesn't introduce new features.

#### Improvements

- The maintenance upgrade is mandatory for all servers that use TLS 1.0 or 1.1 to TLS 1.2. [Connect to Azure Database for MySQL flexible server with encrypted connections](../flexible-server/security-tls-how-to-connect.md)

#### Known issues fixes

This maintenance update doesn't introduce known issue fixes.

## August 2024

The August 2024 maintenance updated existing 8.0.34 and later servers to the 8.0.37 engine version, with security improvements and known issue fixes.

### Version release notes

We're pleased to announce the August 2024 maintenance of the Azure Database for MySQL flexible server. This maintenance updates all existing 8.0.34 and later engine version servers to the 8.0.37 engine version, along with several security improvements and known issue fixes.

#### Engine version changes

The existing engine version is 8.0.34 or later, and the server upgrades to the 8.0.37 engine version.

> [!NOTE]  
> Percona identified a [critical bug](https://www.percona.com/blog/do-not-upgrade-to-any-version-of-mysql-after-8-0-37/?utm_campaign=2024-blog-q3&utm_content=300046226&utm_medium=social&utm_source=linkedin&hss_channel=lcp-421929) in MySQL versions 8.0.38, 8.4.1, and 9.0.0 that causes the MySQL daemon to crash upon restart if more than 10,000 tables exist. Azure MySQL doesn't upgrade to the buggy MySQL versions 8.0.38, 8.4.1, and 9.0.0 in the August maintenance. Instead, the upgrade skips these versions and upgrades directly to a future MySQL engine version that resolves this issue. Microsoft Azure MySQL remains committed to providing customers with the most secure and stable PaaS database service.

#### Features

This maintenance update doesn't introduce any new features.

#### Improvements

- Many security improvements are made to the service during this maintenance.

#### Known issues fixes

- Fix the issue that for some servers migrated from single server to flexible server, execute table partition leads to table corrupted.
- Fix the issue that for some servers with audit or slow log enabled, when a large number of logs are generated, these servers might be missing server metrics. The start operation might be stuck for these servers if they're in a stopped state.

## June 2024

The June 2024 maintenance focused on availability improvements and known issue fixes.

### Version release notes

We're pleased to announce the June 2024 maintenance for Azure Database for MySQL flexible server. In this maintenance update, we address some availability problems that affect a subset of servers. While most servers remain unaffected, a small portion experiences maintenance activities to enhance their performance and stability. We appreciate your understanding and patience as we work to improve our service.

#### Engine version changes

No engine version upgrade in this maintenance.

#### Features

This maintenance update doesn't introduce any new features.

#### Improvements

- Customers can now truncate `performance_schema` tables by invoking a predefined stored procedure.
- Improved the startup time for servers with a large number of tablespaces.

#### Known issues fixes

- Fixed the issue that MySQL engine might not receive the shutdown signal during scaling and maintenance, which might lead to long recovery time.
- Fixed the issue that if server with `originalPrimaryName` is deleted due to HA failover->disable HA action, earlier ATP update operation failed.
- Fixed the issue that unhealthy servers/Burstable servers without credits now throw `ServerNotSucceeded` instead of Internal Server Error.

## May 2024

The May 2024 maintenance introduced improvements, known issue fixes, and security patches.

### Version release notes

We're pleased to announce the May 2024 maintenance for Azure Database for MySQL flexible server. This maintenance incorporates several new features and improvements, along with known issue fixes and security patches.

#### Engine version changes

No engine version upgrade in this maintenance.

#### Improvements

- Improved server restart logic. Server restart has a timeout of two hours for non-burstable servers and a four-hour timeout for burstable servers. After server restart workflow timeout, it rolls back and sets the server state to Succeeded.
- Improved the data-in replication procedures to show the real error message and exit safely when an exception happens.
- Read replica improvement for the creation workflow to precheck the virtual network setting.

#### Known issues fixes

- Fixed the issue that the server parameter `max_connections` and `table_open_cache` can't be configured correctly.
- Fixed the issue where executing `CREATE AADUSER IF NOT EXISTS 'myuser' IDENTIFIED BY 'CLIENT_ID'` when the user already exists incorrectly sets the binlog record, affecting replica and high availability functionalities.

## April 2024

The April 2024 maintenance included minor version upgrades, improvements, known issue fixes, and security patches.

### Version release notes

Azure Database for MySQL flexible server April 2024 maintenance includes several new features and improvements, along with known issue fixes, minor version upgrades, and security patches.

> [!NOTE]  
> After a thorough assessment of the current maintenance processes, Microsoft observed an unusually high failure rate. Consequently, Microsoft decided to cancel the minor version upgrade maintenance scheduled for April. The rescheduling of the next minor version upgrade maintenance isn't determined at this time. Microsoft commits to providing at least one month's notice prior to the rescheduled maintenance to ensure all users are adequately prepared.

#### Engine version changes

All existing engine version server upgrades to 8.0.36 engine version.

#### Improvements

- Expose old_alter_table for 8.0.x.

#### Known issues fixes

- Fixed the issue where `GTID RESET` operation's retry interval was excessively long.
- Fixed the issue that data-in HA failover stuck because of system table corrupt.
- Fixed the issue that in point-in-time restore that database or table starts with special keywords might be ignored.
- Fixed the issue where, if there's replication failure, the system now ignores the replication latency metric instead of displaying a '0' latency value.
- Fixed the issue where under certain circumstances MySQL RP doesn't correctly get notified of a "private dns zone move operation". The issue causes the server to show incorrect ARM resource ID of the associated private dns zone resource.

## February 2024

The February 2024 maintenance focused on known issue fixes, underlying OS upgrades, and vulnerability patching.

### Version release notes

Azure Database for MySQL flexible server is updated in February 2024. This maintenance update mainly focuses on known issue fixes, underlying OS upgrades, and vulnerability patching.

> [!NOTE]  
> During the preliminary stages of the February-March maintenance period, the product team identified a regression issue that necessitated a reevaluation of the scheduled maintenance activities. Consequently, the product team canceled all maintenance sessions originally planned for the period from March 2, 13:00 UTC, to March 14, 00:00 UTC. The product team is currently in the process of rescheduling these maintenance activities. Affected customers are promptly notified of the new maintenance timetable. The product team apologizes for any inconvenience this might cause and thanks you for your understanding and continued support.

#### Engine version changes

- All existing 5.7.42 engine version servers upgrade to 5.7.44 engine version.
- All existing 8.0.34 engine version servers upgrade to 8.0.35 engine version.

#### Features

There are no new features in this maintenance update.

#### Improvements

There are no new improvements in this maintenance update.

#### Known issues fixes

- Fix HA standby replication deadlock issue caused by `slave_preserve_commit_order`.
- Fix promotion stuck issue when source server is unavailable or source region is down. Improve customer experience on replica promotion to better support disaster recovery.
- Fix the default value of `character_set_server` and `collation_server`.
- Allow customer to start InnoDB buffer pool dump.

## January 2024

The January 2024 maintenance includes accelerated logs and audit log enhancements, along with fixes for known issues.

### Version release notes

Azure Database for MySQL flexible server January 2024 maintenance includes several new features and fixes known issues for enhanced performance and reliability.

> [!NOTE]  
> Between 2024/01/12 04:00 UTC and 2024/01/15 07:00 UTC, Microsoft strategically paused Azure MySQL maintenance to proactively address a detected issue that could lead to maintenance interruptions. Maintenance operations are fully restored. For those affected, use the flexible maintenance feature to conveniently reschedule your maintenance times as needed.

#### Engine version changes

This maintenance update doesn't include any engine version changes.

#### Features

##### [Accelerated logs in Azure Database for MySQL](../flexible-server/concepts-accelerated-logs.md)

- Introduces a new type of disk designed to offer superior performance in storing binary logs and redo logs.

#### Improvements

##### [Track database activity with Audit Logs in Azure Database for MySQL flexible server](../flexible-server/concepts-audit-logs.md)

- In alignment with users' expectations for the audit log, Microsoft introduced wildcard support for audit log usernames and added connection status for connection logs.

#### Known issues fixes

##### Support Data-in Replication in Major Version Upgrade

- During an upgrade from 5.7 to 8.0, data-in replication encounters problems due to a known bug in the MySQL community. This January 2024 maintenance addresses this concern and enables data-in replication support for servers upgraded from version 5.7.

##### Server Operations Blockage After Moving Subscription or Resource Group

- Several server operations were blocked after transferring a subscription or resource group because of incomplete server information updates. This January 2024 maintenance resolves the problem and ensures unhindered movement of subscriptions and resource groups.

## Related content

- [What's new in Azure Database for MySQL flexible server in 2024](../whats-new/whats-new-2024.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)
