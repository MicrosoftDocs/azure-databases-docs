---
title: "What's Happening to Azure Database for PostgreSQL Single Server?"
description: The Azure Database for PostgreSQL single server service is being deprecated.
author: markingmyname
ms.author: maghan
ms.reviewer: guybo
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.subservice: single-server
ms.topic: concept-article
ms.custom:
  - single server deprecation announcement
---

# What happens to Azure Database for PostgreSQL - Single Server after the retirement announcement?

**Azure Database for PostgreSQL - Single Server is on the retirement path and is scheduled to retire by March 28, 2025.

Azure Database for PostgreSQL – Single Server generally became available in 2018. Given customer feedback and new advancements in the Azure database landscape's computation, availability, scalability, and performance capabilities, the Single Server offering needs to be retired and upgraded with a new architecture. Azure Database for PostgreSQL - Flexible Server is the next generation of the service and brings you the best Azure open-source database platform.

As part of this retirement, we'll no longer support creating new single server instances from the Azure portal beginning November 30, 2023. However, if you need to create single server instances to meet business continuity needs, you can continue to use Azure CLI until March 2025.

If you currently have an Azure Database for PostgreSQL - Single Server service hosting production servers, we're glad to inform you that you can migrate your Azure Database for PostgreSQL - Single Server to the Azure Database for PostgreSQL - Flexible Server.

Azure Database for PostgreSQL - Flexible Server is a fully managed production-ready database service designed for more granular control and flexibility over database management functions and configuration settings. For more information about it, visit **[Azure Database for PostgreSQL - Flexible Server](../flexible-server/overview.md)**.

## Migrate from Azure Database for PostgreSQL - Single Server to Azure Database for PostgreSQL - Flexible Server

Learn how to migrate from Azure Database for PostgreSQL - Single Server to Azure Database for PostgreSQL - Flexible Server using the [PostgreSQL migration service](../migrate/concepts-single-to-flexible.md).

You can also use Automigration to migrate to Flexible server by nominating the Single server(s) that you want to migrate automatically. [Automigration](./automigration-single-to-flexible-postgresql.md) leverages the [Azure PostgreSQL migration service](./migration-service/overview-migration-service-postgresql.md) to deliver a resilient offline migration during a planned migration window.

## Frequently Asked Questions (FAQs)

**Q. Why is Azure Database for PostgreSQL- Single Server being retired?**

**A.** Azure Database for PostgreSQL – Single Server generally became available in 2018. Given customer feedback and new advancements in the Azure database landscape's computation, availability, scalability, and performance capabilities, the Single Server offering needs to be retired and upgraded with a new architecture. Azure Database for PostgreSQL - Flexible Server is the next generation of the service and brings you the best Azure open-source database platform.

**Q. Why am I being asked to migrate to Azure Database for PostgreSQL - Flexible Server?**

**A.** [Azure Database for PostgreSQL - Flexible Server](/azure/postgresql/flexible-server/overview) is the best platform for running all your open-source PostgreSQL workloads on Azure. Azure Database for PostgreSQL - Flexible Server is economical, provides better performance across all service tiers, and provides more ways to control your costs for cheaper and faster disaster recovery. Other improvements to the flexible server include:

- Support for Postgres version 11 and newer, plus built-in security enhancements
- Better price performance with support for burstable tier compute options.
- Improved uptime by configuring hot standby on the same or a different availability zone and user-controlled maintenance windows.
- A simplified developer experience for high-performance data workloads.

**Q. How soon must I migrate my Single Server to a Flexible Server?**

**A.** Azure Database for PostgreSQL - Single Server is scheduled for retirement by March 28, 2025, so we strongly recommend migrating your Single Server to a Flexible Server at the earliest opportunity to ensure ample time to run through the migration lifecycle and use the benefits offered by the Flexible Server.

**Q. What happens to my existing Azure Database for PostgreSQL - Single Server instances?**

**A.** Your existing Azure Database for PostgreSQL - Single Server workloads are supported until **March 2025**.

**Q. Can I still create a new version 11 Azure Database for PostgreSQL - Single Server after the community EOL date in November 2023?**

