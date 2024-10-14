---
title: max_wal_senders server parameter
description: max_wal_senders server parameter for Azure Database for PostgreSQL - Flexible Server.
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
- Whatever number of WAL senders are being utilized for physical and logical replication, they all become active at once, whenever any backend writes something to the write-ahead log. When that happens, the WAL senders that are assigned to do logical replication, they all wake up to:
    1. Decode all new records in the WAL, 
    1. Filter out log records they're not interested in,
    1. Replicate the data that's relevant to each of them. 
- WAL senders are similar to connections in the sense that, if they are idle, it doesn't matter how many there are. However, if they are active, they'll just compete for the same resources and the performance could end up being terribly bad. This is especially true for senders with logical replication, because the logical decoding is rather CPU expensive. Each worker has to decode the entire WAL, even if it only replicates the operations affecting a single table, and that represents a tiny percentage of all the data in the write-ahead log. For physical replication it's not that important, because the WAL senders don't consume CPU so intensively, and they tend to be bounded by network bandwidth first.
- Therefore, in general, it's better to not have more WAL senders than vCores.
- If you still consider that the maximum value allowed for this parameter is too low for your needs, please [contact us](../overview.md#contacts), describe your scenario in detail and explain what would be the minimum acceptable value you would need for your scenario to work properly.