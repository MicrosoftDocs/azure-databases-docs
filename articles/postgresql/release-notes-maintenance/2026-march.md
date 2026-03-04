---
title: Release Notes for Azure Database for PostgreSQL Maintenance - March 2026
description: Learn about the maintenance release notes for Azure Database for PostgreSQL March 2026.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 03/03/2026
ms.service: azure-database-postgresql
ms.topic: release-notes
---

# Azure Database for PostgreSQL: March 2026 Release

We're excited to announce the March 2026 version of Azure Database for PostgreSQL. Starting March 3, 2026, the service automatically onboards all new servers to this latest version. The service upgrades existing servers during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- Latest minor verions updated for Azure Database for PostgreSQL: 18.2, 17.8, 16.12, 15.16, and 14.21.

## Features

- Added ability for authorized users to assign the pg_use_reserved_connections role.
- Enabled TimescaleDB support for PostgreSQL 18.
- Elastic clusters - Cluster-level point-in-time restore from SSDv1 to SSDv2 storage is now supported, with storage IOPS and throughput automatically calculated.
- Elastic clusters: Execute queries for PostgresDifferentialMetricsCollector and PostgresStatsCollector against Citus database.
- **Server Parameters**: cron.timezone parameter is now configurable, allowing you to set your preferred time zone for scheduled cron jobs.
- Support for VNET-to-Private Endpoint migration for HA servers. High Availability (HA) enabled servers can now be migrated from VNET integration to Private Link.

## Improvements 

- PgBouncer upgraded to latest community version release version v1.25.1 
- Updated anon extension to version 2.5.1.
- Updated PostGIS to version 3.6.1.
- Updated the orafce extension to version 4.16.3.
- Updated TimescaleDB to version 2.23.0.
- Updated Semver extension to version 0.41.0
- Updated Tdigest extension to 1.4.3
- Updated Pg_partman extension to 5.3.1
- Updated Hll extension to version 2.19
- Various improvements to metrics reliability.
- Improved pgms_wait_sampling to capture correct query IDs for utility statements (for example, DDL/maintenance), ensuring wait events are accurately attributed.
- **Elastic clusters**: citus_stat_counters differential metrics are now enabled by default
- **Elastic clusters - Firewall rule consistency**: Firewall rules are now self-healed across primary and standby instances, eliminating metadata mismatches after updates.
- **Elastic clusters - HA firewall mirroring fix**: Firewall rule mirroring on HA clusters now correctly targets the standby Network Security Group.
- **Elastic clusters - Node discoverability**: Cluster node active probe is enabled by default, ensuring new nodes are immediately discoverable.
- **Fabric mirroring – Update table ownership requirement**: Table ownership is no longer required for mirrored tables that have a replica identity configured. Ownership is now only required for tables without a defined replica identity.
- **Fabric mirroring - Pre-validation of mirroring prerequisites**: Added a database-level prerequisite validation step during table selection. If the necessary mirroring prerequisites aren't met, the operation now fails early before initiating publication.
- **MongoDB clusters – Simplified deletion with Private Link enabled**: You can now delete MongoDB clusters that have a Private link configured without first removing the Private Link.
- Several targeted improvements and bug fixes to enhance stability, reliability, and overall service experience.

## Known issues fix

- Fixed an issue to improve cleanup of replication slots, addressing rare edge‑case scenarios.
- Fixed an issue where PgBouncer could be deemed unhealthy when reaching max client connections (leading to PgBouncer restart). This fix prevents unnecessary restarts.
- **Improved server deletion reliability**: Fixed an edge case where a server deletion could become stuck if provisioning was still in progress.
- **Improved deletion stability for server and Private Endpoint**: Resolved a race condition that could cause drop operations to become stuck when rapid deletion requests are issued for both a server and its Private Endpoint.
- **Elastic clusters**: Active node probe now correctly verifies primary role, preventing traffic from being routed to non-primary nodes.



## Related content

- [Release notes - Azure Database for PostgreSQL](../flexible-server/release-notes.md)