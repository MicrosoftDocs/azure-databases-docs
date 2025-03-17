---
title: Release notes for Azure DB for PostgreSQL flexible server
description: Release notes for Azure DB for PostgreSQL flexible server, including feature additions, engine versions support, extensions, and other announcements.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 02/24/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: overview
# customer intent: As a reader, I want the title and description to meet the required length and include the relevant information about the release notes for Azure DB for PostgreSQL flexible server.
---

# Release notes - Azure Database for PostgreSQL flexible server

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

This article highlights the latest updates and enhancements for Azure Database for PostgreSQL flexible server, service including new feature releases, supported engine versions, available extensions, and other important announcements.

## Release: February 2025
- Support for new [minor versions](concepts-supported-versions.md) 17.2, 16.6, 15.10, 14.15, 13.18, and 12.22. <sup>$</sup>
- Support for [pg_signal_autovacuum_worker](how-to-autovacuum-tuning.md#troubleshooting-guides) role in PostgreSQL versions 15 and higher for Azure Database for PostgreSQL flexible server. 
- Public preview of [enhanced connection and CPU monitoring metrics](concepts-monitoring.md#enhanced-metrics) (`TCP_connection_backlog`, `postmaster_process_cpu_usage`) is now available.
- General availability of New Zealand North region.

## Release: January 2025

- Public preview of [Elastic Clusters](./concepts-elastic-clusters.md) for Azure Database for PostgreSQL flexible server.

## Release: December 2024

- General Availability of [oracle_fdw](../extensions/concepts-extensions-versions.md#oracle_fdw) extension.
- General Availability of [index tuning](concepts-index-tuning.md) on Azure Database for PostgreSQL flexible server.
- General Availability of the [Semantic Ranker Solution Accelerator](https://aka.ms/pg-ranker) for Azure Database for PostgreSQL flexible server.
- Public preview of [age](../extensions/concepts-extensions-versions.md#age) extension.
- Public preview of [GraphRAG Solution Accelerator](https://aka.ms/pg-graphrag) for Azure Database for PostgreSQL flexible server.
- Public preview of [On-Demand Backups](concepts-backup-restore.md#on-demand-backups-preview).

## Release: November 2024

- General availability of [High-Availability Health Status Monitoring](how-to-monitor-high-availability.md) for Azure Database for PostgreSQL flexible server.
- [PostgreSQL 12](concepts-version-policy.md) will retire on November 14, 2024. Please upgrade to a supported version before retirement to ensure continued support and security.

## Release: October 2024

- General Availability of [Task Automation](create-automation-tasks.md).
- Preview of [Fabric Mirroring](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/mirroring-azure-database-for-postgresql-flexible-server-in/ba-p/4251876) for Azure Database for PostgreSQL flexible server.

## Release: September 2024

- Public preview of [PostgreSQL 17](concepts-supported-versions.md#postgresql-version-17-preview) for Azure Database for PostgreSQL flexible server.
- Support for new [minor versions](concepts-supported-versions.md) 16.4, 15.8, 14.13, 13.16, and 12.20. <sup>$</sup>
- Support for [Reserved pricing](concepts-reserved-pricing.md) for Intel and AMD V5 Skus for Azure Database for PostgreSQL flexible server.
- Public preview of [postgresql_anonymizer (anon)](../extensions/concepts-extensions-versions.md#anon) extension.
- Support for MD5 is disabled in favor of [SCRAM authentication](how-to-connect-scram.md) authentication for new PostgreSQL 14+ new server deployments.
- Collation sort order might change due to an underlying `glibc` update from 2.27 to 2.35. See [PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Locale_data_changes) for details.

## Release: Aug 2024

- General availability of [Database Size Metrics](concepts-monitoring.md) for Azure Database for PostgreSQL flexible server.
- General availability: [postgres_protobuf](../extensions/concepts-extensions-versions.md#postgres_protobuf) extension.

## Release: July 2024

- General availability of [Major Version Upgrade Support for PostgreSQL 16](concepts-major-version-upgrade.md) for Azure Database for PostgreSQL flexible server.
- General availability of [Pgvector 0.7.0](../extensions/concepts-extensions-versions.md#vector) extension.
- General availability support for [Storage-Autogrow with read replicas](concepts-read-replicas.md)
- Support for [SCRAM authentication](how-to-connect-scram.md) authentication set as default for new PostgreSQL 14+ new server deployments.
- General availability support for [System Assigned Managed Identity](concepts-Identity.md) for Azure Database for PostgreSQL flexible server.

## Release: June 2024

- Support for new [minor versions](concepts-supported-versions.md) 16.3, 15.7, 14.12, 13.15, and 12.19. <sup>$</sup>
- General availability of [IOPS scaling](concepts-storage.md#iops-scaling) on Azure Database for PostgreSQL flexible server.
- CMK support for LTR is in Public preview [long-term backup retention](concepts-backup-restore.md).
- Support for [built-in Azure Policy definitions](concepts-security.md#azure-policy-support)

## Release: May 2024

- General availability of Postgres [azure_ai](generative-ai-azure-overview.md) extension.
- Public preview of [azure_local_ai](azure-local-ai.md) extension.
- Public preview of [index tuning](concepts-index-tuning.md) on Azure Database for PostgreSQL flexible server.
- Public preview of [Updating PostgreSQL extensions](../extensions/how-to-update-extensions.md) on Azure Database for PostgreSQL flexible server.
- Support for the following [extensions](../extensions/how-to-allow-extensions.md):
    - [TimescaleDB (ver 2.13.0) for PG16](../extensions/concepts-extensions-versions.md#timescaledb).
    - [login_hook](../extensions/concepts-extensions-versions.md#login_hook).
    - [session_variable](../extensions/concepts-extensions-versions.md#session_variable).

## Release: April 2024

- General availability of [virtual endpoints](concepts-read-replicas-virtual-endpoints.md) and [promote to primary server](concepts-read-replicas-promote.md) operation for [read replicas](concepts-read-replicas.md).
- Support for new [minor versions](concepts-supported-versions.md) 16.2, 15.6, 14.11, 13.14, 12.18. <sup>$</sup>
- Support for new [PgBouncer versions](concepts-pgbouncer.md) 1.22.1. <sup>$</sup>

## Release: March 2024

- Public preview of [Major Version Upgrade Support for PostgreSQL 16](concepts-major-version-upgrade.md) for Azure Database for PostgreSQL flexible server.
- Public preview of [real-time language translations](generative-ai-azure-cognitive.md#language-translation) with azure_ai extension on Azure Database for PostgreSQL flexible server.
- Public preview of [real-time machine learning predictions](generative-ai-azure-machine-learning.md) with azure_ai extension on Azure Database for PostgreSQL flexible server.
- General availability of version 0.6.0 of [vector](how-to-use-pgvector.md) extension on Azure Database for PostgreSQL flexible server.
- General availability of [Migration service](../../postgresql/migrate/migration-service/concepts-migration-service-postgresql.md) in Azure Database for PostgreSQL flexible server.
- Support for PostgreSQL 16 changes with [BYPASSRLS](concepts-security.md#bypassing-row-level-security)

## Release: February 2024

- Support for new [minor versions](concepts-supported-versions.md) 16.1, 15.5, 14.10, 13.13, 12.17, 11.22. <sup>$</sup>
- General availability of [Major Version Upgrade logs](concepts-major-version-upgrade.md#major-version-upgrade-logs)
- General availability of [private endpoints](concepts-networking-private-link.md).

## Release: January 2024

- General availability of [Server logs](how-to-configure-server-logs.md), including Portal and CLI support.
- General availability of UAE Central region.
- General availability of Israel Central region.
- Worldwide public preview of [long-term backup retention](concepts-backup-restore.md).

## Release: December 2023

- Public preview of [Server logs](how-to-configure-server-logs.md).
- General availability of [TLS Version 1.3 support](concepts-networking-ssl-tls.md#tls-versions).
- General availability of [Microsoft Defender support](concepts-security.md)

## Release: November 2023

- General availability of PostgreSQL 16 for Azure Database for PostgreSQL flexible server.
- General availability of [near-zero downtime scaling](concepts-scaling-resources.md).
- General availability of [Pgvector 0.5.1](../extensions/concepts-extensions-versions.md#vector) extension.
- General availability of Italy North region.
- Public preview of [premium SSD v2](concepts-storage.md).
- Public preview of [decoupling storage and IOPS](concepts-storage.md).
- Public preview of [private endpoints](concepts-networking-private-link.md).
- Public preview of [virtual endpoints and new promote to primary server](concepts-read-replicas.md) operation for read replica.
- Public preview of Postgres [azure_ai](generative-ai-azure-overview.md) extension.
- Public preview of [pg_failover_slots](../extensions/concepts-extensions-versions.md#pg_failover_slots) extension.
- Public preview of [long-term backup retention](concepts-backup-restore.md).

## Release: October 2023

- Support for new [minor versions](concepts-supported-versions.md) 15.4, 14.9, 13.12, 12.16, 11.21. <sup>$</sup>
- General availability of [Grafana Monitoring Dashboard](https://grafana.com/grafana/dashboards/19556-azure-azure-postgresql-flexible-server-monitoring/) for Azure Database for PostgreSQL flexible server.

## Release: September 2023

- General availability of [Storage autogrow](concepts-storage.md) for Azure Database for PostgreSQL flexible server.
- General availability of [Cross Subscription and Cross Resource Group Restore](how-to-restore-server.md) for Azure Database for PostgreSQL flexible server.

## Release: August 2023

- Support for [minor versions](concepts-supported-versions.md) 15.3, 14.8, 13.11, 12.15, 11.20. <sup>$</sup>
- General availability of [Enhanced Metrics](concepts-monitoring.md#enhanced-metrics), [Autovacuum Metrics](concepts-monitoring.md#autovacuum-metrics), [PgBouncer Metrics](concepts-monitoring.md#pgbouncer-metrics) and [Database availability metric](concepts-monitoring.md#database-availability-metric) for Azure Database for PostgreSQL flexible server.

## Release: July 2023

- General Availability of PostgreSQL 15 for Azure Database for PostgreSQL flexible server.
- Public preview of [Automation Tasks](create-automation-tasks.md) for Azure Database for PostgreSQL flexible server.

## Release: June 2023

- Support for [minor versions](concepts-supported-versions.md) 15.2 (preview), 14.7, 13.10, 12.14, 11.19. <sup>$</sup>
- General availability of [Query Performance Insight](concepts-query-performance-insight.md) for Azure Database for PostgreSQL flexible server.
- General availability of [Major Version Upgrade](concepts-major-version-upgrade.md) for Azure Database for PostgreSQL flexible server.
- General availability of [Restore a dropped server](how-to-restore-dropped-server.md) for Azure Database for PostgreSQL flexible server.
- Public preview of [Storage auto-grow](concepts-storage.md) for Azure Database for PostgreSQL flexible server.

## Release: May 2023

- Public preview of [Database availability metric](concepts-monitoring.md#database-availability-metric) for Azure Database for PostgreSQL flexible server.
- PostgreSQL 15 is now available in public preview for Azure Database for PostgreSQL flexible server in limited regions (West Europe, East US, West US2, South East Asia, UK South, North Europe, Japan East).
- General availability: [Pgvector extension](how-to-use-pgvector.md) for Azure Database for PostgreSQL flexible server.
- General availability: [Azure Key Vault Managed HSM](concepts-data-encryption.md) with Azure Database for PostgreSQL flexible server.
- General availability [32 TB Storage](concepts-storage.md) with Azure Database for PostgreSQL flexible server.
- Support for [Ddsv5 and Edsv5 SKUs](concepts-compute.md) with Azure Database for PostgreSQL flexible server.

## Release: April 2023

- Public preview of [Query Performance Insight](concepts-query-performance-insight.md) for Azure Database for PostgreSQL flexible server.
- Public preview of: [Power BI integration](connect-with-power-bi-desktop.md) for Azure Database for PostgreSQL flexible server.
- Public preview of [Troubleshooting guides](concepts-troubleshooting-guides.md) for Azure Database for PostgreSQL flexible server.

## Release: March 2023

- General availability of [Read Replica](concepts-read-replicas.md) for Azure Database for PostgreSQL flexible server.
- Public preview of [PgBouncer Metrics](concepts-monitoring.md#pgbouncer-metrics) for Azure Database for PostgreSQL flexible server.
- General availability of [Azure Monitor workbooks](concepts-workbooks.md) for Azure Database for PostgreSQL flexible server.

## Release: February 2023

- Public preview of [Autovacuum Metrics](concepts-monitoring.md#autovacuum-metrics) for Azure Database for PostgreSQL flexible server.
- Support for [semver](../extensions/concepts-extensions-versions.md#semver) extension with new servers. <sup>$</sup>
- Public Preview of [Major Version Upgrade](concepts-major-version-upgrade.md) for Azure Database for PostgreSQL flexible server.
- Support for [Geo-redundant backup feature](concepts-backup-restore.md#geo-redundant-backup-and-restore) when using [Data encryption with customer managed key](concepts-data-encryption.md).
- Support for [minor versions](concepts-supported-versions.md) 14.6, 13.9, 12.13, 11.18. <sup>$</sup>

## Release: January 2023

- General availability of [Microsoft Entra authentication support](concepts-azure-ad-authentication.md) for Azure Database for PostgreSQL flexible server in all Azure Public Regions.
- General availability of [Customer Managed Key feature](concepts-data-encryption.md) with Azure Database for PostgreSQL flexible server in all Azure public regions.

## Release: December 2022

- Support for [pg_hint_plan](../extensions/concepts-extensions-versions.md#pg_hint_plan) extension with new servers. <sup>$</sup>
- General availability of [Customer Managed Key feature](concepts-data-encryption.md) with Azure Database for PostgreSQL flexible server in Canada East, Canada Central, Southeast Asia, Switzerland North, Switzerland West, Brazil South and East Asia Azure regions.

## Release: November 2022

- Public preview of [Enhanced Metrics](concepts-monitoring.md#enhanced-metrics) for Azure Database for PostgreSQL flexible server.
- Support for [minor versions](concepts-supported-versions.md) 14.5, 13.8, 12.12, 11.17. <sup>$</sup>
- General availability of Azure Database for PostgreSQL flexible server in China North 3 & China East 3 Regions.

## Release: October 2022

- Support for [Read Replica](concepts-read-replicas.md) feature in public preview.
- Support for [Microsoft Entra authentication ](concepts-azure-ad-authentication.md) authentication in public preview.
- Support for [Customer managed keys](concepts-data-encryption.md) in public preview.
- Published [Security and compliance certifications](concepts-compliance.md) for Azure Database for PostgreSQL flexible server.
- Postgres 14 is now the default PostgreSQL version.

## Release: September 2022

- Support for [Fast Restore](concepts-backup-restore.md) feature.
- General availability of [Geo-Redundant Backups](concepts-backup-restore.md). See the [regions](overview.md#azure-regions) where Geo-redundant backup is currently available.

## Release: August 2022

- Support for [PostgreSQL minor version](concepts-supported-versions.md) 14.4. <sup>$</sup>
- Support for [new regions](overview.md#azure-regions) Qatar Central, Switzerland West, France South.

<sup>**$**</sup> New PostgreSQL 14 servers are provisioned with version 14.4. Your existing PostgreSQL 14.3 servers will be upgraded to 14.4 in your server's future maintenance window.

## Release: July 2022

- Support for [Geo-redundant backup](concepts-backup-restore.md#geo-redundant-backup-and-restore) in [more regions](overview.md#azure-regions) - Australia East, Australia Southeast, Canada Central, Canada East, UK South, UK West, East US, West US, East Asia, Southeast Asia, North Central US, South Central US, and France Central.

## Release: June 2022

- Support for [**PostgreSQL version 14**](concepts-supported-versions.md).
- Support for [minor versions](concepts-supported-versions.md) 14.3, 13.7, 12.11, 11.16. <sup>$</sup>
- Support for [Same-zone high availability]/azure/reliability/reliability-postgresql-flexible-server deployment option.
- Support for choosing [standby availability zone](how-to-manage-high-availability-portal.md) when deploying zone-redundant high availability.
- Support for [plv8](../extensions/concepts-extensions-versions.md#plv8) extension with new servers. <sup>$</sup>
- Support for [pgrouting](../extensions/concepts-extensions-versions.md#pgrouting) extension with new servers. <sup>$</sup>
- Version updates for [PostGIS](../extensions/concepts-extensions-versions.md#postgis) extension.
- General availability of Azure Database for PostgreSQL flexible server in Canada East and India West regions.

## Release: May 2022

- Support for [new regions](overview.md#azure-regions) India West, Canada East.

## Release: April 2022

- Support for [latest PostgreSQL minors](concepts-supported-versions.md) 13.6, 12.10 and 11.15 with new server creates. <sup>$</sup>
- Support for updating Private DNS Zone for [Azure Database for PostgreSQL flexible server private networking](concepts-networking-private.md) for existing servers<sup>$</sup>.

## Release: February 2022

- Support for [latest PostgreSQL minors](concepts-supported-versions.md) 13.5, 12.9 and 11.14 with new server creates. <sup>$</sup>
- Support for [US Gov regions](overview.md#azure-regions) - Arizona and Virginia.
- Support for the following [extensions](../extensions/how-to-allow-extensions.md) with new servers: <sup>$</sup>
    - [TimescaleDB](../extensions/concepts-extensions-versions.md#timescaledb).
    - [orafce](../extensions/concepts-extensions-versions.md#orafce).
    - [pg_repack](../extensions/concepts-extensions-versions.md#pg_repack).
- Extensions need to be [allowlisted](../extensions/how-to-allow-extensions.md#allow-extensions) before they can be installed.
- Support for zone redundant high availability for new server creates in [regions](overview.md#azure-regions) Central India, Korea Central, East Asia, and West US 3.
- Several bug fixes, stability, security, and performance improvements. <sup>$</sup>

## Release: November 2021

- Azure Database for PostgreSQL flexible server is [**Generally Available**](https://techcommunity.microsoft.com/t5/azure-database-for-postgresql/azure-database-for-postgresql-flexible-server-is-now-ga/ba-p/2987030).
- Support for [latest PostgreSQL minors](concepts-supported-versions.md) 13.4, 12.8 and 11.13 with new server creates. <sup>$</sup>
- Support for [Geo-redundant backup and restore](concepts-backup-restore.md) feature in preview in selected paired regions - East US 2, Central US, North Europe, West Europe, Japan East, and Japan West.
- Support for [new regions](overview.md#azure-regions) North Central US, Sweden Central, and West US 3.
- Support for [Azure Stream Analytics (ASA) connector in Preview](https://techcommunity.microsoft.com/blog/analyticsonazure/stream-analytics-updates---ignite-fall-2021-new-outputs-new-security-options-and/2919170) to ingest high throughput streaming data to existing table.
- Several bug fixes, stability, and performance improvements.
## Release: October 2021

- Support for [Ddsv4 and Edsv4 SKUs](https://techcommunity.microsoft.com/blog/adforpostgresql/flexible-server-now-supports-v4-compute-series-in-postgresql-on-azure/2815092).
- Ability to choose local disk for temporary tablespace using `azure.enable_temp_tablespaces_on_local_ssd` server parameter.
The server parameters page in the Azure portal shows a unit of measurement and the PostgreSQL doc link for most parameters.
- Several bug fixes, stability, and performance improvements.

## Release: September 2021

- Support for [Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_flexible_server).
- Support for [new regions](overview.md#azure-regions) Central India and Japan West.
- Support for a non-SSL mode of connectivity using a new `require_secure_transport` server parameter.
- Support for the `log_line_prefix` server parameter, which adds the string at the beginning of each log line.
- Support for [Azure Resource Health](/azure/service-health/resource-health-overview) for Azure Database for PostgreSQL flexible server health diagnosis and to get support.
- Several bug fixes, stability, and performance improvements.

## Release: July 2021

- Support for [new regions](overview.md#azure-regions) East Asia, Germany West Central, Korea South, South Central US, UK West.
- Support for [pglogical](concepts-logical.md) extension (2.3.2) with PostgreSQL 11, 12 and 13. <sup>$</sup>
- PgBouncer now includes `ignore_startup_parameters` to ignore certain client-side driver's parameters including `extra_float_digits`, and `pgbouncer.query_wait_timeout` parameters. <sup>$</sup>
- Support for `pg_stat_reset_shared('bgwriter');` and `pg_stat_reset_shared('archiver');` to reset the counters shown in the `pg_stat_bgwriter` and `pg_stat_archiver` views. <sup>$</sup>
- Several bug fixes, stability, and performance improvements.

## Release: June 2021

- Support for [latest PostgreSQL minors](concepts-supported-versions.md) 13.3, 12.7 and 11.12 with new server creates. <sup>$</sup>
- Support for [new regions](overview.md#azure-regions), including Australia Southeast, Brazil South, Korea Central, Norway East, South Africa North, Switzerland North, UAE North, and West US.
- Support for [on-demand failover](/azure/reliability/reliability-postgresql-flexible-server#failover-support) capabilities including forced failover and planned failover for zone redundant high availability deployments.
- Support for [SCRAM authentication](how-to-connect-scram.md) for all major versions with new server creates. <sup>$</sup>
- Support for [pg_prewarm](../extensions/concepts-extensions-versions.md#pg_prewarm) extension to be preloaded using `shared_preload_libraries` with new server creates.
- Support for [lo](../extensions/concepts-extensions-versions.md#lo) extension.
- Several bug fixes, stability, and performance improvements.

## Release: May 2021

- Support for [PostgreSQL major version 13](concepts-supported-versions.md).
- Support for the following [extensions](../extensions/how-to-allow-extensions.md):
    - [pg_partman](../extensions/concepts-extensions-versions.md#pg_partman).
    - [pg_cron](../extensions/concepts-extensions-versions.md#pg_cron).
    - [pgaudit](../extensions/concepts-extensions-versions.md#pgaudit).
- Several bug fixes, stability, and performance improvements.

## Release: April 2021

- Support for [latest PostgreSQL minors](concepts-supported-versions.md) 12.6 and 11.11 with new server creates.
- Support for Virtual Network (virtual network) [private DNS zone](concepts-networking-private.md#private-access-virtual-network-integration).
- Support to choose the Availability zone during Point-in-time recovery operation.
- Support for new [regions](overview.md#azure-regions), including Australia East, Canada Central, and France Central.
- Support for [built-in PgBouncer](concepts-pgbouncer.md) connection pooler.
<!--- * Support for [pglogical](https://github.com/2ndQuadrant/pglogical) extension version 2.3.2. -->
- [Intelligent performance](concepts-query-store.md) .
- Several bug fixes, stability, and performance improvements.

## Release: October 2020 - March 2021

- Improved experience connecting [connect](connect-azure-cli.md) to the Azure Database for PostgreSQL flexible server instance using Azure CLI with the `az postgres flexible- server connect` command.
- Support for [new regions](overview.md#azure-regions).
- Several portal improvements, including the display of minor versions and summary of metrics on the overview page.
- Several bug fixes, stability, and performance improvements.

> [!IMPORTANT]
> **$** - New servers get these features automatically. Your existing servers will be automatically upgraded to the latest supported minor version and also new features are enabled during your server's future maintenance window.

## Contacts

For any questions or suggestions you might have on Azure Database for PostgreSQL flexible server, consider the following points of contact as appropriate:

- To contact Azure Support, [file a ticket from the Azure portal](https://portal.azure.com/?#blade/Microsoft_Azure_Support/HelpAndSupportBlade).
- To fix an issue with your account, file a [support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) in the Azure portal.
- To provide feedback or to request new features, create an entry via [UserVoice](https://feedback.azure.com/forums/597976-azure-database-for-postgresql).

## Frequently Asked Questions

Q. Will the Azure Database for PostgreSQL flexible server replace the Azure Database for PostgreSQL single server, or Will it soon be retired?

A. Yes. However, we'll continue to support Azure Database for PostgreSQL single server until **March 28, 2025**, and encourage you to adopt Azure Database for PostgreSQL flexible server, which has richer capabilities such as zone resilient HA, predictable performance, maximum control, custom maintenance window, cost optimization controls, and simplified developer experience suitable for your enterprise workloads. If we decide to retire any service, feature, API, or SKU, you'll receive advance notice, including a migration or transition path. Learn more about Microsoft Lifecycle policies [here](/lifecycle/faq/general-lifecycle).

## Related content

- [Quickstart: Create an Azure Database for PostgreSQL flexible server](quickstart-create-server.md).
