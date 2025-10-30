---
title: Mirroring in Microsoft Fabric
description: Learn about Mirroring in Microsoft Fabric for Azure Database for PostgreSQL flexible server instances.
author: scoriani
ms.author: scoriani
ms.reviewer: maghan
ms.date: 03/31/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: concept-article
# customer intent: As a user, I want to learn about how can use Fabric Mirroring for my databases in an Azure Database for PostgreSQL.
---

# Azure Database for PostgreSQL Mirroring in Microsoft Fabric

[Mirroring in Fabric](/fabric/database/mirrored-database/azure-database-postgresql) provides an easy experience to avoid complex ETL (Extract Transform Load) and integrate your existing Azure Database for PostgreSQL flexible server estate with the rest of your data in Microsoft Fabric. You can continuously replicate your existing Azure Database for PostgreSQL directly into Fabric OneLake. Inside Fabric, you can unlock powerful business intelligence, artificial intelligence, Data Engineering, Data Science, and data sharing scenarios.

## Architecture

Fabric mirroring in Azure Database for PostgreSQL is built on concepts like [logical replication](concepts-logical.md) and Change Data Capture (CDC) design pattern.

Once Fabric mirroring is established for a database in an Azure Database for a PostgreSQL flexible server instance, a PostgreSQL background process creates an initial snapshot for selected tables to be mirrored, which is shipped to a Fabric OneLake landing zone in Parquet format. A Replicator process running in Fabric takes these initial snapshot files and creates Delta tables in the Mirrored database artifact.

Subsequent changes applied to selected tables are also captured in the source database and shipped to the OneLake landing zone in batches to be applied to the respective Delta tables in the Mirrored database artifact.

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

Azure CDC exports table snapshots and modifications as Parquet files and copies them to a Fabric OneLake landing zone for subsequent processing.

## Enable Fabric mirroring in the Azure portal

Fabric mirroring in the Azure portal for an Azure Database for PostgreSQL flexible server instance allows you to replicate your PostgreSQL databases into Microsoft Fabric. This feature helps you integrate your data seamlessly with other services in Microsoft Fabric, enabling advanced analytics, business intelligence, and data science scenarios. By following a few simple steps in the Azure portal, you can configure the necessary prerequisites and start mirroring your databases to use the full potential of Microsoft Fabric.

### Prerequisites

Several prerequisites must be configured before using Fabric mirroring in Azure Database for the PostgreSQL flexible server instance.

- **System-assigned Managed Identity (SAMI)** must be enabled.\
    - This is the identity used by the Azure CDC to authenticate communications with Fabric OneLake, copy initial snapshots, and change batches to the landing zone.

- **wal_level** server parameter must be set to "logical".
    - Enables logical replication for the source server.

    The Azure CDC extension (azure_cdc) is preloaded on the source server and registered for selected databases to mirror (it requires restart).

- **max_worker_processes** server parameter must be increased to accommodate more background processes for mirroring.

A new page is available in the Azure portal to automate prerequisite configuration on the source server.

:::image type="content" source="media/concepts-fabric-mirroring/start-enablement.png" alt-text="Screenshot showing New Fabric mirroring page in Azure portal to start enablement." lightbox="media/concepts-fabric-mirroring/start-enablement.png":::

Select **Get Started** to initiate the enablement workflow.

:::image type="content" source="media/concepts-fabric-mirroring/select-databases.png" alt-text="Screenshot showing New Fabric mirroring page in Azure portal for select databases." lightbox="media/concepts-fabric-mirroring/select-databases.png":::

This page shows the current status of the required prerequisites. If System Assigned Managed Identity (SAMI) isn't enabled for this server, select the link to be redirected to the page where you can enable this feature.

Once done, you can select the databases to enable Fabric mirroring (up to 3 by default, but this can be increased by changing the **max_mirrored_databases** server parameter) and then select **Prepare**.

