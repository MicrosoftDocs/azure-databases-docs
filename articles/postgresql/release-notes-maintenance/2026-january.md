---
title: Release Notes for Azure Database for PostgreSQL Maintenance - January 2026
description: Learn about the maintenance release notes for Azure Database for PostgreSQL January 2026.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 02/05/2026
ms.service: azure-database-postgresql
ms.topic: release-notes
---

# Azure Database for PostgreSQL: January 2026 Release

We're excited to announce the January 2026 version of Azure Database for PostgreSQL. Starting January 20, 2026, the service automatically onboards all new servers to this latest version. The service upgrades existing servers during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- PG18 is now generally available on Azure Database for PostgreSQL for new server deployments.
- Added PG18 support for Fabric mirroring.

## Features

- credcheck extension is now available. Enforce password and credential validation policies directly within PostgreSQL by using credcheck.
- pg_duckdb extension **(Public Preview)** is now available. Accelerate analytics by using DuckDB’s vectorized, columnar execution.
- anon extension is now available. Enhance data anonymization capabilities for protecting sensitive information in your databases.
- Support for PG18 as a target PG version for migrations.
- Support for Apache AGE 1.6.0 extension in PostgreSQL 16.
- Added a new API to let customers switch their server network from virtual network integration to Private Endpoint. **Note**: This capability is currently limited to servers that are non‑HA and don't have replicas.
- **Elastic clusters**: Introduced support for routing traffic directly to worker nodes in Elastic clusters by using port offsets.
- **Elastic  clusters – Geo Restore**: Restore clusters to a different region with a simple, reliable geo restore workflow.
- **Elastic clusters – Custom Database Name**: Create clusters with a database name of your choice for easier organization and migration during provisioning.

## Improvements 

- Updated validation for the `pg_partman_bgworker_role` server parameter to allow role names that include numeric characters.
- Improved TOAST compression performance by changing the default compression algorithm to LZ4.
- Azure Storage extension now supports importing and exporting Apache Parquet format.
- Updated validation rules to block the use of certain special characters (`'`, `"`, `;`, `--`) in Microsoft Entra ID usernames through the web API.
- Query text captured by Query Store can now be sent to customer Log Analytics via Azure Diagnostics Settings, controlled by the `pg_qs.emit_query_text` server parameter (GUC).
- Query Store supports capturing runtime statistics and waits statistics in read replicas and streaming them to telemetry via Diagnostics Settings.
- Multiple performance improvements in Query Store significantly reduce runtime overhead, resulting in faster and more efficient query execution.
- Query Store now captures and sends parameter names, improving clarity, debuggability, and accuracy of query metadata.
- New performance metrics (`wal_write_bytes`, `wal_write_count`, and `wal_write_latency`) are now emitted by write ahead log (WAL).
- **Elastic clusters – Add Node Firewall Parity**: New nodes automatically inherit existing firewall rules, ensuring seamless and secure scaling out.
- **Elastic clusters**: `citus_stat_counters` metric is enabled by default to provide improved Elastic clusters telemetry.
- **Server Parameters – Reliability Improvements**: Server parameter updates are more resilient, reducing failures and improving configuration consistency.
- **Server Deletion – Name Reuse Reliability**: Enhanced delete reliability ensures server names can be safely reused without delays or stuck resources.
- Several targeted improvements and bug fixes that enhance stability, reliability, and overall service experience.

## Known issues fix

- Fixed a rare race condition that could cause `synchronized_standby_slots` to be incorrect during high availability failover.
- Fixed an issue that could cause near zero downtime scaling operations to stall under certain high availability configurations.
- Fixed a race condition that was causing authentication errors after certification rotation on Fabric mirroring.
- **Elastic clusters**: Adding a node to an Elastic clusters where previously installed extensions need an update no longer fails.


## Related content

- [Release notes - Azure Database for PostgreSQL](../flexible-server/release-notes.md)