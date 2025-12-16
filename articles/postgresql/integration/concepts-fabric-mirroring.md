---
title: Mirroring in Microsoft Fabric
description: Learn about Mirroring in Microsoft Fabric for Azure Database for PostgreSQL flexible server instances.
author: scoriani
ms.author: scoriani
ms.reviewer: maghan
ms.date: 11/18/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
# customer intent: As a user, I want to learn about how can use Fabric Mirroring for my databases in an Azure Database for PostgreSQL.
---

# Azure Database for PostgreSQL mirroring in Microsoft Fabric

[Mirroring in Fabric](/fabric/database/mirrored-database/azure-database-postgresql) (now generally available) provides an easy experience to avoid complex ETL (Extract Transform Load) and integrate your existing Azure Database for PostgreSQL estate with the rest of your data in Microsoft Fabric. You can continuously replicate your existing Azure Database for PostgreSQL directly into Fabric OneLake. Inside Fabric, you can unlock powerful business intelligence, artificial intelligence, Data Engineering, Data Science, and data sharing scenarios.

> [!IMPORTANT]  
> Newly created servers after Ignite 2025 automatically include the latest general availability version of mirroring components. Existing servers upgrade progressively as part of the next maintenance cycles without requiring manual intervention. You don't need to disable and re-enable mirroring to receive updates.

## Architecture

Fabric mirroring in Azure Database for PostgreSQL is built on concepts like [logical replication](../configure-maintain/concepts-logical.md) and Change Data Capture (CDC) design pattern.

Once you establish Fabric mirroring for a database in an Azure Database for PostgreSQL flexible server instance, a PostgreSQL background process creates an initial snapshot for selected tables to be mirrored. It ships the snapshot to a Fabric OneLake landing zone in Parquet format. A Replicator process running in Fabric takes these initial snapshot files and creates Delta tables in the Mirrored database artifact.

The source database captures subsequent changes applied to selected tables. It ships these changes to the OneLake landing zone in batches to be applied to the respective Delta tables in the Mirrored database artifact.

:::image type="content" source="media/concepts-fabric-mirroring/architecture.png" alt-text="Diagram of end-to-end architecture for Fabric mirroring in an Azure Database for PostgreSQL flexible server instance." lightbox="media/concepts-fabric-mirroring/architecture.png":::

## What is Change Data Capture (CDC)?

Change Data Capture (CDC) is a method that enables applications to detect and capture changes made to a database.

It doesn't rely on explicit SQL queries to track changes.

Instead, it involves a continuous stream of change events published by the database server.

Clients can subscribe to this stream to monitor changes, focusing on specific databases, individual tables, or even subsets of columns within a table.

For Fabric mirroring, the CDC pattern is implemented in a proprietary PostgreSQL extension called azure_cdc. The control plane for an Azure Database for PostgreSQL flexible server instance is installed and registered in source databases during the Fabric mirroring enablement workflow.

## Azure Change Data Capture (CDC) extension

Azure CDC is an extension for PostgreSQL that enhances the capabilities of logical decoding.

It interprets and transforms Write-Ahead Log (WAL) data into an understandable logical format.

The extension converts database modifications into a sequence of logical operations like INSERT, UPDATE, and DELETE.

Azure CDC is a layer on top of PostgreSQL's built-in logical decoding plugin, `pgoutput`.

Azure CDC exports table snapshots and modifications as Parquet files and copies them to a Microsoft Fabric OneLake landing zone for subsequent processing.

## Enable Fabric mirroring in the Azure portal

Fabric mirroring in the Azure portal for an Azure Database for PostgreSQL flexible server instance allows you to replicate your PostgreSQL databases into Microsoft Fabric. This feature helps you integrate your data seamlessly with other services in Microsoft Fabric, enabling advanced analytics, business intelligence, and data science scenarios. By following a few simple steps in the Azure portal, you can configure the necessary prerequisites and start mirroring your databases to use the full potential of Microsoft Fabric.

## Supported versions

Azure Database for PostgreSQL supports **PostgreSQL 14 and later** for Fabric mirroring.

## Prerequisites

Before you can use Fabric mirroring in an Azure Database for PostgreSQL flexible server instance, you need to configure several prerequisites.

- **System-assigned Managed Identity (SAMI)** must be [enabled](../security/security-configure-managed-identities-system-assigned.md).
  - Azure CDC uses this identity to authenticate communications with Fabric OneLake, copy initial snapshots, and change batches to the landing zone.

You configure additional prerequisites through a dedicated enablement workflow described in the following section. These prerequisites are:

