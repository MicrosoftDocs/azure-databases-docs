---
title: Citus Upgrade
description: Learn how to upgrade Citus versions on your PostgreSQL cluster, including patch upgrades for minor updates, and major version upgrades.
ms.date: 02/11/2026
ms.service: postgresql-citus
ms.topic: concept-article
ai-usage: ai-assisted
monikerRange: "citus-13 || citus-14"
---

# Citus upgrade

Keeping your Citus extension up to date ensures you have access to the latest features, performance improvements, and bug fixes. This guide covers the process of upgrading Citus versions on your PostgreSQL cluster, including both patch upgrades for minor updates and major version upgrades that might include new capabilities. Understanding the upgrade process helps you maintain a secure and efficient distributed database environment while minimizing downtime and ensuring compatibility with your applications.

## Upgrade Citus versions

To upgrade the Citus version, first get the new Citus extension. Then, install it in each of your database instances. Citus uses separate packages for each minor version. This approach ensures that running a default package upgrade provides bug fixes but never breaks anything. Let's start by examining patch upgrades, the easiest kind.

### Patch version upgrade

To upgrade a Citus version to its latest patch, run a standard upgrade command for your package manager. Assume version 13.0 is currently installed on PostgreSQL 16:

**Ubuntu or Debian**

```bash
sudo apt-get update
sudo apt-get install --only-upgrade postgresql-16-citus-13.0
sudo service postgresql restart
```

**Red Hat**

```bash
sudo yum update citus130_16
sudo service postgresql-16 restart
```

### Major and minor version upgrades

