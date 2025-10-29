---
title: Azure Database Migration Service Tools Matrix
description: Learn about the services and tools available to migrate databases and to support various phases of the migration process.
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 10/28/2025
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

| Source | Target | Discover /<br />Inventory | Target and SKU<br />recommendation |
| --- | --- | --- | --- |
| SQL Server | Azure SQL Database | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Cloudamize*](https://cloudamize.com/) | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) |
| SQL Server | Azure SQL Managed Instance | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Cloudamize*](https://cloudamize.com/) | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) |
| SQL Server | SQL Server on Azure Virtual Machine | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Cloudamize*](https://cloudamize.com/) | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) |
| SQL Server | Azure Synapse Analytics | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Cloudamize*](https://cloudamize.com/) | |
| Amazon RDS for SQL Server | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)<br />[Azure SQL Migration extension](migration-using-azure-data-studio.md) |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[MigVisor*](https://solutionshub.epam.com/solution/migvisor-by-epam) |
| Oracle | Azure Synapse Analytics | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Oracle | Azure Database for PostgreSQL flexible server | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | |
| MongoDB | Azure Cosmos DB | [Cloudamize*](https://cloudamize.com/) | [Cloudamize*](https://cloudamize.com/) |
| Cassandra | Azure Cosmos DB | | |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/) |
| MySQL | Azure Database for MySQL | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | |
| Amazon RDS for MySQL | Azure Database for MySQL | | |
| PostgreSQL | Azure Database for PostgreSQL flexible server | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | |
| Amazon RDS for PostgreSQL | Azure Database for PostgreSQL flexible server | | |
| DB2 | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Access | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Sybase - SAP ASE | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Sybase - SAP IQ | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | | |

## Premigration phase

| Source | Target | App Data Access<br />Layer Assessment | Database<br />Assessment | Performance<br />Assessment |
| --- | --- | --- | --- | --- |
| SQL Server | Azure SQL Database | | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) | [Cloudamize*](https://cloudamize.com/) |
| SQL Server | Azure SQL Managed Instance | | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) | [Cloudamize*](https://cloudamize.com/) |
| SQL Server | SQL Server on Azure VM | | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) | [Cloudamize*](https://cloudamize.com/) |
| SQL Server | Azure Synapse Analytics | | | |
| Amazon RDS for SQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | | [Azure SQL Migration extension](migration-using-azure-data-studio.md) | |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Oracle | Azure Synapse Analytics | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | |
| Oracle | Azure Database for PostgreSQL flexible server | | [Ora2Pg*](https://ora2pg.darold.net/start.html) | |
| MongoDB | Azure Cosmos DB | | [Cloudamize*](https://cloudamize.com/) | [Cloudamize*](https://cloudamize.com/) |
| Cassandra | Azure Cosmos DB | | | |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/) | |
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

## Migration phase

| Source | Target | Schema | Data<br />(Offline) | Data<br />(Online) |
| --- | --- | --- | --- | --- |
| SQL Server | Azure SQL Database | [SQL Database Projects extension](/azure-data-studio/extensions/sql-database-project-extension)<br />[Cloudamize*](https://cloudamize.com/) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/) | [Cloudamize*](https://cloudamize.com/)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| SQL Server | Azure SQL Managed Instance | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| SQL Server | SQL Server on Azure VM | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Cloudamize*](https://cloudamize.com/)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| SQL Server | Azure Synapse Analytics | | | |
| Amazon RDS for SQL Server | Azure SQL Database | [SQL Database Projects extension](/azure-data-studio/extensions/sql-database-project-extension) | [Azure SQL Migration extension](migration-using-azure-data-studio.md) | [Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Amazon RDS for SQL | Azure SQL Managed Instance | [Azure SQL Migration extension](migration-using-azure-data-studio.md) | [Azure SQL Migration extension](migration-using-azure-data-studio.md) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Amazon RDS for SQL Server | SQL Server on Azure VM | [Azure SQL Migration extension](migration-using-azure-data-studio.md) | [Azure SQL Migration extension](migration-using-azure-data-studio.md) | [Azure SQL Migration extension](migration-using-azure-data-studio.md)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[SharePlex*](https://www.quest.com/products/shareplex/)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[SharePlex*](https://www.quest.com/products/shareplex/)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SharePlex*](https://www.quest.com/products/shareplex/)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Oracle | Azure Synapse Analytics | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SharePlex*](https://www.quest.com/products/shareplex/)<br />[Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Oracle | Azure Database for PostgreSQL flexible server | [Ora2Pg*](https://ora2pg.darold.net/start.html)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [Ora2Pg*](https://ora2pg.darold.net/start.html)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) |<br />[Striim*](https://www.striim.com/microsoft-azure) |
| MongoDB | Azure Cosmos DB | [DMS](https://azure.microsoft.com/services/database-migration/)<br />[Cloudamize*](https://cloudamize.com/)<br />[Imanis Data*](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview) | [DMS](https://azure.microsoft.com/services/database-migration/)<br />[Cloudamize*](https://cloudamize.com/)<br />[Imanis Data*](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview) | [DMS](https://azure.microsoft.com/services/database-migration/)<br />[Cloudamize*](https://cloudamize.com/)<br />[Imanis Data*](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Cassandra | Azure Cosmos DB | [Imanis Data*](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview) | [Imanis Data*](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview) | [Imanis Data*](https://marketplace.microsoft.com/product/azure-applications/talena-inc.talena-solution-template?tab=Overview) |
| MySQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| MySQL | Azure Database for MySQL | [DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />[MySQL dump*](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html) | [DMS](tutorial-mysql-azure-mysql-offline-portal.md) | [DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />[MyDumper/MyLoader*](https://centminmod.com/mydumper.html) with [data-in replication](../mysql/concepts-data-in-replication.md) |
| Amazon RDS for MySQL | Azure Database for MySQL | [DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />[MySQL dump*](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html) | [DMS](tutorial-mysql-azure-mysql-offline-portal.md) | [DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />[MyDumper/MyLoader*](https://centminmod.com/mydumper.html) with [data-in replication](../mysql/concepts-data-in-replication.md) |
| Amazon Aurora MySQL | Azure Database for MySQL | [DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />[MySQL dump*](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html) | [DMS](tutorial-mysql-azure-mysql-offline-portal.md) | [DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />[MyDumper/MyLoader*](https://centminmod.com/mydumper.html) with [data-in replication](../mysql/concepts-data-in-replication.md) |
| Google Cloud SQL for MySQL | Azure Database for MySQL | [DMS](concepts-migrate-azure-mysql-schema-migration.md)<br />[MySQL dump*](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html) | [DMS](tutorial-mysql-azure-mysql-offline-portal.md) | [DMS](tutorial-mysql-azure-external-to-flex-online-portal.md)<br />[MyDumper/MyLoader*](https://centminmod.com/mydumper.html) with [data-in replication](../mysql/concepts-data-in-replication.md) |
| PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-iaas-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-iaas-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-iaas-online.md) |
| Amazon RDS for PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-rds-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-rds-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-rds-online.md) |
| Google Cloud SQL for PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-cloud-sql-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-cloud-sql-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-cloud-sql-online.md) |
| Amazon Aurora PostgreSQL | Azure Database for PostgreSQL flexible server | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-aurora-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-aurora-offline.md) | [Migration Service for Azure Database for PostgreSQL](../postgresql/migrate/migration-service/tutorial-migration-service-aurora-online.md) |
| DB2 | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Access | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) | [SSMA](/sql/ssma/sql-server-migration-assistant) |
| Sybase - SAP ASE | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [SSMA](/sql/ssma/sql-server-migration-assistant)<br />[Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [Qlik*](https://www.qlik.com/us/products/qlik-replicate)<br />[Striim*](https://www.striim.com/microsoft-azure) |
| Sybase - SAP IQ | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | [Ispirer*](https://www.ispirer.com/products/migration-to-azure) | [Ispirer*](https://www.ispirer.com/products/migration-to-azure) | |

## Post-migration phase

| Source | Target | Optimize |
| --- | --- | --- |
| SQL Server | Azure SQL Database | [Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) |
| SQL Server | Azure SQL Managed Instance | [Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) |
| SQL Server | SQL Server on Azure VM | [Cloud Atlas*](https://www.unifycloud.com/cloud-migration-tool/)<br />[Cloudamize*](https://cloudamize.com/) |
| SQL Server | Azure Synapse Analytics | |
| RDS SQL | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Oracle | Azure SQL Database, Azure SQL Managed Instance, SQL Server on Azure VM | |
| Oracle | Azure Synapse Analytics | |
| Oracle | Azure Database for PostgreSQL -<br />Single server | |
| MongoDB | Azure Cosmos DB | [Cloudamize*](https://cloudamize.com/) |
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

## Related content

- [What is Azure Database Migration Service?](dms-overview.md)
