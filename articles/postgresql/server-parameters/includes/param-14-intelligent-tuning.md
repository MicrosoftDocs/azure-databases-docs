---
author: nachoalonsoportillo
ms.author: ialonso
ms.reviewer: maghan
ms.date: 02/02/2026
ms.service: azure-database-postgresql
ms.subservice: flexible-server
ms.topic: include
ms.custom: automatically generated
---
### index_tuning.analysis_interval

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
| Description | Minimum number of daily average read operations affecting the table, so that their unused indexes are considered for dropping. |
| Data type | integer |
| Default value | `1000` |
| Allowed values | `0-9999999` |
| Parameter type | dynamic |
| Documentation | [index_tuning.unused_reads_per_table](https://go.microsoft.com/fwlink/?linkid=2274149) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### intelligent_tuning

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
| Description | Enables intelligent tuning |
| Data type | boolean |
| Default value | `off` |
| Allowed values | `on,off` |
| Parameter type | dynamic |
| Documentation | [intelligent_tuning](https://go.microsoft.com/fwlink/?linkid=2274150) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### intelligent_tuning.metric_targets

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
| Description | Specifies which metrics will be adjusted by intelligent tuning. |
| Data type | set |
| Default value | `none` |
| Allowed values | `none,Storage-checkpoint_completion_target,Storage-min_wal_size,Storage-max_wal_size,Storage-bgwriter_delay,tuning-autovacuum,all` |
| Parameter type | dynamic |
| Documentation | [intelligent_tuning.metric_targets](https://go.microsoft.com/fwlink/?linkid=2274150) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



### logfiles.download_enable

| Attribute | Value |
| --- | --- |
| Category | Intelligent Tuning |
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
| Category | Intelligent Tuning |
| Description | Sets the retention period window in days for server logs - after this time data will be deleted. |
| Data type | integer |
| Default value | `3` |
| Allowed values | `1-7` |
| Parameter type | dynamic |
| Documentation | [logfiles.retention_days](https://go.microsoft.com/fwlink/?linkid=2274270) |


[!INCLUDE [server-parameters-azure-notes-void](./server-parameters-azure-notes-void.md)]



