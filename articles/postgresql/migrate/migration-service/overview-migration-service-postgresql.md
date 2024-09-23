---
title: Miigration service in Azure Database for PostgreSQL?
description: Get an overview of using the migration service to migrate to Azure Database for PostgreSQL - Flexible Server, including advantages and migration options.
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 09/03/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
---

# What is the migration service in Azure Database for PostgreSQL?

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The migration service in Azure Database for PostgreSQL simplifies the process of moving your PostgreSQL databases to Azure. The migration service offers migration options from various PostgreSQL-supported sources, including migrating from a cloud service, an on-premises environment, or a virtual machine. The migration service is designed to help you move your PostgreSQL databases to Azure Database for PostgreSQL - Flexible Server with ease and confidence.

The migration service offers several advantages, including:

- Managed migration service
- Support for schema and data migrations
- No complex setup
- Simple-to-use migration experiences by using the Azure portal or the Azure CLI
- Unlimited database size

The following figure is a visual representation of the PostgreSQL sources you can migrate by using the migration service in Azure Database for PostgreSQL. The figure highlights the diversity of source environments, which include on-premises databases, virtual machines, and cloud-hosted instances, and which can be seamlessly transitioned to Azure Database for PostgreSQL.

:::image type="content" source="media/overview-migration-service-postgresql/migrate-postgresql-sources.png" alt-text="Diagram that shows different PostgreSQL sources." border="false" lightbox="media/overview-migration-service-postgresql/migrate-postgresql-sources.png":::

In the next figure, the detailed steps that are involved in migrating from Azure Database for PostgreSQL - Single Server to Azure Database for PostgreSQL - Flexible Server are depicted. The figure illustrates the migration workflow and key stages of the migration for a successful transition into the Azure Database for PostgreSQL - Flexible Server.

:::image type="content" source="media/overview-migration-service-postgresql/concepts-flow-diagram.png" alt-text="Diagram that depicts the migration from Single Server to Flexible Server." border="false" lightbox="media/overview-migration-service-postgresql/concepts-flow-diagram.png":::

## Why use a flexible server?

Azure Database for PostgreSQL - Flexible Server is the next-generation managed PostgreSQL service in Azure. Azure Database for PostgreSQL powered by the PostgreSQL community edition is available in this deployment mode.

Azure Database for PostgreSQL - Flexible Server provides maximum flexibility over your database and built-in cost-optimizations, and it offers several advantages over peer products:

- [Superior performance](../../flexible-server/overview.md) - Flexible server runs on Linux VM that is best suited to run PostgreSQL engine.

- [Cost savings](../../flexible-server/how-to-deploy-on-azure-free-account.md) – Flexible server allows you to stop and start an on-demand server to lower your TCO. Your compute tier billing is stopped immediately, which allows you to have significant cost savings during development and testing and for time-bound predictable production workloads.

- [Support for new versions of PostgreSQL](../../flexible-server/concepts-supported-versions.md) - Flexible server supports all major PostgreSQL versions beginning with version 11.

- Minimized latency – You can collocate your flexible server in the same availability zone as the application server, resulting in a minimal latency.

- [Connection pooling](../../flexible-server/concepts-pgbouncer.md) - Flexible server has a built-in connection pooling mechanism using **pgBouncer** to support thousands of active connections with low overhead.

- [Server parameters](../../flexible-server/concepts-server-parameters.md) - Flexible server offers a rich set of server parameters for configuration and tuning.

- [Custom maintenance window](../../flexible-server/concepts-maintenance.md) - You can schedule the maintenance window of the flexible server for a specific day and time of the week.

- [High availability](../../flexible-server/concepts-high-availability.md) - Flexible server supports HA within the same availability zone and across availability zones by configuring a warm standby server in sync with the primary.

- [Security](../../flexible-server/concepts-security.md) - Flexible server offers multiple layers of information protection and encryption to protect your data.

- Vector Search + Azure AI Extension - With the integration of Vector Search and Azure AI extension for PostgreSQL, users can perform advanced search operations and use AI-driven insights directly within the database, further enhancing query capabilities and application intelligence.

## Migrate to Azure Database for PostgreSQL flexible server

The options you can consider migrating from the source PostgreSQL instance to the Flexible server are:

**Offline migration**: In an offline migration, all applications that connect to your source instance are stopped, and then the database(s) are copied to a flexible server.

**Online migration**: In an online migration, applications that connect to your source instance aren't stopped while database(s) are copied to a flexible server. The initial copy of the databases is followed by replication to keep the flexible server in sync with the source instance. A cutover is performed when the flexible server completely syncs with the source instance, resulting in minimal downtime.

