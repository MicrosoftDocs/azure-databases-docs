---
title: Release Notes for Azure Database for MySQL Flexible Server - March 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server March 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 03/14/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Azure Database For MySQL Flexible Server March 2025 Version Release Notes

We're excited to announce the March 2025 version of Azure Database for MySQL Flexible Server. Starting March 14, 2025, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

No major or minor version upgrade for all existing servers.

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt, or use the CLI command below

```bash 
az mysql flexible-server show --resource-group {resource group name} --name {server name} --query "fullVersion"
```
> [!NOTE]  
> You must have the Azure CLI installed and updated to the latest version to run the above CLI command.

## Features

- Public Preview for HA with dedicated SLB. With this change, we don't change DNS during failover. It reduces the failover time for HA server(usually 30 seconds depending on your DNS Cache TTL setting). Note this feature won't directly applied to existing servers by default due to the nature enabling it will bringing downtime. If your existing server want to enable this feature, try re-enable your HA feature. [Learn more]()

## Improvement


## Known Issues Fix
- Fix the issue due to an internal error, the correct charges of your consumption for geo-redundant servers was not previously reflected in your billing. This issue has now been resolved, and moving forward your billing will align with the actual usage.
