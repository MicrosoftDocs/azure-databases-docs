---
title: Read Replicas
description: "Learn about read replicas in Azure Database for MySQL - Flexible Server: creating replicas, connecting to replicas, monitoring replication, and stopping replication."
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/25/2025
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Read replicas in Azure Database for MySQL

MySQL is one of the popular database engines for running internet-scale web and mobile applications. Many customers use Azure Database for MySQL for a wide range of applications, including online education, video streaming, digital payments, e-commerce, gaming, news portals, government, and healthcare websites. These services must be able to serve and scale as traffic on the web or mobile application increases.

On the applications side, developers typically use Java or PHP. They migrate the application to run on Azure Virtual Machine Scale Sets, Azure App Services, or containerize it to run on Azure Kubernetes Service (AKS). With Virtual Machine Scale Set, App Service, or AKS as the underlying infrastructure, application scaling is simplified by instantaneously provisioning new VMs and replicating the stateless components of applications to cater to the requests. However, the database often becomes a bottleneck as a centralized stateful component.

The read replica feature enables you to replicate data from an Azure Database for MySQL Flexible Server instance to a read-only server. You can replicate from the source server to up to **10** replicas. Replicas are updated asynchronously by using the MySQL engine's native binary log (binlog) file position-based replication technology. To learn more about binlog replication, see the [MySQL binlog replication overview](https://dev.mysql.com/doc/refman/5.7/en/binlog-replication-configuration-overview.html).

