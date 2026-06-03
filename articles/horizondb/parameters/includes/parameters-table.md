---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 06/02/2026
ms.service: azure-database-postgresql
ms.topic: include
ms.custom:
  - automatically generated
---

### Adaptive Autovacuum

| Name | Versions | Description |
| --- | --- | --- |
| `adaptive_autovacuum.open_transaction_threshold` | [17](../parameters-adaptive-autovacuum.md#adaptive_autovacuumopen_transaction_threshold) | Specifies the timeout, in seconds, before an orphan transaction is rolled back and before a long running transaction is terminated. |
| `adaptive_autovacuum.optimize_configurations` | [17](../parameters-adaptive-autovacuum.md#adaptive_autovacuumoptimize_configurations) | Configures parameter tuning as disabled ('OFF') or enabled to tune and update autovacuum parameters. |

### Autovacuum

| Name | Versions | Description |
| --- | --- | --- |
| `autovacuum` | [17](../parameters-autovacuum.md#autovacuum) | Starts the autovacuum subprocess. |
| `autovacuum_analyze_scale_factor` | [17](../parameters-autovacuum.md#autovacuum_analyze_scale_factor) | Number of tuple inserts, updates, or deletes prior to analyze as a fraction of reltuples. |
| `autovacuum_analyze_threshold` | [17](../parameters-autovacuum.md#autovacuum_analyze_threshold) | Minimum number of tuple inserts, updates, or deletes prior to analyze. |
| `autovacuum_freeze_max_age` | [17](../parameters-autovacuum.md#autovacuum_freeze_max_age) | Age at which to autovacuum a table to prevent transaction ID wraparound. |
| `autovacuum_max_workers` | [17](../parameters-autovacuum.md#autovacuum_max_workers) | Sets the maximum number of simultaneously running autovacuum worker processes. |
| `autovacuum_multixact_freeze_max_age` | [17](../parameters-autovacuum.md#autovacuum_multixact_freeze_max_age) | Multixact age at which to autovacuum a table to prevent multixact wraparound. |
| `autovacuum_naptime` | [17](../parameters-autovacuum.md#autovacuum_naptime) | Time to sleep between autovacuum runs. |
| `autovacuum_vacuum_cost_delay` | [17](../parameters-autovacuum.md#autovacuum_vacuum_cost_delay) | Vacuum cost delay in milliseconds, for autovacuum. |
| `autovacuum_vacuum_cost_limit` | [17](../parameters-autovacuum.md#autovacuum_vacuum_cost_limit) | Vacuum cost amount available before napping, for autovacuum. |
| `autovacuum_vacuum_insert_scale_factor` | [17](../parameters-autovacuum.md#autovacuum_vacuum_insert_scale_factor) | Number of tuple inserts prior to vacuum as a fraction of reltuples. |
| `autovacuum_vacuum_insert_threshold` | [17](../parameters-autovacuum.md#autovacuum_vacuum_insert_threshold) | Minimum number of tuple inserts prior to vacuum, or -1 to disable insert vacuums. |
| `autovacuum_vacuum_scale_factor` | [17](../parameters-autovacuum.md#autovacuum_vacuum_scale_factor) | Number of tuple updates or deletes prior to vacuum as a fraction of reltuples. |
| `autovacuum_vacuum_threshold` | [17](../parameters-autovacuum.md#autovacuum_vacuum_threshold) | Minimum number of tuple updates or deletes prior to vacuum. |

### Client Connection Defaults / Locale and Formatting

| Name | Versions | Description |
| --- | --- | --- |
| `client_encoding` | [17](../parameters-client-connection-defaults-locale-formatting.md#client_encoding) | Sets the client's character set encoding. |
| `DateStyle` | [17](../parameters-client-connection-defaults-locale-formatting.md#datestyle) | Sets the display format for date and time values. Also controls interpretation of ambiguous date inputs. |
| `default_text_search_config` | [17](../parameters-client-connection-defaults-locale-formatting.md#default_text_search_config) | Sets default text search configuration. |
| `extra_float_digits` | [17](../parameters-client-connection-defaults-locale-formatting.md#extra_float_digits) | Sets the number of digits displayed for floating-point values. This affects real, double precision, and geometric data types. A zero or negative parameter value is added to the standard number of digits (FLT_DIG or DBL_DIG as appropriate). Any value greater than zero selects precise output mode. |
| `icu_validation_level` | [17](../parameters-client-connection-defaults-locale-formatting.md#icu_validation_level) | Log level for reporting invalid ICU locale strings. |
| `IntervalStyle` | [17](../parameters-client-connection-defaults-locale-formatting.md#intervalstyle) | Sets the display format for interval values. |
| `lc_messages` | [17](../parameters-client-connection-defaults-locale-formatting.md#lc_messages) | Sets the language in which messages are displayed. |
| `lc_monetary` | [17](../parameters-client-connection-defaults-locale-formatting.md#lc_monetary) | Sets the locale for formatting monetary amounts. |
| `lc_numeric` | [17](../parameters-client-connection-defaults-locale-formatting.md#lc_numeric) | Sets the locale for formatting numbers. |
| `lc_time` | [17](../parameters-client-connection-defaults-locale-formatting.md#lc_time) | Sets the locale for formatting date and time values. |
| `TimeZone` | [17](../parameters-client-connection-defaults-locale-formatting.md#timezone) | Sets the time zone for displaying and interpreting time stamps. |
| `timezone_abbreviations` | [17](../parameters-client-connection-defaults-locale-formatting.md#timezone_abbreviations) | Selects a file of time zone abbreviations. |

### Client Connection Defaults / Other Defaults

| Name | Versions | Description |
| --- | --- | --- |
| `dynamic_library_path` | [17](../parameters-client-connection-defaults-defaults.md#dynamic_library_path) | Sets the path for dynamically loadable modules. If a dynamically loadable module needs to be opened and the specified name doesn't have a directory component (i.e., the name doesn't contain a slash), the system will search this path for the specified file. |
| `gin_fuzzy_search_limit` | [17](../parameters-client-connection-defaults-defaults.md#gin_fuzzy_search_limit) | Sets the maximum allowed result for exact search by GIN. |

### Client Connection Defaults / Shared Library Preloading

| Name | Versions | Description |
| --- | --- | --- |
| `jit_provider` | [17](../parameters-client-connection-defaults-shared-library-preload.md#jit_provider) | JIT provider to use. |
| `local_preload_libraries` | [17](../parameters-client-connection-defaults-shared-library-preload.md#local_preload_libraries) | Lists unprivileged shared libraries to preload into each backend. |
| `session_preload_libraries` | [17](../parameters-client-connection-defaults-shared-library-preload.md#session_preload_libraries) | Lists shared libraries to preload into each backend. |
| `shared_preload_libraries` | [17](../parameters-client-connection-defaults-shared-library-preload.md#shared_preload_libraries) | Lists shared libraries to preload into server. |

### Client Connection Defaults / Statement Behavior

| Name | Versions | Description |
| --- | --- | --- |
| `bytea_output` | [17](../parameters-client-connection-defaults-statement-behavior.md#bytea_output) | Sets the output format for bytea. |
| `check_function_bodies` | [17](../parameters-client-connection-defaults-statement-behavior.md#check_function_bodies) | Check routine bodies during CREATE FUNCTION and CREATE PROCEDURE. |
| `client_min_messages` | [17](../parameters-client-connection-defaults-statement-behavior.md#client_min_messages) | Sets the message levels that are sent to the client. Each level includes all the levels that follow it. The later the level, the fewer messages are sent. |
| `createrole_self_grant` | [17](../parameters-client-connection-defaults-statement-behavior.md#createrole_self_grant) | Sets whether a CREATEROLE user automatically grants the role to themselves, and with which options. |
| `default_table_access_method` | [17](../parameters-client-connection-defaults-statement-behavior.md#default_table_access_method) | Sets the default table access method for new tables. |
| `default_tablespace` | [17](../parameters-client-connection-defaults-statement-behavior.md#default_tablespace) | Sets the default tablespace to create tables and indexes in. An empty string selects the database's default tablespace. |
| `default_toast_compression` | [17](../parameters-client-connection-defaults-statement-behavior.md#default_toast_compression) | Sets the default compression method for compressible values. |
| `default_transaction_deferrable` | [17](../parameters-client-connection-defaults-statement-behavior.md#default_transaction_deferrable) | Sets the default deferrable status of new transactions. |
| `default_transaction_isolation` | [17](../parameters-client-connection-defaults-statement-behavior.md#default_transaction_isolation) | Sets the transaction isolation level of each new transaction. |
| `default_transaction_read_only` | [17](../parameters-client-connection-defaults-statement-behavior.md#default_transaction_read_only) | Sets the default read-only status of new transactions. |
| `event_triggers` | [17](../parameters-client-connection-defaults-statement-behavior.md#event_triggers) | Enables event triggers. When enabled, event triggers will fire for all applicable statements. |
| `gin_pending_list_limit` | [17](../parameters-client-connection-defaults-statement-behavior.md#gin_pending_list_limit) | Sets the maximum size of the pending list for GIN index. |
| `idle_in_transaction_session_timeout` | [17](../parameters-client-connection-defaults-statement-behavior.md#idle_in_transaction_session_timeout) | Sets the maximum allowed idle time between queries, when in a transaction. A value of 0 turns off the timeout. |
| `idle_session_timeout` | [17](../parameters-client-connection-defaults-statement-behavior.md#idle_session_timeout) | Sets the maximum allowed idle time between queries, when not in a transaction. A value of 0 turns off the timeout. |
| `lock_timeout` | [17](../parameters-client-connection-defaults-statement-behavior.md#lock_timeout) | Sets the maximum allowed duration of any wait for a lock. A value of 0 turns off the timeout. |
| `restrict_nonsystem_relation_kind` | [17](../parameters-client-connection-defaults-statement-behavior.md#restrict_nonsystem_relation_kind) | Prohibits access to non-system relations of specified kinds. |
| `row_security` | [17](../parameters-client-connection-defaults-statement-behavior.md#row_security) | Enable row security. When enabled, row security will be applied to all users. |
| `search_path` | [17](../parameters-client-connection-defaults-statement-behavior.md#search_path) | Sets the schema search order for names that aren't schema-qualified. |
| `session_replication_role` | [17](../parameters-client-connection-defaults-statement-behavior.md#session_replication_role) | Sets the session's behavior for triggers and rewrite rules. |
| `statement_timeout` | [17](../parameters-client-connection-defaults-statement-behavior.md#statement_timeout) | Sets the maximum allowed duration of any statement. A value of 0 turns off the timeout. |
| `temp_tablespaces` | [17](../parameters-client-connection-defaults-statement-behavior.md#temp_tablespaces) | Sets the tablespace(s) to use for temporary tables and sort files. |
| `transaction_deferrable` | [17](../parameters-client-connection-defaults-statement-behavior.md#transaction_deferrable) | Whether to defer a read-only serializable transaction until it can be executed with no possible serialization failures. |
| `transaction_isolation` | [17](../parameters-client-connection-defaults-statement-behavior.md#transaction_isolation) | Sets the current transaction's isolation level. |
| `transaction_read_only` | [17](../parameters-client-connection-defaults-statement-behavior.md#transaction_read_only) | Sets the current transaction's read-only status. |
| `transaction_timeout` | [17](../parameters-client-connection-defaults-statement-behavior.md#transaction_timeout) | Sets the maximum allowed duration of any transaction within a session (not a prepared transaction). A value of 0 turns off the timeout. |
| `vacuum_failsafe_age` | [17](../parameters-client-connection-defaults-statement-behavior.md#vacuum_failsafe_age) | Age at which VACUUM should trigger failsafe to avoid a wraparound outage. |
| `vacuum_freeze_min_age` | [17](../parameters-client-connection-defaults-statement-behavior.md#vacuum_freeze_min_age) | Minimum age at which VACUUM should freeze a table row. |
| `vacuum_freeze_table_age` | [17](../parameters-client-connection-defaults-statement-behavior.md#vacuum_freeze_table_age) | Age at which VACUUM should scan whole table to freeze tuples. |
| `vacuum_multixact_failsafe_age` | [17](../parameters-client-connection-defaults-statement-behavior.md#vacuum_multixact_failsafe_age) | Multixact age at which VACUUM should trigger failsafe to avoid a wraparound outage. |
| `vacuum_multixact_freeze_min_age` | [17](../parameters-client-connection-defaults-statement-behavior.md#vacuum_multixact_freeze_min_age) | Minimum age at which VACUUM should freeze a MultiXactId in a table row. |
| `vacuum_multixact_freeze_table_age` | [17](../parameters-client-connection-defaults-statement-behavior.md#vacuum_multixact_freeze_table_age) | Multixact age at which VACUUM should scan whole table to freeze tuples. |
| `xmlbinary` | [17](../parameters-client-connection-defaults-statement-behavior.md#xmlbinary) | Sets how binary values are to be encoded in XML. |
| `xmloption` | [17](../parameters-client-connection-defaults-statement-behavior.md#xmloption) | Sets whether XML data in implicit parsing and serialization operations is to be considered as documents or content fragments. |

### Connections and Authentication / Authentication

| Name | Versions | Description |
| --- | --- | --- |
| `authentication_timeout` | [17](../parameters-connections-authentication-authentication.md#authentication_timeout) | Sets the maximum allowed time to complete client authentication. |
| `db_user_namespace` | [17](../parameters-connections-authentication-authentication.md#db_user_namespace) | Enables per-database user names. |
| `gss_accept_delegation` | [17](../parameters-connections-authentication-authentication.md#gss_accept_delegation) | Sets whether GSSAPI delegation should be accepted from the client. |
| `krb_caseins_users` | [17](../parameters-connections-authentication-authentication.md#krb_caseins_users) | Sets whether Kerberos and GSSAPI user names should be treated as case-insensitive. |
| `krb_server_keyfile` | [17](../parameters-connections-authentication-authentication.md#krb_server_keyfile) | Sets the location of the Kerberos server key file. |
| `password_encryption` | [17](../parameters-connections-authentication-authentication.md#password_encryption) | Chooses the algorithm for encrypting passwords. |
| `scram_iterations` | [17](../parameters-connections-authentication-authentication.md#scram_iterations) | Sets the iteration count for SCRAM secret generation. |

### Connections and Authentication / Connection Settings

| Name | Versions | Description |
| --- | --- | --- |
| `bonjour` | [17](../parameters-connections-authentication-connection-settings.md#bonjour) | Enables advertising the server via Bonjour. |
| `bonjour_name` | [17](../parameters-connections-authentication-connection-settings.md#bonjour_name) | Sets the Bonjour service name. |
| `listen_addresses` | [17](../parameters-connections-authentication-connection-settings.md#listen_addresses) | Sets the host name or IP address(es) to listen to. |
| `max_connections` | [17](../parameters-connections-authentication-connection-settings.md#max_connections) | Sets the maximum number of concurrent connections. |
| `port` | [17](../parameters-connections-authentication-connection-settings.md#port) | Sets the TCP port the server listens on. |
| `reserved_connections` | [17](../parameters-connections-authentication-connection-settings.md#reserved_connections) | Sets the number of connection slots reserved for roles with privileges of pg_use_reserved_connections. |
| `superuser_reserved_connections` | [17](../parameters-connections-authentication-connection-settings.md#superuser_reserved_connections) | Sets the number of connection slots reserved for superusers. |
| `unix_socket_directories` | [17](../parameters-connections-authentication-connection-settings.md#unix_socket_directories) | Sets the directories where Unix-domain sockets will be created. |
| `unix_socket_group` | [17](../parameters-connections-authentication-connection-settings.md#unix_socket_group) | Sets the owning group of the Unix-domain socket. The owning user of the socket is always the user that starts the server. |
| `unix_socket_permissions` | [17](../parameters-connections-authentication-connection-settings.md#unix_socket_permissions) | Sets the access permissions of the Unix-domain socket. Unix-domain sockets use the usual Unix file system permission set. The parameter value is expected to be a numeric mode specification in the form accepted by the chmod and umask system calls. (To use the customary octal format the number must start with a 0 (zero).). |

### Connections and Authentication / SSL

| Name | Versions | Description |
| --- | --- | --- |
| `ssl` | [17](../parameters-connections-authentication-ssl.md#ssl) | Enables SSL connections. |
| `ssl_ca_file` | [17](../parameters-connections-authentication-ssl.md#ssl_ca_file) | Location of the SSL certificate authority file. |
| `ssl_cert_file` | [17](../parameters-connections-authentication-ssl.md#ssl_cert_file) | Location of the SSL server certificate file. |
| `ssl_ciphers` | [17](../parameters-connections-authentication-ssl.md#ssl_ciphers) | Sets the list of allowed SSL ciphers. |
| `ssl_crl_dir` | [17](../parameters-connections-authentication-ssl.md#ssl_crl_dir) | Location of the SSL certificate revocation list directory. |
| `ssl_crl_file` | [17](../parameters-connections-authentication-ssl.md#ssl_crl_file) | Location of the SSL certificate revocation list file. |
| `ssl_dh_params_file` | [17](../parameters-connections-authentication-ssl.md#ssl_dh_params_file) | Location of the SSL DH parameters file. |
| `ssl_ecdh_curve` | [17](../parameters-connections-authentication-ssl.md#ssl_ecdh_curve) | Sets the curve to use for ECDH. |
| `ssl_key_file` | [17](../parameters-connections-authentication-ssl.md#ssl_key_file) | Location of the SSL server private key file. |
| `ssl_max_protocol_version` | [17](../parameters-connections-authentication-ssl.md#ssl_max_protocol_version) | Sets the maximum SSL/TLS protocol version to use. |
| `ssl_min_protocol_version` | [17](../parameters-connections-authentication-ssl.md#ssl_min_protocol_version) | Sets the minimum SSL/TLS protocol version to use. |
| `ssl_passphrase_command` | [17](../parameters-connections-authentication-ssl.md#ssl_passphrase_command) | Command to obtain passphrases for SSL. |
| `ssl_passphrase_command_supports_reload` | [17](../parameters-connections-authentication-ssl.md#ssl_passphrase_command_supports_reload) | Controls whether \"ssl_passphrase_command\" is called during server reload. |
| `ssl_prefer_server_ciphers` | [17](../parameters-connections-authentication-ssl.md#ssl_prefer_server_ciphers) | Give priority to server ciphersuite order. |

### Connections and Authentication / TCP Settings

| Name | Versions | Description |
| --- | --- | --- |
| `client_connection_check_interval` | [17](../parameters-connections-authentication-tcp-settings.md#client_connection_check_interval) | Sets the time interval between checks for disconnection while running queries. |
| `tcp_keepalives_count` | [17](../parameters-connections-authentication-tcp-settings.md#tcp_keepalives_count) | Maximum number of TCP keepalive retransmits. Number of consecutive keepalive retransmits that can be lost before a connection is considered dead. A value of 0 uses the system default. |
| `tcp_keepalives_idle` | [17](../parameters-connections-authentication-tcp-settings.md#tcp_keepalives_idle) | Time between issuing TCP keepalives. A value of 0 uses the system default. |
| `tcp_keepalives_interval` | [17](../parameters-connections-authentication-tcp-settings.md#tcp_keepalives_interval) | Time between TCP keepalive retransmits. A value of 0 uses the system default. |
| `tcp_user_timeout` | [17](../parameters-connections-authentication-tcp-settings.md#tcp_user_timeout) | TCP user timeout. A value of 0 uses the system default. |

### Customized Options

| Name | Versions | Description |
| --- | --- | --- |
| `anon.algorithm` | [17](../parameters-customized-options.md#anonalgorithm) | The hash method used for pseudonymizing functions. |
| `anon.k_anonymity_provider` | [17](../parameters-customized-options.md#anonk_anonymity_provider) | The security label provider used for k-anonymity. |
| `anon.masking_policies` | [17](../parameters-customized-options.md#anonmasking_policies) | Define multiple masking policies (NOT IMPLEMENTED YET). |
| `anon.maskschema` | [17](../parameters-customized-options.md#anonmaskschema) | The schema where the dynamic masking views are stored. |
| `anon.privacy_by_default` | [17](../parameters-customized-options.md#anonprivacy_by_default) | Mask all columns with NULL (or the default value for NOT NULL columns). |
| `anon.restrict_to_trusted_schemas` | [17](../parameters-customized-options.md#anonrestrict_to_trusted_schemas) | Masking filters must be in a trusted schema. Activate this option to prevent non-superuser from using their own masking filters. |
| `anon.salt` | [17](../parameters-customized-options.md#anonsalt) | The salt value used for the pseudonymizing functions. |
| `anon.sourceschema` | [17](../parameters-customized-options.md#anonsourceschema) | The schema where the table are masked by the dynamic masking engine. |
| `anon.strict_mode` | [17](../parameters-customized-options.md#anonstrict_mode) | A masking rule can't change a column data type, unless you disable this. Disabling the mode isn't recommended. |
| `anon.transparent_dynamic_masking` | [17](../parameters-customized-options.md#anontransparent_dynamic_masking) | New masking engine (EXPERIMENTAL). |
| `auto_explain.log_analyze` | [17](../parameters-customized-options.md#auto_explainlog_analyze) | Use EXPLAIN ANALYZE for plan logging. |
| `auto_explain.log_buffers` | [17](../parameters-customized-options.md#auto_explainlog_buffers) | Log buffers usage. |
| `auto_explain.log_format` | [17](../parameters-customized-options.md#auto_explainlog_format) | EXPLAIN format to be used for plan logging. |
| `auto_explain.log_level` | [17](../parameters-customized-options.md#auto_explainlog_level) | Log level for the plan. |
| `auto_explain.log_min_duration` | [17](../parameters-customized-options.md#auto_explainlog_min_duration) | Sets the minimum execution time above which plans will be logged. Zero prints all plans. -1 turns this feature off. |
| `auto_explain.log_nested_statements` | [17](../parameters-customized-options.md#auto_explainlog_nested_statements) | Log nested statements. |
| `auto_explain.log_parameter_max_length` | [17](../parameters-customized-options.md#auto_explainlog_parameter_max_length) | Sets the maximum length of query parameters to log. Zero logs no query parameters, -1 logs them in full. |
| `auto_explain.log_settings` | [17](../parameters-customized-options.md#auto_explainlog_settings) | Log modified configuration parameters affecting query planning. |
| `auto_explain.log_timing` | [17](../parameters-customized-options.md#auto_explainlog_timing) | Collect timing data, not just row counts. |
| `auto_explain.log_triggers` | [17](../parameters-customized-options.md#auto_explainlog_triggers) | Include trigger statistics in plans. This has no effect unless log_analyze is also set. |
| `auto_explain.log_verbose` | [17](../parameters-customized-options.md#auto_explainlog_verbose) | Use EXPLAIN VERBOSE for plan logging. |
| `auto_explain.log_wal` | [17](../parameters-customized-options.md#auto_explainlog_wal) | Log WAL usage. |
| `auto_explain.sample_rate` | [17](../parameters-customized-options.md#auto_explainsample_rate) | Fraction of queries to process. |
| `azure.accepted_password_auth_method` | [17](../parameters-customized-options.md#azureaccepted_password_auth_method) | Password authentication methods, separated by comma, that are accepted by the server. |
| `azure_cdc.change_batch_buffer_size` | [17](../parameters-customized-options.md#azure_cdcchange_batch_buffer_size) | Buffer size, in megabytes, for change batches. These buffers are used to temporarily store CDC changes before they are written to disk. |
| `azure_cdc.change_batch_export_timeout` | [17](../parameters-customized-options.md#azure_cdcchange_batch_export_timeout) | Maximum time, in seconds, to wait before a batch of changes is ready to be exported. |
| `azure_cdc.max_fabric_mirrors` | [17](../parameters-customized-options.md#azure_cdcmax_fabric_mirrors) | Maximum number of parallel fabric mirrors that can be run at the same time. |
| `azure_cdc.max_snapshot_workers` | [17](../parameters-customized-options.md#azure_cdcmax_snapshot_workers) | Maximum number of workers launched for snapshot export. Each worker exports one table at a time. |
| `azure_cdc.onelake_buffer_size` | [17](../parameters-customized-options.md#azure_cdconelake_buffer_size) | Buffer size, in megabytes, for upload to Onelake. Onelake uploads files in chunks, buffering the data in memory up to this limit. |
| `azure_cdc.parquet_compression` | [17](../parameters-customized-options.md#azure_cdcparquet_compression) | Compression algorithm to use for parquet files. Determines the compression algorithm to use for parquet files. Supported values are 'uncompressed', 'snappy', 'gzip', and 'zstd'. |
| `azure_cdc.snapshot_buffer_size` | [17](../parameters-customized-options.md#azure_cdcsnapshot_buffer_size) | Buffer size, in megabytes, for snapshot data files. These buffers are used for writing snapshot data. While this indirectly influences the file size, the actual file size might be smaller due to compression and other factors. |
| `azure_cdc.snapshot_export_timeout` | [17](../parameters-customized-options.md#azure_cdcsnapshot_export_timeout) | Maximum time, in minutes, to wait before reporting an error when exporting a snapshot of a database. |
| `azure.enable_temp_tablespaces_on_local_ssd` | [17](../parameters-customized-options.md#azureenable_temp_tablespaces_on_local_ssd) | Stores temporary objects on local Solid State Disk. |
| `azure.extensions` | [17](../parameters-customized-options.md#azureextensions) | List of extensions, separated by comma, that are allowlisted. If an extension isn't in this list, trying to execute CREATE, ALTER, COMMENT, DROP EXTENSION statements on that extension fails. |
| `azure.fabric_mirror_enabled` | [17](../parameters-customized-options.md#azurefabric_mirror_enabled) | Validates prerequisites for Fabric Mirroring to function properly. Validation only occurs at the very moment this setting is changed from 'off' to 'on'. |
| `azure_storage.blob_block_size_mb` | [17](../parameters-customized-options.md#azure_storageblob_block_size_mb) | Size of blob block, in megabytes, for PUT blob operations. |
| `credcheck.auth_delay_ms` | [17](../parameters-customized-options.md#credcheckauth_delay_ms) | Milliseconds to delay before reporting authentication failure. |
| `credcheck.auth_failure_cache_size` | [17](../parameters-customized-options.md#credcheckauth_failure_cache_size) | Maximum of entries in the auth failure cache. |
| `credcheck.encrypted_password_allowed` | [17](../parameters-customized-options.md#credcheckencrypted_password_allowed) | Allow encrypted password to be used or throw an error. |
| `credcheck.history_max_size` | [17](../parameters-customized-options.md#credcheckhistory_max_size) | Maximum of entries in the password history. |
| `credcheck.max_auth_failure` | [17](../parameters-customized-options.md#credcheckmax_auth_failure) | Maximum number of authentication failures before the user login account is invalidated. |
| `credcheck.password_contain` | [17](../parameters-customized-options.md#credcheckpassword_contain) | Password should contain these characters |
| `credcheck.password_contain_username` | [17](../parameters-customized-options.md#credcheckpassword_contain_username) | Password contains username |
| `credcheck.password_ignore_case` | [17](../parameters-customized-options.md#credcheckpassword_ignore_case) | Ignore case while password checking |
| `credcheck.password_min_digit` | [17](../parameters-customized-options.md#credcheckpassword_min_digit) | Minimum password digits |
| `credcheck.password_min_length` | [17](../parameters-customized-options.md#credcheckpassword_min_length) | Minimum password length |
| `credcheck.password_min_lower` | [17](../parameters-customized-options.md#credcheckpassword_min_lower) | Minimum password lowercase letters |
| `credcheck.password_min_repeat` | [17](../parameters-customized-options.md#credcheckpassword_min_repeat) | Minimum password characters repeat |
| `credcheck.password_min_special` | [17](../parameters-customized-options.md#credcheckpassword_min_special) | Minimum special characters |
| `credcheck.password_min_upper` | [17](../parameters-customized-options.md#credcheckpassword_min_upper) | Minimum password uppercase letters |
| `credcheck.password_not_contain` | [17](../parameters-customized-options.md#credcheckpassword_not_contain) | Password shouldn't contain these characters |
| `credcheck.password_reuse_history` | [17](../parameters-customized-options.md#credcheckpassword_reuse_history) | Minimum number of password changes before permitting reuse |
| `credcheck.password_reuse_interval` | [17](../parameters-customized-options.md#credcheckpassword_reuse_interval) | Minimum number of days elapsed before permitting reuse |
| `credcheck.password_valid_max` | [17](../parameters-customized-options.md#credcheckpassword_valid_max) | Force use of VALID UNTIL clause in CREATE ROLE statement with a maximum number of days |
| `credcheck.password_valid_until` | [17](../parameters-customized-options.md#credcheckpassword_valid_until) | Force use of VALID UNTIL clause in CREATE ROLE statement with a minimum number of days |
| `credcheck.reset_superuser` | [17](../parameters-customized-options.md#credcheckreset_superuser) | Restore superuser access when they have been banned. |
| `credcheck.username_contain` | [17](../parameters-customized-options.md#credcheckusername_contain) | Username should contain these characters |
| `credcheck.username_contain_password` | [17](../parameters-customized-options.md#credcheckusername_contain_password) | Username contains password |
| `credcheck.username_ignore_case` | [17](../parameters-customized-options.md#credcheckusername_ignore_case) | Ignore case while username checking |
| `credcheck.username_min_digit` | [17](../parameters-customized-options.md#credcheckusername_min_digit) | Minimum username digits |
| `credcheck.username_min_length` | [17](../parameters-customized-options.md#credcheckusername_min_length) | Minimum username length |
| `credcheck.username_min_lower` | [17](../parameters-customized-options.md#credcheckusername_min_lower) | Minimum username lowercase letters |
| `credcheck.username_min_repeat` | [17](../parameters-customized-options.md#credcheckusername_min_repeat) | Minimum username characters repeat |
| `credcheck.username_min_special` | [17](../parameters-customized-options.md#credcheckusername_min_special) | Minimum username special characters |
| `credcheck.username_min_upper` | [17](../parameters-customized-options.md#credcheckusername_min_upper) | Minimum username uppercase letters |
| `credcheck.username_not_contain` | [17](../parameters-customized-options.md#credcheckusername_not_contain) | Username shouldn't contain these characters |
| `credcheck.whitelist` | [17](../parameters-customized-options.md#credcheckwhitelist) | Comma separated list of usernames to exclude from password policy check. |
| `credcheck.whitelist_auth_failure` | [17](../parameters-customized-options.md#credcheckwhitelist_auth_failure) | Comma separated list of usernames to exclude from max authentication failure check. |
| `cron.database_name` | [17](../parameters-customized-options.md#crondatabase_name) | Database in which pg_cron metadata is kept. |
| `cron.enable_superuser_jobs` | [17](../parameters-customized-options.md#cronenable_superuser_jobs) | Allow jobs to be scheduled as superuser. |
| `cron.host` | [17](../parameters-customized-options.md#cronhost) | Hostname to connect to postgres. This setting has no effect when background workers are used. |
| `cron.launch_active_jobs` | [17](../parameters-customized-options.md#cronlaunch_active_jobs) | Launch jobs that are defined as active. |
| `cron.log_min_messages` | [17](../parameters-customized-options.md#cronlog_min_messages) | log_min_messages for the launcher bgworker. |
| `cron.log_run` | [17](../parameters-customized-options.md#cronlog_run) | Log all jobs runs into the job_run_details table. |
| `cron.log_statement` | [17](../parameters-customized-options.md#cronlog_statement) | Log all cron statements prior to execution. |
| `cron.max_running_jobs` | [17](../parameters-customized-options.md#cronmax_running_jobs) | Maximum number of jobs that can run concurrently. |
| `cron.timezone` | [17](../parameters-customized-options.md#crontimezone) | Specify timezone used for cron schedule. |
| `cron.use_background_workers` | [17](../parameters-customized-options.md#cronuse_background_workers) | Use background workers instead of client sessions. |
| `pgaadauth.enable_group_sync` | [17](../parameters-customized-options.md#pgaadauthenable_group_sync) | Enables synchronization of Microsoft Entra ID group members. |
| `pgaudit.log` | [17](../parameters-customized-options.md#pgauditlog) | Specifies which classes of statements will be logged by session audit logging. Multiple classes can be provided using a comma-separated list and classes can be subtracted by prefacing the class with a - sign. |
| `pgaudit.log_catalog` | [17](../parameters-customized-options.md#pgauditlog_catalog) | Specifies that session logging should be enabled in the case where all relations in a statement are in pg_catalog. Disabling this setting will reduce noise in the log from tools like psql and PgAdmin that query the catalog heavily. |
| `pgaudit.log_client` | [17](../parameters-customized-options.md#pgauditlog_client) | Specifies whether audit messages should be visible to the client. This setting should generally be left disabled but might be useful for debugging or other purposes. |
| `pgaudit.log_level` | [17](../parameters-customized-options.md#pgauditlog_level) | Specifies the log level that will be used for log entries. This setting is used for regression testing and might also be useful to end users for testing or other purposes. It's not intended to be used in a production environment as it might leak which statements are being logged to the user. |
| `pgaudit.log_parameter` | [17](../parameters-customized-options.md#pgauditlog_parameter) | Specifies that audit logging should include the parameters that were passed with the statement. When parameters are present they will be be included in CSV format after the statement text. |
| `pgaudit.log_parameter_max_size` | [17](../parameters-customized-options.md#pgauditlog_parameter_max_size) | Specifies, in bytes, the maximum length of variable-length parameters to log. If 0 (the default), parameters aren't checked for size. If set, when the size of the parameter is longer than the setting, the value in the audit log is replaced with a placeholder. For character types, the length is in bytes for the parameter's encoding, not characters. |
| `pgaudit.log_relation` | [17](../parameters-customized-options.md#pgauditlog_relation) | Specifies whether session audit logging should create a separate log entry for each relation referenced in a SELECT or DML statement. This is a useful shortcut for exhaustive logging without using object audit logging. |
| `pgaudit.log_rows` | [17](../parameters-customized-options.md#pgauditlog_rows) | Specifies whether logging will include the rows retrieved or affected by a statement. |
| `pgaudit.log_statement` | [17](../parameters-customized-options.md#pgauditlog_statement) | Specifies whether logging will include the statement text and parameters. Depending on requirements, the full statement text might not be required in the audit log. |
| `pgaudit.log_statement_once` | [17](../parameters-customized-options.md#pgauditlog_statement_once) | Specifies whether logging will include the statement text and parameters with the first log entry for a statement/substatement combination or with every entry. Disabling this setting will result in less verbose logging but might make it more difficult to determine the statement that generated a log entry, though the statement/substatement pair along with the process id should suffice to identify the statement text logged with a previous entry. |
| `pgaudit.role` | [17](../parameters-customized-options.md#pgauditrole) | Specifies the `master` role to use for object audit logging. Multiple audit roles can be defined by granting them to the `master` role. This allows multiple groups to be in charge of different aspects of audit logging. |
| `pg_hint_plan.debug_print` | [17](../parameters-customized-options.md#pg_hint_plandebug_print) | Logs results of hint parsing. |
| `pg_hint_plan.enable_hint` | [17](../parameters-customized-options.md#pg_hint_planenable_hint) | Force planner to use plans specified in the hint comment preceding to the query. |
| `pg_hint_plan.enable_hint_table` | [17](../parameters-customized-options.md#pg_hint_planenable_hint_table) | Let pg_hint_plan look up the hint table. |
| `pg_hint_plan.message_level` | [17](../parameters-customized-options.md#pg_hint_planmessage_level) | Message level of debug messages. |
| `pg_hint_plan.parse_messages` | [17](../parameters-customized-options.md#pg_hint_planparse_messages) | Message level of parse errors. |
| `pglogical.batch_inserts` | [17](../parameters-customized-options.md#pglogicalbatch_inserts) | Tells PGLogical to use batch insert mechanism if possible. |
| `pglogical.conflict_log_level` | [17](../parameters-customized-options.md#pglogicalconflict_log_level) | Sets the log level for reporting detected conflicts when the pglogical.conflict_resolution is set to anything else than error. |
| `pglogical.conflict_resolution` | [17](../parameters-customized-options.md#pglogicalconflict_resolution) | Sets the resolution method for any detected conflicts between local data and incoming changes. |
| `pglogical.extra_connection_options` | [17](../parameters-customized-options.md#pglogicalextra_connection_options) | connection options to add to all peer node connections. |
| `pglogical.synchronous_commit` | [17](../parameters-customized-options.md#pglogicalsynchronous_commit) | pglogical specific synchronous commit value. |
| `pglogical.temp_directory` | [17](../parameters-customized-options.md#pglogicaltemp_directory) | Directory to store dumps for local restore. |
| `pglogical.use_spi` | [17](../parameters-customized-options.md#pglogicaluse_spi) | Tells PGLogical to use SPI interface to form actual SQL (INSERT, UPDATE, DELETE) statements to apply incoming changes instead of using internal low level interface. |
| `pgms_stats.is_enabled_fs` | [17](../parameters-customized-options.md#pgms_statsis_enabled_fs) | Internal Use Only: This parameter is used as a feature override switch. |
| `pgms_wait_sampling.history_period` | [17](../parameters-customized-options.md#pgms_wait_samplinghistory_period) | Sets the the frequency, in milliseconds, at which wait events are sampled. |
| `pgms_wait_sampling.is_enabled_fs` | [17](../parameters-customized-options.md#pgms_wait_samplingis_enabled_fs) | Internal Use Only: This parameter is used as a feature override switch. If it shows as off, wait sampling will be disabled despite the value set for pgms_wait_sampling.query_capture_mode. |
| `pgms_wait_sampling.query_capture_mode` | [17](../parameters-customized-options.md#pgms_wait_samplingquery_capture_mode) | Selects types of wait events are tracked by this extension. Need to reload the config to make change take effect. |
| `pg_partman_bgw.analyze` | [17](../parameters-customized-options.md#pg_partman_bgwanalyze) | Whether to run an analyze on a partition set whenever a new partition is created during run_maintenance(). Set to 'on' to send TRUE (default). Set to 'off' to send FALSE. |
| `pg_partman_bgw.dbname` | [17](../parameters-customized-options.md#pg_partman_bgwdbname) | CSV list of specific databases in the cluster to run pg_partman BGW on. |
| `pg_partman_bgw.interval` | [17](../parameters-customized-options.md#pg_partman_bgwinterval) | How often run_maintenance() is called (in seconds). |
| `pg_partman_bgw.jobmon` | [17](../parameters-customized-options.md#pg_partman_bgwjobmon) | Whether to log run_maintenance() calls to pg_jobmon if it's installed. Set to 'on' to send TRUE (default). Set to 'off' to send FALSE. |
| `pg_partman_bgw.maintenance_wait` | [17](../parameters-customized-options.md#pg_partman_bgwmaintenance_wait) | How long to wait between each partition set when running maintenance (in seconds). |
| `pg_partman_bgw.role` | [17](../parameters-customized-options.md#pg_partman_bgwrole) | Role to be used by BGW. Must have execute permissions on run_maintenance(). |
| `pg_prewarm.autoprewarm` | [17](../parameters-customized-options.md#pg_prewarmautoprewarm) | Starts the autoprewarm worker. |
| `pg_prewarm.autoprewarm_interval` | [17](../parameters-customized-options.md#pg_prewarmautoprewarm_interval) | Sets the interval between dumps of shared buffers. If set to zero, time-based dumping is disabled. |
| `pg_qs.interval_length_minutes` | [17](../parameters-customized-options.md#pg_qsinterval_length_minutes) | Sets the aggregration window in minutes. Need to reload the config to make change take effect. |
| `pg_qs.max_captured_queries` | [17](../parameters-customized-options.md#pg_qsmax_captured_queries) | Specifies the number of most relevant queries for which query store captures runtime statistics at each interval. |
| `pg_qs.max_plan_size` | [17](../parameters-customized-options.md#pg_qsmax_plan_size) | Sets the maximum number of bytes that will be saved for query plan text; longer plans will be truncated. Need to reload the config for this change to take effect. |
| `pg_qs.max_query_text_length` | [17](../parameters-customized-options.md#pg_qsmax_query_text_length) | Sets the maximum query text length that will be saved; longer queries will be truncated. Need to reload the config to make change take effect. |
| `pg_qs.parameters_capture_mode` | [17](../parameters-customized-options.md#pg_qsparameters_capture_mode) | Selects how positional query parameters are captured by pg_qs. Need to reload the config for the change to take effect. |
| `pg_qs.query_capture_mode` | [17](../parameters-customized-options.md#pg_qsquery_capture_mode) | Selects which statements are tracked by pg_qs. Need to reload the config to make change take effect. |
| `pg_qs.retention_period_in_days` | [17](../parameters-customized-options.md#pg_qsretention_period_in_days) | Sets the retention period window in days for pg_qs - after this time data will be deleted. Need to restart the server to make change take effect. |
| `pg_qs.store_query_plans` | [17](../parameters-customized-options.md#pg_qsstore_query_plans) | Turns saving query plans on or off. Need to reload the config for the change to take effect. |
| `pg_qs.track_utility` | [17](../parameters-customized-options.md#pg_qstrack_utility) | Selects whether utility commands are tracked by pg_qs. Need to reload the config to make change take effect. |
| `pg_stat_statements.max` | [17](../parameters-customized-options.md#pg_stat_statementsmax) | Sets the maximum number of statements tracked by pg_stat_statements. |
| `pg_stat_statements.save` | [17](../parameters-customized-options.md#pg_stat_statementssave) | Save pg_stat_statements statistics across server shutdowns. |
| `pg_stat_statements.track` | [17](../parameters-customized-options.md#pg_stat_statementstrack) | Selects which statements are tracked by pg_stat_statements. |
| `pg_stat_statements.track_planning` | [17](../parameters-customized-options.md#pg_stat_statementstrack_planning) | Selects whether planning duration is tracked by pg_stat_statements. |
| `pg_stat_statements.track_utility` | [17](../parameters-customized-options.md#pg_stat_statementstrack_utility) | Selects whether utility commands are tracked by pg_stat_statements. |
| `postgis.gdal_enabled_drivers` | [17](../parameters-customized-options.md#postgisgdal_enabled_drivers) | Controls postgis GDAL enabled driver settings. |
| `squeeze.max_xlock_time` | [17](../parameters-customized-options.md#squeezemax_xlock_time) | The maximum time the processed table might be locked exclusively. The source table is locked exclusively during the final stage of processing. If the lock time should exceed this value, the lock is released and the final stage is retried a few more times. |
| `squeeze.worker_autostart` | [17](../parameters-customized-options.md#squeezeworker_autostart) | Names of databases for which background workers start automatically. Comma-separated list for of databases which squeeze worker starts as soon as the cluster startup has completed. |
| `squeeze.worker_role` | [17](../parameters-customized-options.md#squeezeworker_role) | Role that background workers use to connect to database. If background worker was launched automatically on cluster startup, it uses this role to initiate database connection(s). |
| `squeeze.workers_per_database` | [17](../parameters-customized-options.md#squeezeworkers_per_database) | Maximum number of squeeze worker processes launched for each database. |
| `timescaledb.bgw_launcher_poll_time` | [17](../parameters-customized-options.md#timescaledbbgw_launcher_poll_time) | Launcher timeout value in milliseconds. Configure the time the launcher waits to look for new TimescaleDB instances. |
| `timescaledb.disable_load` | [17](../parameters-customized-options.md#timescaledbdisable_load) | Disable the loading of the actual extension. |
| `timescaledb.max_background_workers` | [17](../parameters-customized-options.md#timescaledbmax_background_workers) | Maximum background worker processes allocated to TimescaleDB. Max background worker processes allocated to TimescaleDB - set to at least 1 + number of databases in Postgres instance to use background workers. |
| `timescaledb_osm.disable_load` | [17](../parameters-customized-options.md#timescaledb_osmdisable_load) | Disable the loading of the actual extension. |

### Developer Options

| Name | Versions | Description |
| --- | --- | --- |
| `allow_in_place_tablespaces` | [17](../parameters-developer-options.md#allow_in_place_tablespaces) | Allows tablespaces directly inside pg_tblspc, for testing. |
| `allow_system_table_mods` | [17](../parameters-developer-options.md#allow_system_table_mods) | Allows modifications of the structure of system tables. |
| `backtrace_functions` | [17](../parameters-developer-options.md#backtrace_functions) | Log backtrace for errors in these functions. |
| `debug_discard_caches` | [17](../parameters-developer-options.md#debug_discard_caches) | Aggressively flush system caches for debugging purposes. |
| `debug_io_direct` | [17](../parameters-developer-options.md#debug_io_direct) | Use direct I/O for file access. |
| `debug_logical_replication_streaming` | [17](../parameters-developer-options.md#debug_logical_replication_streaming) | Forces immediate streaming or serialization of changes in large transactions. On the publisher, it allows streaming or serializing each change in logical decoding. On the subscriber, it allows serialization of all changes to files and notifies the parallel apply workers to read and apply them at the end of the transaction. |
| `debug_parallel_query` | [17](../parameters-developer-options.md#debug_parallel_query) | Forces the planner's use parallel query nodes. This can be useful for testing the parallel query infrastructure by forcing the planner to generate plans that contain nodes that perform tuple communication between workers and the main process. |
| `ignore_checksum_failure` | [17](../parameters-developer-options.md#ignore_checksum_failure) | Continues processing after a checksum failure. Detection of a checksum failure normally causes PostgreSQL to report an error, aborting the current transaction. Setting ignore_checksum_failure to true causes the system to ignore the failure (but still report a warning), and continue processing. This behavior could cause crashes or other serious problems. Only has an effect if checksums are enabled. |
| `ignore_invalid_pages` | [17](../parameters-developer-options.md#ignore_invalid_pages) | Continues recovery after an invalid pages failure. Detection of WAL records having references to invalid pages during recovery causes PostgreSQL to raise a PANIC-level error, aborting the recovery. Setting \"ignore_invalid_pages\" to true causes the system to ignore invalid page references in WAL records (but still report a warning), and continue recovery. This behavior might cause crashes, data loss, propagate or hide corruption, or other serious problems. Only has an effect during recovery or in standby mode. |
| `ignore_system_indexes` | [17](../parameters-developer-options.md#ignore_system_indexes) | Disables reading from system indexes. It doesn't prevent updating the indexes, so it's safe to use. The worst consequence is slowness. |
| `jit_debugging_support` | [17](../parameters-developer-options.md#jit_debugging_support) | Register JIT-compiled functions with debugger. |
| `jit_dump_bitcode` | [17](../parameters-developer-options.md#jit_dump_bitcode) | Write out LLVM bitcode to facilitate JIT debugging. |
| `jit_expressions` | [17](../parameters-developer-options.md#jit_expressions) | Allow JIT compilation of expressions. |
| `jit_profiling_support` | [17](../parameters-developer-options.md#jit_profiling_support) | Register JIT-compiled functions with perf profiler. |
| `jit_tuple_deforming` | [17](../parameters-developer-options.md#jit_tuple_deforming) | Allow JIT compilation of tuple deforming. |
| `post_auth_delay` | [17](../parameters-developer-options.md#post_auth_delay) | Sets the amount of time to wait after authentication on connection startup. This allows attaching a debugger to the process. |
| `pre_auth_delay` | [17](../parameters-developer-options.md#pre_auth_delay) | Sets the amount of time to wait before authentication on connection startup. This allows attaching a debugger to the process. |
| `remove_temp_files_after_crash` | [17](../parameters-developer-options.md#remove_temp_files_after_crash) | Remove temporary files after backend crash. |
| `send_abort_for_crash` | [17](../parameters-developer-options.md#send_abort_for_crash) | Send SIGABRT not SIGQUIT to child processes after backend crash. |
| `send_abort_for_kill` | [17](../parameters-developer-options.md#send_abort_for_kill) | Send SIGABRT not SIGKILL to stuck child processes. |
| `trace_connection_negotiation` | [17](../parameters-developer-options.md#trace_connection_negotiation) | Logs details of pre-authentication connection handshake. |
| `trace_notify` | [17](../parameters-developer-options.md#trace_notify) | Generates debugging output for LISTEN and NOTIFY. |
| `trace_sort` | [17](../parameters-developer-options.md#trace_sort) | Emit information about resource usage in sorting. |
| `wal_consistency_checking` | [17](../parameters-developer-options.md#wal_consistency_checking) | Sets the WAL resource managers for which WAL consistency checks are done. Full-page images will be logged for all data blocks and cross-checked against the results of WAL replay. |
| `zero_damaged_pages` | [17](../parameters-developer-options.md#zero_damaged_pages) | Continues processing past damaged page headers. Detection of a damaged page header normally causes PostgreSQL to report an error, aborting the current transaction. Setting \"zero_damaged_pages\" to true causes the system to instead report a warning, zero out the damaged page, and continue processing. This behavior will destroy data, namely all the rows on the damaged page. |

### Error Handling

| Name | Versions | Description |
| --- | --- | --- |
| `data_sync_retry` | [17](../parameters-error-handling.md#data_sync_retry) | Whether to continue running after a failure to sync data files. |
| `exit_on_error` | [17](../parameters-error-handling.md#exit_on_error) | Terminate session on any error. |
| `recovery_init_sync_method` | [17](../parameters-error-handling.md#recovery_init_sync_method) | Sets the method for synchronizing the data directory before crash recovery. |
| `restart_after_crash` | [17](../parameters-error-handling.md#restart_after_crash) | Reinitialize server after backend crash. |

### File Locations

| Name | Versions | Description |
| --- | --- | --- |
| `config_file` | [17](../parameters-file-locations.md#config_file) | Sets the server's main configuration file. |
| `data_directory` | [17](../parameters-file-locations.md#data_directory) | Sets the server's data directory. |
| `external_pid_file` | [17](../parameters-file-locations.md#external_pid_file) | Writes the postmaster PID to the specified file. |
| `hba_file` | [17](../parameters-file-locations.md#hba_file) | Sets the server's \"hba\" configuration file. |
| `ident_file` | [17](../parameters-file-locations.md#ident_file) | Sets the server's \"ident\" configuration file. |

### Intelligent Tuning

| Name | Versions | Description |
| --- | --- | --- |
| `index_tuning.analysis_interval` | [17](../parameters-intelligent-tuning.md#index_tuninganalysis_interval) | Sets the frequency at which each index optimization session is triggered when index_tuning.mode is set to 'REPORT'. |
| `index_tuning.max_columns_per_index` | [17](../parameters-intelligent-tuning.md#index_tuningmax_columns_per_index) | Maximum number of columns that can be part of the index key for any recommended index. |
| `index_tuning.max_index_count` | [17](../parameters-intelligent-tuning.md#index_tuningmax_index_count) | Maximum number of indexes that can be recommended for each database during one optimization session. |
| `index_tuning.max_indexes_per_table` | [17](../parameters-intelligent-tuning.md#index_tuningmax_indexes_per_table) | Maximum number of indexes that can be recommended for each table. |
| `index_tuning.max_queries_per_database` | [17](../parameters-intelligent-tuning.md#index_tuningmax_queries_per_database) | Number of slowest queries per database for which indexes can be recommended. |
| `index_tuning.max_regression_factor` | [17](../parameters-intelligent-tuning.md#index_tuningmax_regression_factor) | Acceptable regression introduced by a recommended index on any of the queries analyzed during one optimization session. |
| `index_tuning.max_total_size_factor` | [17](../parameters-intelligent-tuning.md#index_tuningmax_total_size_factor) | Maximum total size, in percentage of total disk space, that all recommended indexes for any given database can use. |
| `index_tuning.min_improvement_factor` | [17](../parameters-intelligent-tuning.md#index_tuningmin_improvement_factor) | Cost improvement that a recommended index must provide to at least one of the queries analyzed during one optimization session. |
| `index_tuning.mode` | [17](../parameters-intelligent-tuning.md#index_tuningmode) | Configures index optimization as disabled ('OFF') or enabled to only emit recommendation. Requires Query Store to be enabled by setting pg_qs.query_capture_mode to 'TOP' or 'ALL'. |
| `index_tuning.unused_dml_per_table` | [17](../parameters-intelligent-tuning.md#index_tuningunused_dml_per_table) | Minimum number of daily average DML operations affecting the table, so that their unused indexes are considered for dropping. |
| `index_tuning.unused_min_period` | [17](../parameters-intelligent-tuning.md#index_tuningunused_min_period) | Minimum number of days the index hasn't been used, based on system statistics, so that it's considered for dropping. |
| `index_tuning.unused_reads_per_table` | [17](../parameters-intelligent-tuning.md#index_tuningunused_reads_per_table) | Minimum number of daily average read operations affecting the table, so that their unused indexes are considered for dropping. |
| `intelligent_tuning` | [17](../parameters-intelligent-tuning.md#intelligent_tuning) | Enables intelligent tuning |
| `intelligent_tuning.metric_targets` | [17](../parameters-intelligent-tuning.md#intelligent_tuningmetric_targets) | Specifies which metrics will be adjusted by intelligent tuning. |
| `logfiles.download_enable` | [17](../parameters-intelligent-tuning.md#logfilesdownload_enable) | Enables or disables server logs functionality. |
| `logfiles.retention_days` | [17](../parameters-intelligent-tuning.md#logfilesretention_days) | Sets the retention period window in days for server logs - after this time data will be deleted. |

### Lock Management

| Name | Versions | Description |
| --- | --- | --- |
| `deadlock_timeout` | [17](../parameters-lock-management.md#deadlock_timeout) | Sets the time to wait on a lock before checking for deadlock. |
| `max_locks_per_transaction` | [17](../parameters-lock-management.md#max_locks_per_transaction) | Sets the maximum number of locks per transaction. The shared lock table is sized on the assumption that at most \"max_locks_per_transaction\" objects per server process or prepared transaction will need to be locked at any one time. |
| `max_pred_locks_per_page` | [17](../parameters-lock-management.md#max_pred_locks_per_page) | Sets the maximum number of predicate-locked tuples per page. If more than this number of tuples on the same page are locked by a connection, those locks are replaced by a page-level lock. |
| `max_pred_locks_per_relation` | [17](../parameters-lock-management.md#max_pred_locks_per_relation) | Sets the maximum number of predicate-locked pages and tuples per relation. If more than this total of pages and tuples in the same relation are locked by a connection, those locks are replaced by a relation-level lock. |
| `max_pred_locks_per_transaction` | [17](../parameters-lock-management.md#max_pred_locks_per_transaction) | Sets the maximum number of predicate locks per transaction. The shared predicate lock table is sized on the assumption that at most \"max_pred_locks_per_transaction\" objects per server process or prepared transaction will need to be locked at any one time. |

### Metrics

| Name | Versions | Description |
| --- | --- | --- |
| `metrics.autovacuum_diagnostics` | [17](../parameters-metrics.md#metricsautovacuum_diagnostics) | Enables metrics collection for all table statistics within a database |
| `metrics.collector_database_activity` | [17](../parameters-metrics.md#metricscollector_database_activity) | Enables metrics collection for database and activity statistics |
| `metrics.pgbouncer_diagnostics` | [17](../parameters-metrics.md#metricspgbouncer_diagnostics) | Enables metrics collection for PgBouncer. |

### Migration

| Name | Versions | Description |
| --- | --- | --- |
| `azure.migration_copy_with_binary` | [17](../parameters-migration.md#azuremigration_copy_with_binary) | When set to on, this parameter will enable the use of the binary format for copying data during migration. |
| `azure.migration_skip_analyze` | [17](../parameters-migration.md#azuremigration_skip_analyze) | When set to on, this parameter will skip the analyze phase (`vacuumdb --analyze-only`) during the migration. |
| `azure.migration_skip_extensions` | [17](../parameters-migration.md#azuremigration_skip_extensions) | When set to on, this parameter will skip the migration of extensions. |
| `azure.migration_skip_large_objects` | [17](../parameters-migration.md#azuremigration_skip_large_objects) | When set to on, this parameter will skip the migration of large objects such as BLOBs. |
| `azure.migration_skip_role_user` | [17](../parameters-migration.md#azuremigration_skip_role_user) | When set to on, this parameter will exclude user roles from the migration process. |
| `azure.migration_table_split_size` | [17](../parameters-migration.md#azuremigration_table_split_size) | When set, this parameter specifies the size at which tables will be partitioned during migration. |

### PgBouncer

| Name | Versions | Description |
| --- | --- | --- |
| `pgbouncer.default_pool_size` | [17](../parameters-pgbouncer.md#pgbouncerdefault_pool_size) | How many server connections to allow per user/database pair. |
| `pgbouncer.enabled` | [17](../parameters-pgbouncer.md#pgbouncerenabled) | Denotes if pgBouncer service is enabled. |
| `pgbouncer.ignore_startup_parameters` | [17](../parameters-pgbouncer.md#pgbouncerignore_startup_parameters) | Comma-separated list of parameters that PgBouncer can ignore because they are going to be handled by the admin. |
| `pgbouncer.max_client_conn` | [17](../parameters-pgbouncer.md#pgbouncermax_client_conn) | Maximum number of client connections allowed. |
| `pgbouncer.max_prepared_statements` | [17](../parameters-pgbouncer.md#pgbouncermax_prepared_statements) | When this is set to a non-zero value PgBouncer tracks protocol-level named prepared statements related commands sent by the client in transaction and statement pooling mode. |
| `pgbouncer.min_pool_size` | [17](../parameters-pgbouncer.md#pgbouncermin_pool_size) | Add more server connections to pool if below this number. |
| `pgbouncer.pool_mode` | [17](../parameters-pgbouncer.md#pgbouncerpool_mode) | Specifies when a server connection can be reused by other clients. |
| `pgbouncer.query_wait_timeout` | [17](../parameters-pgbouncer.md#pgbouncerquery_wait_timeout) | Maximum time (in seconds) queries are allowed to spend waiting for execution. If the query isn't assigned to a server during that time, the client is disconnected. |
| `pgbouncer.server_idle_timeout` | [17](../parameters-pgbouncer.md#pgbouncerserver_idle_timeout) | If a server connection has been idle more than this many seconds it will be dropped. If 0 then timeout is disabled. |
| `pgbouncer.stats_users` | [17](../parameters-pgbouncer.md#pgbouncerstats_users) | Comma-separated list of database users that are allowed to connect and run read-only queries on the pgBouncer console. |

### Preset Options

| Name | Versions | Description |
| --- | --- | --- |
| `block_size` | [17](../parameters-preset-options.md#block_size) | Shows the size of a disk block. |
| `data_checksums` | [17](../parameters-preset-options.md#data_checksums) | Shows whether data checksums are turned on for this cluster. |
| `data_directory_mode` | [17](../parameters-preset-options.md#data_directory_mode) | Shows the mode of the data directory. The parameter value is a numeric mode specification in the form accepted by the chmod and umask system calls. (To use the customary octal format the number must start with a 0 (zero).). |
| `debug_assertions` | [17](../parameters-preset-options.md#debug_assertions) | Shows whether the running server has assertion checks enabled. |
| `huge_pages_status` | [17](../parameters-preset-options.md#huge_pages_status) | Indicates the status of huge pages. |
| `in_hot_standby` | [17](../parameters-preset-options.md#in_hot_standby) | Shows whether hot standby is currently active. |
| `integer_datetimes` | [17](../parameters-preset-options.md#integer_datetimes) | Shows whether datetimes are integer based. |
| `max_function_args` | [17](../parameters-preset-options.md#max_function_args) | Shows the maximum number of function arguments. |
| `max_identifier_length` | [17](../parameters-preset-options.md#max_identifier_length) | Shows the maximum identifier length. |
| `max_index_keys` | [17](../parameters-preset-options.md#max_index_keys) | Shows the maximum number of index keys. |
| `segment_size` | [17](../parameters-preset-options.md#segment_size) | Shows the number of pages per disk file. |
| `server_encoding` | [17](../parameters-preset-options.md#server_encoding) | Shows the server (database) character set encoding. |
| `server_version` | [17](../parameters-preset-options.md#server_version) | Shows the server version. |
| `server_version_num` | [17](../parameters-preset-options.md#server_version_num) | Shows the server version as an integer. |
| `shared_memory_size` | [17](../parameters-preset-options.md#shared_memory_size) | Shows the size of the server's main shared memory area (rounded up to the nearest MB). |
| `shared_memory_size_in_huge_pages` | [17](../parameters-preset-options.md#shared_memory_size_in_huge_pages) | Shows the number of huge pages needed for the main shared memory area. -1 indicates that the value couldn't be determined. |
| `ssl_library` | [17](../parameters-preset-options.md#ssl_library) | Shows the name of the SSL library. |
| `wal_block_size` | [17](../parameters-preset-options.md#wal_block_size) | Shows the block size in the write ahead log. |
| `wal_segment_size` | [17](../parameters-preset-options.md#wal_segment_size) | Shows the size of write ahead log segments. |

### Process Title

| Name | Versions | Description |
| --- | --- | --- |
| `cluster_name` | [17](../parameters-process-title.md#cluster_name) | Sets the name of the cluster, which is included in the process title. |
| `update_process_title` | [17](../parameters-process-title.md#update_process_title) | Updates the process title to show the active SQL command. Enables updating of the process title every time a new SQL command is received by the server. |

### Query Tuning / Genetic Query Optimizer

| Name | Versions | Description |
| --- | --- | --- |
| `geqo` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo) | Enables genetic query optimization. This algorithm attempts to do planning without exhaustive searching. |
| `geqo_effort` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo_effort) | GEQO: effort is used to set the default for other GEQO parameters. |
| `geqo_generations` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo_generations) | GEQO: number of iterations of the algorithm. Zero selects a suitable default value. |
| `geqo_pool_size` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo_pool_size) | GEQO: number of individuals in the population. Zero selects a suitable default value. |
| `geqo_seed` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo_seed) | GEQO: seed for random path selection. |
| `geqo_selection_bias` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo_selection_bias) | GEQO: selective pressure within the population. |
| `geqo_threshold` | [17](../parameters-query-tuning-genetic-query-optimizer.md#geqo_threshold) | Sets the threshold of FROM items beyond which GEQO is used. |

### Query Tuning / Other Planner Options

| Name | Versions | Description |
| --- | --- | --- |
| `constraint_exclusion` | [17](../parameters-query-tuning-planner-options.md#constraint_exclusion) | Enables the planner to use constraints to optimize queries. Table scans will be skipped if their constraints guarantee that no rows match the query. |
| `cursor_tuple_fraction` | [17](../parameters-query-tuning-planner-options.md#cursor_tuple_fraction) | Sets the planner's estimate of the fraction of a cursor's rows that will be retrieved. |
| `default_statistics_target` | [17](../parameters-query-tuning-planner-options.md#default_statistics_target) | Sets the default statistics target. This applies to table columns that haven't had a column-specific target set via ALTER TABLE SET STATISTICS. |
| `from_collapse_limit` | [17](../parameters-query-tuning-planner-options.md#from_collapse_limit) | Sets the FROM-list size beyond which subqueries aren't collapsed. The planner will merge subqueries into upper queries if the resulting FROM list would have no more than this many items. |
| `jit` | [17](../parameters-query-tuning-planner-options.md#jit) | Allow JIT compilation. |
| `join_collapse_limit` | [17](../parameters-query-tuning-planner-options.md#join_collapse_limit) | Sets the FROM-list size beyond which JOIN constructs aren't flattened. The planner will flatten explicit JOIN constructs into lists of FROM items whenever a list of no more than this many items would result. |
| `plan_cache_mode` | [17](../parameters-query-tuning-planner-options.md#plan_cache_mode) | Controls the planner's selection of custom or generic plan. Prepared statements can have custom and generic plans, and the planner will attempt to choose which is better. This can be set to override the default behavior. |
| `recursive_worktable_factor` | [17](../parameters-query-tuning-planner-options.md#recursive_worktable_factor) | Sets the planner's estimate of the average size of a recursive query's working table. |

### Query Tuning / Planner Cost Constants

| Name | Versions | Description |
| --- | --- | --- |
| `cpu_index_tuple_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#cpu_index_tuple_cost) | Sets the planner's estimate of the cost of processing each index entry during an index scan. |
| `cpu_operator_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#cpu_operator_cost) | Sets the planner's estimate of the cost of processing each operator or function call. |
| `cpu_tuple_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#cpu_tuple_cost) | Sets the planner's estimate of the cost of processing each tuple (row). |
| `effective_cache_size` | [17](../parameters-query-tuning-planner-cost-constants.md#effective_cache_size) | Sets the planner's assumption about the total size of the data caches. That is, the total size of the caches (kernel cache and shared buffers) used for PostgreSQL data files. This is measured in disk pages, which are normally 8 kB each. |
| `jit_above_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#jit_above_cost) | Perform JIT compilation if query is more expensive. -1 disables JIT compilation. |
| `jit_inline_above_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#jit_inline_above_cost) | Perform JIT inlining if query is more expensive. -1 disables inlining. |
| `jit_optimize_above_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#jit_optimize_above_cost) | Optimize JIT-compiled functions if query is more expensive. -1 disables optimization. |
| `min_parallel_index_scan_size` | [17](../parameters-query-tuning-planner-cost-constants.md#min_parallel_index_scan_size) | Sets the minimum amount of index data for a parallel scan. If the planner estimates that it will read a number of index pages too small to reach this limit, a parallel scan will not be considered. |
| `min_parallel_table_scan_size` | [17](../parameters-query-tuning-planner-cost-constants.md#min_parallel_table_scan_size) | Sets the minimum amount of table data for a parallel scan. If the planner estimates that it will read a number of table pages too small to reach this limit, a parallel scan will not be considered. |
| `parallel_setup_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#parallel_setup_cost) | Sets the planner's estimate of the cost of starting up worker processes for parallel query. |
| `parallel_tuple_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#parallel_tuple_cost) | Sets the planner's estimate of the cost of passing each tuple (row) from worker to leader backend. |
| `random_page_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#random_page_cost) | Sets the planner's estimate of the cost of a nonsequentially fetched disk page. |
| `seq_page_cost` | [17](../parameters-query-tuning-planner-cost-constants.md#seq_page_cost) | Sets the planner's estimate of the cost of a sequentially fetched disk page. |

### Query Tuning / Planner Method Configuration

| Name | Versions | Description |
| --- | --- | --- |
| `enable_async_append` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_async_append) | Enables the planner's use of async append plans. |
| `enable_bitmapscan` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_bitmapscan) | Enables the planner's use of bitmap-scan plans. |
| `enable_gathermerge` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_gathermerge) | Enables the planner's use of gather merge plans. |
| `enable_group_by_reordering` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_group_by_reordering) | Enables reordering of GROUP BY keys. |
| `enable_hashagg` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_hashagg) | Enables the planner's use of hashed aggregation plans. |
| `enable_hashjoin` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_hashjoin) | Enables the planner's use of hash join plans. |
| `enable_incremental_sort` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_incremental_sort) | Enables the planner's use of incremental sort steps. |
| `enable_indexonlyscan` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_indexonlyscan) | Enables the planner's use of index-only-scan plans. |
| `enable_indexscan` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_indexscan) | Enables the planner's use of index-scan plans. |
| `enable_material` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_material) | Enables the planner's use of materialization. |
| `enable_memoize` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_memoize) | Enables the planner's use of memoization. |
| `enable_mergejoin` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_mergejoin) | Enables the planner's use of merge join plans. |
| `enable_nestloop` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_nestloop) | Enables the planner's use of nested-loop join plans. |
| `enable_parallel_append` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_parallel_append) | Enables the planner's use of parallel append plans. |
| `enable_parallel_hash` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_parallel_hash) | Enables the planner's use of parallel hash plans. |
| `enable_partition_pruning` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_partition_pruning) | Enables plan-time and execution-time partition pruning. Allows the query planner and executor to compare partition bounds to conditions in the query to determine which partitions must be scanned. |
| `enable_partitionwise_aggregate` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_partitionwise_aggregate) | Enables partitionwise aggregation and grouping. |
| `enable_partitionwise_join` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_partitionwise_join) | Enables partitionwise join. |
| `enable_presorted_aggregate` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_presorted_aggregate) | Enables the planner's ability to produce plans that provide presorted input for ORDER BY / DISTINCT aggregate functions. Allows the query planner to build plans that provide presorted input for aggregate functions with an ORDER BY / DISTINCT clause. When disabled, implicit sorts are always performed during execution. |
| `enable_seqscan` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_seqscan) | Enables the planner's use of sequential-scan plans. |
| `enable_sort` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_sort) | Enables the planner's use of explicit sort steps. |
| `enable_tidscan` | [17](../parameters-query-tuning-planner-method-configuration.md#enable_tidscan) | Enables the planner's use of TID scan plans. |

### Replication / Master Server

| Name | Versions | Description |
| --- | --- | --- |
| `synchronous_standby_names` | [17](../parameters-replication-master-server.md#synchronous_standby_names) | Number of synchronous standbys and list of names of potential synchronous ones. |

### Replication / Sending Servers

| Name | Versions | Description |
| --- | --- | --- |
| `max_replication_slots` | [17](../parameters-replication-sending-servers.md#max_replication_slots) | Sets the maximum number of simultaneously defined replication slots. |
| `max_slot_wal_keep_size` | [17](../parameters-replication-sending-servers.md#max_slot_wal_keep_size) | Sets the maximum WAL size that can be reserved by replication slots. Replication slots will be marked as failed, and segments released for deletion or recycling, if this much space is occupied by WAL on disk. |
| `max_wal_senders` | [17](../parameters-replication-sending-servers.md#max_wal_senders) | Sets the maximum number of simultaneously running WAL sender processes. |
| `track_commit_timestamp` | [17](../parameters-replication-sending-servers.md#track_commit_timestamp) | Collects transaction commit time. |
| `wal_keep_size` | [17](../parameters-replication-sending-servers.md#wal_keep_size) | Sets the size of WAL files held for standby servers. |
| `wal_sender_timeout` | [17](../parameters-replication-sending-servers.md#wal_sender_timeout) | Sets the maximum time to wait for WAL replication. |

### Replication / Standby Servers

| Name | Versions | Description |
| --- | --- | --- |
| `hot_standby` | [17](../parameters-replication-standby-servers.md#hot_standby) | Allows connections and queries during recovery. |
| `hot_standby_feedback` | [17](../parameters-replication-standby-servers.md#hot_standby_feedback) | Allows feedback from a hot standby to the primary that will avoid query conflicts. |
| `max_standby_archive_delay` | [17](../parameters-replication-standby-servers.md#max_standby_archive_delay) | Sets the maximum delay before canceling queries when a hot standby server is processing archived WAL data. |
| `max_standby_streaming_delay` | [17](../parameters-replication-standby-servers.md#max_standby_streaming_delay) | Sets the maximum delay before canceling queries when a hot standby server is processing streamed WAL data. |
| `primary_conninfo` | [17](../parameters-replication-standby-servers.md#primary_conninfo) | Sets the connection string to be used to connect to the sending server. |
| `primary_slot_name` | [17](../parameters-replication-standby-servers.md#primary_slot_name) | Sets the name of the replication slot to use on the sending server. |
| `recovery_min_apply_delay` | [17](../parameters-replication-standby-servers.md#recovery_min_apply_delay) | Sets the minimum delay for applying changes during recovery. |
| `synchronized_standby_slots` | [17](../parameters-replication-standby-servers.md#synchronized_standby_slots) | Lists streaming replication standby server replication slot names that logical WAL sender processes will wait for. Logical WAL sender processes will send decoded changes to output plugins only after the specified replication slots have confirmed receiving WAL. |
| `sync_replication_slots` | [17](../parameters-replication-standby-servers.md#sync_replication_slots) | Enables a physical standby to synchronize logical failover replication slots from the primary server. |
| `wal_receiver_create_temp_slot` | [17](../parameters-replication-standby-servers.md#wal_receiver_create_temp_slot) | Sets whether a WAL receiver should create a temporary replication slot if no permanent slot is configured. |
| `wal_receiver_status_interval` | [17](../parameters-replication-standby-servers.md#wal_receiver_status_interval) | Sets the maximum interval between WAL receiver status reports to the sending server. |
| `wal_receiver_timeout` | [17](../parameters-replication-standby-servers.md#wal_receiver_timeout) | Sets the maximum wait time to receive data from the sending server. |
| `wal_retrieve_retry_interval` | [17](../parameters-replication-standby-servers.md#wal_retrieve_retry_interval) | Sets the time to wait before retrying to retrieve WAL after a failed attempt. |

### Replication / Subscribers

| Name | Versions | Description |
| --- | --- | --- |
| `max_logical_replication_workers` | [17](../parameters-replication-subscribers.md#max_logical_replication_workers) | Maximum number of logical replication worker processes. |
| `max_parallel_apply_workers_per_subscription` | [17](../parameters-replication-subscribers.md#max_parallel_apply_workers_per_subscription) | Maximum number of parallel apply workers per subscription. |
| `max_sync_workers_per_subscription` | [17](../parameters-replication-subscribers.md#max_sync_workers_per_subscription) | Maximum number of table synchronization workers per subscription. |

### Reporting and Logging / What to Log

| Name | Versions | Description |
| --- | --- | --- |
| `application_name` | [17](../parameters-reporting-logging-what-log.md#application_name) | Sets the application name to be reported in statistics and logs. |
| `debug_pretty_print` | [17](../parameters-reporting-logging-what-log.md#debug_pretty_print) | Indents parse and plan tree displays. |
| `debug_print_parse` | [17](../parameters-reporting-logging-what-log.md#debug_print_parse) | Logs each query's parse tree. |
| `debug_print_plan` | [17](../parameters-reporting-logging-what-log.md#debug_print_plan) | Logs each query's execution plan. |
| `debug_print_rewritten` | [17](../parameters-reporting-logging-what-log.md#debug_print_rewritten) | Logs each query's rewritten parse tree. |
| `log_autovacuum_min_duration` | [17](../parameters-reporting-logging-what-log.md#log_autovacuum_min_duration) | Sets the minimum execution time above which autovacuum actions will be logged. Zero prints all actions. -1 turns autovacuum logging off. |
| `log_checkpoints` | [17](../parameters-reporting-logging-what-log.md#log_checkpoints) | Logs each checkpoint. |
| `log_connections` | [17](../parameters-reporting-logging-what-log.md#log_connections) | Logs each successful connection. |
| `log_disconnections` | [17](../parameters-reporting-logging-what-log.md#log_disconnections) | Logs end of a session, including duration. |
| `log_duration` | [17](../parameters-reporting-logging-what-log.md#log_duration) | Logs the duration of each completed SQL statement. |
| `log_error_verbosity` | [17](../parameters-reporting-logging-what-log.md#log_error_verbosity) | Sets the verbosity of logged messages. |
| `log_hostname` | [17](../parameters-reporting-logging-what-log.md#log_hostname) | Logs the host name in the connection logs. By default, connection logs only show the IP address of the connecting host. If you want them to show the host name you can turn this on, but depending on your host name resolution setup it might impose a non-negligible performance penalty. |
| `log_line_prefix` | [17](../parameters-reporting-logging-what-log.md#log_line_prefix) | Controls information prefixed to each log line. If blank, no prefix is used. |
| `log_lock_waits` | [17](../parameters-reporting-logging-what-log.md#log_lock_waits) | Logs long lock waits. |
| `log_parameter_max_length` | [17](../parameters-reporting-logging-what-log.md#log_parameter_max_length) | Sets the maximum length in bytes of data logged for bind parameter values when logging statements. -1 to print values in full. |
| `log_parameter_max_length_on_error` | [17](../parameters-reporting-logging-what-log.md#log_parameter_max_length_on_error) | Sets the maximum length in bytes of data logged for bind parameter values when logging statements, on error. -1 to print values in full. |
| `log_recovery_conflict_waits` | [17](../parameters-reporting-logging-what-log.md#log_recovery_conflict_waits) | Logs standby recovery conflict waits. |
| `log_replication_commands` | [17](../parameters-reporting-logging-what-log.md#log_replication_commands) | Logs each replication command. |
| `log_statement` | [17](../parameters-reporting-logging-what-log.md#log_statement) | Sets the type of statements logged. |
| `log_temp_files` | [17](../parameters-reporting-logging-what-log.md#log_temp_files) | Log the use of temporary files larger than this number of kilobytes. Zero logs all files. The default is -1 (turning this feature off). |
| `log_timezone` | [17](../parameters-reporting-logging-what-log.md#log_timezone) | Sets the time zone to use in log messages. |

### Reporting and Logging / When to Log

| Name | Versions | Description |
| --- | --- | --- |
| `log_min_duration_sample` | [17](../parameters-reporting-logging-when-log.md#log_min_duration_sample) | Sets the minimum execution time above which a sample of statements will be logged. Sampling is determined by log_statement_sample_rate. Zero logs a sample of all queries. -1 turns this feature off. |
| `log_min_duration_statement` | [17](../parameters-reporting-logging-when-log.md#log_min_duration_statement) | Sets the minimum execution time above which all statements will be logged. Zero prints all queries. -1 turns this feature off. |
| `log_min_error_statement` | [17](../parameters-reporting-logging-when-log.md#log_min_error_statement) | Causes all statements generating error at or above this level to be logged. Each level includes all the levels that follow it. The later the level, the fewer messages are sent. |
| `log_min_messages` | [17](../parameters-reporting-logging-when-log.md#log_min_messages) | Sets the message levels that are logged. Each level includes all the levels that follow it. The later the level, the fewer messages are sent. |
| `log_startup_progress_interval` | [17](../parameters-reporting-logging-when-log.md#log_startup_progress_interval) | Time between progress updates for long-running startup operations. 0 turns this feature off. |
| `log_statement_sample_rate` | [17](../parameters-reporting-logging-when-log.md#log_statement_sample_rate) | Fraction of statements exceeding \"log_min_duration_sample\" to be logged. Use a value between 0.0 (never log) and 1.0 (always log). |
| `log_transaction_sample_rate` | [17](../parameters-reporting-logging-when-log.md#log_transaction_sample_rate) | Sets the fraction of transactions from which to log all statements. Use a value between 0.0 (never log) and 1.0 (log all statements for all transactions). |

### Reporting and Logging / Where to Log

| Name | Versions | Description |
| --- | --- | --- |
| `event_source` | [17](../parameters-reporting-logging-where-log.md#event_source) | Sets the application name used to identify PostgreSQL messages in the event log. |
| `log_destination` | [17](../parameters-reporting-logging-where-log.md#log_destination) | Sets the destination for server log output. Valid values are combinations of \"stderr\", \"syslog\", \"csvlog\", \"jsonlog\", and \"eventlog\", depending on the platform. |
| `log_directory` | [17](../parameters-reporting-logging-where-log.md#log_directory) | Sets the destination directory for log files. Can be specified as relative to the data directory or as absolute path. |
| `log_file_mode` | [17](../parameters-reporting-logging-where-log.md#log_file_mode) | Sets the file permissions for log files. The parameter value is expected to be a numeric mode specification in the form accepted by the chmod and umask system calls. (To use the customary octal format the number must start with a 0 (zero).). |
| `log_filename` | [17](../parameters-reporting-logging-where-log.md#log_filename) | Sets the file name pattern for log files. |
| `logging_collector` | [17](../parameters-reporting-logging-where-log.md#logging_collector) | Start a subprocess to capture stderr, csvlog and/or jsonlog into log files. |
| `log_rotation_age` | [17](../parameters-reporting-logging-where-log.md#log_rotation_age) | Sets the amount of time to wait before forcing log file rotation. |
| `log_rotation_size` | [17](../parameters-reporting-logging-where-log.md#log_rotation_size) | Sets the maximum size a log file can reach before being rotated. |
| `log_truncate_on_rotation` | [17](../parameters-reporting-logging-where-log.md#log_truncate_on_rotation) | Truncate existing log files of same name during log rotation. |
| `syslog_facility` | [17](../parameters-reporting-logging-where-log.md#syslog_facility) | Sets the syslog \"facility\" to be used when syslog enabled. |
| `syslog_ident` | [17](../parameters-reporting-logging-where-log.md#syslog_ident) | Sets the program name used to identify PostgreSQL messages in syslog. |
| `syslog_sequence_numbers` | [17](../parameters-reporting-logging-where-log.md#syslog_sequence_numbers) | Add sequence number to syslog messages to avoid duplicate suppression. |
| `syslog_split_messages` | [17](../parameters-reporting-logging-where-log.md#syslog_split_messages) | Split messages sent to syslog by lines and to fit into 1024 bytes. |

### Resource Usage / Asynchronous Behavior

| Name | Versions | Description |
| --- | --- | --- |
| `backend_flush_after` | [17](../parameters-resource-usage-asynchronous-behavior.md#backend_flush_after) | Number of pages after which previously performed writes are flushed to disk. |
| `effective_io_concurrency` | [17](../parameters-resource-usage-asynchronous-behavior.md#effective_io_concurrency) | Number of simultaneous requests that can be handled efficiently by the disk subsystem. |
| `maintenance_io_concurrency` | [17](../parameters-resource-usage-asynchronous-behavior.md#maintenance_io_concurrency) | A variant of \"effective_io_concurrency\" that is used for maintenance work. |
| `max_notify_queue_pages` | [17](../parameters-resource-usage-asynchronous-behavior.md#max_notify_queue_pages) | Sets the maximum number of allocated pages for NOTIFY / LISTEN queue. |
| `max_parallel_maintenance_workers` | [17](../parameters-resource-usage-asynchronous-behavior.md#max_parallel_maintenance_workers) | Sets the maximum number of parallel processes per maintenance operation. |
| `max_parallel_workers` | [17](../parameters-resource-usage-asynchronous-behavior.md#max_parallel_workers) | Sets the maximum number of parallel workers that can be active at one time. |
| `max_parallel_workers_per_gather` | [17](../parameters-resource-usage-asynchronous-behavior.md#max_parallel_workers_per_gather) | Sets the maximum number of parallel processes per executor node. |
| `max_worker_processes` | [17](../parameters-resource-usage-asynchronous-behavior.md#max_worker_processes) | Maximum number of concurrent worker processes. |
| `parallel_leader_participation` | [17](../parameters-resource-usage-asynchronous-behavior.md#parallel_leader_participation) | Controls whether Gather and Gather Merge also run subplans. Should gather nodes also run subplans or just gather tuples?. |

### Resource Usage / Background Writer

| Name | Versions | Description |
| --- | --- | --- |
| `bgwriter_delay` | [17](../parameters-resource-usage-background-writer.md#bgwriter_delay) | Background writer sleep time between rounds. |
| `bgwriter_flush_after` | [17](../parameters-resource-usage-background-writer.md#bgwriter_flush_after) | Number of pages after which previously performed writes are flushed to disk. |
| `bgwriter_lru_maxpages` | [17](../parameters-resource-usage-background-writer.md#bgwriter_lru_maxpages) | Background writer maximum number of LRU pages to flush per round. |
| `bgwriter_lru_multiplier` | [17](../parameters-resource-usage-background-writer.md#bgwriter_lru_multiplier) | Multiple of the average buffer usage to free per round. |

### Resource Usage / Cost-Based Vacuum Delay

| Name | Versions | Description |
| --- | --- | --- |
| `vacuum_cost_delay` | [17](../parameters-resource-usage-cost-based-vacuum-delay.md#vacuum_cost_delay) | Vacuum cost delay in milliseconds. |
| `vacuum_cost_limit` | [17](../parameters-resource-usage-cost-based-vacuum-delay.md#vacuum_cost_limit) | Vacuum cost amount available before napping. |
| `vacuum_cost_page_dirty` | [17](../parameters-resource-usage-cost-based-vacuum-delay.md#vacuum_cost_page_dirty) | Vacuum cost for a page dirtied by vacuum. |
| `vacuum_cost_page_hit` | [17](../parameters-resource-usage-cost-based-vacuum-delay.md#vacuum_cost_page_hit) | Vacuum cost for a page found in the buffer cache. |
| `vacuum_cost_page_miss` | [17](../parameters-resource-usage-cost-based-vacuum-delay.md#vacuum_cost_page_miss) | Vacuum cost for a page not found in the buffer cache. |

### Resource Usage / Disk

| Name | Versions | Description |
| --- | --- | --- |
| `temp_file_limit` | [17](../parameters-resource-usage-disk.md#temp_file_limit) | Limits the total size of all temporary files used by each process. -1 means no limit. |

### Resource Usage / Kernel Resources

| Name | Versions | Description |
| --- | --- | --- |
| `max_files_per_process` | [17](../parameters-resource-usage-kernel-resources.md#max_files_per_process) | Sets the maximum number of simultaneously open files for each server process. |

### Resource Usage / Memory

| Name | Versions | Description |
| --- | --- | --- |
| `autovacuum_work_mem` | [17](../parameters-resource-usage-memory.md#autovacuum_work_mem) | Sets the maximum memory to be used by each autovacuum worker process. |
| `commit_timestamp_buffers` | [17](../parameters-resource-usage-memory.md#commit_timestamp_buffers) | Sets the size of the dedicated buffer pool used for the commit timestamp cache. Specify 0 to have this value determined as a fraction of shared_buffers. |
| `dynamic_shared_memory_type` | [17](../parameters-resource-usage-memory.md#dynamic_shared_memory_type) | Selects the dynamic shared memory implementation used. |
| `hash_mem_multiplier` | [17](../parameters-resource-usage-memory.md#hash_mem_multiplier) | Multiple of \"work_mem\" to use for hash tables. |
| `huge_pages` | [17](../parameters-resource-usage-memory.md#huge_pages) | Use of huge pages on Linux or Windows. |
| `huge_page_size` | [17](../parameters-resource-usage-memory.md#huge_page_size) | The size of huge page that should be requested. |
| `io_combine_limit` | [17](../parameters-resource-usage-memory.md#io_combine_limit) | Limit on the size of data reads and writes. |
| `logical_decoding_work_mem` | [17](../parameters-resource-usage-memory.md#logical_decoding_work_mem) | Sets the maximum memory to be used for logical decoding. This much memory can be used by each internal reorder buffer before spilling to disk. |
| `maintenance_work_mem` | [17](../parameters-resource-usage-memory.md#maintenance_work_mem) | Sets the maximum memory to be used for maintenance operations. This includes operations such as VACUUM and CREATE INDEX. |
| `max_prepared_transactions` | [17](../parameters-resource-usage-memory.md#max_prepared_transactions) | Sets the maximum number of simultaneously prepared transactions. |
| `max_stack_depth` | [17](../parameters-resource-usage-memory.md#max_stack_depth) | Sets the maximum stack depth, in kilobytes. |
| `min_dynamic_shared_memory` | [17](../parameters-resource-usage-memory.md#min_dynamic_shared_memory) | Amount of dynamic shared memory reserved at startup. |
| `multixact_member_buffers` | [17](../parameters-resource-usage-memory.md#multixact_member_buffers) | Sets the size of the dedicated buffer pool used for the MultiXact member cache. |
| `multixact_offset_buffers` | [17](../parameters-resource-usage-memory.md#multixact_offset_buffers) | Sets the size of the dedicated buffer pool used for the MultiXact offset cache. |
| `notify_buffers` | [17](../parameters-resource-usage-memory.md#notify_buffers) | Sets the size of the dedicated buffer pool used for the LISTEN/NOTIFY message cache. |
| `serializable_buffers` | [17](../parameters-resource-usage-memory.md#serializable_buffers) | Sets the size of the dedicated buffer pool used for the serializable transaction cache. |
| `shared_buffers` | [17](../parameters-resource-usage-memory.md#shared_buffers) | Sets the number of shared memory buffers used by the server. |
| `shared_memory_type` | [17](../parameters-resource-usage-memory.md#shared_memory_type) | Selects the shared memory implementation used for the main shared memory region. |
| `subtransaction_buffers` | [17](../parameters-resource-usage-memory.md#subtransaction_buffers) | Sets the size of the dedicated buffer pool used for the subtransaction cache. Specify 0 to have this value determined as a fraction of shared_buffers. |
| `temp_buffers` | [17](../parameters-resource-usage-memory.md#temp_buffers) | Sets the maximum number of temporary buffers used by each session. |
| `transaction_buffers` | [17](../parameters-resource-usage-memory.md#transaction_buffers) | Sets the size of the dedicated buffer pool used for the transaction status cache. Specify 0 to have this value determined as a fraction of shared_buffers. |
| `vacuum_buffer_usage_limit` | [17](../parameters-resource-usage-memory.md#vacuum_buffer_usage_limit) | Sets the buffer pool size for VACUUM, ANALYZE, and autovacuum. |
| `work_mem` | [17](../parameters-resource-usage-memory.md#work_mem) | Sets the maximum memory to be used for query workspaces. This much memory can be used by each internal sort operation and hash table before switching to temporary disk files. |

### Statistics / Cumulative Query and Index Statistics

| Name | Versions | Description |
| --- | --- | --- |
| `stats_fetch_consistency` | [17](../parameters-statistics-cumulative-query-index-statistics.md#stats_fetch_consistency) | Sets the consistency of accesses to statistics data. |
| `track_activities` | [17](../parameters-statistics-cumulative-query-index-statistics.md#track_activities) | Collects information about executing commands. Enables the collection of information on the currently executing command of each session, along with the time at which that command began execution. |
| `track_activity_query_size` | [17](../parameters-statistics-cumulative-query-index-statistics.md#track_activity_query_size) | Sets the size reserved for pg_stat_activity.query, in bytes. |
| `track_counts` | [17](../parameters-statistics-cumulative-query-index-statistics.md#track_counts) | Collects statistics on database activity. |
| `track_functions` | [17](../parameters-statistics-cumulative-query-index-statistics.md#track_functions) | Collects function-level statistics on database activity. |
| `track_io_timing` | [17](../parameters-statistics-cumulative-query-index-statistics.md#track_io_timing) | Collects timing statistics for database I/O activity. |
| `track_wal_io_timing` | [17](../parameters-statistics-cumulative-query-index-statistics.md#track_wal_io_timing) | Collects timing statistics for WAL I/O activity. |

### Statistics / Monitoring

| Name | Versions | Description |
| --- | --- | --- |
| `compute_query_id` | [17](../parameters-statistics-monitoring.md#compute_query_id) | Enables in-core computation of query identifiers. |
| `log_executor_stats` | [17](../parameters-statistics-monitoring.md#log_executor_stats) | Writes executor performance statistics to the server log. |
| `log_parser_stats` | [17](../parameters-statistics-monitoring.md#log_parser_stats) | Writes parser performance statistics to the server log. |
| `log_planner_stats` | [17](../parameters-statistics-monitoring.md#log_planner_stats) | Writes planner performance statistics to the server log. |
| `log_statement_stats` | [17](../parameters-statistics-monitoring.md#log_statement_stats) | Writes cumulative performance statistics to the server log. |

### TLS

| Name | Versions | Description |
| --- | --- | --- |
| `require_secure_transport` | [17](../parameters-tls.md#require_secure_transport) | Whether client connections to the server are required to use some form of secure transport. |

### Version and Platform Compatibility / Other Platforms and Clients

| Name | Versions | Description |
| --- | --- | --- |
| `allow_alter_system` | [17](../parameters-version-platform-compatibility-platforms-clients.md#allow_alter_system) | Allows running the ALTER SYSTEM command. Can be set to off for environments where global configuration changes should be made using a different method. |
| `transform_null_equals` | [17](../parameters-version-platform-compatibility-platforms-clients.md#transform_null_equals) | Treats \"expr=NULL\" as \"expr IS NULL\". When turned on, expressions of the form expr = NULL (or NULL = expr) are treated as expr IS NULL, that is, they return true if expr evaluates to the null value, and false otherwise. The correct behavior of expr = NULL is to always return null (unknown). |

### Version and Platform Compatibility / Previous PostgreSQL Versions

| Name | Versions | Description |
| --- | --- | --- |
| `array_nulls` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#array_nulls) | Enable input of NULL elements in arrays. When turned on, unquoted NULL in an array input value means a null value; otherwise it's taken literally. |
| `backslash_quote` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#backslash_quote) | Sets whether \"\\'\" is allowed in string literals. |
| `escape_string_warning` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#escape_string_warning) | Warn about backslash escapes in ordinary string literals. |
| `lo_compat_privileges` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#lo_compat_privileges) | Enables backward compatibility mode for privilege checks on large objects. Skips privilege checks when reading or modifying large objects, for compatibility with PostgreSQL releases prior to 9.0. |
| `quote_all_identifiers` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#quote_all_identifiers) | When generating SQL fragments, quote all identifiers. |
| `standard_conforming_strings` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#standard_conforming_strings) | Causes '...' strings to treat backslashes literally. |
| `synchronize_seqscans` | [17](../parameters-version-platform-compatibility-postgresql-versions.md#synchronize_seqscans) | Enable synchronized sequential scans. |

### Write-Ahead Log / Archive Recovery

| Name | Versions | Description |
| --- | --- | --- |
| `archive_cleanup_command` | [17](../parameters-write-ahead-log-archive-recovery.md#archive_cleanup_command) | Sets the shell command that will be executed at every restart point. |
| `recovery_end_command` | [17](../parameters-write-ahead-log-archive-recovery.md#recovery_end_command) | Sets the shell command that will be executed once at the end of recovery. |
| `restore_command` | [17](../parameters-write-ahead-log-archive-recovery.md#restore_command) | Sets the shell command that will be called to retrieve an archived WAL file. |

### Write-Ahead Log / Archiving

| Name | Versions | Description |
| --- | --- | --- |
| `archive_command` | [17](../parameters-write-ahead-log-archiving.md#archive_command) | Sets the shell command that will be called to archive a WAL file. This is used only if \"archive_library\" isn't set. |
| `archive_library` | [17](../parameters-write-ahead-log-archiving.md#archive_library) | Sets the library that will be called to archive a WAL file. An empty string indicates that \"archive_command\" should be used. |
| `archive_mode` | [17](../parameters-write-ahead-log-archiving.md#archive_mode) | Allows archiving of WAL files using \"archive_command\". |
| `archive_timeout` | [17](../parameters-write-ahead-log-archiving.md#archive_timeout) | Sets the amount of time to wait before forcing a switch to the next WAL file. |

### Write-Ahead Log / Checkpoints

| Name | Versions | Description |
| --- | --- | --- |
| `checkpoint_completion_target` | [17](../parameters-write-ahead-log-checkpoints.md#checkpoint_completion_target) | Time spent flushing dirty buffers during checkpoint, as fraction of checkpoint interval. |
| `checkpoint_flush_after` | [17](../parameters-write-ahead-log-checkpoints.md#checkpoint_flush_after) | Number of pages after which previously performed writes are flushed to disk. |
| `checkpoint_timeout` | [17](../parameters-write-ahead-log-checkpoints.md#checkpoint_timeout) | Sets the maximum time between automatic WAL checkpoints. |
| `checkpoint_warning` | [17](../parameters-write-ahead-log-checkpoints.md#checkpoint_warning) | Sets the maximum time before warning if checkpoints triggered by WAL volume happen too frequently. Write a message to the server log if checkpoints caused by the filling of WAL segment files happen more frequently than this amount of time. Zero turns off the warning. |
| `max_wal_size` | [17](../parameters-write-ahead-log-checkpoints.md#max_wal_size) | Sets the WAL size that triggers a checkpoint. |
| `min_wal_size` | [17](../parameters-write-ahead-log-checkpoints.md#min_wal_size) | Sets the minimum size to shrink the WAL to. |

### Write-Ahead Log / Recovery

| Name | Versions | Description |
| --- | --- | --- |
| `recovery_prefetch` | [17](../parameters-write-ahead-log-recovery.md#recovery_prefetch) | Prefetch referenced blocks during recovery. Look ahead in the WAL to find references to uncached data. |
| `wal_decode_buffer_size` | [17](../parameters-write-ahead-log-recovery.md#wal_decode_buffer_size) | Buffer size for reading ahead in the WAL during recovery. Maximum distance to read ahead in the WAL to prefetch referenced data blocks. |

### Write-Ahead Log / Recovery Target

| Name | Versions | Description |
| --- | --- | --- |
| `recovery_target` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target) | Set to \"immediate\" to end recovery as soon as a consistent state is reached. |
| `recovery_target_action` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_action) | Sets the action to perform upon reaching the recovery target. |
| `recovery_target_inclusive` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_inclusive) | Sets whether to include or exclude transaction with recovery target. |
| `recovery_target_lsn` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_lsn) | Sets the LSN of the write-ahead log location up to which recovery will proceed. |
| `recovery_target_name` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_name) | Sets the named restore point up to which recovery will proceed. |
| `recovery_target_time` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_time) | Sets the time stamp up to which recovery will proceed. |
| `recovery_target_timeline` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_timeline) | Specifies the timeline to recover into. |
| `recovery_target_xid` | [17](../parameters-write-ahead-log-recovery-target.md#recovery_target_xid) | Sets the transaction ID up to which recovery will proceed. |
| `summarize_wal` | [17](../parameters-write-ahead-log-recovery-target.md#summarize_wal) | Starts the WAL summarizer process to enable incremental backup. |

### Write-Ahead Log / Settings

| Name | Versions | Description |
| --- | --- | --- |
| `commit_delay` | [17](../parameters-write-ahead-log-settings.md#commit_delay) | Sets the delay in microseconds between transaction commit and flushing WAL to disk. |
| `commit_siblings` | [17](../parameters-write-ahead-log-settings.md#commit_siblings) | Sets the minimum number of concurrent open transactions required before performing \"commit_delay\". |
| `fsync` | [17](../parameters-write-ahead-log-settings.md#fsync) | Forces synchronization of updates to disk. The server will use the fsync() system call in several places to make sure that updates are physically written to disk. This ensures that a database cluster will recover to a consistent state after an operating system or hardware crash. |
| `full_page_writes` | [17](../parameters-write-ahead-log-settings.md#full_page_writes) | Writes full pages to WAL when first modified after a checkpoint. A page write in process during an operating system crash might be only partially written to disk. During recovery, the row changes stored in WAL aren't enough to recover. This option writes pages when first modified after a checkpoint to WAL so full recovery is possible. |
| `synchronous_commit` | [17](../parameters-write-ahead-log-settings.md#synchronous_commit) | Sets the current transaction's synchronization level. |
| `wal_buffers` | [17](../parameters-write-ahead-log-settings.md#wal_buffers) | Sets the number of disk-page buffers in shared memory for WAL. Specify -1 to have this value determined as a fraction of shared_buffers. |
| `wal_compression` | [17](../parameters-write-ahead-log-settings.md#wal_compression) | Compresses full-page writes written in WAL file. |
| `wal_init_zero` | [17](../parameters-write-ahead-log-settings.md#wal_init_zero) | Writes zeroes to new WAL files before first use. |
| `wal_level` | [17](../parameters-write-ahead-log-settings.md#wal_level) | Sets the level of information written to the WAL. |
| `wal_log_hints` | [17](../parameters-write-ahead-log-settings.md#wal_log_hints) | Writes full pages to WAL when first modified after a checkpoint, even for a non-critical modification. |
| `wal_recycle` | [17](../parameters-write-ahead-log-settings.md#wal_recycle) | Recycles WAL files by renaming them. |
| `wal_skip_threshold` | [17](../parameters-write-ahead-log-settings.md#wal_skip_threshold) | Minimum size of new file to fsync instead of writing WAL. |
| `wal_summary_keep_time` | [17](../parameters-write-ahead-log-settings.md#wal_summary_keep_time) | Time for which WAL summary files should be kept. |
| `wal_sync_method` | [17](../parameters-write-ahead-log-settings.md#wal_sync_method) | Selects the method used for forcing WAL updates to disk. |
| `wal_writer_delay` | [17](../parameters-write-ahead-log-settings.md#wal_writer_delay) | Time between WAL flushes performed in the WAL writer. |
| `wal_writer_flush_after` | [17](../parameters-write-ahead-log-settings.md#wal_writer_flush_after) | Amount of WAL written out by WAL writer that triggers a flush. |
