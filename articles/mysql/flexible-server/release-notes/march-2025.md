---
title: Release Notes for Azure Database for MySQL - March 2025
description: Learn about the release notes for Azure Database for MySQL Flexible Server March 2025.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 04/22/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database For MySQL Flexible Server March 2025 Version Release Notes

We're excited to announce the March 2025 version of Azure Database for MySQL. All new servers are automatically onboarded to the latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by visiting [Scheduled maintenance in Azure Database for MySQL](https://aka.ms/mysql/virtual-canary).

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

- Public Preview for HA with dedicated SLB. With this feature, a dedicated [Load Balancer](/azure/load-balancer/load-balancer-overview) is added to a High availability (HA) configuration, helping the HA servers use the benefits offered by a load balancer i.e., low latency, high throughput network traffic distribution of front-end requests to back-end servers. SLB managing the MySQL data traffic path eliminates the need for changing the DNS during failover, thereby improving the failover time by ~ 20 seconds.

## Improvement

- No major improvement in this release.

## Known Issues Fix

- Fix the issue due to an internal error, the correct charges of your consumption for geo-redundant servers wasn't previously reflected in your billing. This issue is now resolved, and moving forward your billing aligns with the actual usage.
