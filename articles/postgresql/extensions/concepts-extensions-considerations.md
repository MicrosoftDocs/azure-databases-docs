---
title: Extension Considerations Specific to Azure Database for PostgreSQL Flexible Server
description: Learn about the extension considerations specific to Azure Database for PostgreSQL flexible server.
author: varun-dhawan
ms.author: varundhawan
ms.reviewer: maghan
ms.date: 12/12/2024
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
---

# Extension considerations specific to Azure Database for PostgreSQL - Flexible Server

This article describes some special considerations that you must be aware of when using certain extensions in an instance of Azure Database for PostgreSQL flexible server.

## Prerequisites

Read the article [how to use PostgreSQL extensions for Azure Database for PostgreSQL](how-to-allow-extensions.md) to learn how to:

 - Allowlist extensions in Azure Database for PostgreSQL Flexible Server
 - Load the libraries of extensions that deploy binary libraries, which require allocating and accessing shared memory and need to be loaded when the server starts.
 - Install extensions in some database, so that the SQL objects packaged in that extension are deployed in that database, and can be accessed in its context.
 - Drop extensions from some database, so that the SQL objects packaged in that extension are removed from that database.
 - Update the SQL artifacts deployed by an extension that is already installed.
 - View which extensions are installed and their corresponding versions.
 - Learn what are the possible errors you can receive when managing extensions in Azure Database for PostgreSQL Flexible Server, and what could be the cause of each of them.

## Extensions

The following list enumerates all the supported extensions that require specific considerations when used in the Azure Database for PostgreSQL flexible server service:

- `dblink`
- `pg_buffercache`
- `pg_cron`
- `pg_failover_slots`
- `pg_hint_plan`
- `pg_prewarm`
- `pg_repack`
- `pg_stat_statements`
- `postgres_fdw`
- `pgstattuple`

### dblink

