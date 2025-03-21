---
title: Fabric Mirroring
description: Learn about Fabric Mirroring in Azure Database for PostgreSQL flexible server.
author: scoriani
ms.author: scoriani
ms.reviewer: 
ms.date: 03/31/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: conceptual
#customer intent: As a user, I want to learn about how can use Fabric Mirroring for my databases in an Azure Database for PostgreSQL flexible server.
---

# Mirroring Azure Database for PostgreSQL flexible server in Microsoft Fabric

[!INCLUDE [applies-to-postgresql-flexible-server](~/reusable-content/ce-skilling/azure/includes/postgresql/includes/applies-to-postgresql-flexible-server.md)]


[Mirroring in Fabric](/fabric/database/mirrored-database/azure-database-postgresql) provides an easy experience to avoid complex ETL (Extract Transform Load) and integrate your existing Azure Database for PostgreSQL flexible server estate with the rest of your data in Microsoft Fabric. You can continuously replicate your existing Azure Database for PostgreSQL flexible server directly into Fabric's OneLake. Inside Fabric, you can unlock powerful business intelligence, artificial intelligence, Data Engineering, Data Science, and data sharing scenarios.


## Architecture

Fabric mirroring in Azure Database for PostgreSQL flexible server is built on concepts like [logical replication](concepts-logical.md) and Change Data Capture (CDC) design pattern.

Once Fabric mirroring is established for a database in Azure Database for PostgreSQL flexible server, an initial snapshot is created by a PostgreSQL background process for selected tables to be mirrored, and it's shipped to a Fabric OneLake's landing zone in Parquet format. A Replicator process running in Fabric is then taking these initial snapshot files and creating Delta tables in the Mirrored database artifact.

Subsequent changes applied to selected tables are also captured in the source database and shipped to OneLake's landing zone in batches to be applied to the respective Delta tables in the Mirrored database artifact.

 :::image type="content" source="media/concepts-fabric-mirroring/architecture.png" alt-text="Diagram of end to end architecture for Fabric mirroring in Azure Database for PostgreSQL flexible server.":::

## What is CDC?

- CDC stands for Change Data Capture, a method that enables applications to detect and capture changes made to a database.
- It does not rely on explicit SQL queries to track changes.
- Instead, it involves a continuous stream of change events published by the database server.
- Clients can subscribe to this stream to monitor changes, focusing on specific databases, individual tables, or even subsets of columns within a table.

For Fabric mirroring, the CDC pattern is implemented in a proprietary PostgreSQL extension called azure_cdc, which is installed and registered in source databases by the Azure Database for PostgreSQL flexible server control plane during Fabric mirroring enablement workflow.

## Azure CDC Extension

- Azure CDC is an extension for PostgreSQL that enhances the capabilities of logical decoding.
- It interprets and transforms Write-Ahead Log (WAL) data into an understandable logical format.
- The extension converts database modifications into a sequence of logical operations like INSERT, UPDATE, and DELETE.
- Azure CDC acts as a layer on top of PostgreSQL's built-in logical decoding plugin, “pgoutput”.
- Azure CDC exports table snapshots and modifications as Parquet files, and copy them to a Fabric OneLake landing zone for subsequent processing.

## Fabric mirroring enablement in Azure Database for PostgreSQL flexible server portal 

There are several pre-requisites that need to be configured before using Fabric mirroring in Azure Database for PostgreSQL flexible server. These pre-requisites are:

- **System-assigned Managed Identity (SAMI)** must be enabled.
    - This is the identity used by the Azure CDC to authenticate communications with Fabric OneLake and copy initial snapshots and change batches to landing zone.
- **wal_level** server parameter must be set to "logical".
    - Enables logical replication for the source server.
- Azure CDC extension (azure_cdc) to be pre-loaded on source server and registered for selected databases to mirror (requires restart).
- **max_worker_processes** server parameter must be increased to accommodate additional background processes for mirroring.

To automate pre-requisites configuration on source server, a new page is available in the Azure Portal 

:::image type="content" source="media/concepts-fabric-mirroring/start-enablement.png" alt-text="New Fabric mirroring page in Azure Portal for automate pre-requisites configuration.":::

Click on **Get Started** for initiating the enablement workflow and you're presented with the following blade.