Major and minor version upgrades follow the same steps, but be careful: they can make backward-incompatible changes in the Citus API. Review the Citus [changelog](https://github.com/citusdata/citus/blob/master/CHANGELOG.md) before an upgrade and look for any changes that might cause problems for your application.

> [!NOTE]  
> Starting at version 8.1, new Citus nodes expect and require encrypted inter-node communication by default, whereas nodes upgraded to 8.1 from an earlier version preserve their earlier SSL settings. Be careful when adding a new Citus 8.1 (or newer) node to an upgraded cluster that doesn't yet use SSL. The adding a worker section covers that situation.

Each major and minor version of Citus is published as a package with a separate name. Installing a newer package automatically removes the older version.

#### Step 1. Update Citus package

If you upgrade both Citus and PostgreSQL, always upgrade the Citus extension first, and upgrade the PostgreSQL version second (see `Upgrade_postgres`). Here's how to do a Citus upgrade from 12.1 to 13.0 on PostgreSQL 16:

**Ubuntu or Debian**

```bash
sudo apt-get update
sudo apt-get install postgresql-16-citus-13.0
sudo service postgresql restart
```

**Red Hat**

```bash
# Fedora, CentOS, or Red Hat
sudo yum swap citus121_16 citus130_16
sudo service postgresql-16 restart
```

#### Step 2. Apply update in database

After installing the new package and restarting the database, run the extension upgrade script.

```sql
-- you must restart PostgreSQL before running this
ALTER EXTENSION citus UPDATE;

-- you should see the upgraded Citus version
SELECT * FROM citus_version();

-- Run this procedure during one of these upgrade paths:
--   * upgrading to Citus 11 or later while still on a pre-11 version, OR
--   * upgrading to Citus 14 or later while still on a pre-14 version.
-- Run it on the coordinator node.
CALL citus_finish_citus_upgrade();
```

> [!NOTE]  
> - If you upgrade to Citus 13.x from an earlier major version, the `citus_finish_citus_upgrade()` procedure ensures that all worker nodes have the right schema and metadata. It might take several minutes to run, depending on how much metadata needs to be synced.
> - If you upgrade to Citus 14.x from an earlier major version, `citus_finish_citus_upgrade()` also fixes any colocation groups where the registered collation columns don't match the distribution columns of the tables in the group. This is a metadata-only operation (no data movement) that updates `pg_dist_colocation` and `pg_dist_partition` on all nodes if needed.

During a major version upgrade, from the moment of yum installing a new version, Citus doesn't run distributed queries until the server is restarted and `ALTER EXTENSION` is executed. This stipulation protects your data, as Citus object and function definitions are specific to a version. After a yum install, you should (a) restart and (b) run alter extension. In rare cases if you experience an error with upgrades, you can disable this check via the `citus.enable_version_checks <enable_version_checks>` configuration parameter. You can also [contact us](https://www.citusdata.com/about/contact_us) providing information about the error, so we can help debug the issue.

## Upgrade PostgreSQL version from 16 to 17

> [!NOTE]  
> Don't attempt to upgrade *both* Citus and PostgreSQL versions at once. If you want to upgrade both, upgrade Citus first.
>
> Also, if you're running Citus 10.0 or 10.1, don't upgrade your PostgreSQL version. Upgrade to at least Citus 10.2 and then perform the PostgreSQL upgrade.

Before you start, record the following paths. Your actual paths might be different from the paths listed here:

Existing data directory (for example, `/opt/pgsql/16/data`)  
`export OLD_PG_DATA=/opt/pgsql/16/data`

Existing PostgreSQL installation path (for example, `/usr/pgsql-16`)  
`export OLD_PG_PATH=/usr/pgsql-16`

New data directory after upgrade  
`export NEW_PG_DATA=/opt/pgsql/17/data`

New PostgreSQL installation path  
`export NEW_PG_PATH=/usr/pgsql-17`

### For every node

Follow these steps to upgrade the PostgreSQL version with Citus on every node (coordinator and workers):

1. Back up Citus metadata.

   ```sql
   -- run this on the coordinator and worker nodes

   SELECT citus_prepare_pg_upgrade();
   ```

1. Configure the new database instance to use Citus.

   - Include Citus as a shared preload library in `postgresql.conf`.

     ``` ini
     shared_preload_libraries = 'citus'
     ```

   - **DO NOT CREATE** a Citus extension.
   - **DO NOT** start the new server yet.

1. Stop the old server.

1. Check upgrade compatibility.

   ```bash
   $NEW_PG_PATH/bin/pg_upgrade -b $OLD_PG_PATH/bin/ -B $NEW_PG_PATH/bin/ \
                               -d $OLD_PG_DATA -D $NEW_PG_DATA --check
   ```

   You should see a "Clusters are compatible" message. If you don't, fix any errors before proceeding. Ensure that:

   - `NEW_PG_DATA` contains an empty database initialized by new PostgreSQL version
   - The Citus extension **IS NOT** created

1. Perform the upgrade (like before but without the `--check` option).

   ```bash
   $NEW_PG_PATH/bin/pg_upgrade -b $OLD_PG_PATH/bin/ -B $NEW_PG_PATH/bin/ \
   -d $OLD_PG_DATA -D $NEW_PG_DATA
   ```

1. If you didn't set up the Transport Layer Security (TLS) configuration yourself, Citus does that and you need to copy the Citus-generated `postgresql.auto.conf` file along with the generated certificate files (`server.crt` and `server.key`).

   ```bash
   cp $OLD_PG_DATA/postgresql.auto.conf $NEW_PG_DATA/
   cp $OLD_PG_DATA/server.crt $NEW_PG_DATA/
   cp $OLD_PG_DATA/server.key $NEW_PG_DATA/
   ```

1. Start the new server.

1. **DO NOT** run any query before running the queries given in the next step.

1. Restore metadata on new coordinator node.

   ```sql
   -- run this on the coordinator and worker nodes

   SELECT citus_finish_pg_upgrade();
   ```

## Related content

- [Cluster management in Citus](cluster-management.md)
- [Citus table management](table-management.md)
- [Diagnostic queries for Citus](diagnostic-queries.md)
- [What is Citus?](what-is-citus.md)
