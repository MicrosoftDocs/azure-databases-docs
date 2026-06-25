---
title: Major Version Upgrades
description: Learn how to use Azure Database for PostgreSQL to do in-place major version upgrades of PostgreSQL on a server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 06/15/2026
ms.service: azure-database-postgresql
ms.subservice: configuration
ms.topic: concept-article
ms.custom:
  - references_regions
  - build-2026
---

# Major version upgrades in Azure Database for PostgreSQL flexible server

Your Azure Database for PostgreSQL flexible server instance supports PostgreSQL versions [!INCLUDE [supported-versions](../includes/major-versions-ascending.md)]. The Postgres community releases a new major version that contains new features about once a year. Additionally, each major version receives periodic bug fixes in the form of minor releases. Minor version upgrades include changes that are backward compatible with existing applications. An Azure Database for PostgreSQL flexible server instance periodically updates the minor versions during a customer's maintenance window.

Major version upgrades are more complicated than minor version upgrades. They can include internal changes and new features that might not be backward compatible with existing applications.

Your Azure Database for PostgreSQL flexible server instance has a feature that performs an in-place major version upgrade of the server. This feature simplifies the upgrade process by minimizing the disruption to users and applications that access the server.

In-place upgrades retain the server name and other settings of the current server after the upgrade of a major version. They don't require data migration or changes to the application connection strings. In-place upgrades are faster and involve shorter downtime than data migration.

> [!NOTE]
> Azure Database for PostgreSQL supports in-place major version upgrades only to currently supported PostgreSQL versions. The target version must be officially supported by Azure at the time of the upgrade. The Azure portal prevents selecting unsupported versions, but API or CLI calls that target a deprecated version will fail. Always consult the [Azure PostgreSQL versioning policy](/azure/postgresql/flexible-server/concepts-version-policy) and [upgrade how-to guide](/azure/postgresql/flexible-server/how-to-perform-major-version-upgrade) before initiating a major version upgrade.

## Upgrade Validation Checks (Preview)

Azure Database for PostgreSQL flexible server provides Upgrade Validation Checks to help assess upgrade readiness before starting a major version upgrade.

Upgrade Validation Checks run a series of compatibility and configuration validations against the server to identify conditions that could cause the upgrade to fail or behave unexpectedly. Common checks include unsupported extensions, logical replication slots, prepared transactions, event triggers, unsupported object dependencies, and pending restart-required configuration changes.

The validation process is designed to evaluate upgrade readiness without initiating the actual upgrade operation. The same validation checks are also performed automatically during the major version upgrade workflow. These checks don't modify the server version, trigger downtime, or restart the server. We strongly recommend running validation checks before scheduling a production upgrade window.

After the validation completes, one of the following outcomes is returned:

- **No blocking issues detected**: Upgrade Validation Checks completed successfully and didn't identify any issues that would block the upgrade.
- **Blocking issues detected**: Upgrade Validation Checks identified one or more issues that must be resolved before the upgrade can proceed.

Depending on the results, you can either proceed with the upgrade or remediate the reported issues and rerun validation.

### Limitations

When using the Upgrade Validation Checks, consider the following limitations:

- The server status must be **Ready**.
- Validation checks aren't supported on read replicas.
- Validation can't run while another server operation is already in progress.
- Validation checks require connectivity to all databases on the server. Unresponsive or inaccessible databases can cause validation failures.
- Although validation checks don't cause downtime, consider running them during periods of lower database activity.

For step-by-step instructions, see [Run upgrade validation checks (Preview)](how-to-run-upgrade-validation-checks.md).

## Upgrade process

Here are some of the important considerations with in-place major version upgrades:

- Before starting the upgrade, ensure that your server has at least 10-20% free storage available. During the upgrade process, temporary log files and metadata operations might increase disk usage. Insufficient free space can result in upgrade failures or rollback issues.
- During the process of an in-place major version upgrade, your Azure Database for PostgreSQL flexible server instance runs a precheck procedure to identify any potential issues that might cause the upgrade to fail.
  - If the precheck finds any incompatibilities, it creates a log event that shows that the upgrade precheck failed, along with an error message.
  - If the precheck is successful, the Azure Database for PostgreSQL flexible server instance stops the service and takes an implicit backup just before starting the upgrade. The service can use this implicit backup to restore the database instance to its previous version if there's an upgrade error.
