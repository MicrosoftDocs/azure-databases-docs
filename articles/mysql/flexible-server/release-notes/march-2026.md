---
title: Release Notes for Azure Database for MySQL Flexible Server - April 2026
description: Learn about the release notes for Azure Database for MySQL Flexible Server April 2026.
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 03/28/2026
ms.service: azure-database-mysql
ms.topic: release-notes
ai-usage: ai-assisted
---

# Azure Database for MySQL March 2026 version release notes

The March 2026 version of Azure Database for MySQL Flexible Server is now available. Starting March 31, 2026, all new servers will automatically use this version. Existing servers upgrade during their next scheduled maintenance. To upgrade your servers earlier, enroll in the [Virtual Canary Program](https://aka.ms/mysql/virtual-canary).

This version introduces enhancements, resolves known problems, and includes important security patches to ensure optimal performance and security.

## Maintenance scheduling considerations
  
The maintenance reschedule window can be extended up to the end of April.
Some servers with CMW enabled might be assigned a maintenance date outside of their preferred window. You can still reschedule the maintenance in the Azure portal to better align with your original CMW preference.

## Engine version changes

This version doesn't include any engine version changes.

## Features

This version doesn't introduce any new features.

## Improvements

- Returns clear, actionable customer‑facing errors for invalid key scenarios, improving troubleshooting and support experience.
- Enables self‑service configuration of binlog_row_metadata, unblocking CDC/Data Out integrations and reducing support dependency.

## Known issues fixes

- Adds check to see if target AZ is available as a supported zone for the specific SKU.
