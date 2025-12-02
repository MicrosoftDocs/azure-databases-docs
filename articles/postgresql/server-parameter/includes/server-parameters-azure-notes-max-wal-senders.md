---
title: max_wal_senders server parameter
description: max_wal_senders server parameter for Azure Database for PostgreSQL flexible server.
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.date: 10/14/2024
author: nachoalonsoportillo
ms.author: ialonso
zone_pivot_groups: postgresql-server-version
---
#### Azure-specific notes
The default value for the `max_wal_senders` server parameter set when you provision the instance of Azure Database for PostgreSQL flexible server must never be decreased below `2 (if HA is enabled) + number of read replicas provisioned + slots_used_in_logical_replication`.

When considering the need to increase `max_wal_senders` to a much higher value to be able to cope with the logical replication of a substantial number of tables, have the following important points in mind:

- Logically replicating a large number of tables doesn't necessarily need a large number of WAL senders.
- The only reason why you need separate WAL sender per-table or group of tables is if you need separate subscriptions for each of those tables or groups of.
- Whatever number of WAL senders are being utilized for physical and logical replication, they all become active at once, whenever any backend writes something to the write-ahead log. When that happens, the WAL senders that are assigned to do logical replication all wake up to:
    1. Decode all new records in the WAL, 
    1. Filter out log records they're not interested in,
    1. Replicate the data that's relevant to each of them. 
- WAL senders are similar to connections in the sense that, if they are idle, it doesn't matter how many there are. However, if they are active, they'll just compete for the same resources and the performance could end up being terribly bad. This is especially true for senders with logical replication, because the logical decoding is rather CPU expensive. Each worker has to decode the entire WAL, even if it only replicates the operations affecting a single table, and that represents a tiny percentage of all the data in the write-ahead log. For physical replication it's not that important, because the WAL senders don't consume CPU so intensively, and they tend to be bounded by network bandwidth first.
- Therefore, in general, it's better to not have many more WAL senders than vCores.
- It's a good practice to add room for a few extra WAL senders to accommodate future growth or temporary spikes in replication connections. The following two examples might help illustrate it better.
    - For a server with 8 vCores, HA disabled, 2 read replicas, and 3 logical replication slots, you may want to configure `max_wal_senders` as the sum of physical slots for HA (0) + physical slots for read replicas (2) + logical slots(3) + some extra for future growth, considering available vCores (1) = **6**.
    - For a server with 16 vCores, HA enabled, 4 read replicas, and 5 logical replication slots, you may want to configure `max_wal_senders` as the sum of physical slots for HA (2) + physical slots for read replicas (4) + logical slots(5) + some extra for future growth, considering available vCores (2) = **13**.
    -  If you enable high availability, you need a minimum of 4 `max_wal_senders` for high availability to function properly. For a server with high availability enabled, plus 5 read replicas, and 12 logical replication slots, you might want to configure `max_wal_senders` to 21. This is because each read replica and each logical replication slot requires one `max_wal_senders`. Therefore, it requires a total of 1 (slot) * 5 (read replicas) + 12 (logical replication slots) + 4 (for high availability to function properly) = 21.
- If you still consider that the maximum value allowed for this parameter is too low for your needs, [contact us](../configure-maintain/overview.md#feedback-and-support), describe your scenario in detail and explain what do you consider that would be the minimum acceptable value you would need for your scenario to perform properly.
