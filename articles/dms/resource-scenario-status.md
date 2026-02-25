---
title: Supported Database Migration Scenarios
titleSuffix: Azure Database Migration Service
description: Learn which migration scenarios are currently supported for Azure Database Migration Service and their availability status.
author: rwestMSFT
ms.author: randolphwest
ms.reviewer: abhishekum
ms.date: 02/19/2026
ms.service: azure-database-migration-service
ms.topic: troubleshooting
ms.collection:
  - sql-migration-content
ms.custom:
  - mvc
---

# Azure Database Migration Service supported scenarios

Azure Database Migration Service (Azure DMS) supports a mix of database migration scenarios (source and target pairs) for both offline (one-time) and online (continuous sync) database migrations. New scenarios are added over time to extend Database Migration Service scenario coverage. This article lists the migration scenarios currently supported by Database Migration Service and their availability status, which is *preview* or *generally available*.

## Offline vs. online migration

In Database Migration Service, you can migrate your databases offline or while they're online. In an *offline* migration, application downtime starts when the migration starts. To limit downtime to the time it takes you to cut over to the new environment after the migration, use an *online* migration. We recommend that you test an offline migration to determine whether the downtime is acceptable. If the expected downtime isn't acceptable, do an online migration.

## Migration scenario status

The status of migration scenarios supported by Database Migration Service varies over time. Generally, scenarios are first released in *preview*. In preview, Database Migration Service users can try out migration scenarios directly in the UI. No sign-up is required. Migration scenarios that have a preview release status might not be available in all regions, and they might be revised before final release.

After preview, the scenario status changes to *general availability* (GA). GA is the final release status. Scenarios that have a status of GA have complete functionality and are accessible to all users.

## Supported migration scenarios

The tables in the following sections show the status of specific migration scenarios that are supported in Database Migration Service.

### Offline (one-time) migration support

The following table describes the current status of Database Migration Service (DMS) support for *offline* migrations:

| Target | Source | Support | Status |
| --- | --- | :---: | :---: |
| **Azure SQL Database** | SQL Server <sup>1</sup> | Yes [using DMS] | GA |
| | Amazon RDS SQL Server | Yes [using DMS] | GA |
| | Oracle | Yes [using DMS via SSMA] | Preview |
| **Azure SQL Database Managed Instance** | SQL Server <sup>1</sup> | Yes [using DMS] | GA |
| | Amazon RDS SQL Server | Yes [using DMS] | GA |
| | Oracle | Yes [using DMS via SSMA] | Preview |
| **Azure SQL VM** | SQL Server <sup>1</sup> | Yes [using DMS] | GA |
| | Amazon RDS SQL Server | Yes [using DMS] | GA |
| | Oracle | Yes [using DMS via SSMA] | Preview |
| **Azure Cosmos DB** | MongoDB | Yes | GA |
| **Azure Database for MySQL - Flexible Server** | MySQL | Yes | GA |
| | Amazon RDS MySQL | Yes | GA |
| | Amazon Aurora MySQL | Yes | GA |
| | Google Cloud SQL for MySQL | Yes | GA |
| | Percona MySQL | Yes | GA |
| | Azure Database for MySQL <sup>2</sup> | Yes | GA |
| **Azure Database for PostgreSQL flexible server** | PostgreSQL | No | |
| | Amazon RDS PostgreSQL | No | |

<sup>1</sup> Offline migrations by using Azure DMS are supported for Azure SQL Managed Instance, SQL Server on Azure Virtual Machines, and Azure SQL Database.

<sup>2</sup> If your source database is already in an Azure platform as a service (PaaS) like Azure Database for MySQL or Azure Database for PostgreSQL, choose the corresponding engine when you create your migration activity. For example, if you're migrating from Azure Database for MySQL - Flexible Server to another Azure Database for MySQL - Flexible Server, choose MySQL as the source engine when you create your scenario. If you're migrating from Amazon RDS for PostgreSQL to Azure Database for PostgreSQL flexible server, choose PostgreSQL as the source engine when you create your scenario.

### Online (continuous sync) migration support

The following table describes the current status of Database Migration Service (DMS) support for *online* migrations:

| Target | Source | Support | Status |
| --- | --- | :---: | :---: |
| **Azure SQL Database** | SQL Server <sup>1</sup> | No | |
| | Amazon RDS SQL | No | |
| | Oracle | No | |
| **Azure SQL Database MI** | SQL Server <sup>1</sup> | Yes [using DMS] | GA |
| | Amazon RDS SQL | Yes [using DMS] | GA |
| | Oracle | No | |
| **Azure SQL VM** | SQL Server <sup>1</sup> | Yes [using DMS] | GA |
| | Amazon RDS SQL | Yes [using DMS] | GA |
| | Oracle | No | |
| **Azure Cosmos DB** | MongoDB | Yes | GA |
| **Azure Database for MySQL - Flexible Server** | MySQL | Yes | GA |
| | Amazon RDS MySQL | Yes | GA |
| | Amazon Aurora MySQL | Yes | GA |
| | Google Cloud SQL for MySQL | Yes | GA |
| | Percona MySQL | Yes | GA |
| | Azure Database for MySQL <sup>2</sup> | Yes | GA |
| **Azure Database for PostgreSQL flexible server** | PostgreSQL | Yes | GA |
| | Amazon RDS PostgreSQL | Yes | GA |

<sup>1</sup> Online migrations (minimal downtime) by using Azure DMS are supported for Azure SQL Managed Instance and SQL Server on Azure Virtual Machines targets.

<sup>2</sup> If your source database is already in an Azure PaaS like Azure Database for MySQL or Azure Database for PostgreSQL, choose the corresponding engine when you create your migration activity. For example, if you're migrating from Azure Database for MySQL - Flexible Server to another Azure Database for MySQL - Flexible Server, choose MySQL as the source engine when you create the scenario. If you're migrating from Amazon RDS for PostgreSQL to Azure Database for PostgreSQL flexible server, choose PostgreSQL as the source engine when you create the scenario.

## Related content

- [What is Azure Database Migration Service?](dms-overview.md)
