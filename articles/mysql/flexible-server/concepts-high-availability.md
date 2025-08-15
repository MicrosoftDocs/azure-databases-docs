---
title: Zone-Redundant HA
description: Get a conceptual overview of zone-redundant high availability in Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 08/15/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ai-usage: ai-assisted
---

# High availability in Azure Database for MySQL

Azure Database for MySQL Flexible Server lets you configure high availability with automatic failover. This solution ensures that committed data is never lost because of failures and that the database isn't a single point of failure in your software architecture. When you configure high availability, Flexible Server automatically provisions and manages a standby replica. You pay for the provisioned compute and storage for both the primary and secondary replica. Two high availability architectural models are available:

- **Zone-redundant High Availability (HA)**. This option offers complete isolation and redundancy of infrastructure across multiple availability zones. It provides the highest level of availability, but it requires you to configure application redundancy across zones. Choose zone-redundant HA when you want to achieve the highest level of availability against any infrastructure failure in the availability zone and when latency across the availability zone is acceptable. You can enable it only when you create the server. Zone-redundant HA is available in a [subset of Azure regions](./overview.md#azure-regions) where the region supports multiple [availability zones](/azure/reliability/availability-zones-overview) and [zone-redundant Premium file shares](/azure/storage/common/storage-redundancy#zone-redundant-storage) are available.

- **Same-zone High Availability (HA)**. This option offers infrastructure redundancy with lower network latency because the primary and standby servers are in the same availability zone. It provides high availability without the need to configure application redundancy across zones. Choose same-zone HA when you want to achieve the highest level of availability within a single availability zone with the lowest network latency. Same-zone HA is available in all [Azure regions](./overview.md#azure-regions) where you can use Azure Database for MySQL Flexible Server.

## Zone-redundant High Availability (HA) architecture

When you deploy a server with zone-redundant HA, you create two servers:
- A primary server in one availability zone.
- A standby replica server that has the same configuration as the primary server (compute tier, compute size, storage size, and network configuration) in another availability zone of the same Azure region.

You can choose the availability zone for the primary and the standby replica. Placing the standby database servers and standby applications in the same zone reduces latency. It also helps you prepare for disaster recovery situations and "zone down" scenarios.

:::image type="content" source="media/concepts-high-availability/1-flexible-server-overview-zone-redundant-ha.png" alt-text="Diagram that shows the architecture for zone-redundant high availability." lightbox="media/concepts-high-availability/1-flexible-server-overview-zone-redundant-ha.png":::

The data and log files are hosted in [zone-redundant storage (ZRS)](/azure/storage/common/storage-redundancy#redundancy-in-the-primary-region). The standby server continuously reads and replays the log files from the primary server's storage account, which is protected by storage-level replication.

If a failover occurs:
- The standby replica activates.
- The binary log files of the primary server continue to apply to the standby server to bring it online to the last committed transaction on the primary.

Logs in ZRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica activates and binary logs apply, the current standby replica server takes the role of the primary server. DNS updates so that client connections direct to the new primary when the client reconnects. The failover is fully transparent from the client application and doesn't require any action from you. The HA solution then brings back the old primary server when possible and places it as a standby.

You use the database server name to connect applications to the primary server. Standby replica information isn't exposed for direct access. Commits and writes are acknowledged after the log files are flushed at the primary server's ZRS. Because of the sync replication technology used in ZRS storage, you can expect 5-10 percent increased latency for application writes and commits.

Automatic backups, both snapshots and log backups, are performed on zone-redundant storage from the primary database server.

## Same-zone HA architecture

When you deploy a server with same-zone HA, you create two servers in the same zone:
- A primary server
- A standby replica server that has the same configuration as the primary server (compute tier, compute size, storage size, and network configuration)

The standby server provides infrastructure redundancy with a separate virtual machine (compute). This redundancy reduces failover time and network latency between the application and the database server because of colocation.

:::image type="content" source="media/concepts-high-availability/flexible-server-overview-same-zone-ha.png" alt-text="Diagram that shows the architecture for same-zone high availability." lightbox="media/concepts-high-availability/flexible-server-overview-same-zone-ha.png":::

The data and log files are hosted in [locally redundant storage (LRS)](/azure/storage/common/storage-redundancy#locally-redundant-storage). The standby server continuously reads and replays the log files from the primary server's storage account, which is protected by storage-level replication.

If a failover occurs:
- The standby replica activates.
- The binary log files of the primary server continue to apply to the standby server to bring it online to the last committed transaction on the primary.

Logs in LRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica is activated and binary logs are applied, the current standby replica takes the role of the primary server. DNS is updated to redirect connections to the new primary when the client reconnects. The failover is fully transparent from the client application and doesn't require any action from you. The HA solution then brings back the old primary server when possible and places it as a standby.

Applications use the database server name to connect to the primary server. The solution doesn't expose standby replica information for direct access. Commits and writes are acknowledged after the log files are flushed at the primary server's LRS. Because the primary and the standby replica are in the same zone, there's less replication lag and lower latency between the application server and the database server.

The same-zone setup doesn't provide high availability when dependent infrastructures are down for the specific availability zone. The application experiences downtime until all dependent services are back online for that availability zone.

Automatic backups, both snapshots and log backups, are performed on locally redundant storage from the primary database server.

> [!NOTE]  
> For both zone-redundant and same-zone HA:
> - If a failure occurs, the time needed for the standby replica to take over the role of primary depends on the time it takes to replay the binary log from the primary storage account to the standby. We recommend using primary keys on all tables to reduce failover time. Failover times typically range between 60 and 120 seconds.
> - The standby server isn't available for read or write operations. It's a passive standby to enable fast failover.
> - Always use a fully qualified domain name (FQDN) to connect to your primary server. Avoid using an IP address to connect. If a failover occurs, after the primary and standby server roles are switched, a DNS A record might change. That change prevents the application from connecting to the new primary server if an IP address is used in the connection string.

## Failover process

During the failover process in Azure Database for MySQL, the system automatically switches from the primary server to the standby replica. This switch ensures continuity and minimizes downtime. When the system detects a failure, it promotes the standby replica to become the new primary server. The system applies the binary log files from the original primary server to the standby replica. This process synchronizes the standby replica with the last committed transaction and ensures no data loss. This seamless transition helps maintain high availability and reliability of the database service.

### Planned: Forced failover

Azure Database for MySQL Flexible Server forced failover enables you to manually force a failover. This capability enables you to test your application scenarios' functionality and prepares you for outages.

Forced failover triggers a failover that activates the standby replica to become the primary server with the same database server name by updating the DNS record. The original primary server is restarted and switched to the standby replica. Client connections are disconnected and need to be reconnected to resume their operations.

The overall failover time depends on the current workload and the last checkpoint. In general, it takes between 60 and 120 seconds.

> [!NOTE]  
> An Azure Resource Health event is generated during a planned failover. The event represents the failover time during which the server is unavailable. You can see the triggered events when you select **Resource Health** in the portal. The status represents user-initiated or manual failover as **"Unavailable"** and tagged as **"Planned"**. For example, "A failover operation was triggered by an authorized user (Planned)". If your resource remains in this state for an extended period, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we assist you.

### Unplanned: Automatic failover

Unplanned service downtime can occur because of software bugs or infrastructure faults. These faults include compute, network, or storage failures, or power outages that affect the database's availability. If the database becomes unavailable, replication to the standby replica stops, and the standby replica becomes the primary database. DNS updates, and clients reconnect to the database server and resume their operations.

The overall failover time is usually between 60 and 120 seconds. However, depending on the activity in the primary database server at the time of the failover (such as large transactions and recovery time), the failover might take longer.

> [!NOTE]  
> During an unplanned failover, Azure Resource Health generates an event that represents the failover time when the server is unavailable. You can see the triggered events when you select **Resource Health** in the left pane. Automatic failover shows a status of **"Unavailable"** and is tagged as **"Unplanned"**.
>
> For example: Unavailable: A failover operation was triggered automatically (Unplanned). If your resource stays in this state for a long time, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we assist you.

#### How automatic failover detection works in HA enabled servers

The primary server and the secondary server have two network endpoints:
- Customer Endpoint: Customers connect and run queries on the instance by using this endpoint.
- Management Endpoint: Used internally for service communications to management components and to connect to backend storage.

The health monitor component continuously does the following checks:
- The monitor pings the nodes' Management network Endpoint. If this check fails two times in a row, it triggers an automatic failover operation. This health check addresses scenarios such as a node being unavailable or not responding due to an OS issue or a networking issue between management components and nodes.
- The monitor runs a simple query on the instance. If the queries fail to run, automatic failover is triggered. This health check addresses scenarios such as MySQL daemon crashes, stops, or hangs, and backend storage issues.

> [!NOTE]  
> The health check doesn't monitor any networking issues between the application and the customer networking endpoint (Private/Public access). These issues can occur in the networking path, on the endpoint, or DNS issues on the client side. If you're using private access, make sure the NSG rules for the virtual network don't block communication to the instance customer networking endpoint on port 3306. For public access, make sure that the firewall rules are set and network traffic is allowed on port 3306 (if the network path has any other firewalls). You also need to take care of the DNS resolution from the client application side.

<a id="monitoring-for-high-availability"></a>

## Monitor high availability

You can monitor the server's high availability configuration status by using the **High Availability Status** in the server's *High Availability* pane in the portal.

| **Status** | **Description** |
| --- | --- |
| **NotEnabled** | High availability isn't enabled. |
| **ReplicatingData** | The standby server synchronizes with the primary server during high availability server provisioning or when you enable the high availability option. |
| **FailingOver** | The database server is in the process of failing over from the primary to the standby. |
| **Healthy** | High availability option is enabled. |
| **RemovingStandby** | When the high availability option is disabled, and the deletion process is underway. |

You can also use the following metrics to monitor the health of the high availability server.

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| HA `IO` Status | ha_io_running | State | HA `IO` Status indicates the state of HA replication. The metric value is 1 if the I/O thread is running and 0 if not. |
| HA SQL Status | ha_sql_running | State | HA SQL Status indicates the state of HA replication. The metric value is 1 if the SQL thread is running and 0 if not. |
| HA Replication Lag | replication_lag | Seconds | Replication lag is the number of seconds the standby is behind in replaying the transactions received at the primary server. |

## Limitations

Keep the following considerations in mind when you use high availability:

- You can only configure zone-redundant high availability during server creation.
- The burstable compute tier doesn't support high availability.
- Restarting the primary database server to apply static parameter changes also restarts the standby replica.
- GTID mode is turned on because the HA solution uses GTID. Check whether your workload has [restrictions or limitations on replication with GTIDs](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-restrictions.html).

> [!NOTE]  
> To enable same-zone HA after creating the server, make sure the server parameters `enforce_gtid_consistency` and ["gtid_mode"](./concepts-read-replicas.md#global-transaction-identifier-gtid) are set to `ON` before enabling HA.

> [!NOTE]  
> Storage autogrow is enabled by default for a high availability configured server and can't be disabled.

## Health Checks

When you configure high availability (HA) for Azure Database for MySQL, health checks play a crucial role in maintaining the reliability and performance of your database. These checks continuously monitor the status and health of both the primary and standby replicas, ensuring that any issues are detected promptly. By tracking various metrics such as server responsiveness, replication lag, and resource utilization, health checks help ensure that failover processes can be executed seamlessly, minimizing downtime and preventing data loss. Properly configured health checks are essential for achieving the desired level of availability and resilience in your database setup.

### Monitoring health

You can monitor the health of your HA setup through the Azure portal. Key metrics to observe include:

- **Server responsiveness:** Indicates whether the primary server is reachable.
- **Replication lag:** Measures the delay between the primary and standby replicas, ensuring data consistency.
- **Resource utilization:** Monitors CPU, memory, and storage usage to prevent bottlenecks.

## Frequently asked questions (FAQ)

- **What are the SLAs for same-zone vs. zone-redundant HA-enabled Flexible server?**

  SLA information for Azure Database for MySQL Flexible Server is available at [SLA for Azure Database for MySQL](https://azure.microsoft.com/support/legal/sla/mysql/v1_2/).

- **How am I billed for high available (HA) servers?**

  Servers enabled with HA have a primary and secondary replica. The secondary replica can be in the same zone or a redundant zone. You're billed for the provisioned compute and storage for both the primary and secondary replicas. For example, if you have a primary with 4 vCores of compute and 512 GB of provisioned storage, your secondary replica also has 4 vCores and 512 GB of provisioned storage. Your zone redundant HA server is billed for 8 vCores and 1,024 GB of storage. Depending on your backup storage volume, you might also be billed for backup storage.

- **Can I use the standby replica for read or write operations?**

  The standby server is unavailable for both read and write operations. It's a passive standby to enable fast failover.

- **Will I have data loss when a failover happens?**

  Logs in ZRS are accessible even when the primary server is unavailable. This availability helps ensure there's no loss of data. After the standby replica is activated and binary logs are applied, it takes the role of the primary server.

- **Do I need to take any action after a failover?**

  Failovers are fully transparent from the client application. You don't need to take any action. Applications should just use the retry logic for their connections.

- **What happens when I don't choose a specific zone for my standby replica? Can I change the zone later?**

  If you don't choose a zone, one is randomly selected. It's the one used for the primary server. To change the zone later, set **High Availability** to **Disabled** on the **High Availability** pane, then set it back to **Zone Redundant** and choose a zone.

- **Is replication between the primary and standby replicas synchronous?**

  The replication between the primary and the standby is similar to [semisynchronous mode](https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html) in MySQL. When a transaction is committed, it doesn't necessarily commit to the standby. But when the primary is unavailable, the standby replicates all data changes from the primary to make sure there's no data loss.

- **Is there a failover to the standby replica for all unplanned failures?**

  If there's a database crash or node failure, the Flexible Server VM restarts on the same node. At the same time, an automatic failover is triggered. If the Flexible Server VM restart succeeds before the failover finishes, the failover operation is canceled. The determination of which server to use as the primary replica depends on the process that finishes first.

- **Is there a performance impact when I use HA?**

  For zone-redundant HA, while there's no significant performance impact for read workloads across availability zones, there might be up to a 40 percent drop in write-query latency. The increase in write latency is due to synchronous replication across the Availability zone. The write latency impact is twice in zone redundant HA compared to the same zone HA. For same-zone HA, because the primary and the standby replicas are in the same zone, the replication latency and so the synchronous write latency are lower. In summary, if write-latency is more critical for you compared to availability, you might want to choose same-zone HA. However, if the availability and resiliency of your data are more critical to you, even if it means a write-latency drop, you must choose zone-redundant HA. To measure the accurate impact of the latency drop in HA setup, we recommend that you perform performance testing for your workload to make an informed decision.

- **How does maintenance of my HA server happen?**

  Planned events, such as scaling of compute and minor version upgrades, are performed on the original standby instance first. This process is followed by triggering a planned failover operation and then operating on the original primary Instance. You can set the [scheduled maintenance window](concepts-maintenance.md) for HA servers as you do for Flexible Servers. The amount of downtime is the same as the downtime for the Azure Database for MySQL Flexible Server instance when HA is disabled.

- **Can I do a point-in-time restore (PITR) of my HA server?**

  You can do a [PITR](./concepts-backup-restore.md#point-in-time-restore) for an HA-enabled Azure Database for MySQL Flexible Server instance to a new Azure Database for MySQL Flexible Server instance that has HA disabled. If the source server was created with zone-redundant HA, you can enable zone-redundant HA or same-zone HA on the restored server later. If the source server was created with same-zone HA, you can enable only same-zone HA on the restored server.

- **Can I enable HA on a server after I create the server?**

  Zone-redundant HA must be enabled during server creation. You can enable same-zone HA after server creation, but ensure that the server parameters **enforce_gtid_consistency** and **gtid_mode** are set to `ON` before proceeding.

- **Can I disable HA for a server after I create it?**

  You can disable HA on a server after you create it. Billing stops immediately.

- **How can I mitigate downtime?**

  You need to be able to mitigate downtime for your application even when you're not using HA. Service downtime, like scheduled patches, minor version upgrades, or customer-initiated operations like scaling of compute, can be performed during scheduled maintenance windows. To minimize the impact on the application, you can schedule Azure-initiated maintenance tasks on a day and time that minimizes disruption.

- **Can I use a read replica for an HA-enabled server?**

  Yes, Azure Database for MySQL supports read replicas for high availability servers.

- **Can I use Data-in Replication for HA servers?**

Azure Database for MySQL supports data-in replication for high-availability (HA) enabled servers only through GTID-based replication. All HA-enabled servers provide the stored procedure for replication by the name `mysql.az_replication_with_gtid`.

- **To reduce downtime, can I fail over to the standby server during server restarts or while scaling up or down?**

  Currently, Azure Database for MySQL Flexible Server uses planned failover to optimize the HA operations, including scaling up or down, and planned maintenance to help reduce downtime. When you start such operations, the service first operates on the original standby instance, then triggers a planned failover operation, and finally operates on the original primary instance.

- **Can we change the availability mode (Zone-redundant HA/same-zone) of the server**

  If you create the server with Zone-redundant HA mode enabled, you can change from Zone-redundant HA to same-zone and vice versa. To change the availability mode, set **High Availability** to **Disabled** on the **High Availability** pane, then set it back to **Zone Redundant or same-zone** and choose **High Availability Mode**.

## Related content

- [business continuity](concepts-business-continuity.md)
- [zone-redundant high availability](concepts-high-availability.md)
- [backup and recovery](concepts-backup-restore.md)
