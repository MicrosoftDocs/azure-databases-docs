---
title: What's new - 2026
description: 2026 feature announcements for Azure Database for MySQL flexible server, listed newest first.
author: SudheeshGH
ms.author: sunaray
ms.reviewer: maghan
ms.date: 06/18/2026
ms.service: azure-database-mysql
ms.subservice: flexible-server
ms.topic: overview
ai-usage: ai-assisted
---

# What's new in Azure Database for MySQL flexible server in 2026?

This article summarizes the 2026 feature announcements for Azure Database for MySQL flexible server, listed newest first.

> [!NOTE]  
> This article references the term slave, which Microsoft no longer uses. When the term is removed from the software, we'll remove it from this article.

## July 2026

In July 2026, Azure Database for MySQL flexible server previewed a new storage option for demanding workloads. The following update introduces Premium SSD v2 support with independent scaling of storage capacity, IOPS, and throughput.

### Azure Database for MySQL now supports Premium SSD v2 storage in Private Preview

Azure MySQL now offers Premium SSD v2 storage option which enables you to independently scale storage capacity, IOPS, and throughput, helping optimize both performance and cost. The new managed disk-based architecture also introduces support for the latest General Purpose and Memory Optimized V6 SKU families, enabling you to run larger and more demanding workloads with better price-performance.

The feature is currently available in Private Preview for supported compute SKUs and regions. To enroll in the preview, submit your details using this [form](https://aka.ms/mysql-premium-ssdv2).

## June 2026

In June 2026, Azure Database for MySQL flexible server expanded its migration options. The following update adds Azure Database Migration Service support for migrating workloads to MySQL 8.4.

### Azure Database Migration Service adds support for MySQL 8.4

Azure Database Migration Service (Azure DMS) now supports migrating MySQL workloads to Azure Database for MySQL 8.4. With this update, you can migrate your data to MySQL 8.4 on Azure by using the automation that Azure DMS provides.

For more information, see [Tutorial: Migrate from MySQL to Azure Database for MySQL flexible server online using DMS via the Azure portal](../../dms/tutorial-mysql-azure-external-to-flex-online-portal.md) and [Azure Database for MySQL version support policy](../concepts-version-policy.md).

## Related content

- [Azure Database for MySQL flexible server release notes 2026](../release-notes/release-notes-2026.md)
- [Azure Database for MySQL flexible server 2026 release notes](../release-notes/release-notes-2026.md)
- [What is Azure Database for MySQL flexible server?](../flexible-server/overview.md)

