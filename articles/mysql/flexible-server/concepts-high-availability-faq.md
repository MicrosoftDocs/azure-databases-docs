---
title: High availability - FAQ
description: FAQ related to high availability in Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ai-usage: ai-assisted
---

# High availability FAQ in Azure Database for MySQL - Flexible Server

## Frequently asked questions (FAQ)

- **What are the SLAs for same-zone vs zone-redundant HA enabled Flexible server?**

  SLA information for Azure Database for MySQL Flexible Server can be found at [SLA for Azure Database for MySQL](https://azure.microsoft.com/support/legal/sla/mysql/v1_2/).

- **How am I billed for high available (HA) servers?**
Servers enabled with HA have a primary and secondary replica. Secondary replica can be in same zone or zone redundant. You're billed for the provisioned compute and storage for both the primary and secondary replica. For example, if you have a primary with 4 vCores of compute and 512 GB of provisioned storage, your secondary replica will also have 4 vCores and 512 GB of provisioned storage. Your zone redundant HA server will be billed for 8 vCores and 1,024 GB of storage. Depending on your backup storage volume, you might also be billed for backup storage.

- **Can I use the standby replica for read or write operations?** </br>
The standby server isn't available for read or write operations. It's a passive standby to enable fast failover.

- **Will I have data loss when failover happens?**</br>
Logs in ZRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica is activated and binary logs are applied, it takes the role of the primary server. </br>

- **Do I need to take any action after a failover?**</br>
Failovers are fully transparent from the client application. You don't need to take any action. Applications should just use the retry logic for their connections. </br>

- **What happens when I don't choose a specific zone for my standby replica? Can I change the zone later?**</br>
If you don't choose a zone, one will be randomly selected. It will be the one used for the primary server. To change the zone later, you can set **High Availability** to **Disabled** on the **High Availability** pane, and then set it back to **Zone Redundant** and choose a zone.</br>

- **Is replication between the primary and standby replicas synchronous?**</br>
The replication between the primary and the standby is similar to [semisynchronous mode](https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html) in MySQL. When a transaction is committed, it doesn't necessarily commit to the standby. But when the primary is unavailable, the standby does replicate all data changes from the primary to make sure there's no data loss.</br>

- **Is there a failover to the standby replica for all unplanned failures?**</br>
If there's a database crash or node failure, the Flexible Server VM is restarted on the same node. At the same time, an automatic failover is triggered. If the Flexible Server VM restart is successful before the failover finishes, the failover operation will be canceled. The determination of which server to use as the primary replica depends on the process that finishes first.</br>

- **Is there a performance impact when I use HA?**</br>
For zone-redundant HA, while there is no major performance impact for read workloads across availability zones, there might be up to 40 percent drop in write-query latency. The increase in write-latency is due to synchronous replication across Availability zone. The write latency impact is generally twice in zone redundant HA compared to the same zone HA. For same-zone HA, because the primary and the standby replica is in the same zone, the replication latency and consequently the synchronous write latency is lower. In summary, if write-latency is more critical for you compared to availability, you might want to choose same-zone HA but if availability and resiliency of your data is more critical for you at the expense of write-latency drop, you must choose zone-redundant HA. To measure the accurate impact of the latency drop in HA setup, we recommend you to perform performance testing for your workload to take an informed decision.</br>

- **How does maintenance of my HA server happen?**</br>
Planned events like scaling of compute and minor version upgrades happen on the original standby instance first, and followed by triggering a planned failover operation, and then operate on the original primary instance. You can set the [scheduled maintenance window](concepts-maintenance.md) for HA servers as you do for Flexible Servers. The amount of downtime will be the same as the downtime for the Azure Database for MySQL Flexible Server instance when HA is disabled. </br>

- **Can I do a point-in-time restore (PITR) of my HA server?**</br>
You can do a [PITR](./concepts-backup-restore.md#point-in-time-restore) for an HA-enabled Azure Database for MySQL Flexible Server instance to a new Azure Database for MySQL Flexible Server instance that has HA disabled. If the source server was created with zone-redundant HA, you can enable zone-redundant HA or same-zone HA on the restored server later. If the source server was created with same-zone HA, you can enable only same-zone HA on the restored server.</br>

- **Can I enable HA on a server after I create the server?**</br>
Zone-redundant HA must be enabled during server creation. You can enable same-zone HA after server creation, but ensure that the server parameters **enforce_gtid_consistency** and **gtid_mode** are set to **ON** before proceeding.</br>

- **Can I disable HA for a server after I create it?** </br>
You can disable HA on a server after you create it. Billing stops immediately. </br>

- **How can I mitigate downtime?**</br>
You need to be able to mitigate downtime for your application even when you're not using HA. Service downtime, like scheduled patches, minor version upgrades, or customer-initiated operations like scaling of compute can be performed during scheduled maintenance windows. To mitigate application impact for Azure-initiated maintenance tasks, you can schedule them on a day of the week and time that minimizes the impact on the application.</br>

- **Can I use a read replica for an HA-enabled server?**</br>
Yes, read replicas are supported for HA servers.</br>

- **Can I use Data-in Replication for HA servers?**</br>
Support for data-in replication for high availability (HA) enabled server is available only through GTID-based replication.
The stored procedure for replication using GTID is available on all HA-enabled servers by the name `mysql.az_replication_with_gtid`.

- **To reduce downtime, can I fail over to the standby server during server restarts or while scaling up or down?** </br>
Currently, Azure Database for MySQL Flexible Server has utlized Planned Failover to optmize the HA operations including scaling up/down, and planned maintenance to help reduce the downtime.
When such operations started, it would operate on the original standby instance first, followed by triggering a planned failover operation, and then operate on the original primary instance. </br>

- **Can we change the availability mode (Zone-redundant HA/same-zone) of server** </br>
If you create the server with Zone-redundant HA mode enabled then you can change from Zone-redundant HA to same-zone and vice versa. To change the availability mode, you can set **High Availability** to **Disabled** on the **High Availability** pane, and then set it back to **Zone Redundant or same-zone** and choose **High Availability Mode**.</br>

## Related content
- [High Availability](concepts-high-availability.md)
- [business continuity](concepts-business-continuity.md)
- [zone-redundant high availability](concepts-high-availability.md)
- [backup and recovery](concepts-backup-restore.md)
