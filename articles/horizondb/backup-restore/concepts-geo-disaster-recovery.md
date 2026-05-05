---
title: Geo-disaster recovery
description: Learn about the concepts of Geo-disaster recovery with an Azure HorizonDB flexible server instance.
author: kabharati
ms.author: kabharati
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.subservice: backup-restore
ms.topic: concept-article
---

# Geo-disaster recovery in Azure HorizonDB

If there's a region-wide disaster, Azure can provide protection from regional or large geography disasters with disaster recovery by making use of another region. For more information on Azure disaster recovery architecture, see [Azure to Azure disaster recovery architecture](/azure/site-recovery/azure-to-azure-architecture).

Azure HorizonDB provides features that protect data and mitigates downtime for your mission-critical databases during planned and unplanned downtime events. Built on top of the Azure infrastructure that offers robust resiliency and availability, Azure HorizonDB offers business continuity features that provide fault-protection, address recovery time requirements, and reduce data loss exposure. As you architect your applications, you should consider the downtime tolerance - the recovery time objective (RTO), and data loss exposure - the recovery point objective (RPO). For example, your business-critical database requires stricter uptime than a test database.

## Read replicas

Cross region read replicas can be deployed to protect your databases from region-level failures. Read replicas are updated asynchronously using an Azure HorizonDB instance's physical replication technology, and can lag the primary. Read replicas are supported in general purpose and memory optimized compute tiers.

For more information on read replica features and considerations, see [Read replicas](/azure/postgresql/flexible-server/concepts-read-replicas).

## Outage detection, notification, and management

If your server is configured with geo-redundant backup, you can perform geo-restore in the paired region. A new server is provisioned and recovered to the last available data that was copied to this region.

You can also use cross region read replicas. In the event of region failure you can perform disaster recovery operation by promoting your read replica to be a standalone read-writeable server. RPO is expected to be up to 5 minutes (data loss possible) except if there's severe regional failure, the RPO can be close to the replication lag at the time of failure.

For more information on unplanned downtime mitigation and recovery after regional disaster, see [Unplanned downtime mitigation](/azure/postgresql/flexible-server/concepts-business-continuity#unplanned-downtime-mitigation).

## Related content

- [Azure HorizonDB documentation](/azure/postgresql/)
- [Reliability in Azure](/azure/reliability/availability-zones-overview)
