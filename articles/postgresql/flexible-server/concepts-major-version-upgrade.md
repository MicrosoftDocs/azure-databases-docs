---
title: Major version upgrades in Azure Database for PostgreSQL flexible server
description: Learn how to use Azure Database for PostgreSQL flexible server to do in-place major version upgrades of PostgreSQL on a server.
author: varun-dhawan
ms.author: varundhawan
ms.date: 5/21/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
---

# Introduction

[!INCLUDE [applies-to-postgresql-Flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]

Azure Database for PostgreSQL flexible server supports PostgreSQL versions [!INCLUDE [supported-versions](includes/major-versions-ascending.md)]. The Postgres community releases a new major version that contains new features about once a year. Additionally, each major version receives periodic bug fixes in the form of minor releases. Minor version upgrades include changes that are backward compatible with existing applications. Azure Database for PostgreSQL flexible server periodically updates the minor versions during a customer's maintenance window.

Major version upgrades are more complicated than minor version upgrades. They can include internal changes and new features that might not be backward compatible with existing applications.

Azure Database for PostgreSQL flexible server has a feature that performs an in-place major version upgrade of the server with just a click. This feature simplifies the upgrade process by minimizing the disruption to users and applications that access the server.

In-place upgrades retain the server name and other settings of the current server after the upgrade of a major version. They don't require data migration or changes to the application connection strings. In-place upgrades are faster and involve shorter downtime than data migration.

## Upgrade Process

Here are some of the important considerations with in-place major version upgrades:

- During the process of an in-place major version upgrade, Azure Database for PostgreSQL flexible server runs a precheck procedure to identify any potential issues that might cause the upgrade to fail.
    - If the precheck finds any incompatibilities, it creates a log event that shows that the upgrade precheck failed, along with an error message.
    - If the precheck is successful, Azure Database for PostgreSQL flexible server stops the service and takes an implicit backup just before starting the upgrade. The service can use this backup to restore the database instance to its previous version if there's an upgrade error.
- Azure Database for PostgreSQL flexible server uses the [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) tool to perform in-place major version upgrades. The service provides the flexibility to skip versions and upgrade directly to later versions.
- During an in-place major version upgrade of a server which is enabled for high availability (HA), the service disables HA, performs the upgrade on the primary server, and then re-enables HA after the upgrade is complete.
- Most extensions are automatically upgraded to later versions during an in-place major version upgrade, with [some exceptions](#upgrade-considerations-and-limitations).
- The process of an in-place major version upgrade for Azure Database for PostgreSQL flexible server automatically deploys the latest supported minor version.
- An in-place major version upgrade is an offline operation that results in a brief period of downtime. The downtime is typically less than 15 minutes. The duration can vary, depending on the number of system tables involved.
- Long-running transactions or high workload before the upgrade might increase the time taken to shut down the database and increase upgrade time.
- After an in-place major version upgrade is successful, there are no automated ways to revert to the earlier version. However, you can perform a point-in-time recovery (PITR) to a time before the upgrade to restore the previous version of the database instance.
- Azure Database for PostgreSQL Flexible Server takes snapshot of your database during an upgrade. The snapshot is taken before the upgrade starts. If the upgrade fails, the system automatically restores your database to its state from the snapshot.
- [PostgreSQL 16 introduces role-based security](concepts-security.md#postgresql-16-changes-with-role-based-security) measures. After a major version upgrade on Azure Database for PostgreSQL Flexible Server, the first user created on the server—who is granted the ADMIN option—will now have administrative privileges over other roles for essential maintenance operations.

## View upgrade logs

Major version upgrade logs (`PG_Upgrade_Logs`) provide direct access to detailed [server logs](how-to-configure-server-logs.md). Integrating `PG_Upgrade_Logs` into your upgrade process can help ensure a smoother and more transparent transition to new PostgreSQL versions.

You can configure your major version upgrade logs in the same way as server logs, by using the following server parameters:

- To turn on the feature, set `logfiles.download_enable` to `ON`.
- To define the retention of log files in days, use `logfiles.retention_days`.

#### Setup upgrade logs

To start using `PG_Upgrade_Logs`, you can [Configure capture of PostgreSQL server logs and major version upgrade logs](how-to-configure-server-logs.md).

You can access the upgrade logs through the UI for server logs. There, you can monitor the progress and details of your PostgreSQL major version upgrades in real time. This UI provides a centralized location for viewing logs, so you can more easily track and troubleshoot the upgrade process.

#### Benefits of using upgrade logs

- **Insightful diagnostics**: `PG_Upgrade_Logs` provides valuable insights into the upgrade process. It captures detailed information about the operations performed, and it highlights any errors or warnings that occur. This level of detail is instrumental in diagnosing and resolving problems that might arise during the upgrade, for a smoother transition.
- **Streamlined troubleshooting**: With direct access to these logs, you can quickly identify and address potential upgrade obstacles, reduce downtime, and minimize the impact on your operations. The logs serve as a crucial troubleshooting tool by enabling more efficient and effective problem resolution.

## Considerations for PostgreSQL upgrades

If a precheck operation fails during an in-place major version upgrade, the upgrade is blocked with a detailed error message. Below are the known limitations that can cause the upgrade to fail or behave unexpectedly:

### Unsupported Server Configurations

- Read replicas are not supported during in-place upgrades. You must delete the read replica before upgrading the primary server. After the upgrade, you can re-create the replica.
- Network traffic rules may block upgrade operations. 
    - Ensure your flexible server can send/receive traffic on ports 5432 and 6432 within its virtual network and to Azure Storage (for log archiving).
    - If Network Security Groups (NSGs) restrict this traffic, HA will not re-enable automatically post-upgrade. You may need to manually update NSG rules and re-enable HA.
- Logical replication slots are not supported during in-place major version upgrades.
- Servers using SSDv2 storage are not eligible for major version upgrades.
- Views dependent on `pg_stat_activity` are not supported during major version upgrades.

### Extension Limitations

In-place major version upgrades do not support all PostgreSQL extensions. The upgrade will fail during the precheck if unsupported extensions are found.
- The following extensions are not supported across any PostgreSQL versions: `timescaledb`, `pgaudit`, `dblink`, `orafce`, `pg_partman`, `postgres_fdw`
- The following extensions are not supported when the upgrade target is PostgreSQL 16 or higher: `pgrouting`
- The following extensions are not supported when upgrading to PostgreSQL 17: `pgrouting`, `age`, `azure_ai`, `hll`, `pg_diskann`

These extensions must be removed from the **azure.extensions** server parameter prior to upgrade. If present, the upgrade will be blocked.

### PostGIS-Specific Considerations

If you're using PostGIS or any dependent extensions, you must configure the search_path server parameter to include:
- Schemas related to PostGIS
- Dependent extensions, including: `postgis`, `postgis_raster`, `postgis_sfcgal`, `postgis_tiger_geocoder`, `postgis_topology`, `address_standardizer`, `address_standardizer_data_us`, `fuzzystrmatch`

Failure to configure the search_path correctly can lead to upgrade failures or broken objects post-upgrade.

## Post upgrade

After the major version upgrade is complete, we recommend running the `ANALYZE` command  in each database to refresh the [`pg_statistic`](https://www.postgresql.org/docs/current/catalog-pg-statistic.html) table. Missing or stale statistics can lead to bad query plans, which in turn might degrade performance and take up excessive memory.

```sql
postgres=> analyze;
ANALYZE
```

> [!NOTE]  
> In-place major version upgrades are supported on [automigrated servers](../migrate/automigration-single-to-flexible-postgresql.md). After a successful in-place Major Version Upgrade on an automigrated server, the username format **username@servername** will no longer be supported. Instead, you must use the standard format: **username**.
To avoid authentication issues, carefully review and update all connection strings in your applications and scripts to ensure they use the updated username format after the upgrade.


## Related content

- [Major version upgrade of Azure Database for PostgreSQL flexible server](how-to-perform-major-version-upgrade.md?tabs=portal).
- [High availability in Azure Database for PostgreSQL flexible server](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL flexible server](concepts-backup-restore.md).
