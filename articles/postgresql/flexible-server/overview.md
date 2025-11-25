---
title: What Is Azure Database for PostgreSQL?
description: Provides an overview of Azure Database for PostgreSQL.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 10/30/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
---

# What is Azure Database for PostgreSQL?

This article provides an overview of Azure Database for PostgreSQL, helping you get acquainted with its key features and core concepts.

Azure Database for PostgreSQL is a fully managed database service designed to give you granular control and flexibility over database management functions and configuration settings. The service provides flexibility and server configuration customizations based on your requirements. The architecture lets you collocate the database engine with the client tier for lower latency and choose high availability within a single availability zone and across multiple availability zones. Azure Database for PostgreSQL flexible server instance also provides cost optimization controls with the ability to stop and start your server and a burstable compute tier that's ideal for workloads that don't need full compute capacity continuously. The service supports various major community versions of PostgreSQL. For details on the specific versions supported, see [Supported versions of PostgreSQL in Azure Database for PostgreSQL](concepts-supported-versions.md). The service is available in various [Azure regions](https://azure.microsoft.com/global-infrastructure/services/).

:::image type="content" source="./media/overview/overview-flexible-server.png" alt-text="Diagram of Azure Database for PostgreSQL - Overview." lightbox="./media/overview/overview-flexible-server.png":::

Azure Database for PostgreSQL is best suited for:

- Application developments requiring control and customizations.
- Zone redundant high availability.
- Managed maintenance windows.

## Architecture and high availability

The Azure Database for PostgreSQL deployment model is designed to support high availability within a single availability zone and across multiple availability zones. The architecture separates compute and storage. The database engine runs on a container inside a Linux virtual machine, while data files reside on Azure storage. The storage maintains three locally redundant synchronous copies of the database files, ensuring data durability.

If you configure zone redundant high availability, the service provisions and maintains a warm standby server across the availability zone within the same Azure region. The data changes on the source server are synchronously replicated to the standby server to ensure zero data loss. With zone redundant high availability, once the planned or unplanned failover event is triggered, the standby server comes online immediately and is available to process incoming transactions. This feature allows the service resiliency from availability zone failure within an Azure region that supports multiple availability zones, as shown in the following picture.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/postgresql/concepts-zone-redundant-high-availability-architecture.png" alt-text="Diagram of Zone redundant high availability." lightbox="~/reusable-content/ce-skilling/azure/media/postgresql/concepts-zone-redundant-high-availability-architecture.png":::

See [High availability](/azure/reliability/reliability-postgresql-flexible-server) for more details.

## Automated patching with a managed maintenance window

The service performs automated patching of the underlying hardware, OS, and database engine. The patching includes security and software updates. The planned maintenance release includes minor version upgrades for the PostgreSQL engine. You can configure the patching schedule to be system-managed or define your custom schedule. During the maintenance schedule, the patch is applied, and the server might need to be restarted as part of the patching process to complete the update. With the custom schedule, you can make your patching cycle predictable and choose a maintenance window with minimum impact on your business. Generally, the service follows a monthly release schedule as part of the continuous integration and release.

## Automatic backups

Azure Database for PostgreSQL automatically creates server backups and stores them on the region's zone redundant storage (ZRS). You can restore your server to any point within the backup retention period. The default backup retention period is seven days. You can optionally configure the retention for up to 35 days. All backups are encrypted by using AES 256-bit encryption. For more information, see [Backups](concepts-backup-restore.md).

## Adjust performance and scale within seconds

Azure Database for PostgreSQL is available in three compute tiers: Burstable, General Purpose, and Memory Optimized. The Burstable tier is best for low-cost development and low concurrency workloads without continuous compute capacity. The General Purpose and Memory Optimized tiers are better for production workloads that require high concurrency, scale, and predictable performance. You can build your first application on a small database for a few dollars a month, then seamlessly adjust the scale to meet the needs of your solution.

## Stop and start server to lower TCO

Azure Database for PostgreSQL allows you to stop and start the server on demand to lower your TCO. The compute tier billing stops immediately when you stop the server. This feature can provide significant cost savings during development, testing, and time-bound predictable production workloads. The server remains stopped for seven days unless you restart it sooner.

## Enterprise-grade security

Azure Database for PostgreSQL uses the FIPS 140-2 validated cryptographic module for storage encryption of data at rest. The service encrypts data, including backups and temporary files created while running queries. It uses the AES 256-bit cipher included in Azure storage encryption, and the keys can be system-managed (default). Azure Database for PostgreSQL encrypts data in motion with default transport layer security (SSL/TLS) enforced by default. The service enforces and supports TLS version 1.2 and later.

Azure Database for PostgreSQL flexible server instance allows full private access to the servers by using Azure virtual network. Servers in the Azure virtual network can only be reached and connected through private IP addresses. With virtual network integration, public access is denied, and servers can't be reached by using public endpoints.

## Monitor and alerting

Azure Database for PostgreSQL has built-in performance monitoring and alerting features. All Azure metrics have a one-minute frequency, each providing 30 days of history. You can configure alerts on the metrics. The service exposes host server metrics to monitor resource utilization and allows configuring slow query logs. Using these tools, you can quickly optimize your workloads and configure your server for the best performance.

## Built-in PgBouncer

An Azure Database for PostgreSQL flexible server instance has a [built-in PgBouncer](concepts-pgbouncer.md) and a connection pooler. You can enable it and connect your applications to your Azure Database for PostgreSQL flexible server instance through PgBouncer by using the same hostname and port 6432. When enabled, PgBouncer is also available for elastic clusters under port 8432.

## Azure regions

One advantage of running your workload in Azure is global reach. Azure Database for PostgreSQL is currently available in the following Azure regions:

[!INCLUDE [regions-table](includes/regions-table.md)]

$ New zone-redundant high availability deployments are temporarily blocked in these regions. The service fully supports already provisioned HA servers.

$ New server deployments are temporarily blocked in these regions. The service fully supports already provisioned servers.

** You can now deploy zone-redundant high availability when you provision new servers in these regions. For existing servers deployed in AZ with *no preference* (check this on the Azure portal) before the region started to support AZ, even when you enable zone-redundant HA, the standby is provisioned in the same AZ (same-zone HA) as the primary server. To enable zone-redundant high availability in such cases, see these [special considerations](how-to-configure-high-availability.md#limitations-and-considerations).

(*) Certain regions are access-restricted to support specific customer scenarios, such as in-country/region disaster recovery. You can access these regions only upon request by creating a new support request.

> [!NOTE]  
> If your application requires zone-redundant high availability and it's unavailable in your preferred Azure region, consider using other regions within the same geography where zone-redundant HA is available, such as US East for US East 2, Central US for North Central US, and so on.

## V6 SKU Family limitations

- Scaling from V6 SKU family to Burstable tier isn't supported.
- Scaling from Burstable to V6 SKU family isn't supported.
- Virtual Network integration isn't supported.

## Migration

Azure Database for PostgreSQL runs the community version of PostgreSQL. This version provides full application compatibility and requires minimal refactoring to migrate an existing application developed on the PostgreSQL engine to Azure Database for PostgreSQL.

- **Azure Database Migration Service** – For seamless and simplified migrations to Azure Database for PostgreSQL with minimal downtime, use Azure Database Migration Service. Visit [What is the migration service in Azure Database for PostgreSQL?](../migrate/migration-service/overview-migration-service-postgresql.md)
- **Dump and Restore** – For offline migrations where you can afford some downtime, dump, and restore using community tools like pg_dump and pg_restore provides the fastest way to migrate. See [Migrate using dump and restore](../howto-migrate-using-dump-and-restore.md) for details.

## Feedback and support

If you have questions or suggestions about Azure Database for PostgreSQL, you can get help and support through the following channels:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/forums/597976-azure-database-for-postgresql).

## Related content

- [Create an Azure Database for PostgreSQL](quickstart-create-server.md)
