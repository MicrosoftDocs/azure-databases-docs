---
title: Major Version Upgrades
description: Learn how to use Azure Database for PostgreSQL to do in-place major version upgrades of PostgreSQL on a server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 12/8/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Major version upgrades in Azure Database for PostgreSQL 

Your Azure Database for PostgreSQL flexible server instance supports PostgreSQL versions [!INCLUDE [supported-versions](includes/major-versions-ascending.md)]. The Postgres community releases a new major version that contains new features about once a year. Additionally, each major version receives periodic bug fixes in the form of minor releases. Minor version upgrades include changes that are backward compatible with existing applications. An Azure Database for PostgreSQL flexible server instance periodically updates the minor versions during a customer's maintenance window.

Major version upgrades are more complicated than minor version upgrades. They can include internal changes and new features that might not be backward compatible with existing applications.

Your Azure Database for PostgreSQL flexible server instance has a feature that performs an in-place major version upgrade of the server with just a click. This feature simplifies the upgrade process by minimizing the disruption to users and applications that access the server.

In-place upgrades retain the server name and other settings of the current server after the upgrade of a major version. They don't require data migration or changes to the application connection strings. In-place upgrades are faster and involve shorter downtime than data migration.

> [!NOTE]
> Azure Database for PostgreSQL supports in-place major version upgrades only to currently supported PostgreSQL versions. For example, you can upgrade the current version given the target version is officially supported by Azure at the time of the upgrade. Unsupported versions can't be selected as upgrade targets, and attempting to upgrade to a deprecated version may result in failure or service disruption. Always consult the [Azure PostgreSQL versioning policy](/azure/postgresql/flexible-server/concepts-version-policy) and [upgrade documentation](/azure/postgresql/flexible-server/concepts-major-version-upgrade) before initiating a major version upgrade. 

> [!NOTE]
> Major version upgrades to PostgreSQL 18 are being enabled in phases. At this time, MVU to PostgreSQL 18 is available in the AustraliaSoutheast, CanadaCentral, CentralIndia, CentralUS, EastAsia, EastUS, EastUS2, NorthCentralUS, SouthAfricaNorth, SouthCentralUS, SwedenCentral, WestCentralUS, WestUS2, and WestUS3 regions.

## Upgrade Process

Here are some of the important considerations with in-place major version upgrades:

- Before starting the upgrade, ensure that your server has at least 10–20% free storage available. During the upgrade process, temporary log files and metadata operations may increase disk usage. Insufficient free space can result in upgrade failures or rollback issues.
- During the process of an in-place major version upgrade, your Azure Database for PostgreSQL flexible server instance runs a precheck procedure to identify any potential issues that might cause the upgrade to fail.
    - If the precheck finds any incompatibilities, it creates a log event that shows that the upgrade precheck failed, along with an error message.
    - If the precheck is successful, the Azure Database for PostgreSQL flexible server instance stops the service and takes an implicit backup just before starting the upgrade. The service can use this backup to restore the database instance to its previous version if there's an upgrade error.
