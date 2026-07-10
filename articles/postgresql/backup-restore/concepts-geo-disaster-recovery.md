---
title: Geo-Disaster Recovery in Azure Database for PostgreSQL Flexible Server
description: Geo-disaster recovery in Azure Database for PostgreSQL Flexible Server protects your databases from region-wide failures. Explore your options today.
#customer intent: As a user, I want to understand geo-disaster recovery options in Azure Database for PostgreSQL flexible server, so that I can protect my databases from region-wide failures.
author: jjfrost
ms.author: jfrost
ms.reviewer: maghan
ms.date: 07/05/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
ai-usage: ai-assisted
---

# Geo-disaster recovery in Azure Database for PostgreSQL flexible server

If there's a region-wide disaster, Azure can protect you from regional or large geography disasters by using another region for disaster recovery. For more information on resiliency to Azure region outages, see the [Azure reliability documentation](/azure/reliability).

Azure Database for PostgreSQL provides features that protect data and mitigate downtime for your mission-critical databases during planned and unplanned downtime events. Built on top of the Azure infrastructure that offers robust resiliency and availability, Azure Database for PostgreSQL offers business continuity features that provide fault protection, address recovery time requirements, and reduce data loss exposure. As you architect your applications, consider the downtime tolerance - the recovery time objective (RTO), and data loss exposure - the recovery point objective (RPO). For example, your business-critical database requires stricter uptime than a test database.

## Compare geo-replication with geo-redundant backup storage
Both geo-replication with read replicas and geo-backup are solutions for geo-disaster recovery. However, they differ in the details of their offerings. To choose the right solution for your system, understand and compare their features.

| **Feature**                                            | **Geo-replication** | **Geo-backup** |
|--------------------------------------------------------|--------------------|----------------|
| <b> Automatic failover                                 | No                 | No             |
| <b> User must update connection string after failover	 | No                 | Yes            |
| <b> Can be in non-paired region                        | Yes                | No             |
| <b> Supports read scale                                | Yes                | No             |
| <b> Can be configured after the creation of the server | Yes                | No             |
| <b> Restore to specific point in time                  | No                 | No             |
| <b> Capacity guaranteed                                | Yes                | No             |    

## Geo-redundant backup and restore

Geo-redundant backup and restore allows you to restore your server in a different region in the event of a disaster. It also provides at least 99.99999999999999 percent (16 nines) durability of backup objects over a year.

You can configure geo-redundant backup only at the time of server creation. When you configure the server with geo-redundant backup, the backup data and transaction logs are copied to the paired region asynchronously through storage replication.

For more information on geo-redundant backup and restore, see [geo-redundant backup and restore](/azure/postgresql/flexible-server/concepts-backup-restore#geo-redundant-backup-and-restore).

## Read replicas

Deploy cross-region read replicas to protect your databases from region-level failures. Azure Database for PostgreSQL flexible server instances use physical replication technology to update read replicas asynchronously, so they can lag the primary. The general purpose and memory optimized compute tiers support read replicas.

For more information about read replica features and considerations, see [Read replicas](/azure/postgresql/flexible-server/concepts-read-replicas).

## Outage detection, notification, and management

If you configure your server with geo-redundant backup, you can perform geo-restore in the paired region. The process provisions a new server and recovers it to the last available data that was copied to this region.

You can also use cross-region read replicas. In the event of region failure, you can perform disaster recovery operation by promoting your read replica to be a standalone read-writeable server. RPO is expected to be up to five minutes (data loss possible) except if there's severe regional failure, the RPO can be close to the replication lag at the time of failure.

For more information about unplanned downtime mitigation and recovery after regional disaster, see [Unplanned downtime mitigation](/azure/postgresql/flexible-server/concepts-business-continuity#unplanned-downtime-mitigation).

## Related content

- [Azure Database for PostgreSQL documentation](/azure/postgresql/).
- [Reliability in Azure](/azure/reliability/availability-zones-overview).
