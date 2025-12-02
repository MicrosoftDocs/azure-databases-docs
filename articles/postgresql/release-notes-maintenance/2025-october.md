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

We're excited to announce the October 2025 version of Azure Database for PostgreSQL. Starting October 24, 2025, all new servers are automatically onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- No engine version upgrade in this maintenance release.

## Features

- [PgBouncer](https://www.pgbouncer.org/usage.html#admin-console) updated from version 1.22 to 1.23. Admin console queries now include additional columns with this update.
- [Citus 13.2](https://www.citusdata.com/updates/v13-2/) set as the default for PG16 & PG17 for all new Elastic Cluster provisions
- Enabled the query store extension for PG18.
- [pg_squeeze](https://github.com/cybertec-postgresql/pg_squeeze) extension upgraded to version 1.9 resolving a critical bug in the squeeze.squeeze_table() function that could lead to data corruption.
- [IP4R](https://github.com/RhodiumToad/ip4r) extension enabled.
- TimescaleDB extension upgraded to V2.22.0

## Known issues fix

- Fixed issue, which could leave a server in a failed state after user attempts a Start operation multiple times in a region experiencing capacity constraints. The server is now brought to a deallocated state in these situations, and a capacity-related error message is returned to the user. This fix now enables users to reattempt Start operations without the server entering a failed state.


## Related content

- [Release notes - Azure Database for PostgreSQL](../flexible-server/release-notes.md)