- An Azure Database for PostgreSQL flexible server instance uses the [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) tool to perform in-place major version upgrades. The service provides the flexibility to skip versions and upgrade directly to later versions.
- During an in-place major version upgrade of a server which is enabled for high availability (HA), the service disables HA, performs the upgrade on the primary server, and then re-enables HA after the upgrade is complete.
- Most extensions are automatically upgraded to later versions during an in-place major version upgrade, with [some exceptions](#upgrade-considerations-and-limitations).
- The process of an in-place major version upgrade for an Azure Database for PostgreSQL flexible server instance automatically deploys the latest supported minor version.
- An in-place major version upgrade is an offline operation, meaning the server will be unavailable during the process. While most upgrades complete in under 15 minutes, the actual duration depends on the size and complexity of the database. Specifically, the time required is directly proportional to the number of objects (tables, indexes, schemas) in your PostgreSQL instance. Larger or more complex schemas may experience longer upgrade times.
- Long-running transactions or high workload before the upgrade might increase the time taken to shut down the database and increase upgrade time.
- After an in-place major version upgrade is successful, there are no automated ways to revert to the earlier version. However, you can perform a point-in-time recovery (PITR) to a time before the upgrade to restore the previous version of the database instance.
- Your Azure Database for PostgreSQL flexible server instance takes a snapshot of your database during an upgrade. The snapshot is taken before the upgrade starts. If the upgrade fails, the system automatically restores your database to its state from the snapshot.
- [PostgreSQL 16 introduces role-based security](concepts-security.md#postgresql-16-changes-with-role-based-security) measures. After a major version upgrade on an Azure Database for PostgreSQL flexible server instance, the first user created on the server—who is granted the ADMIN option—will now have administrative privileges over other roles for essential maintenance operations.

## Upgrade Considerations and Limitations

If a precheck operation fails during an in-place major version upgrade, the upgrade is blocked with a detailed error message. Below are the known limitations that can cause the upgrade to fail or behave unexpectedly:

### Unsupported Server Configurations

- [Read replicas](./concepts-read-replicas-geo.md) are not supported during in-place upgrades. You must delete the read replica (including any cascading read replica) before upgrading the primary server. After the upgrade, you can re-create the replica.
- Network traffic rules may block upgrade operations. 
    - Ensure your flexible server instance can send/receive traffic on ports 5432 and 6432 within its virtual network and to Azure Storage (for log archiving).
    - If Network Security Groups (NSGs) restrict this traffic, HA will not re-enable automatically post-upgrade. You may need to manually update NSG rules and re-enable HA.
- Logical replication slots are not supported during in-place major version upgrades.
- Servers using SSDv2 storage are not eligible for major version upgrades.
- Views dependent on `pg_stat_activity` are not supported during major version upgrades.
- If you are performing the upgrade from PG11 to a higher version, you must first configure your flexible server to use [SCRAM authentication ](./security-connect-scram.md#configure-scram-authentication) by enabling SCRAM and resetting all login-role passwords.

### Extension Limitations

In-place major version upgrades do not support all PostgreSQL extensions. The upgrade will fail during the precheck if unsupported extensions are found.
- The following extensions are supported for regular use, **but will block an in-place major version upgrade if present**. Remove them before the upgrade and re-enable them after, if supported on the target version: `timescaledb`, `dblink`, `orafce`, `postgres_fdw`.
- The following extensions are **non-persistent utility extensions** and will need to be dropped and re-created after the upgrade by design: `pg_repack`, `hypopg`.
- When upgrading to PostgreSQL 17, the following extensions are **not supported** and must be removed before upgrade. You may re-enable them only if supported on the target version: `age`, `azure_ai`, `hll`, `pg_diskann`, `pgrouting`.

**Note:** If any of these extensions appear in the `azure.extensions` server parameter, the upgrade will be blocked. Remove them from the parameter before starting the upgrade.

### PostGIS-Specific Considerations

If you're using PostGIS or any dependent extensions, you must configure the search_path server parameter to include:
- Schemas related to PostGIS
- Dependent extensions, including: `postgis`, `postgis_raster`, `postgis_sfcgal`, `postgis_tiger_geocoder`, `postgis_topology`, `address_standardizer`, `address_standardizer_data_us`, `fuzzystrmatch`
- Failure to configure the search_path correctly can lead to upgrade failures or broken objects post-upgrade.

### Other upgrade considerations

- Event triggers: Upgrade pre-check blocks event triggers because they hook into DDL commands and may reference system catalogs that change between major versions—drop all `EVENT TRIGGER`s before upgrading and then recreate them after the upgrade to ensure a smooth upgrade.
- Large objects (LOs): Databases with millions of large objects (stored in `pg_largeobject`) can cause upgrade failures due to high memory usage or log volume. Use [vacuumlo](https://www.postgresql.org/docs/current/vacuumlo.html) utility to clean up unused LOs, and consider scaling up your server before upgrade if many LOs are still in use.

> [!WARNING]
> Use caution with vacuumlo. `vacuumlo` identifies orphaned large objects based on conventional reference columns (oid, lo). If your application uses custom or indirect reference types, valid large objects may be mistakenly deleted. Additionally, `vacuumlo` may consume significant CPU, memory, and IOPS, especially in databases with millions of large objects. Run it during maintenance windows and test on non-prod first.

## Post upgrade

After the major version upgrade is complete, we recommend running the `ANALYZE` command  in each database to refresh the [`pg_statistic`](https://www.postgresql.org/docs/current/catalog-pg-statistic.html) table. Missing or stale statistics can lead to bad query plans, which in turn might degrade performance and take up excessive memory.

```sql
postgres=> analyze;
ANALYZE
```
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

> [!NOTE]  
> In-place major version upgrades are supported on [automigrated servers](../migrate/automigration-single-to-flexible-postgresql.md). After a successful in-place Major Version Upgrade on an automigrated server, the username format **username@servername** will no longer be supported. Instead, you must use the standard format: **username**.
To avoid authentication issues, carefully review and update all connection strings in your applications and scripts to ensure they use the updated username format after the upgrade.

## Related content

- [Major version upgrade](how-to-perform-major-version-upgrade.md?tabs=portal).
- [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL](concepts-backup-restore.md).