The following table gives an overview of offline and online options:

| Option | Pros | Cons | Recommended scenarios |
| --- | --- | --- | --- |
| Offline | - Simple, easy, and less complex to execute.<br />- Far fewer chances of failure.<br />- No restrictions regarding database objects it can handle. | Downtime for applications. | - Best for scenarios where simplicity and a high success rate are essential.<br />- Ideal for scenarios where the database can be taken offline without significant impact on business operations.<br />- Suitable for databases when the migration process can be completed within a planned maintenance window. |
| Online | - Very minimal downtime to application.<br />- Ideal for large databases and customers having limited downtime requirements. | - Replication used in online migration has a few [restrictions](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html#pgcopydb-follow) (for example, Primary Keys needed in all tables).<br />- Tough and more complex to execute than offline migration.<br />- Greater chances of failure due to the complexity of migration.<br />- There's an impact on the source instance's storage and computing if the migration runs for a long time. The impact needs to be monitored closely during migration. | - Best suited for businesses where continuity is critical and downtime must be kept to an absolute minimum.<br />- Recommended for databases when the migration process needs to occur without interrupting ongoing operations. |

The following table lists the various sources supported by the migration service.

| PostgreSQL Source Type | Offline Migration | Online Migration |
| --- | --- | --- |
| [Azure Database for PostgreSQL – Single server](../how-to-migrate-single-to-flexible-portal.md) | supported | supported |
| Amazon RDS for PostgreSQL | [supported](tutorial-migration-service-aws-offline.md) | [supported](tutorial-migration-service-aws-online.md) |
| On-premises | [supported](tutorial-migration-service-iaas-offline.md) | [supported](tutorial-migration-service-iaas-online.md) |
| Azure virtual machine(s) | [supported](tutorial-migration-service-iaas-offline.md) | [supported](tutorial-migration-service-iaas-online.md) |
| Amazon Aurora PostgreSQL | [supported](tutorial-migration-service-aurora-offline.md) | [supported](tutorial-migration-service-aurora-online.md) |

:::image type="content" source="media/overview-migration-service-postgresql/migrate-different-sources-option.png" alt-text="Screenshot of the migration setup showing different sources." lightbox="media/overview-migration-service-postgresql/migrate-different-sources-option.png":::

## Advantages of the migration service in Azure Database for PostgreSQL vs. Azure DMS (Classic)

Below are the key benefits of using this service for your PostgreSQL migrations:

- **Fully managed service**: The migration Service in Azure Database for PostgreSQL is a fully managed service, meaning that we handle the complexities of the migration process.
- **Comprehensive migration**: Supports both schema and data migrations, ensuring a complete and accurate transfer of your entire database environment to Azure
- **Ease of setup**: Designed to be user-friendly, eliminating complex setup procedures that can often be a barrier to starting a migration project.
- **No data size constraints**: With the ability to handle databases of any size, the service surpasses the 1-TB data migration limit of Azure DMS (Classic), making it suitable for all types of database migrations.
- **Addressing DMS (Classic) limitations**: The migration service resolves many of the issues and limitations encountered with Azure DMS (Classic), leading to a more reliable migration process.
- **Interface options**: Users can choose between a portal-based interface for an intuitive experience or a command-line interface (CLI) for automation and scripting, accommodating various user preferences.

## Get started

Get started with the migration service by using any of the following methods:

- [Migrate from Azure Database for PostgreSQL - Single Server](tutorial-migration-service-single-to-flexible.md)
- [Migrate from on-premises or IaaS](tutorial-migration-service-iaas.md)
- [Migrate from Amazon RDS for PostgreSQL](tutorial-migration-service-aws.md)

## More information

The migration service for Azure Database for PostgreSQL is a hosted solution. We use a binary called [pgcopydb](https://github.com/dimitri/pgcopydb) to provide a fast and efficient way of copying databases from the source PostgreSQL instance to the target.

## Related content

- [Premigration validations](concepts-premigration-migration-service.md)
- [Migration from Azure Database for PostgreSQL - Single Server](tutorial-migration-service-single-to-flexible.md)
- [Migrate from on-premises and Azure VMs](tutorial-migration-service-iaas.md)
- [Migrate from Amazon RDS for PostgreSQL](tutorial-migration-service-aws.md)
- [Network setup](how-to-network-setup-migration-service.md)
- [Known issues and limitations](concepts-known-issues-migration-service.md)
