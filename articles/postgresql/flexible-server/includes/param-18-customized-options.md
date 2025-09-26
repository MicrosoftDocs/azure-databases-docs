---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 05/05/2025
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
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
| Documentation | [auto_explain.log_analyze](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-ANALYZE) |


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
| Documentation | [auto_explain.log_buffers](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-BUFFERS) |


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
| Documentation | [auto_explain.log_format](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-FORMAT) |


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
| Documentation | [auto_explain.log_level](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-LEVEL) |


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
| Documentation | [auto_explain.log_min_duration](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-MIN-DURATION) |


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
| Documentation | [auto_explain.log_nested_statements](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-NESTED-STATEMENTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### auto_explain.log_parameter_max_length

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum length of query parameters to log. Zero logs no query parameters, -1 logs them in full. |
| Data type | integer |
| Default value | `-1` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [auto_explain.log_parameter_max_length](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-MIN-DURATION) |


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
| Documentation | [auto_explain.log_settings](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-SETTINGS) |


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
| Documentation | [auto_explain.log_timing](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TIMING) |


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
| Documentation | [auto_explain.log_triggers](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TRIGGERS) |


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
| Documentation | [auto_explain.log_verbose](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-VERBOSE) |


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
| Documentation | [auto_explain.log_wal](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-WAL) |


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
| Documentation | [auto_explain.sample_rate](https://www.postgresql.org/docs/18/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-SAMPLE-RATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_vacuum_max_threshold

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of tuple updates or deletes prior to vacuum. -1 disables the maximum threshold. |
| Data type | integer |
| Default value | `100000000` |
| Allowed values | `-1-2147483647` |
| Parameter type | dynamic |
| Documentation | [autovacuum_vacuum_max_threshold](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-VACUUM-MAX-THRESHOLD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### autovacuum_worker_slots

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the number of backend slots to allocate for autovacuum workers. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `1-262143` |
| Parameter type | static |
| Documentation | [autovacuum_worker_slots](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-AUTOVACUUM-WORKER-SLOTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.accepted_password_auth_method

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Password authentication methods, separated by comma, that are accepted by the server. |
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
| Description | Buffer size, in megabytes, for snapshot data files. These buffers are used for writing snapshot data. While this indirectly influences the file size, the actual file size may be smaller due to compression and other factors. |
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
| Description | Stores temporary objects on local Solid State Disk. |
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
| Description | List of extensions, separated by comma, that are allowlisted. If an extension is not in this list, trying to execute CREATE, ALTER, COMMENT, DROP EXTENSION statements on that extension fails. |
| Data type | set |
| Default value | |
| Allowed values | `address_standardizer,address_standardizer_data_us,amcheck,anon,azure_storage,bloom,btree_gin,btree_gist,citext,cube,dblink,dict_int,dict_xsyn,earthdistance,fuzzystrmatch,hll,hstore,hypopg,intagg,intarray,isn,lo,login_hook,ltree,oracle_fdw,orafce,pageinspect,pg_buffercache,pg_cron,pg_freespacemap,pg_hint_plan,pg_partman,pg_prewarm,pg_repack,pg_squeeze,pg_stat_statements,pg_trgm,pg_visibility,pgaudit,pgcrypto,pglogical,pgrouting,pgrowlocks,pgstattuple,plpgsql,plv8,postgis,postgis_raster,postgis_sfcgal,postgis_tiger_geocoder,postgis_topology,postgres_fdw,postgres_protobuf,semver,session_variable,sslinfo,tablefunc,tdigest,tds_fdw,topn,tsm_system_rows,tsm_system_time,unaccent,uuid-ossp,vector` |
| Parameter type | dynamic |
| Documentation | [azure.extensions](https://go.microsoft.com/fwlink/?linkid=2274269) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.fabric_mirror_enabled

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Validates prerequisites for Fabric Mirroring to function properly. Validation only occurs at the very moment this setting is changed from 'off' to 'on'. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure.fabric_mirror_enabled](https://go.microsoft.com/fwlink/?linkid=2285682) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_copy_with_binary

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | When set to on, this parameter will enable the use of the binary format for copying data during migration. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_copy_with_binary](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_analyze

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | When set to on, this parameter will skip the analyze phase (`vacuumdb --analyze-only`) during the migration. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_analyze](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_extensions

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | When set to on, this parameter will skip the migration of extensions. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_extensions](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_large_objects

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | When set to on, this parameter will skip the migration of large objects such as BLOBs. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [azure.migration_skip_large_objects](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_skip_role_user

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | When set to on, this parameter will exclude user roles from the migration process. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [azure.migration_skip_role_user](https://aka.ms/migration_parameters) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### azure.migration_table_split_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | When set, this parameter specifies the size at which tables will be partitioned during migration. |
| Data type | integer |
| Default value | `20480` |
| Allowed values | `1-204800` |
| Parameter type | dynamic |
| Documentation | [azure.migration_table_split_size](https://aka.ms/migration_parameters) |


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



### credcheck.whitlist

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Comma separated list of usernames to exclude from password policy check. |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.whitlist](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### credcheck.whitlist_auth_failure

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Comma separated list of usernames to exclude from max authentication failure check. |
| Data type | string |
| Default value | |
| Allowed values | `.*` |
| Parameter type | dynamic |
| Documentation | [credcheck.whitlist_auth_failure](https://github.com/HexaCluster/credcheck/blob/master/README.md#checks) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### cron.database_name

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Database in which pg_cron metadata is kept. |
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
| Description | Maximum number of jobs that can run concurrently. |
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



### enable_distinct_reordering

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables reordering of DISTINCT keys. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [enable_distinct_reordering](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-ENABLE-DISTINCT-REORDERING) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### enable_group_by_reordering

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables reordering of GROUP BY keys. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [enable_group_by_reordering](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-ENABLE-GROUPBY-REORDERING) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### enable_self_join_elimination

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables removal of unique self-joins. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [enable_self_join_elimination](https://www.postgresql.org/docs/18/runtime-config-query.html#GUC-ENABLE-SELF-JOIN-ELIMINATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### extension_control_path

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | A path to search for extensions, specifically extension control files (name.control). |
| Data type | string |
| Default value | `$system` |
| Allowed values | `$system` |
| Parameter type | read-only |
| Documentation | [extension_control_path](https://www.postgresql.org/docs/18/runtime-config-client.html#GUC-EXTENSION-CONTROL-PATH) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### file_copy_method

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects the file copy method. |
| Data type | enumeration |
| Default value | `COPY` |
| Allowed values | `COPY` |
| Parameter type | read-only |
| Documentation | [file_copy_method](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC_FILE_COPY_METHOD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### huge_pages_status

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Indicates the status of huge pages. |
| Data type | enumeration |
| Default value | `on` |
| Allowed values | `on` |
| Parameter type | read-only |
| Documentation | [huge_pages_status](https://www.postgresql.org/docs/18/runtime-config-preset.html#GUC-HUGE-PAGES-STATUS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### idle_replication_slot_timeout

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the duration a replication slot can remain idle before it is invalidated. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-35791394` |
| Parameter type | dynamic |
| Documentation | [idle_replication_slot_timeout](https://www.postgresql.org/docs/18/runtime-config-replication.html#GUC-IDLE-REPLICATION-SLOT-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.analysis_interval

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to 'REPORT'. |
| Data type | integer |
| Default value | `720` |
| Allowed values | `60-10080` |
| Parameter type | dynamic |
| Documentation | [index_tuning.analysis_interval](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.max_columns_per_index

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of columns that can be part of the index key for any recommended index. |
| Data type | integer |
| Default value | `2` |
| Allowed values | `1-10` |
| Parameter type | dynamic |
| Documentation | [index_tuning.max_columns_per_index](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.max_index_count

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of indexes that can be recommended for each database during one optimization session. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `1-25` |
| Parameter type | dynamic |
| Documentation | [index_tuning.max_index_count](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.max_indexes_per_table

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of indexes that can be recommended for each table. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `1-25` |
| Parameter type | dynamic |
| Documentation | [index_tuning.max_indexes_per_table](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.max_queries_per_database

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Number of slowest queries per database for which indexes can be recommended. |
| Data type | integer |
| Default value | `25` |
| Allowed values | `5-100` |
| Parameter type | dynamic |
| Documentation | [index_tuning.max_queries_per_database](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.max_regression_factor

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Acceptable regression introduced by a recommended index on any of the queries analyzed during one optimization session. |
| Data type | numeric |
| Default value | `0.1` |
| Allowed values | `0.05-0.2` |
| Parameter type | dynamic |
| Documentation | [index_tuning.max_regression_factor](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.max_total_size_factor

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum total size, in percentage of total disk space, that all recommended indexes for any given database can use. |
| Data type | numeric |
| Default value | `0.1` |
| Allowed values | `0-1.0` |
| Parameter type | dynamic |
| Documentation | [index_tuning.max_total_size_factor](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.min_improvement_factor

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Cost improvement that a recommended index must provide to at least one of the queries analyzed during one optimization session. |
| Data type | numeric |
| Default value | `0.2` |
| Allowed values | `0-20.0` |
| Parameter type | dynamic |
| Documentation | [index_tuning.min_improvement_factor](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.mode

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Configures index optimization as disabled ('OFF') or enabled to only emit recommendation. Requires Query Store to be enabled by setting pg_qs.query_capture_mode to 'TOP' or 'ALL'. |
| Data type | enumeration |
| Default value | `off` |
| Allowed values | `off,report` |
| Parameter type | dynamic |
| Documentation | [index_tuning.mode](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.unused_dml_per_table

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum number of daily average DML operations affecting the table, so that their unused indexes are considered for dropping. |
| Data type | integer |
| Default value | `1000` |
| Allowed values | `0-9999999` |
| Parameter type | dynamic |
| Documentation | [index_tuning.unused_dml_per_table](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.unused_min_period

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum number of days the index has not been used, based on system statistics, so that it is considered for dropping. |
| Data type | integer |
| Default value | `35` |
| Allowed values | `30-720` |
| Parameter type | dynamic |
| Documentation | [index_tuning.unused_min_period](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### index_tuning.unused_reads_per_table

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Minimum number of daily average read operations affecting the table, so that their unused indexes are considered for dropping. |
| Data type | integer |
| Default value | `1000` |
| Allowed values | `0-9999999` |
| Parameter type | dynamic |
| Documentation | [index_tuning.unused_reads_per_table](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### io_combine_limit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Limit on the size of data reads and writes. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `1-128` |
| Parameter type | dynamic |
| Documentation | [io_combine_limit](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-IO-COMBINE-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### io_max_combine_limit

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Server-wide limit that clamps io_combine_limit. |
| Data type | integer |
| Default value | `16` |
| Allowed values | `1-128` |
| Parameter type | dynamic |
| Documentation | [io_max_combine_limit](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-IO-MAX-COMBINE-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### io_max_concurrency

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Max number of IOs that one process can execute simultaneously. |
| Data type | integer |
| Default value | `64` |
| Allowed values | `-1-1024` |
| Parameter type | static |
| Documentation | [io_max_concurrency](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-IO-MAX-CONCURRENCY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### io_method

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects the method for executing asynchronous I/O. |
| Data type | enumeration |
| Default value | `worker` |
| Allowed values | `worker,sync` |
| Parameter type | static |
| Documentation | [io_method](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-IO-METHOD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### io_workers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Number of IO worker processes, for io_method=worker. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-32` |
| Parameter type | dynamic |
| Documentation | [io_workers](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-IO-WORKERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### logfiles.download_enable

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables or disables server logs functionality. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [logfiles.download_enable](https://go.microsoft.com/fwlink/?linkid=2274270) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### logfiles.retention_days

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the retention period window in days for server logs - after this time data will be deleted. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-7` |
| Parameter type | dynamic |
| Documentation | [logfiles.retention_days](https://go.microsoft.com/fwlink/?linkid=2274270) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### log_lock_failure

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Controls whether a detailed log message is produced when a lock acquisition fails. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [log_lock_failure](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-LOG-LOCK-FAILURE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_active_replication_origins

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum number of active replication origins. |
| Data type | integer |
| Default value | `10` |
| Allowed values | `0-262143` |
| Parameter type | static |
| Documentation | [max_active_replication_origins](https://www.postgresql.org/docs/18/runtime-config-replication.html#GUC-MAX-ACTIVE-REPLICATION-ORIGINS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### max_notify_queue_pages

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the maximum number of allocated pages for NOTIFY / LISTEN queue. |
| Data type | integer |
| Default value | `1048576` |
| Allowed values | `1048576` |
| Parameter type | read-only |
| Documentation | [max_notify_queue_pages](https://www.postgresql.org/docs/18/runtime-config-resource.html#GUC-MAX-NOTIFY-QUEUE-PAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### md5_password_warnings

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables deprecation warnings for MD5 passwords. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [md5_password_warnings](https://www.postgresql.org/docs/18/runtime-config-logging.html#GUC-MD5-PASSWORD-WARNINGS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### num_os_semaphores

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Shows the number of semaphores required for the server. |
| Data type | integer |
| Default value | `3511` |
| Allowed values | `3511` |
| Parameter type | read-only |
| Documentation | [num_os_semaphores](https://www.postgresql.org/docs/18/runtime-config-preset.html#GUC-NUM-OS-SEMAPHORES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### oauth_validator_libraries

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Lists libraries that may be called to validate OAuth v2 bearer tokens. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z0-9\\._,]*` |
| Parameter type | dynamic |
| Documentation | [oauth_validator_libraries](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-OAUTH-VALIDATOR-LIBRARIES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaadauth.enable_group_sync

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables synchronization of Microsoft Entra ID group members. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies which classes of statements will be logged by session audit logging. Multiple classes can be provided using a comma-separated list and classes can be subtracted by prefacing the class with a - sign. |
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
| Description | Specifies that session logging should be enabled in the case where all relations in a statement are in pg_catalog. Disabling this setting will reduce noise in the log from tools like psql and PgAdmin that query the catalog heavily. |
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
| Description | Specifies whether audit messages should be visible to the client. This setting should generally be left disabled but may be useful for debugging or other purposes. |
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
| Description | Specifies the log level that will be used for log entries. This setting is used for regression testing and may also be useful to end users for testing or other purposes. It is not intended to be used in a production environment as it may leak which statements are being logged to the user. |
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
| Description | Specifies that audit logging should include the parameters that were passed with the statement. When parameters are present they will be be included in CSV format after the statement text. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_parameter](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_parameter_max_size

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies, in bytes, the maximum length of variable-length parameters to log. If 0 (the default), parameters are not checked for size. If set, when the size of the parameter is longer than the setting, the value in the audit log is replaced with a placeholder. Note that for character types, the length is in bytes for the parameter's encoding, not characters. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-1073741823` |
| Parameter type | dynamic |
| Documentation | [pgaudit.log_parameter_max_size](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgaudit.log_relation

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Specifies whether session audit logging should create a separate log entry for each relation referenced in a SELECT or DML statement. This is a useful shortcut for exhaustive logging without using object audit logging. |
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
| Description | Specifies whether logging will include the statement text and parameters with the first log entry for a statement/substatement combination or with every entry. Disabling this setting will result in less verbose logging but may make it more difficult to determine the statement that generated a log entry, though the statement/substatement pair along with the process id should suffice to identify the statement text logged with a previous entry. |
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
| Description | Specifies the master role to use for object audit logging. Multiple audit roles can be defined by granting them to the master role. This allows multiple groups to be in charge of different aspects of audit logging. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z\\._]*` |
| Parameter type | dynamic |
| Documentation | [pgaudit.role](https://github.com/pgaudit/pgaudit/blob/master/README.md) |


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
| Description | Sets the the frequency, in milliseconds, at which wait events are sampled. |
| Data type | integer |
| Default value | `100` |
| Allowed values | `1-600000` |
| Parameter type | dynamic |
| Documentation | [pgms_wait_sampling.history_period](https://go.microsoft.com/fwlink/?linkid=2274607) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pgms_wait_sampling.query_capture_mode

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects types of wait events are tracked by this extension. Need to reload the config to make change take effect. |
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
| Description | Whether to run an analyze on a partition set whenever a new partition is created during run_maintenance(). Set to 'on' to send TRUE (default). Set to 'off' to send FALSE. |
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
| Description | CSV list of specific databases in the cluster to run pg_partman BGW on. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z0-9_,-]*` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.dbname](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.interval

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | How often run_maintenance() is called (in seconds). |
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
| Description | Whether to log run_maintenance() calls to pg_jobmon if it is installed. Set to 'on' to send TRUE (default). Set to 'off' to send FALSE. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [pg_partman_bgw.jobmon](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.maintenance_wait

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | How long to wait between each partition set when running maintenance (in seconds). |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0` |
| Parameter type | read-only |
| Documentation | [pg_partman_bgw.maintenance_wait](https://github.com/pgpartman/pg_partman) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_partman_bgw.role

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Role to be used by BGW. Must have execute permissions on run_maintenance(). |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z\\._]*` |
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
| Documentation | [pg_prewarm.autoprewarm](https://www.postgresql.org/docs/18/pgprewarm.html#PGPREWARM-CONFIG-PARAMS) |


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
| Documentation | [pg_prewarm.autoprewarm_interval](https://www.postgresql.org/docs/18/pgprewarm.html#PGPREWARM-CONFIG-PARAMS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_qs.interval_length_minutes

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the aggregration window in minutes. Need to reload the config to make change take effect. |
| Data type | integer |
| Default value | `15` |
| Allowed values | `1-30` |
| Parameter type | static |
| Documentation | [pg_qs.interval_length_minutes](https://go.microsoft.com/fwlink/?linkid=2274607) |


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
| Description | Sets the maximum number of bytes that will be saved for query plan text; longer plans will be truncated. Need to reload the config for this change to take effect. |
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
| Description | Sets the maximum query text length that will be saved; longer queries will be truncated. Need to reload the config to make change take effect. |
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
| Description | Selects how positional query parameters are captured by pg_qs. Need to reload the config for the change to take effect. |
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
| Description | Selects which statements are tracked by pg_qs. Need to reload the config to make change take effect. |
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
| Description | Sets the retention period window in days for pg_qs - after this time data will be deleted. Need to restart the server to make change take effect. |
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
| Description | Turns saving query plans on or off. Need to reload the config for the change to take effect. |
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
| Description | Selects whether utility commands are tracked by pg_qs. Need to reload the config to make change take effect. |
| Data type | boolean |
| Default value | `off` |
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
| Documentation | [pg_stat_statements.max](https://www.postgresql.org/docs/18/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) |


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
| Documentation | [pg_stat_statements.save](https://www.postgresql.org/docs/18/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### pg_stat_statements.track

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Selects which statements are tracked by pg_stat_statements. |
| Data type | enumeration |
| Default value | `none` |
| Allowed values | `top,all,none` |
| Parameter type | dynamic |
| Documentation | [pg_stat_statements.track](https://www.postgresql.org/docs/18/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) |


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
| Documentation | [pg_stat_statements.track_planning](https://www.postgresql.org/docs/18/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) |


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
| Documentation | [pg_stat_statements.track_utility](https://www.postgresql.org/docs/18/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) |


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



### squeeze.workers_per_database

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Maximum number of squeeze worker processes launched for each database. |
| Data type | integer |
| Default value | `1` |
| Allowed values | `1` |
| Parameter type | read-only |
| Documentation | [squeeze.workers_per_database](https://github.com/cybertec-postgresql/pg_squeeze/blob/master/README.md) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_groups

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the group(s) to use for Diffie-Hellman key exchange. Multiple groups can be specified using a colon-separated list. |
| Data type | string |
| Default value | `X25519:prime256v1` |
| Allowed values | `X25519:prime256v1` |
| Parameter type | read-only |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### ssl_tls13_ciphers

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Sets the list of allowed TLSv1.3 cipher suites. An empty string means use the default cipher suites. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [ssl_tls13_ciphers](https://www.postgresql.org/docs/18/runtime-config-connection.html#GUC-SSL-TLS13-CIPHERS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### summarize_wal

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Starts the WAL summarizer process to enable incremental backup. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [summarize_wal](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SUMMARIZE-WAL) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### synchronized_standby_slots

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Lists streaming replication standby server replication slot names that logical WAL sender processes will wait for. Logical WAL sender processes will send decoded changes to output plugins only after the specified replication slots have confirmed receiving WAL. |
| Data type | string |
| Default value | |
| Allowed values | |
| Parameter type | read-only |
| Documentation | [synchronized_standby_slots](https://www.postgresql.org/docs/18/runtime-config-replication.html#GUC-SYNCHRONIZED-STANDBY-SLOTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### sync_replication_slots

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables a physical standby to synchronize logical failover replication slots from the primary server. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [sync_replication_slots](https://www.postgresql.org/docs/18/runtime-config-replication.html#GUC-SYNC-REPLICATION-SLOTS) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### trace_connection_negotiation

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Logs details of pre-authentication connection handshake. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [trace_connection_negotiation](https://www.postgresql.org/docs/18/runtime-config-developer.html#GUC-TRACE-NOTIFY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### track_cost_delay_timing

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Collects timing statistics for cost-based vacuum delay. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [track_cost_delay_timing](https://www.postgresql.org/docs/18/runtime-config-statistics.html#GUC-TRACK-COST-DELAY-TIMING) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_max_eager_freeze_failure_rate

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Fraction of pages in a relation vacuum can scan and fail to freeze before disabling eager scanning. A value of 0.0 disables eager scanning and a value of 1.0 will eagerly scan up to 100 percent of the all-visible pages in the relation. If vacuum successfully freezes these pages, the cap is lower than 100 percent, because the goal is to amortize page freezing across multiple vacuums. |
| Data type | numeric |
| Default value | `0.03` |
| Allowed values | `0.0-1.0` |
| Parameter type | dynamic |
| Documentation | [vacuum_max_eager_freeze_failure_rate](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-VACUUM-MAX-EAGER-FREEZE-FAILURE-RATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_truncate

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Enables vacuum to truncate empty pages at the end of the table. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [vacuum_truncate](https://www.postgresql.org/docs/18/runtime-config-vacuum.html#GUC-VACUUM-TRUNCATE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### wal_summary_keep_time

| Attribute | Value |
| --- | --- |
| Category | Customized Options |
| Description | Time for which WAL summary files should be kept. |
| Data type | integer |
| Default value | `14400` |
| Allowed values | `14400` |
| Parameter type | read-only |
| Documentation | [wal_summary_keep_time](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-WAL-SUMMARY-KEEP-TIME) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



