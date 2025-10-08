---
title: Considerations with the Use of Extensions and Modules
description: Learn about the extension considerations specific to an Azure Database for PostgreSQL flexible server instance.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 03/26/2025
ms.service: azure-database-postgresql
ms.subservice: extensions
ms.topic: concept-article
ms.custom:
  - build-2025
---

# Considerations with the use of extensions and modules

This article describes some special considerations that you must be aware of, when using certain extensions or modules in an Azure Database for PostgreSQL flexible server instance.

## Generic considerations with extensions

To use an extension in your Azure Database for PostgreSQL flexible server instance, you have to:

- [Allow extension](how-to-allow-extensions.md). If the extension isn't allowed, any attempt to execute `CREATE EXTENSION`, `ALTER EXTENSION`, `DROP EXTENSION`, or `COMMENT ON EXTENSION` fails with an error indicating that the referred extension isn't allowed.
- If the extension deploys some shared binary library which requires allocating and accessing shared memory, and need to be loaded when the server starts, you should also follow the instructions provided in [load libraries](how-to-load-libraries.md).
- [Create extension](how-to-create-extensions.md) in the databases in which you want the extension to deploy the SQL objects distributed with that extension.
- [Drop extension](how-to-drop-extensions.md). When you want to remove from the database in which you execute the command all the SQL objects distributed by that extension.
- [Update extensions](how-to-update-extensions.md), to update to its newest version all the SQL artifacts deployed by an extension that is already installed.
- [View installed extensions](how-to-view-installed-extensions.md) and their corresponding versions.

If you get any error while executing the `CREATE EXTENSION`, `ALTER EXTENSION`, `DROP EXTENSION` or `COMMENT ON EXTENSION` commands on your Azure Database for PostgreSQL flexible server instance, see the list of [possible errors](errors-extensions.md), and what could be the cause of each of those errors.

## Generic considerations with modules

To use a module in your Azure Database for PostgreSQL flexible server instance, you only have to add it to the `shared_preload_libraries` server parameter as described in [load libraries](how-to-load-libraries.md).

Modules don't need to be [allowlisted](how-to-allow-extensions.md). That's an exclusive requirement for extensions.

## Extensions with specific considerations

The following list enumerates all the supported extensions that require specific considerations when used in an Azure Database for PostgreSQL flexible server instance:

- `AGE`
- `dblink`
- `pg_buffercache`
- `pg_cron`
- `pg_hint_plan`
- `pg_prewarm`
- `pg_repack`
- `pg_stat_statements`
- `postgres_fdw`
- `pgstattuple`
 
### AGE