**A.** Beginning November 30, 2023, you'll no longer be able to create new single server instances for PostgreSQL version 11 through the Azure portal. However, you can still [make them via CLI until March 2025](https://azure.microsoft.com/updates/singlepg11-retirement/). We support single servers through our [versioning support policy.](../flexible-server/concepts-version-policy.md). It would be best to start migrating to Azure Database for PostgreSQL - Flexible Server immediately.

**Q. Can I continue running my Azure Database for PostgreSQL - Single Server beyond the sunset date of March 28, 2025?**

**A.** We plan to support Single Server until the sunset date of March 28, 2025, and we strongly advise that you start planning your migration as soon as possible. We plan to end support for Single Server deployments at the sunset date of **March 28, 2025**.

**Q. What happens if I do not migrate or my server is not auto migrated by March 28th, 2025??​**

**A.** Azure Database for PostgreSQL Single Server will be retired on 28 March 2025. To prevent disruptions or service loss, you must migrate to Azure Database for PostgreSQL Flexible Server before this date.

**Key Changes**:
- Starting 29 March 2025, you will no longer be able to create new Single Server instances.

- Existing Single Server instances will be automatically migrated to the comparable Flexible Server in a phased manner—regardless of downtime requirements or application compatibility.

- Single Servers using the following features will **NOT** be automatically migrated and will be deleted in a phased manner, resulting in data loss:
  - **Customer Managed Keys(CMK)**
  - **Deny Public Access** set to **Yes**

To avoid service disruptions, please plan your migration as soon as possible.

**Q. After the Single Server retirement announcement, what if I still need to create a new single server to meet my business needs?**

**A.** We aren't stopping the ability to create new single servers immediately, so you can continue to create new single servers through CLI to meet your business needs for all PostgreSQL versions supported on Azure Database for PostgreSQL – Single Server. We strongly encourage you to explore Flexible Server and see if that will meet your needs. Don't hesitate to contact us if necessary so we can guide you and suggest the best path forward.

**Q. Are there any additional costs associated with performing the migration?**

