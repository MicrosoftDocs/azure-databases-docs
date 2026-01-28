---
title: Release Notes for Azure Database for MySQL Flexible Server - October 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server October 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 10/01/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database for MySQL Flexible Server October 2025 version release notes

We're excited to announce the October 2025 version of Azure Database for MySQL Flexible Server. Starting October 1, 2025, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

- No changes to existing 8.0 server.
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

- General availability of custom port support in Azure Database for MySQL Flexible Server. [Learn more](../concepts-networking.md#custom-port-support)
  
## Improvements

- Resource movement now support move resources that has private endpoints. 

## Known issues fix

- Fixed the issue where replicas of source servers with geo-backup enabled could experience worsening replication lag under certain conditions. Once lag began, replicas failed to catch up and the delay continued to grow, independent of workload. This fix ensures replication lag now stabilizes and recovery mechanisms behave as expected. 
