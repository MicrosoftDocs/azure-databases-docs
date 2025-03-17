---
title: Read replicas
description: This article describes the read replica feature in Azure Database for PostgreSQL flexible server.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 05/02/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
ms.custom:
  - ignite-2023
---

# Read replicas in Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The read replica feature allows you to replicate data from an Azure Database for PostgreSQL flexible server instance to a read-only replica. Replicas are updated **asynchronously** with the PostgreSQL engine's native physical replication technology. Streaming replication by using replication slots is the default operation mode. When necessary, file-based log shipping is used to catch up. You can replicate from the primary server to up to five replicas.

Replicas are new servers you manage similar to regular Azure Database for PostgreSQL flexible server instances. For each read replica, you're billed for the provisioned compute in vCores and storage in GB/ month.

Learn how to [create and manage replicas](how-to-read-replicas-portal.md).

## When to use a read replica

The read replica feature helps to improve the performance and scale of read-intensive workloads. Read workloads can be isolated to the replicas, while write workloads can be directed to the primary. Read replicas can also be deployed in a different region and can be promoted to a read-write server if disaster recovery is needed.

A typical scenario is to have BI and analytical workloads use the read replica as the data source for reporting.

Because replicas are read-only, they don't directly reduce write-capacity burdens on the primary.

### Considerations

Read replicas are primarily designed for scenarios where offloading queries is beneficial, and a slight lag is manageable. They're optimized to provide near real time updates from the primary for most workloads, making them an excellent solution for read-heavy scenarios. However, it's important to note that they aren't intended for synchronous replication scenarios requiring up-to-the-minute data accuracy. While the data on the replica eventually becomes consistent with the primary, there might be a delay, which typically ranges from a few seconds to minutes, and in some heavy workload or high-latency scenarios, this delay could extend to hours. Typically, read replicas in the same region as the primary has less lag than geo-replicas, as the latter often deals with geographical distance-induced latency. For more insights into the performance implications of geo-replication, refer to [Geo-replication](concepts-read-replicas-geo.md) article. The data on the replica eventually becomes consistent with the data on the primary. Use this feature for workloads that can accommodate this delay.

> [!NOTE]  
> For most workloads, read replicas offer near-real-time updates from the primary. However, with persistent heavy write-intensive primary workloads, the replication lag could continue to grow and might only be able to catch up with the primary. This might also increase storage usage at the primary as the WAL files are only deleted once received at the replica. If this situation persists, deleting and recreating the read replica after the write-intensive workloads are completed, you can bring the replica back to a good state for lag.
> Asynchronous read replicas are not suitable for such heavy write workloads. When evaluating read replicas for your application, monitor the lag on the replica for a complete app workload cycle through its peak and non-peak times to assess the possible lag and the expected RTO/RPO at various points of the workload cycle.

## Create a replica

A primary server for Azure Database for PostgreSQL flexible server can be deployed in [any region that supports the service](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=postgresql&regions=all). You can create replicas of the primary server within the same region or across different global Azure regions where Azure Database for PostgreSQL flexible server is available. The capability to create replicas now extends to some special Azure regions. See the [Geo-replication](concepts-read-replicas-geo.md) article for a list of special regions where you can create replicas.

When you start the create replica workflow, a blank Azure Database for PostgreSQL flexible server instance is created. The new server is filled with the data on the primary server. For the creation of replicas in the same region, a snapshot approach is used. Therefore, the time of creation is independent of the size of the data. Geo-replicas are created using the base backup of the primary instance, which is then transmitted over the network; therefore, the creation time might range from minutes to several hours, depending on the primary size.

Replica is only considered successfully created when two conditions are met: the entire backup of the primary instance must be copied to the replica, and the transaction logs must synchronize with no more than a 1-GB lag.

