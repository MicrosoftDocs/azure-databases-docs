---
title: Major Version Upgrades
description: Learn how to use Azure Database for PostgreSQL to do in-place major version upgrades of PostgreSQL on a server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 3/23/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
ms.custom: references_regions
---

# Major version upgrades in Azure Database for PostgreSQL 

Your Azure Database for PostgreSQL flexible server instance supports PostgreSQL versions [!INCLUDE [supported-versions](../includes/major-versions-ascending.md)]. The Postgres community releases a new major version that contains new features about once a year. Additionally, each major version receives periodic bug fixes in the form of minor releases. Minor version upgrades include changes that are backward compatible with existing applications. An Azure Database for PostgreSQL flexible server instance periodically updates the minor versions during a customer's maintenance window.

Major version upgrades are more complicated than minor version upgrades. They can include internal changes and new features that might not be backward compatible with existing applications.

Your Azure Database for PostgreSQL flexible server instance has a feature that performs an in-place major version upgrade of the server with just a click. This feature simplifies the upgrade process by minimizing the disruption to users and applications that access the server.

In-place upgrades retain the server name and other settings of the current server after the upgrade of a major version. They don't require data migration or changes to the application connection strings. In-place upgrades are faster and involve shorter downtime than data migration.

> [!NOTE]
> Azure Database for PostgreSQL supports in-place major version upgrades only to currently supported PostgreSQL versions. For example, you can upgrade the current version given the target version is officially supported by Azure at the time of the upgrade. Unsupported versions can't be selected as upgrade targets, and attempting to upgrade to a deprecated version may result in failure or service disruption. Always consult the [Azure PostgreSQL versioning policy](/azure/postgresql/flexible-server/concepts-version-policy) and [upgrade documentation](/azure/postgresql/flexible-server/concepts-major-version-upgrade) before initiating a major version upgrade. 

## Upgrade Process

Here are some of the important considerations with in-place major version upgrades:

- Before starting the upgrade, ensure that your server has at least 10–20% free storage available. During the upgrade process, temporary log files and metadata operations may increase disk usage. Insufficient free space can result in upgrade failures or rollback issues.
- During the process of an in-place major version upgrade, your Azure Database for PostgreSQL flexible server instance runs a precheck procedure to identify any potential issues that might cause the upgrade to fail.
    - If the precheck finds any incompatibilities, it creates a log event that shows that the upgrade precheck failed, along with an error message.
    - If the precheck is successful, the Azure Database for PostgreSQL flexible server instance stops the service and takes an implicit backup just before starting the upgrade. The service can use this backup to restore the database instance to its previous version if there's an upgrade error.
