---
title: Release Notes for Azure Database for MySQL Flexible Server - September 2024
description: Learn about the release notes for Azure Database for MySQL Flexible Server September 2024.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan, randolphwest
ms.date: 01/05/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database for MySQL Flexible Server September 2024 maintenance

The September 2024 maintenance for Azure Database for MySQL Flexible Server upgrades servers that use TLS 1.0 or 1.1 to TLS 1.2.

## Engine version changes

This maintenance doesn't upgrade the engine version.

To check your engine version, run the `SELECT VERSION();` command at the MySQL prompt.

## Features

This maintenance update doesn't introduce new features.

## Improvement

- The maintenance upgrade is mandatory for all servers that use TLS 1.0 or 1.1 to TLS 1.2. [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](../security-tls-how-to-connect.md)

## Known issues fixes

This maintenance update doesn't introduce known issue fixes.
