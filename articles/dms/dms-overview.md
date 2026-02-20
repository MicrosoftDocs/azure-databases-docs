---
title: What Is Azure Database Migration Service?
description: Overview of Azure Database Migration Service, which provides seamless migrations from many database sources to Azure Data platforms.
author: rwestMSFT
ms.author: randolphwest
ms.reviewer: abhishekum
ms.date: 02/19/2026
ms.service: azure-database-migration-service
ms.topic: overview
ms.collection:
  - sql-migration-content
---
# What is Azure Database Migration Service?

Azure Database Migration Service (Azure DMS) is a fully managed service designed to enable seamless migrations from multiple database sources to Azure data platforms with minimal downtime (online migrations).

Azure DMS is available through the [Azure portal](https://portal.azure.com/#create/Microsoft.AzureDMS), [PowerShell](https://github.com/Azure-Samples/data-migration-sql/tree/main/PowerShell), and [Azure CLI](https://github.com/Azure-Samples/data-migration-sql/tree/main/CLI).

Currently, it supports SQL Database modernization to Azure. For improved functionality and supportability, consider migrating to Azure SQL Database by using DMS.

## Tracking resource

Azure DMS provides a capability to create a free and optional SQL Server instance Azure resource to improve your migration tracking experience. Specify the SQL Server instance name and subscription, resource group, and location where you want to create the tracking resource. You must register your subscription to the `Microsoft.AzureArcData` resource provider to create the Azure resource. We attempt to register your subscription to the resource provider if your subscription isn't already registered to it.

## Compare versions

The following table compares the functionality of the versions of Azure DMS:

| Feature | DMS (Azure portal) | Notes |
| --- | --- | --- |
| Assessment | No | Assess compatibility of the source. |
| SKU recommendation | No | SKU recommendations for the target based on the assessment of the source. |
| Azure SQL Database - Offline migration | Yes | Migrate to Azure SQL Database offline. |
| Azure SQL Managed Instance - Online migration | Yes | Migrate to Azure SQL Managed Instance online with minimal downtime. |
| Azure SQL Managed Instance - Offline migration | Yes | Migrate to Azure SQL Managed Instance offline. |
| SQL Server on Azure SQL Virtual Machine - Online migration | Yes | Migrate to SQL Server on Azure VMs online with minimal downtime. |
| SQL Server on Azure SQL Virtual Machine - Offline migration | Yes | Migrate to SQL Server on Azure VMs offline. |
| Migrate logins | No | Migrate logins from your source to your target. |
| Migrate schemas | Yes | Migrate schemas from your source to your target. |
| Azure portal support | Yes | Create and monitor your migration by using the Azure portal. |
| Regional availability | Yes | For regional availability, see Products available by region. |
| Improved user experience | Yes | The DMS is faster, more secure, and easier to troubleshoot. |
| Automation | Yes | The DMS supports PowerShell and Azure CLI. |
| Private endpoints | Yes | Connect to your source and target using private endpoints. |
| TDE support | No | Migrate databases encrypted with TDE. |

## Migrate databases to Azure with familiar tools

Azure DMS integrates some of the functionality of our existing tools and services. It provides customers with a comprehensive, highly available solution.

The service uses the same underlying technology as the [Azure Arc readiness assessment](/sql/sql-server/azure-arc/migration-assessment) to provide recommendations to guide you through the required changes before a migration. It's up to you to perform any remediation required.

Azure DMS performs all the required steps when ready to begin the migration process. Knowing that the process takes advantage of Microsoft's best practices, you can fire and forget your migration projects with peace of mind.

## Regional availability

For up-to-date info about the regional availability of Azure DMS, see [Products available by region](https://azure.microsoft.com/global-infrastructure/services/?products=database-migration).

## Related content

- [Azure Database Migration Service supported scenarios](resource-scenario-status.md)
- [Services and tools available for data migration scenarios](dms-tools-matrix.md)
- [FAQ about using Azure Database Migration Service](faq.yml)