- An Azure Database for PostgreSQL flexible server instance uses the [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) tool to perform in-place major version upgrades. The service provides the flexibility to skip versions and upgrade directly to later versions.
- During an in-place major version upgrade of a server which is enabled for high availability (HA), the service disables HA, performs the upgrade on the primary server, and then re-enables HA after the upgrade is complete. Re-enabling HA requires sufficient capacity to provision a new standby instance.
- Most extensions are automatically upgraded to later versions during an in-place major version upgrade, with [some exceptions](#upgrade-considerations-and-limitations).
- The process of an in-place major version upgrade for an Azure Database for PostgreSQL flexible server instance automatically deploys the latest supported minor version.
- Upgrade duration depends on the size and complexity of your database, including the number of objects (tables, indexes, schemas), large objects, and extensions. Larger or more complex workloads may experience longer upgrade times.
- Long-running transactions or high workload before the upgrade might increase the time taken to shut down the database and increase upgrade time.
- After an in-place major version upgrade is successful, there are no automated ways to revert to the earlier version. You can perform a point-in-time recovery (PITR) to a time before the upgrade to restore the previous version on a new server.
- Your Azure Database for PostgreSQL flexible server instance takes a snapshot of your database during an upgrade. The snapshot is taken before the upgrade starts. If the upgrade fails, the system automatically restores your database to its state from the snapshot.
- [PostgreSQL 16 introduces role-based security](../security/security-overview.md) measures. After a major version upgrade on an Azure Database for PostgreSQL flexible server instance, the first user created on the server—who is granted the ADMIN option—will now have administrative privileges over other roles for essential maintenance operations.

## Upgrade Considerations and Limitations

If a precheck operation fails during an in-place major version upgrade, the upgrade is blocked with a detailed error message. Below are the known limitations that can cause the upgrade to fail or behave unexpectedly:

### Unsupported Server Configurations

- [Read replicas](../read-replica/concepts-read-replicas-geo.md) are not supported during in-place upgrades. You must delete the read replica (including any cascading read replica) before upgrading the primary server. After the upgrade, you can re-create the replica.
- Network traffic rules may block upgrade operations. 
    - Ensure your flexible server instance can send/receive traffic on ports 5432 and 6432 within its virtual network and to Azure Storage (for log archiving).
    - If Network Security Groups (NSGs) restrict this traffic, HA will not re-enable automatically post-upgrade. You may need to manually update NSG rules and re-enable HA.
- Logical replication slots must be dropped before performing an in-place major version upgrade. You can recreate them after the upgrade is complete.
- Views dependent on `pg_stat_activity` are not supported during major version upgrades.
- If you are performing the upgrade from PG11 to a higher version, you must first configure your flexible server to use [SCRAM authentication ](../security/security-connect-scram.md#configure-scram-authentication) by enabling SCRAM and resetting all login-role passwords.

### Extension Limitations

In-place major version upgrades do not support all PostgreSQL extensions. The upgrade will fail during the precheck if unsupported extensions are found.
- The following extensions are supported for regular use, **but will block an in-place major version upgrade if present**. Remove them before the upgrade and re-enable them after, if supported on the target version: `timescaledb`, `postgres_fdw`.
- The following extensions are **non-persistent utility extensions** and will need to be dropped and re-created after the upgrade by design: `pg_repack`, `hypopg`.
- When upgrading to PostgreSQL 17 and above, the following extensions are **not supported** and must be removed before upgrade. You may re-enable them only if supported on the target version: `age`, `azure_ai`, `hll`, `pg_diskann`, `pgrouting`.

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

Use `PG_Upgrade_Logs` to monitor upgrade progress and troubleshoot issues.

### Enable upgrade logs using server log parameters:
- Set `logfiles.download_enable` to ON.
- Configure retention with `logfiles.retention_days`.

See [Configure capture of PostgreSQL server logs and major version upgrade logs](../monitor/how-to-configure-server-logs.md) to get started.

### Access PG_Upgrade_Logs from the server logs UI.

- Review `PG_Upgrade_Logs` during and after the upgrade to monitor progress and diagnose failures or delays.
- Check for errors or warnings if the upgrade fails or takes longer than expected.
- Use logs to identify blocking issues and take corrective action quickly.

### Benefits of using upgrade logs
- Diagnose issues quickly: Use `PG_Upgrade_Logs` to review each step of the upgrade and identify errors or warnings.
- Troubleshoot efficiently: Analyze logs to pinpoint failures, reduce downtime, and take corrective action faster.

`PG_Upgrade_Logs` helps you understand what happened during the upgrade and resolve issues with confidence.

> [!NOTE]  
> In-place major version upgrades are supported on [automigrated servers](../migrate/automigration-single-to-flexible-postgresql.md). After a successful in-place Major Version Upgrade on an automigrated server, the username format **username@servername** will no longer be supported. Instead, you must use the standard format: **username**.
To avoid authentication issues, carefully review and update all connection strings in your applications and scripts to ensure they use the updated username format after the upgrade.

## Related content

- [Major version upgrade](how-to-perform-major-version-upgrade.md?tabs=portal).
- [High availability in Azure Database for PostgreSQL](/azure/reliability/reliability-postgresql-flexible-server).
- [Backup and restore in Azure Database for PostgreSQL](../backup-restore/concepts-backup-restore.md).