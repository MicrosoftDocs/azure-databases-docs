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

# Azure Database for PostgreSQL: April 2026 Release

We're excited to announce the April 2026 version of Azure Database for PostgreSQL. Beginning April 22, 2026, the service automatically onboards all new servers to this latest version. The service upgrades existing servers during their next scheduled maintenance.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- No change.

## Features

- Virtual network to private endpoint migration for high availability enabled servers is now available.

## Improvements 

- Improved error handling when the Private DNS Zone subscription isn't registered for Microsoft.DBforPostgreSQL, preventing prolonged retries and surfacing a clearer customer facing error.
- Subnets with both IPv4 & IPv6 now supported for Flexible Server integration. Note: PostgreSQL connections are still limited to IPv4 only.

## Known issues fix

- Fixed an issue that could lead to authentication failures when Microsoft Entra ID token size exceeds 4 KB (~4,080 characters) while using Bouncer with Microsoft Entra ID authentication.
- Improved handling of race conditions during server deletion when private endpoints are configured.
- Addressed an issue where virtual network to private endpoint migration could leave public access enabled.



## Related content

- [Release notes - Azure Database for PostgreSQL](../flexible-server/release-notes.md)