---
title: Release Notes for Azure Database for MySQL Flexible Server - April 2024
description: Learn about the release notes for Azure Database for MySQL Flexible Server April 2024.
author: xboxeer
ms.author: yuzheng1
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Azure Database For MySQL - Flexible Server April 2024 maintenance

We're pleased to announce the April 2024 maintenance for Azure Database for MySQL Flexible Server. This maintenance incorporates several new features and improvement, along with known issue fix, minor version upgrade, and security patches.

> [!NOTE]  
> We regret to inform our users that after a thorough assessment of our current maintenance processes, we have observed an unusually high failure rate across the board. Consequently, we have made the difficult decision to cancel the minor version upgrade maintenance scheduled for April. The rescheduling of the next minor version upgrade maintenance remains undetermined at this time. We commit to providing at least one month's notice prior to the rescheduled maintenance to ensure all users are adequately prepared.
>  
> Notes that if your maintenance has already been completed, whether it was rescheduled to an earlier date or carried out as initially scheduled, and concluded successfully, your services are not affected by this cancellation. Your maintenance is considered successful and will not be affected by the current round of cancellations.

## Engine version changes

All existing engine version server upgrades to 8.0.36 engine version.

To check your engine version, run `SELECT VERSION();` command at the MySQL prompt

## Features

### [Microsoft Defender for Cloud](/azure/defender-for-cloud/defender-for-databases-introduction)

- Introducing Defender for Cloud support to simplify security management with threat protection from anomalous database activities in Azure Database for MySQL Flexible Server instances.

## Improvement

- Expose old_alter_table for 8.0.x.

## Known issues fixes

- Fixed the issue where `GTID RESET` operation's retry interval was excessively long.
- Fixed the issue that data-in HA failover stuck because of system table corrupt
- Fixed the issue that in point-in-time restore that database or table starts with special keywords might be ignored
- Fixed the issue where, if there's replication failure, the system now ignores the replication latency metric instead of displaying a '0' latency value.
- Fixed the issue where under certain circumstances MySQL RP does not correctly get notified of a "private dns zone move operation". The issue will cause the server to be showing incorrect ARM resource ID of the associated private dns zone resource.
