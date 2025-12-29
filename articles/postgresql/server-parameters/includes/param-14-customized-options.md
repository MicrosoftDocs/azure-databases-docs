---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 12/29/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### age.enable_containment

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Use @> operator to transform MATCH's filter. Otherwise, use -> operator. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [age.enable_containment](https://age.apache.org/age-manual/master/index.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.algorithm

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The hash method used for pseudonymizing functions. |
| Data type | string |
| Default value | `sha256` |
| Allowed values | `sha256` |
| Parameter type | read-only |
| Documentation | [anon.algorithm](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.k_anonymity_provider

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The security label provider used for k-anonymity. |
| Data type | string |
| Default value | `k_anonymity` |
| Allowed values | `k_anonymity` |
| Parameter type | read-only |
| Documentation | [anon.k_anonymity_provider](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.masking_policies

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Define multiple masking policies (NOT IMPLEMENTED YET). |
| Data type | string |
| Default value | `anon` |
| Allowed values | `anon` |
| Parameter type | read-only |
| Documentation | [anon.masking_policies](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.maskschema

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The schema where the dynamic masking views are stored. |
| Data type | string |
| Default value | `mask` |
| Allowed values | `mask` |
| Parameter type | read-only |
| Documentation | [anon.maskschema](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.privacy_by_default

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Mask all columns with NULL (or the default value for NOT NULL columns). |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [anon.privacy_by_default](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.restrict_to_trusted_schemas

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Masking filters must be in a trusted schema. Activate this option to prevent non-superuser from using their own masking filters. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [anon.restrict_to_trusted_schemas](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.salt

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The salt value used for the pseudonymizing functions. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [anon.salt](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.sourceschema

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The schema where the table are masked by the dynamic masking engine. |
| Data type | string |
| Default value | `public` |
| Allowed values | `public` |
| Parameter type | read-only |
| Documentation | [anon.sourceschema](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.strict_mode

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | A masking rule cannot change a column data type, unless you disable this. Disabling the mode is not recommended. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [anon.strict_mode](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### anon.transparent_dynamic_masking

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | New masking engine (EXPERIMENTAL). |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [anon.transparent_dynamic_masking](https://postgresql-anonymizer.readthedocs.io/en/stable/) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_analyze

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Use EXPLAIN ANALYZE for plan logging. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_analyze](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.2.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_buffers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log buffers usage. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_buffers](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.3.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_format

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | EXPLAIN format to be used for plan logging. |
| Data type | enumeration |
| Default value | `text` |
| Allowed values | `text,xml,json,yaml` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_format](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.9.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_level

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log level for the plan. |
| Data type | enumeration |
| Default value | `log` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,debug,info,notice,warning,log` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_level](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.10.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_min_duration

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the minimum execution time above which plans will be logged. Zero prints all plans. -1 turns this feature off. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_min_duration](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.1.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_nested_statements

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log nested statements. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_nested_statements](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.11.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_settings

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log modified configuration parameters affecting query planning. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_settings](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.8.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_timing

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Collect timing data, not just row counts. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_timing](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.5.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_triggers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Include trigger statistics in plans. This has no effect unless log_analyze is also set. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_triggers](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.6.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_verbose

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Use EXPLAIN VERBOSE for plan logging. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_verbose](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.7.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_wal

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log WAL usage. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_wal](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.4.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.sample_rate

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Fraction of queries to process. |
| Data type | numeric |
| Default value | `1.0` |
| Allowed values | `0.0-1.0` |
| Parameter type | dynamic |
| Documentation | [auto_explain.sample_rate](https://www.postgresql.org/docs/14/auto-explain.html#id-1.11.7.13.5.3.12.1.3) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.accepted_password_auth_method

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Accepted password authentication method. |
| Data type | set |
| Default value | `md5,scram-sha-256` |
| Allowed values | `md5,scram-sha-256` |
| Parameter type | dynamic |
| Documentation | [azure.accepted_password_auth_method](https://go.microsoft.com/fwlink/?linkid=2274147) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.change_batch_buffer_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Buffer size, in megabytes, for change batches. These buffers are used to temporarily store CDC changes before they are written to disk. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `1-100` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.change_batch_export_timeout

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum time, in seconds, to wait before a batch of changes is ready to be exported. |
| Data type | integer |
| Default value | `30` |
| Allowed values | `10-60` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.max_fabric_mirrors

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of parallel fabric mirrors that can be run at the same time. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-6` |
| Parameter type | static |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.max_snapshot_workers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of workers launched for snapshot export. Each worker exports one table at a time. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.onelake_buffer_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Buffer size, in megabytes, for upload to Onelake. Onelake uploads files in chunks, buffering the data in memory up to this limit. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `1-1024` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.parquet_compression

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Compression algorithm to use for parquet files. Determines the compression algorithm to use for parquet files. Supported values are 'uncompressed', 'snappy', 'gzip', and 'zstd'. |
| Data type | enumeration |
| Default value | `zstd` |
| Allowed values | `uncompressed,snappy,gzip,zstd` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.snapshot_buffer_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum size (in MB) of the initial snapshot buffer. Per table, up to this much data is buffered before sent to Fabric. Keep in mind that azure_cdc.snapshot_buffer_size*azure_cdc.max_snapshot_workers is the total memory buffer used during initial snapshot. |
| Data type | integer |
| Default value | `1000` |
| Allowed values | `10-4000` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_cdc.snapshot_export_timeout

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum time, in minutes, to wait before reporting an error when exporting a snapshot of a database. |
| Data type | integer |
| Default value | `180` |
| Allowed values | `0-1440` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.enable_temp_tablespaces_on_local_ssd

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Create temp tablespace on ephemeral disk. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.extensions

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies which extensions are allowed to be created in the server. |
| Data type | set |
| Default value | |
| Allowed values | `address_standardizer,address_standardizer_data_us,age,amcheck,anon,azure_ai,azure_storage,bloom,btree_gin,btree_gist,citext,credcheck,cube,dblink,dict_int,dict_xsyn,earthdistance,fuzzystrmatch,hll,hstore,hypopg,intagg,intarray,ip4r,isn,lo,login_hook,ltree,oracle_fdw,orafce,pageinspect,pg_buffercache,pg_cron,pg_diskann,pg_duckdb,pg_freespacemap,pg_hint_plan,pg_partman,pg_prewarm,pg_repack,pg_squeeze,pg_stat_statements,pg_trgm,pg_visibility,pgaudit,pgcrypto,pglogical,pgrouting,pgrowlocks,pgstattuple,plpgsql,plv8,postgis,postgis_raster,postgis_sfcgal,postgis_tiger_geocoder,postgis_topology,postgres_fdw,postgres_protobuf,semver,session_variable,sslinfo,tablefunc,tdigest,tds_fdw,timescaledb,topn,tsm_system_rows,tsm_system_time,unaccent,uuid-ossp,vector` |
| Parameter type | dynamic |
| Documentation | [azure.extensions](https://go.microsoft.com/fwlink/?linkid=2274269) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.fabric_mirror_enabled

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sepcifies the flag indicating if mirroring is enabled on server. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.service_principal_id

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | A unique identifier for a service principal in Azure, used to grant permissions and access to resources within a tenant. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.service_principal_tenant_id

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | A unique identifier for the tenant in which a service principal is created, ensuring the necessary permissions and access to resources within that tenant. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.single_to_flex_migration

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies if this is a server created for migrating from Azure Database for PostgreSQL Single Server to Flexible Server. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_storage.allow_network_access

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Allows accessing Azure Storage Blob service from azure_storage extension. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure_storage.allow_network_access](https://go.microsoft.com/fwlink/?linkid=2323791) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_storage.blob_block_size_mb

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Size of blob block, in megabytes, for PUT blob operations. |
| Data type | integer |
| Default value | Depends on resources (vCores, RAM, or disk space) allocated to the server. |
| Allowed values | `1024` |
| Parameter type | read-only |
| Documentation | [azure_storage.blob_block_size_mb](https://go.microsoft.com/fwlink/?linkid=2323791) |


[!INCLUDE [server-parameters-azure-notes-azure-storage-blob-block-size-mb](./server-parameters-azure-notes-azure-storage-blob-block-size-mb.md)]



### azure_storage.log_level

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log level used by the azure_storage extension. |
| Data type | enumeration |
| Default value | `log` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,debug,log,info,notice,warning,error` |
| Parameter type | dynamic |
| Documentation | [azure_storage.log_level](https://go.microsoft.com/fwlink/?linkid=2323791) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure_storage.public_account_access

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Allows all users to access data in storage accounts for which there are no credentials, and the storage account access is configured as public. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure_storage.public_account_access](https://go.microsoft.com/fwlink/?linkid=2323791) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.bucket_limit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Max login tokens per bucket. |
| Data type | integer |
| Default value | `2000` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.enable

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables temporary connection throttling per IP for too many login failures. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.factor_bias

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The factor bias for calculating number of tokens for an IP's bucket. |
| Data type | numeric |
| Default value | `0.8` |
| Allowed values | `0.0-0.9` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.hash_entries_max

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Max number of entries in the login failures hash table. |
| Data type | integer |
| Default value | `500` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.reset_time

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Time between resetting the login bucket. |
| Data type | integer |
| Default value | `120` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.restore_factor

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Factor to increase number of tokens by for IPs with low failure rate. |
| Data type | numeric |
| Default value | `2` |
| Allowed values | `1.0-100.0` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### connection_throttle.update_time

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Time between updating the login bucket. |
| Data type | integer |
| Default value | `20` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.auth_delay_ms

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Milliseconds to delay before reporting authentication failure. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483` |
| Parameter type | dynamic |
| Documentation | [credcheck.auth_delay_ms](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.auth_failure_cache_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum of entries in the auth failure cache. |
| Data type | integer |
| Default value | `1024` |
| Allowed values | `1-2097151` |
| Parameter type | dynamic |
| Documentation | [credcheck.auth_failure_cache_size](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.encrypted_password_allowed

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Allow encrypted password to be used or throw an error. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [credcheck.encrypted_password_allowed](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.history_max_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum of entries in the password history. |
| Data type | integer |
| Default value | `65535` |
| Allowed values | `1-2097151` |
| Parameter type | dynamic |
| Documentation | [credcheck.history_max_size](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.max_auth_failure

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of authentication failures before the user login account is invalidated. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-64` |
| Parameter type | dynamic |
| Documentation | [credcheck.max_auth_failure](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.no_password_logging

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Prevent exposing the password in error messages logged. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [credcheck.no_password_logging](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_contain

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Password should contain these characters |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_contain](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_contain_username

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Password contains username |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_contain_username](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_ignore_case

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Ignore case while password checking |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_ignore_case](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_min_digit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum password digits |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_min_digit](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_min_length

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum password length |
| Data type | integer |
| Default value | `1` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_min_length](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_min_lower

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum password lowercase letters |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_min_lower](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_min_repeat

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum password characters repeat |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_min_repeat](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_min_special

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum special characters |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_min_special](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_min_upper

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum password uppercase letters |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_min_upper](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_not_contain

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Password should not contain these characters |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_not_contain](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_reuse_history

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum number of password changes before permitting reuse |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-100` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_reuse_history](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_reuse_interval

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum number of days elapsed before permitting reuse |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-730` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_reuse_interval](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_valid_max

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Force use of VALID UNTIL clause in CREATE ROLE statement with a maximum number of days |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_valid_max](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.password_valid_until

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Force use of VALID UNTIL clause in CREATE ROLE statement with a minimum number of days |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.password_valid_until](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.reset_superuser

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Restore superuser access when they have been banned. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [credcheck.reset_superuser](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_contain

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Username should contain these characters |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_contain](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_contain_password

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Username contains password |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_contain_password](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_ignore_case

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Ignore case while username checking |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_ignore_case](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_min_digit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum username digits |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_min_digit](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_min_length

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum username length |
| Data type | integer |
| Default value | `1` |
| Allowed values | `1-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_min_length](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_min_lower

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum username lowercase letters |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_min_lower](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_min_repeat

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum username characters repeat |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_min_repeat](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_min_special

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum username special characters |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_min_special](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_min_upper

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum username uppercase letters |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_min_upper](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.username_not_contain

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Username should not contain these characters |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.username_not_contain](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.whitelist

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Comma separated list of usernames to exclude from password policy check. |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.whitelist](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.whitelist_auth_failure

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Comma separated list of usernames to exclude from max authentication failure check. |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.whitelist_auth_failure](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.database_name

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the database in which pg_cron metadata is kept. |
| Data type | string |
| Default value | `postgres` |
| Allowed values | `[A-Za-z0-9_]+` |
| Parameter type | static |
| Documentation | [cron.database_name](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.enable_superuser_jobs

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Allow jobs to be scheduled as superuser. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [cron.enable_superuser_jobs](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.host

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Hostname to connect to postgres. This setting has no effect when background workers are used. |
| Data type | string |
| Default value | `/tmp` |
| Allowed values | `/tmp` |
| Parameter type | read-only |
| Documentation | [cron.host](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.launch_active_jobs

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Launch jobs that are defined as active. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [cron.launch_active_jobs](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.log_min_messages

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | log_min_messages for the launcher bgworker. |
| Data type | enumeration |
| Default value | `warning` |
| Allowed values | `warning` |
| Parameter type | read-only |
| Documentation | [cron.log_min_messages](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.log_run

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log all jobs runs into the job_run_details table. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | static |
| Documentation | [cron.log_run](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.log_statement

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Log all cron statements prior to execution. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | static |
| Documentation | [cron.log_statement](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.max_running_jobs

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum number of jobs that can run concurrently. This value is limited by max_connections. |
| Data type | integer |
| Default value | `32` |
| Allowed values | `0-5000` |
| Parameter type | static |
| Documentation | [cron.max_running_jobs](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.timezone

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specify timezone used for cron schedule. |
| Data type | enumeration |
| Default value | `GMT` |
| Allowed values | `GMT` |
| Parameter type | read-only |
| Documentation | [cron.timezone](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.use_background_workers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Use background workers instead of client sessions. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [cron.use_background_workers](https://github.com/citusdata/pg_cron) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.allow_community_extensions

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Disable installing community extensions. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [duckdb.allow_community_extensions](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.allow_unsigned_extensions

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Allow DuckDB to load extensions with invalid or missing signatures. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [duckdb.allow_unsigned_extensions](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.autoinstall_known_extensions

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Whether known extensions are allowed to be automatically installed when a DuckDB query depends on them. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [duckdb.autoinstall_known_extensions](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.autoload_known_extensions

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Whether known extensions are allowed to be automatically loaded when a DuckDB query depends on them. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [duckdb.autoload_known_extensions](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.disabled_filesystems

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Disable specific file systems preventing access (e.g., LocalFileSystem). |
| Data type | string |
| Default value | `LocalFileSystem` |
| Allowed values | `LocalFileSystem` |
| Parameter type | read-only |
| Documentation | [duckdb.disabled_filesystems](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.enable_external_access

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Allow the DuckDB to access external state. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [duckdb.enable_external_access](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.force_execution

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Force queries to use DuckDB execution. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [duckdb.force_execution](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.max_memory

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The maximum memory DuckDB can use (e.g., 1GB). |
| Data type | integer |
| Default value | `1024` |
| Allowed values | `1024` |
| Parameter type | read-only |
| Documentation | [duckdb.max_memory](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.max_workers_per_postgres_scan

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of PostgreSQL workers used for a single Postgres scan. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `0-1024` |
| Parameter type | static |
| Documentation | [duckdb.max_workers_per_postgres_scan](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.memory_limit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The maximum memory DuckDB can use (e.g., 1GB), alias for duckdb.max_memory |
| Data type | integer |
| Default value | `1024` |
| Allowed values | `1024` |
| Parameter type | read-only |
| Documentation | [duckdb.memory_limit](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.postgres_role

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Which postgres role should be allowed to use DuckDB execution, use the secrets and create MotherDuck tables. Defaults to superusers only. |
| Data type | string |
| Default value | `azure_pg_duckdb_admin` |
| Allowed values | `azure_pg_duckdb_admin` |
| Parameter type | read-only |
| Documentation | [duckdb.postgres_role](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.threads

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of DuckDB threads per Postgres backend. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-96` |
| Parameter type | static |
| Documentation | [duckdb.threads](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### duckdb.worker_threads

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of DuckDB threads per Postgres backend, alias for duckdb.threads. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-96` |
| Parameter type | static |
| Documentation | [duckdb.worker_threads](https://github.com/duckdb/pg_duckdb) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaadauth.enable_group_sync

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables synchronization of Entra ID group members. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaadauth.enable_group_sync](https://go.microsoft.com/fwlink/?linkid=2338467) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies which classes of statements will be logged by session audit logging. |
| Data type | set |
| Default value | `none` |
| Allowed values | `none,read,write,function,role,ddl,misc,all` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_catalog

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies that session logging should be enabled in the case where all relations in a statement are in pg_catalog. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_catalog](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_client

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies whether audit messages should be visible to client. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_client](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_level

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies the log level that will be used for log entries. |
| Data type | enumeration |
| Default value | `log` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,info,notice,warning,log` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_level](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_parameter

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies that audit logging should include the parameters that were passed with the statement. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_parameter](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_relation

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies whether session audit logging should create a separate log entry for each relation referenced in a SELECT or DML statement. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_relation](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_rows

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies whether logging will include the rows retrieved or affected by a statement. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_rows](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_statement

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies whether logging will include the statement text and parameters. Depending on requirements, the full statement text might not be required in the audit log. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_statement](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_statement_once

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies whether logging will include the statement text and parameters with the first log entry for a statement/substatement combination or with every entry. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_statement_once](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.role

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies the master role to use for object audit logging. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z\\._]*` |
| Parameter type | dynamic |
| Documentation | [pgaudit.role](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.drop_extra_slots

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | whether to drop extra slots on standby that don't match pg_failover_slots.synchronize_slot_names. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.drop_extra_slots](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.primary_dsn

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | connection string to the primary server for synchronization logical slots on standby. if empty, uses the defaults to primary_conninfo. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.primary_dsn](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.standby_slot_names

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | list of names of slot that must confirm changes before they're sent by the decoding plugin. List of physical replication slots that must confirm durable flush of a given lsn before commits up to that lsn may be replicated to logical peers by the output plugin. Imposes ordering of physical replication before logical replication. |
| Data type | string |
| Default value | `azure_standby_, wal_replica_` |
| Allowed values | `azure_standby_, wal_replica_` |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.standby_slot_names](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.standby_slots_min_confirmed

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Number of slots from pg_failover_slots.standby_slot_names that must confirm lsn. Modifies behaviour of pg_failover_slots.standby_slot_names so to allow logical replication of a transaction after at least pg_failover_slots.standby_slots_min_confirmed physical peers have confirmed the transaction as durably flushed. The value -1 (default) means all entries in pg_failover_slots.standby_slot_namesmust confirm the write. The value 0 causes pg_failover_slots.standby_slots_min_confirmedto be effectively ignored. |
| Data type | integer |
| Default value | `1` |
| Allowed values | `1` |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.standby_slots_min_confirmed](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.synchronize_slot_names

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | list of slots to synchronize from primary to physical standby. |
| Data type | string |
| Default value | `name_like:%%` |
| Allowed values | `name_like:%%` |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.synchronize_slot_names](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.version

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | pg_failover_slots module version. |
| Data type | string |
| Default value | `1.0.1` |
| Allowed values | `1.0.1` |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.version](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_failover_slots.wait_for_inactive_slots

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | whether to wait for an inactive replication slots on primary to catchup with standby. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [pg_failover_slots.wait_for_inactive_slots](https://github.com/EnterpriseDB/pg_failover_slots) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_hint_plan.debug_print

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Logs results of hint parsing. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [pg_hint_plan.debug_print](https://github.com/ossc-db/pg_hint_plan/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_hint_plan.enable_hint

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Force planner to use plans specified in the hint comment preceding to the query. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pg_hint_plan.enable_hint](https://github.com/ossc-db/pg_hint_plan/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_hint_plan.enable_hint_table

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Let pg_hint_plan look up the hint table. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [pg_hint_plan.enable_hint_table](https://github.com/ossc-db/pg_hint_plan/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_hint_plan.hints_anywhere

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Read hints from anywhere in a query. This option lets pg_hint_plan ignore syntax so be cautious for false reads. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [pg_hint_plan.hints_anywhere](https://github.com/ossc-db/pg_hint_plan/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_hint_plan.message_level

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Message level of debug messages. |
| Data type | enumeration |
| Default value | `log` |
| Allowed values | `log` |
| Parameter type | read-only |
| Documentation | [pg_hint_plan.message_level](https://github.com/ossc-db/pg_hint_plan/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_hint_plan.parse_messages

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Message level of parse errors. |
| Data type | enumeration |
| Default value | `info` |
| Allowed values | `info` |
| Parameter type | read-only |
| Documentation | [pg_hint_plan.parse_messages](https://github.com/ossc-db/pg_hint_plan/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.batch_inserts

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Tells PGLogical to use batch insert mechanism if possible. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pglogical.batch_inserts](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.conflict_log_level

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the log level for reporting detected conflicts when the pglogical.conflict_resolution is set to anything else than error. |
| Data type | enumeration |
| Default value | `log` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,info,notice,warning,error,log,fatal,panic` |
| Parameter type | dynamic |
| Documentation | [pglogical.conflict_log_level](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.conflict_resolution

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the resolution method for any detected conflicts between local data and incoming changes. |
| Data type | enumeration |
| Default value | `apply_remote` |
| Allowed values | `error,apply_remote,keep_local,last_update_wins,first_update_wins` |
| Parameter type | dynamic |
| Documentation | [pglogical.conflict_resolution](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.extra_connection_options

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | connection options to add to all peer node connections. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [pglogical.extra_connection_options](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.synchronous_commit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | pglogical specific synchronous commit value. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [pglogical.synchronous_commit](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.temp_directory

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Directory to store dumps for local restore. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [pglogical.temp_directory](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pglogical.use_spi

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Tells PGLogical to use SPI interface to form actual SQL (INSERT, UPDATE, DELETE) statements to apply incoming changes instead of using internal low level interface. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pglogical.use_spi](https://github.com/ArmMbedCloud/pglogical) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgms_stats.is_enabled_fs

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Internal Use Only: This parameter is used as a feature override switch. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgms_wait_sampling.history_period

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Set the frequency, in milliseconds, at which wait events are sampled. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `1-600000` |
| Parameter type | dynamic |
| Documentation | [pgms_wait_sampling.history_period](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgms_wait_sampling.is_enabled_fs

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Internal Use Only: This parameter is used as a feature override switch. If it shows as off, wait sampling will be disabled despite the value set for pgms_wait_sampling.query_capture_mode. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pgms_wait_sampling.is_enabled_fs](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgms_wait_sampling.query_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects which statements are tracked by the pgms_wait_sampling extension. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `all,none` |
| Parameter type | dynamic |
| Documentation | [pgms_wait_sampling.query_capture_mode](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.analyze

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Same purpose as the p_analyze argument to run_maintenance(). |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.analyze](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.dbname

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Required. The database(s) that run_maintenance() will run on. If more than one, use a comma separated list. If not set, BGW will do nothing. |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.dbname](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.interval

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Number of seconds between calls to run_maintenance(). |
| Data type | integer |
| Default value | `3600` |
| Allowed values | `1-315360000` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.interval](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.jobmon

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Same purpose as the p_jobmon argument to run_maintenance(). |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.jobmon](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.role

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The role that run_maintenance() will run as. Default is postgres. Only a single role name is allowed. |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.role](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_prewarm.autoprewarm

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Starts the autoprewarm worker. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pg_prewarm.autoprewarm](https://www.postgresql.org/docs/16/pgprewarm.html#PGPREWARM-CONFIG-PARAMS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_prewarm.autoprewarm_interval

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the interval between dumps of shared buffers. If set to zero, time-based dumping is disabled. |
| Data type | integer |
| Default value | `300` |
| Allowed values | `300` |
| Parameter type | read-only |
| Documentation | [pg_prewarm.autoprewarm_interval](https://www.postgresql.org/docs/16/pgprewarm.html#PGPREWARM-CONFIG-PARAMS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.interval_length_minutes

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the query_store capture interval in minutes for pg_qs - this is the frequency of data persistence. |
| Data type | integer |
| Default value | `15` |
| Allowed values | `1-30` |
| Parameter type | dynamic |
| Documentation | [pg_qs.interval_length_minutes](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.is_enabled_fs

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Internal Use Only: This parameter is used as a feature override switch. If it shows as off, Query Store will be disabled despite the value set for pg_qs.query_capture_mode. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [pg_qs.is_enabled_fs](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.max_captured_queries

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies the number of most relevant queries for which query store captures runtime statistics at each interval. |
| Data type | integer |
| Default value | `500` |
| Allowed values | `100-500` |
| Parameter type | dynamic |
| Documentation | [pg_qs.max_captured_queries](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.max_plan_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum number of bytes that will be saved for query plan text for pg_qs; longer plans will be truncated. |
| Data type | integer |
| Default value | `7500` |
| Allowed values | `100-10000` |
| Parameter type | dynamic |
| Documentation | [pg_qs.max_plan_size](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.max_query_text_length

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum query text length that will be saved; longer queries will be truncated. |
| Data type | integer |
| Default value | `6000` |
| Allowed values | `100-10000` |
| Parameter type | dynamic |
| Documentation | [pg_qs.max_query_text_length](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.parameters_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Whether and when to capture query positional parameters. |
| Data type | enumeration |
| Default value | `capture_parameterless_only` |
| Allowed values | `capture_parameterless_only,capture_first_sample` |
| Parameter type | dynamic |
| Documentation | [pg_qs.parameters_capture_mode](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.query_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets query capture mode for query store. None disables any capturing. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `top,all,none` |
| Parameter type | dynamic |
| Documentation | [pg_qs.query_capture_mode](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.retention_period_in_days

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the retention period window in days for pg_qs - after this time data will be deleted. |
| Data type | integer |
| Default value | `7` |
| Allowed values | `1-30` |
| Parameter type | dynamic |
| Documentation | [pg_qs.retention_period_in_days](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.store_query_plans

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Turns saving query plans on or off for pg_qs |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_qs.store_query_plans](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.track_utility

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects whether utility commands are tracked by pg_qs. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_qs.track_utility](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_stat_statements.max

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum number of statements tracked by pg_stat_statements. |
| Data type | integer |
| Default value | `5000` |
| Allowed values | `100-2147483647` |
| Parameter type | static |
| Documentation | [pg_stat_statements.max](https://www.postgresql.org/docs/14/pgstatstatements.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_stat_statements.save

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Save pg_stat_statements statistics across server shutdowns. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_stat_statements.save](https://www.postgresql.org/docs/14/pgstatstatements.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_stat_statements.track

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Controls which statements are counted by pg_stat_statements. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `top,all,none` |
| Parameter type | dynamic |
| Documentation | [pg_stat_statements.track](https://www.postgresql.org/docs/14/pgstatstatements.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_stat_statements.track_planning

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects whether planning duration is tracked by pg_stat_statements. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_stat_statements.track_planning](https://www.postgresql.org/docs/14/pgstatstatements.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_stat_statements.track_utility

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects whether utility commands are tracked by pg_stat_statements. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_stat_statements.track_utility](https://www.postgresql.org/docs/14/pgstatstatements.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### postgis.gdal_enabled_drivers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Controls postgis GDAL enabled driver settings. |
| Data type | enumeration |
| Default value | `DISABLE_ALL` |
| Allowed values | `DISABLE_ALL,ENABLE_ALL` |
| Parameter type | dynamic |
| Documentation | [postgis.gdal_enabled_drivers](https://postgis.net/docs/postgis_gdal_enabled_drivers.html) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### squeeze.max_xlock_time

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | The maximum time the processed table may be locked exclusively. The source table is locked exclusively during the final stage of processing. If the lock time should exceed this value, the lock is released and the final stage is retried a few more times. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [squeeze.max_xlock_time](https://github.com/cybertec-postgresql/pg_squeeze/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### squeeze.worker_autostart

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Names of databases for which background workers start automatically. Comma-separated list for of databases which squeeze worker starts as soon as the cluster startup has completed. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [squeeze.worker_autostart](https://github.com/cybertec-postgresql/pg_squeeze/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### squeeze.worker_role

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Role that background workers use to connect to database. If background worker was launched automatically on cluster startup, it uses this role to initiate database connection(s). |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [squeeze.worker_role](https://github.com/cybertec-postgresql/pg_squeeze/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### timescaledb.bgw_launcher_poll_time

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Launcher timeout value in milliseconds. Configure the time the launcher waits to look for new TimescaleDB instances. |
| Data type | integer |
| Default value | `60000` |
| Allowed values | `60000` |
| Parameter type | read-only |
| Documentation | [timescaledb.bgw_launcher_poll_time](https://github.com/timescale/timescaledb/blob/main/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### timescaledb.disable_load

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Disable the loading of the actual extension. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [timescaledb.disable_load](https://github.com/timescale/timescaledb/blob/main/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### timescaledb.max_background_workers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum background worker processes allocated to TimescaleDB. Max background worker processes allocated to TimescaleDB - set to at least 1 + number of databases in Postgres instance to use background workers. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `16` |
| Parameter type | read-only |
| Documentation | [timescaledb.max_background_workers](https://github.com/timescale/timescaledb/blob/main/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### timescaledb_osm.disable_load

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Disable the loading of the actual extension. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [timescaledb_osm.disable_load](https://github.com/timescale/timescaledb/blob/main/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