- **wal_level** server parameter must be set to "logical".
  - Enables logical replication for the source server.

- **max_worker_processes** server parameter must be increased to accommodate more background processes for mirroring.

- **azure_cdc** extension. The Azure CDC extension (azure_cdc) is preloaded on the source server and registered for selected databases to mirror (it requires restart).

A new page is available in the Azure portal to automate these prerequisite configurations on the source server.

:::image type="content" source="media/concepts-fabric-mirroring/start-enablement.png" alt-text="Screenshot showing New Fabric mirroring page in Azure portal to start enablement." lightbox="media/concepts-fabric-mirroring/start-enablement.png":::

Select **Get Started** to initiate the enablement workflow.

:::image type="content" source="media/concepts-fabric-mirroring/select-databases.png" alt-text="Screenshot showing New Fabric mirroring page in Azure portal for select databases." lightbox="media/concepts-fabric-mirroring/select-databases.png":::

This page shows the current status of the required prerequisites. If System Assigned Managed Identity (SAMI) isn't enabled for this server, select the link to be redirected to the page where you can enable this feature.

When you're done, select the databases to enable Fabric mirroring (up to three by default, but you can increase this limit by changing the **max_mirrored_databases** server parameter) and then select **Prepare**.

The workflow presents a Restart Server pop-up. By selecting **Restart**, you start the process. The workflow automates all remaining configuration steps. You can start creating your mirrored database from the [Fabric user interface](/fabric/database/mirrored-database/azure-database-postgresql-tutorial).

:::image type="content" source="media/concepts-fabric-mirroring/server-ready.png" alt-text="Fabric mirroring page showing server ready for mirroring." lightbox="media/concepts-fabric-mirroring/server-ready.png":::

## Create a database role for Fabric Mirroring

Next, you need to provide or create a PostgreSQL role for the Fabric service to connect to your Azure Database for PostgreSQL flexible server.

