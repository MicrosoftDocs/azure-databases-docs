---
title: Read replicas in Azure Database for PostgreSQL Flexible Server
description: This article describes the read replica feature usage for an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to understand how read replicas work in Azure Database for PostgreSQL flexible server, so that I can decide whether they fit my read-intensive workloads.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: how-to
---

# Read replicas in Azure Database for PostgreSQL flexible server

The read replica feature allows you to replicate data from an Azure Database for PostgreSQL flexible server to a read-only replica. Replicas are updated **asynchronously** by using the PostgreSQL engine's native physical replication technology. Streaming replication by using replication slots is the default operation mode. When necessary, file-based log shipping is used to catch up. You can replicate from the primary server to up to five replicas.

Replicas are new servers you manage similar to regular Azure Database for PostgreSQL flexible server. For each read replica, you pay for the provisioned compute in vCores and storage in GB per month.

Learn how to [create a read replica](how-to-create-read-replica.md).

## When to use a read replica

The read replica feature helps improve the performance and scale of read-intensive workloads. You can isolate read workloads to the replicas, while you direct write workloads to the primary. You can also deploy read replicas in a different region and promote them to a read-write server if disaster recovery is needed.

A typical scenario is to have BI and analytical workloads use the read replica as the data source for reporting.

Because replicas are read-only, they don't directly reduce write-capacity burdens on the primary.

### Considerations

Read replicas are primarily designed for scenarios where offloading queries is beneficial, and a slight lag is manageable. They're optimized to provide near real-time updates from the primary for most workloads, making them an excellent solution for read-heavy scenarios. However, it's important to note that they aren't intended for synchronous replication scenarios requiring up-to-the-minute data accuracy. While the data on the replica eventually becomes consistent with the primary, there might be a delay, which typically ranges from a few seconds to minutes, and in some heavy workload or high-latency scenarios, this delay could extend to hours. Typically, read replicas in the same region as the primary have less lag than geo-replicas, as the latter often deals with geographical distance-induced latency. For more insights into the performance implications of geo-replication, refer to [Geo-replication](concepts-read-replicas-geo.md) article. The data on the replica eventually becomes consistent with the data on the primary. Use this feature for workloads that can accommodate this delay.

> [!NOTE]  
> For most workloads, read replicas offer near-real-time updates from the primary. However, with persistent heavy write-intensive primary workloads, the replication lag can continue to grow and might only be able to catch up with the primary. This situation might also increase storage usage at the primary as the WAL files are only deleted once received at the replica. If this situation persists, deleting and recreating the read replica after the write-intensive workloads are completed brings the replica back to a good state for lag.
> Asynchronous read replicas aren't suitable for such heavy write workloads. When evaluating read replicas for your application, monitor the lag on the replica for a complete app workload cycle through its peak and non-peak times to assess the possible lag and the expected RTO/RPO at various points of the workload cycle.

## Create a replica

You can deploy a primary server for Azure Database for PostgreSQL flexible server in [any region that supports the service](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=postgresql&regions=all). You can create replicas of the primary server within the same region or across different global Azure regions where Azure Database for PostgreSQL is available. You can also create replicas in some Azure regions in sovereign clouds. For a list of sovereign cloud regions where you can create replicas, see the [Geo-replication](concepts-read-replicas-geo.md) article.

When you start the create replica workflow, the process creates a blank Azure Database for PostgreSQL flexible server. The new server is filled with the data on the primary server. For the creation of replicas in the same region, the process uses a snapshot approach. Therefore, the time of creation is independent of the size of the data. Geo-replicas are created by using the base backup of the primary, which is then transmitted over the network. Therefore, the creation time might range from minutes to several hours, depending on the primary size.

A replica is only considered successfully created when two conditions are met: the entire backup of the primary is copied to the replica, and the transaction logs synchronize with no more than a 1-GB lag.

