---
title: Release Notes for Azure Database for MySQL Flexible Server - February 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server February 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 02/06/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: article
---

# Azure Database For MySQL Flexible Server February 2025 Version Release Notes

We're excited to announce the February 2025 version of Azure Database for MySQL Flexible Server. Starting February 10, 2025, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

No major or minor version upgrade for existing 5.7 servers.

All existing 8.0 major version servers are upgraded to 8.0.40 minor version, learn more about MySQL 8.0.40 version by following this [link](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-40.html)

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt.

After the maintenance succeeds, you can run the following command in the Azure CLI to check the Azure MySQL minor version as well:

```bash 
az mysql flexible-server show --resource-group {resource group name} --name {server name} --query "fullVersion"
```
> [!NOTE]  
> You must have the Azure CLI installed and updated to the latest version to run the above CLI command.

## Features

- Support customer managed plugin enablement for MySQL Flexible Server: validate_password are supported.
- Support checking the full version information through Azure CLI.
- Support enrollment of Virtual Canary Program through Azure CLI.

## Improvement
- Enhancements to online schema changes now prevent data loss and duplicate key issues, ensuring better data integrity. These improvements is applied to all new and existing servers. DDL operations on tables are now more reliable, reducing the risk of inconsistencies. For more details on the bug, [check the blog](https://techcommunity.microsoft.com/blog/adformysql/best-practices-for-safely-performing-schema-changes-in-azure-database-for-mysql/4356830).
- Export backup destination folder name is changed from timestamp to backupName.

## Known Issues Fix
- Fixed the issue where changing the customer maintenance window failed in certain scenarios.
- Fixed the issue where migrating a server from Single Server to Flexible Server and creating a new partial table after migration caused the major version upgrade to fail.
- Fixed the issue where the MySQL parameter `event_scheduler` was incorrectly turned off during an HA server failover.
- Fixed the issue where the major version upgrade failed when the audit log was enabled with ConnectionV2.
- Fixed the issue where a major version upgrade could lead to incomplete rollbacks, causing MySQL to repeatedly crash after rolling back to version 5.7.
- Fixed the issue where the `audit_log_exclude_users` parameter was unavailable with the `table_access` event.