You can accomplish this task by specifying a [database role](#use-a-database-role) for connecting to your source system.

> [!NOTE]  
> Both Entra ID and local database roles are supported to connect Fabric mirroring to Azure Database for PostgreSQL, select the [authentication method](../security/security-overview.md#access-control) that best fits your purposes.

#### Use a database role

1. Connect to your Azure Database for PostgreSQL using [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql) or [pgAdmin](https://www.pgadmin.org/). Connect with a principal that is a member of the role `azure_pg_admin`.
1. Create a PostgreSQL role named `fabric_user`. You can choose any name for this role. Provide your own strong password. Grant the permissions needed for Fabric mirroring in the database. Run the following SQL script to grant the `CREATEDB`, `CREATEROLE`, `LOGIN`, `REPLICATION`, and `azure_cdc_admin` permissions to the new role named `fabric_user`.

   ```sql
   -- create a new user to connect from Fabric
   CREATE ROLE fabric_user CREATEDB CREATEROLE LOGIN REPLICATION PASSWORD '<strong password>';

   -- grant role for replication management to the new user
   GRANT azure_cdc_admin TO fabric_user;
   -- grant create permission on the database to mirror to the new user
   GRANT CREATE ON DATABASE <database_to_mirror> TO fabric_user;
   ```

1. The database user you create also needs to be `owner` of the tables to replicate in the mirrored database. This requirement means that the user creates the tables or changes the ownership of those tables by using `ALTER TABLE <table name here> OWNER TO fabric_user;`.
   - When switching ownership to new user, you might need to grant to that user all privileges on `public` schema before. For more information regarding user account management, see Azure Database for PostgreSQL [user management](../security/security-manage-database-users.md) documentation, PostgreSQL product documentation for [Database Roles and Privileges](https://www.postgresql.org/docs/current/static/user-manag.html), [GRANT Syntax](https://www.postgresql.org/docs/current/static/sql-grant.html), and [Privileges](https://www.postgresql.org/docs/current/static/ddl-priv.html).

> [!IMPORTANT]  
> Missing one of the previous security configuration steps cause subsequent mirrored operations in Fabric portal to fail with an `Internal error` message.

## Server parameters

These server parameters directly affect Fabric mirroring for Azure Database for PostgreSQL and can be used to tune replication process to Fabric OneLake:

- **Azure.fabric_mirror_enabled**: The default is off. This parameter specifies the flag indicating whether mirroring is enabled on the server. It's set automatically at the end of the server enablement workflow, so you shouldn't change it manually.

- **max_replication_slots**: Default 10. We consume one replication slot per mirrored database, but customers might consider increasing this if they create more mirrors or have other replication slots created for other purposes (logical replication).

- **max_wal_senders**: The default is 10. As with the previous parameter, we use one `wal` sender process per mirror, which should be increased when mirroring more databases.

- **max_worker_processes**: The default is 8. After the initial snapshot, we use one process per mirrored database or where mirroring is enabled (but no mirrored artifact has been created in Fabric yet). You must increase this value if you have other extensions or workloads using more worker processes.

- **max_parallel_workers**: The default is 8, which limits the number of workers that can run simultaneously. If you enable multiple mirroring sessions on the same server, you might consider increasing this parameter to allow more parallel operations (for example, increasing parallelism in initial snapshots).

- **azure_cdc.max_fabric_mirrors** Default is 3. Customers can increase this value if they need to mirror more than three databases on this server. It's important to consider that every new mirrored database consumes server resources (five background processes using CPU and Memory resources for snapshot creation and change batching), so depending on how busy your server is, you should monitor resource utilization and scale up your compute size to the next size available if CPU and memory utilization are constantly above 80% or performance aren't what you expect.

- **azure_cdc.max_snapshot_workers**: Default is 3. Maximum number of worker processes used during initial snapshot creation. Increase this to speed up initial snapshot creation when increasing the number of mirrored databases. However, you should consider all the other background processes running in the system before doing that.

- **azure_cdc.change_batch_buffer_size**: Default is 16 MB. Maximum buffer size (in MB) for change batch. The table shows much data is buffered up to this before being written to the local disk. Depending on the data change frequency on your mirrored databases, you could tweak this value to reduce the change batch frequency or increase it if you want to prioritize overall throughput.

- **azure_cdc.change_batch_export_timeout**: Default is 30. Maximum idle time (in seconds) between change batch messages. When exceeded, we mark the current batch as complete. Depending on the data change frequency on your mirrored databases, you could tweak this value to reduce the change batch frequency or increase it if you want to prioritize overall throughput.

- **azure_cdc.parquet_compression**: Default is ZSTD. This parameter is for internal use only, so you shouldn't modify it.

- **azure_cdc.snapshot_buffer_size**: Defaults to 1000.
  The maximum size (in MB) of the initial snapshot buffer. Per the table, much data is buffered up to this before being sent to Fabric. Remember that azure_cdc.snapshot_buffer_size*azure_cdc.max_snapshot_workers is the total memory buffer used during the initial snapshot.

- **azure_cdc.snapshot_export_timeout**: Defaults to 180. Maximum time (in minutes) to export initial snapshot. If the maximum time is exceeded, then it restarts.

- **azure_cdc.prune_local_batches**: Defaults to True. If set, remove batch data from local disk, once it's successfully uploaded and acknowledged to wal_sender.

## Monitor

Monitoring the Fabric mirroring in Azure Database for PostgreSQL flexible server instances is essential to ensure that the mirroring process runs smoothly and efficiently. By monitoring the status of the mirrored databases, you can identify any potential issues and take corrective actions.

You can use several user-defined functions and tables to monitor important CDC metrics in the Azure Database for PostgreSQL flexible server instances and troubleshoot the mirroring process to Fabric.

### Monitoring functions

The mirroring function for fabric mirroring in Azure Database for PostgreSQL replicates your PostgreSQL databases into Microsoft Fabric seamlessly, so you can use advanced analytics and data integration scenarios.

- **azure_cdc.list_tracked_publications()**: For each publication in the source flexible server instance, returns a comma-separated string containing the following information
  - publicationName (text)
  - includeData (bool)
  - includeChanges (bool)
  - active (bool)
  - baseSnapshotDone (bool)
  - generationId (int)

- **azure_cdc.publication_status('pub_name')**: For each publication in the source, the flexible server instance returns a comma-separated string with the following information
  - <status, start_lsn, stop_lsn, flush_lsn>.
  - Status consists of ["Slot name," "Origin name," "CDC data destination path," "Active," "Snapshot Done," "Progress percentage," "Generation ID," "Completed Batch ID," "Uploaded Batch ID," "CDC start time"]

- **azure_cdc.get_all_tables_mirror_status()**: Returns the mirroring status for all eligible tables in the database. Excludes system schemas (pg_catalog, information_schema, pg_toast) and extension-owned tables. 

| Column Name | Postgres Type | Explanation |
| --- | --- | --- |
| table_schema | text | schema name of the table |
| table_name | text |  name of the table |
| mirroring_status | text | Overall status - OK, WARNING, or ERROR |
| mirroring_data | jsonb | JSONB array containing detailed status entries with status, status_code, and optional details |

| Status Code | Level | Description |
|------------|-------|-------------|
| SCHEMA_DOES_NOT_EXIST | ERROR | The specified schema does not exist |
| TABLE_DOES_NOT_EXIST | ERROR | The specified table does not exist in the schema |
| FORBIDDEN_CHARS_IN_COLUMN_NAME | ERROR | Column names contain forbidden characters |
| FORBIDDEN_CHARS_IN_TABLE_NAME | ERROR | Table name contains forbidden characters |
| UNSUPPORTED_DATA_TYPE | WARNING | Table has columns with unsupported data types |
| UNSUPPORTED_TYPE_IN_REPLICA_IDENTITY | ERROR | Unsupported data type in replica identity columns (when no unique index exists) |
| NOT_REGULAR_TABLE | ERROR | Table is not a regular, permanent table |
| NOT_TABLE_OWNER | ERROR | Current user is not the owner of the table |
| HAS_PRIMARY_KEY | OK | Table has a primary key |
| HAS_UNIQUE_INDEX | OK | Table has a suitable unique index |
| NO_INDEX_FULL_IDENTITY | WARNING | No suitable unique index; full row identity will be used (may affect performance) |
 
  - For a table to be mirrorable, it needs to satisfy the following conditions:
      - The column names don't contain any of the following characters: `[ ;{}\n\t=()]`
      - The column types are one of the following types:
        - `bigint`
        - `bigserial`
        - `boolean`
        - `bytes`
        - `character`
        - `character varying`
        - `date`
        - `double precision`
        - `integer`
        - `numeric`
        - `real`
        - `serial`
        - `oid`
        - `money`
        - `smallint`
        - `smallserial`
        - `text`
        - `time without time zone`
        - `time with time zone`
        - `timestamp without time zone`
        - `timestamp with time zone`
        - `uuid`
      - The table isn't a view, materialized view, foreign table, toast table, or partitioned table
      - The table has a primary key or a unique, non-nullable, and nonpartial index. If these requisites aren't met, Mirroring will still work applying [replica identity FULL](https://www.postgresql.org/docs/current/logical-replication-publication.html#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY), but **this will have significant impact on overall replication performance and on WAL utilization**. We recommend having a primary key or unique index for tables of nontrivial size.
    
### Tracking tables

- **azure_cdc.tracked_publications**: one row for each existing mirrored database in Fabric. Query this table to understand the status of each publication.

| Column Name | Postgres Type | Explanation |
| --- | --- | --- |
| publication_id | oid | Oid of the publication |
| destination_path | text | Path to the landing zone in Fabric OneLake |
| destination_format | azure_cdc.data_format | Format of the data in Azure CDC |
| include_data | bool | Whether to include initial snapshot data in the publication |
| include_changes | bool | Whether to include changes in the publication |
| active | bool | Whether the publication is active |
| snapshot_done | bool | Whether the snapshot is completed |
| snapshot_progress | smallint | Progress of the snapshot |
| snapshot_progress_percentage | text | Percentage progress of the snapshot |
| generation_id | int | Generation identifier |
| stream_start_lsn | pg_lsn | Log sequence number where the change stream started |
| stream_start_time | timestamp | Timestamp when the change stream started |
| stream_stop_lsn | pg_lsn | Log sequence number where the change stream stopped |
| snapshot_size | bigint | Total size of the snapshot (in bytes) |
| total_time | int | Total time(in seconds) taken for the publication |

- **azure_cdc.tracked_batches**: one row for each change batch captured and shipped to Fabric OneLake. Query this table to understand which batch is already captured and uploaded to Fabric OneLake. With the `last_written_lsn` column, you can understand if a given transaction in your source database is already shipped to Fabric.

| Name | Postgres Type | Explanation |
| --- | --- | --- |
| publication_id | oid | Oid of the publication |
| completed_batch_id | bigint | Sequence number(starting from 1) of the batch. Unique per publication |
| last_written_lsn | pg_lsn | LSN of the last write of this batch |

- **azure_cdc.tracked_tables**: one row for each table tracked across all publications. Has the following fields for all published tables, in all publications. If a table is part of two publications, it would be listed twice.

| Name | Postgres Type | Explanation |
| --- | --- | --- |
| publication_id | oid | Oid of the publication |
| table_oid | oid | Oid of the table |
| sequence_number | bigint | sequence number of the generated file |

## Related content

- [System assigned managed identity](../security/security-configure-managed-identities-system-assigned.md)
- [Firewall rules in Azure Database for PostgreSQL](../security/security-firewall-rules.md)
- [Networking overview for Azure Database for PostgreSQL instances with public access](../network/../network/concepts-networking-public.md)
