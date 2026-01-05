---
title: Zone-Redundant High-Availability (HA)
description: Get a conceptual overview of zone-redundant high-availability in Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 08/15/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ai-usage: ai-assisted
---

# High-availability in Azure Database for MySQL

Azure Database for MySQL Flexible Server lets you configure high-availability with automatic failover. This solution ensures that failures never cause loss of committed data and that the database isn't a single point of failure in your software architecture. When you configure high-availability, Flexible Server automatically provisions and manages a standby replica. You pay for the provisioned compute and storage for both the primary and secondary replicas. Two high-availability architectural models are available:

- **Zone-redundant high-availability**. This option provides complete isolation and redundancy of infrastructure across multiple availability zones. It offers the highest level of availability, but it requires you to configure application redundancy across zones. Choose zone-redundant HA when you want to protect against any infrastructure failure in the availability zone and when latency across the availability zone is acceptable. You can enable zone-redundant HA only when you create the server. Zone-redundant HA is available in a [subset of Azure regions](./overview.md#azure-regions) where the region supports multiple [availability zones](/azure/reliability/availability-zones-overview) and [zone-redundant Premium file shares](/azure/storage/common/storage-redundancy#zone-redundant-storage) are available.

- **Local-redundant high-availability**. This option provides infrastructure redundancy with lower network latency because the primary and standby servers are in the same availability zone. It offers high-availability without the need to configure application redundancy across zones. Choose Local-redundant HA when you want to achieve the highest level of availability within a single availability zone with the lowest network latency. Local-redundant HA is available in all [Azure regions](./overview.md#azure-regions) where you can use Azure Database for MySQL Flexible Server.

## Zone-redundant high-availability (HA) architecture

When you deploy a server with zone-redundant high-availability, Azure creates two servers:

- A primary server in one availability zone.
- A standby replica server in another availability zone of the same Azure region. The standby replica server has the same configuration as the primary server, including the compute tier, compute size, storage size, and network configuration.

You can choose the availability zone for both the primary server and the standby replica. Placing the standby database servers and standby applications in the same zone reduces latency. It also helps you prepare for disaster recovery situations and "zone down" scenarios.

:::image type="content" source="media/concepts-high-availability/1-flexible-server-overview-zone-redundant-ha.png" alt-text="Diagram that shows the architecture for zone-redundant high-availability." lightbox="media/concepts-high-availability/1-flexible-server-overview-zone-redundant-ha.png":::

The data and log files are hosted in [zone-redundant storage (ZRS)](/azure/storage/common/storage-redundancy#redundancy-in-the-primary-region). The standby server continuously reads and replays the log files from the primary server's storage account, which storage-level replication protects.

If a failover occurs:

- The standby replica activates.
- The binary log files of the primary server continue to apply to the standby server to bring it online to the last committed transaction on the primary server.

Logs in ZRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica activates and binary logs are applied, the current standby replica server takes the role of the primary server. DNS updates so that client connections are direct to the new primary when the client reconnects. The failover is fully transparent from the client application and doesn't require any action from you. The HA solution then brings back the old primary server when possible and places it as a standby.

You use the database server name to connect applications to the primary server. The solution doesn't expose standby replica information for direct access. Commits and writes are acknowledged after the log files are flushed at the primary server's ZRS. Because of the sync replication technology used in ZRS storage, you can expect 5-10 percent increased latency for application writes and commits.

Automatic backups, both snapshots and log backups, are performed on zone-redundant storage from the primary database server.

## Local-redundant high-availability (HA) architecture

When you deploy a server with Local-redundant HA, you create two servers in the same zone:

- A primary server
- A standby replica server that has the same configuration as the primary server (compute tier, compute size, storage size, and network configuration)

The standby server provides infrastructure redundancy with a separate virtual machine (compute). This redundancy reduces failover time and network latency between the application and the database server because of colocation.

:::image type="content" source="media/concepts-high-availability/flexible-server-overview-same-zone-ha.png" alt-text="Diagram that shows the architecture for Local-redundant high-availability." lightbox="media/concepts-high-availability/flexible-server-overview-same-zone-ha.png":::

The data and log files are hosted in [locally redundant storage (LRS)](/azure/storage/common/storage-redundancy#locally-redundant-storage). The standby server continuously reads and replays the log files from the primary server's storage account, which is protected by storage-level replication.

If a failover occurs:

- The standby replica activates.
- The binary log files of the primary server continue to apply to the standby server to bring it online to the last committed transaction on the primary server.

Logs in LRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica is activated and binary logs are applied, the current standby replica takes the role of the primary server. DNS is updated to redirect connections to the new primary when the client reconnects. The failover is fully transparent from the client application and doesn't require any action from you. The HA solution then brings back the old primary server when possible and places it as a standby.

The database server name connects applications to the primary server. Standby replica information isn't exposed for direct access. Commits and writes are acknowledged after the log files are flushed at the primary server's LRS. Because the primary and the standby replica are in the same zone, there's less replication lag and lower latency between the application server and the database server. The Local-redundant setup doesn't provide high-availability when dependent infrastructures are down for the specific availability zone. There's downtime until all dependent services are back online for that availability zone.

Automatic backups, both snapshots and log backups, are performed on locally redundant storage from the primary database server.

> [!NOTE]  
> For both Zone-redundant and Local-redundant HA:
> - If a failure occurs, the time needed for the standby replica to take over the role of primary depends on the time it takes to replay the binary log from the primary storage account to the standby. To reduce failover time, use primary keys on all tables. Failover times typically take between 60 and 120 seconds.
> - The standby server isn't available for read or write operations. It's a passive standby to enable fast failover.
> - Always use a fully qualified domain name (FQDN) to connect to your primary server. Avoid using an IP address to connect. If a failover occurs, after the primary and standby server roles are switched, a DNS A record might change. That change prevents the application from connecting to the new primary server if an IP address is used in the connection string.

## Failover process

During the failover process in Azure Database for MySQL, the system automatically switches from the primary server to the standby replica. This switch ensures continuity and minimizes downtime. When the system detects a failure, it promotes the standby replica to become the new primary server. The system applies the binary log files from the original primary server to the standby replica. This process synchronizes the standby replica with the last committed transaction and ensures no data loss. This seamless transition helps maintain high-availability and reliability of the database service.

> [!NOTE]  
> To reduce failover time dependency on DNS caching, starting October 2025, all new HA servers created with public access or private link will adopt the new architecture featuring a dedicated SLB for each HA server. By managing the MySQL data traffic path, SLB eliminates the need for DNS changes during failover and significantly improves failover performance. It redirects traffic to the current primary instance during failover using load-balancing rules.
> Existing servers with public access or private link will be migrated gradually to minimize impact. Customers who prefer early migration can disable and re-enable HA.
> This feature is not supported for servers using private access with VNet integration.

### Planned: Forced failover

Azure Database for MySQL Flexible Server forced failover enables you to manually force a failover. This capability allows you to test the functionality with your application scenarios and helps you prepare for outages.

Forced failover triggers a failover that activates the standby replica to become the primary server with the same database server name by updating the DNS record. The original primary server restarts and switches to the standby replica. Client connections disconnect and need to reconnect to resume their operations.

The overall failover time depends on the current workload and the last checkpoint. In general, it takes between 60 and 120 seconds.

> [!NOTE]  
> An Azure Resource Health event is generated during a planned failover. The event represents the failover time during which the server is unavailable. You can see the triggered events when selected on **Resource Health** in the left pane. The status represents user-initiated or manual failover as **"Unavailable"** and tagged as **"Planned"**. Example - "A failover operation was triggered by an authorized user (Planned)". If your resource remains in this state for an extended period, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we assist you.

### Unplanned: Automatic failover

Unplanned service downtime can occur due to software bugs or infrastructure faults, such as compute, network, or storage failures. Power outages can also affect the availability of the database. If the database becomes unavailable, replication to the standby replica stops, and the standby replica becomes the primary database. DNS updates occur, and clients reconnect to the database server, resuming their operations.

The overall failover time is usually between 60 and 120 seconds. However, depending on the activity in the primary database server at the time of the failover (such as large transactions and recovery time), the failover might take longer.

> [!NOTE]  
> An Azure Resource Health event is generated during an unplanned failover. The event represents the failover time when the server is unavailable. You can see the triggered events when you select **Resource Health** in the left pane. Automatic failover shows a status of **"Unavailable"** and is tagged as **"Unplanned"**.
>
> For example, Unavailable: A failover operation was triggered automatically (Unplanned). If your resource stays in this state for a long time, open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we help you.

#### How automatic failover detection works in HA enabled servers

The primary server and the secondary server each have two network endpoints:
- Customer Endpoint: Customers connect and run queries on the instance by using this endpoint.
- Management Endpoint: Used internally for service communications to management components and to connect to backend storage.

The health monitor component continuously does the following checks:
- The monitor pings the node's Management network Endpoint. If this check fails two times in a row, it triggers an automatic failover operation. This health check addresses scenarios such as node unavailability or nonresponsiveness due to OS issues, networking issues between management components and nodes, and similar issues.
- The monitor runs a simple query on the instance. If the queries fail to run, automatic failover triggers. This health check addresses scenarios such as MySQL daemon crashes, stops, or hangs, and backend storage issues and similar problems.

> [!NOTE]  
> The health check doesn't monitor networking issues between the application and the customer networking endpoint (Private/Public access). These issues can occur in the networking path, on the endpoint, or in DNS issues on the client side. If you use private access, make sure that the NSG rules for the virtual network don't block communication to the instance customer networking endpoint on port 3306. For public access, make sure that the firewall rules are set and network traffic is allowed on port 3306 (if the network path has any other firewalls). You also need to take care of DNS resolution from the client application side.

<a id="monitoring-for-high-availability"></a>

## Monitor high-availability

To check the server's high-availability configuration status, use the **high-availability Status** in the server's *high-availability* pane in the portal.

| **Status** | **Description** |
| --- | --- |
| **NotEnabled** | high-availability isn't enabled. |
| **ReplicatingData** | Standby server synchronizes with the primary server during high-availability server provisioning or when you enable the high-availability option. |
| **FailingOver** | The database server is failing over from the primary to the standby. |
| **Healthy** | high-availability option is enabled. |
| **RemovingStandby** | The deletion process is underway when you disable the high-availability option. |

To monitor the health of the high-availability server, use the following metrics.

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| HA `IO` Status | ha_io_running | State | HA `IO` Status shows the state of HA replication. The metric value is 1 if the I/O thread is running and 0 if not. |
| HA SQL Status | ha_sql_running | State | HA SQL Status shows the state of HA replication. The metric value is 1 if the SQL thread is running and 0 if not. |
| HA Replication Lag | replication_lag | Seconds | Replication lag is the number of seconds the standby is behind in replaying the transactions received at the primary server. |

## Limitations

Keep the following considerations in mind when you use high-availability:
- You can configure zone-redundant high-availability only during server creation.

- The burstable compute tier doesn't support high-availability.
- Restarting the primary database server to apply static parameter changes also restarts the standby replica.
- The solution turns on GTID mode because it uses GTID. Check whether your workload has [restrictions or limitations on replication with GTIDs](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-restrictions.html).

> [!NOTE]  
> Storage autogrow is enabled by default for a high-availability configured server and can't be disabled.

## Known Issues

Azure Database for MySQL Flexible Server uses native MySQL replication at the backend. A known issue has been identified in the MySQL Community Edition 8.0 and greater that can break replication when performing a multi‑table DELETE operation that relies on foreign key constraints with ON DELETE CASCADE. This issue is tracked as [MySQL Bug 102586](https://bugs.mysql.com/bug.php?id=102586). As a result, when High Availability is enabled on Azure Database for MySQL Flexible Server, we recommend that applications avoid using cascaded deletes with foreign keys, as this can lead to replication failures and may impact the availability of the server.


## Health checks

When you configure high-availability (HA) for Azure Database for MySQL, health checks play a crucial role in maintaining the reliability and performance of your database. These checks continuously monitor the status and health of both the primary and standby replicas, ensuring that they detect any issues promptly. By tracking various metrics such as server responsiveness, replication lag, and resource utilization, health checks help ensure that failover processes can be executed seamlessly, minimizing downtime and preventing data loss. Properly configured health checks are essential for achieving the desired level of availability and resilience in your database setup.

### Monitoring health

You can monitor the health of your HA setup through the Azure portal. Key metrics to observe include:

- **Server responsiveness:** Indicates whether the primary server is reachable.
- **Replication lag:** Measures the delay between the primary and standby replicas, ensuring data consistency.
- **Resource utilization:** Monitors CPU, memory, and storage usage to prevent bottlenecks.

## Related content

- [high-availability](concepts-high-availability-faq.md)
- [Business continuity](concepts-business-continuity.md)
- [Zone-redundant high-availability](concepts-high-availability.md)
- [Backup and recovery](concepts-backup-restore.md)
