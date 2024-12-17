---
title: Release Notes for Azure Database for MySQL Flexible Server - January 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server January 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 01/06/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Azure Database For MySQL Flexible Server January 2025 Version Release Notes

We're excited to announce the January 2025 version of Azure Database for MySQL Flexible Server. Starting January 6, 2025, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this link.

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

All existing 8.0 major version servers are upgraded to 8.0.40 minor version

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt, or run the following command in the Azure Cloud Shell:

```bash 
az mysql flexible-server show --resource-group {resource group name} --name {server name} --query "fullVersion"
```

Note you must have the Azure CLI installed and updated to the latest version to run the above CLI command.

## Features

- Support customer managed plugin enablement for MySQL Flexible Server: validate_password are supported.
- Support checking the full version information through Azure CLI.
- Support enrollment of Virtual Canary Program through Azure CLI.

## Improvement
- Export backup destination folder name is changed from timestamp to backupName

## Known Issues Fix
- Fix the issue that changing customer maintenance window failed in some scenarios
- Fix the issue that when server is migrated from single server to flexible server and new partial table is created after the migration, the major version upgrade will fail.
