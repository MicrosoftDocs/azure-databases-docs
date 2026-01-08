---
title: Release Notes for Azure Database for MySQL Flexible Server - September 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server September 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database for MySQL Flexible Server September 2025 version release notes

The September 2025 version of Azure Database for MySQL Flexible Server is now available. Starting September 1, 2025, all new servers automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

This version introduces new features and enhancements, resolves known problems, and includes important security patches to ensure optimal performance and security.

> [!IMPORTANT]  
> - During maintenance for this version, Azure Database for MySQL forces an upgrade of the TLS 1.0/1.1 setting to TLS 1.2. If you still use TLS 1.0 or 1.1 to connect to your MySQL servers, update your clients to support TLS 1.2. Otherwise, you might experience connectivity problems after the new version is applied.
> - To maintain strong security and compliance standards, Azure Database for MySQL rotates certificate authorities (CAs) during maintenance for this version. For more information about the process and actions you can take to preserve connectivity across the maintenance, see [Certificate rotation for Azure Database for MySQL Flexible Server](/azure/mysql/flexible-server/security-tls-root-certificate-rotation).

## Engine version changes

- All existing 8.0 servers upgrade to version 8.0.42.
- No changes to existing 8.4 servers.
- No changes to existing 5.7 servers.
- No changes to innovation release version servers.

To check your engine version, run the `SELECT VERSION();` command at the MySQL prompt.

After the maintenance succeeds, run the following command in Azure CLI to check the Azure MySQL minor version:

```azurecli
az mysql flexible-server show --resource-group {resource group name} --name {server name} --query "fullVersion"
```

> [!NOTE]  
> To run the preceding CLI command, install Azure CLI and update it to the latest version.

## Features

- General availability of Azure Database for MySQL 8.4. [Learn more](../../concepts-version-policy.md#supported-mysql-versions).
- Preview of dedicated SLB based HA. [Learn more](../how-to-configure-high-availability.md).
- Support for in place major version upgrade from 8.0 to 8.4. [Learn more](../how-to-upgrade.md).

> [!NOTE]  
> Existing servers must upgrade to the latest version through the next scheduled maintenance to gain the capability to in place upgrade from 8.0 to 8.4.

## Improvements

- Data migration service can now detect data corruption during external data migration, with both rest API and mysql import CLI support.
- Capacity related server creation error messages are more descriptive and include the link to the customer-facing troubleshooting guide.
- Error message related to private endpoint operations is more descriptive.
- Introduced a new built-in store procedure `mysql.az_drop_broken_table` to fix table corruption issue. [Learn more](../concepts-built-in-store-procedure.md#drop-problematic-table).

## Known issues fix

- Fixed the issue that in certain scenarios, virtual network server enabling fails.
- Fixed the issue that in certain scenarios, virtual network server creation or point in time recovery gets stuck until a timeout or customer cancel it.
- Fixed the issue that the resource ID isn't properly returned when executing an ARG query on the `servicehealthresources` table.