**A.** You pay for the target flexible server and the source single server during the migration. The configuration and computing of the target flexible server will determine the extra costs incurred (see [Pricing](https://azure.microsoft.com/pricing/details/postgresql/flexible-server/) for more details). Once you've decommissioned the source single server after a successful migration, you only pay for your flexible server. Using the Single Server to Flexible Server migration service doesn't cost extra. If you have questions or concerns about the cost of migrating your single server to a flexible server, contact your Microsoft account representative.

**Q. Will my billing be affected by running Azure Database for PostgreSQL - Flexible Server instead of Azure Database for PostgreSQL - Single Server?**

**A.** The billing should be comparable if you choose a similar configuration to your Azure Database for PostgreSQL - Single Server. However, if you select the same zone or zone redundant with high availability for the target flexible server, your bill will be higher than on your single server. Same zone or zone redundant high availability requires an additional hot standby server to be spun up and store redundant backup data, hence the added cost for the second server. This architecture enables reduced downtime during unplanned outages and planned maintenance. Generally speaking, Flexible Server provides better price performance, however, this depends on your workload.

**Q. Will I incur downtime when I migrate my Azure Database from PostgreSQL - Single Server to a Flexible Server?**

**A.** The PostgreSQL migration service supports offline and online migrations. Offline migration requires downtime to your applications during the migration process. Online migration helps you migrate databases with limited downtime but few restrictions. For more information, see [PostgreSQL migration service - Azure Database for PostgreSQL Single Server to Flexible Server](../migrate/concepts-single-to-flexible.md).

Downtime depends on several factors, including the number and size of your databases, the number of tables inside each database, the number of indexes, and the distribution of data across tables. It also depends on the SKU of the source and target server and the IOPS available on the source and target server.

Given the many factors involved in a migration, the best approach to estimate downtime to your application is to try the migration on a PITR server restored from the primary server to plan for your production migration.

Offline migrations are less complex and have few chances of failure. They're the recommended way to migrate workloads with service windows from a single server to a flexible server. Online migration can be used for production environments with low downtime tolerance.

**Q. Will there be future updates to Single Server to support the latest PostgreSQL versions?**

**A.** We recommend you migrate to Flexible Server if you must run on the latest PostgreSQL engine versions. We continue to deploy minor versions released by the community for Postgres version 11 until it's retired by the community in Nov'2023.

> [!NOTE]  
> We're extending support for Postgres version 11 past the community retirement date and will support PostgreSQL version 11 on both [Single Server](https://azure.microsoft.com/updates/singlepg11-retirement/) and [Flexible Server](https://azure.microsoft.com/updates/flexpg11-retirement/) to ease this transition. Consider migrating to Flexible Server to use the benefits of the latest Postgres engine versions.

**Q. How does the Flexible Server 99.99% availability SLA differ from the Single Server?**

**A.** Flexible Server zone-redundant deployment provides 99.99% availability with zonal-level resiliency, and Single Server delivers 99.99% availability but without zonal resiliency. Flexible Server High Availability (HA) architecture deploys a hot standby server with redundant compute and storage (with each site's data stored in 3x copies). A Single Server HA architecture doesn't have a passive hot standby to help recover from zonal failures. Flexible Server HA architecture reduces downtime during unplanned outages and planned maintenance.

**Q. My Single Server is deployed in a region that doesn't support Flexible Server. How should I proceed with migration?**

**A.** We're close to regional parity with a Single Server. These are the regions with no Flexible Server presence.

- China East (CE and CE2),
- China North (CN and CN2)
- West India
- Sweden Central

We recommend migrating to CN3/CE3, Central India, Sweden Central, and Sweden South regions.
**Q. I have a private link configured for my single server. How do I migrate?**

**A.** Private Link support is now available on Flexible Server. You can use the runtime server to move to a Flexible server with Private link support. For more information, see [Runtime server - Azure Database for PostgreSQL Single Server to Flexible Server](../migrate/migration-service/concepts-migration-service-runtime-server.md).

**Q. Is there an option to roll back Single Server to a Flexible Server migration?**

**A.** You can perform any number of test migrations, test the success of your migration, and perform the final migration once you're ready. Test migrations don't affect the single server source, which remains operational until you migrate and change your connection strings to point to the Flexible server. If there are any errors during the test migration, you can postpone the final migration and keep your source server running. You can then reattempt the final migration after you resolve the errors. After you've performed a final migration to a flexible server and opened it up for the production workload, you'll lose the ability to go back to Single Server without incurring a data loss.

**Q. How should I migrate my DB (> 1TB)**

**A.** [The PostgreSQL migration service](../migrate/concepts-single-to-flexible.md) can migrate databases of all sizes from a Single Server to a Flexible Server. The migration service has no restrictions regarding the size of the databases.

**Q. Is cross-region migration supported?**

**A.** Yes.

**Q. Is cross-subscription migration supported?**

**A.** The PostgreSQL migration service supports cross-subscription migrations.

**Q. Is cross-resource group subscription-supported?**

**A.** The PostgreSQL migration service supports cross-resource group migrations.

**Q. Is there cross-version support?**

**A.** The PostgreSQL migration service supports migrating from a lower PostgreSQL version (PG 9.5 and above) to any higher version. As always, application compatibility with higher PostgreSQL versions should be checked beforehand.

### PostgreSQL migration service

The [The PostgreSQL migration service](/azure/postgresql/migrate/concepts-single-to-flexible)is a powerful service that allows you to easily migrate your PostgreSQL Server database from a single server to a flexible server. With this service, you can easily move your database from an on-premises server or a virtual machine to a flexible server in the cloud, allowing you to take advantage of the scalability and flexibility of cloud computing.

**Q. Which data, schema, and metadata components are migrated as part of the migration?**

**A.** The PostgreSQL migration service migrates schema, data, and metadata from the source to the destination. All the following data, schema, and metadata components are migrated as part of the database migration:

Data Migration

- All tables from all databases/schemas.

- Schema Migration:
    - Naming
    - Primary key
    - Data type
    - Ordinal position
    - Default value
    - Nullability
    - Autoincrement attributes
    - Secondary indexes

- Metadata Migration:
    - Stored Procedures
    - Functions
    - Triggers
    - Views
    - Foreign key constraints

**Q. What's the difference between offline and online migration?**

**A.** With an offline migration, application downtime starts when the migration begins. With an online migration, downtime is limited to the time required to cut over at the end of migration. However, it uses a logical replication mechanism that is subject to a few [restrictions](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html#pgcopydb-follow).

The following table gives an overview of offline and online options.

| Option | PROs | CONs | Recommended For |
| --- | --- | --- | --- |
| Offline | - Simple, easy, and less complex to execute.<br />- Very few chances of failure.<br />- No restrictions regarding database objects it can handle | Downtime to applications. | - Best for scenarios where simplicity and a high success rate are essential.<br />- Ideal for scenarios where the database can be offline without significantly affecting business operations.<br />- Suitable for databases when the migration process can be completed within a planned maintenance window. |
| Online | - Very minimal downtime to application.<br />- Ideal for large databases and customers having limited downtime requirements. | - Replication used in online migration has a few [restrictions](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html#pgcopydb-follow) (for example, Primary Keys needed in all tables).<br />- Tough and more complex to execute than offline migration.<br />- Greater chances of failure due to the complexity of migration.<br />- There's an impact on the source instance's storage and computing if the migration runs for a long time. The impact needs to be monitored closely during migration. | - Best suited for businesses where continuity is critical and downtime must be minimal.<br />- Recommended for databases when the migration process needs to occur without interrupting ongoing operations. |

**Q. Are there any recommendations for optimizing the performance of the Single Server to Flexible Server migration?**

**A.** Yes. To perform faster migrations, pick a higher SKU for your flexible server. Pick a minimum of 4VCore or higher to complete the migration quickly. You can always change the SKU to match the application needs post-migration. [Check out more best practices](../migrate/migration-service/best-practices-migration-service-postgresql.md).

**Q. How long does performing an offline migration from the Single Server to Flexible Server take with the migration service?**

**A.** The following table shows the time spent performing offline migrations for databases of various sizes using the PostgreSQL migration service. The migration was performed using a flexible server with the SKU:

**Standard_D4ds_v4(4 cores, 16GB Memory and 500 IOPS)**

| Database Size | Time (HH:MM) |
| --- | --- |
| 1 GB | 00:01 |
| 5 GB | 00:03 |
| 10 GB | 00:08 |
| 50 GB | 00:35 |
| 100 GB | 01:00 |
| 500 GB | 04:00 |
| 1,000 GB | 07:00 |

> [!NOTE]  
> The numbers above approximate the time taken to complete the migration. To get the precise time required to migrate to your server, we strongly recommend taking a PITR (point in time restore) of your single server and migrating it with the PostgreSQL migration service.

**Q. How long does performing an online migration from Single Server to Flexible Server take with the migration service?**

**A.** Online migration involves the following steps:

1. Initial copy of databases
1. Change data capture - Replaying all the transactions on the source during step #1 to the target.

The time taken in step #1 is the same as for offline migrations (refer to the previous question).

The time taken for step #2 depends on the transactions that occur on the source. If it's a write-intensive workload, it's longer.

**Q. Is there any support offered by Microsoft for moving from Single Server to Flexible Server?**

**A.** Yes. In addition to continuously updating the migration service, we work with internal partner teams that can engage with you throughout the migration process. Contact your account representative for more information.

**Q. Can Microsoft help me migrate my Single server to Flexible server automatically?**
**A.** Yes. You can nominate your servers for **Auto migration**. You can read more about it and nominate your servers for Automigration [here](../migrate/automigration-single-to-flexible-postgresql.md).

### Additional support

**Q. I have further questions about retirement.**

**A.** You can get further information in a few different ways.
- Gett answers from community experts in [Microsoft Q&A](/answers/tags/214/azure-database-postgresql).

- If you have a support plan and you need technical help, create a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest):
    - For Summary, type a description of your issue.
    - For Issue type, select Technical.
    - For Subscription, select your subscription.
    - For Service, select My services.
    - For Service type, select Azure Database for PostgreSQL single server.
    - For Resource, select your resource.
    - For Problem type, select Migrating to Azure DB for PostgreSQL.
    - For Problem subtype, select migrating from single to flexible server.

> [!WARNING]  
> This article is not for Azure Database for PostgreSQL - Flexible Server users. It is for Azure Database for PostgreSQL - Single Server customers who need to upgrade to Azure Database for PostgreSQL - Flexible Server.

We know migrating services can be frustrating, and we apologize in advance for any inconvenience this might cause you. You can choose what scenario best works for you and your environment.

## Related content

- [PostgreSQL migration service](../migrate/concepts-single-to-flexible.md)
- [What is flexible server?](../flexible-server/overview.md)
