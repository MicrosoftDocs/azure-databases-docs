---
title: Release Notes for Azure Database for PostgreSQL Maintenance - April 2026
description: Learn about the maintenance release notes for Azure Database for PostgreSQL April 2026.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 04/21/2026
ms.service: azure-database-postgresql
ms.topic: release-notes
---

# Azure Database for PostgreSQL: April 2026 release

We're excited to announce the April 2026 version of Azure Database for PostgreSQL. Beginning April 22, 2026, the service automatically onboards all new servers to this latest version. The service upgrades existing servers during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- Latest minor versions updated for Azure Database for PostgreSQL: 18.3, 17.9, 16.13, 15.17 and 14.22

## Features

- Added support for the Apache AGE extension in PostgreSQL 18.
- Added support for the pg_diskANN extension in PostgreSQL 18.
- Virtual network (VNET) to private endpoint migration for high availability enabled servers is now available.
- **Premium SSD V2 storage**: Now **Generally Available**. It includes instant snapshot access for read-replicas, point-in-time restore (PITR), restore of deleted servers, customer managed keys (CMK) and online storage scaling.
- **Cascading Replicas**: Now **Generally Available** with several known issues addressed.
- **Cross-Tenant Customer Managed Keys (CMK)**: Introduced support for customer-managed keys across tenants **(Private Preview)**
- **Fabric mirroring - support for servers with read replicas**: Fabric mirroring is now enabled on servers with read replicas.
- **Fabric mirroring – support for HA servers running PG14 – 16**: Fabric mirroring now available on HA PostgreSQL servers running PG14-16. Mirroring must be restarted after a failover unlike on PG17+ servers.


## Improvements 

- Updated pg_duckdb extension to version 1.1.1, adding write support for Azure Blob Storage along with improvements.
- Updated pgvector extension to version 0.8.0.2.
- Improved error handling when the Private DNS Zone subscription isn’t registered for Microsoft.DBforPostgreSQL, preventing prolonged retries and surfacing a clearer customer facing error.
- Subnets with both IPv4 & IPv6 now supported for Flexible Server integration. PostgreSQL connections are still limited to IPv4 only.
- Improved export behavior for unconstrained numeric columns by using Decimal128(38, 0) as the default, aligning with SQL standard conventions and avoiding unnecessary fractional digits.
- **Replica creation timeout enhancement**: Introduced dynamic timeout handling for geo-replica creation operations.
- **Improved Error Messaging**: Enhanced several user-facing error messages to provide clearer and more actionable feedback.
- Converted the following PostgreSQL native types to string representation: XML, JSON, JSONB, INET, CIDR, MACADDR, MACADDR8, TSVECTOR, TSQUERY, INT4RANGE, INT8RANGE, NUMRANGE, TSRANGE, TSTZRANGE, DATERANGE, CIRCLE, LINE, LSEG, BOX, PATH, POINT, POLYGON


## Known issues fix

- Fixed an issue that could lead to authentication failures when Microsoft Entra ID token size exceeds 4 KB (~4,080 characters) while using PgBouncer with Microsoft Entra ID authentication.
- Improved handling of race conditions during server deletion when private endpoints are configured.
- Addressed an issue where virtual network (VNET) to private endpoint migration could leave public access enabled.
- Included security fixes for CVE-2026-2004, CVE-2026-2005, CVE-2026-2006, and CVE-2025-4207 in PostgreSQL 11 through 13 under extended support.



## Related content

- [Release notes - Azure Database for PostgreSQL](../flexible-server/release-notes.md)