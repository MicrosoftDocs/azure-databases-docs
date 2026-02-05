---
title: Dashboards in Azure Database Migration Service
description: Overview of Discovery and Assessment dashboards available in the Azure Database Migration Service portal.
author: rwestMSFT
ms.author: randolphwest
ms.reviewer: niball
ms.date: 02/19/2026
ms.service: azure-database-migration-service
ms.topic: overview
ms.collection:
  - sql-migration-content
---
# Dashboards in Azure Database Migration Service

Azure Database Migration Service (DMS) enables seamless, guided, and large-scale migration of your databases to Azure. This article describes the Discovery and Assessment dashboards available through the Azure DMS portal.

> [!NOTE]  
> Azure DMS supports multiple source databases including SQL Server, PostgreSQL, MySQL, and Oracle. This article focuses on SQL Server discovery and assessment.

## Overview

Azure Database Migration Service supports discovery, assessment, and migration of SQL Server instances to Azure SQL targets. The Discovery and Assessment dashboards help visualize your on-premises inventory, connection status, and migration readiness.

Make sure you have the required permissions and connected sources for full discovery and assessment functionality.

## Discovery dashboard

The Discovery dashboard provides visibility into the discovered SQL Server estate, helping you plan your migration strategy.

### Version distribution

The dashboard categorizes discovered instances based on SQL Server version.

### Connection mode

Identifies how each instance connects to Azure service. For example, **Connected**, **Registered**, and **Connected from Azure Arc**.

### Source platform

Displays the underlying platforms of the discovered SQL Servers. For example, **Physical Server**, **VMware**, etc.

Use this view to identify legacy platforms or unsupported configurations.

## Assessment dashboard

The Assessment dashboard helps you evaluate SQL Server instances for compatibility, target recommendations, and migration readiness.

### Migration assessment status

Tracks whether SQL Server instances have been assessed for compatibility:

- Not assessed
- Assessed
- Outdated

### Suggested target recommendation

Displays recommended Azure targets:

- Azure SQL Virtual Machine
- Azure SQL Managed Instance
- Azure SQL Database
- Unknown (requires more data)

### Migration readiness

Indicates which databases are ready to migrate:

- Most instances show **Ready** for migration
- Some instances are **Not ready**, or require extra steps

## How to access the dashboards

1. Open the Azure portal.

1. Search for **Azure Database Migration Service**.

1. Navigate to:

   - **Discovery** for inventory insights
   - **Assessment** for readiness evaluation

## Related content

- [Migration to Azure SQL Managed Instance - SQL Server migration in Azure Arc](/sql/sql-server/azure-arc/migrate-to-azure-sql-managed-instance)
- [Connect your SQL Server to Azure Arc](/sql/sql-server/azure-arc/connect)
- [Use Azure Migrate for full assessment](/azure/migrate/concepts-overview)