The [`dblink`](https://www.postgresql.org/docs/current/contrib-dblink-function.html) extension allows you to connect from one Azure Database for PostgreSQL flexible server instance to another or another database in the same server. Azure Database for PostgreSQL flexible server supports both incoming and outgoing connections to any PostgreSQL server. The sending server needs to allow outbound connections to the receiving server. Similarly, the receiving server needs to allow connections from the sending server.

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

To use `pg_cron`, make sure it's [library is added to be loaded upon server start](how-to-allow-extensions.md#load-libraries), it's [allowlisted](how-to-allow-extensions.md#allow-extensions), and it's [installed](how-to-allow-extensions.md#create-extensions) in any database from which you want to interact with its functionality, using the SQL artifacts it creates.

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

The `cron_schedule_in_database` function allows for the user name as an optional parameter. Setting the username to a non-null value requires PostgreSQL superuser privilege and isn't supported in Azure Database for PostgreSQL flexible server. Preceding examples show running this function with an optional user name parameter omitted or set to null, which runs the job in the context of the user scheduling the job, which should have `azure_pg_admin` role privileges.

1. To delete old data on Saturday at 3:30 am (GMT) on database DBName.

    ```sql
    SELECT cron.schedule_in_database('JobName', '30 3 * * 6', $$DELETE FROM events WHERE event_time < now() - interval '1 week'$$,'DBName');
    ```

1. To update or change the database name for the existing schedule

    ```sql
    SELECT cron.alter_job(job_id:=MyJobID,database:='NewDBName');
    ```

### pg_failover_slots

The `pg_failover_slots` extension enhances Azure Database for PostgreSQL flexible server when operating with both logical replication and high availability enabled servers. It effectively addresses the challenge within the standard PostgreSQL engine that doesn't preserve logical replication slots after a failover. Maintaining these slots is critical to prevent replication pauses or data mismatches during primary server role changes, ensuring operational continuity and data integrity.

The extension streamlines the failover process by managing the necessary transfer, cleanup, and synchronization of replication slots, thus providing a seamless transition during server role changes.

You can find more information and instructions on using the `pg_failover_slots` extension on its [GitHub page](https://github.com/EnterpriseDB/pg_failover_slots).

To use the `pg_failover_slots` extension, make sure that its [library was loaded](how-to-allow-extensions.md#load-libraries) when the server started.

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

To use `pg_hint_plan` extension, make sure that you [allowlist](how-to-allow-extensions.md#allow-extensions) the extension, [load its library](how-to-allow-extensions.md#load-libraries), and [install the extension](how-to-allow-extensions.md#create-extensions) in the database on which you plan to use its functionality.

### pg_prewarm

The `pg_prewarm` extension loads relational data into the cache. Prewarming your caches means your queries have better response times on their first run after a restart. The autoprewarm functionality for the PostgreSQL flexible server isn't currently available in the Azure Database.

### pg_repack

First time users of the `pg_repack` extension typically ask the following question: Is `pg_repack` an extension or a client-side executable like `psql` or `pg_dump`?

pg_repack is actually both. [pg_repack/lib](https://github.com/reorg/pg_repack/tree/master/lib) has the code for the extension, including the schema and SQL artifacts it creates, and the C library implementing the code of several of those functions.

On the other hand, [pg_repack/bin](https://github.com/reorg/pg_repack/tree/master/bin) has the code for the client application, which knows how to interact with the programmability elements implemented in the extension. This client application aims to ease the complexity of interacting with the different interfaces surfaced by the server-side extension. It offers the user some command-line options which are easier to understand. The client application is useless without the extension created on the database it's being pointing to. The server side extension on its own would be fully functional, but would require the user to understand a complicated interaction pattern. That pattern would consist on executing queries to retrieve data that is used as input to functions implemented by the extension, etc.

#### Permission denied for schema repack

Currently, because we grant permissions to the repack schema created by this extension, we only support running `pg_repack` functionality from the context of `azure_pg_admin`.

You might notice that if the owner of a table, who isn't `azure_pg_admin`, tries to run `pg_repack`, they end up receiving an error like the following:

```sql
NOTICE: Setting up workers.conns
ERROR: pg_repack failed with error: ERROR:  permission denied for schema repack
LINE 1: select repack.version(), repack.version_sql()
```

To avoid that error, run pg_repack from the context of `azure_pg_admin`.

### pg_stat_statements

The [pg_stat_statements extension](https://www.postgresql.org/docs/current/pgstatstatements.html) gives you a view of all the queries that run on your database. This is useful for understanding your query workload performance on a production system.

The [pg_stat_statements extension](https://www.postgresql.org/docs/current/pgstatstatements.html) is preloaded in `shared_preload_libraries` on every Azure Database for PostgreSQL flexible server instance to provide a means of tracking SQL statement execution statistics.

For security reasons, you must [allowlist](how-to-allow-extensions.md#allow-extensions) the [pg_stat_statements extension](https://www.postgresql.org/docs/current/pgstatstatements.html) and install it using [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) command.

The setting `pg_stat_statements.track`, which controls what statements are tracked by the extension, defaults to `top`, meaning all statements issued directly by clients are tracked. The two other tracking levels are `none` and `all`. This setting is configurable as a server parameter.

There's a tradeoff between the query execution information the `pg_stat_statements` extension provides on the server performance as it logs each SQL statement. If you aren't actively using the `pg_stat_statements` extension, we recommend that you set `pg_stat_statements.track` to `none`. Some third-party monitoring services might rely on `pg_stat_statements` to deliver query performance insights, so confirm whether this is the case for you.

### postgres_fdw

The [`postgres_fdw`](https://www.postgresql.org/docs/current/postgres-fdw.html) extension allows you to connect from one Azure Database for PostgreSQL flexible server instance to another or another database in the same server. Azure Database for PostgreSQL flexible server supports both incoming and outgoing connections to any PostgreSQL server. The sending server needs to allow outbound connections to the receiving server. Similarly, the receiving server needs to allow connections from the sending server.

If you plan to use this extension, we recommend deploying your servers with [virtual network integration](../flexible-server/concepts-networking-private.md). By default, virtual network integration allows connections between servers in the virtual network. You can also choose to use [virtual network network security groups](/azure/virtual-network/manage-network-security-group) to customize access.

### pgstattuple

When using the `pgstattuple` extension to try to obtain tuple statistics from objects kept in the `pg_toast` schema in versions of Postgres 11 through 13, you receive a "permission denied for schema pg_toast" error.

#### Permission denied for schema pg_toast

Customers using PostgreSQL versions 11 through 13 on Azure Database for Flexible Server can't use the `pgstattuple` extension on objects within the `pg_toast` schema.

In PostgreSQL 16 and 17, the `pg_read_all_data` role is automatically granted to `azure_pg_admin`, allowing `pgstattuple` to function correctly. In PostgreSQL 14 and 15, customers can manually grant the `pg_read_all_data` role to `azure_pg_admin` to achieve the same result. However, in PostgreSQL 11 through 13, the `pg_read_all_data` role doesn't exist.

Customers can't directly grant the necessary permissions. If you need to be able to run `pgstattuple` to access objects under the `pg_toast` schema, proceed to [create an Azure support request](/azure/azure-portal/supportability/how-to-create-azure-support-request).

### timescaleDB

The `timescaleDB` extension is a time-series database packaged as an extension for PostgreSQL. It provides time-oriented analytical functions and optimizations and scales Postgres for time-series workloads.
[Learn more about TimescaleDB](https://docs.timescale.com/timescaledb/latest/), a registered trademark of Timescale, Inc. Azure Database for PostgreSQL flexible server provides the TimescaleDB [Apache-2 edition](https://www.timescale.com/legal/licenses).

#### Install TimescaleDB

To use `timescaleDB`, make sure that you [allowlist](how-to-allow-extensions.md#allow-extensions) the extension, [load its library](how-to-allow-extensions.md#load-libraries), and [install the extension](how-to-allow-extensions.md#create-extensions) in the database on which you plan to use its functionality.

You can now create a TimescaleDB hypertable [from scratch](https://docs.timescale.com/getting-started/creating-hypertables) or migrate [existing time-series data in PostgreSQL](https://docs.timescale.com/getting-started/migrating-data).

#### Restore a Timescale database using pg_dump and pg_restore

To restore a Timescale database using `pg_dump` and `pg_restore`, you must run two helper procedures in the destination database: `timescaledb_pre_restore()` and `timescaledb_post restore()`.

First, prepare the destination database:

```sql
--create the new database where you want to perform the restore
CREATE DATABASE tutorial;
\c tutorial --connect to the database
CREATE EXTENSION timescaledb;

SELECT timescaledb_pre_restore();
```

Now, you can run `pg_dump` on the original database and then do `pg_restore`. After the restore, be sure to run the following command in the restored database:

```sql
SELECT timescaledb_post_restore();
```

For more information on the restore method with Timescale enabled database, see [Timescale documentation](https://docs.timescale.com/timescaledb/latest/how-to-guides/backup-and-restore/pg-dump-and-restore/#restore-your-entire-database-from-backup).

#### Restore a Timescale database using timescaledb-backup

While running the `SELECT timescaledb_post_restore()` procedure, you might get permissions denied when updating timescaledb.restoring flag. This is due to limited ALTER DATABASE permission in Cloud PaaS database services. In this case, you can perform an alternative method using the `timescaledb-backup` tool to back up and restore the Timescale database. Timescaledb-backup is a program that makes dumping and restoring a TimescaleDB database simpler, less error-prone, and more performant.

To do so, follow these steps:

1. Install tools as detailed [here](https://github.com/timescale/timescaledb-backup#installing-timescaledb-backup).

1. Create a target Azure Database for PostgreSQL flexible server instance and database.

1. Enable Timescale extension.

1. Grant the `azure_pg_admin` role to the user that is used by [ts-restore](https://github.com/timescale/timescaledb-backup#using-ts-restore).

1. Run [ts-restore](https://github.com/timescale/timescaledb-backup#using-ts-restore) to restore database.

More details on these utilities can be found [here](https://github.com/timescale/timescaledb-backup).

## Extensions and major version upgrade

Azure Database for PostgreSQL flexible server offers an [in-place major version upgrade feature](../flexible-server/concepts-major-version-upgrade.md), that performs an in-place upgrade of the Azure Database for PostgreSQL flexible server instance with just a simple interaction from the user. In-place major version upgrade simplifies the Azure Database for PostgreSQL flexible server upgrade process, minimizing the disruption to users and applications accessing the server. In-place major version upgrades don't support specific extensions, and there are some limitations to upgrading certain extensions.

The extensions `anon`, `Apache AGE`, `dblink`, `orafce`, `pgaudit`, `postgres_fdw`, and `timescaledb` are unsupported for all Azure Database for PostgreSQL flexible server versions when using in-place major version update feature.

[Share your suggestions and bugs with the Azure Database for PostgreSQL product team](https://aka.ms/pgfeedback).

## Related content

- [How to use extensions](how-to-allow-extensions.md).
- [Special considerations with extensions](concepts-extensions-considerations.md).
- [List of extensions by name](concepts-extensions-versions.md).
