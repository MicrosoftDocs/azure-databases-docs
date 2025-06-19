---
title: Release Notes for Azure Database for MySQL Flexible Server - September 2024
description: Learn about the release notes for Azure Database for MySQL Flexible Server September 2024.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: article
---

# Azure Database For MySQL Flexible Server September 2024 Maintenance

We're pleased to announce the September 2024 maintenance for Azure Database for MySQL Flexible Server. This maintenance is to upgrade servers that are still on TLS 1.0/1.1 to TLS 1.2 version

## Engine version changes

No engine version upgrade in this maintenance.

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt

## Features

No new features are being introduced in this maintenance update.

## Improvement

- Mandatory upgrade of all servers currently using TLS 1.0 or 1.1 to TLS 1.2. [Connect to Azure Database for MySQL - Flexible Server with encrypted connections](../how-to-connect-tls-ssl.md)

## Known issues fixes

No known issue fixes are being introduced in this maintenance update.
