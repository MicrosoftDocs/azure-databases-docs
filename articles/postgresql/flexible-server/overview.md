---
title: What Is Azure Database for PostgreSQL flexible server?
description: Provides an overview of Azure Database for PostgreSQL flexible server.
author: gbowerman
ms.author: guybo
ms.reviewer: maghan
ms.date: 07/06/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
---

# What is Azure Database for PostgreSQL?

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article provides an overview and introduction to the core concepts of Azure Database for PostgreSQL flexible server deployment model.
Whether you're just starting out or looking to refresh your knowledge, this introductory video offers a comprehensive overview of Azure Database for PostgreSQL flexible server, helping you get acquainted with its key features and capabilities.

> [!Video https://www.youtube.com/embed/NSEmJfUgNzE?si=8Ku9Z53PP455dICZ&amp;start=121]

Azure Database for PostgreSQL flexible server is a fully managed database service designed to provide more granular control and flexibility over database management functions and configuration settings. The service generally provides more flexibility and server configuration customizations based on user requirements. The flexible server architecture allows users to collocate the database engine with the client tier for lower latency and choose high availability within a single availability zone and across multiple availability zones. Azure Database for PostgreSQL flexible server instances also provides better cost optimization controls with the ability to stop/start your server and a burstable compute tier ideal for workloads that don't need full compute capacity continuously. The service supports various major community versions of PostgreSQL. Please refer to the [Supported PostgreSQL versions in Azure Database for PostgreSQL flexible server](concepts-supported-versions.md) for details on the specific versions supported. The service is available in various [Azure regions](https://azure.microsoft.com/global-infrastructure/services/).

:::image type="content" source="./media/overview/overview-flexible-server.png" alt-text="Diagram of Azure Database for PostgreSQL flexible server - Overview." lightbox="./media/overview/overview-flexible-server.png":::

Azure Database for PostgreSQL flexible server instances are best suited for:

- Application developments requiring better control and customizations.
- Zone redundant high availability.
- Managed maintenance windows.

## Architecture and high availability

The Azure Database for PostgreSQL flexible server deployment model is designed to support high availability within a single availability zone and across multiple availability zones. The architecture separates compute and storage. The database engine runs on a container inside a Linux virtual machine, while data files reside on Azure storage. The storage maintains three locally redundant synchronous copies of the database files, ensuring data durability.

If zone redundant high availability is configured, the service provisions and maintains a warm standby server across the availability zone within the same Azure region. The data changes on the source server are synchronously replicated to the standby server to ensure zero data loss. With zone redundant high availability, once the planned or unplanned failover event is triggered, the standby server comes online immediately and is available to process incoming transactions. This allows the service resiliency from availability zone failure within an Azure region that supports multiple availability zones, as shown in the picture below.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/postgresql/concepts-zone-redundant-high-availability-architecture.png" alt-text="Diagram of Zone redundant high availability." lightbox="~/reusable-content/ce-skilling/azure/media/postgresql/concepts-zone-redundant-high-availability-architecture.png":::

See [High availability]/azure/reliability/reliability-postgresql-flexible-server for more details.

## Automated patching with a managed maintenance window

The service performs automated patching of the underlying hardware, OS, and database engine. The patching includes security and software updates. The planned maintenance release includes minor version upgrades for the PostgreSQL engine. Users can configure the patching schedule to be system-managed or define their custom schedule. During the maintenance schedule, the patch is applied, and the server might need to be restarted as part of the patching process to complete the update. With the custom schedule, users can make their patching cycle predictable and choose a maintenance window with minimum impact on the business. Generally, the service follows a monthly release schedule as part of the continuous integration and release.

## Automatic backups

Azure Database for PostgreSQL flexible server automatically creates server backups and stores them on the region's zone redundant storage (ZRS). Backups can restore your server to any point within the backup retention period. The default backup retention period is seven days. The retention can be optionally configured for up to 35 days. All backups are encrypted using AES 256-bit encryption. See [Backups](concepts-backup-restore.md) for more details.

## Adjust performance and scale within seconds

Azure Database for PostgreSQL flexible server is available in three compute tiers: Burstable, General Purpose, and Memory Optimized. The Burstable tier best suits low-cost development and low concurrency workloads without continuous compute capacity. The General Purpose and Memory Optimized are better suited for production workloads requiring high concurrency, scale, and predictable performance. You can build your first application on a small database for a few dollars a month and then seamlessly adjust the scale to meet the needs of your solution.

## Stop/Start server to lower TCO

Azure Database for PostgreSQL flexible server allows you to stop and start the server on demand to lower your TCO. The compute tier billing stops immediately when the server is stopped. This can allow significant cost savings during development, testing, and time-bound predictable production workloads. The server remains stopped for seven days unless restarted sooner.

## Enterprise-grade security

Azure Database for PostgreSQL flexible server uses the FIPS 140-2 validated cryptographic module for storage encryption of data at rest. Data are encrypted, including backups and temporary files created while running queries. The service uses the AES 256-bit cipher included in Azure storage encryption, and the keys can be system-managed (default). Azure Database for PostgreSQL flexible server encrypts data in motion with default transport layer security (SSL/TLS) enforced by default. The service enforces and supports TLS version 1.2 and above.

Azure Database for PostgreSQL flexible server instances allows full private access to the servers using Azure virtual network (VNet integration). Servers in the Azure virtual network can only be reached and connected through private IP addresses. With VNet integration, public access is denied, and servers can't be reached using public endpoints.

## Monitor and alerting

Azure Database for PostgreSQL flexible server has built-in performance monitoring and alerting features. All Azure metrics have a one-minute frequency, each providing 30 days of history. You can configure alerts on the metrics. The service exposes host server metrics to monitor resource utilization and allows configuring slow query logs. Using these tools, you can quickly optimize your workloads and configure your server for the best performance.

## Built-in PgBouncer

An Azure Database for PostgreSQL flexible server instance has a [built-in PgBouncer](concepts-pgbouncer.md) and a connection pooler. You can enable it and connect your applications to your Azure Database for PostgreSQL flexible server instance via PgBouncer using the same hostname and port 6432. When enabled, PgBouncer is also available for elastic clusters under port 8432.

## Azure regions

One advantage of running your workload in Azure is global reach. Azure Database for PostgreSQL flexible server is currently available in the following Azure regions:

[!INCLUDE [regions-table](includes/regions-table.md)]

$ New Zone-redundant high availability deployments are temporarily blocked in these regions. Already provisioned HA servers are fully supported.

$$ New server deployments are temporarily blocked in these regions. Already provisioned servers are fully supported.

** Zone-redundant high availability can now be deployed when you provision new servers in these regions. Any existing servers deployed in AZ with *no preference* (check this on the Azure portal) before the region started to support AZ, even when you enable zone-redundant HA, the standby is provisioned in the same AZ (same-zone HA) as the primary server. To enable zone-redundant high availability in such cases, read these [special considerations](how-to-configure-high-availability.md#special-considerations).

(*) Certain regions are access-restricted to support specific customer scenarios, such as in-country/region disaster recovery. These regions are available only upon request by creating a new support request.

> [!NOTE]
> If your application requires Zone redundant HA and is unavailable in your preferred Azure region, consider using other regions within the same geography where Zone redundant HA is available, such as US East for US East 2, Central US for North Central US, etc.

## Migration

Azure Database for PostgreSQL flexible server runs the community version of PostgreSQL. This allows full application compatibility and requires a minimal refactoring cost to migrate an existing application developed on the PostgreSQL engine to Azure Database for PostgreSQL flexible server.

- **Azure Database Migration Service** – For seamless and simplified migrations to Azure Database for PostgreSQL flexible server with minimal downtime, Azure Database Migration Service can be used. Visit [What is the migration service in Azure Database for PostgreSQL?](../migrate/migration-service/overview-migration-service-postgresql.md)
- **Dump and Restore** – For offline migrations, where users can afford some downtime, dump and restore using community tools like pg_dump and pg_restore can provide the fastest way to migrate. See [Migrate using dump and restore](../howto-migrate-using-dump-and-restore.md) for details.

## Frequently asked questions (FAQ)

This section addresses common questions about Azure Database for PostgreSQL flexible server, including its features, configurations, and best practices. Whether you're new to the service or looking for specific details, these FAQs provide quick answers to help you get started and optimize your experience.

### What is Microsoft's policy to address PostgreSQL engine defects?

Refer to Microsoft's current policy [here](../../postgresql/flexible-server/concepts-supported-versions.md#managing-postgresql-engine-defects).

## Contacts

If you have any questions or suggestions about Azure Database for PostgreSQL, send an email to the [Azure Database for PostgreSQL team](mailto:AskAzurePostgreSQL@microsoft.com).

> [!NOTE]
> This email address is for general inquiries and suggestions only. It is not a technical support alias.

In addition, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/forums/597976-azure-database-for-postgresql).

## Related content

- [Create an Azure Database for PostgreSQL flexible server](quickstart-create-server.md)
