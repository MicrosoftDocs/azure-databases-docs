---
title: Release Notes for Azure Database for PostgreSQL Maintenance - January 2026
description: Learn about the maintenance release notes for Azure Database for PostgreSQL January 2026.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 01/30/2026
ms.service: azure-database-postgresql
ms.topic: concept-article
---

# Azure Database For PostgreSQL January 2026 Maintenance Release Notes

We're excited to announce the January 2026 version of Azure Database for PostgreSQL. Starting January 20, 2026, all new servers are automatically onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- PG18 now generally available on Azure Database for PostgreSQL for new server deployments.
- Latest [minor versions](https://learn.microsoft.com/azure/postgresql/configure-maintain/concepts-supported-versions) updated for Azure Postgres Flexible Server: 18.1, 17.7, 16.11, 15.15, 14.20, and 13.23 .
- Added PG18 support for Fabric mirroring.

## Features

- credcheck extension is now available. Enforce password and credential validation policies directly within PostgreSQL using credcheck.
- pg_duckdb extension **(Public Preview)** is now available.  Accelerate analytics using DuckDB’s vectorized, columnar execution.
- anon extension is now available. Enhance data anonymization capabilities for protecting sensitive information in your databases.
- Support for PG18 as a target PG version for migrations.
- Support for Apache AGE 1.6.0 extension in PostgreSQL 16.
- Added a new API to let customers switch their server network from VNet integration to Private Endpoint. **Note**: This capability is currently limited to servers that are non‑HA and do not have replicas.
- **Elastic cluster**: Introduced support for routing traffic directly to worker nodes in Elastic cluster by using port offsets.
- **Elastic  cluster – Geo Restore**: Restore cluster to a different region with a simple, reliable geo restore workflow.
- **Elastic cluster – Custom Database Name**: Create clusters with a database name of your choice for easier organization and migration during provisioning.
- **Cascading Replica (Limited Public Preview)**: Scale read workloads with multi-level cascading replicas, now available in select regions.

## Improvemnents 

- Updated validation for the pg_partman_bgworker_role server parameter to allow role names that include numeric characters.
- Improved TOAST compression performance by changing the default compression algorithm to LZ4.
- Azure Storage extension now supports importing and exporting Apache Parquet format.
- Updated validation rules to block the use of certain special characters (', ", ;, --) in Entra ID usernames through the web API.
- Query text captured by Query Store can now be emitted to customer Log Analytics via Azure Diagnostics Settings, controlled by the pg_qs.emit_query_text server parameter (GUC).
- Query Store supports capturing runtime statistics and wait statistics in read replicas and streaming them to telemetry via Diagnostics Settings.
- Multiple performance improvements in Query Store significantly reduce runtime overhead, resulting in faster and more efficient query execution.
- Query Store now captures and emits parameters names - improving clarity, debuggability and accuracy of query metadata.
- New performance metrics (wal_write_bytes, wal_write_count, and wal_write_latency) are now emitted by write ahead log (WAL).
- **Elastic cluster – Add Node Firewall Parity**: New nodes now automatically inherit existing firewall rules, ensuring seamless and secure scale out.
- **Elastic cluster**: Citus_stat_counters metric is enabled by default to provide improved Elastic cluster telemetry.
- **Server Parameters – Reliability Improvements**: Server parameter updates are now more resilient, reducing failures and improving configuration consistency.
- **Server Deletion – Name Reuse Reliability**: Enhanced delete reliability ensures server names can be safely reused without delays or stuck resources.
- Several targeted improvements and bug fixes that enhance stability, reliability, and overall service experience.

## Known issues fix

- Fixed a rare race condition that could cause synchronized_standby_slots to be incorrect during high availability failover.
- Fixed an issue that could cause near zero downtime scaling operations to stall under certain high availability configurations.
- Fixed a race condition that was causing authentication errors after certification rotation on Fabric mirroring.
- Elastic cluster - Adding a node to an Elastic cluster where previously installed extensions need an update no longer fails.


## Related content

- [Release notes - Azure Database for PostgreSQL](../flexible-server/release-notes.md)