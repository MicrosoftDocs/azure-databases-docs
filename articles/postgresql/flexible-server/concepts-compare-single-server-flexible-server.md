---
title: Compare deployment options
description: Detailed comparison of features and capabilities between Azure Database for PostgreSQL - Single Server and Azure Database for PostgreSQL - Flexible Server.
author: akashraokm
ms.author: akashrao
ms.reviewer: maghan
ms.date: 04/29/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Comparison chart: Azure Database for PostgreSQL - Flexible Server vs. Single Server

[!INCLUDE [applies-to-postgresql-flexible-server](../includes/applies-to-postgresql-flexible-server.md)]## Overview

Azure Database for PostgreSQL flexible server is the next generation managed PostgreSQL service in Azure. It provides maximum flexibility over your database, built-in cost-optimizations, and offers several improvements over Azure Database for PostgreSQL single server.

>[!NOTE]
> For all your new deployments, we recommend using Azure Database for PostgreSQL flexible server. However, you should consider your own requirements against the comparison table below.

## Comparison table
The following table provides a list of high-level features and capabilities comparisons between Azure Database for PostgreSQL single server and Azure Database for PostgreSQL flexible server. 

| **Feature / Capability** | **Azure Database for PostgreSQL single server** | **Azure Database for PostgreSQL flexible server** |
| ---- | ---- | ---- |
| **General**  | | |
| General availability | GA since 2018 | GA since 2021|
| PostgreSQL | Community | Community |
| Supported versions | 10, 11 | 11, 12, 13, 14, 15, 16|
| Underlying O/S | Windows | Linux  |
| Availability zone selection for application colocation | No | Yes |
| Built-in connection pooler | No | Yes (PgBouncer)|
| Uptime SLA | [99.99% SLA](https://azure.microsoft.com/support/legal/sla/postgresql)| [Up to 99.99% SLA](https://azure.microsoft.com/support/legal/sla/postgresql) |
| **Connectivity** | | |
| Username in connection string | `<user_name>@server_name`. For example, `pgadmusr@mypgServer` | Just username. For example, `pgadmusr` | 
| lc_collate  | English_United States.1252 | en_US.utf8 |
| lc_ctype    | English_United States.1252 |en_US.utf8 |
|lc_messages | English_United States.1252 |en_US.utf8|
| lc_monetary | English_United States.1252 |  en_US.utf-8 |
| lc_numeric  | English_United States.1252 |  en_US.utf-8 |
| lc_time     | English_United States.1252 | en_US.utf8 |
| Connection port | 5432 | 5432 (DB), 6432 (PgBouncer) |
| Max. connections | 1982 | 5000 |
| Connections limit configurable? | No | Yes (`max_connections` parameter) |
| **Compute & Storage** | | |
| Compute tiers | Basic, General Purpose, Memory Optimized | Burstable, General Purpose, Memory Optimized |
| Burstable SKUs | No | Yes |
| Ability to scale across compute tiers | Can't scale Basic tier | Yes. Can scale across tiers |
| Stop/Start | No | Yes (for all compute SKUs). Only compute is stopped/started |
| Max. Storage size | 1 TB (Basic), 4 TB or 16 TB (GP, MO). Note: Not all regions support 16 TB. | 64 TB. Note: Not all regions support 64 TB.|
| Min storage size | 5 GB (Basic), 100 GB (GP, MO) | 32 GB |
| Storage autogrow | Yes | Yes |
| Max IOPS | Basic - Variable. GP/MO: up to 18 K  | Up to 80 K |
| **Networking/Security** | | |
| Supported networking | Virtual network, private link, public access | Private access (VNET injection in a delegated subnet), public access |
| Public access control | Firewall | Firewall |
| Private link support | Yes | Yes (Preview) |
| Private VNET injection support | No | Yes |
| Private DNS Zone support | No | Yes |
| Ability to move between private and public access | No | No |
| TLS support | TLS 1.2 | TLS 1.2, 1.3 enforced|
| Can turn off SSL | Yes | Yes (set ``require_secure_transport`` to OFF) |
| SCRAM authentication | No | Yes |
| **High Availability** | | |
| Zone-redundant HA | No | Yes (a synchronous standby is established in another zone within a region) |
| Same-zone HA | No | Yes (a synchronous standby is established in the same zone as the primary) |
| HA Configuration | Built-in with storage pinned to a zone. Compute can float across regions. | Physically separate compute & storage provisioned |
| Cost | 1x | 2x (compute + storage) |
| Availability with non-HA configuration | Automatic restart, compute relocation | Automatic restart, compute relocation
| Protect from zone failure | Compute - Yes. Storage - No | Compute & storage - Yes |
| Protect from region failure | No | Yes |
| Mode of HA replication | N/A | Postgres physical streaming replication in SYNC mode
| Standby can be used for read purposes | N/A | No |
| Application performance impact | No (not replicating) | Yes (Due to sync replication. Depends on the workload) |
| Automatic failover | Yes (spins another server)| Yes |
| Application connection string post failover | No change | No change |
| **Logical Replication** | | |
| Support for logical decoding | Yes | Yes |
| Support for native logical replication | No | Yes |
| Support for pglogical extension | No | Yes |
| Support logical replication with HA | N/A | [Limited](concepts-high-availability.md#high-availability---limitations) |
| **Disaster Recovery** | | |
| Cross region DR | Using read replicas, geo-redundant backup | Using read replicas, Geo-redundant backup (in [selected regions](overview.md#azure-regions)) |
| DR using replica | Using async physical replication | Using async physical replication |
| Automatic failover | No | No |
| Can use the same r/w endpoint | No | No |
| **Backup and Recovery** | | |
| Automated backups | Yes | Yes |
| Backup retention | 7-35 days | 7-35 days |
| PITR capability to any time within the retention period | Yes | Yes
| Ability to restore on a different zone | N/A | Yes |
| Ability to restore to a different VNET | No | Yes |
| Ability to restore to a different region | Yes (Geo-redundant) | Yes (in [selected regions](overview.md#azure-regions)) |
| Ability to restore a deleted server | Limited via API | Limited via API |
| **Read Replica** | | |
| Support for read replicas | Yes | Yes |
| Number of read replicas | 5 | 5 |
| Mode of replication | Async | Async |
| Cross-region support | Yes | Yes |
| **Maintenance Window** | | |
| System scheduled window | Yes | Yes |
| Customer scheduled window | No | Yes (can choose any 1 hr on any day) |
| Notice period | Three days | Five days |
| Maintenance period | Anytime within 15-hrs window | 1 hour window | 
| **Metrics** | | |
| Errors | Failed connections | Failed connections |
| Latency | Max lag across replicas, Replica lag | Max lag across replicas, Replica lag  |
| Saturation | Backup storage used, CPU %, IO %, Memory %, Server log storage limit, server log storage %, server log storage used, Storage limit, Storage %, Storage used | Backup storage used, CPU credits consumed, CPU credits remaining, CPU %, Disk queue depth, IOPS, Memory %, Read IOPS, Read throughput bytes/s, storage free, storage %, storage used, Transaction log storage used, Write IOPS, Write throughput bytes/s |
| Traffic | Active connections, Network In, Network out | Active connections, Max. used transaction ID, Network In, Network Out, succeeded connections |
| **Extensions** | | (offers latest versions)|
| TimescaleDB, orafce | Yes | Yes |
| pg_cron, pglogical | No | Yes |
| pgAudit | Yes | Yes |
| **Security** | | |
| Microsoft Entra ID Support (Microsoft Entra ID) | Yes | Yes |
| Customer managed encryption key (BYOK) | Yes | Yes |
| SCRAM Authentication (SHA-256) | No | Yes |
| Secure Sockets Layer (SSL) support | Yes | Yes |
| **Other features** | | |
| Alerts | Yes | Yes |
| Microsoft Defender for Cloud | Yes | Yes |
| Resource health | Yes | Yes |
| Service health | Yes | Yes |
| Performance insights (iPerf) | Yes | Yes |
| Major version upgrades support | No | Yes |
| Minor version upgrades | Yes. Automatic during maintenance window | Yes. Automatic during maintenance window |

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [Compute options in Azure Database for PostgreSQL - Flexible Server](concepts-compute.md).
- [Storage options in Azure Database for PostgreSQL - Flexible Server](concepts-storage.md).
- [Supported versions of PostgreSQL in Azure Database for PostgreSQL - Flexible Server](concepts-supported-versions.md).
- [Limits in Azure Database for PostgreSQL - Flexible Server](concepts-limits.md).
