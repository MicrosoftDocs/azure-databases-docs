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
### bytea_output

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the output format for values of type bytea. Valid values are hex (the default) and escape (the traditional PostgreSQL format). |
| Data type | enumeration |
| Default value | `hex` |
| Allowed values | `escape,hex` |
| Parameter type | dynamic |
| Documentation | [bytea_output](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-BYTEA-OUTPUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### check_function_bodies

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Checks function bodies during CREATE FUNCTION. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [check_function_bodies](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-CHECK-FUNCTION-BODIES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### client_min_messages

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Controls the message levels that are sent to the client. |
| Data type | enumeration |
| Default value | `notice` |
| Allowed values | `debug5,debug4,debug3,debug2,debug1,log,notice,warning,error` |
| Parameter type | dynamic |
| Documentation | [client_min_messages](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-CLIENT-MIN-MESSAGES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_table_access_method

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the default table access method for new tables. |
| Data type | string |
| Default value | `heap` |
| Allowed values | `heap` |
| Parameter type | read-only |
| Documentation | [default_table_access_method](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TABLE-ACCESS-METHOD) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_tablespace

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the default tablespace to create tables and indexes in. |
| Data type | string |
| Default value | |
| Allowed values | `[A-Za-z._]*` |
| Parameter type | dynamic |
| Documentation | [default_tablespace](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TABLESPACE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_toast_compression

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the default compression method for compressible values. |
| Data type | enumeration |
| Default value | `pglz` |
| Allowed values | `pglz` |
| Parameter type | read-only |
| Documentation | [default_toast_compression](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TOAST-COMPRESSION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_transaction_deferrable

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | This parameter controls the default deferrable status of each new transaction. It has no effect on read-write transactions or those operating at isolation levels lower than serializable. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [default_transaction_deferrable](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-DEFERRABLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_transaction_isolation

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | This parameter controls the default isolation level of each new transaction. The default is 'read committed'. |
| Data type | enumeration |
| Default value | `read committed` |
| Allowed values | `serializable,repeatable read,read committed,read uncommitted` |
| Parameter type | dynamic |
| Documentation | [default_transaction_isolation](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-ISOLATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### default_transaction_read_only

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the default read-only status of each new transaction. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [default_transaction_read_only](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### gin_pending_list_limit

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the maximum size of the pending list for GIN index. |
| Data type | integer |
| Default value | `4096` |
| Allowed values | `64-2097151` |
| Parameter type | dynamic |
| Documentation | [gin_pending_list_limit](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-GIN-PENDING-LIST-LIMIT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### idle_in_transaction_session_timeout

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the maximum allowed duration of any idling transaction. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [idle_in_transaction_session_timeout](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### idle_session_timeout

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the maximum allowed idle time between queries, when not in a transaction. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [idle_session_timeout](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-IDLE-SESSION-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### lock_timeout

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the maximum allowed duration (in milliseconds) of any wait for a lock. 0 turns this off. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [lock_timeout](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-LOCK-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### row_security

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Enables row security. |
| Data type | boolean |
| Default value | `on` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### search_path

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the schema search order for names that are not schema-qualified. |
| Data type | string |
| Default value | `\"$user\", public` |
| Allowed values | `[A-Za-z0-9.\"$,_ -]+` |
| Parameter type | dynamic |
| Documentation | [search_path](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-SEARCH-PATH) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### session_replication_role

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Controls firing of replication-related triggers and rules for the current session. |
| Data type | enumeration |
| Default value | `origin` |
| Allowed values | `origin,replica,local` |
| Parameter type | dynamic |
| Documentation | [session_replication_role](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-SESSION-REPLICATION-ROLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### statement_timeout

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the maximum allowed duration (in milliseconds) of any statement. 0 turns this off. |
| Data type | integer |
| Default value | `0` |
| Allowed values | `0-2147483647` |
| Parameter type | dynamic |
| Documentation | [statement_timeout](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-STATEMENT-TIMEOUT) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### temp_tablespaces

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the default tablespace(s) to use for temporary tables and sort files if not specified in the CREATE command. |
| Data type | string |
| Default value | `temptblspace` |
| Allowed values | `[A-Za-z._]*` |
| Parameter type | dynamic |
| Documentation | [temp_tablespaces](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-TEMP-TABLESPACES) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### transaction_deferrable

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Whether to defer a read-only serializable transaction until it can be executed with no possible serialization failures. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [transaction_deferrable](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-TRANSACTION-DEFERRABLE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### transaction_isolation

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the current transaction's isolation level. |
| Data type | enumeration |
| Default value | `read committed` |
| Allowed values | `read committed` |
| Parameter type | read-only |
| Documentation | [transaction_isolation](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-TRANSACTION-ISOLATION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### transaction_read_only

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets the current transaction's read-only status. |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `off` |
| Parameter type | read-only |
| Documentation | [transaction_read_only](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-TRANSACTION-READ-ONLY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_failsafe_age

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Age at which VACUUM should trigger failsafe to avoid a wraparound outage. |
| Data type | integer |
| Default value | `1600000000` |
| Allowed values | `0-2100000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_failsafe_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-FAILSAFE-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_freeze_min_age

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Specifies the cutoff age (in transactions) that VACUUM should use to decide whether to freeze row versions while scanning a table. |
| Data type | integer |
| Default value | `50000000` |
| Allowed values | `0-1000000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_freeze_min_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-FREEZE-MIN-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_freeze_table_age

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Age at which VACUUM should scan whole table to freeze tuples. |
| Data type | integer |
| Default value | `150000000` |
| Allowed values | `0-2000000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_freeze_table_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-FREEZE-TABLE-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_multixact_failsafe_age

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Multixact age at which VACUUM should trigger failsafe to avoid a wraparound outage. |
| Data type | integer |
| Default value | `1600000000` |
| Allowed values | `0-2100000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_multixact_failsafe_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-FREEZE-TABLE-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_multixact_freeze_min_age

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Specifies the cutoff age (in multixacts) that VACUUM should use to decide whether to replace multixact IDs with a newer transaction ID or multixact ID while scanning a table. |
| Data type | integer |
| Default value | `5000000` |
| Allowed values | `0-1000000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_multixact_freeze_min_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-MULTIXACT-FREEZE-MIN-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### vacuum_multixact_freeze_table_age

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | VACUUM performs a full table scan to freeze rows if the table has reached the age specified by this setting. |
| Data type | integer |
| Default value | `150000000` |
| Allowed values | `0-2000000000` |
| Parameter type | dynamic |
| Documentation | [vacuum_multixact_freeze_table_age](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-VACUUM-MULTIXACT-FREEZE-TABLE-AGE) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### xmlbinary

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets how binary values are to be encoded in XML. |
| Data type | enumeration |
| Default value | `base64` |
| Allowed values | `base64,hex` |
| Parameter type | dynamic |
| Documentation | [xmlbinary](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-XMLBINARY) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### xmloption

| Attribute | Value |
| --- | --- |
| Category | Client Connection Defaults / Statement Behavior |
| Description | Sets whether XML data in implicit parsing and serialization operations is to be considered as documents or content fragments. |
| Data type | enumeration |
| Default value | `content` |
| Allowed values | `content,document` |
| Parameter type | dynamic |
| Documentation | [xmloption](https://www.postgresql.org/docs/14/runtime-config-client.html#GUC-XMLOPTION) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