To achieve a successful create operation, avoid making replicas during times of high transactional load. For example, avoid creating replicas when migrating from other sources to an Azure Database for PostgreSQL flexible server or during heavy bulk load operations. If you're migrating data or loading large amounts of data, finish this task first. After completing it, you can then start setting up the replicas. Once the migration or bulk load operation finishes, check whether the transaction log size has returned to its normal size. Typically, the transaction log size should be close to the value defined in the `max_wal_size` parameter for your server. You can track the transaction log storage footprint by using the [Transaction Log Storage Used](../monitor/concepts-monitoring.md#default-metrics) metric, which provides insights into the amount of storage used by the transaction log. By monitoring this metric, you can ensure that the transaction log size is within the expected range and that the replica creation process can start.

> [!IMPORTANT]  
> Read replicas are currently supported for the General Purpose and Memory Optimized server compute tiers. The Burstable server compute tier isn't supported.

> [!IMPORTANT]  
> When you perform replica creation, deletion, and promotion operations, the primary server enters an **updating state**. During this time, server management operations such as modifying parameters, changing high availability options, or adding or removing firewalls aren't available. The updating state only affects server management operations and doesn't affect [data plane](/azure/azure-resource-manager/management/control-plane-and-data-plane#data-plane) operations. This condition means that your database server remains fully functional and able to accept connections, as well as serve read and write traffic.

Learn how to [Create a read replica](how-to-create-read-replica.md).

### Configuration management

When you set up read replicas for an Azure Database for PostgreSQL flexible server, you need to understand which server configurations you can adjust, which configurations the replica inherits from the primary server, and any related limitations.

**Inherited configurations**

When you create a read replica, it inherits specific server configurations from the primary server. You can change these configurations during the replica's creation or after you set up the replica. However, the read replica doesn't inherit specific settings, like geo-backup, from the primary server.

**Configurations during replica creation**

- **Tier, storage size**: For the **promote to primary server** operation, the tier and storage size must match the primary server. For the **promote to independent server and remove from replication** operation, the tier and storage size can match or exceed the primary server.
- **Performance tier (IOPS)**: Adjustable.
- **Data encryption**: Adjustable, including moving from service-managed keys to customer-managed keys.

**Configurations after creation**

- **Firewall rules**: You can add, delete, or modify rules.
- **Tier, storage size**: For the **promote to primary server** operation, the tier and storage size must match the primary server. For the **promote to independent server and remove from replication** operation, the tier and storage size can match or exceed the primary server.
- **Performance tier (IOPS)**: Adjustable.
- **Authentication method**: Adjustable, options include switching from PostgreSQL authentication to Microsoft Entra.
- **Parameters**: Most parameters are adjustable. However, those [affecting shared memory size](#parameters) should align with the primary server, especially for potential **promote to primary server** scenarios. For the **promote to independent server and remove from replication** operation, these parameters should match or exceed those on the primary server.
- **Maintenance schedule**: Adjustable.

**Unsupported features on read replicas**

Primary servers support certain functionalities that you can't set up on read replicas. These functionalities include:
- Backups, including geo-backups.
- High availability (HA).

If your source Azure Database for PostgreSQL flexible server is encrypted with customer-managed keys, see the [documentation](../security/security-data-encryption.md) for other considerations.

## Create cascading read replicas

Cascading read replicas can help distribute read workloads, reducing the load on the primary server. Deploying read replicas in different regions (cross-region read replicas) can help distribute read traffic closer to users in various geographies. You can add cascading read replicas to Azure Database for PostgreSQL server. This feature allows you to create new read replicas on top of an existing read replica, with the existing read replica acting as the source for the next level. 

The first-level read replica asynchronously replicates data from the primary server. You can then create a second-level read replica by using the first-level replica as its source, forming a two-tier replication hierarchy. This architecture increases scalability, supporting up to 30 read replica servers with the primary server allowing up to five read replicas, and each of those replicas supporting five additional replicas. To add a cascading read replica to Azure Database for PostgreSQL flexible server, select the existing read replica (created from the primary server), go to the **Replication** tab, and select **Create replica**.

For example, your primary server can have up to five read replicas (level 1). One of these, say `read-replica-1`, acts as the source for another replica `read-replica-2` which becomes part of (level 2).

#### Key considerations
- You can create up to five read replicas per source read replica, with support for two levels of replication.
- The switchover operation supports intermediate read replica (source) and cascading read replica.
- The promote to primary operation doesn't support intermediate read replicas with cascading read replicas.
- Virtual endpoints aren't supported for cascading replicas.
- Cascading read replicas are supported on intermediate replicas with PostgreSQL version 14 and above.
   
## Connect to a replica

When you create a replica, it doesn't inherit the firewall rules or virtual network service endpoint of the primary server. You can set these rules during replica creation and change them later.

The replica inherits the admin account from the primary server. All user accounts on the primary server are replicated to the read replicas. You can only connect to a read replica by using the user accounts available on the primary server.

You can use two methods to connect to the replica:

* **Direct to the replica**: You can connect to the replica by using its hostname and a valid user account, just like you would on a regular Azure Database for PostgreSQL flexible server. For a server named **myreplica** with the admin username **myadmin**, you can connect to the replica by using `psql`:

```bash
psql -h myreplica.postgres.database.azure.com -U myadmin postgres
```

At the prompt, enter the password for the user account.

To make the connection process easier, the Azure portal provides ready-to-use connection strings. You can find these connection strings in the **Connect** page. They include both `libpq` variables and connection strings tailored for bash consoles.

* **Via Virtual Endpoints**: An alternative connection method uses virtual endpoints. For more information, see [Virtual endpoints](concepts-read-replicas-virtual-endpoints.md). By using virtual endpoints, you can configure the read-only endpoint to always point to the replica, regardless of which server currently holds the replica role.


## Monitor replication

The read replica feature in Azure Database for PostgreSQL relies on the replication slots mechanism. The main advantage of replication slots is that they automatically adjust the number of transaction logs (WAL segments) required by all replica servers. This adjustment helps prevent replicas from going out of sync because it avoids deleting WAL segments on the primary before the replicas receive them. The disadvantage of this approach is the risk of running out of space on the primary if the replication slot remains inactive for an extended time. In such situations, the primary accumulates WAL files, causing incremental growth of the storage usage. When the storage usage reaches 95% or if the available capacity is less than 5 GiB, the server automatically switches to read-only mode to avoid errors associated with disk-full situations.  
Therefore, monitoring the replication lag and replication slots status is crucial for read replicas.

Set alert rules for storage used or storage percentage, and for replication lags, when they exceed certain thresholds so that you can proactively act, increase the storage size, and delete lagging read replicas. For example, you can set an alert if the storage percentage exceeds 80% usage, and if the replica lag is higher than 5 minutes. The [Transaction Log Storage Used](../monitor/concepts-monitoring.md#default-metrics) metric shows you if the WAL files accumulation is the main reason for the excessive storage usage.

#### Monitoring metrics

Azure Database for PostgreSQL service provides the following metrics for monitoring replication. 

[!INCLUDE [Read-Replica Metrics](includes/read-replica-metrics-table.md)]

To learn more, see [read replica how-to article](../read-replica/how-to-create-read-replica.md).

The **Max Physical Replication Lag** metric shows the lag in bytes between the primary and the most-lagging replica. This metric is applicable and available on the primary server only, and is available only if at least one of the read replicas is connected to the primary. The lag information is present also when the replica is in the process of catching up with the primary, during replica creation, or when replication becomes inactive.

The **Read Replica Lag** metric shows the time since the last replayed transaction. For example, if no transactions are occurring on your primary server, and the last transaction was replayed 5 seconds ago, the Read Replica Lag shows 5-second delay. This metric is applicable and available on replicas only.

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
| <b> Provisioning | The read replica is being provisioned and replication between the two servers hasn't started yet. Until provisioning completes, you can't connect to the read replica. | N/A | 1 |
| <b> Updating | Server configuration is under preparation following a triggered action like promotion or read replica creation. | 2 | 2 |
| <b> Catchup | WAL files are being applied on the replica. The duration for this phase during promotion depends on the data sync option chosen - planned or forced. | 3 | 3 |
| <b> Active | Healthy state, indicating that the read replica is successfully connected to the primary. If the servers are stopped but were successfully connected prior, the status remains as active. | 4 | 4 |
| <b> Broken | Unhealthy state, indicating the promote operation might have failed, or the replica is unable to connect to the primary for some reason. To resolve this state, drop the replica and recreate the replica. | N/A | N/A |

Learn how to [monitor replication](../read-replica/how-to-create-read-replica.md).


## Considerations

This section summarizes considerations about the read replica feature. The following considerations apply.

- **Power operations**: You can apply power operations, including [start](../configure-maintain/how-to-start-server.md) and [stop](../configure-maintain/how-to-stop-server.md) actions, to both the primary and replica servers. However, to preserve system integrity, follow a specific sequence. Before stopping the read replicas, ensure the primary server is stopped first. When commencing operations, initiate the start action on the replica servers before starting the primary server.
- If a server has read replicas, delete the read replicas first before deleting the primary server.
- [In-place major version upgrade](../configure-maintain/concepts-major-version-upgrade.md) for an Azure Database for PostgreSQL flexible server requires removing any read replicas and cascading read replicas that are enabled on the server. Once the replicas are deleted, you can upgrade the primary server to the desired major version. After the upgrade is complete, you can recreate the replicas to resume the replication process.
  - **Resetting admin password**: Resetting the admin password on the replica server isn't currently supported. Additionally, updating the admin password along with [promoting](concepts-read-replicas-promote.md) replica operation in the same request isn't supported. If you want to perform these actions, first promote the replica server, and then update the password on the newly promoted server separately.

### New replicas

You create a read replica as a new Azure Database for PostgreSQL flexible server. You can't make an existing server into a replica.

### Resource move

You can create read replicas in a different resource group than the primary. However, moving read replicas to another resource group after their creation isn't supported. Additionally, moving replicas to a different subscription isn't supported. Moving the primary that has read replicas to another resource group or subscription isn't supported.

### Storage autogrow
When you configure read replicas for an Azure Database for PostgreSQL flexible server, ensure that the storage autogrow setting on the replicas matches that of the primary server. The storage autogrow feature allows the database storage to increase automatically to prevent running out of space, which could lead to database outages.
Here’s how to manage storage autogrow settings effectively:

- You can have storage autogrow enabled on any replica regardless of the primary server’s setting.
- If storage autogrow is enabled on the primary server, it must also be enabled on the replicas to ensure consistency in storage scaling behaviors.
- To enable storage autogrow on the primary, you must first enable it on the replicas. This order of operations is crucial to maintain replication integrity.
- Conversely, if you wish to disable storage autogrow, begin by disabling it on the primary server before the replicas to avoid replication complications.

### Back up and restore

When you manage backups and restores for your Azure Database for PostgreSQL flexible server, keep in mind the current and previous role of the server in different [promotion scenarios](concepts-read-replicas-promote.md). Remember these key points:

**Promote to primary server**

- **No backups from read replicas**: The system never takes backups from read replica servers, regardless of their past role.
- **Preservation of past backups**: If a server was once a primary and the system took backups during that period, it preserves those backups up to the user-defined retention period.
- **Restore operation restrictions**: Even if past backups exist for a server that transitions to a read replica, restore operations are restricted. You can only initiate a restore operation when the server is promoted back to the primary role.

For clarity, the following table illustrates these points:

| **Server role** | **Backup taken** | **Restore allowed** |
| --- | --- | --- |
| Primary | Yes | Yes |
| Read replica | No | No |
| Read replica promoted to primary | Yes | Yes |

**Promote to independent server and remove from replication**

While the server is a read replica, the system doesn't take backups. However, once you promote it to an independent server, the system takes backups for both the promoted server and the primary server. You can restore backups on both servers.

### Networking

Read replicas support all the networking options that Azure Database for PostgreSQL flexible server supports.

> [!IMPORTANT]  
> Bi-directional communication between the primary server and read replicas is crucial for the Azure Database for PostgreSQL setup. The Azure virtual network subnet must allow sending and receiving traffic on destination port 5432.

This requirement not only facilitates the synchronization process but also ensures proper functioning of the promote mechanism. Replicas might need to communicate in reverse order - from replica to primary - especially during promote to primary operations. Moreover, you must permit connections to the Azure storage account that stores Write-Ahead Logging (WAL) archives to uphold data durability and enable efficient recovery processes.

For more information about how to configure private access (virtual network integration) for your read replicas and understand the implications for replication across Azure regions and virtual networks within a private networking context, see the [Replication across Azure regions and virtual networks with private networking](../network/concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking) article.

### Replication slot issues mitigation

In rare cases, high lag caused by replication slots can lead to increased storage usage on the primary server due to accumulated WAL files. If the storage usage reaches 95% or the available capacity falls below 5 GiB, the server automatically switches to read-only mode to prevent disk-full errors.

Maintaining the primary server's health and functionality is a priority. In such edge cases, the server might drop the replication slot to ensure the primary server remains operational for read and write traffic. So, replication switches to file-based log shipping mode, which could result in a higher replication lag.

Monitor storage usage and replication lag closely and take necessary actions to mitigate potential issues before they escalate.

### Parameters

When you create a read replica, it inherits the parameters from the primary server. This inheritance ensures a consistent and reliable starting point. However, any changes to the parameters on the primary server that you make after creating the read replica aren't automatically replicated. This behavior offers the advantage of individual tuning of the read replica, such as enhancing its performance for read-intensive operations without modifying the primary server's parameters. While this behavior provides flexibility and customization options, it also necessitates careful and manual management to maintain consistency between the primary and its replica when uniformity of parameters is required.

Administrators can change parameters on the read replica server and set different values than on the primary server. The only exception is parameters that might affect the recovery of the replica, mentioned also in the "Scaling" section below: `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders`, `max_worker_processes`. To ensure the read replica's recovery is seamless and it doesn't encounter shared memory limitations, always set these particular parameters to values that are either equivalent to or [greater than those configured on the primary server](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN). Before lowering parameter values on a read replica server, ensure that replication lag is minimal or the replica is fully caught up with the primary server, to avoid potential replication or recovery issues.

### Scale

You can scale up and down compute (vCores), change the service tier from General Purpose to Memory Optimized (or vice versa), and scale up the storage. However, the following caveats apply.

For compute scaling:

- Azure Database for PostgreSQL service requires several parameters on replicas to be [greater than or equal to the setting on the primary](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN) to ensure that the replica doesn't run out of shared memory during recovery. The affected parameters are: `max_connections`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_wal_senders`, `max_worker_processes`.

- **Scaling up**: First scale up a replica's compute, then scale up the primary.

- **Scaling down**: First scale down the primary's compute, then scale down the replica.

- Compute on the primary must always be equal to or smaller than the compute on the smallest replica.

For storage scaling:

- **Scaling up**: First scale up a replica's storage, then scale up the primary.

- Storage size on the primary must always be equal to or smaller than the storage size on the smallest replica.

## Related content

- [Geo-replication in Azure Database for PostgreSQL](concepts-read-replicas-geo.md).
- [Promote read replicas in Azure Database for PostgreSQL](concepts-read-replicas-promote.md).
- [Virtual endpoints for read replicas in Azure Database for PostgreSQL](concepts-read-replicas-virtual-endpoints.md).
- [Create a read replica](how-to-create-read-replica.md).
- [Replication across Azure regions and virtual networks with private networking](../network/concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking).
