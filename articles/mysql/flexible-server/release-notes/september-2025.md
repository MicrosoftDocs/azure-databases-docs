---
title: Release Notes for Azure Database for MySQL Flexible Server - September 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server September 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 09/01/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database for MySQL Flexible Server September 2025 version release notes

We're excited to announce the September 2025 version of Azure Database for MySQL Flexible Server. Starting September 1, 2025, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

> [!IMPORTANT]
> - We'll force upgrade TLS 1.0/1.1 setting to TLS 1.2 during maintenance for this version. For customer who are still using TLS 1.0/1.1 to connect to their MySQL servers, we recommend updating their clients to support TLS 1.2, otherwise they may experience connectivity issues after the new version is applied. 
> - A new certificate authorities (CAs) will be rotated during the maintenance for this version to maintain strong security and compliance standards. For more details about the process and actions to be taken to preserve connectivity across the maintenance, you can review our documentation here: [Certificate rotation for Azure Database for MySQL Flexible Server](/azure/mysql/flexible-server/concepts-root-certificate-rotation).

## Engine version changes

- All existing 8.0 server upgrades to 8.0.42 version.
- No changes to existing 8.4 server.
- No changes to existing 5.7 server.
- No changes to innovation release version server. 

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt.

After the maintenance succeeds, you can run the following command in the Azure CLI to check the Azure MySQL minor version as well:

```bash 
az mysql flexible-server show --resource-group {resource group name} --name {server name} --query "fullVersion"
```
> [!NOTE]  
> You must have the Azure CLI installed and updated to the latest version to run the above CLI command.

## Features

- General availability of Azure Database for MySQL 8.4. [Learn more](../../concepts-version-policy.md#supported-mysql-versions)
- Public Preview of dedicated SLB based HA. [Learn more](../how-to-configure-high-availability.md)
- Support for in place major version upgrade from 8.0 to 8.4. [Learn more](../how-to-upgrade.md)

> [!NOTE]  
> Existing servers must be upgraded to the latest version through the next scheduled maintenance gain the capability to in place upgrade from 8.0 to 8.4.

## Improvements

- Data migration service can now detect data corruption during external data migration, with both rest API and mysql import CLI support
- Improve capacity related server creation error messages, make them more descriptive and to include the link to the customer-facing troubleshooting guide. 
- Improve the error message related to private endpoint operations.
- Introduced a new built-in store procedure `mysql.az_drop_broken_table` to fix table corruption issue. [Learn more](../concepts-built-in-store-procedure.md#drop-problematic-table)

## Known issues fix

- Fix the issue that in certain scenarios, VNet server enabling would fail.
- Fix the issue that in certain scenarios, VNet server creation or point in time recovery gets stuck until a timeout or customer cancel it
- Fix the issue that the resource id is not being properly returned when executing an ARG query on servicehealthresources table.