The Apache AGE extension is a graph extension for PostgreSQL supported by Azure Database for PostgreSQL. It provides graph database functionalities, open cypher query support, and the ability to execute complex queries on graph data stored in PostgreSQL. ['Apache AGE'](https://age.apache.org/) is an open-source project released under the Apache License 2.0. 

#### Install AGE
To use AGE, make sure that you ['allowlist'](/azure/postgresql/extensions/how-to-allow-extensions) the extension, ['load its library'](/azure/postgresql/extensions/how-to-load-libraries), and ['install the extension'](/azure/postgresql/extensions/how-to-create-extensions) in the database on which you plan to use its functionality. 

### dblink

The [`dblink`](https://www.postgresql.org/docs/current/contrib-dblink-function.html) extension allows you to connect from one Azure Database for PostgreSQL flexible server instance to another or another database in the same server. Azure Database for PostgreSQL supports both incoming and outgoing connections to any PostgreSQL server. The sending server needs to allow outbound connections to the receiving server. Similarly, the receiving server needs to allow connections from the sending server.

If you plan to use this extension, we recommend deploying your servers with [virtual network integration](../flexible-server/concepts-networking-private.md). By default, virtual network integration allows connections between servers in the virtual network. You can also choose to use [virtual network network security groups](/azure/virtual-network/manage-network-security-group) to customize access.

### pg_buffercache

The `pg_buffercache` extension can be used to study the contents of *shared_buffers*. Using [this extension](https://www.postgresql.org/docs/current/pgbuffercache.html), you can tell whether a particular relation is cached (in `shared_buffers`). This extension can help you troubleshoot performance issues (caching-related performance issues).

This extension is integrated with the core installation of PostgreSQL, and it's easy to install.

```sql
CREATE EXTENSION pg_buffercache;
```

### pg_cron

The [`pg_cron`](https://github.com/citusdata/pg_cron/) extension is a simple, cron-based job scheduler for PostgreSQL that runs inside the database as an extension. The `pg_cron` extension can run scheduled maintenance tasks within a PostgreSQL database. For example, you can run a periodic vacuum of a table or remove old data jobs.

The `pg_cron` extension can run multiple jobs in parallel, but it runs at most one instance of a job at a time. If a second run is supposed to start before the first one finishes, then the second run is queued and started as soon as the first run completes. In such a way, it ensures that jobs run precisely as many times as scheduled and don't run concurrently with themselves.

Make sure that the value to which `shared_preload_libraries` is set, includes `pg_cron`. This extension doesn't support loading the library as the effect of executing [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html). Any attempt to run CREATE EXTENSION if the extension wasn't added to `shared_preload_libraries`, or the server wasn't restarted after it was added, results in an error whose text says `pg_cron can only be loaded via shared_preload_libraries`, and whose hint is `Add pg_cron to the shared_preload_libraries configuration variable in postgresql.conf`.

To use `pg_cron`, make sure you [load its shared library upon server start](how-to-load-libraries.md), it's [allowlisted](how-to-allow-extensions.md#allow-extensions), and it's [installed](how-to-create-extensions.md) in any database from which you want to interact with its functionality, using the SQL artifacts it creates.

#### Examples

1. To delete old data on Saturday at 3:30 am (GMT).

    ```sql
    SELECT cron.schedule('30 3 * * 6', $$DELETE FROM events WHERE event_time < now() - interval '1 week'$$);
    ```

1. To run the vacuum every day at 10:00 am (GMT) in the default database `postgres`.

    ```sql
    SELECT cron.schedule('0 10 * * *', 'VACUUM');
    ```

1. To unschedule all tasks from `pg_cron`.

    ```sql
    SELECT cron.unschedule(jobid) FROM cron.job;
    ```

1. To see all jobs currently scheduled with `pg_cron`.

    ```sql
    SELECT * FROM cron.job;
    ```

1. To run the vacuum every day at 10:00 am (GMT) in the database `test cron` under the `azure_pg_admin` role account.

    ```sql
    SELECT cron.schedule_in_database('VACUUM',' 0 10 * * * ', 'VACUUM', 'testcron',null,TRUE);
    ```

#### More examples

Starting with `pg_cron` version 1.4, you can use the `cron.schedule_in_database` and `cron.alter_job` functions to schedule your job in a specific database and update an existing schedule, respectively.

The `cron_schedule_in_database` function allows for the user name as an optional parameter. Setting the username to a non-null value requires PostgreSQL superuser privilege and isn't supported for an Azure Database for PostgreSQL flexible server instance. Preceding examples show running this function with an optional user name parameter omitted or set to null, which runs the job in the context of the user scheduling the job, which should have `azure_pg_admin` role privileges.

1. To delete old data on Saturday at 3:30 am (GMT) on database DBName.

    ```sql
    SELECT cron.schedule_in_database('JobName', '30 3 * * 6', $$DELETE FROM events WHERE event_time < now() - interval '1 week'$$,'DBName');
    ```

1. To update or change the database name for the existing schedule

    ```sql
    SELECT cron.alter_job(job_id:=MyJobID,database:='NewDBName');
    ```

### pg_hint_plan

The `pg_hint_plan` extension makes it possible to tweak PostgreSQL execution plans using so-called "hints" in SQL comments, like:

```sql
/*+ SeqScan(a) */
```

The `pg_hint_plan` extension reads hinting phrases in a comment of the special form given with the target SQL statement. The particular form begins with the character sequence "/\*+" and ends with "\*/". Hint phrases consist of hint names and following parameters enclosed by parentheses and delimited by spaces. New lines for readability can delimit each hinting phrase.

Example:

```sql
/*+
 HashJoin(a b)
 SeqScan(a)
 */
    SELECT *
    FROM pgbench_branches b
    JOIN pgbench_accounts an ON b.bid = a.bid
    ORDER BY a.aid;
```

The previous example causes the planner to use the results of a `seqscan` on table `a` to combine with table `b` as a `hashjoin`.

To use `pg_hint_plan` extension, make sure that you [allowlist](how-to-allow-extensions.md#allow-extensions) the extension, [load its library](how-to-load-libraries.md), and [install the extension](how-to-create-extensions.md) in the database on which you plan to use its functionality.

### pg_prewarm

The `pg_prewarm` extension loads relational data into the cache. Prewarming your caches means your queries have better response times on their first run after a restart. The autoprewarm functionality for the PostgreSQL isn't currently available in the Azure Database.

### pg_repack

First time users of the `pg_repack` extension typically ask the following question: Is `pg_repack` an extension or a client-side executable like `psql` or `pg_dump`?

pg_repack is actually both. [pg_repack/lib](https://github.com/reorg/pg_repack/tree/master/lib) has the code for the extension, including the schema and SQL artifacts it creates, and the C library implementing the code of several of those functions.

On the other hand, [pg_repack/bin](https://github.com/reorg/pg_repack/tree/master/bin) has the code for the client application, which knows how to interact with the programmability elements implemented in the extension. This client application aims to ease the complexity of interacting with the different interfaces surfaced by the server-side extension. It offers the user some command-line options which are easier to understand. The client application is useless without the extension created on the database it's being pointing to. The server side extension on its own would be fully functional, but would require the user to understand a complicated interaction pattern. That pattern would consist on executing queries to retrieve data that is used as input to functions implemented by the extension, etc.

#### Permission denied for schema repack

Currently, because we grant permissions to the repack schema created by this extension, we only support running `pg_repack` functionality from the context of `azure_pg_admin`.

You might notice that if the owner of a table, who isn't `azure_pg_admin`, tries to run `pg_repack`, they end up receiving the following error:

```sql
NOTICE: Setting up workers.conns
ERROR: pg_repack failed with error: ERROR:  permission denied for schema repack
LINE 1: select repack.version(), repack.version_sql()
```

To avoid that error, run pg_repack from the context of `azure_pg_admin`.

### pg_stat_statements

The [pg_stat_statements extension](https://www.postgresql.org/docs/current/pgstatstatements.html) gives you a view of all the queries that run on your database. This information is useful for understanding your query workload performance on a production system.

The [pg_stat_statements extension](https://www.postgresql.org/docs/current/pgstatstatements.html) is preloaded in `shared_preload_libraries` on every Azure Database for PostgreSQL flexible server instance to provide a means of tracking SQL statement execution statistics.

For security reasons, you must [allowlist](how-to-allow-extensions.md#allow-extensions) the [pg_stat_statements extension](https://www.postgresql.org/docs/current/pgstatstatements.html) and install it using [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command.

The setting `pg_stat_statements.track`, which controls what statements the extension tracks, defaults to `top`, meaning all statements issued directly by clients are tracked. The two other tracking levels are `none` and `all`. This setting is configurable as a server parameter.

There's a tradeoff between the query execution information the `pg_stat_statements` extension provides on the server performance as it logs each SQL statement. If you aren't actively using the `pg_stat_statements` extension, we recommend that you set `pg_stat_statements.track` to `none`. Some third-party monitoring services might rely on `pg_stat_statements` to deliver query performance insights, so confirm whether it's the case for you.

### postgres_fdw

The [`postgres_fdw`](https://www.postgresql.org/docs/current/postgres-fdw.html) extension allows you to connect from one Azure Database for PostgreSQL flexible server instance to another or another database in the same server. Azure Database for PostgreSQL supports both incoming and outgoing connections to any PostgreSQL server. The sending server needs to allow outbound connections to the receiving server. Similarly, the receiving server needs to allow connections from the sending server.

If you plan to use this extension, we recommend deploying your servers with [virtual network integration](../flexible-server/concepts-networking-private.md). By default, virtual network integration allows connections between servers in the virtual network. You can also choose to use [virtual network network security groups](/azure/virtual-network/manage-network-security-group) to customize access.

### pgstattuple

When using the `pgstattuple` extension to try to obtain tuple statistics from objects kept in the `pg_toast` schema in versions of Postgres 11 through 13, you receive a "permission denied for schema pg_toast" error.

#### Permission denied for schema pg_toast

Customers using PostgreSQL versions 11 through 13 on Azure Database for PostgreSQL flexible server instance can't use the `pgstattuple` extension on objects within the `pg_toast` schema.

In PostgreSQL 16 and 17, the `pg_read_all_data` role is automatically granted to `azure_pg_admin`, allowing `pgstattuple` to function correctly. In PostgreSQL 14 and 15, customers can manually grant the `pg_read_all_data` role to `azure_pg_admin` to achieve the same result. However, in PostgreSQL 11 through 13, the `pg_read_all_data` role doesn't exist.

Customers can't directly grant the necessary permissions. If you need to be able to run `pgstattuple` to access objects under the `pg_toast` schema, proceed to [create an Azure support request](/azure/azure-portal/supportability/how-to-create-azure-support-request).

### timescaleDB

The `timescaleDB` extension is a time-series database packaged as an extension for PostgreSQL. It provides time-oriented analytical functions and optimizations and scales Postgres for time-series workloads.
[Learn more about TimescaleDB](https://docs.timescale.com/timescaledb/latest/), a registered trademark of Timescale, Inc. Azure Database for PostgreSQL provides the TimescaleDB [Apache-2 edition](https://www.timescale.com/legal/licenses).

#### Install TimescaleDB

To use `timescaleDB`, make sure that you [allowlist](how-to-allow-extensions.md#allow-extensions) the extension, [load its library](how-to-load-libraries.md), and [install the extension](how-to-create-extensions.md) in the database on which you plan to use its functionality.

You can now create a TimescaleDB hypertable [from scratch](https://github.com/timescale/docs.timescale.com-content/blob/master/getting-started/creating-hypertables.md) or migrate [existing time-series data in PostgreSQL](https://github.com/timescale/docs.timescale.com-content/blob/master/getting-started/migrating-data.md).

For more information on restoring a Timescale database using `pg_dump` and `pg_restore`, see [Timescale documentation](https://github.com/timescale/docs.timescale.com-content/blob/master/using-timescaledb/backup.md).

#### Restore a Timescale database using timescaledb-backup

While running the `SELECT timescaledb_post_restore()` procedure, you might get permissions denied when updating timescaledb.restoring flag. The reason why you get this error is because of the limited ALTER DATABASE permission in Cloud PaaS database services. In this case, you can perform an alternative method using the `timescaledb-backup` tool to back up and restore the Timescale database. Timescaledb-backup is a program that makes dumping and restoring a TimescaleDB database simpler, less error-prone, and more performant.

To do so, follow these steps:

1. Install tools as detailed [here](https://github.com/timescale/timescaledb-backup#installing-timescaledb-backup).

1. Create a target Azure Database for PostgreSQL flexible server instance and database.

1. Enable Timescale extension.

1. Grant the `azure_pg_admin` role to the user that is used by [ts-restore](https://github.com/timescale/timescaledb-backup#using-ts-restore).

1. Run [ts-restore](https://github.com/timescale/timescaledb-backup#using-ts-restore) to restore database.

More details on these utilities can be found [here](https://github.com/timescale/timescaledb-backup).

## Extensions and major version upgrade

Azure Database for PostgreSQL offers an [in-place major version upgrade feature](../flexible-server/concepts-major-version-upgrade.md) that performs an in-place upgrade of the Azure Database for PostgreSQL flexible server instance, with just a simple interaction from the user. In-place major version upgrade simplifies the Azure Database for PostgreSQL upgrade process, minimizing the disruption to users and applications accessing the server. In-place major version upgrades don't support specific extensions, and there are some limitations to upgrading certain extensions.

The extensions `anon`, `Apache AGE`, `dblink`, `orafce`, `postgres_fdw`, and `timescaledb` are unsupported for all Azure Database for PostgreSQL flexible server instance versions when using in-place major version update feature.

## Modules with specific considerations

The following list enumerates all the supported modules that require specific considerations when used in an Azure Database for PostgreSQL flexible server instance:

- `pg_failover_slots`

### pg_failover_slots

The `pg_failover_slots` module enhances Azure Database for PostgreSQL when operating with both logical replication and high availability enabled servers. It effectively addresses the challenge within the standard PostgreSQL engine that doesn't preserve logical replication slots after a failover. Maintaining these slots is critical to prevent replication pauses or data mismatches during primary server role changes, ensuring operational continuity and data integrity.

The extension streamlines the failover process by managing the necessary transfer, cleanup, and synchronization of replication slots, thus providing a seamless transition during server role changes.

You can find more information and instructions on using the `pg_failover_slots` module on its [GitHub page](https://github.com/EnterpriseDB/pg_failover_slots).

To use the `pg_failover_slots` module, make sure that its [library was loaded](how-to-load-libraries.md) when the server started.


## Related content

- [Extensions](concepts-extensions.md)
- [Allow extensions](how-to-allow-extensions.md)
- [List of extensions and modules by name](concepts-extensions-versions.md)
- [List of extensions and modules by version of PostgreSQL](concepts-extensions-by-engine.md)
