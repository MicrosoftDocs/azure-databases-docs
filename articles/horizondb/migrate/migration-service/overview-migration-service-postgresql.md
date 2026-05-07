---
title: Migration Service in Azure HorizonDB
description: Get an introduction to using the migration service to migrate to Azure HorizonDB, including advantages and migration options.
author: avnishrastogimsft
ms.author: avrastog
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: overview
---

# What is the migration service in Azure HorizonDB?

The migration service in Azure HorizonDB simplifies the process of moving your PostgreSQL databases to Azure. The migration service offers migration options from various PostgreSQL-supported sources, including migrating from a cloud service, from an on-premises environment, or from a virtual machine in Azure. The migration service is designed to help you move your PostgreSQL databases to Azure HorizonDB with ease and confidence.

Some of the advantages of using the migration service include:

- Managed migration service
- Support for schema and data migrations
- No complex setup
- Simple-to-use migration experiences by using the Azure portal or the Azure CLI
- Unlimited database size

The following figure shows the PostgreSQL sources you can migrate by using the migration service in Azure HorizonDB. All supported environments can be seamlessly transitioned to Azure HorizonDB.

:::image type="content" source="media/overview-migration-service-postgresql/migrate-postgresql-sources.png" alt-text="Diagram that shows different PostgreSQL sources." lightbox="media/overview-migration-service-postgresql/migrate-postgresql-sources.png":::

The next figure depicts the detailed steps that are involved in migrating from any PostgreSQL source to Azure HorizonDB. The figure illustrates the migration workflow and key stages of the migration for a successful transition to Azure HorizonDB.

:::image type="content" source="media/overview-migration-service-postgresql/concepts-flow-diagram.png" alt-text="Diagram that depicts the migration from Single Server to flexible server." lightbox="media/overview-migration-service-postgresql/concepts-flow-diagram.png":::

## Why use a flexible server?

Azure HorizonDB is the next-generation managed PostgreSQL service in Azure. Azure HorizonDB powered by the PostgreSQL community edition is available in a flexible server deployment.

Azure HorizonDB provides maximum flexibility over your database and built-in cost optimizations. Advantages over peer products include:

- {[What is Azure HorizonDB?](../../overview.md)}: Azure HorizonDB runs on a Linux VM, the VM that's best suited to run the PostgreSQL engine.

- {[Create an Azure HorizonDB database](../../configure-maintain/quickstart-create-server.md)}: You can stop and start Azure HorizonDB on an on-demand server to lower your total cost of operation (TCO). Your compute tier billing is stopped immediately, for significant cost savings during development and testing and for time-bound predictable production workloads.

- {[Supported versions of PostgreSQL in Azure HorizonDB](../../configure-maintain/concepts-supported-versions.md)}: Azure HorizonDB supports all major PostgreSQL versions beginning with version 11.

- Minimized latency: You can collocate your flexible server in the same availability zone as the application server for minimal latency.

- {[PgBouncer in Azure HorizonDB](../../connectivity/concepts-pgbouncer.md)}: Azure HorizonDB has a built-in connection pooling mechanism via the pgBouncer plugin to support thousands of active connections with low overhead.

- {[Parameters in Azure HorizonDB](../../server-parameters/concepts-server-parameters.md)}: Azure HorizonDB offers a rich set of server parameters for configuration and tuning.

- {[Scheduled maintenance in Azure HorizonDB](../../configure-maintain/concepts-maintenance.md)}: You can schedule the maintenance window of the flexible server for a specific day of the week and time.

- **High availability**: Azure HorizonDB supports high availability within the same availability zone and across availability zones by configuring a warm standby server in sync with the primary server.

- {[Secure your Azure HorizonDB](../../security/security-overview.md)}: Azure HorizonDB offers multiple layers of information protection and encryption to protect your data.

- Vector Search and Azure AI Extension: With the integration of Vector Search and Azure AI extension for PostgreSQL, users can perform advanced search operations and use AI-driven insights directly in the database for enhanced query capabilities and application intelligence.

## Migrate to Azure HorizonDB

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
| On-premises | [Migrate offline, from an Azure VM or an on-premises PostgreSQL server to Azure HorizonDB, with the migration service](tutorial-migration-service-iaas-offline.md) | [Migrate online, from an Azure VM or an on-premises PostgreSQL server to Azure HorizonDB, with the migration service](tutorial-migration-service-iaas-online.md) |
| Azure virtual machine | [Migrate offline, from an Azure VM or an on-premises PostgreSQL server to Azure HorizonDB, with the migration service](tutorial-migration-service-iaas-offline.md) | [Migrate online, from an Azure VM or an on-premises PostgreSQL server to Azure HorizonDB, with the migration service](tutorial-migration-service-iaas-online.md) |
| Amazon Aurora PostgreSQL | [Migrate offline, from an Amazon Aurora PostgreSQL to Azure HorizonDB, with the migration service](tutorial-migration-service-aurora-offline.md) | [Migrate online, from an Amazon Aurora PostgreSQL server to Azure HorizonDB, with the migration service](tutorial-migration-service-aurora-online.md) |
| Google Cloud SQL for PostgreSQL | [Migrate offline, from a Google Cloud SQL for PostgreSQL to Azure HorizonDB, with the migration service](tutorial-migration-service-cloud-sql-offline.md) | [Migrate online, from a Google Cloud SQL for PostgreSQL server to Azure HorizonDB, with the migration service](tutorial-migration-service-cloud-sql-online.md) |

:::image type="content" source="media/overview-migration-service-postgresql/migrate-different-sources-option.png" alt-text="Screenshot of the migration setup showing different sources." lightbox="media/overview-migration-service-postgresql/migrate-different-sources-option.png":::

## Advantages of using the migration service vs. Azure Database Migration Service (Classic)

The following list describes the key benefits of using the migration service in Azure HorizonDB for your PostgreSQL migrations:

- **Fully managed service**: The migration service in Azure HorizonDB is a fully managed service. We handle the complexities of the migration process.
- **Comprehensive migration**: Supports both schema and data migrations. A complete and accurate transfer of your entire database environment to Azure.
- **Ease of setup**: Designed to be user-friendly, the service eliminates complex setup procedures that might be a barrier to starting a migration project.
- **No data size constraints**: With the ability to handle databases of any size, the service surpasses the 1-TB data migration limit of Azure Database Migration Service (Classic), so it's suitable for all types of database migrations.
- **Addressing Azure Database Migration Service (Classic) limitations**: The migration service resolves many of the issues and limitations in Azure Database Migration Service (Classic), for a more reliable migration process.
- **Interface options**: You can choose between an Azure portal-based interface for an intuitive experience or a command-line interface (the Azure CLI) for automation and scripting.

## Get started

Get started with the migration service by using one of the following methods:

- {[Migrate from an on-premises or infrastructure as a service (IaaS) environment](/azure/postgresql/migrate/migration-service/tutorial-migration-service-iaas-offline)}
- {[Migrate from Amazon RDS for PostgreSQL](/azure/postgresql/migrate/migration-service/tutorial-migration-service-aws-offline)}

## Get more information

The migration service for Azure HorizonDB is a hosted solution. It uses a binary called [pgcopydb](https://github.com/dimitri/pgcopydb) to quickly and efficiently copy databases from your source PostgreSQL instance to Azure.

## Related content

- [Premigration validation for the migrations service in Azure HorizonDB](concepts-premigration-migration-service.md)
- [Migrate from on-premises and Azure VMs](/azure/postgresql/migrate/migration-service/tutorial-migration-service-iaas-offline)