- An Azure Database for PostgreSQL flexible server instance uses the [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) tool to perform in-place major version upgrades. The service provides the flexibility to skip versions and upgrade directly to later versions.
- During an in-place major version upgrade of a server, which is enabled for high availability (HA), the service disables HA, performs the upgrade on the primary server, and then re-enables HA after the upgrade is complete. Re-enabling HA requires sufficient capacity to provision a new standby instance.
- Most extensions are automatically upgraded to later versions during an in-place major version upgrade, with [some exceptions](#upgrade-considerations-and-limitations).
- The process of an in-place major version upgrade for an Azure Database for PostgreSQL flexible server instance automatically deploys the latest supported minor version.
- Upgrade duration depends on the size and complexity of your database, including the number of objects (tables, indexes, schemas), large objects, and extensions. Larger or more complex workloads might experience longer upgrade times.
- Long-running transactions or high workload before the upgrade might increase the time taken to shut down the database and increase upgrade time.
- After an in-place major version upgrade is successful, there are no automated ways to revert to the earlier version. You can perform a point-in-time recovery (PITR) to a time before the upgrade to restore the previous version on a new server.
- Your Azure Database for PostgreSQL flexible server instance takes an implicit backup of your database during an upgrade. The implicit backup is taken before the upgrade starts. If the upgrade fails, the system automatically restores your database to its state from the implicit backup.
- [Secure your Azure Database for PostgreSQL Server](../security/security-overview.md) measures. After a major version upgrade on an Azure Database for PostgreSQL flexible server instance, the first user created on the server, who is granted the ADMIN option, now has administrative privileges over other roles for essential maintenance operations.

## Upgrade considerations and limitations

If a precheck operation fails during an in-place major version upgrade, the upgrade is blocked with a detailed error message. The following are the known limitations that can cause the upgrade to fail or behave unexpectedly:

### Unsupported server configurations

- [Geo-replication in Azure Database for PostgreSQL](../read-replica/concepts-read-replicas-geo.md) aren't supported during in-place upgrades. You must delete the read replica (including any cascading read replica) before upgrading the primary server. After the upgrade, you can re-create the replica.
- Network traffic rules might block upgrade operations.
  - Ensure your flexible server instance can send/receive traffic on ports 5432 and 6432 within its virtual network and to Azure Storage (for log archiving).
  - If Network Security Groups (NSGs) restrict this traffic, HA won't re-enable automatically post-upgrade. You might need to manually update NSG rules and re-enable HA.
- Logical replication slots must be dropped before performing an in-place major version upgrade. You can recreate them after the upgrade is complete.
- Views dependent on `pg_stat_activity` aren't supported during major version upgrades.
- If you're performing the upgrade from PostgreSQL 11 to a higher version, you must first configure your flexible server to use [SCRAM authentication](../security/security-connect-scram.md#configure-scram-authentication) by enabling SCRAM and resetting all login-role passwords.

### Extension limitations

In-place major version upgrades don't support all PostgreSQL extensions. The upgrade fails during the precheck if a blocked extension is present on an affected upgrade path. Most blocks are scoped to specific **target** (and sometimes **source**) versions rather than every upgrade, as noted in the following lists.

- The following extensions **block an in-place major version upgrade on all upgrade paths**. Remove them before the upgrade and re-enable them after, if supported on the target version: `session_variable`, `anon`, `age`, `pg_duckdb`.
- The following extensions are **non-persistent utility extensions** and must be dropped before the upgrade and re-created after, by design (all upgrade paths): `pg_repack`, `hypopg`, `pg_partman`.
- The following extensions are blocked only on **specific version paths**. Remove them before the upgrade if your upgrade matches the listed condition, and re-enable them after if supported on the target version:

  | Extension | Blocked when |
  | --- | --- |
  | `pg_hint_plan` | Target version is PostgreSQL 14 |
  | `semver` | Target version is PostgreSQL 16 or 17 |
  | `azure_local_ai` | Target version is PostgreSQL 17 or 18 |
  | `pg_failover_slots` | Target version is PostgreSQL 17 or 18 (shared preload library) |
  | `azure_ai` | Target version is PostgreSQL 18 |
  | `azure_storage` | Target version is PostgreSQL 18 |
  | `pg_diskann` | Target version is PostgreSQL 18 |
  | `pgrouting` | Target version is PostgreSQL 15; or source is earlier than PostgreSQL 16 and target is PostgreSQL 16 or later; or target version is PostgreSQL 18 |
  | `orafce` | Source version is PostgreSQL 11, 12, or 13 |

- The following extensions are blocked when other database objects **depend on their objects**, because the upgrade would otherwise fail. Resolve the dependencies before the upgrade:
  - `pg_stat_statements`: blocked when other objects depend on its view or function, which would cause `ALTER EXTENSION pg_stat_statements UPDATE` to fail. Remove the dependent objects first.
  - `pgcrypto`: when installed in the `pg_catalog` schema and upgrading from PostgreSQL 11 or 12 to PostgreSQL 13 or later, blocked when customer objects depend on it (a conflict with the built-in `gen_random_uuid()` function). Relocate the extension to another schema or drop the dependent objects first.

### PostGIS-specific considerations

If you're using PostGIS or any dependent extensions, you must configure the search_path parameter to include:
- Schemas related to PostGIS
- Dependent extensions, including: `postgis`, `postgis_raster`, `postgis_sfcgal`, `postgis_tiger_geocoder`, `postgis_topology`, `address_standardizer`, `address_standardizer_data_us`, `fuzzystrmatch`
- Failure to configure the search_path correctly can lead to upgrade failures or broken objects post-upgrade.

### TimescaleDB-specific considerations

If you're using [TimescaleDB](../extensions/concepts-extensions-versions.md), in-place major version upgrades are supported only for specific PostgreSQL source and target version combinations:

| Source PostgreSQL version | Supported target versions |
| ------------------------- | ------------------------- |
| PostgreSQL 11             | PostgreSQL 12             |
| PostgreSQL 12             | PostgreSQL 13, 14, 15     |
| PostgreSQL 13             | PostgreSQL 14, 15, 16     |
| PostgreSQL 14             | PostgreSQL 15, 16         |
| PostgreSQL 15             | PostgreSQL 16, 17, 18     |
| PostgreSQL 16             | PostgreSQL 17, 18         |
| PostgreSQL 17             | PostgreSQL 18             |

If your TimescaleDB upgrade path isn't listed in the supported matrix, the in-place major version upgrade is blocked. To proceed, either drop the TimescaleDB extension before upgrade, if feasible, or use an alternate migration approach such as [side-by-side migration with logical replication](https://techcommunity.microsoft.com/blog/adforpostgresql/upgrade-azure-database-for-postgresql-with-minimal-downtime-using-logical-replic/4466784).

Ensure that your source and target versions are included in the supported matrix before starting the upgrade.

### Other upgrade considerations

- Event triggers: Upgrade precheck blocks event triggers because they hook into DDL commands and might reference system catalogs that change between major versions. Drop all `EVENT TRIGGER`s before upgrading and then recreate them after the upgrade to ensure a smooth upgrade.
- Large objects (LOs): Databases with millions of large objects (stored in `pg_largeobject`) can cause upgrade failures due to high memory usage or log volume. Use [vacuumlo](https://www.postgresql.org/docs/current/vacuumlo.html) utility to clean up unused LOs, and consider scaling up your server before upgrade if many LOs are still in use.

> [!WARNING]  
> Use caution with vacuumlo. `vacuumlo` identifies orphaned large objects based on conventional reference columns (oid, lo). If your application uses custom or indirect reference types, valid large objects might be mistakenly deleted. Additionally, `vacuumlo` might consume significant CPU, memory, and IOPS, especially in databases with millions of large objects. Run it during maintenance windows and test on nonproduction first.

## Post upgrade

After the major version upgrade is complete, run the `ANALYZE` command in each database to refresh the [`pg_statistic`](https://www.postgresql.org/docs/current/catalog-pg-statistic.html) table. Missing or stale statistics can lead to bad query plans, which in turn might degrade performance and take up excessive memory.

```sql
postgres=> analyze;
ANALYZE
```

## View upgrade logs

Use `PG_Upgrade_Logs` to monitor upgrade progress and troubleshoot issues.

### Enable upgrade logs using server log parameters

- Set `logfiles.download_enable` to ON.
- Configure retention with `logfiles.retention_days`.

See [Download PostgreSQL and upgrade logs](../monitor/how-to-configure-server-logs.md) to get started.

### Access PG_Upgrade_Logs from the server logs UI

- Review `PG_Upgrade_Logs` during and after the upgrade to monitor progress and diagnose failures or delays.
- Check for errors or warnings if the upgrade fails or takes longer than expected.
- Use logs to identify blocking issues and take corrective action quickly.

### Benefits of using upgrade logs

- Diagnose issues quickly: Use `PG_Upgrade_Logs` to review each step of the upgrade and identify errors or warnings.
- Troubleshoot efficiently: Analyze logs to pinpoint failures, reduce downtime, and take corrective action faster.

`PG_Upgrade_Logs` helps you understand what happened during the upgrade and resolve issues with confidence.

> [!NOTE]  
> In-place major version upgrades are supported on [automigrated servers](../migrate/automigration-single-to-flexible-postgresql.md). After a successful in-place major version upgrade on an automigrated server, the username format **username@servername** will no longer be supported. Instead, you must use the standard format: **username**.
To avoid authentication issues, carefully review and update all connection strings in your applications and scripts to ensure they use the updated username format after the upgrade.

## Related content

- [Major version upgrade](how-to-perform-major-version-upgrade.md?tabs=portal)
- [Run upgrade validation checks (Preview)](how-to-run-upgrade-validation-checks.md)