:::image type="content" source="media/concepts-fabric-mirroring/select-databases.png" alt-text="New Fabric mirroring page in Azure Portal for automate pre-requisites configuration.":::

In this blade you can find current status of required pre-requisites. If System Assigned Managed Identity (SAMI) is not enabled for this server, you can click the link and get redirected to that page for enabling this feature.

Once done, you can select the databases to enable for Fabric mirroring (up to 3 by default, but this can be increased by changing the **max_mirrored_databases** server parameter) and then click **Prepare**.

The workflow will present a Restart Server pop-up, and by clicking **Restart** you can start the process which automates all remaining configuration steps, and you can start creating your mirrored database from [Fabric user interface](/fabric/database/mirrored-database/azure-database-postgresql-tutorial) 

:::image type="content" source="media/concepts-fabric-mirroring/server-ready.png" alt-text="Fabric mirroring page showing server ready for mirroring.":::

### Server parameters

These are server parameters that have a direct impact in Fabric mirroring for Azure Database for PostgreSQL flexible server. 

- **azure.fabric_mirror_enabled**: Default is off. Specifies the flag indicating if mirroring is enabled on server. This parameter is set automatically at the end of the server enablement workflow. You should not change this manually.
- **max_replication_slots**: Default 10. We consume 1 replication slot per mirrored database, and customers may consider to increase if they are creating more mirrors or have other replication slots created for other purposes (logical replication). 
- **max_wal_senders**: Default is 10. As previous parameter, we use 1 wal sender process per mirror and should be increased when mirroring more databases.  
- **max_worker_processes**: Default is 8. After initial snapshot, we use 1 process per mirrored database or where mirroring is enabled (but no mirrored artifact is created in Fabric yet). If you have other extensions or workloads using additional worker processes, you need to increase this value.
- **max_parallel_workers**: Default is 8. This will limit how many workers can run at the same time. If you enable multiple mirroring sessions on the same server, you may consider increasing this parameter to allow more parallel operations (e.g. increase parallelism in initial snapshots). 
- **azure_cdc.max_fabric_mirrors** Default is 3. Customers can increase this value if they need to mirror more than 3 databases in this server. It is important to consider that every new mirrored database consumes server resources (5 background processes using CPU and Memory resources for snapshot creation and change batching) so, depending on how busy your server is, you should monitor resource utilization and scale up your compute size to the next size available if CPU and memory utilization is constantly above 80% or performance are not what you expect.
- **azure_cdc.max_snapshot_workers**: Default is 3. Maximum number of worker processes used during initial snapshot creation. You could increase this to speed up initial snapshot creation when increasing the number of mirrored database, but you should consider all the other background processes running in the system before doing that.
- **azure_cdc.change_batch_buffer_size**: Default is 16MB. Maximum buffer size (in MB) for change batch. Per table, up to this much data is buffered before written to local disk. Depending on data change frequency on your mirrored databases, you could tweak this value if you want to reduce change batches frequency or increase if you want to prioritize overall throughput.
- **azure_cdc.change_batch_export_timeout**: Default is 30. Maximum idle time (in seconds) between change batch messages. When exceeded, we mark the current batch as complete. Depending on data change frequency on your mirrored databases, you could tweak this value if you want to reduce change batches frequency or increase if you want to prioritize overall throughput.
- **azure_cdc.parquet_compression**: Default is ZSTD. This parameter is for internal use only, you shouldn't modify this.
- **azure_cdc.snapshot_buffer_size**: Default is 1000.
Maximum size (in MB) of the initial snapshot buffer. Per table, up to this much data is buffered before sent to Fabric. Keep in mind that azure_cdc.snapshot_buffer_size*azure_cdc.max_snapshot_workers is the total memory buffer used during initial snapshot.
- **azure_cdc.snapshot_export_timeout**: Default is 180. Maximum time (in minutes) to export initial snapshot. On exceed, we restart.

### Monitoring and troubleshooting

Customers can leverage several User Defined Functions and tables to monitor important CDC metrics in Azure Database for PostgreSQL flexible server and troubleshoot the Mirroring process to Fabric.

**Monitoring Functions**

- **azure_cdc.list_tracked_publications()**: for each publication in the source flexible server, returns a comma-separated string containing the following information
    - publicationName (text)
    - includeData (bool)
    - includeChanges (bool)
    - active (bool)
    - baseSnapshotDone (bool)
    - generationId (int)
    
