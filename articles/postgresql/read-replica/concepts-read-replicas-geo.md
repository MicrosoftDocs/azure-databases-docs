---
title: Geo-replication in Azure Database for PostgreSQL Flexible Server
description: This article describes the Geo-replication in an Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to understand how geo-replication works in Azure Database for PostgreSQL flexible server, so that I can plan a disaster recovery strategy for my applications.
author: gkasar
ms.author: gkasar
ms.reviewer: maghan
ms.date: 07/13/2026
ms.service: azure-database-postgresql
ms.subservice: replication
ms.topic: concept-article
---

# Geo-replication in Azure Database for PostgreSQL flexible server

You can create a read replica in the same region as the primary server or in a different geographical region. Geo-replication is helpful for scenarios like disaster recovery planning or bringing data closer to your users.

You can have a primary server in any [Azure Database for PostgreSQL flexible server service region](https://azure.microsoft.com/global-infrastructure/services/?products=postgresql). A primary server can also have replicas in any global region of Azure that supports Azure Database for PostgreSQL flexible server. Additionally, the service supports regions in the [Azure Government](/azure/azure-government/documentation-government-welcome) and [Microsoft Azure operated by 21Vianet](/azure/china/overview-operations) sovereign clouds.


## Paired regions for disaster recovery purposes

You can create replicas in any supported region, but you get notable benefits when you choose replicas in [paired Azure regions](/azure/reliability/regions-paired), especially when you architect for disaster recovery purposes:

- **Region Recovery Sequence**: In a geography-wide outage, recovery of one region from every paired set is prioritized. This priority ensures that applications across paired regions always have a region expedited for recovery.

- **Sequential Updating**: Paired regions' updates are staggered chronologically, which minimizes the risk of downtime from update-related issues.

- **Data Residency**: With a few exceptions, regions in a paired set reside within the same geography, so they meet data residency requirements.

- **Performance**: While paired regions typically offer low network latency, which enhances data accessibility and user experience, they might not always be the regions with the absolute lowest latency. If the primary objective is to serve data closer to users rather than prioritize disaster recovery, evaluate all available regions for latency. In some cases, a non-paired region might exhibit the lowest latency. For a comprehensive understanding, you can reference [Azure's round-trip latency figures](/azure/networking/azure-network-latency#round-trip-latency-figures) to make an informed choice.

For a deeper understanding of the advantages of paired regions, refer to [Azure's documentation on cross-region replication](/azure/reliability/cross-region-replication-azure#azure-paired-regions).


## Regional failures and recovery

Azure facilities across various regions are designed to be highly reliable. However, under rare circumstances, an entire region can become inaccessible due to reasons ranging from network failures to severe scenarios like natural disasters. Azure's capabilities allow you to create applications that are distributed across multiple regions, ensuring that a failure in one region doesn't affect others.

### Prepare for regional disasters

Being prepared for potential regional disasters is critical to ensure the uninterrupted operation of your applications and services. If you're considering a robust contingency plan for your Azure Database for PostgreSQL flexible server, consider these key steps and considerations:

1.  **Establish a geo-replicated read replica**: Set up a read replica in a separate region from your primary. This setup ensures continuity in case the primary region faces an outage. 
1.  **Ensure server symmetry**: The most recommended action for handling regional outages is **promote to primary server**, but it comes with a [server symmetry](concepts-read-replicas.md#configuration-management) requirement. This requirement means both the primary and replica servers must have identical configurations of specific settings. The advantages of using this action include:
     * No need to modify application connection strings if you use [virtual endpoints](concepts-read-replicas-virtual-endpoints.md).
     * It provides a seamless recovery process where, once the affected region is back online, the original primary server automatically resumes its function, but in a new replica role.
1.  **Set up virtual endpoints**: Virtual endpoints allow for a smooth transition of your application to another region if there's an outage. They eliminate the need for any changes in the connection strings of your application.
1.  **Configure the read replica**: Not all settings from the primary server are replicated over to the read replica. Ensure that you appropriately set up all necessary configurations and features (for example, PgBouncer) on your read replica. For more information, see the [Configuration management](concepts-read-replicas-promote.md#configuration-management) section.
1.  **Prepare for high availability (HA)**: If your setup requires high availability, it isn't automatically enabled on a promoted replica. Be ready to activate it post-promotion. Consider automating this step to minimize downtime.
1.  **Regular testing**: Regularly simulate regional disaster scenarios to validate existing thresholds, targets, and configurations. Ensure that your application responds as expected during these test scenarios.
1.  **Follow Azure's general guidance**: Azure provides comprehensive guidance on [reliability and disaster preparedness](/azure/reliability/overview). Consult these resources and integrate best practices into your preparedness plan.

Being proactive and preparing in advance for regional disasters ensures the resilience and reliability of your applications and data.

### When outages impact your SLA

If a prolonged outage occurs with an Azure Database for PostgreSQL flexible server in a specific region that threatens your application's service-level agreement (SLA), be aware that both the actions discussed in the following section aren't service-driven. Both actions require user intervention. Automate the entire process as much as possible and have robust monitoring in place. For more information about what information is provided during an outage, see the [Service outage](../backup-restore/concepts-business-continuity.md#service-outage) page. Only a **forced** promote is possible in a region down scenario, meaning the amount of data loss is roughly equal to the current lag between the replica and primary. Hence, it's crucial to [monitor the lag](concepts-read-replicas.md#monitor-replication). Consider the following options:

**Promote to primary server**

This option doesn't require updating the connection strings in your application, provided you configure virtual endpoints. Once activated, the writer endpoint repoints to the new primary in a different region and the [replication state](concepts-read-replicas.md#monitor-replication) column in the Azure portal displays "Reconfiguring". Once the affected region is restored, the former primary server automatically resumes, but now in a replica role.

**Promote to independent server and remove from replication**

In some cases, this option might be the only viable option. After promoting the server, update your application's connection strings. Once the original region is restored, the old primary might become active again. Ensure to remove it to avoid incurring unnecessary costs. If you wish to maintain the previous topology, recreate the read replica.

## Related content

- [Read replicas in Azure Database for PostgreSQL](concepts-read-replicas.md).
- [Promote read replicas in Azure Database for PostgreSQL](concepts-read-replicas-promote.md).
- [Virtual endpoints for read replicas in Azure Database for PostgreSQL](concepts-read-replicas-virtual-endpoints.md).
- [Create a read replica](how-to-create-read-replica.md).
- [Replication across Azure regions and virtual networks with private networking](../network/concepts-networking-private.md#replication-across-azure-regions-and-virtual-networks-with-private-networking).
