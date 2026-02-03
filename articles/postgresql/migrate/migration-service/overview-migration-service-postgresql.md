---
title: "Migration Service in Azure Database for PostgreSQL"
description: Get an introduction to using the migration service to migrate to Azure Database for PostgreSQL flexible server, including advantages and migration options.
author: hariramt
ms.author: hariramt
ms.reviewer: maghan
ms.date: 02/07/2025
ms.service: azure-database-postgresql
ms.topic: overview
---

# What is the migration service in Azure Database for PostgreSQL?

The migration service in Azure Database for PostgreSQL simplifies the process of moving your PostgreSQL databases to Azure. The migration service offers migration options from various PostgreSQL-supported sources, including migrating from a cloud service, from an on-premises environment, or from a virtual machine in Azure. The migration service is designed to help you move your PostgreSQL databases to Azure Database for PostgreSQL flexible server with ease and confidence.

Some of the advantages of using the migration service include:

- Managed migration service
- Support for schema and data migrations
- No complex setup
- Simple-to-use migration experiences by using the Azure portal or the Azure CLI
- Unlimited database size

The following figure shows the PostgreSQL sources you can migrate by using the migration service in Azure Database for PostgreSQL. All supported environments can be seamlessly transitioned to Azure Database for PostgreSQL.

:::image type="content" source="media/overview-migration-service-postgresql/migrate-postgresql-sources.png" alt-text="Diagram that shows different PostgreSQL sources." lightbox="media/overview-migration-service-postgresql/migrate-postgresql-sources.png":::

The next figure depicts the detailed steps that are involved in migrating from any PostgreSQL source to Azure Database for PostgreSQL flexible server. The figure illustrates the migration workflow and key stages of the migration for a successful transition to Azure Database for PostgreSQL flexible server.

:::image type="content" source="media/overview-migration-service-postgresql/concepts-flow-diagram.png" alt-text="Diagram that depicts the migration from Single Server to flexible server." lightbox="media/overview-migration-service-postgresql/concepts-flow-diagram.png":::

## Why use a flexible server?

Azure Database for PostgreSQL flexible server is the next-generation managed PostgreSQL service in Azure. Azure Database for PostgreSQL powered by the PostgreSQL community edition is available in a flexible server deployment.

Azure Database for PostgreSQL flexible server provides maximum flexibility over your database and built-in cost optimizations. Advantages over peer products include:

- [Superior performance](../../flexible-server/overview.md): Azure Database for PostgreSQL flexible server runs on a Linux VM, the VM that's best suited to run the PostgreSQL engine.

- [Cost savings](../../flexible-server/how-to-deploy-on-azure-free-account.md): You can stop and start Azure Database for PostgreSQL flexible server on an on-demand server to lower your total cost of operation (TCO). Your compute tier billing is stopped immediately, for significant cost savings during development and testing and for time-bound predictable production workloads.

- [Support for new versions of PostgreSQL](../../flexible-server/concepts-supported-versions.md): Azure Database for PostgreSQL flexible server supports all major PostgreSQL versions beginning with version 11.

- Minimized latency: You can collocate your flexible server in the same availability zone as the application server for minimal latency.

- [Connection pooling](../../flexible-server/concepts-pgbouncer.md): Azure Database for PostgreSQL flexible server has a built-in connection pooling mechanism via the pgBouncer plugin to support thousands of active connections with low overhead.

- [Server parameters](../../flexible-server/concepts-server-parameters.md): Azure Database for PostgreSQL flexible server offers a rich set of server parameters for configuration and tuning.

- [Custom maintenance window](../../flexible-server/concepts-maintenance.md): You can schedule the maintenance window of the flexible server for a specific day of the week and time.

- [High availability](../../flexible-server/concepts-high-availability.md): Azure Database for PostgreSQL flexible server supports high availability within the same availability zone and across availability zones by configuring a warm standby server in sync with the primary server.

- [Security](../../flexible-server/concepts-security.md): Azure Database for PostgreSQL flexible server offers multiple layers of information protection and encryption to protect your data.

- Vector Search and Azure AI Extension: With the integration of Vector Search and Azure AI extension for PostgreSQL, users can perform advanced search operations and use AI-driven insights directly in the database for enhanced query capabilities and application intelligence.

## Migrate to Azure Database for PostgreSQL flexible server

You can choose from the following options to migrate from a source PostgreSQL server to a flexible server:

**Offline migration**: In an offline migration, all applications that connect to your source instance are stopped. Then, databases are copied to a flexible server.

**Online migration**: In an online migration, applications that connect to your source server aren't stopped while databases are copied to a flexible server. The initial database copy is followed by replication to keep the flexible server in sync with the source instance. A cutover is performed and the flexible server completely syncs with the source instance, resulting in minimal downtime.

The following table describes offline and online options:

| Option | Advantages | Considerations | Recommended scenarios |
| --- | --- | --- | --- |
| Offline | - Simple, easy, and less complex to execute.<br />- Far fewer chances of failure.<br />- No restrictions on the number of database objects it can handle. | - Downtime for applications. | - Best for scenarios in which simplicity and a high success rate are essential.<br />- Ideal when a database can be taken offline without significant impact on business operations.<br />- Suitable when databases can be migrated within a planned maintenance window. |
| Online | - Very minimal downtime for your application.<br />- Ideal for large databases and for customers who have requirements for limited downtime. | - Replication used in online migration has a few [restrictions](https://pgcopydb.readthedocs.io/en/latest/ref/pgcopydb_follow.html#pgcopydb-follow). For example, primary keys are required in all tables.<br />- More complex to execute than offline migration.<br />- Greater chances of failure due to the complexity of the migration process.<br />- There's an impact on the source instance storage and computing if the migration runs for a long time. The impact needs to be monitored closely during migration. | - Best suited for businesses where continuity is critical and downtime must be kept to an absolute minimum.<br />- Recommended when database migration needs to occur without interrupting ongoing operations. |

The following table lists the sources that the migration service supports:

| PostgreSQL source type | Offline migration | Online migration |
| --- | --- | --- |
| Amazon RDS for PostgreSQL | [Supported](tutorial-migration-service-aws-offline.md) | [Supported](tutorial-migration-service-aws-online.md) |
| On-premises | [Supported](tutorial-migration-service-iaas-offline.md) | [Supported](tutorial-migration-service-iaas-online.md) |
| Azure virtual machine | [Supported](tutorial-migration-service-iaas-offline.md) | [Supported](tutorial-migration-service-iaas-online.md) |
| Amazon Aurora PostgreSQL | [Supported](tutorial-migration-service-aurora-offline.md) | [Supported](tutorial-migration-service-aurora-online.md) |
| Google Cloud SQL for PostgreSQL | [Supported](tutorial-migration-service-cloud-sql-offline.md) | [Supported](tutorial-migration-service-cloud-sql-online.md) |

:::image type="content" source="media/overview-migration-service-postgresql/migrate-different-sources-option.png" alt-text="Screenshot of the migration setup showing different sources." lightbox="media/overview-migration-service-postgresql/migrate-different-sources-option.png":::

## Advantages of using the migration service vs. Azure Database Migration Service (Classic)

The following list describes the key benefits of using the migration service in Azure Database for PostgreSQL for your PostgreSQL migrations:

- **Fully managed service**: The migration service in Azure Database for PostgreSQL is a fully managed service. We handle the complexities of the migration process.
- **Comprehensive migration**: Supports both schema and data migrations. A complete and accurate transfer of your entire database environment to Azure.
- **Ease of setup**: Designed to be user-friendly, the service eliminates complex setup procedures that might be a barrier to starting a migration project.
- **No data size constraints**: With the ability to handle databases of any size, the service surpasses the 1-TB data migration limit of Azure Database Migration Service (Classic), so it's suitable for all types of database migrations.
- **Addressing Azure Database Migration Service (Classic) limitations**: The migration service resolves many of the issues and limitations in Azure Database Migration Service (Classic), for a more reliable migration process.
- **Interface options**: You can choose between an Azure portal-based interface for an intuitive experience or a command-line interface (the Azure CLI) for automation and scripting.

## Get started

Get started with the migration service by using one of the following methods:

- [Migrate from an on-premises or infrastructure as a service (IaaS) environment](tutorial-migration-service-iaas.md)
- [Migrate from Amazon RDS for PostgreSQL](tutorial-migration-service-aws.md)

## Get more information

The migration service for Azure Database for PostgreSQL is a hosted solution. It uses a binary called [pgcopydb](https://github.com/dimitri/pgcopydb) to quickly and efficiently copy databases from your source PostgreSQL instance to Azure.

## Related content

- [Premigration validations](concepts-premigration-migration-service.md)
- [Migrate from on-premises and Azure VMs](tutorial-migration-service-iaas.md)
