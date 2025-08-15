---
title: Zone-Redundant HA
description: Get a conceptual overview of zone-redundant high availability in Azure Database for MySQL - Flexible Server.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 07/21/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
ai-usage: ai-assisted
---

# High availability concepts in Azure Database for MySQL - Flexible Server

Azure Database for MySQL Flexible Server allows configuring high availability with automatic failover. The high availability solution is designed to ensure that committed data is never lost because of failures and that the database won't be a single point of failure in your software architecture. When high availability is configured, Flexible Server automatically provisions and manages a standby replica. You're billed for the provisioned compute and storage for both the primary and secondary replica. There are two high availability architectural models:

- **Zone-redundant HA**. This option is preferred for complete isolation and redundancy of infrastructure across multiple availability zones. It provides the highest level of availability, but it requires you to configure application redundancy across zones. Zone-redundant HA is preferred when you want to achieve the highest level of availability against any infrastructure failure in the availability zone and when latency across the availability zone is acceptable. It can be enabled only when the server is created. Zone-redundant HA is available in a [subset of Azure regions](./overview.md#azure-regions) where the region supports multiple [availability zones](/azure/reliability/availability-zones-overview) and [zone-redundant Premium file shares](/azure/storage/common/storage-redundancy#zone-redundant-storage) are available.

- **Same-zone HA**. This option is preferred for infrastructure redundancy with lower network latency because the primary and standby servers will be in the same availability zone. It provides high availability without the need to configure application redundancy across zones. Same-zone HA is preferred when you want to achieve the highest level of availability within a single availability zone with the lowest network latency. Same-zone HA is available in all [Azure regions](./overview.md#azure-regions) where you can use Azure Database for MySQL Flexible Server.

## Zone-redundant HA architecture

When you deploy a server with zone-redundant HA, two servers will be created:
- A primary server in one availability zone.
- A standby replica server that has the same configuration as the primary server (compute tier, compute size, storage size, and network configuration) in another availability zone of the same Azure region.

You can choose the availability zone for the primary and the standby replica. Placing the standby database servers and standby applications in the same zone reduces latency. It also allows you to better prepare for disaster recovery situations and "zone down" scenarios.

:::image type="content" source="media/concepts-high-availability/1-flexible-server-overview-zone-redundant-ha.png" alt-text="Diagram that shows the architecture for zone-redundant high availability." lightbox="media/concepts-high-availability/1-flexible-server-overview-zone-redundant-ha.png":::

The data and log files are hosted in [zone-redundant storage (ZRS)](/azure/storage/common/storage-redundancy#redundancy-in-the-primary-region). The standby server reads and replay the log files continuously from the primary server's storage account, which is protected by storage-level replication.

If there's a failover:
- The standby replica is activated.
- The binary log files of the primary server continue to apply to the standby server to bring it online to the last committed transaction on the primary.

Logs in ZRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica is activated and binary logs are applied, the current standby replica server takes the role of the primary server. DNS is updated so that client connections are directed to the new primary when the client reconnects. The failover is fully transparent from the client application and doesn't require any action from you. The HA solution then brings back the old primary server when possible and places it as a standby.

The database server name is used to connect applications to the primary server. Standby replica information isn't exposed for direct access. Commits and writes are acknowledged after the log files are flushed at the primary server's ZRS. Because of the sync replication technology used in ZRS storage, you can expect 5-10 percent increased latency for application writes and commits.

Automatic backups, both snapshots and log backups, are performed on zone-redundant storage from the primary database server.

## Same-zone HA architecture

When you deploy a server with same-zone HA, two servers will be created in the same zone:
- A primary server
- A standby replica server that has the same configuration as the primary server (compute tier, compute size, storage size, and network configuration)

The standby server offers infrastructure redundancy with a separate virtual machine (compute). This redundancy reduces failover time and network latency between the application and the database server because of colocation.

:::image type="content" source="media/concepts-high-availability/flexible-server-overview-same-zone-ha.png" alt-text="Diagram that shows the architecture for same-zone high availability." lightbox="media/concepts-high-availability/flexible-server-overview-same-zone-ha.png":::

The data and log files are hosted in [locally redundant storage (LRS)](/azure/storage/common/storage-redundancy#locally-redundant-storage). The standby server reads and replay the log files continuously from the primary server's storage account, which is protected by storage-level replication.

If there's a failover:
- The standby replica is activated.
- The binary log files of the primary server continue to apply to the standby server to bring it online to the last committed transaction on the primary.

Logs in LRS are accessible even when the primary server is unavailable. This availability helps to ensure there's no loss of data. After the standby replica is activated and binary logs are applied, the current standby replica takes the role of the primary server. DNS is updated to redirect connections to the new primary when the client reconnects. The failover is fully transparent from the client application and doesn't require any action from you. The HA solution then brings back the old primary server when possible and places it as a standby.

The database server name is used to connect applications to the primary server. Standby replica information isn't exposed for direct access. Commits and writes are acknowledged after the log files are flushed at the primary server's LRS. Because the primary and the standby replica are in the same zone, there's less replication lag and lower latency between the application server and the database server. The same-zone setup doesn't provide high availability when dependent infrastructures are down for the specific availability zone. There will be downtime until all dependent services are back online for that availability zone.

Automatic backups, both snapshots and log backups, are performed on locally redundant storage from the primary database server.

> [!NOTE]  
> For both zone-redundant and same-zone HA:
> - If there's a failure, the time needed for the standby replica to take over the role of primary depends on the time it takes to replay the binary log from the primary storage account to the standby. So we recommend that you use primary keys on all tables to reduce failover time. Failover times are typically between 60 and 120 seconds.
> - The standby server isn't available for read or write operations. It's a passive standby to enable fast failover.
> - Always use a fully qualified domain name (FQDN) to connect to your primary server. Avoid using an IP address to connect. If there's a failover, after the primary and standby server roles are switched, a DNS A record might change. That change would prevent the application from connecting to the new primary server if an IP address is used in the connection string.

## Failover process

During the failover process in Azure Database for MySQL, the system automatically switches from the primary server to the standby replica to ensure continuity and minimize downtime. When a failure is detected, the standby replica is promoted to become the new primary server. The binary log files from the original primary server are applied to the standby replica to synchronize it with the last committed transaction, ensuring no data loss. This seamless transition helps maintain high availability and reliability of the database service.

### Planned: Forced failover

Azure Database for MySQL Flexible Server forced failover enables you to manually force a failover. This capability allows you to test the functionality with your application scenarios and helps make you ready for outages.

Forced failover triggers a failover that activates the standby replica to become the primary server with the same database server name by updating the DNS record. The original primary server is restarted and switched to the standby replica. Client connections are disconnected and need to be reconnected to resume their operations.

The overall failover time depends on the current workload and the last checkpoint. In general, it's expected to take between 60 and 120 seconds.

> [!NOTE]  
> Azure Resource Health event is generated in the event of planned failover, representing the failover time during which server was unavailable. The triggered events can be seen when selected on "Resource Health" in the left pane. User initiated/ Manual failover is represented by status as **"Unavailable"** and tagged as **"Planned"**. Example - "A failover operation was triggered by an authorized user (Planned)". If your resource remains in this state for an extended period of time, please open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we will assist you.

### Unplanned: Automatic failover

Unplanned service downtime can be caused by software bugs or infrastructure faults like compute, network, or storage failures, or power outages that affect the availability of the database. If the database becomes unavailable, replication to the standby replica is severed and the standby replica is activated as the primary database. DNS is updated, and clients reconnect to the database server and resume their operations.

The overall failover time is expected to be between 60 and 120 seconds. But, depending on the activity in the primary database server at the time of the failover (like large transactions and recovery time), the failover might take longer.

> [!NOTE]  
> Azure Resource Health event is generated in the event of unplanned failover, representing the failover time during which server was unavailable. The triggered events can be seen when selected on "Resource Health" in the left pane. Automatic failover is represented by status as **"Unavailable"** and tagged as **"Unplanned"**. Example - "Unavailable : A failover operation was triggered automatically (Unplanned)". If your resource remains in this state for an extended period of time, please open a [support ticket](https://azure.microsoft.com/support/create-ticket/) and we will assist you.

#### How automatic failover detection works in HA enabled servers

The primary server and the secondary server has two network endpoints,
- Customer Endpoint: Customer connects and runs query on the instance using this endpoint.
- Management Endpoint: Used internally for service communications to management components and to connect to backend storage.

The health monitor component continuously does the following checks
- The monitor pings to the nodes Management network Endpoint. If this check fails two times continuously, it triggers automatic failover operation. The scenario like node is unavailable/not responding because of OS issue, networking issue between management components and nodes etc. will be addressed by this health check.
- The monitor also runs a simple query on the Instance. If the queries fail to run, automatic failover will be triggered. The scenarios like MySQL demon crashed/ stopped/hung, Backend storage issue etc., will be addressed by this health check.

> [!NOTE]  
> If there are any networking issue between the application and the customer networking endpoint (Private/Public access), either in networking path , on the endpoint or DNS issues in client side, the health check does not monitor this scenario. If you are using private access, make sure that the NSG rules for the VNet does not block the communication to the instance customer networking endpoint on port 3306. For public access make sure that the firewall rules are set and network traffic is allowed on port 3306 (if network path has any other firewalls). The DNS resolution from the client application side also needs to be taken care of.

<a id="monitoring-for-high-availability"></a>

## Monitor for high availability

The **High Availability Status** located in the server's *High Availability* pane in portal can be used to determine the server's HA configuration status.

| **Status** | **Description** |
| :--- | :--- |
| **NotEnabled** | HA isn't enabled. |
| **ReplicatingData** | Standby server is in the process of synchronizing with the primary server at the time of HA server provisioning or when HA option is enabled. |
| **FailingOver** | The database server is in the process of failing over from the primary to the standby. |
| **Healthy** | HA option is enabled. |
| **RemovingStandby** | When the HA option is disabled, and the deletion process is underway. |

You can also use the below metrics to monitor the health of the HA server.

| Metric display name | Metric | Unit | Description |
| --- | --- | --- | --- |
| HA IO Status | ha_io_running | State | HA IO Status indicates the state of HA replication. Metric value is 1 if the I/O thread is running and 0 if not. |
| HA SQL Status | ha_sql_running | State | HA SQL Status indicates the state of HA replication. Metric value is 1 if the SQL thread is running and 0 if not. |
| HA Replication Lag | replication_lag | Seconds | Replication lag is the number of seconds the standby is behind in replaying the transactions received at the primary server. |

## Limitations

Here are some considerations to keep in mind when you use high availability:
- Zone-redundant high availability can only be configured during server creation.

- High availability isn't supported in the burstable compute tier.
- Restarting the primary database server to pick up static parameter changes also restarts the standby replica.
- GTID mode will be turned on as the HA solution uses GTID. Check whether your workload has [restrictions or limitations on replication with GTIDs](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-restrictions.html).

> [!NOTE]  
> If you are enabling same-zone HA post the server create, you need to make sure the server parameters enforce_gtid_consistency" and ["gtid_mode"](./concepts-read-replicas.md#global-transaction-identifier-gtid) is set to ON before enabling HA.

> [!NOTE]  
> Storage autogrow is default enabled for a High-Availability configured server and can not to be disabled.

## Health Checks

When configuring High Availability (HA) for Azure Database for MySQL, health checks play a crucial role in maintaining the reliability and performance of your database. These checks continuously monitor the status and health of both the primary and standby replicas, ensuring that any issues are detected promptly. By tracking various metrics such as server responsiveness, replication lag, and resource utilization, health checks help to ensure that failover processes can be executed seamlessly, minimizing downtime and preventing data loss. Properly configured health checks are essential for achieving the desired level of availability and resilience in your database setup.

### Monitoring health

"Users can monitor the health of their HA setup through the Azure portal. Key metrics to observe include:

- **Server responsiveness:** Indicates whether the primary server is reachable.
- **Replication lag:** Measures the delay between the primary and standby replicas, ensuring data consistency.
- **Resource utilization:** Monitors CPU, memory, and storage usage to prevent bottlenecks."

## Related content
- [High Availability](concepts-high-availability-faq.md)
- [business continuity](concepts-business-continuity.md)
- [zone-redundant high availability](concepts-high-availability.md)
- [backup and recovery](concepts-backup-restore.md)