- **azure_cdc.publication_status('pub_name')**: for each publication in the source flexible server returns a comma-separated string with the following information 
    - <status, start_lsn, stop_lsn, flush_lsn>. 
    - Status consist of ["Slot name", "Origin name", "CDC data destination path", "Active", "Snapshot Done", "Progress percentage", "Generation ID", "Completed Batch ID", "Uploaded Batch ID", "CDC start time"]

- **azure_cdc.is_table_mirrorable('schema_name','table_name')**: Given schema and table name, it returns if table is mirrorable. For a table to be mirrorable, it needs to satisfy following:
     - column names does not contain one of the chars '[ ;{}\n\t=()]'
     - column types are one of ['bigint', 'bigserial', 'boolean', 'bytea',
    			'character', 'character varying', 'date', 'double precision',
    			'integer', 'numeric', 'real', 'serial', 'oid',
    			'money', 'smallint', 'smallserial', 'text',
    			'time without time zone', 'time with time zone',
    			'timestamp without time zone', 'timestamp with time zone', 'uuid']
     - table is not a view, materialized view, foreign table, toast table, or partitioned table
     - table has a primary key or a unique, non-null, and non-partial index


**Tracking tables**

- **azure_cdc.tracked_publications**: one row for each existing Mirrored database in Fabric. Query this table to understand the status of each publication.

| Column Name                     | Postgres Type           | Explanation                                                |
|--------------------------|-------------------------|------------------------------------------------------------|
| publication_id           | oid                     | Oid of the publication                      |
| destination_path         | text                    | Path to the landing zone in Fabric OneLake                       |
| destination_format       | azure_cdc.data_format   | Format of the data in Azure CDC                            |
| include_data             | bool                    | Whether to include initial snapshot data in the publication|
| include_changes          | bool                    | Whether to include changes in the publication              |
| active                   | bool                    | Whether the publication is active                          |
| snapshot_done            | bool                    | Whether the snapshot is completed                          |
| snapshot_progress        | smallint                | Progress of the snapshot                                   |
| snapshot_progress_percentage | text                | Percentage progress of the snapshot                        |
| generation_id            | int                     | Generation identifier                                      |
| stream_start_lsn         | pg_lsn                  | Log sequence number where the change stream started        |
| stream_start_time        | timestamp               | Timestamp when the change stream started                   |
| stream_stop_lsn          | pg_lsn                  | Log sequence number where the change stream stopped        |
| snapshot_size            | bigint                  | Total size of the snapshot (in bytes)                      |
| total_time               | int                     | Total time(in seconds) taken for the publication           |

- **azure_cdc.tracked_batches**: one row for each change batch captured and shipped to Fabric OneLake. Query this table to understand which batch has been already captured and uploaded to Fabric OneLake. With `last_written_lsn` column you can understand if a given transaction in your source database has been already shipped to Fabric.

| Name                     | Postgres Type           | Explanation                                                |
|--------------------------|-------------------------|------------------------------------------------------------|
|publication_id            |oid| Oid of the publication |
|completed_batch_id        |bigint|Sequence number(starting from 1) of the batch. Unique per publication|
|last_written_lsn          | pg_lsn |LSN of the last write of this batch |
|last_received_lsn         |pg_lsn | Last LSN received |
|server_lsn                |pg_lsn| current server LSN (at the time when capturing of this batch finalized) |
|is_batch_uploaded| bool| Whether the batch is uploaded |
|is_batch_acknowledged| bool| Whether we acknowledged wal_sender for this batch data(last_written_lsn) |
|batch_start_time | TIMESTAMPTZ|Timestamp of the batch start |
|batch_completion_time | TIMESTAMPTZ| Timestamp of the batch completion |
|batch_uploaded_time |TIMESTAMPTZ |Timestamp of the batch upload |
|batch_acknowledged_time |TIMESTAMPTZ |Timestamp of the batch when LSN is ack'ed to the publisher |
|batch_size | int |Size of the batch (in bytes) |


## Related content

- [Configure system or user assigned managed identities in Azure Database for PostgreSQL flexible server](how-to-configure-managed-identities.md).
- [Firewall rules in Azure Database for PostgreSQL flexible server](concepts-firewall-rules.md).
- [Public access and private endpoints in Azure Database for PostgreSQL flexible server](concepts-networking-public.md).
