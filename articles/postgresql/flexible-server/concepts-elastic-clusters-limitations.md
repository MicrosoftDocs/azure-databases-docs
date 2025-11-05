---
title: Elastic Clusters Limitations FAQ
description: "Learn about existing limitations of elastic clusters with Azure Database for PostgreSQL flexible server instances."
author: JaredMSFT
ms.author: JaredMSFT
ms.reviewer: adamwolk, maghan
ms.service: azure-database-postgresql
ms.topic: faq
ms.date: 11/18/2025
---
# Frequently asked questions about elastic clusters

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

The following section describes capacity and functional limits in elastic clusters with Azure Database for PostgreSQL.

Current [limitations of Azure Database for PostgreSQL Flexible](concepts-limits.md) server also apply to elastic clusters. The rest of the document describes differences that apply only to elastic clusters.

## General

**Q: In what regions can I use elastic clusters?**

A: Elastic clusters are a feature of Azure Database for PostgreSQL flexible server instances and as such are available in the [same regions](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/).

**Q: Elastic clusters aren't available in the region I need, what can I do?**

A: We're enabling other regions shortly, if you're interested in specific regions fill out [this form](https://aka.ms/preview-pg-citus).

**Q: Can I create more databases in an elastic cluster?**

A: The Azure portal provides credentials to connect to exactly one database per cluster. Currently, creating another database isn't allowed, and the `CREATE DATABASE` command fails with an error.

Custom database names at cluster provisioning time will be supported.

**Q: What PostgreSQL version is supported with elastic clusters?**

A: Elastic clusters support PostgreSQL version 16.

**Q: Can I use Major Version Upgrades with elastic clusters?**

A: Currently, Major Version Upgrades aren't supported.

**Q: Can I download server logs?**

A: Currently, downloading server logs aren't supported. You can use Azure Metrics, Log Analytic Workspaces and PostgreSQL views to analyze cluster behavior.

**Q: Can I use terraform to deploy elastic clusters?**

A: Currently, terraform isn't supported. ARM templates are supported.

## Backups

**Q: Can I use GEO backups & GEO restore?**

A: Currently, GEO backups & GEO restore aren't supported.

**Q: Is Long Term Retention (LTR) supported?**

A: Currently, Long Term Retention isn't supported.

## Extensions

**Q: Why is TimescaleDB not available with elastic clusters?**

A: TimescaleDB extension isn't supported on elastic cluster due to low-level conflicts with the Citus extension.

**Q: What extensions aren't supported?**

A: The following extensions aren't supported:
- anon
- pg_qs - Query Store
- postgis_topology
- TimescaleDB

## Migrations

**Q: How can I migrate to/from elastic clusters?**

A: Currently, migrations to/from elastic clusters can be done with pg_dump, pg_restore, and pgcopydb. Any other tool working with standard PostgreSQL should work.

## Networking

**Q: Can I use PgBouncer for connection pooling with elastic clusters?**

A: Yes, you can use PgBouncer with elastic clusters. Port 6432 should be used for schema and node management operations, while port 8432 is load-balanced to PgBouncer instances running across all nodes in the cluster.

**Q: Can I use virtual network (VNet) with elastic clusters?**

A: Currently, virtual network isn't supported.

**Q: Are Private Domain Name System (DNS) Zones supported with elastic clusters?**

A: Currently, Private DNS Zones aren't supported.

## Storage

**Q: Can I use customer-managed keys (CMK) for storage encryption?**

A: Currently, customer-managed keys aren't supported.

**Q: Is Storage Auto Scale available?**

A: Currently, Storage Auto Scale isn't supported.

## Authentication

**Q: Can I use Microsoft Entra ID authentication with elastic clusters?**

A: Currently, Microsoft Entra ID authentication isn't supported.

## Performance

**Q: Can I use Query Performance Insights with elastic clusters?**

A: Currently, Query Performance Insights isn't supported.

**Q: Can I use Automatic Index Tuning with elastic clusters?**

A: Currently, Automatic Index Tuning isn't supported.

**Q: Can I use replicas with elastic clusters?**

A: Currently, replicas aren't supported.
