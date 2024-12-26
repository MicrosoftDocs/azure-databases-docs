---
author: abhims14
ms.author: abhishekum
ms.reviewer: randolphwest
ms.date: 09/18/2024
ms.service: azure-database-migration-service
ms.topic: include
ms.collection:
  - sql-migration-content
---

### Migrate databases with Azure SQL Migration extension for Azure Data Studio

The [Azure SQL Migration extension for Azure Data Studio](/azure-data-studio/extensions/azure-sql-migration-extension) brings together a simplified assessment, recommendation, and migration experience that delivers the following capabilities:
- A responsive user interface that provides you with an end-to-end migration experience that starts with a migration readiness assessment, and SKU recommendation (based on performance data), and finalizes with the actual migration to Azure SQL.
- An enhanced assessment mechanism that can evaluate SQL Server instances, identifying databases that are ready for migration to the different Azure SQL targets.
- An SKU recommendations engine (Preview) that collects performance data from the source SQL Server instance on-premises, generating right-sized SKU recommendations based on your Azure SQL target.
- A reliable Azure service powered by Azure Database Migration Service that orchestrates data movement activities to deliver a seamless migration experience.
- The ability to run online (for migrations requiring minimal downtime) or offline (for migrations where downtime persists through the migration) migration modes to suit your business requirements.
- The flexibility to create and configure a self-hosted integration runtime to provide your own compute for accessing the source SQL Server and backups in your on-premises environment.
- Provides a secure and improved user experience for migrating TDE databases and SQL/Windows logins to Azure SQL.

Check the following step-by-step tutorials for more information about each specific migration scenario by Azure SQL target:

| Migration scenario | Migration mode
| --- | --- |
| SQL Server to Azure SQL Managed Instance | [Online](/data-migration/sql-server/managed-instance/database-migration-service) / [Offline](/data-migration/sql-server/managed-instance/database-migration-service) |
| SQL Server to SQL Server on Azure Virtual Machine | [Online](/data-migration/sql-server/virtual-machines/database-migration-service) / [Offline](/data-migration/sql-server/virtual-machines/database-migration-service) |
| SQL Server to Azure SQL Database | [Offline](/data-migration/sql-server/database/database-migration-service) |

To learn more, see [Migrate databases by using the Azure SQL Migration extension for Azure Data Studio](../migration-using-azure-data-studio.md).
