---
title: Release Notes for Azure Database for MySQL Flexible Server - October 2024
description: Learn about the release notes for Azure Database for MySQL Flexible Server October 2024.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: release-notes
---

# Azure Database For MySQL Flexible Server October 2024 Maintenance

We're pleased to announce the October 2024 maintenance for Azure Database for MySQL Flexible Server. This maintenance incorporates several new features and improvement, along with known issue fix, and security patches.

## Engine version changes

No engine version upgrade in this maintenance.

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt

## Features

No new features are being introduced in this maintenance update.

## Improvement

- The default value of the server parameter tls_version change to "TLSv1.2, TLSv1.3" on MySQL 8.0, which means connections with TLSv1.3 are accepted by default.
- Expose the server parameters innodb_ddl_buffer_size and innodb_ddl_threads
- US region servers will be upgraded to a FIPS-compliant version by default. For more information, see [Azure FIPS compliance](/azure/compliance/offerings/offering-fips-140-2)

## Known Issues Fix

- Fix the issue that if the authentication plugin of the admin user changed, resetting password feature doesn't work.
- Fix the issue that Servers configured with high max_connections might not work as expected.
- Fix the issue that if a server start/stop more than 120 times the server would unable to be deleted.
- Fix the issue that major version upgrade validate function might stuck and block upcoming management operations such as server stop/start/update/delete.
- Fix old geo replica promote stuck issue
