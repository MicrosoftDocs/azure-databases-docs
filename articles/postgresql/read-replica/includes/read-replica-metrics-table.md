---
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 2/4/2025
ms.service: azure-database-postgresql
ms.topic: include

---

You can use enhanced metrics for monitoring and alerting on read replication.

#### Enabling enhanced metrics

- Most of these new metrics are *disabled* by default. There are a few exceptions though, which are enabled by default. Rightmost column in the following tables indicates whether each metric is enabled by default or not.
- To enable those metrics which are not enabled by default, set the server parameter `metrics.collector_database_activity` to `ON`. This parameter is dynamic and doesn't require an instance restart.

##### Logical replication

|Display name|Metric ID|Unit|Description|Dimension|Default enabled|
|---|---|---|---|---|---|
|**Max Logical Replication Lag** |`logical_replication_delay_in_bytes`|Bytes|Maximum lag across all logical replication slots.|Doesn't apply|Yes |

##### Replication

|Display name|Metric ID|Unit|Description|Dimension|Default enabled|
|---|---|---|---|---|---|
|**Max Physical Replication Lag** |`physical_replication_delay_in_bytes`|Bytes|Maximum lag across all asynchronous physical replication slots.|Doesn't apply|Yes |
|**Read Replica Lag** |`physical_replication_delay_in_seconds`|Seconds|Read replica lag in seconds. |Doesn't apply|Yes |