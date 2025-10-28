---
title: Release Notes for Azure Database for PostgreSQL Maintenance - October 2025
description: Learn about the maintenance release notes for Azure Database for PostgreSQL Flexible Server October 2025.
author: jasomaning
ms.author: jasomaning
ms.reviewer: maghan
ms.date: 10/24/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Azure Database For PostgreSQL October 2025 Maintenance Release Notes

We're excited to announce the October 2025 version of Azure Database for PostgreSQL. Starting October 24th, 2025, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- No engine version upgrade in this maintenance.

## Features

- [PgBouncer](https://www.pgbouncer.org/usage.html#admin-console) updated from version 1.22 to 1.23. Admin console queries now include additional columns with this update.
- [Citus 13.2](https://www.citusdata.com/updates/v13-2/) set as the default for PG16 & P17 for all new Elastic Cluster provisions
- Enabled the query store extension for PG 18.
- [pg_squeeze](https://github.com/cybertec-postgresql/pg_squeeze) extension upgraded to version 1.9 resolving a critical bug in the squeeze.squeeze_table() function that could lead to data corruption.
- [IP4R](https://github.com/RhodiumToad/ip4r) extension enabled.
- timescaleDb upgraded to V2.22.0


## Improvements

- No major improvements are being introduced in this maintenance update.

## Known issues fix

- Fixed issue which left VM in a failed state after user attempts start operation multiple times in a region experiencing a capacity outage. VM will now be brought to a deallocated state in these situations, and a capacity-related error message will be returned to the user.