You manage replicas as new servers, just like your source Azure Database for MySQL Flexible Server instances. You incur billing charges for each read replica based on the provisioned compute in vCores and storage in GB per month. For more information, see [pricing](./concepts-compute-storage.md#pricing).

The read replica feature is only available for Azure Database for MySQL Flexible Server instances in the General Purpose or Memory-Optimized pricing tiers. Ensure the source server is in one of these pricing tiers.

To learn more about MySQL replication features and issues, see the [MySQL replication documentation](https://dev.mysql.com/doc/refman/5.7/en/replication-features.html).

> [!NOTE]
> This article contains references to the term *slave*, a term that Microsoft no longer uses. When we remove the term from the software, we remove it from this article.

## Common use cases for read replica

The read replica feature helps you improve the performance and scale of read-intensive workloads. You can isolate read workloads to the replicas, while directing write workloads to the source.

Common scenarios include:

- Scaling read workloads coming from the application by using a lightweight connection proxy like [ProxySQL](https://aka.ms/ProxySQLLoadBalanceReplica) or using a microservices-based pattern to scale out your read queries coming from the application to read replicas
- Using read replicas as a data source for BI or analytical reporting workloads
- Ingesting telemetry information into the MySQL database engine while using multiple read replicas for reporting of data in IoT or Manufacturing scenarios

Because replicas are read-only, they don't directly reduce write-capacity burdens on the source. This feature isn't targeted at write-intensive workloads.

The read replica feature uses MySQL asynchronous replication. The feature isn't meant for synchronous replication scenarios. There's a measurable delay between the source and the replica. The data on the replica eventually becomes consistent with the data on the source. Use this feature for workloads that can accommodate this delay.

## Cross-region replication

You can create a read replica in a different region from your source server. Cross-region replication can be helpful for scenarios like disaster recovery planning or bringing data closer to your users. Azure Database for MySQL Flexible Server allows you to provision a read-replica in any [Azure supported regions](/azure/reliability/cross-region-replication-azure) where Azure Database for MySQL Flexible Server is available. Using this feature, a source server can have a replica in its paired region or the universal replica regions. See [here](./overview.md#azure-regions) to find the list of Azure regions where Azure Database for MySQL Flexible Server is available today.

## Create a replica

When you start the create replica workflow, you create a blank Azure Database for MySQL Flexible Server instance. The new server contains the data that was on the source server. The creation time depends on the amount of data on the source and the time since the last weekly full backup. The time can range from a few minutes to several hours.

> [!NOTE]  
> You create read replicas with the same server configuration as the source. You can change the replica server configuration after creation. You always create the replica server in the same resource group and subscription as the source server. If you want to create a replica server in a different resource group or a different subscription, you can [move the replica server](/azure/azure-resource-manager/management/move-resource-group-and-subscription) after creation. Keep the replica server's configuration at equal or greater values than the source to ensure the replica can keep up with the source.

Learn how to [create a read replica in the Azure portal](how-to-read-replicas-portal.md).

## Connect to a replica

When you create a replica, it inherits the connectivity method of the source server. You can't change the connectivity method of the replica. For example, if the source server uses **Private access (VNet Integration)**, the replica can't use **Public access (allowed IP addresses)**.

The replica inherits the admin account from the source server. All user accounts on the source server are replicated to the read replicas. You can only connect to a read replica by using the user accounts available on the source server.

You can connect to the replica by using its hostname and a valid user account, as you would on a regular Azure Database for MySQL Flexible Server instance. For a server named **myreplica** with the admin username **myadmin**, you can connect to the replica by using the MySQL CLI:

```bash
mysql -h myreplica.mysql.database.azure.com -u myadmin -p
```

At the prompt, enter the password for the user account.

## Monitor replication

Azure Database for MySQL Flexible Server provides the **Replication lag in seconds** metric in Azure Monitor. This metric is available for replicas only. Azure Monitor calculates this metric by using the `seconds_behind_master` metric in MySQL's `SHOW SLAVE STATUS` command. Set an alert to notify you when the replication lag exceeds an unacceptable threshold for your workload.

If you see increased replication lag, refer to [troubleshooting replication latency](./../howto-troubleshoot-replication-latency.md) to troubleshoot and understand possible causes.

> [!IMPORTANT]  
> Read Replica uses storage-based replication technology, which no longer uses the `SLAVE_IO_RUNNING`/`REPLICA_IO_RUNNING` metric available in MySQL's `SHOW SLAVE` `STATUS'/'SHOW` `REPLICA STATUS` command. This value is always displayed as "No" and isn't indicative of replication status. To know the correct status of replication, refer to replication metrics - **Replica `IO` Status** and **Replica SQL Status** under the Monitoring page.

## Stop replication

You can stop replication between a source server and a replica server. When you stop replication between a source server and a read replica, the replica server becomes a standalone server. The standalone server contains the data that was available on the replica server when you started the stop replication command. The standalone server doesn't synchronize any missing data from the source server.

When you stop replication to a replica server, the replica server loses all links to its previous source server and to other replica servers. There's no automated failover between a source server and its replica servers.

> [!IMPORTANT]  
> You can't convert the standalone server back into a replica server.
> Before you stop replication on a read replica, make sure the replica server has all the data you need.

For more information, see [stop replication to a replica](how-to-read-replicas-portal.md).

## Failover

There's no automated failover between source and replica servers.

Read replicas scale read-intensive workloads and don't provide high availability for a server. You perform manual failover by stopping replication on a read replica by bringing it online in read-write mode.

Because replication is asynchronous, there's a lag between the source and the replica. Many factors influence the amount of lag, such as the workload on the source server and the latency between data centers. In most cases, replica lag ranges between a few seconds to a couple of minutes. You can track your actual replication lag by using the *Replica Lag* metric, which is available for each replica. This metric shows the time since the last replayed transaction. We recommend that you identify your average lag by observing your replica lag over time. You can set an alert on replica lag, so that if it goes outside your expected range, you can take action.

> [!TIP]  
> If you fail over to the replica, the lag at the time you unlink the replica from the source indicates how much data is lost.

After you decide to fail over to a replica:

1. Stop replication to the replica

    You need to stop replication to make the replica server able to accept writes. This process delinks the replica server from the source. After you initiate stop replication, the backend process typically takes about two minutes to complete. See the [stop replication](#stop-replication) section of this article to understand the implications of this action.

1. Point your application to the (former) replica

    Each server has a unique connection string. Update your application to point to the (former) replica instead of the source.

When your application successfully processes reads and writes, you complete the failover. The amount of downtime your application experiences depends on when you detect an issue and complete steps 1 and 2.

## Global transaction identifier (GTID)

A global transaction identifier (GTID) is a unique identifier that the source server creates with each committed transaction. Azure Database for MySQL Flexible Server turns off GTID by default. Versions 5.7 and 8.0 support GTID. For more information about GTID and how replication uses it, see MySQL's [replication with GTID](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids.html) documentation.

Use the following server parameters to configure GTID:

| **Server parameter** | **Description** | **Default Value** | **Values** |
| --- | --- | --- | --- |
| `gtid_mode` | Indicates if GTIDs are used to identify transactions. Changes between modes can only be done one step at a time in ascending order (ex., `OFF` -> `OFF_PERMISSIVE` -> `ON_PERMISSIVE` -> `ON`) | `OFF*` | `OFF`: Both new and replication transactions must be anonymous<br />`OFF_PERMISSIVE`: New transactions are anonymous. Replicated transactions can either be anonymous or GTID transactions.<br />`ON_PERMISSIVE`: New transactions are GTID transactions. Replicated transactions can either be anonymous or GTID transactions.<br />`ON`: Both new and replicated transactions must be GTID transactions. |
| `enforce_gtid_consistency` | Enforces GTID consistency by allowing execution of only those statements that can be logged in a transactionally safe manner. Set the value `ON` before enabling GTID replication. | `OFF*` | `OFF`: All transactions are allowed to violate GTID consistency.<br />`ON`: No transaction is allowed to violate GTID consistency.<br />`WARN`: All transactions are allowed to violate GTID consistency, but a warning is generated. |


> [!NOTE]
> For Azure Database for MySQL Flexible Server instances that have the High-availability feature enabled, the default value is set to `ON`.

After you enable GTID, you can't turn it off. If you need to turn off GTID, contact support.

You can change GTIDs from one value to another only one step at a time in ascending order of modes. For example, if `gtid_mode` is currently set to `OFF_PERMISSIVE`, you can change it to `ON_PERMISSIVE` but not to `ON`.

To keep replication consistent, you can't update it for a primary or replica server.

Set `enforce_gtid_consistency` to `ON` before setting `gtid_mode` to `ON`.

To enable GTID and configure the consistency behavior, update the `gtid_mode` and `enforce_gtid_consistency` server parameters. Use [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](how-to-configure-server-parameters-portal.md) or [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure CLI](how-to-configure-server-parameters-cli.md).

If a source server enables GTID (`gtid_mode` = `ON`), newly created replicas also enable GTID and use GTID replication. To ensure replication consistency, you can't change `gtid_mode` after creating primary or replica servers with GTID enabled.

## Considerations and limitations

| Scenario | Limitation/Consideration |
| --- | --- |
| Replica on server in Burstable Pricing Tier | Not supported |
| Pricing | The cost of running the replica server depends on the region where the replica server runs. |
| Source server downtime/restart | No restart or downtime is needed when creating a read replica. This operation is an online operation. |
| New replicas | You create a read replica as a new Azure Database for MySQL Flexible Server instance. You can't make an existing server into a replica. You can't create a replica of another read replica. |
| Replica configuration | You create a replica by using the same server configuration as the source. After you create a replica, you can change several settings independently from the source server: compute generation, vCores, storage, and backup retention period. You can also change the compute tier independently.<br /><br />**IMPORTANT** - Before you update a source server configuration to new values, update the replica configuration to equal or greater values. This action ensures the replica can keep up with any changes made to the source.<br />Connectivity method and parameter settings are inherited from the source server to the replica when you create the replica. Afterwards, the replica's rules are independent. |
| Stopped replicas | If you stop replication between a source server and a read replica, the stopped replica becomes a standalone server that accepts both reads and writes. You can't make the standalone server into a replica again. |
| Deleted source servers | When you delete a source server, replication stops to all read replicas. These replicas automatically become standalone servers and can accept both reads and writes. The source server itself is deleted. |
| User accounts | Users on the source server are replicated to the read replicas. You can only connect to a read replica by using the user accounts available on the source server. |
| Server parameters | To prevent data from becoming out of sync and to avoid potential data loss or corruption, some server parameters are locked from being updated when using read replicas.<br />The following server parameters are locked on both the source and replica servers:<br />- [`innodb_file_per_table`](https://dev.mysql.com/doc/refman/8.0/en/innodb-file-per-table-tablespaces.html)<br />- [`log_bin_trust_function_creators`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_log_bin_trust_function_creators)<br />The [`event_scheduler`](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_event_scheduler) parameter is locked on the replica servers.<br />To update one of the preceding parameters on the source server, delete replica servers, update the parameter value on the source, and recreate replicas. |
| Session level parameters | When configuring session level parameters such as 'foreign_keys_checks' on the read replica, ensure the parameter values you're setting on the read replica are consistent with those of the source server. |
| Adding an AUTO_INCREMENT Primary Key column to the existing table in the source server | We don't recommend altering the table with `AUTO_INCREMENT` after creating a read replica, as this action breaks replication. If you want to add an auto increment column after creating a replica server, consider these approaches:<br />- Create a new table with the same schema as the table you want to modify. In the new table, alter the column with `AUTO_INCREMENT`, and then restore the data from the original table. Drop the old table and rename it in the source; this approach doesn't require deleting the replica server, but it might incur a large insert cost to create a backup table.<br />- Recreate the replica after adding all auto increment columns. |
| Other | - Creating a replica of a replica isn't supported.<br /> - In-memory tables might cause replicas to become out of sync. This limitation is due to the MySQL replication technology. For more information, see the [MySQL reference documentation](https://dev.mysql.com/doc/refman/5.7/en/replication-features-memory.html).<br />- Ensure the source server tables have primary keys. Lack of primary keys might result in replication latency between the source and replicas.<br />- Review the full list of MySQL replication limitations in the [MySQL documentation](https://dev.mysql.com/doc/refman/5.7/en/replication-features.html). |

## Related content

- [Create and manage read replicas by using the Azure portal](how-to-read-replicas-portal.md)
- [Create and manage read replicas by using the Azure CLI](how-to-read-replicas-cli.md)