To achieve a successful create operation, avoid making replicas during times of high transactional load. For example, you should avoid creating replicas when migrating from other sources to Azure Database for PostgreSQL flexible server or during heavy bulk load operations. If you're migrating data or loading large amounts of data right now, it's best to finish this task first. After completing it, you can then start setting up the replicas. Once the migration or bulk load operation has finished, check whether the transaction log size has returned to its normal size. Typically, the transaction log size should be close to the value defined in the max_wal_size server parameter for your instance. You can track the transaction log storage footprint using the [Transaction Log Storage Used](concepts-monitoring.md#default-metrics) metric, which provides insights into the amount of storage used by the transaction log. By monitoring this metric, you can ensure that the transaction log size is within the expected range and that the replica creation process might be started.

> [!IMPORTANT]  
> Read Replicas are currently supported for the General Purpose and Memory Optimized server compute tiers. The Burstable server compute tier is not supported.

> [!IMPORTANT]  
> When performing replica creation, deletion, and promotion operations, the primary server will enter an **updating state**. During this time, server management operations such as modifying server parameters, changing high availability options, or adding or removing firewalls will be unavailable. It's important to note that the updating state only affects server management operations and does not affect [data plane](/azure/azure-resource-manager/management/control-plane-and-data-plane#data-plane) operations. This means that your database server will remain fully functional and able to accept connections, as well as serve read and write traffic.

Learn how to [create a read replica in the Azure portal](how-to-read-replicas-portal.md).

### Configuration management

When setting up read replicas for Azure Database for PostgreSQL flexible server, it's essential to understand the server configurations that can be adjusted, the ones inherited from the primary, and any related limitations.

**Inherited configurations**

When a read replica is created, it inherits specific server configurations from the primary server. These configurations can be changed either during the replica's creation or after it has been set up. However, specific settings, like geo-backup, won't be replicated to the read replica.

**Configurations during replica creation**

- **Tier, storage size**: For the "promote to primary server" operation, it must be the same as the primary. For the "promote to independent server and remove from replication" operation, it can be the same or higher than the primary.
- **Performance tier (IOPS)**: Adjustable.
- **Data encryption**: Adjustable, include moving from service-managed keys to customer-managed keys.

**Configurations post creation**

- **Firewall rules**: Can be added, deleted, or modified.
- **Tier, storage size**: For the "promote to primary server" operation, it must be the same as the primary. For the "promote to independent server and remove from replication" operation, it can be the same or higher than the primary.
- **Performance tier (IOPS)**: Adjustable.
- **Authentication method**: Adjustable, options include switching from PostgreSQL authentication to Microsoft Entra.
- **Server parameters**: Most are adjustable. However, those [affecting shared memory size](#server-parameters) should align with the primary, especially for potential "promote to primary server" scenarios. For the "promote to independent server and remove from replication" operation, these parameters should be the same or exceed those on the primary.
- **Maintenance schedule**: Adjustable.

**Unsupported features on read replicas**

Certain functionalities are restricted to primary servers and can't be set up on read replicas. These include:
- Backups, including geo-backups.
- High availability (HA)

If your source Azure Database for PostgreSQL flexible server instance is encrypted with customer-managed keys, see the [documentation](concepts-data-encryption.md) for other considerations.

## Connect to a replica

When you create a replica, it does inherit the firewall rules or virtual network service endpoint of the primary server. These rules might be changed during replica creation and at any later point in time.

The replica inherits the admin account from the primary server. All user accounts on the primary server are replicated to the read replicas. You can only connect to a read replica by using the user accounts available on the primary server.

There are two methods to connect to the replica:

* **Direct to the Replica Instance**: You can connect to the replica using its hostname and a valid user account, as you would on a regular Azure Database for PostgreSQL flexible server instance. For a server named **myreplica** with the admin username **myadmin**, you can connect to the replica by using `psql`:

```bash
psql -h myreplica.postgres.database.azure.com -U myadmin postgres
```

At the prompt, enter the password for the user account.

Furthermore, to ease the connection process, the Azure portal provides ready-to-use connection strings. These can be found in the **Connect** page. They encompass both `libpq` variables and connection strings tailored for bash consoles.

* **Via Virtual Endpoints**: There's an alternative connection method using virtual endpoints, as detailed in [Virtual endpoints](concepts-read-replicas-virtual-endpoints.md) article. By using virtual endpoints, you can configure the read-only endpoint to consistently point to the replica, regardless of which server currently holds the replica role.


## Monitor replication

Read replica feature in Azure Database for PostgreSQL flexible server relies on replication slots mechanism. The main advantage of replication slots is that they automatically adjust the number of transaction logs (WAL segments) required by all replica servers. This helps prevent replicas from going out of sync because it avoids deleting WAL segments on the primary before they are sent to the replicas. The disadvantage of the approach is the risk of going out of space on the primary in case the replication slot remains inactive for an extended time. In such situations, primary accumulates WAL files causing incremental growth of the storage usage. When the storage usage reaches 95% or if the available capacity is less than 5 GiB, the server is automatically switched to read-only mode to avoid errors associated with disk-full situations.  
Therefore, monitoring the replication lag and replication slots status is crucial for read replicas.

We recommend setting alert rules for storage used or storage percentage, and for replication lags, when they exceed certain thresholds so that you can proactively act, increase the storage size, and delete lagging read replicas. For example, you can set an alert if the storage percentage exceeds 80% usage, and if the replica lag is higher than 5 minutes. The [Transaction Log Storage Used](concepts-monitoring.md#default-metrics) metric shows you if the WAL files accumulation is the main reason of the excessive storage usage.

#### Moniotring metrics

Azure Database for PostgreSQL flexible server provides following metrics for monitoring replication. 

[!INCLUDE [Read-Replica Metrics](includes/read-replica-metrics-table.md)]

To learn more, see [read replica how-to article](how-to-read-replicas-portal.md#monitor-a-replica).

The **Max Physical Replication Lag** metric shows the lag in bytes between the primary and the most-lagging replica. This metric is applicable and available on the primary server only, and will be available only if at least one of the read replicas is connected to the primary. The lag information is present also when the replica is in the process of catching up with the primary, during replica creation, or when replication becomes inactive.

The **Read Replica Lag** metric shows the time since the last replayed transaction. For instance if no transactions are occurring on your primary server, and the last transaction was replayed 5 seconds ago, then the Read Replica Lag shows 5-second delay. This metric is applicable and available on replicas only.

Set an alert to inform you when the replica lag reaches a value that isn't acceptable for your workload.

For more insight, query the primary server directly to get the replication lag on all replicas.

> [!NOTE]  
> If a primary server or read replica restarts, the time it takes to restart and catch up is reflected in the Replica Lag metric.

**Replication state**

To monitor the progress and status of the replication and promote operation, refer to the **Replication state** column in the Azure portal. This column is located in the replication page and displays various states that provide insights into the current condition of the read replicas and their link to the primary. For users relying on the Azure Resource Manager API, when invoking the `GetReplica` API, the state appears as ReplicationState in the `replica` property bag.

Here are the possible values:

| **Replication state** | **Description** | **Promote order** | **Read replica creation order** |
| --- | --- | --- | --- |
| <b> Reconfiguring | Awaiting start of the replica-primary link. It might remain longer if the replica or its region is unavailable, for example, due to a disaster. | 1 | N/A |
| <b> Provisioning | The read replica is being provisioned and replication between the two servers has yet to start. Until provisioning completes, you can't connect to the read replica. | N/A | 1 |
| <b> Updating | Server configuration is under preparation following a triggered action like promotion or read replica creation. | 2 | 2 |
| <b> Catchup | WAL files are being applied on the replica. The duration for this phase during promotion depends on the data sync option chosen - planned or forced. | 3 | 3 |
| <b> Active | Healthy state, indicating that the read replica has been successfully connected to the primary. If the servers are stopped but were successfully connected prior, the status remains as active. | 4 | 4 |
| <b> Broken | Unhealthy state, indicating the promote operation might have failed, or the replica is unable to connect to the primary for some reason. Please drop the replica and recreate the replica to resolve this." | N/A | N/A |

Learn how to [monitor replication](how-to-read-replicas-portal.md#monitor-a-replica).


## Considerations

This section summarizes considerations about the read replica feature. The following considerations do apply.

- **Power operations**: Power operations, including [start](how-to-start-server.md) and [stop](how-to-stop-server.md) actions, can be applied to both the primary and replica servers. However, to preserve system integrity, a specific sequence should be followed. Before stopping the read replicas, ensure the primary server is stopped first. When commencing operations, initiate the start action on the replica servers before starting the primary server.
- If server has read replicas, then read replicas should be deleted first before deleting the primary server.
- [In-place major version upgrade](concepts-major-version-upgrade.md) in Azure Database for PostgreSQL flexible server requires removing any read replicas currently enabled on the server. Once the replicas have been deleted, the primary server can be upgraded to the desired major version. After the upgrade is complete, you can recreate the replicas to resume the replication process.
- **Premium SSD v2**: As of the current release, if the primary server uses Premium SSD v2 for storage, the creation of read replicas isn't supported.
- **Resetting admin password**: Resetting the admin password on the replica server is currently not supported. Additionally, updating the admin password along with [promoting](concepts-read-replicas-promote.md) replica operation in the same request is also not supported. If you wish to do this you must first promote the replica server, and then update the password on the newly promoted server separately.

### New replicas

A read replica is created as a new Azure Database for PostgreSQL flexible server instance. An existing server can't be made into a replica. You can't create a replica of another read replica, that is, cascading replication isn't supported.

### Resource move

Users can create read replicas in a different resource group than the primary. However, moving read replicas to another resource group after their creation is unsupported. Additionally, moving replicas to a different subscription, and moving the primary that has read replicas to another resource group or subscription, it's not supported.

### Storage autogrow
When configuring read replicas for an Azure Database for PostgreSQL flexible server instance, it's essential to ensure that the storage autogrow setting on the replicas matches that of the primary server. The storage autogrow feature allows the database storage to increase automatically to prevent running out of space, which could lead to database outages.
Here’s how to manage storage autogrow settings effectively:

- You can have storage autogrow enabled on any replica regardless of the primary server’s setting.
- If storage autogrow is enabled on the primary server, it must also be enabled on the replicas to ensure consistency in storage scaling behaviors.
- To enable storage autogrow on the primary, you must first enable it on the replicas. This order of operations is crucial to maintain replication integrity.
- Conversely, if you wish to disable storage autogrow, begin by disabling it on the primary server before the replicas to avoid replication complications.

### Back up and Restore

When managing backups and restores for your Azure Database for PostgreSQL flexible server instance, it's essential to keep in mind the current and previous role of the server in different [promotion scenarios](concepts-read-replicas-promote.md). Here are the key points to remember:

**Promote to primary server**

1. **No backups are taken from read replicas**: Backups are never taken from read replica servers, regardless of their past role.

1. **Preservation of past backups**: If a server was once a primary and has backups taken during that period, those backups are preserved. They'll be retained up to the user-defined retention period.

1. **Restore Operation Restrictions**: Even if past backups exist for a server that has transitioned to a read replica, restore operations are restricted. You can only initiate a restore operation when the server has been promoted back to the primary role.

For clarity, here's a table illustrating these points:

| **Server role** | **Backup taken** | **Restore allowed** |
| --- | --- | --- |
| Primary | Yes | Yes |
| Read replica | No | No |
| Read replica promoted to primary | Yes | Yes |

**Promote to independent server and remove from replication**

While the server is a read replica, no backups are taken. However, once it's promoted to an independent server, both the promoted server and the primary server have backups taken, and restores are allowed on both.

### Networking

Read replicas support all the networking options supported by Azure Database for PostgreSQL Flexible Server.

> [!IMPORTANT]  
> Bi-directional communication between the primary server and read replicas is crucial for the Azure Database for PostgreSQL flexible server setup. There must be a provision to send and receive traffic on destination port 5432 within the Azure virtual network subnet.

The above requirement not only facilitates the synchronization process but also ensures proper functioning of the promote mechanism where replicas might need to communicate in reverse order - from replica to primary - especially during promote to primary operations. Moreover, connections to the Azure storage account that stores Write-Ahead Logging (WAL) archives must be permitted to uphold data durability and enable efficient recovery processes.

For more information about how to configure private access (virtual network integration) for your read replicas and understand the implications for replication across Azure regions and virtual networks within a private networking context, see the [Replication across Azure regions and virtual networks with private networking](concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking) page.

### Replication slot issues mitigation

In rare cases, high lag caused by replication slots can lead to increased storage usage on the primary server due to accumulated WAL files. If the storage usage reaches 95% or the available capacity falls below 5 GiB, the server automatically switches to read-only mode to prevent disk-full errors.

Since maintaining the primary server's health and functionality is a priority, in such edge cases, the replication slot might be dropped to ensure the primary server remains operational for read and write traffic. So, replication switches to file-based log shipping mode, which could result in a higher replication lag.

It's essential to monitor storage usage and replication lag closely and take necessary actions to mitigate potential issues before they escalate.

### Server parameters

When a read replica is created, it inherits the server parameters from the primary server. This is to ensure a consistent and reliable starting point. However, any changes to the server parameters on the primary server made after creating the read replica aren't automatically replicated. This behavior offers the advantage of individual tuning of the read replica, such as enhancing its performance for read-intensive operations without modifying the primary server's parameters. While this provides flexibility and customization options, it also necessitates careful and manual management to maintain consistency between the primary and its replica when uniformity of server parameters is required.

Administrators can change server parameters on the read replica server and set different values than on the primary server. The only exception is parameters that might affect the recovery of the replica, mentioned also in the "Scaling" section below: `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders`, `max_worker_processes`. To ensure the read replica's recovery is seamless and it doesn't encounter shared memory limitations, these particular parameters should always be set to values that are either equivalent to or [greater than those configured on the primary server](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN).

### Scale

You're free to scale up and down compute (vCores), changing the service tier from General Purpose to Memory Optimized (or vice versa) and scaling up the storage, but the following caveats do apply.

For compute scaling:

- Azure Database for PostgreSQL flexible server requires several parameters on replicas to be [greater than or equal to the setting on the primary](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN) to ensure that the replica doesn't run out of shared memory during recovery. The parameters affected are: `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders`, `max_worker_processes`.

- **Scaling up**: First scale up a replica's compute, then scale up the primary.

- **Scaling down**: First scale down the primary's compute, then scale down the replica.

- Compute on the primary must always be equal or smaller than the compute on the smallest replica.

For storage scaling:

- **Scaling up**: First scale up a replica's storage, then scale up the primary.

- Storage size on the primary must be always equal or smaller than the storage size on the smallest replica.

## Related content

- [Geo-replication in Azure Database for PostgreSQL flexible server](concepts-read-replicas-geo.md).
- [Promote read replicas in Azure Database for PostgreSQL flexible server](concepts-read-replicas-promote.md).
- [Virtual endpoints for read replicas in Azure Database for PostgreSQL flexible server](concepts-read-replicas-virtual-endpoints.md).
- [Create and manage read replicas in Azure Database for PostgreSQL flexible server](how-to-read-replicas-portal.md).
- [Replication across Azure regions and virtual networks with private networking](concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking).
