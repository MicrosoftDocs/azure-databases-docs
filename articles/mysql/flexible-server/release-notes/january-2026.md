---
title: Release Notes for Azure Database for MySQL Flexible Server - January 2026
description: Learn about the release notes for Azure Database for MySQL Flexible Server January 2026.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 01/14/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database For MySQL - Flexible Server January 2026 version release notes

We're excited to announce the January 2026 version of Azure Database for MySQL Flexible Server. Starting January 14, 2026, all new servers will automatically be onboarded to this latest version. Existing servers are upgraded during their next scheduled maintenance. If you prefer to upgrade your servers earlier, you can enroll in our Virtual Canary Program by following this [link](https://aka.ms/mysql/virtual-canary).

This new version introduces a range of new features and enhancements, resolves known issues, and includes essential security patches to ensure optimal performance and security.

## Engine version changes

There will be no engine version changes in this version.

## Features

No new features are being introduced in this version.

## Improvement

- Improved the error message when customer failed to enable HA on instance on VNET with Accelerated logs enabled
- Add auto linking support when reader endpoint enabled server are creating new read replica server.

## Known issues fixes

- Fixed the issue that after opening geo backup, the GTID reset would fail
- Fixed the issue that for some HA servers on dedicate SLB, enable private endpoint would fail


