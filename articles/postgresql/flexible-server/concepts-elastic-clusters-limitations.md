---
title: Elastic Clusters Limitations FAQ
description: "Learn about existing limitations of elastic clusters of Azure Database for PostgreSQL flexible server instances."
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.topic: faq
---

# Frequently asked questions about elastic clusters in Azure Database for PostgreSQL

The following section describes capacity and functional limits in elastic clusters of Azure Database for PostgreSQL.

Current [limitations of Azure Database for PostgreSQL](concepts-limits.md) server also apply to elastic clusters. The rest of the document describes differences that apply only to elastic clusters.

## General

**Q: In what regions can I use elastic clusters?**

A: Elastic clusters are a feature of Azure Database for PostgreSQL flexible server instances. You can use them in the [same regions](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/) as those instances.

**Q: Elastic clusters aren't available in the region I need. What can I do?**

A: We're enabling other regions shortly. If you're interested in specific regions, fill out [this form](https://aka.ms/preview-pg-citus).

**Q: Can I create more databases in an elastic cluster?**

A: The Azure portal provides credentials to connect to exactly one database per cluster. Currently, you can't create another database, and the `CREATE DATABASE` command fails with an error.

You can use custom database names at cluster provisioning time.

**Q: What PostgreSQL version is supported with elastic clusters?**

A: Elastic clusters support PostgreSQL version 16.

**Q: Can I use major version upgrades with elastic clusters?**

A: Currently, major version upgrades aren't supported.

**Q: Can I download server logs?**

A: Currently, downloading server logs isn't supported. You can use Azure Metrics, Log Analytic Workspaces, and PostgreSQL views to analyze cluster behavior.

**Q: Can I use Terraform to deploy elastic clusters?**

A: Currently, Terraform isn't supported. ARM templates are supported.

## Backups

**Q: Can I use GEO backups and GEO restore?**

A: Currently, the service doesn't support GEO backups and GEO restore.

**Q: Is Long Term Retention (LTR) supported?**

A: Currently, the service doesn't support Long Term Retention.

## Extensions

**Q: Why isn't TimescaleDB available with elastic clusters?**

A: The service doesn't support the TimescaleDB extension on elastic clusters because of low-level conflicts with the Citus extension.

**Q: What extensions aren't supported?**

A: The service doesn't support the following extensions:
- anon
- pg_qs - Query Store
- postgis_topology
- TimescaleDB

## Migrations

**Q: How can I migrate to and from elastic clusters?**

A: Currently, you can migrate to and from elastic clusters with pg_dump, pg_restore, and pgcopydb. Any other tool that works with standard PostgreSQL should work.

## Networking

**Q: Can I use PgBouncer for connection pooling with elastic clusters?**

A: Yes, you can use PgBouncer with elastic clusters. Use port 6432 for schema and node management operations. Port 8432 is load-balanced to PgBouncer instances running across all nodes in the cluster.

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

## Related content

- [What is an elastic cluster in Azure Database for PostgreSQL?](concepts-elastic-clusters.md)
