---
title: Limitations FAQ - Elastic Clusters in Azure Database for PostgreSQL Flexible Server
description: Learn about existing limitations of elastic clusters of Azure Database for PostgreSQL flexible server.
#customer intent: As a user, I want to understand the capacity and functional limitations of elastic clusters, so that I can determine if they meet my workload requirements.
author: JaredMSFT
ms.author: jaredmeade
ms.reviewer: adamwolk, maghan
ms.date: 07/08/2026
ms.service: azure-database-postgresql
ms.subservice: elastic-clusters
ms.topic: faq
---

# Frequently asked questions about elastic clusters in Azure Database for PostgreSQL flexible server

The following section describes capacity and functional limits in elastic clusters of Azure Database for PostgreSQL.

Current [limitations of Azure Database for PostgreSQL](../configure-maintain/concepts-limits.md) server also apply to elastic clusters. The rest of the document describes differences that apply only to elastic clusters.

## General

This section lists the key capacity and functional limitations specific to elastic clusters in Azure Database for PostgreSQL flexible server. Use this information to understand which features are unsupported or behave differently compared to standard flexible servers.
 
### Q: In what regions can I use elastic clusters?

A: Elastic clusters are a feature of Azure Database for PostgreSQL flexible servers and as such are available in the [same regions](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/).
 
### Q: Can I create more databases in an elastic cluster?

A: The Azure portal provides credentials to connect to exactly one database per cluster. Currently, you can't create another database, and the `CREATE DATABASE` command fails with an error. This database is called `postgres` by default.

### Q: How many nodes can I add to an elastic cluster?

A: Elastic clusters can be scaled out to 20 nodes using the Azure Portal, CLI, or related IaC tools. If your workload requires more than 20 nodes, please contact Customer Support to assist with scaling out further.

### Q: Can I decrease the number of nodes in an elastic cluster?

A: Scaling in or decreasing the number of nodes in an elastic cluster is currently not supported.
 
### Q: What PostgreSQL version is supported with elastic clusters?

A: Elastic clusters support PostgreSQL version 17.
 
### Q: Can I use major version upgrades with elastic clusters?

A: Currently, major version upgrades aren't supported.
 
### Q: Can I download server logs?

A: Currently, downloading server logs isn't supported. You can use Azure Metrics, Log Analytic Workspaces, and PostgreSQL views to analyze cluster behavior.
 
## Extensions

This section lists PostgreSQL extensions that elastic clusters support or don't support. It also notes any special considerations when enabling them. Use this information to determine compatibility and known conflicts, such as between Citus and TimescaleDB.
 
### Q: What extensions aren't supported?

A: The following extensions aren't supported:
 
- anon
- pg_qs - Query Store
- postgis_topology
- TimescaleDB

### Q: Why isn't TimescaleDB available with elastic clusters?

A: The TimescaleDB extension isn't supported on elastic clusters because of low-level conflicts with the Citus extension.
 
## Migrations

This section describes supported methods and considerations for migrating data to and from elastic clusters. It includes recommended tools and known limitations. Use `pg_dump`/`pg_restore` or `pgcopydb` for logical migrations and verify extension compatibility before starting.
 
### Q: How can I migrate to or from elastic clusters?

A: Currently, you can migrate to and from elastic clusters by using `pg_dump`, `pg_restore`, and `pgcopydb`. Any other tool that works with standard PostgreSQL should work.
 
## Networking

This section describes networking considerations and limitations specific to elastic clusters. It includes supported connectivity options, ports used for management and pooling, and features that aren't currently available. Use this guidance to plan access, connection pooling, and network security for your cluster deployments.
 
### Q: Can I use PgBouncer for connection pooling with elastic clusters?

A: Yes, you can use PgBouncer with elastic clusters. Use port 6432 for schema and node management operations. Port 8432 is load-balanced to PgBouncer instances running across all nodes in the cluster.
 
### Q: Can I use virtual network (VNet) with elastic clusters?

A: Yes, you can add your elastic cluster Private Link Endpoints to your VNet. Additionally, if you need to limit network traffic to use your VNet exclusively, you can disable public network access. Virtual network injection isn't supported.
 
## Storage

This section outlines storage-related limitations and behaviors specific to elastic clusters, including provisioning, scaling, and backup considerations. Use this information to plan capacity, understand unsupported features, and avoid disruptions during migrations or scaling operations.

### Q: Is Storage Auto Scale available?

A: Currently, Storage Auto Scale isn't supported.
 
## Performance

This section describes performance-related limitations and behaviors for elastic clusters, including supported features, unsupported monitoring and tuning tools, and practical guidance for optimizing query and cluster performance. Use this information to plan workloads and set expectations for latency, scaling, and diagnostic capabilities.
 
### Q: Can I use Query Performance Insights with elastic clusters?

A: Currently, Query Performance Insights isn't supported.
 
### Q: Can I use Automatic Index Tuning with elastic clusters?

A: Currently, Automatic Index Tuning isn't supported.
 
### Q: Can I use read replicas with elastic clusters?

A: Currently, a single read replica is supported.

## Related content

- [What is an elastic cluster in Azure Database for PostgreSQL?](../elastic-clusters/concepts-elastic-clusters.md)
