---
title: Release Notes for Azure Database for MySQL Flexible Server - January 2026
description: Learn about the release notes for Azure Database for MySQL Flexible Server January 2026.
ai-usage: ai-assisted
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 01/14/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database For MySQL - Flexible Server January 2026 version release notes

We're excited to announce the January 2026 version of Azure Database for MySQL Flexible Server. Starting January 22, 2026, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

There will be no engine version changes in this version.

## Features

No new features are being introduced in this version.

## Improvement

- Improved the error message shown when customers attempt to enable HA on a VNET-based instance that still has Accelerated Logs enabled

## Known issues fixes

- Fixed an issue where enabling geo backup caused subsequent GTID reset operations to fail
- Fixed an issue where certain HA servers behind a dedicated SLB could not enable a private endpoint


