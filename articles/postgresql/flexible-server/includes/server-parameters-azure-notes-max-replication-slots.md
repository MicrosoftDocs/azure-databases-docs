---
title: max_replication_slots server parameter
description: max_replication_slots server parameter for Azure Database for PostgreSQL flexible server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/14/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes

The default value for `max_replication_slots` parameter is 10, if you have enabled HA you will need a minimum of 4 `max_replication_slots` for HA to function properly. For a HA setup with 5 read replicas and 12 logical replication slots you may want to configure `max_replication_slots` to 21 this is because each read replica and logical replication slot requires one `max_replication_slot`, so total of 5 * 1 (one for each read replica) + 12 (one for each logical replication slot) + 4 (for HA to function properly) = 21.
