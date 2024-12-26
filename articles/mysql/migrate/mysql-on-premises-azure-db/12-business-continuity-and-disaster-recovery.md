---
title: "Migrate MySQL On-Premises to Azure Database for MySQL: Business Continuity and Disaster Recovery (BCDR)"
description: "As with any mission critical system, having a backup and restore and a disaster recovery (BCDR) strategy is an important part of your overall system design."
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 11/27/2024
ms.service: azure-database-mysql
ms.subservice: migration-guide
ms.topic: how-to
---

# Migrate MySQL on-premises to Azure Database for MySQL: Business Continuity and Disaster Recovery (BCDR)

Ensuring business continuity and disaster recovery (BCDR) is critical to migrating MySQL databases from on-premises environments to Azure Database for MySQL. This article delves into the strategies and best practices for maintaining uninterrupted operations and safeguarding data during and after migration. By using Azure's robust BCDR capabilities, you can minimize downtime, protect against data loss, and ensure rapid recovery during a disaster. This guide provides the insights needed to develop a comprehensive BCDR plan, address potential risks, and use Azure's advanced features to enhance resilience and reliability. Whether you aim to improve your disaster recovery capabilities or ensure continuous availability, this article equips you with the knowledge to achieve a seamless and secure migration.

## Prerequisites

[Migrate MySQL on-premises to Azure Database for MySQL: Optimization](11-optimization.md)

## Back up and restore

As with any mission critical system, having a backup and restore and a disaster recovery (BCDR) strategy is an important part of your overall system design. If an unforeseen event occurs, you should have the ability to restore your data to a point in time (Recovery Point Objective) in a reasonable amount of time (Recovery Time Objective).

### Backup

Azure Database for MySQL supports automatic backups for seven days by default. It might be appropriate to modify this to the current maximum of 35 days. It's important to be aware that if the value is changed to 35 days, there are charges for any extra backup storage over 1x of the storage allocated.

There are several current limitations to the database backup feature as described in the [Backup and restore in Azure Database for MySQL](../../concepts-backup.md) docs article. It's important to understand them when deciding what additional strategies that should be implemented.

Some items to be aware of include:

- No direct access to the backups

- Tiers that allow up to 4 TB have a full backup once per week, differential twice a day, and logs every five minutes

- Tiers that allow up to 16 TB have backups that are snapshot-based

    > [!NOTE]  
    > [Some regions](../../concepts-pricing-tiers.md#storage) do not yet support storage up to 16TB.

### Restore

Redundancy (local or geo) must be configured during server creation. However, a geo-restore can be performed and allows the modification of these options during the restore process. Performing a restore operation can temporarily stop connectivity and any applications is down during the restore process.

During a database restore, any supporting items outside of the database need to be restored.  
Review the migration process. See [Perform post-restore tasks](../../concepts-backup.md#perform-post-restore-tasks) for more information.

## Read replicas

[Read replicas](../../concepts-read-replicas.md) can be used to increase the MySQL read throughput, improve performance for regional users and to implement disaster recovery. When creating one or more read replicas, be aware that additional charges are applied for the same compute and storage as the primary server.

## Deleted servers

If an administrator or bad actor deletes the server in the Azure portal or via automated methods, all backups and read replicas are deleted. It's important that [resource locks](/azure/azure-resource-manager/management/lock-resources) are created on the Azure Database for MySQL resource group to add an extra layer of deletion prevention to the instances.

## Regional failure

Although rare, if a regional failure occurs geo-redundant backups or a read replica can be used to get the data workloads running again. It's best to have both geo-replication and a read replica available for the best protection against unexpected regional failures.

> [!NOTE]  
> Changing the database server region also means the endpoint does change and application configurations needs to be updated accordingly.

### Load balancers

If the application is made up of many different instances around the world, it might not be feasible to update all of the clients. Utilize an [Azure Load Balancer](/azure/load-balancer/load-balancer-overview) or [Application Gateway](/azure/application-gateway/overview) to implement a seamless failover functionality. Although helpful and time-saving, these tools aren't required for regional failover capability.

## WWI scenario

WWI wanted to test the failover capabilities of read replicas so they performed the steps outlined below.

### Create a read replica

- Open the Azure portal.

- Browse to the Azure Database for MySQL instance.

- Under **Settings**, select **Replication**.

- Select **Add Replica**.

- Type a server name.

- Select the region.

- Select **OK**, wait for the instance to deploy. Depending on the size of the main instance, it could take some time to replicate.

    > [!NOTE]  
    > Each replica incurs additional charges equal to the main instance.

### Fail over to read replica

Once a read replica has been created and has completed the replication process, it can be used for failed over. Replication stops during a failover and makes the read replica its own main instance.

Failover Steps:

- Open the Azure portal.

- Browse to the Azure Database for MySQL instance.

- Under **Settings**, select **Replication**.

- Select one of the read replicas.

- Select **Stop Replication**. This breaks the read replica.

- Modify all applications connection strings to point to the new main instance.

## BCDR checklist

- Modify backup frequency to meet requirements.

- Setup read replicas for read intensive workloads and regional failover.

- Create resource locks on resource groups.

- Implement a load-balancing strategy for applications for quick failover.

## Next step

> [!div class="nextstepaction"]
> [Migrate MySQL on-premises to Azure Database for MySQL: Security](13-security.md)
