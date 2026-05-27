---
title: Frequently asked questions (FAQs)
description: Frequently asked questions about major version upgrades
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 05/26/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: how-to
ai-usage: ai-assisted
---

# Frequently asked questions (FAQs)

- Q: **Can I upgrade directly from MySQL 5.7 to 8.4 (or skip major versions)?**

  A. Cross-major version upgrades (for example, upgrading directly from MySQL 5.7 to 8.4) aren't supported. You must upgrade from 5.7 to 8.0 and then from 8.0 to 8.4. If new MySQL major versions are released in the future, direct upgrades skipping major versions aren't supported. Each major version upgrade must be performed sequentially.

- Q: **Will this cause downtime of the server, and if so, how long?**

  A. To minimize downtime during upgrades, follow the steps in Recommended major version upgrade procedure across major versions. The server is unavailable during the upgrade process, so perform this operation during your planned maintenance window. The estimated downtime depends on the database size, storage size provisioned (IOPs provisioned), and the number of tables on the database. The upgrade time is directly proportional to the number of tables on the server. To estimate the downtime for your server environment, first perform an upgrade on a restored copy of the server.

- Q: **I'm using an HA server. Can I expect a near zero downtime experience for a major version upgrade, similar to routine maintenance?**

  A. No. Major version upgrades differ significantly from routine maintenance. The replication between HA primary and standby servers across major versions isn't stable, which prevents Azure Database for MySQL from offering a near zero downtime experience during such upgrades.

- Q: **What happens to my backups after the upgrade?**

  A. When you restore backups (automated or on-demand) taken before a major version upgrade, you restore to a server with the previous version. When you restore backups (automated or on-demand) taken after a major version upgrade, you restore to the server with the upgraded version. Take an on-demand backup before performing the major version upgrade to enable an easy rollback.

## Known issues and limitations

### Microsoft Entra ID authentication blocked on replica

If you configure both a primary server and its replica with Microsoft Entra authentication, and you perform a major version upgrade on the replica (from 5.7 to 8.0, or from 8.0 to 8.4), any subsequent change to the Microsoft Entra authentication configuration on the primary server can cause a problem on the upgraded replica. Specifically, the replica's authentication method resets from "MySQL and Microsoft Entra authentication" to "MySQL authentication only," which blocks Entra ID authentication on the replica.

#### Resolution

To avoid this problem, don't modify the Microsoft Entra authentication configuration while the primary and replica servers are running on different MySQL versions. Only change Entra ID authentication settings after every server in the replication hierarchy is upgraded to the same version.

If you already encountered this problem, use the following steps to recover:

1. Upgrade the primary server to version 8.0 (or 8.4) and configure the required Microsoft Entra admin user.
1. Create a new replica on version 8.0 (or 8.4).
1. Decommission the old replica that has broken replication.
1. Switch your workload to use the new replica.

### Slowness or high CPU usage in 8.0 compared to 5.7

Depending on the workload, you might observe slowness or high CPU usage in version 8.0 compared to 5.7. Upgrade a read replica or restore and upgrade to Azure Database for MySQL Flexible Server 8.0. Use the replica to test and tune production load and queries before upgrading the primary.

If you observe slowness with queries such as update, insert, or delete, enabling **Accelerated Logs** on your server under **Settings** > **Compute + Storage** in the side pane of your server's portal page might help.

### Silent data inconsistency when inserting timestamp literals with fractional seconds and timezone offsets after upgrading from 5.7 to 8.0 (and 8.4)

In MySQL 8.0, timestamp literals that include both fractional seconds and a timezone offset (for example, `'2025-01-01 12:00:00.123+00:00'`) can be silently converted to incorrect values during `INSERT` or `UPDATE` operations. The incorrect value is stored without any error or warning, which can lead to data inconsistency that's difficult to detect after the fact. Customers upgrading from MySQL 5.7 to 8.0 (and 8.4) might encounter this issue if their applications insert datetime values in this format.

This problem is a known MySQL community bug. For more information, see [MySQL Bug #118011](https://bugs.mysql.com/bug.php?id=118011).

#### Resolution

Until the upstream fix is available, take the following precautions before and after the upgrade:

- Audit your application code for timestamp literals that combine fractional seconds with timezone offsets, and normalize them to UTC (or a single timezone) without an inline offset before insertion.
- Set the session or server `time_zone` explicitly, and write datetime values without an inline offset so the server applies the configured timezone consistently.
- Validate a representative sample of newly inserted rows after the upgrade to confirm that stored values match the expected values.

### Performance regression for IN() queries on indexed string columns after upgrading to 8.4

In MySQL 8.4, a query that uses an `IN()` predicate on an indexed nonbinary string column (for example, `VARCHAR` with a `utf8mb4` or `utf8mb3` nonbinary collation such as `utf8mb4_0900_ai_ci`) can deteriorate to a full table or index scan when at least one value in the `IN()` list is longer than the column's defined length, or longer than a prefix index's defined length. Queries that previously used efficient index range scans on the same data in MySQL 5.7 or 8.0 might experience performance degradation after upgrading to 8.4.

This problem is a known MySQL community bug. For more information, see [MySQL Bug #118009](https://bugs.mysql.com/bug.php?id=118009).

#### Resolution

Until the fix is available on Azure Database for MySQL Flexible Server, use one or more of the following mitigations:

- Audit application queries that use `IN()` on indexed string columns, and filter or truncate values on the application side so that none of the values exceed the column's defined length (or the prefix index length).
- For affected queries, split the `IN()` list into multiple shorter `IN()` lists or `OR` conditions that exclude oversized values, so the optimizer can continue to use index range scans.
- Use binary collations (for example, `utf8mb4_bin`) or the `latin1` character set for affected columns, because these collations aren't affected by this regression. Evaluate the change against your application's sorting and comparison requirements before adopting it.
- Review query plans by using `EXPLAIN` after the upgrade to identify queries that have switched from `range` to `ALL` or `index` access, and prioritize them for mitigation.

### Slowness or high CPU usage for SELECT queries with large IN() lists after upgrading to 8.0 or 8.4

After upgrading to MySQL 8.0 or 8.4, `SELECT` queries that use an `IN()` predicate with a large set of values (for example, several thousand or more values in a single `IN()` list) might exhibit significantly higher query latency and CPU usage compared to the same workload on MySQL 5.7. The optimizer's handling of large `IN()` lists is more expensive in 8.0 and 8.4, and the cost grows with the number of values in the list.

#### Resolution

- Reduce the number of values passed in the `IN()` list. Where possible, refactor the application to send a smaller, more selective set of values per query.
- For workloads that need to filter against a large set of values, load the values into a temporary or staging table and use a `JOIN` against that table instead of a single large `IN()` list.
- Batch the query into multiple smaller queries with shorter `IN()` lists and combine the results in the application layer.
- Test the refactored queries on a read replica or restored copy of the server before applying changes to the primary.

## Related content

- [Major version upgrade in Azure Database for MySQL](how-to-upgrade.md)