The workflow presents a Restart Server pop-up, and by selecting **Restart**, you can start the process, which automates all remaining configuration steps, and you can start creating your mirrored database from [Fabric user interface](/fabric/database/mirrored-database/azure-database-postgresql-tutorial)

:::image type="content" source="media/concepts-fabric-mirroring/server-ready.png" alt-text="Fabric mirroring page showing server ready for mirroring." lightbox="media/concepts-fabric-mirroring/server-ready.png":::

### Server parameters

These server parameters directly affect Fabric mirroring for Azure Database for PostgreSQL.

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

### Monitor

Monitoring Fabric mirroring in Azure Database for PostgreSQL flexible server instances is essential to ensure that the mirroring process is running smoothly and efficiently. By monitoring the status of the mirrored databases, you can identify any potential issues and take corrective actions as needed.

You can use several User Defined Functions and tables to monitor important CDC metrics in the Azure Database for the PostgreSQL flexible server instances and troubleshoot the Mirroring process to Fabric.

### Monitoring functions

The mirroring function for Fabric mirroring in Azure Database for PostgreSQL allows you to replicate your PostgreSQL databases into Microsoft Fabric seamlessly, enabling advanced analytics and data integration scenarios.

- **azure_cdc.list_tracked_publications()**: for each publication in the source flexible server instance, returns a comma-separated string containing the following information
    - publicationName (text)
    - includeData (bool)
    - includeChanges (bool)
    - active (bool)
    - baseSnapshotDone (bool)
    - generationId (int)

- **azure_cdc.publication_status('pub_name')**: for each publication in the source, the flexible server instance returns a comma-separated string with the following information
    - <status, start_lsn, stop_lsn, flush_lsn>.
    - Status consists of ["Slot name," "Origin name," "CDC data destination path," "Active," "Snapshot Done," "Progress percentage," "Generation ID," "Completed Batch ID," "Uploaded Batch ID," "CDC start time"]

- **azure_cdc.is_table_mirrorable('schema_name','table_name')**: Given schema and table name, it returns if the table is mirrorable. For a table to be mirrorable, it needs to satisfy the following:
    - The column names don't contain any of the following characters: `[ ;{}\n\t=()]`
    - The column types are one of the following:
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
    - The table has a primary key or a unique, non-null, and nonpartial index

### Tracking tables

- **azure_cdc.tracked_publications**: one row for each existing Mirrored database in Fabric. Query this table to understand the status of each publication.

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

- **azure_cdc.tracked_batches**: one row for each change batch captured and shipped to Fabric OneLake. Query this table to understand which batch has already been captured and uploaded to Fabric OneLake. With the `last_written_lsn` column, you can understand if a given transaction in your source database has already been shipped to Fabric.

| Name | Postgres Type | Explanation |
| --- | --- | --- |
| publication_id | oid | Oid of the publication |
| completed_batch_id | bigint | Sequence number(starting from 1) of the batch. Unique per publication |
| last_written_lsn | pg_lsn | LSN of the last write of this batch |
| last_received_lsn | pg_lsn | Last LSN received |
| server_lsn | pg_lsn | current server LSN (at the time when capturing of this batch finalized) |
| is_batch_uploaded | bool | Whether the batch is uploaded |
| is_batch_acknowledged | bool | Whether we acknowledged wal_sender for this batch data(last_written_lsn) |
| batch_start_time | TIMESTAMPTZ | Timestamp of the batch start |
| batch_completion_time | TIMESTAMPTZ | Timestamp of the batch completion |
| batch_uploaded_time | TIMESTAMPTZ | Timestamp of the batch upload |
| batch_acknowledged_time | TIMESTAMPTZ | Timestamp of the batch when LSN is ack`ed to the publisher |
| batch_size | int | Size of the batch (in bytes) |

## Related content

- [System assigned managed identity](how-to-configure-managed-identities.md)
- [Firewall rules in Azure Database for PostgreSQL](concepts-firewall-rules.md)
- [Networking overview for Azure Database for PostgreSQL instances with public access](concepts-networking-public.md)
