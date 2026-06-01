---
title: Max_replication_slots Parameter
description: max_replication_slots Parameter for Azure HorizonDB.
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: include
---

#### Azure-specific notes

The default value for `max_replication_slots` parameter is 10. If you enable high availability, you need a minimum of 4 `max_replication_slots` for high availability to function properly.

For a server with high availability enabled, plus 5 read replicas, and 12 logical replication slots, you might want to configure `max_replication_slots` to 21. This is because each read replica and each logical replication slot requires one `max_replication_slot`. Therefore, it requires a total of 1 (slot) * 5 (read replicas) + 12 (logical replication slots) + 4 (for high availability to function properly) = 21.
