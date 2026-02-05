---
title: Azure Database Migration Service Tools Matrix
description: Learn about the services and tools available to migrate databases and to support various phases of the migration process.
author: rwestMSFT
ms.author: randolphwest
ms.reviewer: abhishekum
ms.date: 02/19/2026
ms.service: azure-database-migration-service
ms.topic: reference
ms.collection:
  - sql-migration-content
ms.custom:
  - mvc
---

# Services and tools available for data migration scenarios

This article provides a matrix of the Microsoft and third-party services and tools available to assist you with various database and data migration scenarios and specialty tasks.

The following tables identify the services and tools you can use to plan for data migration and complete its various phases successfully.

> [!NOTE]  
> In the following tables, items marked with an asterisk (`*`) represent third-party tools.

## Business justification phase

| Source | Target | Discover / inventory | Target and SKU recommendation |
| --- | --- | --- | --- |
| SQL Server | Azure SQL Database | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />-&nbsp;[Cloud&nbsp;Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | Azure SQL Managed Instance | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />- [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | SQL Server on Azure Virtual Machine | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />-&nbsp;[Cloud&nbsp;Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | Azure Synapse Analytics | - [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | |
| Amazon RDS for SQL Server | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [MigVisor](https://solutionshub.epam.com/solution/migvisor-by-epam)<sup>1</sup> |
| Oracle | Azure Synapse Analytics | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Oracle | Azure Database for PostgreSQL flexible server | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | |
| MongoDB | Azure Cosmos DB | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| Cassandra | Azure Cosmos DB | | |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup> |
| MySQL | Azure Database for MySQL | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | |
| Amazon RDS for MySQL | Azure Database for MySQL | | |
| PostgreSQL | Azure Database for PostgreSQL flexible server | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | |
| Amazon RDS for PostgreSQL | Azure Database for PostgreSQL flexible server | | |
| DB2 | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Access | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Sybase - SAP ASE | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Sybase - SAP IQ | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | | |

<sup>1</sup> This is a non-Microsoft product or service, provided by a third-party.

## Premigration phase

| Source | Target | App data access layer assessment | Database assessment | Performance assessment |
| --- | --- | --- | --- | --- |
| SQL Server | Azure SQL Database | | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | Azure SQL Managed Instance | | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | SQL Server on Azure VM | | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migration-overview)<br />- [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | Azure Synapse Analytics | | | |
| Amazon RDS for SQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | | [Azure portal](/data-migration) | |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Oracle | Azure Synapse Analytics | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Oracle | Azure Database for PostgreSQL flexible server | | [Ora2Pg](https://ora2pg.darold.net/start.html)<sup>1</sup> | |
| MongoDB | Azure Cosmos DB | | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| Cassandra | Azure Cosmos DB | | | |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup> | |
| MySQL | Azure Database for MySQL | | | |
| Amazon RDS for MySQL | Azure Database for MySQL | | | |
| PostgreSQL | Azure Database for PostgreSQL flexible server | | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/concepts-premigration-migration-service.md) | |
| Amazon RDS for PostgreSQL | Azure Database for PostgreSQL flexible server | | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/concepts-premigration-migration-service.md) | |
| Amazon Aurora PostgreSQL | Azure Database for PostgreSQL flexible server | | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/concepts-premigration-migration-service.md) | |
| Google Cloud SQL for PostgreSQL | Azure Database for PostgreSQL flexible server | | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/concepts-premigration-migration-service.md) | |
| DB2 | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Access | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Sybase - SAP ASE | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Sybase - SAP IQ | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | | | |

<sup>1</sup> This is a non-Microsoft product or service, provided by a third-party.

## Migration phase

| Source | Target | Schema | Offline data | Online data |
| --- | --- | --- | --- | --- |
| SQL Server | Azure SQL Database | - [SQL Database Projects extension](/sql/tools/visual-studio-code-extensions/sql-database-projects/getting-started-sql-database-projects-extension)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | - [Cloudamize](https://cloudamize.com/)<sup>1</sup><br />- [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| SQL Server | Azure SQL Managed Instance | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | - [SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migrate-to-azure-sql-managed-instance)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup><br />- [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| SQL Server | SQL Server on Azure VM | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | [Cloudamize](https://cloudamize.com/)<sup>1</sup> | - [Cloudamize](https://cloudamize.com/)<sup>1</sup><br />- [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| SQL Server | Azure Synapse Analytics | | | |
| Amazon RDS for SQL Server | Azure SQL Database | [SQL Database Projects extension](/sql/tools/visual-studio-code-extensions/sql-database-projects/getting-started-sql-database-projects-extension) | [Azure portal](/azure/azure-sql/migration-guides/database/sql-server-to-sql-database-overview) | - [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Amazon RDS for SQL | Azure SQL Managed Instance | [Azure portal](/azure/azure-sql/migration-guides/managed-instance/sql-server-to-managed-instance-overview) | [Azure portal](/azure/azure-sql/migration-guides/managed-instance/sql-server-to-managed-instance-overview) | [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Amazon RDS for SQL Server | SQL Server on Azure VM | [Azure portal](/azure/azure-sql/migration-guides/virtual-machines/sql-server-to-sql-on-azure-vm-individual-databases-guide) | [Azure portal](/azure/azure-sql/migration-guides/virtual-machines/sql-server-to-sql-on-azure-vm-individual-databases-guide) | - [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [SharePlex](https://www.quest.com/products/shareplex/)<sup>1</sup><br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [SharePlex](https://www.quest.com/products/shareplex/)<sup>1</sup><br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SharePlex](https://www.quest.com/products/shareplex/)<sup>1</sup><br />- [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Oracle | Azure Synapse Analytics | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SharePlex](https://www.quest.com/products/shareplex/)<sup>1</sup><br />- [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Oracle | Azure Database for PostgreSQL flexible server | - [Ora2Pg](https://ora2pg.darold.net/start.html)<sup>1</sup><br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [Ora2Pg](https://ora2pg.darold.net/start.html)<sup>1</sup><br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| MongoDB | Azure Cosmos DB | - [Azure DMS](https://azure.microsoft.com/services/database-migration/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup><br />- [Imanis Data](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<sup>1</sup> | - [Azure DMS](https://azure.microsoft.com/services/database-migration/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup><br />- [Imanis Data](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<sup>1</sup> | - [Azure DMS](https://azure.microsoft.com/services/database-migration/)<br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup><br />- [Imanis Data](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Cassandra | Azure Cosmos DB | [Imanis Data](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<sup>1</sup> | [Imanis Data](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<sup>1</sup> | [Imanis Data](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<sup>1</sup> |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| MySQL | Azure Database for MySQL | - [Azure DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />- [MySQL dump](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html)<sup>1</sup> | [Azure DMS](tutorial-mysql-azure-mysql-offline-portal.md) | - [Azure DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />- [MyDumper/MyLoader](https://centminmod.com/mydumper.html)<sup>1</sup> with [data-in replication](../mysql/concepts-data-in-replication.md) |
| Amazon RDS for MySQL | Azure Database for MySQL | - [Azure DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />- [MySQL dump](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html)<sup>1</sup> | [Azure DMS](tutorial-mysql-azure-mysql-offline-portal.md) | - [Azure DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />- [MyDumper/MyLoader](https://centminmod.com/mydumper.html)<sup>1</sup> with [data-in replication](../mysql/concepts-data-in-replication.md) |
| Amazon Aurora MySQL | Azure Database for MySQL | - [Azure DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />- [MySQL dump](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html)<sup>1</sup> | [Azure DMS](tutorial-mysql-azure-mysql-offline-portal.md) | - [Azure DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />- [MyDumper/MyLoader](https://centminmod.com/mydumper.html)<sup>1</sup> with [data-in replication](../mysql/concepts-data-in-replication.md) |
| Google Cloud SQL for MySQL | Azure Database for MySQL | - [Azure DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />- [MySQL dump](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html)<sup>1</sup> | [Azure DMS](tutorial-mysql-azure-mysql-offline-portal.md) | - [Azure DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />- [MyDumper/MyLoader](https://centminmod.com/mydumper.html)<sup>1</sup> with [data-in replication](../mysql/concepts-data-in-replication.md) |
| PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-iaas-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-iaas-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-iaas-online.md) |
| Amazon RDS for PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-rds-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-rds-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-rds-online.md) |
| Google Cloud SQL for PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-cloud-sql-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-cloud-sql-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-cloud-sql-online.md) |
| Amazon Aurora PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-aurora-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-aurora-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-aurora-online.md) |
| DB2 | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Access | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Sybase - SAP ASE | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [SSMA](/sql/ssma/sql-server-migration-assistant)<br />- [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | - [Qlik](https://www.qlik.com/us/products/qlik-replicate)<sup>1</sup><br />- [Striim](https://www.striim.com/microsoft-azure)<sup>1</sup> |
| Sybase - SAP IQ | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | [Ispirer](https://www.ispirer.com/products/migration-to-azure)<sup>1</sup> | |

<sup>1</sup> This is a non-Microsoft product or service, provided by a third-party.

## Post-migration phase

| Source | Target | Optimize |
| --- | --- | --- |
| SQL Server | Azure SQL Database | - [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | Azure SQL Managed Instance | - [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | SQL Server on Azure VM | - [Cloud Atlas](https://www.unifycloud.com/cloud-migration-tool/)<sup>1</sup><br />- [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| SQL Server | Azure Synapse Analytics | |
| RDS SQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Oracle | Azure Synapse Analytics | |
| Oracle | Azure Database for PostgreSQL -<br />- Single server | |
| MongoDB | Azure Cosmos DB | [Cloudamize](https://cloudamize.com/)<sup>1</sup> |
| Cassandra | Azure Cosmos DB | |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| MySQL | Azure Database for MySQL | |
| Amazon RDS for MySQL | Azure Database for MySQL | |
| PostgreSQL | Azure Database for PostgreSQL flexible server | |
| Amazon RDS for PostgreSQL | Azure Database for PostgreSQL flexible server | |
| DB2 | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Access | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Sybase - SAP ASE | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Sybase - SAP IQ | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |

<sup>1</sup> This is a non-Microsoft product or service, provided by a third-party.

## Related content

- [What is Azure Database Migration Service?](dms-overview.md)
